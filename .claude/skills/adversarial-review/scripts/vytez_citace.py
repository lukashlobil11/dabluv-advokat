#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deterministický rejstřík citací v českém právním textu (skill adversarial-review).

Najde:
  * rozhodnutí ÚOHS (č. j. / sp. zn.), soudů (NSS, krajské soudy, NS, ÚS), SDEU a ECLI
    včetně data uvedeného u citace,
  * ustanovení (§ …, čl. …) a předpis, ke kterému se v textu vztahují,
  * předpisy (zákon / vyhláška / nařízení vlády č. X/RRRR Sb., směrnice a nařízení EU),
  * legislativní zkratky „(dále jen …)“ a jejich použití.

Nic neověřuje ani nedomýšlí - je to vstup pro agenta overovatel-citaci. Navíc označí
formální nesrovnalosti zjistitelné bez internetu: rok nebo datum v budoucnosti, datum
rozhodnutí dřívější než rok spisové značky, různá data u téže citace, chybějící číslo
listu u č. j. soudu, § nad rozsah ZZVZ, citaci zrušeného ZVZ, nepoužitou či
přepsanou legislativní zkratku.

Použití:
  python vytez_citace.py SOUBOR [SOUBOR ...] [--json] [--out CESTA]

SOUBOR: .txt / .md (UTF-8) nebo .docx (převede se stejně jako v extrahuj_text.py,
takže čísla řádků odpovídají jeho výstupu).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

DNES = dt.date.today()
# ZZVZ (zák. č. 134/2016 Sb.) končí § 279 „Účinnost“ (znění účinné 03.04.2025–31.12.2026).
MAX_PARAGRAF_ZZVZ = 279

MESICE = {"ledna": 1, "února": 2, "března": 3, "dubna": 4, "května": 5, "června": 6, "července": 7,
          "srpna": 8, "září": 9, "října": 10, "listopadu": 11, "prosince": 12}
RE_DATUM = re.compile(r"(\d{1,2})\.\s*(?:(\d{1,2})\.|(" + "|".join(MESICE) + r"))\s*(\d{4})")

# --------------------------------------------------------------------------- rozhodnutí

RE_UOHS = re.compile(r"(?<!\w)[ÚU]OHS\s*[-–]\s*([A-Z]?\d{1,6})/(\d{4})((?:/[^\s,;:()\[\]„“\"]+)?)")
RE_UOHS_SPZN = re.compile(r"(?<![\w/-])([SR]\d{3,5})/(\d{4})/(VZ|HS|VS|KD|POV)\b")
REJSTRIKY_NSS = {"As", "Afs", "Ads", "Ans", "Aos", "Aps", "Ars", "Azs", "Ao", "Na", "Nad", "Komp", "Konf"}
REJSTRIKY_KS = {"A", "Ad", "Af", "Az", "Ca", "Cad"}
REJSTRIKY_NS = {"Cdo", "Odo", "Tdo"}
RE_SOUD = re.compile(
    r"(?<![\w/.])(\d{1,3})\s+("
    + "|".join(sorted(REJSTRIKY_NSS | REJSTRIKY_KS | REJSTRIKY_NS, key=len, reverse=True))
    + r")\s+(\d{1,6})\s*/\s*(\d{4})(?:\s*[-–]\s*(\d{1,4}))?(?![\w/])")
