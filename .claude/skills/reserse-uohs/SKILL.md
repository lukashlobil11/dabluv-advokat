---
name: reserse-uohs
description: Rešerše rozhodovací praxe ÚOHS v oblasti veřejných zakázek. Vyhledává relevantní rozhodnutí k zadanému právnímu problému. Použij tento skill kdykoliv uživatel hledá rozhodnutí ÚOHS, potřebuje judikaturu k právnímu problému, chce zjistit jak ÚOHS rozhoduje v obdobných případech, nebo zmíní "rešerše", "rozhodovací praxe", "judikatura ÚOHS", "jak rozhodl ÚOHS", "najdi rozhodnutí", "precedent".
---

# Rešerše rozhodovací praxe ÚOHS

## Zdroje
Primární zdroj: https://uohs.gov.cz/cs/verejne-zakazky/sbirky-rozhodnuti.html

Sekundární zdroje pro judikaturu správních soudů:
- Krajský soud v Brně (věcně příslušný pro žaloby proti ÚOHS)
- Nejvyšší správní soud (kasační stížnosti)

## Postup rešerše

### Krok 1: Definice rešeršní otázky
Na základě analýzy case formuluj:
- Přesný právní problém (např. "přiměřenost kvalifikačního předpokladu u stavebních prací")
- Dotčená ustanovení ZZVZ
- Klíčová slova pro vyhledávání

### Krok 2: Vyhledávání
Pokud máš přístup k web search:
- Hledej na uohs.gov.cz kombinací klíčových slov
- Hledej i na rozhodnutích správních soudů
- Prověř odborné komentáře a články

Formuluj vyhledávací dotazy cíleně:
- "ÚOHS kvalifikační předpoklady přiměřenost stavební práce"
- "ÚOHS § 73 odst. 6 ZZVZ reference"
- "site:uohs.gov.cz [klíčová slova problému]"

### Krok 3: Zpracování nalezených rozhodnutí
Pro každé relevantní rozhodnutí vytvoř kartu:

```
## Rozhodnutí č. [N]
**Č.j.:** ÚOHS-XXXXX/YYYY/500
**Datum:** DD.MM.RRRR
**Předseda/člen ÚOHS:** [jméno]
**Typ rozhodnutí:** [prvostupňové / rozklad / předběžné opatření]
**Zadavatel:** [název]
**Předmět VZ:** [stručně]
**Právní otázka:** [co ÚOHS řešil]
**Právní věta:** [klíčový závěr — vlastními slovy, ne kopie]
**Relevance pro náš case:** [VYSOKÁ / STŘEDNÍ / NÍZKÁ]
**Jak použít:** [konkrétní návod jak rozhodnutí použít v argumentaci]
**Status:** [platné / zrušeno soudem / překonané]
```

### Krok 4: Syntéza
- Shrň trend rozhodovací praxe k dané otázce
- Identifikuj případné rozpory mezi rozhodnutími
- Identifikuj vývoj v čase (zpřísnění / uvolnění)
- Doporuč nejsilnější rozhodnutí pro argumentaci

### Výstup
Ulož do `reserse/reserse-[tema]-[datum].md`

## Důležitá pravidla
- NIKDY nevymýšlej čísla jednací — pokud rozhodnutí nenajdeš, řekni to
- U každého rozhodnutí uveď jak jsi ho našel (URL / zdroj)
- Ověř zda rozhodnutí nebylo zrušeno soudem
- Rozlišuj prvostupňová rozhodnutí a rozhodnutí o rozkladu (rozklad má vyšší váhu)
- Rozhodnutí předsedy ÚOHS o rozkladu mají obecně nejvyšší autoritu
