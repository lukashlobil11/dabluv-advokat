# VZ Legal Workspace

Komplexní systém pro právní analýzu veřejných zakázek, dotačních kontrol a řízení před Úřadem pro ochranu hospodářské soutěže (ÚOHS).

Workspace je určen pro právníky a právní poradce specializované na administraci veřejných zakázek dle zákona č. 134/2016 Sb. (ZZVZ) a práci se správními řízením.

## 🎯 Funkce

### 1. **Právní analýza zadávacího řízení** (`/pravni-analyza`)
- Systematické posouzení legality zadávacího řízení
- Analýza kvalifikačních předpokladů, technických podmínek a hodnotících kritérií
- Identifikace právních rizik s kategorizací závažnosti
- Zjištění problémových oblastí a doporučení na nápravu

### 2. **Adversarial Review — Ďáblův advokát** (`/adversarial-review [case] [role] [režim]`)
- Kritické testování odolnosti právní argumentace z pozice protistrany (navrhovatel, ÚOHS, předseda ÚOHS, správní soud, dotační kontrolor)
- Tři režimy: `rychly` (jen hlavní model), `standard` (výchozí), `hloubkovy` (tři nezávislí oponenti + nezávislá simulace rozhodnutí)
- Odstupňované modely: **Opus 5.5** útočí, konsoliduje a simuluje rozhodnutí; **Sonnet 5.5** ověřuje citace a rešeršuje; **Haiku 4.5** připravuje podklady a formálně kontroluje posudek
- Deterministický rejstřík citací odhalí formálně nemožné citace (rok v budoucnosti, datum před rokem sp. zn., § nad rozsah ZZVZ) i přepsané legislativní zkratky
- Výstup: oponentní posudek se slabinami seřazenými podle závažnosti, protokolem ověření citací a simulací rozhodnutí

### 3. **Rešerše rozhodovací praxe ÚOHS** (`/reserse-uohs`)
- Vyhledávání relevantních rozhodnutí ÚOHS
- Zpracování a kategorizace nalezené judikatury
- Syntéza rozhodovací praxe k právnímu problému
- Identifikace trendů v rozhodování

### 4. **Verifikace výstupů z externích AI** (`/verifikace-vystupu`)
- Fact-checking právních argumentací z ChatGPT, Gemini a jiných AI
- Ověřování správnosti citací zákonů a rozhodnutí
- Analýza kvality právní argumentace
- Kritické hodnocení úplnosti a logické konzistence

## 📁 Struktura

```
vz-legal-workspace/
├── CLAUDE.md                          # Hlavní instrukce, modelová politika
├── .claude/
│   ├── skills/                        # Čtyři AI skills
│   │   ├── pravni-analyza/SKILL.md
│   │   ├── adversarial-review/        # Ďáblův advokát
│   │   │   ├── SKILL.md               # Orchestrace (Opus 5.5)
│   │   │   ├── references/            # Role oponentů, kontrolní otázky A–G
│   │   │   ├── assets/                # Šablona oponentního posudku
│   │   │   ├── scripts/               # Převod podkladů, rejstřík citací (Python)
│   │   │   └── evals/                 # Testovací „kanárek“ s nastraženými chybami
│   │   ├── reserse-uohs/SKILL.md
│   │   └── verifikace-vystupu/SKILL.md
│   └── agents/                        # Subagenti s pevně přiřazeným modelem
│       ├── oponent.md                 # Opus 5.5
│       ├── simulator-rozhodnuti.md    # Opus 5.5
│       ├── overovatel-citaci.md       # Sonnet 5.5
│       ├── reserse-protiargumentu.md  # Sonnet 5.5
│       ├── priprava-podkladu.md       # Haiku 4.5
│       └── formalni-kontrola.md       # Haiku 4.5
├── cases/                             # Jednotlivé případy
│   ├── _template/                     # Šablona pro nový case
│   │   ├── README.md                  # Popis case
│   │   ├── zadani/                    # Vstupní dokumenty
│   │   ├── reserse/                   # Nalezená rozhodnutí
│   │   ├── analyza/                   # Analytické výstupy
│   │   ├── argumentace/               # Návrhy argumentací
│   │   ├── oponentura/                # Adversarial review
│   │   └── final/                     # Finální dokumenty
└── references/
    ├── pravni-ramec.md                # Klíčová ustanovení ZZVZ
    ├── metodika-argumentace.md        # Struktura právní argumentace
    └── checklist-uohs.md              # Co ÚOHS typicky kontroluje
```

## 🚀 Workflow — Jak začít

### Inicializace nového case:

```bash
# Klonování repository
git clone https://github.com/lukashlobil11/dabluv-advokat.git
cd dabluv-advokat/vz-legal-workspace

# Vytvoření nového case z šablony
cp -r cases/_template cases/nazev-muj-case
```

### Práce s case:

1. **Vyplnění metadat**
   - Otevřeš `cases/nazev-muj-case/README.md`
   - Vyplníš základní údaje: zadavatel, PH, typ VZ, fázi řízení

2. **Nahrání dokumentů**
   - Vložíš PDF/Word do `cases/nazev-muj-case/zadani/`
   - Např: ZD.pdf, namitky.pdf, rozhodovani.pdf

