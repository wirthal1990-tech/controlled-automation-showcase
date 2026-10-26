"""Synthetic technical evidence exercise; no commercial scoring or external write."""
import argparse
import hashlib
import json
from pathlib import Path
import re

CRITERIA = ("format_checked", "review_note_present")


def valid_record(record):
    if (type(record) is not dict or set(record) != {"object", "evidence"}
            or type(record["object"]) is not str
            or re.fullmatch(r"EXAMPLE_ORG_[A-Z]", record["object"]) is None
            or type(record["evidence"]) is not list
            or not 1 <= len(record["evidence"]) <= 16):
        return False
    seen = set()
    for evidence in record["evidence"]:
        if (type(evidence) is not dict or set(evidence) != {"id", "criterion", "observed"}
                or type(evidence["id"]) is not str
                or re.fullmatch(r"EVIDENCE_[A-Z]", evidence["id"]) is None
                or evidence["id"] in seen
                or evidence["criterion"] not in CRITERIA
                or type(evidence["observed"]) is not bool):
            return False
        seen.add(evidence["id"])
    return True


def record_hash(record):
    """Sorted-key compact ASCII JSON; evidence array order remains significant."""
    if not valid_record(record):
        raise ValueError("INVALID_RECORD")
    return hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=True, allow_nan=False).encode("ascii")).hexdigest()


def assess(record):
    if not valid_record(record):
        return {"status": "NO_GO", "demo_score": 0, "evidence_ids": [], "reasons": ["INVALID_RECORD"]}
    values = {criterion: set() for criterion in CRITERIA}
    for evidence in record["evidence"]:
        values[evidence["criterion"]].add(evidence["observed"])
    reasons = []
    if any(not observed for observed in values.values()):
        reasons.append("MISSING_EVIDENCE")
    if any(len(observed) > 1 for observed in values.values()):
        reasons.append("CONTRADICTORY_EVIDENCE")
    if any(False in observed for observed in values.values()):
        reasons.append("NEGATIVE_EVIDENCE")
    # Two equally weighted technical checks, 50 points each; no business meaning.
    score = 50 * sum(True in observed for observed in values.values())
    return {"status": "NO_GO" if reasons else "REVIEW_REQUIRED", "demo_score": score,
            "evidence_ids": sorted(item["id"] for item in record["evidence"]), "reasons": reasons}


class Simulator:
    def __init__(self):
        self.releases = []
        self.consumed_hashes = set()

    def release(self, record, approval):
        if assess(record)["status"] != "REVIEW_REQUIRED":
            return {"status": "NOT_RELEASED", "reason": "EVIDENCE_BLOCKED"}
        digest = record_hash(record)
        if (type(approval) is not dict or set(approval) != {"decision", "record_sha256"}
                or approval["decision"] != "APPROVED"
                or approval["record_sha256"] != digest):
            return {"status": "NOT_RELEASED", "reason": "APPROVAL_REQUIRED"}
        if digest in self.consumed_hashes:
            return {"status": "NOT_RELEASED", "reason": "REPLAY"}
        self.consumed_hashes.add(digest)
        self.releases.append(record["object"])
        return {"status": "RELEASED_SIMULATED", "record_sha256": digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=["review", "missing", "contradiction", "unapproved", "approved", "tampered"])
    scenario = parser.parse_args().scenario
    fixtures = json.loads(Path(__file__).with_name("fixtures.json").read_text())
    record = fixtures[scenario] if scenario in ("missing", "contradiction") else fixtures["complete"]
    simulator = Simulator()
    if scenario in ("review", "missing", "contradiction"):
        result = assess(record)
    else:
        # Scripted fixture input simulates explicit approval; it authenticates nobody.
        approval = {"decision": "APPROVED", "record_sha256": record_hash(record)} if scenario != "unapproved" else None
        if scenario == "tampered":
            record["object"] = "EXAMPLE_ORG_B"
        result = simulator.release(record, approval)
    print(json.dumps(result | {"virtual_releases": len(simulator.releases)}, sort_keys=True))
    return 0 if result["status"] in ("REVIEW_REQUIRED", "RELEASED_SIMULATED") else 3


if __name__ == "__main__":
    raise SystemExit(main())
