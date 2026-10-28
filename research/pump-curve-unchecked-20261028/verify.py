#!/usr/bin/env python3
"""Score the L32 Pump build after the curve-dispatch and line-997 edits."""
import gzip
import hashlib
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "repro/pump_amm/claim-self-transfer-v144/static-tool"))
from elf_reader import Elf

HERE = Path(__file__).resolve().parent
ORIGINAL = ROOT / "evidence/original/pump/deployed.so"
BASELINE = ROOT / "research/claude-pump-integration-20261027/r37-layout-32/unstripped.so"
INVENTORY = ROOT / "research/claude-pump-integration-20261027/r37-layout-32/inventory.json.gz"
CANDIDATE = HERE / "builds/unstripped.so.gz"


def load_gz(path):
    data = gzip.decompress(path.read_bytes())
    temporary = tempfile.NamedTemporaryFile(suffix=".so", delete=False)
    temporary.write(data)
    temporary.close()
    return Elf(Path(temporary.name))


def index(elf):
    found = {}
    for function in elf.funcs:
        start, size = function["start"], function["size"]
        found.setdefault(
            (size, hashlib.sha256(elf.normalized[start : start + size]).digest()),
            [],
        ).append(elf.b[start : start + size])
    return found


def score(elf, windows, original):
    found = index(elf)
    normalized = raw = 0
    hits = set()
    for window in windows:
        start, end = window["start"], window["end"]
        body = original.b[start:end]
        norm = original.normalized[start:end]
        matches = found.get((end - start, hashlib.sha256(norm).digest()), [])
        if matches:
            normalized += 1
            hits.add(start)
            if body in matches:
                raw += 1
    return normalized, raw, hits


def main():
    original = Elf(ORIGINAL)
    windows = json.loads(gzip.decompress(INVENTORY.read_bytes()))["windows"]
    assert len(windows) == 1035
    baseline = score(Elf(BASELINE), windows, original)
    candidate = score(load_gz(CANDIDATE), windows, original)
    gained = sorted(candidate[2] - baseline[2])
    lost = sorted(baseline[2] - candidate[2])
    report = {
        "baseline_normalized": baseline[0],
        "baseline_raw": baseline[1],
        "candidate_normalized": candidate[0],
        "candidate_raw": candidate[1],
        "gained": [hex(item) for item in gained],
        "lost": [hex(item) for item in lost],
        "matched_percent": round(100 * candidate[0] / 1035, 2),
    }
    print(json.dumps(report, indent=2))
    assert baseline[0] == 990 and baseline[1] == 166, report
    assert candidate[0] == 992 and candidate[1] == 164, report
    assert gained == [0x857A8, 0x9B430] and lost == [], report


if __name__ == "__main__":
    main()
