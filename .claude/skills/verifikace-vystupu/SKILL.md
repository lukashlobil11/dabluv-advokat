---
name: verifikace-vystupu
description: Verifikace a kritická analýza právních výstupů z externích AI modelů (ChatGPT, Gemini, jiná instance Claude). Systematicky ověřuje správnost citací, kvalitu argumentace, faktickou přesnost a úplnost. Použij tento skill kdykoliv uživatel chce ověřit výstup z jiného AI, verifikovat argumentaci, zkontrolovat text od ChatGPT/Gemini, nebo zmíní "ověř tohle", "zkontroluj výstup", "tohle napsal ChatGPT", "verifikace", "je tohle správně", "zkontroluj citace", "fact-check".
---

# Verifikace výstupů z externích AI

## Kontext
LLM modely (včetně Claude) mají tendenci k halucinacím — vymýšlení neexistujících §, rozhodnutí, judikatury. Tento skill systematicky ověřuje právní výstupy.

## Postup verifikace

### Krok 1: Identifikace ověřitelných tvrzení
Projdi celý text a označ každé tvrzení které jde ověřit:
- Citace § zákonů
- Čísla jednací rozhodnutí ÚOHS
- Citace judikatury (č.j. rozsudků)
- Faktická tvrzení o právní úpravě
- Tvrzení o rozhodovací praxi
- Lhůty, termíny, limity

### Krok 2: Ověření právních citací
Pro každou citaci zákona:
- [ ] Existuje tento § v citovaném zákoně?
- [ ] Odpovídá obsah § tomu, co text tvrdí?
- [ ] Je § citován úplně (správný odstavec, písmeno)?
- [ ] Je § aktuální (nebyl zrušen/novelizován)?
- [ ] Je § aplikovatelný na danou situaci?

### Krok 3: Ověření rozhodovací praxe
Pro každé citované rozhodnutí:
- [ ] Existuje rozhodnutí s tímto č.j.? → [OVĚŘENO / NELZE OVĚŘIT / NEEXISTUJE]
- [ ] Odpovídá uváděná právní věta skutečnému obsahu rozhodnutí?
- [ ] Je rozhodnutí stále relevantní (nebylo zrušeno soudem)?
- [ ] Je ratio decidendi aplikovatelné na tento případ?

### Krok 4: Analýza kvality argumentace
- Je argumentační struktura logicky konzistentní?
- Nejsou v textu logické mezery nebo skoky?
- Jsou závěry podložené premisami?
- Neobsahuje text vnitřní rozpory?
- Rozlišuje text mezi de lege lata a de lege ferenda?

### Krok 5: Analýza úplnosti
- Chybí relevantní právní úprava kterou text opomíjí?
- Existují protichůdné argumenty které text nezohledňuje?
- Je pokryta procesní stránka (lhůty, legitimace, formální náležitosti)?

### Výstupní formát

```
# Verifikační report

## Celkové hodnocení: [SPOLEHLIVÝ / ČÁSTEČNĚ SPOLEHLIVÝ / NESPOLEHLIVÝ]

## Ověřené citace
| # | Citace | Status | Poznámka |
|---|--------|--------|----------|
| 1 | § XX ZZVZ | ✅ / ⚠️ / ❌ | detail |

## Identifikované problémy
### [KRITICKÉ] — vyžadují okamžitou opravu
### [DŮLEŽITÉ] — ovlivňují kvalitu argumentace
### [DROBNÉ] — stylistické / formální nedostatky

## Doporučené úpravy
[konkrétní návrhy na opravu s odůvodněním]
```

### Výstup
Ulož do `analyza/verifikace-[zdroj]-[datum].md`

## Důležité
- Rozlišuj mezi "ověřeně špatné" a "nelze ověřit" — to jsou dvě různé kategorie
- U rozhodnutí ÚOHS — pokud nemůžeš ověřit existenci, označ jako [NELZE OVĚŘIT — doporučuji manuální kontrolu na uohs.gov.cz]
- NIKDY neoznačuj něco jako ověřené pokud jsi to skutečně neověřil
- Pokud máš přístup k webu (web search), aktivně vyhledávej a ověřuj