RE_US = re.compile(r"(?<![\w.])(Pl\.|IV\.|III\.|II\.|I\.)\s*ÚS(-st\.)?\s*(\d{1,5})/(\d{2,4})(?:\s*[-–]\s*(\d{1,4}))?")
RE_SDEU = re.compile(r"(?<![\w/-])([CTF])\s?[-–‑]\s?(\d{1,4})/(\d{2})(?:\s*(P|PPU|RENV|R))?(?![\w/])")
RE_ECLI = re.compile(r"\bECLI:[A-Z]{2}:[A-Z0-9]{1,7}:\d{4}:[A-Za-z0-9.:]*[A-Za-z0-9]")
RE_SOUD_V_TEXTU = [
    (re.compile(r"Nejvyšší(?:ho|m)?\s+správní(?:ho|m)?\s+soud|\bNSS\b"), "NSS"),
    (re.compile(r"Krajsk(?:ý|ého|ém)\s+soud(?:u|em)?\s+v\s+Brně|\bKS\s+v\s+Brně|\bKSBR\b"), "KS v Brně"),
    (re.compile(r"Krajsk(?:ý|ého|ém)\s+soud|\bKS\b"), "krajský soud"),
    (re.compile(r"Nejvyšší(?:ho|m)?\s+soud(?!\w*\s+správní)|\bNS\b"), "NS"),
    (re.compile(r"Ústavní(?:ho|m)?\s+soud|\bÚS\b"), "ÚS"),
    (re.compile(r"Soudní(?:ho|m)?\s+dv(?:ůr|ora|oře)|\bSDEU\b|\bSD\s?EU\b"), "SDEU"),
]

# --------------------------------------------------------------------------- ustanovení a předpisy

_SPOJKA = r"(?:\s*(?:,|a|až|–|-)\s*)"
RE_PARAGRAF = re.compile(
    r"§§?\s*(\d+)([a-z]?)"
    r"(?:\s*(?:odst\.|odstavc[eiů]|odstavec)\s*\d+[a-z]?(?:" + _SPOJKA + r"\d+[a-z]?)*)?"
    r"(?:\s*(?:písm\.|písmen[oaeu]?)\s*[a-z]{1,2}\)(?:" + _SPOJKA + r"[a-z]{1,2}\))*)?"
    r"(?:\s*bod(?:u|ě|y|ů)?\s*\d+(?:" + _SPOJKA + r"\d+)*)?"
    r"(?:\s*vět(?:a|y|ě|u)\s*(?:první|druhá|druhé|třetí|čtvrtá|čtvrté|poslední|\d+)"
    r"(?:\s*(?:před|za)\s*středníkem)?)?"
    r"(?:\s*(?:až|–)\s*(?:§\s*)?\d+[a-z]?)?")
RE_CLANEK = re.compile(r"(?<!\w)čl\.\s*\d+[a-z]?(?:\s*odst\.\s*\d+)?(?:\s*písm\.\s*[a-z]\))?")
RE_PREDPIS = re.compile(
    r"(?:zákon(?:a|u|em|ě|y|ů)?|zák\.|vyhlášk(?:a|y|u|ou|ách)|vyhl\.|nařízení\s+vlády)\s*č\.\s*(\d{1,4})/(\d{4})\s*Sb\.",
    re.IGNORECASE)
RE_EU = re.compile(
    r"(směrnic\w*|nařízení)\s+(?:Evropského\s+parlamentu\s+a\s+Rady\s+|Komise\s+(?:v\s+přenesené\s+pravomoci\s+)?|Rady\s+)?"
    r"(?:\((EU|ES|EHS|Euratom)\)\s*)?(?:č\.\s*)?(\d{2,4}/\d{1,4}(?:/(?:EU|ES|EHS))?)")
