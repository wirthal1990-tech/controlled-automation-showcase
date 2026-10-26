"""Behavior tests: changed bindings, malformed input or replay must not act."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from demo import Simulator, request_hash

FIXTURE = json.loads(Path(__file__).with_name("fixtures.json").read_text())
DIGEST = "cab4fd57fb3001f14c95ea44255f1a6ab97453a3a01b14fc3caff6d7dc7b49a6"


class ApprovalTests(unittest.TestCase):
    def setUp(self):
        self.request = copy.deepcopy(FIXTURE["request"])
        self.approval = copy.deepcopy(FIXTURE["approval"])
        self.simulator = Simulator()

    def refuse(self, request, approval, now=100):
        before = dict(self.simulator.reports)
        result = self.simulator.execute(request, approval, now)
        self.assertEqual(result["status"], "REFUSED")
        self.assertEqual(self.simulator.reports, before)

    def test_valid_approval_executes_exactly_the_bound_virtual_report(self):
        self.assertEqual(self.simulator.execute(self.request, self.approval, 100)["status"], "EXECUTED")
        self.assertEqual(self.simulator.reports, {"SYNTHETIC_REPORT_A": "synthetic report"})

    def test_canonical_hash_is_independently_fixed_and_order_independent(self):
        self.assertEqual(request_hash(self.request), DIGEST)
        self.assertEqual(request_hash(dict(reversed(list(self.request.items())))), DIGEST)

    def test_missing_approval_refuses(self):
        self.refuse(self.request, None)

    def test_denied_approval_refuses(self):
        self.approval["decision"] = "DENIED"
        self.refuse(self.request, self.approval)

    def test_wrong_hash_refuses(self):
        self.approval["request_sha256"] = "0" * 64
        self.refuse(self.request, self.approval)

    def test_mutated_payload_cannot_reuse_old_approval(self):
        for field, value in (("text", "changed report"), ("report", "SYNTHETIC_REPORT_B"), ("action", "other")):
            with self.subTest(field=field):
                changed = dict(self.request, **{field: value})
                self.refuse(changed, self.approval)

    def test_expiry_boundary_and_past_refuse(self):
        self.refuse(self.request, self.approval, 200)
        self.refuse(self.request, self.approval, 201)

    def test_replay_refuses_and_preserves_first_result(self):
        self.assertEqual(self.simulator.execute(self.request, self.approval, 100)["status"], "EXECUTED")
        self.refuse(self.request, self.approval)
        self.approval["approval_id"] = "APPROVAL_B"
        self.refuse(self.request, self.approval)

    def test_reused_approval_id_for_different_request_refuses(self):
        self.assertEqual(self.simulator.execute(self.request, self.approval, 100)["status"], "EXECUTED")
        self.request["report"] = "SYNTHETIC_REPORT_B"
        self.approval["request_sha256"] = request_hash(self.request)
        self.refuse(self.request, self.approval)

    def test_invalid_request_shape_types_and_unknown_fields_refuse(self):
        bad = [None, [], {}, dict(self.request, extra=True), dict(self.request, text=1),
               dict(self.request, report="../outside"), dict(self.request, text=""),
               dict(self.request, text="x" * 81), dict(self.request, text="\u2603")]
        for request in bad:
            with self.subTest(request_type=type(request).__name__):
                self.refuse(request, self.approval)

    def test_invalid_approval_shape_types_and_unknown_fields_refuse(self):
        for approval in ([], {}, True, dict(self.approval, extra=True),
                         dict(self.approval, expires_at=True), dict(self.approval, expires_at=200.0),
                         dict(self.approval, decision=True), dict(self.approval, approval_id=""),
                         dict(self.approval, request_sha256=1)):
            with self.subTest(approval_type=type(approval).__name__):
                self.refuse(self.request, approval)

    def test_invalid_clock_refuses(self):
        for now in (True, None, -1, 100.0, "100"):
            with self.subTest(now_type=type(now).__name__):
                self.refuse(self.request, self.approval, now)

    def test_failed_attempt_does_not_consume_valid_approval(self):
        self.refuse(self.request, dict(self.approval, decision="DENIED"))
        self.assertEqual(self.simulator.execute(self.request, self.approval, 100)["status"], "EXECUTED")

    def test_hash_rejects_invalid_request_instead_of_binding_it(self):
        with self.assertRaisesRegex(ValueError, "INVALID_REQUEST"):
            request_hash(dict(self.request, extra=True))

    def test_cli_scenarios_enforce_exit_codes_and_deterministic_output(self):
        for scenario, status, count, code in (("approved", "EXECUTED", 1, 0),
                ("missing", "REFUSED", 0, 3), ("denied", "REFUSED", 0, 3),
                ("tampered", "REFUSED", 0, 3), ("expired", "REFUSED", 0, 3),
                ("replay", "REFUSED", 1, 3)):
            with self.subTest(scenario=scenario):
                cmd = [sys.executable, "-B", str(Path(__file__).with_name("demo.py")), scenario]
                first = subprocess.run(cmd, capture_output=True, text=True)
                second = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual((first.returncode, second.returncode), (code, code))
                self.assertEqual(first.stderr, "")
                self.assertEqual(first.stdout, second.stdout)
                result = json.loads(first.stdout)
                self.assertEqual(result["status"], status)
                self.assertEqual(result["virtual_reports"], count)

    def test_cli_invalid_scenario_is_usage_error(self):
        result = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("demo.py")), "unknown"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
