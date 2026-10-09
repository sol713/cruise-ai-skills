# Drink calculator CLI contract

The Python helper calculates **drink packages only**. Wi-Fi, dining, photo,
bundle, and other package types return an explicit `note` that their handler
is not implemented. Their formulas remain available for inline use in the
skill; the script does not calculate those packages or optimize bundles.

## Run and test

Use Python 3.10 or newer. There are no third-party dependencies, installation
steps, API keys, network requests, or booking services. From the repository root:

```bash
python3 -m unittest discover -s tests -v
```

Run the supplied example:

```bash
python3 skills/cruise-package-calculator/scripts/calculator.py \
  < skills/cruise-package-calculator/examples/drink-package.input.json
```

[Input](drink-package.input.json) and [expected output](drink-package.output.json)
are checked together by the test suite. They reproduce the existing
[Royal Caribbean example](royal-caribbean-drink-package.md), using an illustrative
user quote of $89 per adult per day, seven nights, two adults, and each adult's
daily estimate of four cocktails, two sodas, and one premium coffee. These are
example assumptions, not a current offer or verified policy.

The result is a $1,470.28 adult package total, $966.00 adult à-la-carte total,
and $504.28 extra cost for the package. With the helper's default scoring
inputs, the score is 33.0 and the verdict is `SKIP (lean)`.

## Input fields

The request must be a JSON object. `packages` defaults to `[]` and must be an
array of objects; omitted or empty packages return `{"results": []}`.
The following fields are validated when a drink package is evaluated:

| Request field | Requirement / default |
|---|---|
| `cruise_line` | Required string; known names use the existing gratuity table, unknown strings retain the 18% fallback |
| `nights` | Required positive integer; multiplier for the quoted daily price |
| `adults` | Non-negative integer, default `1`; all adults use the same daily consumption estimate |
| `kids` | Non-negative integer, default `0`; **not included in the calculation** |
| `consumption_per_adult_per_day` | Object, default `{}`; recognized quantities must be finite non-negative numbers |
| `convenience_score` | Finite number from 0 to 100, default `60` |
| `risk_score` | Finite number from 0 to 100, default `60` |
| `pre_cruise_discount_pct` | Finite number, default `15`; negative values are allowed for a pre-cruise markup |

Recognized consumption keys are `cocktails`, `beers`, `wine_glasses`, `sodas`,
`premium_coffees`, and `bottled_waters`. Omitted quantities default to zero;
fractional daily averages such as `0.5` are accepted. Unrecognized consumption
keys and extra request metadata are ignored. Booleans and numeric strings are
not accepted as numbers. Nights and people counts must be integers.

| Drink package field | Requirement / default |
|---|---|
| `type` | `"drink"` selects calculation; other or omitted types return an unimplemented note |
| `daily_price` | Required finite non-negative number in USD, per adult per day; `0` is valid for a free package |
| `name` | Optional output label, default `"drink package"` |
| `gratuity_already_included` | Boolean, default `false`; `true` prevents an additional gratuity |
| `purchased` | Descriptive metadata only; does not change costs or infer a discount |

The helper retains its existing scoring defaults even when `purchased` is
`"onboard"`. Supply `pre_cruise_discount_pct: 0` if there is no pre-cruise
discount, and choose convenience/risk scores from the
[rubric](../references/value_score_rubric.md) for the user's situation.
Missing consumption is treated as zero for compatibility; agents should gather
the user's consumption before making a recommendation, as required by `SKILL.md`.

## What the result means

Each package produces one result, in input order. Multiple drink packages are
evaluated independently against the same adult consumption; their totals are
not added together or optimized.

- `package_total_for_household` is effective daily package price × nights × adults.
- `alacarte_total_for_household` uses all six drink categories × nights × adults.
- `net_position` is package total minus à-la-carte total: positive means the
  package costs more; negative means it saves money.
- `savings_pct` is `(à-la-carte total - package total) / à-la-carte total × 100`.
  When the à-la-carte total is zero, the existing helper uses `-100` as a sentinel,
  not a measured percentage. Zero adults remain valid and yield zero household
  costs with that same sentinel; the verdict is not meaningful for that case.
- `breakeven_drinks_per_day` means **$14 cocktail equivalents per adult**. It
  does not use a weighted mixed-drink average, despite the broader skill formula.
- `user_drinks_per_day` counts **alcoholic drinks only** (cocktails, beer, wine)
  per adult. Sodas, coffee, and water still contribute to the à-la-carte cost.
- Money rounds to two decimal places; savings, break-even, and score round to
  one. `value_score` uses the existing weighted rubric and the supplied/default
  scores; `verdict` is derived from that score, not solely from cash savings.

Unit-price assumptions remain $14 cocktails, $9 beer, $13 wine, $4 soda,
$5 premium coffee, and $4.50 bottled water. The existing gratuity table uses
20% for NCL / Norwegian Cruise Line and Celebrity, 0% for Princess and Disney,
and 18% for the other listed lines and unknown strings. These are the helper's
static assumptions, **not verified current prices, policy, or package availability**.
The script does not model exclusions, drink caps, port-day consumption changes,
kids' purchases, different consumption by adult, or other bundle benefits.
Verify real quotes and inclusions separately; use `gratuity_already_included`
when the user's quote includes gratuity.

## Errors for agents

Success exits with status `0` and emits `{"results": [...]}` on stdout.
Invalid JSON, malformed containers, missing required drink fields, invalid
counts/prices/consumption/scores, or arithmetic overflow exit with status `1`
and emit one `{"error": "..."}` JSON object on stdout, without a traceback.
No partial results are emitted if a later package fails. `NaN`, `Infinity`,
and `-Infinity` JSON tokens are rejected; computed non-finite values are also
rejected so agents receive standard JSON.

For example, replacing the example's `daily_price` with `-1` returns:

```json
{"error": "packages[0]: package.daily_price must be >= 0"}
```

Drink-specific fields are not required for an unsupported-only request:

```json
{"packages": [{"type": "wifi", "name": "Example Wi-Fi"}]}
```

Its result contains `package_name`, `type`, and the unimplemented `note`;
it contains no price, savings, score, or verdict.
