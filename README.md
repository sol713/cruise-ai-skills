# Cruise AI Skills

Open-source AI skills for cruise travelers, cruise bloggers, travel advisors, and AI agents. This GitHub-ready skill repo includes focused decision tools for cruise package value, cruise line comparison, and shore excursion planning.

## What's Included

| Skill | Status | Best for |
|---|---|---|
| `cruise-package-calculator` | Live | Drink packages, Wi-Fi plans, dining packages, photo packages, onboard bundles, and pre-cruise add-on math |
| `cruise-line-comparator` | Live | Carnival vs Royal Caribbean, Princess vs Celebrity, NCL vs MSC, family cruises, solo cruises, Alaska, Caribbean, and Mediterranean comparisons |
| `shore-excursion-optimizer` | Live | Ship-sponsored excursions vs independent tours vs self-guided port days, with return-to-ship risk scoring |

## Why This Repo Exists

Cruise planning is full of high-intent decisions where travelers need a clear answer, not vague inspiration:

- Is the drink package actually worth buying?
- Which cruise line fits my family, budget, and travel style?
- Is an independent shore excursion worth the return-to-ship risk?

These skills are built to answer those questions with structured inputs, visible tradeoffs, cost logic, freshness warnings, and practical recommendations.

## Repository Structure

```text
cruise-ai-skills-github/
├── SKILL.md
├── skills/
│   ├── cruise-package-calculator/
│   │   └── SKILL.md
│   ├── cruise-line-comparator/
│   │   └── SKILL.md
│   └── shore-excursion-optimizer/
│       └── SKILL.md
├── README.md
└── LICENSE
```

Each skill folder may also include `SYSTEM_PROMPT.md`, `metadata.yaml`, `examples/`, `references/`, `scripts/`, or `agents/` resources. Upload or install the full skill folder, not only `SKILL.md`.

## How To Use

### Claude, Perplexity, or SKILL.md-Compatible Agents

Upload one of these full folders:

```text
skills/cruise-package-calculator/
skills/cruise-line-comparator/
skills/shore-excursion-optimizer/
```

### Codex Local Skills

Copy the live skills into your local Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/cruise-package-calculator ~/.codex/skills/
cp -R skills/cruise-line-comparator ~/.codex/skills/
cp -R skills/shore-excursion-optimizer ~/.codex/skills/
```

### GPT Store, Poe, Gemini, or Claude Projects

Open the relevant `SYSTEM_PROMPT.md` file and use the platform-specific variant:

- GPT Store: Variant B
- Poe: Variant C
- Gemini Gem: Variant D
- Claude Project: Variant E

## Example Prompts

```text
I am taking a 7-night Royal Caribbean cruise. The Deluxe Beverage Package is $89 per person per day before gratuity. I drink about 4 cocktails, 2 sodas, and 1 coffee per day. Is it worth it?
```

```text
We are a family of four comparing Carnival and Royal Caribbean for a 7-night Caribbean cruise from Florida. Budget is around $4,000. Which line fits better?
```

```text
We are in Cozumel from 8:00 AM to 4:30 PM with two kids. Should we book the ship excursion, use an independent snorkeling tour, or do a self-guided beach day?
```

## SEO Keywords

Cruise AI skills, cruise package calculator, cruise drink package calculator, cruise Wi-Fi package calculator, cruise line comparison, Carnival vs Royal Caribbean, NCL vs MSC cruise comparison, cruise shore excursion planner, ship excursion vs independent tour, cruise port day planner, cruise travel AI tools.

## License

MIT. You can use, fork, adapt, and publish these skills commercially.
