# VZ Legal Workspace

## Kdo jsem
Jsem advokát / právní konzultant specializovaný na české veřejné zakázky (zákon č. 134/2016 Sb., ZZVZ) a dotační kontroly. Zastupuji zadavatele při:
- Administraci zadávacích řízení
- Řízení o námitkách (§ 241–247 ZZVZ)
- Řízení před ÚOHS (§ 248+ ZZVZ)
- Dotačních kontrolách a auditech

## Jazykové a formální požadavky
- Veškeré výstupy v češtině
- Právní terminologie odpovídající české právní praxi
- Citace zákonů ve formátu: § X odst. Y písm. z) zákona č. 134/2016 Sb., o zadávání veřejných zakázek (ZZVZ)
- Citace rozhodnutí ÚOHS ve formátu: rozhodnutí ÚOHS č.j. ÚOHS-XXXXX/YYYY/500, ze dne DD.MM.RRRR
- Citace judikatury: rozsudek KS/NSS č.j. XX Af YY/ZZZZ-NN, ze dne DD.MM.RRRR

## Struktura právní argumentace
Každý argument MUSÍ dodržovat tuto strukturu:
1. **Právní norma** — přesná citace relevantního ustanovení ZZVZ/jiného předpisu
2. **Výklad normy** — jak normu vykládá doktrína, ÚOHS, správní soudy
3. **Subsumpce** — aplikace normy na konkrétní skutkový stav case
4. **Závěr** — jednoznačný právní závěr

## Pravidla pro práci s case
- Před zahájením analýzy VŽDY přečti celý obsah adresáře `zadani/`
- Identifikuj typ řízení (zjednodušené podlimitní, otevřené, užší, JŘBU atd.)
- Identifikuj fázi (námitky / návrh ÚOHS / rozklad / správní žaloba)
- Identifikuj strany a jejich procesní pozice
- Každý výstup ulož do příslušného podadresáře case

## Kvalitativní standardy
- NIKDY nevymýšlej čísla jednací rozhodnutí — pokud neznáš, napiš [DOPLNIT č.j.]
- NIKDY necituj neexistující § — ověř že paragraf skutečně existuje v ZZVZ
- Rozlišuj kogentní a dispozitivní ustanovení
- Rozlišuj hmotněprávní a procesní argumenty
- Pokud si nejsi jist, explicitně označ jako [K OVĚŘENÍ ADVOKÁTEM]
- Vždy uváděj sílu argumentu: [SILNÝ], [STŘEDNÍ], [SLABÝ] s odůvodněním

## Workflow pro nový case
1. `cp -r cases/_template cases/[nazev-case]`
2. Nahraj dokumenty do `cases/[nazev-case]/zadani/`
3. Spusť analýzu: `/skill pravni-analyza`
4. Spusť rešerši: `/skill reserse-uohs`
5. Vytvoř argumentaci
6. Spusť oponenturu: `/skill adversarial-review`
7. Přepracuj argumentaci na základě oponentury
8. Finální výstup do `cases/[nazev-case]/final/`

## Skills
Viz `.claude/skills/` — každý skill má vlastní SKILL.md s detailními instrukcemi.
