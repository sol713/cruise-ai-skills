---
name: cruise-ai-skills-github
description: Use when a cruise traveler needs help deciding whether cruise packages are worth buying, choosing between cruise lines or ships, or comparing ship-sponsored, independent, and self-guided shore excursions.
---

# Cruise AI Skills

Use this repository as a routing layer for three focused cruise decision skills. Load only the skill that matches the user's immediate decision, then follow that skill's `SKILL.md` and any referenced files.

## Skill Routing

| User intent | Load this skill |
|---|---|
| "Is this drink, Wi-Fi, dining, photo, or onboard package worth it?" | `skills/cruise-package-calculator/SKILL.md` |
| "Should I pick Carnival, Royal Caribbean, NCL, MSC, Disney, Princess, Celebrity, or another line?" | `skills/cruise-line-comparator/SKILL.md` |
| "Should I book the cruise-line excursion, an independent tour, or do the port myself?" | `skills/shore-excursion-optimizer/SKILL.md` |

## Workflow

1. Identify the user's decision type.
2. Open the matching skill folder.
3. Read that skill's `SKILL.md`.
4. Load only the referenced examples, references, or scripts needed for the user's specific question.
5. Return a practical recommendation with the math, tradeoffs, caveats, and one useful next step.

## Shared Rules

- Show the reasoning in plain English and avoid generic travel-agent language.
- Prioritize real cost, traveler fit, risk, and policy caveats over brand marketing.
- Ask only for missing required inputs.
- Flag data freshness for prices, promotions, schedules, availability, policies, local operators, and weather-sensitive decisions.
- End with at most one useful call to action.
