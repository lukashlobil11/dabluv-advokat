#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Převod podkladů spisu na prostý text pro skill adversarial-review.

Podporuje:
  .docx        text včetně rekonstruovaného automatického číslování, tabulek,
               poznámek pod čarou, vysvětlivek a komentářů; hlásí nepřijaté revize
  .xlsx        všechny listy (uložené hodnoty buněk, ne vzorce); hlásí skryté listy
  .pdf         jen evidence s odhadem počtu stran - Claude Code čte PDF nativně (Read)
  .txt / .md   jen evidence - čtou se přímo nástrojem Read

Jen standardní knihovna Pythonu 3.8+, žádné závislosti.

Použití:
  python extrahuj_text.py VSTUP [VSTUP ...] --out ADRESAR [--max-radku N]

VSTUP je soubor nebo adresář (zpracuje se jeho obsah, nerekurzivně). Každý
převedený soubor -> ADRESAR/<původní jméno>.txt, kde jeden řádek = jeden odstavec,
takže číslo řádku slouží jako přesný odkaz do textu. Souhrn -> ADRESAR/_manifest.md.
"""
from __future__ import annotations

import argparse
import datetime as dt
import posixpath
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
S = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"
MC = "{http://schemas.openxmlformats.org/markup-compatibility/2006}"

NEPODPOROVANE = {".doc", ".xls", ".odt", ".ods", ".rtf", ".msg", ".eml", ".zip", ".7z", ".rar"}


def _xml(zf: zipfile.ZipFile, nazev: str):
    try:
        return ET.fromstring(zf.read(nazev))
    except KeyError:
        return None


def _val(el, vychozi):
    return vychozi if el is None else el.get(W + "val", vychozi)


# --------------------------------------------------------------------------- číslování

def _rimske(n: int) -> str:
    hodnoty = ((1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
               (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"))
    vysledek = []
    for hodnota, znak in hodnoty:
        while n >= hodnota:
            vysledek.append(znak)
            n -= hodnota
    return "".join(vysledek)


def _pismena(n: int) -> str:
    # Word čísluje a … z, aa … zz, aaa … (opakuje písmeno, nejde o dvacetišestkovou soustavu)
    if n <= 0:
        return ""
    return chr(ord("a") + (n - 1) % 26) * ((n - 1) // 26 + 1)


def _formatuj(n: int, fmt: str) -> str:
    if fmt == "lowerLetter":
        return _pismena(n)
    if fmt == "upperLetter":
        return _pismena(n).upper()
    if fmt == "lowerRoman":
        return _rimske(n).lower()
    if fmt == "upperRoman":
        return _rimske(n)
    if fmt == "decimalZero":
        return f"{n:02d}"
    if fmt == "bullet":
        return "•"
    if fmt == "none":
        return ""
    return str(n)


class Cislovani:
    """Přibližná rekonstrukce automatického číslování Wordu.

    Bez ní by z textu zmizelo označení bodů (I., 1., a) …), na které se oponentura
    odkazuje. Čítače se vedou pro abstraktní seznam (seznamy se stejným abstractNum
    na sebe navazují); startOverride restartuje úroveň při prvním použití numId.
    Číslování převzaté ze stylu (např. číslované nadpisy) se dohledává ve styles.xml
    včetně dědičnosti basedOn.
    """

    def __init__(self, zf: zipfile.ZipFile) -> None:
        self.urovne = {}   # abstractNumId -> {ilvl: (start, numFmt, lvlText, pStyle)}
        self.seznamy = {}  # numId -> (abstractNumId, {ilvl: startOverride})
        self.styly = {}    # styleId -> (numId, ilvl | None)
        self.citace = {}   # abstractNumId -> [hodnota čítače pro úrovně 0..9]
        self.pouzite = set()
        self._nacti_cislovani(zf)
        self._nacti_styly(zf)

    def _nacti_cislovani(self, zf: zipfile.ZipFile) -> None:
        koren = _xml(zf, "word/numbering.xml")
        if koren is None:
            return
        for an in koren.findall(W + "abstractNum"):
            urovne = {}
            for lvl in an.findall(W + "lvl"):
                urovne[int(lvl.get(W + "ilvl", "0"))] = (
                    int(_val(lvl.find(W + "start"), "1")),
                    _val(lvl.find(W + "numFmt"), "decimal"),
                    _val(lvl.find(W + "lvlText"), ""),
                    _val(lvl.find(W + "pStyle"), None),
                )
            self.urovne[an.get(W + "abstractNumId")] = urovne
        for num in koren.findall(W + "num"):
            prepisy = {}
            for ov in num.findall(W + "lvlOverride"):
                so = ov.find(W + "startOverride")
                if so is not None:
                    prepisy[int(ov.get(W + "ilvl", "0"))] = int(so.get(W + "val", "1"))
            self.seznamy[num.get(W + "numId")] = (_val(num.find(W + "abstractNumId"), None), prepisy)

    def _nacti_styly(self, zf: zipfile.ZipFile) -> None:
        koren = _xml(zf, "word/styles.xml")
        if koren is None:
            return
        prime, rodic = {}, {}
        for st in koren.findall(W + "style"):
            sid = st.get(W + "styleId")
            ppr = st.find(W + "pPr")
            numpr = ppr.find(W + "numPr") if ppr is not None else None
            if numpr is not None:
                il = numpr.find(W + "ilvl")
                prime[sid] = (_val(numpr.find(W + "numId"), None),
                              int(il.get(W + "val")) if il is not None else None)
            zaklad = st.find(W + "basedOn")
            if zaklad is not None:
                rodic[sid] = zaklad.get(W + "val")
        for sid in set(prime) | set(rodic):
            num_id, il, aktualni, hloubka = None, None, sid, 0
            while aktualni and hloubka < 20:
                if aktualni in prime:
                    n, i = prime[aktualni]
                    num_id = n if num_id is None else num_id
                    il = i if il is None else il
                aktualni, hloubka = rodic.get(aktualni), hloubka + 1
            if num_id is not None:
                self.styly[sid] = (num_id, il)

    def predpona(self, p) -> str:
        """Vrátí označení odstavce (např. „II.2. “) a posune čítače; pro nečíslovaný odstavec ""."""
        ppr = p.find(W + "pPr")
        styl = num_id = il = None
        if ppr is not None:
            styl = _val(ppr.find(W + "pStyle"), None)
            numpr = ppr.find(W + "numPr")
            if numpr is not None:
                num_id = _val(numpr.find(W + "numId"), None)
                il_el = numpr.find(W + "ilvl")
                il = int(il_el.get(W + "val")) if il_el is not None else None
        if num_id is None and styl in self.styly:
            num_id, il_stylu = self.styly[styl]
            il = il_stylu if il is None else il
        if not num_id or num_id == "0" or num_id not in self.seznamy:
            return ""
        abstraktni, prepisy = self.seznamy[num_id]
        urovne = self.urovne.get(abstraktni or "")
        if not urovne:
            return ""
        if il is None:
            il = next((k for k, v in urovne.items() if v[3] and v[3] == styl), 0)
        if not 0 <= il < 10:
            return ""
        citace = self.citace.setdefault(abstraktni, [None] * 10)
        if num_id not in self.pouzite:
            self.pouzite.add(num_id)
            for uroven, start in prepisy.items():
                if 0 <= uroven < 10:
                    citace[uroven] = start - 1
                    for hlubsi in range(uroven + 1, 10):
                        citace[hlubsi] = None
        start, fmt, vzor, _ = urovne.get(il, (1, "decimal", "", None))
        citace[il] = start if citace[il] is None else citace[il] + 1
        for hlubsi in range(il + 1, 10):
            citace[hlubsi] = None
        if fmt == "bullet":
            return "• "

        def nahrad(m):
            k = int(m.group(1)) - 1
            if not 0 <= k < 10:
                return ""
            st, f, _, _ = urovne.get(k, (1, "decimal", "", None))
            return _formatuj(citace[k] if citace[k] is not None else st, f)

        oznaceni = re.sub(r"%(\d)", nahrad, vzor).strip()
        return f"{oznaceni} " if oznaceni else ""


# --------------------------------------------------------------------------- .docx

def _text_odstavce(p) -> str:
    # Text přesunutý pryč (moveFrom) a náhradní verze objektů (mc:Fallback) by se zdvojily.
    preskocit = set()
    for obal in p.iter():
        if obal.tag in (W + "moveFrom", MC + "Fallback"):
            preskocit.update(id(beh) for beh in obal.iter(W + "r"))
    casti = []
    for beh in p.iter(W + "r"):
        if id(beh) in preskocit:
            continue
        for el in beh:
            tag = el.tag
            if tag == W + "t":
                casti.append(el.text or "")
            elif tag == W + "tab":
                casti.append("\t")
            elif tag in (W + "br", W + "cr"):
                casti.append(" ")
            elif tag == W + "noBreakHyphen":
                casti.append("-")
            elif tag == W + "footnoteReference":
                casti.append(f"[^{el.get(W + 'id')}]")
            elif tag == W + "endnoteReference":
                casti.append(f"[^v{el.get(W + 'id')}]")
    # Smazaný text (w:delText) se nebere - výstup odpovídá stavu po přijetí revizí.
    text = "".join(casti).replace(" ", " ")
    return re.sub(r"[ \t]{2,}", " ", text).strip()


def _bloky(rodic):
    for el in rodic:
        if el.tag in (W + "p", W + "tbl"):
            yield el
        elif el.tag == W + "sdt":
            obsah = el.find(W + "sdtContent")
            if obsah is not None:
                yield from _bloky(obsah)
        elif el.tag in (W + "customXml", W + "smartTag"):
            yield from _bloky(el)


def _radky_tabulky(tbl, cislovani: Cislovani) -> list:
    radky = []
    for tr in tbl.findall(W + "tr"):
        bunky = []
        for tc in tr.findall(W + "tc"):
            texty = []
            for p in tc.iter(W + "p"):
                predpona = cislovani.predpona(p)
                text = _text_odstavce(p)
                if text:
                    texty.append(predpona + text)
            bunky.append(" / ".join(texty).replace("|", "/"))
        if any(bunky):
            radky.append("| " + " | ".join(bunky) + " |")
    return radky


def _poznamky(zf: zipfile.ZipFile, nazev: str, tag: str, znacka: str) -> list:
    koren = _xml(zf, nazev)
    if koren is None:
        return []
    vysledek = []
    for pozn in koren.findall(W + tag):
        if pozn.get(W + "type") in ("separator", "continuationSeparator", "continuationNotice"):
            continue
        text = " ".join(t for t in (_text_odstavce(p) for p in pozn.iter(W + "p")) if t)
        if text:
            vysledek.append(f"[^{znacka}{pozn.get(W + 'id')}]: {text}")
    return vysledek


def _komentare(zf: zipfile.ZipFile) -> list:
    koren = _xml(zf, "word/comments.xml")
    if koren is None:
        return []
    vysledek = []
    for kom in koren.findall(W + "comment"):
        text = " ".join(t for t in (_text_odstavce(p) for p in kom.iter(W + "p")) if t)
        vysledek.append(f"[komentář {kom.get(W + 'id')} – {kom.get(W + 'author', '?')}]: {text}")
    return vysledek


def extrahuj_docx(cesta: Path):
    """Vrátí (řádky, popis rozsahu, upozornění). Používá i vytez_citace.py."""
    with zipfile.ZipFile(cesta) as zf:
        dokument = _xml(zf, "word/document.xml")
        if dokument is None:
            raise ValueError("chybí word/document.xml – nejde o platný .docx")
        telo = dokument.find(W + "body")
        cislovani = Cislovani(zf)
        radky, odstavcu, tabulek = [], 0, 0
        for blok in _bloky(telo if telo is not None else dokument):
            if blok.tag == W + "p":
                predpona = cislovani.predpona(blok)  # čítač se posouvá i u prázdných odstavců
                text = _text_odstavce(blok)
                if text:
                    radky.append(predpona + text)
                    odstavcu += 1
            else:
                tabulek += 1
                radky.extend(_radky_tabulky(blok, cislovani))
        poznamky = (_poznamky(zf, "word/footnotes.xml", "footnote", "")
                    + _poznamky(zf, "word/endnotes.xml", "endnote", "v"))
        komentare = _komentare(zf)
        vlozeno = sum(1 for _ in dokument.iter(W + "ins"))
        smazano = sum(1 for _ in dokument.iter(W + "del"))
    if poznamky:
        radky += ["", "----- POZNÁMKY POD ČAROU A VYSVĚTLIVKY -----"] + poznamky
    if komentare:
        radky += ["", "----- KOMENTÁŘE V DOKUMENTU -----"] + komentare
    upozorneni = []
    if vlozeno or smazano:
        upozorneni.append(f"NEPŘIJATÉ REVIZE (vloženo {vlozeno}×, smazáno {smazano}×) – text zachycen "
                          "ve stavu po přijetí změn; před podáním revize vyřešit")
    if komentare:
        upozorneni.append(f"KOMENTÁŘE V DOKUMENTU: {len(komentare)} – před podáním odstranit")
    return radky, f"{odstavcu} odstavců, {tabulek} tabulek, {len(poznamky)} poznámek", upozorneni


# --------------------------------------------------------------------------- .xlsx

def _sloupec(ref: str) -> int:
    n = 0
    for znak in ref.upper():
        if "A" <= znak <= "Z":
            n = n * 26 + (ord(znak) - 64)
        else:
            break
    return n


def _hodnota(c, sdilene: list) -> str:
    typ = c.get("t")
    if typ == "inlineStr":
        is_ = c.find(S + "is")
        text = "".join(t.text or "" for t in is_.iter(S + "t")) if is_ is not None else ""
    else:
        v = c.find(S + "v")
        if v is None or v.text is None:
            return ""
        text = v.text
        if typ == "s":
            try:
                text = sdilene[int(text)]
            except (ValueError, IndexError):
                pass
        elif typ == "b":
            text = "PRAVDA" if text == "1" else "NEPRAVDA"
    return re.sub(r"\s+", " ", text).strip()


def extrahuj_xlsx(cesta: Path, max_radku: int = 0):
    with zipfile.ZipFile(cesta) as zf:
        sdilene = []
        koren = _xml(zf, "xl/sharedStrings.xml")
        if koren is not None:
            for si in koren.findall(S + "si"):
                casti = []
                for dite in si:  # fonetické přepisy (rPh) vynecháváme
                    if dite.tag == S + "t":
                        casti.append(dite.text or "")
                    elif dite.tag == S + "r":
                        casti.extend(t.text or "" for t in dite.findall(S + "t"))
                sdilene.append("".join(casti))
        sesit = _xml(zf, "xl/workbook.xml")
        if sesit is None:
            raise ValueError("chybí xl/workbook.xml – nejde o platný .xlsx")
        vztahy = _xml(zf, "xl/_rels/workbook.xml.rels")
        cile = {} if vztahy is None else {
            r.get("Id"): r.get("Target", "") for r in vztahy.findall(PKG + "Relationship")}
        radky, celkem, listu, skryte = [], 0, 0, []
        for list_ in sesit.iter(S + "sheet"):
            listu += 1
            nazev = list_.get("name", "?")
            skryty = list_.get("state", "visible") != "visible"
            if skryty:
                skryte.append(nazev)
            cil = cile.get(list_.get(REL + "id"), "")
            cesta_listu = cil.lstrip("/") if cil.startswith("/") else posixpath.normpath(posixpath.join("xl", cil))
            radky.append(f"=== List: {nazev}{' (SKRYTÝ)' if skryty else ''} ===")
            try:
                proud = zf.open(cesta_listu)
            except KeyError:
                radky.append("(list v archivu nenalezen)")
                continue
            pocet = 0
            with proud:
                for _, el in ET.iterparse(proud, events=("end",)):
                    if el.tag != S + "row":
                        continue
                    hodnoty, posledni = {}, 0
                    for c in el.findall(S + "c"):
                        sloupec = _sloupec(c.get("r", "")) or posledni + 1
                        posledni = sloupec
                        hodnota = _hodnota(c, sdilene)
                        if hodnota:
                            hodnoty[sloupec] = hodnota
                    if hodnoty:
                        bunky = [hodnoty.get(i, "") for i in range(1, max(hodnoty) + 1)]
                        radky.append(el.get("r", "?") + "\t" + "\t".join(bunky))
                        pocet += 1
                    el.clear()
                    if max_radku and pocet >= max_radku:
                        radky.append(f"… zkráceno po {max_radku} řádcích (--max-radku)")
                        break
            celkem += pocet
    upozorneni = [f"SKRYTÉ LISTY: {', '.join(skryte)}"] if skryte else []
    return radky, f"{listu} listů, {celkem} neprázdných řádků", upozorneni


# --------------------------------------------------------------------------- ostatní

def _odhad_stran_pdf(cesta: Path):
    try:
        data = cesta.read_bytes()
    except OSError:
        return None
    stran = len(re.findall(rb"/Type\s*/Page(?![a-zA-Z])", data))
    if stran:
        return stran
    pocty = [int(x) for x in re.findall(rb"/Count\s+(\d+)", data)]
    return max(pocty) if pocty else None


def _velikost(n: float) -> str:
    for jednotka in ("B", "kB", "MB"):
        if n < 1024:
            return f"{n:.0f} {jednotka}" if jednotka == "B" else f"{n:.1f} {jednotka}"
        n /= 1024
    return f"{n:.1f} GB"


def _soubory(vstupy):
    for vstup in vstupy:
        p = Path(vstup)
        if p.is_dir():
            yield from sorted(x for x in p.iterdir() if x.is_file() and not x.name.startswith((".", "~$")))
        elif p.is_file():
            yield p
        else:
            print(f"VAROVÁNÍ: {vstup} neexistuje – přeskakuji", file=sys.stderr)


def _zapis_manifest(vystup: Path, zaznamy: list) -> Path:
    radky = [
        "# Manifest podkladů",
        "",
        f"Vygenerováno {dt.datetime.now():%Y-%m-%d %H:%M} skriptem `extrahuj_text.py`. "
        "V převedených .txt odpovídá jeden řádek jednomu odstavci (u tabulek jednomu řádku tabulky).",
        "",
        "| Soubor | Typ | Velikost | Text / jak číst | Rozsah | Upozornění |",
        "|---|---|---|---|---|---|",
    ]
    for z in zaznamy:
        jak_cist = f"`{z['vystup']}`" if z["vystup"].endswith(".txt") else z["vystup"]
        radky.append("| " + " | ".join([f"`{z['soubor']}`", z["typ"], z["velikost"], jak_cist,
                                        z["rozsah"] or "—", "; ".join(z["upozorneni"]) or "—"]) + " |")
    cesta = vystup / "_manifest.md"
    with open(cesta, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(radky) + "\n")
    return cesta


def main(argv=None) -> int:
    for proud in (sys.stdout, sys.stderr):
        if hasattr(proud, "reconfigure"):
            proud.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Převod podkladů spisu (.docx, .xlsx) na prostý text + manifest.")
    parser.add_argument("vstupy", nargs="+", help="soubory nebo adresáře")
    parser.add_argument("--out", required=True, help="výstupní adresář, např. cases/X/oponentura/_podklady")
    parser.add_argument("--max-radku", type=int, default=0,
                        help="max. počet neprázdných řádků na list .xlsx (0 = bez limitu)")
    args = parser.parse_args(argv)

    vystup = Path(args.out)
    vystup.mkdir(parents=True, exist_ok=True)
    zaznamy, pouzite = [], set()
    for soubor in _soubory(args.vstupy):
        pripona = soubor.suffix.lower()
        zaznam = {"soubor": soubor.as_posix(), "typ": pripona.lstrip(".") or "?",
                  "velikost": _velikost(soubor.stat().st_size), "vystup": "", "rozsah": "", "upozorneni": []}
        try:
            if pripona in (".docx", ".xlsx"):
                if pripona == ".docx":
                    radky, rozsah, upozorneni = extrahuj_docx(soubor)
                else:
                    radky, rozsah, upozorneni = extrahuj_xlsx(soubor, args.max_radku)
                jmeno = soubor.name + ".txt"
                if jmeno in pouzite:
                    jmeno = f"{soubor.parent.name}__{jmeno}"
                pouzite.add(jmeno)
                with open(vystup / jmeno, "w", encoding="utf-8", newline="\n") as f:
                    f.write("\n".join(radky) + "\n")
                zaznam.update(vystup=(vystup / jmeno).as_posix(), rozsah=rozsah, upozorneni=upozorneni)
            elif pripona == ".pdf":
                stran = _odhad_stran_pdf(soubor)
                zaznam["rozsah"] = f"~{stran} stran" if stran else "počet stran nezjištěn"
                zaznam["vystup"] = "přímo nástrojem Read (nad 10 stran po rozsazích `pages`)"
            elif pripona in (".txt", ".md"):
                zaznam["vystup"] = "přímo nástrojem Read"
            else:
                zaznam["vystup"] = "NEPŘEVEDENO"
                zaznam["upozorneni"].append("nepodporovaný formát – převeďte na .docx nebo PDF"
                                            if pripona in NEPODPOROVANE else "neznámý formát")
        except (zipfile.BadZipFile, ET.ParseError, ValueError, OSError) as chyba:
            zaznam["vystup"] = "CHYBA"
            zaznam["upozorneni"].append(f"{type(chyba).__name__}: {chyba}")
        zaznamy.append(zaznam)

    manifest = _zapis_manifest(vystup, zaznamy)
    prevedeno = sum(1 for z in zaznamy if z["vystup"].endswith(".txt"))
    print(f"Zpracováno {len(zaznamy)} souborů, převedeno na text {prevedeno}. Manifest: {manifest.as_posix()}")
    for z in zaznamy:
        for u in z["upozorneni"]:
            print(f"  ! {Path(z['soubor']).name}: {u}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
