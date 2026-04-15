---
name: pravni-analyza
description: Komplexní právní analýza zadávacího řízení na veřejnou zakázku. Použij tento skill kdykoliv uživatel chce analyzovat zadávací řízení, posoudit zákonnost postupu zadavatele, identifikovat právní rizika, nebo připravit podklad pro argumentaci. Spouští se i při zmínce "analýza", "posouzení ZD", "právní rizika", "zákonnost postupu", "rozbor řízení", nebo když uživatel nahraje zadávací dokumentaci a chce s ní pracovat.
---

# Právní analýza zadávacího řízení

## Postup analýzy

### Krok 1: Identifikace základních parametrů
Přečti všechny dokumenty v `zadani/` a extrahuj:
- Zadavatel (typ: § 4 ZZVZ — ČR, územní celek, jiná PO dle § 4 odst. 1–4)
- Předmět VZ (dodávky / služby / stavební práce)
- Předpokládaná hodnota a kategorie (nadlimitní / podlimitní / VZMR)
- Druh zadávacího řízení (§ 55–72 ZZVZ)
- Zdroj financování (vlastní / dotace EU / národní dotace / NPO)
- Časová osa (zahájení, lhůta pro nabídky, rozhodnutí, námitky)

### Krok 2: Analýza zadávacích podmínek
Pro každou oblast posoudit soulad s ZZVZ:

**Kvalifikace (§ 73–88 ZZVZ):**
- Jsou kvalifikační předpoklady přiměřené předmětu a hodnotě VZ?
- Není kvalifikace diskriminační nebo nepřiměřeně omezující?
- Je reference list adekvátní? (hodnota, rozsah, doba)

**Technické podmínky (§ 89–95 ZZVZ):**
- Jsou technické podmínky definovány nediskriminačně?
- Odkazuje se na konkrétní značku/výrobce bez "nebo rovnocenné"?
- Je umožněna varianta/alternativa tam kde má být?

**Hodnotící kritéria (§ 114–119 ZZVZ):**
- Je hodnocení transparentní a přezkoumatelné?
- Mají subjektivní kritéria dostatečně popsanou metodu hodnocení?
- Odpovídá nastavení kritérií předmětu VZ?

**Obchodní/smluvní podmínky:**
- Jsou smluvní podmínky přiměřené?
- Nejsou sankce nepřiměřeně vysoké?
- Je alokace rizik vyvážená?

### Krok 3: Identifikace problémových oblastí
Pro každý identifikovaný problém vytvoř záznam:

```
## Problém č. [N]: [název]
**Závažnost:** [KRITICKÁ / VYSOKÁ / STŘEDNÍ / NÍZKÁ]
**Dotčená ustanovení ZZVZ:** § XX odst. Y
**Popis problému:** [co je špatně]
**Riziko:** [jaký je důsledek — zrušení zadávacího řízení / nápravné opatření / finanční korekce]
**Doporučení:** [jak napravit / jak argumentovat]
**Relevantní rozhodovací praxe:** [pokud znáš, jinak "provést rešerši"]
```

### Krok 4: Souhrnné hodnocení
Vytvoř celkové hodnocení s kategorizací:
- ZELENÁ — zadávací řízení je v pořádku
- ORANŽOVÁ — existují rizika, ale jsou obhajitelná
- ČERVENÁ — závažné porušení ZZVZ, vysoké riziko zrušení

### Výstup
Ulož kompletní analýzu do `analyza/pravni-analyza-[datum].md`