# Pořadí určuje přednost při shodné pozici v textu (s. ř. s. musí předejít s. ř.).
PREDPISY = [
    (re.compile(r"s\.\s*ř\.\s*s\.|soudní(?:ho|m)?\s+řád(?:u|em)?\s+správní(?:ho|m)?|150/2002"), "s. ř. s. (zák. č. 150/2002 Sb.)"),
    (re.compile(r"\bZZVZ\b|zadávání\s+veřejných\s+zakázek|134/2016"), "ZZVZ (zák. č. 134/2016 Sb.)"),
    (re.compile(r"\bZVZ\b|o\s+veřejných\s+zakázkách|137/2006"), "ZVZ (zák. č. 137/2006 Sb., zrušen)"),
    (re.compile(r"správní(?:ho|m)?\s+řád(?:u|em)?|\bSŘ\b|\bs\.\s*ř\.(?!\s*s\.)|500/2004"), "správní řád (zák. č. 500/2004 Sb.)"),
    (re.compile(r"o\.\s*s\.\s*ř\.|občansk(?:ý|ého|ém)\s+soudní(?:ho|m)?\s+řád|99/1963"), "o. s. ř. (zák. č. 99/1963 Sb.)"),
    (re.compile(r"občansk(?:ý|ého|ém)\s+zákoník|\bOZ\b|89/2012"), "OZ (zák. č. 89/2012 Sb.)"),
    (re.compile(r"rozpočtov(?:á|ých)\s+pravid|218/2000"), "rozpočtová pravidla (zák. č. 218/2000 Sb.)"),
    (re.compile(r"finanční\s+kontrol|320/2001"), "zák. o finanční kontrole (č. 320/2001 Sb.)"),
    (re.compile(r"kontrolní(?:ho|m)?\s+řád|255/2012"), "kontrolní řád (zák. č. 255/2012 Sb.)"),
    (re.compile(r"(?:vyhlášk\w*|vyhl\.)\s*č\.\s*(\d{1,4}/\d{4})\s*Sb\."), "vyhl. č. {0} Sb."),
    (re.compile(r"nařízení\s+vlády\s*č\.\s*(\d{1,4}/\d{4})\s*Sb\."), "nař. vl. č. {0} Sb."),
    (re.compile(r"(?:zákon\w*|zák\.)\s*č\.\s*(\d{1,4}/\d{4})\s*Sb\."), "zák. č. {0} Sb."),
    (re.compile(r"Listin\w*\s+základních\s+práv"), "Listina základních práv a svobod"),
    (re.compile(r"\bSFEU\b|Smlouv\w*\s+o\s+fungování"), "SFEU"),
    (re.compile(r"směrnic\w*\s+(?:Evropského\s+parlamentu\s+a\s+Rady\s+)?(\d{4}/\d{1,4}/EU)"), "směrnice {0}"),
]

PREDPISY_CLANKY = [
    (re.compile(r"směrnic\w*\s+(?:Evropského\s+parlamentu\s+a\s+Rady\s+)?(?:\((?:EU|ES)\)\s*)?(?:č\.\s*)?(\d{2,4}/\d{1,4}(?:/(?:EU|ES|EHS))?)"), "směrnice {0}"),
    (re.compile(r"nařízení\s+(?:Evropského\s+parlamentu\s+a\s+Rady\s+|Komise\s+|Rady\s+)?\((?:EU|ES)\)\s*(?:č\.\s*)?(\d{2,4}/\d{1,4})"), "nařízení (EU) {0}"),
    (re.compile(r"Listin\w*\s+základních\s+práv|\bListiny\b"), "Listina základních práv a svobod"),
    (re.compile(r"Ústav\w*\s+(?:České\s+republiky|ČR)|\bÚstavy\b"), "Ústava ČR"),
    (re.compile(r"\bSFEU\b|Smlouv\w*\s+o\s+fungování"), "SFEU"),
    (re.compile(r"\bSEU\b|Smlouv\w*\s+o\s+Evropské\s+unii"), "SEU"),
    (re.compile(r"Úmluv\w*"), "mezinárodní úmluva"),
    (re.compile(r"zadávací\w*\s+dokumentac|ZD|smlouv\w*|obchodních\s+podmín|výzv\w*|dokumentac\w*"),
     "článek dokumentu (ZD, smlouva…), ne předpisu"),
]

RE_ZKRATKA = re.compile(r"\(\s*dále\s+(?:jen|také|též)\s+(?:jako\s+)?[„\"“']([^“”\"']{1,60})[“”\"']")


# --------------------------------------------------------------------------- pomocné

