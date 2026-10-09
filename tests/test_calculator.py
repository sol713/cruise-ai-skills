"""Offline checks for the calculator's JSON CLI and existing arithmetic."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cruise-package-calculator"
SCRIPT = SKILL / "scripts" / "calculator.py"
spec = importlib.util.spec_from_file_location("calculator", SCRIPT)
calculator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calculator)


def request():
    return json.loads((SKILL / "examples" / "drink-package.input.json").read_text())


class CalculatorTests(unittest.TestCase):
    def run_cli(self, raw):
        return subprocess.run(
            [sys.executable, str(SCRIPT)], input=raw, text=True,
            capture_output=True, cwd=ROOT, timeout=10,
        )

    def strict_json(self, raw):
        def reject_constant(value):
            self.fail(f"Output contains non-JSON constant {value}")
        return json.loads(raw, parse_constant=reject_constant)

    def assert_error(self, raw, field=None):
        run = self.run_cli(raw)
        self.assertEqual(run.returncode, 1, run.stdout + run.stderr)
        self.assertEqual(run.stderr, "", run.stderr)
        output = self.strict_json(run.stdout)
        self.assertEqual(set(output), {"error"})
        self.assertIsInstance(output["error"], str)
        if field:
            self.assertIn(field, output["error"])

    def test_documented_example_through_cli(self):
        expected = json.loads((SKILL / "examples" / "drink-package.output.json").read_text())
        run = self.run_cli(json.dumps(request()))
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertEqual(run.stderr, "")
        self.assertEqual(self.strict_json(run.stdout), expected)

    def test_empty_and_malformed_json(self):
        for raw in ("", " \n", "{", "{} trailing"):
            with self.subTest(raw=raw):
                self.assert_error(raw)

    def test_invalid_request_structure(self):
        for req, field in (
            (None, "request"), ([], "request"), (True, "request"),
            (42, "request"), ("drink", "request"),
            ({"packages": None}, "packages"),
            ({"packages": {}}, "packages"),
            ({"packages": "drink"}, "packages"),
            ({"packages": [None]}, "packages[0]"),
            ({"packages": ["drink"]}, "packages[0]"),
            ({"packages": [[]]}, "packages[0]"),
        ):
            with self.subTest(req=req):
                self.assert_error(json.dumps(req), field)

    def test_missing_required_drink_fields(self):
        for field in ("cruise_line", "nights", "daily_price"):
            req = request()
            target = req["packages"][0] if field == "daily_price" else req
            del target[field]
            with self.subTest(field=field):
                self.assert_error(json.dumps(req), field)

    def test_invalid_cruise_line_type(self):
        for value in (None, [], {}, 42, False):
            req = request()
            req["cruise_line"] = value
            with self.subTest(value=value):
                self.assert_error(json.dumps(req), "cruise_line")

    def test_nights_and_people_are_integer_counts(self):
        for field in ("nights", "adults", "kids"):
            invalid = [-1, 1.5, "2", True, None]
            if field == "nights":
                invalid.append(0)
            for value in invalid:
                req = request()
                req[field] = value
                with self.subTest(field=field, value=value):
                    self.assert_error(json.dumps(req), field)

    def test_invalid_price(self):
        for value in (-1, "89", True, None, [], {}):
            req = request()
            req["packages"][0]["daily_price"] = value
            with self.subTest(value=value):
                self.assert_error(json.dumps(req), "daily_price")

    def test_gratuity_flag_requires_boolean(self):
        for value in ("false", 0, 1, None, []):
            req = request()
            req["packages"][0]["gratuity_already_included"] = value
            with self.subTest(value=value):
                self.assert_error(json.dumps(req), "gratuity_already_included")

    def test_invalid_consumption_structure(self):
        for value in (None, [], "four", 4):
            req = request()
            req["consumption_per_adult_per_day"] = value
            with self.subTest(value=value):
                self.assert_error(json.dumps(req), "consumption_per_adult_per_day")

    def test_invalid_consumption_values(self):
        for drink in calculator.UNIT_PRICES:
            for value in (-1, "4", True, None, []):
                req = request()
                req["consumption_per_adult_per_day"][drink] = value
                with self.subTest(drink=drink, value=value):
                    self.assert_error(json.dumps(req), drink)

    def test_scores_follow_zero_to_100_rubric(self):
        for field in ("convenience_score", "risk_score"):
            for value in (-1, 101, "60", True, None):
                req = request()
                req[field] = value
                with self.subTest(field=field, value=value):
                    self.assert_error(json.dumps(req), field)

    def test_invalid_discount_type(self):
        for value in ("15", True, None):
            req = request()
            req["pre_cruise_discount_pct"] = value
            with self.subTest(value=value):
                self.assert_error(json.dumps(req), "pre_cruise_discount_pct")

    def test_nonstandard_json_constants(self):
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(token=token):
                self.assert_error(json.dumps(request()).replace('"daily_price": 89', f'"daily_price": {token}'))

    def test_nonfinite_exponents_and_arithmetic_overflow(self):
        cases = []
        for field in ("daily_price", "convenience_score", "risk_score", "pre_cruise_discount_pct"):
            req = request()
            target = req["packages"][0] if field == "daily_price" else req
            target[field] = 1e308
            if field != "pre_cruise_discount_pct":
                cases.append(json.dumps(req))
            cases.append(json.dumps(req).replace("1e+308", "1e309"))
        req = request()
        req["consumption_per_adult_per_day"]["cocktails"] = 1e308
        cases.append(json.dumps(req))
        req = request()
        req["nights"] = 10 ** 400
        cases.append(json.dumps(req))
        for raw in cases:
            with self.subTest(raw=raw[:120]):
                self.assert_error(raw)

    def test_invalid_later_package_returns_no_partial_success(self):
        req = request()
        req["packages"].append({"type": "drink", "daily_price": -1})
        self.assert_error(json.dumps(req), "packages[1]")

    def test_direct_drink_analysis_rejects_invalid_inputs(self):
        req = request()
        req["packages"][0]["daily_price"] = -1
        with self.assertRaises(ValueError):
            calculator.analyze_drink_package(req["packages"][0], req)

    def test_absent_or_empty_packages_remain_empty_success(self):
        for req in ({}, {"packages": []}):
            with self.subTest(req=req):
                run = self.run_cli(json.dumps(req))
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertEqual(self.strict_json(run.stdout), {"results": []})

    def test_optional_defaults_and_zero_consumption(self):
        req = {"cruise_line": "Royal Caribbean", "nights": 7}
        result = calculator.analyze_drink_package({"daily_price": 89}, req)
        self.assertEqual(result["package_name"], "drink package")
        self.assertEqual(result["package_total_for_household"], 735.14)
        self.assertEqual(result["alacarte_total_for_household"], 0)
        self.assertEqual(result["savings_pct"], -100)
        self.assertEqual(result["user_drinks_per_day"], 0)
        self.assertEqual(result["value_score"], 33)

    def test_zero_price_and_zero_adults_remain_supported(self):
        req = request()
        req["packages"][0]["daily_price"] = 0
        result = calculator.analyze_drink_package(req["packages"][0], req)
        self.assertEqual(result["package_total_for_household"], 0)
        self.assertEqual(result["net_position"], -966)
        self.assertEqual(result["savings_pct"], 100)
        req["adults"] = 0
        result = calculator.analyze_drink_package(req["packages"][0], req)
        self.assertEqual(result["alacarte_total_for_household"], 0)
        self.assertEqual(result["net_position"], 0)
        self.assertEqual(result["savings_pct"], -100)

    def test_fractional_consumption_and_ignored_metadata(self):
        req = request()
        req["consumption_per_adult_per_day"] = {"cocktails": 0.5, "sodas": 1.5, "notes": "daily average"}
        result = calculator.analyze_drink_package(req["packages"][0], req)
        self.assertEqual(result["alacarte_total_for_household"], 182)
        self.assertEqual(result["user_drinks_per_day"], 0.5)

    def test_kids_do_not_change_adult_totals(self):
        req = request()
        baseline = calculator.analyze_drink_package(req["packages"][0], req)
        req["kids"] = 3
        self.assertEqual(calculator.analyze_drink_package(req["packages"][0], req), baseline)

    def test_household_scaling(self):
        req = request()
        baseline = calculator.analyze_drink_package(req["packages"][0], req)
        req["nights"] *= 2
        req["adults"] *= 2
        result = calculator.analyze_drink_package(req["packages"][0], req)
        for key in ("package_total_for_household", "alacarte_total_for_household", "net_position"):
            self.assertAlmostEqual(result[key], baseline[key] * 4, places=2)
        for key in ("savings_pct", "breakeven_drinks_per_day", "user_drinks_per_day", "value_score", "verdict"):
            self.assertEqual(result[key], baseline[key])

    def test_existing_gratuity_table_and_fallback(self):
        for line, expected in (
            ("Royal Caribbean", 118), ("Carnival", 118), ("MSC", 118),
            ("Holland America", 118), ("NCL", 120),
            ("Norwegian Cruise Line", 120), ("Celebrity", 120),
            ("Princess", 100), ("Disney", 100), ("unknown line", 118),
        ):
            with self.subTest(line=line):
                self.assertAlmostEqual(calculator.effective_daily_cost(100, line, False), expected)
                self.assertEqual(calculator.effective_daily_cost(100, line, True), 100)

    def test_included_gratuity_and_alcohol_only_count(self):
        req = request()
        req["packages"][0]["gratuity_already_included"] = True
        req["consumption_per_adult_per_day"] = dict.fromkeys(calculator.UNIT_PRICES, 1)
        result = calculator.analyze_drink_package(req["packages"][0], req)
        self.assertEqual(result["package_total_for_household"], 1246)
        self.assertEqual(result["alacarte_total_for_household"], 693)
        self.assertEqual(result["user_drinks_per_day"], 3)
        self.assertEqual(result["breakeven_drinks_per_day"], 6.4)

    def test_savings_score_thresholds(self):
        for savings, expected in ((30, 50), (29.9, 40), (15, 40), (14.9, 30), (5, 30), (4.9, 20), (0, 20), (-0.1, 12.5), (-5, 12.5), (-5.1, 0)):
            with self.subTest(savings=savings):
                self.assertEqual(calculator.value_score(savings, 0, 0, -1), expected)

    def test_discount_score_thresholds(self):
        for discount, expected in ((25, 15), (24.9, 12), (15, 12), (14.9, 7.5), (5, 7.5), (4.9, 3), (0, 3), (-0.1, 0)):
            with self.subTest(discount=discount):
                self.assertEqual(calculator.value_score(-10, 0, 0, discount), expected)

    def test_negative_and_large_finite_discounts_remain_supported(self):
        req = request()
        for discount, expected_score in ((-10, 21), (1e308, 36)):
            req["pre_cruise_discount_pct"] = discount
            with self.subTest(discount=discount):
                result = calculator.analyze_drink_package(req["packages"][0], req)
                self.assertEqual(result["value_score"], expected_score)

    def test_verdict_thresholds(self):
        for score, expected in ((100, "BUY"), (75, "BUY"), (74.9, "BUY (lean)"), (60, "BUY (lean)"), (59.9, "DEPENDS"), (45, "DEPENDS"), (44.9, "SKIP (lean)"), (30, "SKIP (lean)"), (29.9, "SKIP"), (0, "SKIP")):
            with self.subTest(score=score):
                self.assertEqual(calculator.verdict_from_score(score), expected)

    def test_mixed_packages_preserve_order_and_mark_unimplemented(self):
        req = request()
        req["packages"].extend({"type": kind, "name": f"example {kind}"} for kind in ("wifi", "dining", "photo", "bundle", "other"))
        run = self.run_cli(json.dumps(req))
        self.assertEqual(run.returncode, 0, run.stderr)
        results = self.strict_json(run.stdout)["results"]
        self.assertEqual(len(results), 6)
        self.assertEqual(results[0]["package_total_for_household"], 1470.28)
        for result, kind in zip(results[1:], ("wifi", "dining", "photo", "bundle", "other")):
            self.assertEqual(set(result), {"package_name", "type", "note"})
            self.assertEqual(result["type"], kind)
            self.assertIn("not implemented", result["note"])

    def test_non_drink_packages_need_no_drink_inputs(self):
        run = self.run_cli('{"packages": [{"type": "wifi"}]}')
        self.assertEqual(run.returncode, 0, run.stderr)
        self.assertIn("not implemented", self.strict_json(run.stdout)["results"][0]["note"])


if __name__ == "__main__":
    unittest.main()
