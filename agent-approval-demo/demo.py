"""Synthetic in-memory approval exercise; no authenticated approval channel."""
import argparse
import hashlib
import json
from pathlib import Path
import re


def valid_request(request):
    return (type(request) is dict and set(request) == {"action", "report", "text"}
            and request["action"] == "write_report"
            and type(request["report"]) is str
            and re.fullmatch(r"SYNTHETIC_REPORT_[A-Z]", request["report"]) is not None
            and type(request["text"]) is str
            and re.fullmatch(r"[A-Za-z0-9 _.\-]{1,80}", request["text"]) is not None)


def request_hash(request):
    """Sorted-key compact ASCII JSON over the strict flat request schema only."""
    if not valid_request(request):
        raise ValueError("INVALID_REQUEST")
    data = json.dumps(request, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True, allow_nan=False).encode("ascii")
    return hashlib.sha256(data).hexdigest()


class Simulator:
    def __init__(self):
        self.reports = {}
        self.consumed_ids = set()
        self.consumed_hashes = set()

    def execute(self, request, approval, now):
        def refuse(reason):
            return {"status": "REFUSED", "reason": reason}

        if not valid_request(request):
            return refuse("INVALID_REQUEST")
        request = dict(request)
        if type(now) is not int or now < 0:
            return refuse("INVALID_CLOCK")
        if type(approval) is not dict or set(approval) != {
                "approval_id", "request_sha256", "decision", "expires_at"}:
            return refuse("INVALID_APPROVAL")
        approval = dict(approval)
        if (type(approval["approval_id"]) is not str
                or re.fullmatch(r"APPROVAL_[A-Z]", approval["approval_id"]) is None
                or type(approval["expires_at"]) is not int
                or approval["expires_at"] < 0
                or type(approval["request_sha256"]) is not str
                or re.fullmatch(r"[0-9a-f]{64}", approval["request_sha256"]) is None
                or approval["decision"] not in ("APPROVED", "DENIED")):
            return refuse("INVALID_APPROVAL")
        digest = request_hash(request)
        if approval["decision"] != "APPROVED":
            return refuse("DENIED")
        if approval["request_sha256"] != digest:
            return refuse("HASH_MISMATCH")
        if now >= approval["expires_at"]:
            return refuse("EXPIRED")
        if approval["approval_id"] in self.consumed_ids or digest in self.consumed_hashes:
            return refuse("REPLAY")
        self.consumed_ids.add(approval["approval_id"])
        self.consumed_hashes.add(digest)
        self.reports[request["report"]] = request["text"]
        return {"status": "EXECUTED", "request_sha256": digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", choices=["approved", "missing", "denied", "tampered", "expired", "replay"])
    scenario = parser.parse_args().scenario
    fixture = json.loads(Path(__file__).with_name("fixtures.json").read_text())
    request, approval, now = fixture["request"], fixture["approval"], fixture["now"]
    simulator = Simulator()
    if scenario == "missing":
        approval = None
    elif scenario == "denied":
        approval["decision"] = "DENIED"
    elif scenario == "tampered":
        request["text"] = "changed report"
    elif scenario == "expired":
        now = approval["expires_at"]
    elif scenario == "replay":
        simulator.execute(request, approval, now)
    result = simulator.execute(request, approval, now)
    print(json.dumps(result | {"virtual_reports": len(simulator.reports)}, sort_keys=True))
    return 0 if result["status"] == "EXECUTED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