def _nacti_radky(cesta: Path) -> list:
    if cesta.suffix.lower() == ".docx":
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from extrahuj_text import extrahuj_docx  # stejný převod => stejná čísla řádků
        radky, _, _ = extrahuj_docx(cesta)
        return radky
    data = cesta.read_bytes()
    for kodovani in ("utf-8-sig", "cp1250"):
        try:
            return data.decode(kodovani).splitlines()
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace").splitlines()


def _normalizuj(text: str) -> str:
    text = text.replace(" ", " ").replace(" ", " ").replace("‑", "-")
    return re.sub(r"\s+", " ", text).strip()


def _kontext(radek: str, zacatek: int, konec: int, okolo: int = 160) -> str:
    a, b = max(0, zacatek - okolo), min(len(radek), konec + okolo)
    usek = ("…" if a else "") + radek[a:b] + ("…" if b < len(radek) else "")
    return usek.replace("|", "/").replace("`", "'")


def _datum_z_nalezu(m):
    den, mesic = int(m.group(1)), int(m.group(2)) if m.group(2) else MESICE[m.group(3)]
    rok = int(m.group(4))
    text = f"{den}. {mesic}. {rok}"
    try:
        return text, dt.date(rok, mesic, den)
    except ValueError:
        return text, False  # neplatné datum (např. 31. 2.)


def _datum_u(radek: str, zacatek: int, konec: int):
    """Datum citovaného rozhodnutí: za citací („č. j. … ze dne 7. 7. 2023“),
    jinak těsně před ní („ze dne 25. 1. 2011, č. j. …“)."""
    okno = radek[konec:konec + 45]
    m = RE_DATUM.search(okno)
    if m and re.match(r"^[\s,;:(]*(?:ze\s+dne|dne|ze|z)?\s*$", okno[:m.start()]):
        return _datum_z_nalezu(m)
    okno = radek[max(0, zacatek - 60):zacatek]
    for m in reversed(list(RE_DATUM.finditer(okno))):
        if re.match(r"^\s*[,;]?\s*(?:č\.\s*j\.|čj\.|sp\.\s*zn\.)?\s*$", okno[m.end():]):
            return _datum_z_nalezu(m)
        break
    return None, None


ZNAME_PREDPISY = {
    "134/2016": "ZZVZ (zák. č. 134/2016 Sb.)", "137/2006": "ZVZ (zák. č. 137/2006 Sb., zrušen)",
    "500/2004": "správní řád (zák. č. 500/2004 Sb.)", "150/2002": "s. ř. s. (zák. č. 150/2002 Sb.)",
    "99/1963": "o. s. ř. (zák. č. 99/1963 Sb.)", "89/2012": "OZ (zák. č. 89/2012 Sb.)",
    "218/2000": "rozpočtová pravidla (zák. č. 218/2000 Sb.)",
    "320/2001": "zák. o finanční kontrole (č. 320/2001 Sb.)", "255/2012": "kontrolní řád (zák. č. 255/2012 Sb.)",
}


def _popis(m, popis: str) -> str:
    if popis.startswith("zák. č.") and m.group(1) in ZNAME_PREDPISY:
        return ZNAME_PREDPISY[m.group(1)]
    return popis.format(*m.groups()) if m.groups() else popis


def _predpis_u(radek: str, zacatek: int, konec: int, vzory=PREDPISY, vychozi="neurčen (doplní ověřovatel z kontextu)") -> str:
    """Předpis uvedený za citací („§ 36 odst. 3 ZZVZ“), jinak těsně před ní („ZZVZ předpokládá v § 98“)."""
    okno = radek[konec:konec + 140].split(";")[0]
    nejlepsi = None
    for poradi, (vzor, popis) in enumerate(vzory):
        m = vzor.search(okno)
        if m and (nejlepsi is None or (m.start(), poradi) < nejlepsi[0]):
            nejlepsi = ((m.start(), poradi), _popis(m, popis))
    if nejlepsi:
        return nejlepsi[1]
    okno = radek[max(0, zacatek - 80):zacatek].split(";")[-1]
    for poradi, (vzor, popis) in enumerate(vzory):
        nalezy = list(vzor.finditer(okno))
        if nalezy and (nejlepsi is None or (-nalezy[-1].end(), poradi) < nejlepsi[0]):
            m = nalezy[-1]
            nejlepsi = ((-m.end(), poradi), _popis(m, popis))
    return f"{nejlepsi[1]} – uveden před citací" if nejlepsi else vychozi


