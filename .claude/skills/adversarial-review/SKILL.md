---
name: adversarial-review
description: Adversarial review — ďáblův advokát pro právní argumentaci. Systematicky napadá a testuje odolnost právní argumentace z pozice protistrany (navrhovatel, ÚOHS, dotační orgán, správní soud). Použij tento skill kdykoliv uživatel chce otestovat argumentaci, provést oponenturu, najít slabiny, verifikovat právní text, provést "crash test" argumentace, nebo zmíní "ďáblův advokát", "oponentura", "napadni to", "rozbij tu argumentaci", "co na to řekne ÚOHS", "jak to napadne protistrana", "adversarial", "review argumentace", "stress test".
---

# Adversarial Review — Ďáblův advokát

## Účel
Systematicky testovat odolnost právní argumentace tím, že zaujmeš pozici protistrany a pokusíš se argumentaci rozbít. Cílem NENÍ dokázat že argumentace je špatná — cílem je identifikovat slabá místa, aby mohla být posílena.

## Postup

### Krok 0: Určení role oponenta
Na základě kontextu case zvol jednu z rolí:
- **Advokát navrhovatele** — pokud je klient zadavatel a argumentace je vyjádření k námitkám/návrhu
- **Právník ÚOHS** — pokud testuješ odolnost argumentace vůči přezkumnému řízení
- **Auditor/kontrolor** — pokud jde o dotační kontrolu
- **Soudce správního soudu** — pokud testuješ odolnost vůči žalobě/kasační stížnosti

Vždy explicitně uveď z jaké pozice argumentuješ.

### Krok 1: Strukturální analýza
Projdi argumentaci a pro každý tvrzený argument ověř:

**A) Úplnost právní normy**
- Je citovaný § správný a úplný?
- Není vytržen z kontextu (chybí navazující odstavce/písmena)?
- Neexistuje speciální úprava která má přednost?
- Nebyl § novelizován?

**B) Kvalita subsumpce**
- Jsou skutkové závěry podložené důkazy ze spisu?
- Není subsumpce příliš obecná / vágní?
- Neobsahuje logické skoky?
- Funguje subsumpce i při jiném výkladu skutkového stavu?

**C) Konzistence**
- Neprotiřečí si argumenty navzájem?
- Je argumentační linie koherentní?
- Nepoužívá argumentace selektivně fakta?

**D) Rozhodovací praxe**
- Jsou citovaná rozhodnutí ÚOHS/soudů relevantní?
- Nejsou překonaná novější praxí?
- Neexistují protichůdná rozhodnutí?
- Je ratio decidendi aplikovatelné na tento případ?

### Krok 2: Protiargumentace
Pro každý identifikovaný slabý bod:

```
## Slabina č. [N]: [název]
**Napadený argument:** [který argument z původní argumentace]
**Typ slabiny:** [právní / skutková / logická / procesní]
**Protiargument:** [konkrétní argument protistrany]
**Podpora protiargumentu:** [§ ZZVZ / rozhodnutí ÚOHS / judikatura]
**Síla protiargumentu:** [DEVASTUJÍCÍ / SILNÝ / STŘEDNÍ / SLABÝ]
**Doporučení na posílení:** [jak původní argumentaci upravit aby odolala]
```

### Krok 3: Simulace rozhodnutí
Na základě analýzy vytvoř stručnou simulaci:
- Jak by pravděpodobně rozhodl ÚOHS / správní soud?
- Které argumenty by obstály a které ne?
- Jaká je celková šance na úspěch: [VYSOKÁ / STŘEDNÍ / NÍZKÁ]

### Krok 4: Souhrnné doporučení
- Seřaď slabiny podle závažnosti
- Navrhni konkrétní úpravy argumentace
- Identifikuj argumenty které je lepší zcela přepracovat vs. mírně upravit
- Navrhni případné doplnění argumentace o nové body

### Výstup
Ulož do `oponentura/adversarial-review-[datum].md`

## Důležitá pravidla
- Buď NEMILOSRDNÝ — skutečná protistrana nebude ohleduplná
- Nebuď ale destruktivní bezdůvodně — každá kritika musí být podložená
- Pokud je argument skutečně silný a nevidíš slabinu, řekni to explicitně
- NIKDY nevymýšlej neexistující rozhodnutí ÚOHS nebo judikaturu
- Pokud by protiargument vyžadoval specifické rozhodnutí a neznáš je, napiš [REŠERŠIT — protiargument by byl silnější s konkrétním rozhodnutím k tématu XY]
