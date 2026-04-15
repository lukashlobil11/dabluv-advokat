# VZ Legal Workspace

Komplexní systém pro právní analýzu veřejných zakázek, dotačních kontrol a řízení před Úřadem pro ochranu hospodářské soutěže (ÚOHS).

Workspace je určen pro právníky a právní poradce specializované na administraci veřejných zakázek dle zákona č. 134/2016 Sb. (ZZVZ) a práci se správními řízením.

## 🎯 Funkce

### 1. **Právní analýza zadávacího řízení** (`/skill pravni-analyza`)
- Systematické posouzení legality zadávacího řízení
- Analýza kvalifikačních předpokladů, technických podmínek a hodnotících kritérií
- Identifikace právních rizik s kategorizací závažnosti
- Zjištění problémových oblastí a doporučení na nápravu

### 2. **Adversarial Review — Ďáblův advokát** (`/skill adversarial-review`)
- Kritické testování odolnosti právní argumentace
- Simulace pozice protistrany (navrhovatel, ÚOHS, správní soud)
- Identifikace slabých míst v argumentaci
- Konkrétní doporučení na posílení argumentů

### 3. **Rešerše rozhodovací praxe ÚOHS** (`/skill reserse-uohs`)
- Vyhledávání relevantních rozhodnutí ÚOHS
- Zpracování a kategorizace nalezené judikatury
- Syntéza rozhodovací praxe k právnímu problému
- Identifikace trendů v rozhodování

### 4. **Verifikace výstupů z externích AI** (`/skill verifikace-vystupu`)
- Fact-checking právních argumentací z ChatGPT, Gemini a jiných AI
- Ověřování správnosti citací zákonů a rozhodnutí
- Analýza kvality právní argumentace
- Kritické hodnocení úplnosti a logické konzistence

## 📁 Struktura

```
vz-legal-workspace/
├── CLAUDE.md                          # Hlavní instrukce
├── .claude/skills/                    # Čtyři AI skills
│   ├── pravni-analyza/SKILL.md
│   ├── adversarial-review/SKILL.md
│   ├── reserse-uohs/SKILL.md
│   └── verifikace-vystupu/SKILL.md
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
   /skill pravni-analyza
   ```
   - Skill čte z `zadani/`, analyzuje dokumenty
   - Výstup → `analyza/pravni-analyza-[datum].md`

4. **Rešerše rozhodovací praxe** (opt.)
   ```
   /skill reserse-uohs
   ```
   - Vyhledá relevantní rozhodnutí ÚOHS
   - Výstup → `reserse/reserse-[tema]-[datum].md`

5. **Ruční příprava argumentace**
   - Napíšeš vyjádření k námitkám nebo návrhu
   - Uložíš do `argumentace/`

6. **Testování argumentace — Ďáblův advokát**
   ```
   /skill adversarial-review
   ```
   - Skill napadá tvou argumentaci
   - Identifikuje slabiny a navrhuje posílení
   - Výstup → `oponentura/adversarial-review-[datum].md`

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
- Apenas kostra + reference jsou na GitHubu

### 📚 Reference
- **Právní rámec:** Klíčová ustanovení ZZVZ, procesní lhůty, zásady
- **Metodika:** Jak strukturovat právní argumentaci, argumentační chyby
- **Checklist:** Co ÚOHS typicky kontroluje, nejčastější důvody zrušení VZ

## 🛠️ Technické požadavky

- **Claude Code** s přístupem k Claude Opus 4.6+ (nebo jiný Haiku/Sonnet)
- **Přístup k web search** pro `/skill reserse-uohs` (volitelné, ale doporučené)
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

Tento workspace je nástrojem na podporu právní analýzy. Není to právní poradenství a nahrazuje skutečného právníka. Používání předpokládá:

- Hluboké porozumění ZZVZ a správnímu řádu
- Kritické posouzení výstupů (LLM mají tendenci k halucinacím)
- Ověření všech citací zákona a rozhodnutí v autentických zdrojích
- Zodpovědnost za finální právní pozici leží na právníkovi

## 📝 Licence

[Doplnit podle preference — např. MIT, CC BY-NC-SA, Private]

---

**Autor:** [Tvoje jméno / kontakt]  
**Poslední aktualizace:** duben 2026  
**Technologie:** Claude AI, Python (volitelně), Markdown