def _soud_pred(radek: str, zacatek: int, rejstrik: str) -> str:
    okno = radek[max(0, zacatek - 90):zacatek]
    nalezene = [(m.end(), nazev) for vzor, nazev in RE_SOUD_V_TEXTU for m in vzor.finditer(okno)]
    if nalezene:
        return max(nalezene)[1] + " (dle textu)"
    if rejstrik in REJSTRIKY_NSS:
        return "NSS (dle rejstříku)"
    if rejstrik in REJSTRIKY_KS:
        return "krajský soud (dle rejstříku)"
    return "NS (dle rejstříku)"


# --------------------------------------------------------------------------- vytěžení

class Rejstrik:
    def __init__(self) -> None:
        self.polozky = {}  # (skupina, citace) -> položka

    def pridej(self, skupina, typ, citace, soubor, cislo_radku, radek, m, **extra):
        klic = (skupina, citace)
        polozka = self.polozky.get(klic)
        if polozka is None:
            polozka = {"skupina": skupina, "typ": typ, "citace": citace, "vyskyty": [], "data": [],
                       "upozorneni": [], "kontext": _kontext(radek, m.start(), m.end()), **extra}
            self.polozky[klic] = polozka
        misto = f"{soubor}:{cislo_radku}"
        if misto not in polozka["vyskyty"]:
            polozka["vyskyty"].append(misto)
        return polozka

    @staticmethod
    def upozorni(polozka, zprava):
        if zprava not in polozka["upozorneni"]:
            polozka["upozorneni"].append(zprava)


def _kontrola_roku(rej, polozka, rok_znacky, datum):
    if rok_znacky > DNES.year:
        rej.upozorni(polozka, f"⚠ rok {rok_znacky} ve sp. zn./č. j. je v budoucnosti")
    if rok_znacky < 1990:
        rej.upozorni(polozka, f"⚠ nepravděpodobný rok {rok_znacky}")
    if datum is False:
        rej.upozorni(polozka, "⚠ neplatné kalendářní datum")
    elif datum:
        if datum > DNES:
            rej.upozorni(polozka, "⚠ datum rozhodnutí je v budoucnosti")
        if datum.year < rok_znacky:
            rej.upozorni(polozka, "⚠ datum rozhodnutí předchází roku ve sp. zn./č. j. – nemožné")


def _zaznamenej_datum(polozka, text_data):
    if text_data and text_data not in polozka["data"]:
        polozka["data"].append(text_data)


