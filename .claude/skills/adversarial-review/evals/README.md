# Testy skillu adversarial-review

`kanarek/` je fiktivní case s návrhem rozhodnutí o námitkách, do kterého jsou záměrně nastražené
vady (smyšlená a formálně nemožná rozhodnutí, neexistující §, rozpory se spisem i uvnitř textu,
logická chyba, útok na osobu, přepsaná legislativní zkratka) a několik správných pasáží, které
skill napadat nemá. Očekávané nálezy jsou v `evals.json`.

## Spuštění (z kořene `vz-legal-workspace`)

```bash
cp -r .claude/skills/adversarial-review/evals/kanarek cases/_kanarek
```

Pak v Claude Code: `/adversarial-review _kanarek standard` a posudek
`cases/_kanarek/oponentura/adversarial-review-<datum>.md` porovnej s `expectations` v `evals.json`.
Složka `cases/_kanarek/` je v `.gitignore`.

Kanárka spusť po každé větší úpravě skillu, agentů nebo po změně modelu — zachytí, když skill
přestane hlídat smyšlené citace nebo začne vyrábět nepodložené výtky.

## Ukázka a základní výsledek
`ukazka-posudku.md` je výstup prvního běhu (2026-10-06). Slouží jako ukázka formátu a jako
základ pro porovnání dalších běhů — není to „správná odpověď“. Při tom běhu:

- všech 14 očekávání ze zadání č. 1 bylo splněno (včetně dvou správných pasáží, které skill nenapadl);
- běh byl záložní: vlastní agenti nebyli načteni, subagenti běželi jako `general-purpose` s modelem
  Haiku 4.5 a Sonnet 5.5 (potvrzeno jejich vlastním hlášením), oddíly 5–8 dopsal Sonnet 5.5;
- rešerše nedoběhla (limit relace), a proto jsou všechny rešeršní úkoly v oddílu 8 otevřené;
- zadání č. 2 a č. 3 se zatím nespouštěla.
