"""Evidence must support review; human approval must bind the same input."""
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

from demo import Simulator, assess, record_hash

FIXTURES = json.loads(Path(__file__).with_name("fixtures.json").read_text())


def approval_for(record):
    # Independent test-side serialization, never the production digest helper.
    digest = hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"),
                                       ensure_ascii=True, allow_nan=False).encode("ascii")).hexdigest()
    return {"decision": "APPROVED", "record_sha256": digest}


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.record = copy.deepcopy(FIXTURES["complete"])
        self.simulator = Simulator()

    def not_released(self, record, approval):
        before = list(self.simulator.releases)
        self.assertEqual(self.simulator.release(record, approval)["status"], "NOT_RELEASED")
        self.assertEqual(self.simulator.releases, before)

    def test_complete_evidence_requires_review_with_resolving_support(self):
        result = assess(self.record)
        self.assertEqual(result, {"status": "REVIEW_REQUIRED", "demo_score": 100,
                                 "evidence_ids": ["EVIDENCE_A", "EVIDENCE_B"], "reasons": []})
        self.assertEqual(self.simulator.releases, [])

    def test_missing_required_evidence_is_no_go(self):
        result = assess(FIXTURES["missing"])
        self.assertEqual(result["status"], "NO_GO")
        self.assertEqual(result["demo_score"], 50)
        self.assertIn("MISSING_EVIDENCE", result["reasons"])

    def test_contradiction_blocks_even_with_score_100(self):
        result = assess(FIXTURES["contradiction"])
        self.assertEqual(result["demo_score"], 100)
        self.assertEqual(result["status"], "NO_GO")
        self.assertIn("CONTRADICTORY_EVIDENCE", result["reasons"])

    def test_explicit_false_evidence_blocks(self):
        self.record["evidence"][1]["observed"] = False
        self.assertEqual(assess(self.record)["status"], "NO_GO")

    def test_missing_or_denied_human_approval_cannot_release(self):
        for approval in (None, False, True, {}, approval_for(self.record) | {"decision": "DENIED"}):
            with self.subTest(approval_type=type(approval).__name__):
                self.not_released(self.record, approval)

    def test_exact_approval_releases_only_in_memory(self):
        result = self.simulator.release(self.record, approval_for(self.record))
        self.assertEqual(result["status"], "RELEASED_SIMULATED")
        self.assertEqual(self.simulator.releases, ["EXAMPLE_ORG_A"])

    def test_changed_object_or_evidence_invalidates_old_approval(self):
        approval = approval_for(self.record)
        changed = copy.deepcopy(self.record)
        changed["object"] = "EXAMPLE_ORG_B"
        self.not_released(changed, approval)
        changed = copy.deepcopy(self.record)
        changed["evidence"][1]["id"] = "EVIDENCE_C"
        self.not_released(changed, approval)

    def test_missing_or_conflicting_evidence_never_releases_even_if_approved(self):
        for name in ("missing", "contradiction"):
            self.not_released(FIXTURES[name], approval_for(FIXTURES[name]))

    def test_replay_cannot_duplicate_simulated_release(self):
        approval = approval_for(self.record)
        self.assertEqual(self.simulator.release(self.record, approval)["status"], "RELEASED_SIMULATED")
        self.not_released(self.record, approval)

    def test_unexpected_record_or_evidence_shapes_fail_closed(self):
        bad = [None, [], {}, self.record | {"score": 100}, self.record | {"object": ""},
               self.record | {"object": "REAL_NAME"}, self.record | {"evidence": []},
               self.record | {"evidence": None}, self.record | {"evidence": [True]},
               self.record | {"evidence": [self.record["evidence"][0]] * 2}]
        for record in bad:
            with self.subTest(record_type=type(record).__name__):
                self.assertEqual(assess(record)["status"], "NO_GO")
                self.not_released(record, None)

    def test_invalid_evidence_values_and_empty_ids_fail_closed(self):
        for field, value in (("id", ""), ("observed", 1), ("observed", "true"),
                             ("criterion", "unknown"), ("extra", True)):
            changed = copy.deepcopy(self.record)
            changed["evidence"][0][field] = value
            with self.subTest(field=field):
                self.assertEqual(assess(changed)["status"], "NO_GO")
                self.not_released(changed, None)

    def test_approval_extra_fields_or_malformed_hash_refuse(self):
        approval = approval_for(self.record)
        for changed in (approval | {"extra": True}, approval | {"record_sha256": "0" * 64},
                        approval | {"record_sha256": 1}):
            self.not_released(self.record, changed)

    def test_hash_binds_order_independent_object_keys(self):
        self.assertEqual(record_hash(self.record), approval_for(self.record)["record_sha256"])
        self.assertEqual(record_hash(dict(reversed(list(self.record.items())))), record_hash(self.record))

    def test_refusal_does_not_consume_future_valid_release(self):
        self.not_released(self.record, None)
        self.assertEqual(self.simulator.release(self.record, approval_for(self.record))["status"], "RELEASED_SIMULATED")

    def test_hash_rejects_invalid_record_instead_of_binding_it(self):
        with self.assertRaisesRegex(ValueError, "INVALID_RECORD"):
            record_hash(self.record | {"extra": True})

    def test_cli_scenarios_enforce_exit_codes_and_deterministic_output(self):
        for scenario, status, count, code in (("review", "REVIEW_REQUIRED", 0, 0),
                ("missing", "NO_GO", 0, 3), ("contradiction", "NO_GO", 0, 3),
                ("unapproved", "NOT_RELEASED", 0, 3), ("approved", "RELEASED_SIMULATED", 1, 0),
                ("tampered", "NOT_RELEASED", 0, 3)):
            with self.subTest(scenario=scenario):
                cmd = [sys.executable, "-B", str(Path(__file__).with_name("demo.py")), scenario]
                first = subprocess.run(cmd, capture_output=True, text=True)
                second = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual((first.returncode, second.returncode), (code, code))
                self.assertEqual(first.stderr, "")
                self.assertEqual(first.stdout, second.stdout)
                result = json.loads(first.stdout)
                self.assertEqual(result["status"], status)
                self.assertEqual(result["virtual_releases"], count)

    def test_cli_invalid_scenario_is_usage_error(self):
        result = subprocess.run([sys.executable, "-B", str(Path(__file__).with_name("demo.py")), "unknown"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()