def vytez(soubor: str, radky: list, rej: Rejstrik) -> None:
    for cislo, surovy in enumerate(radky, start=1):
        radek = _normalizuj(surovy)
        if not radek:
            continue
        obsazeno = []

        for m in RE_UOHS.finditer(radek):
            zbytek = m.group(3).rstrip(".")
            citace = f"ÚOHS-{m.group(1)}/{m.group(2)}{zbytek}"
            druh = "sp. zn." if m.group(1)[:1] in "SR" and not re.search(r"/\d{4}/\d+", zbytek) else "č. j."
            p = rej.pridej("R", f"ÚOHS ({druh})", citace, soubor, cislo, radek, m)
            text_data, datum = _datum_u(radek, m.start(), m.end())
            _zaznamenej_datum(p, text_data)
            _kontrola_roku(rej, p, int(m.group(2)), datum)
            obsazeno.append(m.span())
        for m in RE_UOHS_SPZN.finditer(radek):
            if any(a <= m.start() < b for a, b in obsazeno):
                continue
            p = rej.pridej("R", "ÚOHS (sp. zn.)", f"{m.group(1)}/{m.group(2)}/{m.group(3)}", soubor, cislo, radek, m)
            text_data, datum = _datum_u(radek, m.start(), m.end())
            _zaznamenej_datum(p, text_data)
            _kontrola_roku(rej, p, int(m.group(2)), datum)

        for m in RE_SOUD.finditer(radek):
            senat, rejstrik, cislo_vec, rok, list_ = m.groups()
            citace = f"{senat} {rejstrik} {cislo_vec}/{rok}" + (f"-{list_}" if list_ else "")
            p = rej.pridej("R", "soud", citace, soubor, cislo, radek, m,
                           soud=_soud_pred(radek, m.start(), rejstrik))
            text_data, datum = _datum_u(radek, m.start(), m.end())
            _zaznamenej_datum(p, text_data)
            _kontrola_roku(rej, p, int(rok), datum)
            if not list_:
                rej.upozorni(p, "ℹ chybí číslo listu – jde o sp. zn., ne č. j. (CLAUDE.md vyžaduje č. j.)")

        for m in RE_US.finditer(radek):
            prefix, st, cislo_vec, rok, list_ = m.groups()
            citace = f"{prefix} ÚS{st or ''} {cislo_vec}/{rok}" + (f"-{list_}" if list_ else "")
            p = rej.pridej("R", "Ústavní soud", citace, soubor, cislo, radek, m)
            text_data, datum = _datum_u(radek, m.start(), m.end())
            _zaznamenej_datum(p, text_data)
            rok_cely = int(rok) + (2000 if len(rok) == 2 and int(rok) < 90 else 1900 if len(rok) == 2 else 0)
            _kontrola_roku(rej, p, rok_cely, datum)

        for m in RE_SDEU.finditer(radek):
            citace = f"{m.group(1)}-{m.group(2)}/{m.group(3)}" + (f" {m.group(4)}" if m.group(4) else "")
            p = rej.pridej("R", "SDEU", citace, soubor, cislo, radek, m)
            text_data, _ = _datum_u(radek, m.start(), m.end())
            _zaznamenej_datum(p, text_data)

        for m in RE_ECLI.finditer(radek):
            rej.pridej("R", "ECLI", m.group(0), soubor, cislo, radek, m)

        for m in RE_PARAGRAF.finditer(radek):
            citace = re.sub(r"§§?\s*", "§ ", m.group(0))
            citace = re.sub(r"\s*(odst\.|písm\.)\s*", r" \1 ", citace).strip()
            predpis = _predpis_u(radek, m.start(), m.end())
            p = rej.pridej("U", "ustanovení", f"{citace} [{predpis.split(' (')[0].split(' –')[0]}]",
                           soubor, cislo, radek, m, predpis=predpis)
            if predpis.startswith("ZZVZ") and int(m.group(1)) > MAX_PARAGRAF_ZZVZ:
                rej.upozorni(p, f"⚠ ZZVZ končí § {MAX_PARAGRAF_ZZVZ} – takové ustanovení neexistuje")
            if predpis.startswith("ZVZ"):
                rej.upozorni(p, "⚠ cituje zrušený zákon č. 137/2006 Sb. – ověř, zda je to záměr (intertemporalita)")

        for m in RE_CLANEK.finditer(radek):
            # České zákony se člení na §; články mají předpisy EU, ústavní předpisy a mezinárodní
            # smlouvy - jinak jde nejspíš o článek dokumentu (např. zadávací dokumentace).
            predpis = _predpis_u(radek, m.start(), m.end(), vzory=PREDPISY_CLANKY,
                                 vychozi="patrně článek dokumentu (např. ZD), ne předpisu")
            rej.pridej("U", "článek", f"{_normalizuj(m.group(0))} [{predpis.split(' (')[0].split(' –')[0]}]",
                       soubor, cislo, radek, m, predpis=predpis)

        for m in RE_PREDPIS.finditer(radek):
            druh = "vyhláška" if m.group(0).lower().startswith("vyhl") else \
                "nařízení vlády" if m.group(0).lower().startswith("nařízení") else "zákon"
            p = rej.pridej("P", "předpis ČR", f"{druh} č. {m.group(1)}/{m.group(2)} Sb.", soubor, cislo, radek, m)
            if (m.group(1), m.group(2)) == ("137", "2006"):
                rej.upozorni(p, "⚠ zrušený zákon o veřejných zakázkách – ověř intertemporalitu")
            if int(m.group(2)) > DNES.year:
                rej.upozorni(p, "⚠ rok předpisu je v budoucnosti")

        for m in RE_EU.finditer(radek):
            druh = "směrnice" if m.group(1).lower().startswith("směrnic") else "nařízení"
            oznaceni = f"({m.group(2)}) {m.group(3)}" if m.group(2) else m.group(3)
            rej.pridej("P", "předpis EU", f"{druh} {oznaceni}", soubor, cislo, radek, m)


