# Ďáblův advokát - VZ Legal Workspace

Pracovní prostředí pro české právníky zaměřené na veřejné a dotované zakázky, řízení před ÚOHS, kontroly Finanční správy a obranu proti tvrzenému porušení rozpočtové kázně.

Projekt kombinuje trvalá pravidla, specializované AI workflow a důvěrnou strukturu jednotlivých případů. Výstupy jsou pracovní podklady a vždy vyžadují schválení advokátem.

## Funkce

### 1. Právní analýza zadávacího řízení

- kvalifikace, technické a obchodní podmínky;
- předpokládaná hodnota a související plnění;
- hodnocení nabídek, procesní rizika a nápravná opatření.

### 2. Ďáblův advokát

- oponentura z pozice dodavatele, zadavatele, ÚOHS, auditora nebo soudu;
- identifikace právních, skutkových, důkazních a procesních slabin;
- konkrétní návrhy na posílení argumentace.

### 3. Rešerše ÚOHS a správních soudů

- vyhledání a ověření relevantních rozhodnutí;
- kontrola rozkladu a soudního přezkumu;
- syntéza rozhodovací praxe s odkazy na primární zdroje.

### 4. Verifikace právního výstupu

- kontrola paragrafů, rozhodnutí, lhůt a faktických tvrzení;
- rozlišení ověřené chyby, neověřitelného tvrzení a sporného výkladu;
- claim ledger s pinpoint citacemi.

### 5. Kontrola Finanční správy u dotační zakázky

Nativní Codex skill `$kontrola-financniho-uradu` a kompatibilní Claude workflow pokrývají:

- oznámení o zahájení a změně rozsahu daňové kontroly;
- výzvy k prokázání skutečností;
- dosavadní výsledek kontrolního zjištění (DVKZ) a vyjádření podle daňového řádu;
- zprávu a ukončení daňové kontroly;
- platební výměr na odvod a penále;
- odvolání, mimořádné prostředky a žádost o prominutí;
- dotační podmínky, PpVD/ZZVZ, kategorizaci sankcí, výpočet odvodu a prekluzi.

Workflow odděluje šest vrstev: daňový proces, dotační titul, zadání zakázky, porušení rozpočtové kázně, finanční dopad a opravné prostředky.

## Rychlý start

```powershell
git clone https://github.com/lukashlobil11/dabluv-advokat.git
cd dabluv-advokat
powershell -ExecutionPolicy Bypass -File scripts/new-case.ps1 -Name muj-case
```

Skript vytvoří úplnou strukturu v `cases/muj-case/`. Reálné cases jsou celé ignorované Gitem.

Vlož dokumenty do `cases/muj-case/zadani/` a vyplň:

- `cases/muj-case/README.md`;
- `cases/muj-case/matter.yaml`.

## Použití v Codexu

Codex automaticky načte [AGENTS.md](AGENTS.md). Kontrolu Finanční správy lze spustit například:

```text
$kontrola-financniho-uradu Analyzuj DVKZ v cases/muj-case/zadani a připrav matici tvrzení a důkazů.
```

U ostatních úloh stačí přirozený požadavek, například „proveď adversarial review argumentace“. `AGENTS.md` načte odpovídající workflow z `.claude/skills/`.

## Použití v Claude Code

Claude workflow jsou v `.claude/skills/`. Pro kontrolu Finanční správy použij:

```text
/skill kontrola-financniho-uradu
```

## Doporučený postup u kontroly Finanční správy

1. Zapiš doručení dokumentu a urgentní lhůtu.
2. Doplň rozhodnutí o dotaci, všechny změny, PpVD a rozhodnou sankční kategorizaci.
3. Vytvoř inventář spisu a označ chybějící dokumenty.
4. Rozlož každé kontrolní zjištění na normu, skutkový předpoklad, důkaz a inferenci.
5. Připrav hlavní i subsidiární obranu a konkrétní důkazní návrhy.
6. Přepočítej základ, sazbu, zaokrouhlení, penále a alternativní scénáře.
7. Proveď oponenturu a verifikaci citací před finalizací.

## Struktura

```text
dabluv-advokat/
├── AGENTS.md
├── CLAUDE.md
├── .agents/skills/
│   └── kontrola-financniho-uradu/
├── .claude/skills/
│   ├── pravni-analyza/
│   ├── adversarial-review/
│   ├── reserse-uohs/
│   ├── verifikace-vystupu/
│   └── kontrola-financniho-uradu/
├── cases/
│   └── _template/
├── references/
└── scripts/
    └── new-case.ps1
```

## Ochrana důvěrných dat

- `.gitignore` ignoruje celý obsah `cases/*` kromě sanitizované šablony.
- Dočasné extrakce a rendery patří do `tmp/`, které je také ignorované.
- Identifikátory klienta se nesmějí používat ve webových dotazech.
- `.gitignore` není náhradou za profesní povinnost mlčenlivosti, řízení přístupu a kontrolu staged souborů před commitem.

## Standard právní práce

- U každého závěru určit rozhodný den a účinné znění.
- Rozlišovat právní předpis, dotační podmínku, metodiku a návrh novely.
- Skutková tvrzení citovat na dokument a stranu/bod.
- Veřejné zdroje dokládat URL a datem přístupu.
- Neověřená tvrzení viditelně označit.
- Lhůty a finanční dopady uvádět s reprodukovatelným výpočtem.

## Hlavní oficiální zdroje

- [e-Sbírka](https://e-sbirka.gov.cz/)
- [Finanční správa - daňová kontrola](https://financnisprava.gov.cz/cs/dane/danovy-system-cr/postup-v-danovem-rizeni/danova-kontrola)
- [Finanční správa - odvody za porušení rozpočtové kázně](https://financnisprava.gov.cz/cs/dane/odvody-za-poruseni-rozpoctove-kazne/)
- [Sbírka rozhodnutí ÚOHS](https://uohs.gov.cz/cs/verejne-zakazky/sbirky-rozhodnuti.html)
- [Vyhledávač NSS](https://vyhledavac.nssoud.cz/)
- [EUR-Lex](https://eur-lex.europa.eu/)

## Právní upozornění

Workspace je podpůrný nástroj a nenahrazuje právní posouzení advokáta. Před použitím výstupu v konkrétní věci je nutné ověřit zdroje, rozhodné znění a skutkovou úplnost spisu.

## Licence

MIT License - viz [LICENSE](LICENSE).