3. **Automatická právní analýza**
   ```
   /pravni-analyza
   ```
   - Skill čte z `zadani/`, analyzuje dokumenty
   - Výstup → `analyza/pravni-analyza-[datum].md`

4. **Rešerše rozhodovací praxe** (opt.)
   ```
   /reserse-uohs
   ```
   - Vyhledá relevantní rozhodnutí ÚOHS
   - Výstup → `reserse/reserse-[tema]-[datum].md`

5. **Ruční příprava argumentace**
   - Napíšeš vyjádření k námitkám nebo návrhu
   - Uložíš do `argumentace/`

6. **Testování argumentace — Ďáblův advokát**
   ```
   /adversarial-review nazev-muj-case standard
   ```
   - Role oponenta se odvodí z fáze řízení (nebo ji zadej: `navrhovatel`, `uohs`, `predseda`, `soud`, `kontrolor`, `vse`)
   - Pro zásadní podání (návrh, rozklad, žaloba) použij režim `hloubkovy`
   - Skill napadá tvou argumentaci, ověřuje citace a simuluje rozhodnutí
   - Výstup → `oponentura/adversarial-review-[datum].md`, pracovní podklady → `oponentura/_podklady/`

7. **Finální úpravy**
   - Přepracuješ argumentaci na základě oponentury
   - Finální verzi ulož do `final/`

## 📋 Klíčové vlastnosti

### ✅ Kvalitativní standardy
- **Právní přesnost:** Nikdy se nevymýšlí paragrafy či rozhodnutí ÚOHS
- **Strukturovanost:** Každý argument dodržuje strukturu: norma → výklad → subsumpce → závěr
- **Transparentnost:** Vždy je jasné, co je ověřeno, co je [K OVĚŘENÍ] a jaká je síla argumentu
- **Bezpečnost dat:** Real case data se **neuploadují na GitHub** (`.gitignore`)

### 🔒 Ochrana citlivých údajů
- `.gitignore` filtruje všechny case dokumenty (až na šablonu)
- Můžeš bezpečně pracovat s real case bez rizika leakage
- Na GitHubu je jen kostra a reference
- Lokální paměť agenta `overovatel-citaci` (registr ověřených citací, `.claude/agent-memory-local/`) se také neverzuje

### 📚 Reference
- **Právní rámec:** Klíčová ustanovení ZZVZ, procesní lhůty, zásady
- **Metodika:** Jak strukturovat právní argumentaci, argumentační chyby
- **Checklist:** Co ÚOHS typicky kontroluje, nejčastější důvody zrušení VZ

## 🛠️ Technické požadavky

- **Claude Code** (aktuální verze) s přístupem k modelům **Opus 5.5** (hlavní), **Sonnet 5.5** a **Haiku 4.5**
- Claude Code spouštěj ve složce `vz-legal-workspace` (v aplikaci ji otevři jako pracovní složku) — jen tak se spolehlivě načte `CLAUDE.md` a najdou se subagenti z `.claude/agents/`
- Subagenty Claude Code hledá od pracovního adresáře směrem nahoru až ke kořeni repozitáře; relace spuštěná v nadřazené složce je nenajde a skill přejde na záložní režim (`general-purpose` + parametr `model`). Změny v existujících agentech se projeví do několika sekund, úplně první vytvoření složky `.claude/agents/` vyžaduje restart relace
- **Přístup k web search** pro `/reserse-uohs` a ověřování citací (volitelné, ale doporučené)
- **Python 3.8+** pro skripty skillu `adversarial-review` (jen standardní knihovna; bez Pythonu skill funguje v omezeném režimu)
- Textový editor (VS Code, Sublime, vim...)

## 📖 Dokumentace

- **[CLAUDE.md](CLAUDE.md)** — Hlavní instrukce, pravidla, workflow
- **[references/pravni-ramec.md](references/pravni-ramec.md)** — Přehled právní úpravy
- **[references/metodika-argumentace.md](references/metodika-argumentace.md)** — Jak psát právní argumenty
- **[references/checklist-uohs.md](references/checklist-uohs.md)** — Co kontroluje ÚOHS

## 💡 Příklady use-casů

1. **Obrana v řízení o námitkách:** Analýza námitek + příprava vyjádření zadavatele
2. **Příprava návrhu na ÚOHS:** Komplexní analýza + rešerše relevantní praxe + argumentace
3. **Správní žaloba:** Stress test argumentace skrze adversarial review
4. **Dotační kontrola:** Analýza kontrol a příprava vyjádření
5. **Verifikace AI výstupů:** Fact-check právních analýz od ChatGPT/Gemini

## ⚖️ Právní upozornění

Tento workspace je nástrojem na podporu právní analýzy. Není to právní poradenství a nenahrazuje skutečného právníka. Používání předpokládá:

- Hluboké porozumění ZZVZ a správnímu řádu
- Kritické posouzení výstupů (LLM mají tendenci k halucinacím)
- Ověření všech citací zákona a rozhodnutí v autentických zdrojích
- Zodpovědnost za finální právní pozici leží na právníkovi

## 📝 Licence

MIT License — viz [LICENSE](LICENSE) pro úplné znění.

---

**Autor:** Lukáš Hlobil  
**Poslední aktualizace:** říjen 2026  
**Technologie:** Claude AI, Python (volitelně), Markdown