def kontrola_zkratek(soubor: str, radky: list) -> list:
    """Legislativní zkratky: definovaná, ale nepoužitá, nebo zřejmě přepsaná (anagram)."""
    text = "\n".join(_normalizuj(r) for r in radky)
    nalezy = []
    for m in RE_ZKRATKA.finditer(text):
        zkratka = m.group(1).strip()
        cislo = text.count("\n", 0, m.start()) + 1
        zbytek = text[m.end():]
        pouziti = len(re.findall(r"(?<!\w)" + re.escape(zkratka) + r"(?!\w)", zbytek))
        zaznam = {"zkratka": zkratka, "definice": f"{soubor}:{cislo}", "pouziti": pouziti, "upozorneni": []}
        if pouziti == 0:
            zaznam["upozorneni"].append("⚠ definovaná zkratka se dále v textu nepoužívá")
        if re.fullmatch(r"[A-ZÁ-Ž]{3,8}", zkratka):
            kandidati = {}
            for slovo in re.findall(r"(?<!\w)[A-ZÁ-Ž]{3,8}(?!\w)", zbytek):
                if slovo != zkratka and sorted(slovo) == sorted(zkratka):
                    kandidati[slovo] = kandidati.get(slovo, 0) + 1
            for slovo, pocet in sorted(kandidati.items(), key=lambda x: -x[1]):
                zaznam["upozorneni"].append(f"⚠ pravděpodobný překlep: text dále používá „{slovo}“ ({pocet}×)")
        nalezy.append(zaznam)
    return nalezy


# --------------------------------------------------------------------------- výstup

SKUPINY = (("R", "Rozhodnutí (ÚOHS, soudy, SDEU)"), ("U", "Ustanovení"), ("P", "Předpisy"))


