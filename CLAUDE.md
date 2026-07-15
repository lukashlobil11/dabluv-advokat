# VZ Legal Workspace - Claude Code

Před každou prací přečti a dodrž kořenový `AGENTS.md`. Obsahuje společná pravidla důvěrnosti, právního ověřování, citací a práce s case.

## Claude skills

- `.claude/skills/pravni-analyza/SKILL.md`
- `.claude/skills/adversarial-review/SKILL.md`
- `.claude/skills/reserse-uohs/SKILL.md`
- `.claude/skills/verifikace-vystupu/SKILL.md`
- `.claude/skills/kontrola-financniho-uradu/SKILL.md`

## Nový case

```powershell
powershell -ExecutionPolicy Bypass -File scripts/new-case.ps1 -Name nazev-case
```

## Kontrola Finanční správy

Při výzvě, DVKZ, zprávě o daňové kontrole, platebním výměru, odvodu, penále, odvolání nebo žádosti o prominutí spusť:

```text
/skill kontrola-financniho-uradu
```

Kanonické instrukce tohoto workflow jsou v `.agents/skills/kontrola-financniho-uradu/` a jsou společné pro Claude i Codex.