def _markdown(zdroje: list, rej: Rejstrik, zkratky: list) -> str:
    polozky = list(rej.polozky.values())
    pocty = {k: sum(1 for p in polozky if p["skupina"] == k) for k, _ in SKUPINY}
    s_upozornenim = sum(1 for p in polozky if p["upozorneni"]) + sum(1 for z in zkratky if z["upozorneni"])
    radky = [
        "# Rejstřík citací",
        "",
        f"- Zdroj: {', '.join(f'`{z}`' for z in zdroje)} (číslo za dvojtečkou = řádek / odstavec)",
        f"- Vygenerováno {dt.datetime.now():%Y-%m-%d %H:%M} skriptem `vytez_citace.py` – deterministická "
        "extrakce, **nic z toho není ověřeno**.",
        f"- Souhrn: rozhodnutí {pocty['R']}, ustanovení {pocty['U']}, předpisy {pocty['P']}; "
        f"položek s formálním upozorněním: {s_upozornenim}",
        "",
    ]
    for kod, nadpis in SKUPINY:
        vyber = [p for p in polozky if p["skupina"] == kod]
        radky.append(f"## {nadpis}")
        radky.append("")
        if not vyber:
            radky += ["_Nenalezeno._", ""]
            continue
        if kod == "R":
            radky += ["| ID | Typ | Citace | Soud | Datum v textu | Výskyty | Formální upozornění | Kontext 1. výskytu |",
                      "|---|---|---|---|---|---|---|---|"]
        else:
            radky += ["| ID | Typ | Citace | Předpis | Výskyty | Formální upozornění | Kontext 1. výskytu |",
                      "|---|---|---|---|---|---|---|"]
        for i, p in enumerate(vyber, start=1):
            p["id"] = f"{kod}{i}"
            if len(p["data"]) > 1:
                Rejstrik.upozorni(p, "⚠ v textu uvedena různá data: " + " × ".join(p["data"]))
            vyskyty = ", ".join(v.rsplit(":", 1)[1] for v in p["vyskyty"]) if len(zdroje) == 1 \
                else ", ".join(p["vyskyty"])
            upoz = "<br>".join(p["upozorneni"]) or "—"
            if kod == "R":
                radky.append(f"| {p['id']} | {p['typ']} | **{p['citace']}** | {p.get('soud', '—')} | "
                             f"{' × '.join(p['data']) or '—'} | {vyskyty} | {upoz} | {p['kontext']} |")
            else:
                radky.append(f"| {p['id']} | {p['typ']} | {p['citace']} | {p.get('predpis', '—')} | "
                             f"{vyskyty} | {upoz} | {p['kontext']} |")
        radky.append("")
    radky += ["## Legislativní zkratky", ""]
    if zkratky:
        radky += ["| Zkratka | Definice | Použití po definici | Formální upozornění |", "|---|---|---|---|"]
        for z in zkratky:
            radky.append(f"| „{z['zkratka']}“ | {z['definice']} | {z['pouziti']}× | "
                         f"{'<br>'.join(z['upozorneni']) or '—'} |")
    else:
        radky.append("_Žádná definice „(dále jen …)“ nenalezena._")
    radky.append("")
    return "\n".join(radky)


def main(argv=None) -> int:
    for proud in (sys.stdout, sys.stderr):
        if hasattr(proud, "reconfigure"):
            proud.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Deterministický rejstřík citací v právním textu.")
    parser.add_argument("soubory", nargs="+", help=".txt / .md / .docx")
    parser.add_argument("--json", action="store_true", help="výstup jako JSON místo Markdownu")
    parser.add_argument("--out", help="cesta výstupního souboru (jinak standardní výstup)")
    args = parser.parse_args(argv)

    rej, zkratky, zdroje = Rejstrik(), [], []
    for jmeno in args.soubory:
        cesta = Path(jmeno)
        if not cesta.is_file():
            print(f"CHYBA: {jmeno} neexistuje", file=sys.stderr)
            return 2
        radky = _nacti_radky(cesta)
        zdroje.append(cesta.name)
        vytez(cesta.name, radky, rej)
        zkratky += kontrola_zkratek(cesta.name, radky)

    vystup = _markdown(zdroje, rej, zkratky)  # přidělí i ID
    if args.json:
        vystup = json.dumps({"zdroje": zdroje, "vygenerovano": dt.datetime.now().isoformat(timespec="minutes"),
                             "citace": list(rej.polozky.values()), "zkratky": zkratky},
                            ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        with open(args.out, "w", encoding="utf-8", newline="\n") as f:
            f.write(vystup + "\n")
        print(f"Rejstřík uložen: {Path(args.out).as_posix()} ({len(rej.polozky)} citací)")
    else:
        print(vystup)
    return 0


if __name__ == "__main__":
    sys.exit(main())
