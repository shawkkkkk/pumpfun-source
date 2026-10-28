#!/usr/bin/env python3
"""Check the line-997 Truncation closure against the captured Pump program.

The candidate is one extra normalized window over the published L31 ELF.
Call operands and relocated lddw immediates are masked the same way as
repro/pump_amm/claim-self-transfer-v144/static-tool/elf_reader.py.
"""
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
BASELINE = ROOT / "research/claude-pump-integration-20261027/r37-layout-31/unstripped.so"
INVENTORY = ROOT / "research/claude-pump-integration-20261027/r37-layout-31/inventory.json.gz"
CANDIDATE = HERE / "builds/unstripped.so.gz"
GAIN = 0x857A8


def load_candidate():
    data = gzip.decompress(CANDIDATE.read_bytes())
    temporary = tempfile.NamedTemporaryFile(suffix=".so", delete=False)
    temporary.write(data)
    temporary.close()
    return Elf(Path(temporary.name))


def index(elf):
    found = {}
    for function in elf.funcs:
        start, size = function["start"], function["size"]
        body = elf.b[start : start + size]
        norm = elf.normalized[start : start + size]
        found.setdefault((size, hashlib.sha256(norm).digest()), []).append(body)
    return found


def score(elf, windows):
    found = index(elf)
    normalized = raw = 0
    hits = set()
    for window in windows:
        start, end = window["start"], window["end"]
        size = end - start
        body = elf_orig.b[start:end]
        norm = elf_orig.normalized[start:end]
        matches = found.get((size, hashlib.sha256(norm).digest()), [])
        if matches:
            normalized += 1
            hits.add(start)
            if body in matches:
                raw += 1
    return normalized, raw, hits


def main():
    global elf_orig
    elf_orig = Elf(ORIGINAL)
    windows = json.loads(gzip.decompress(INVENTORY.read_bytes()))["windows"]
    assert len(windows) == 1035
    baseline = score(Elf(BASELINE), windows)
    candidate = score(load_candidate(), windows)
    gained = sorted(candidate[2] - baseline[2])
    lost = sorted(baseline[2] - candidate[2])
    report = {
        "baseline_normalized": baseline[0],
        "baseline_raw": baseline[1],
        "candidate_normalized": candidate[0],
        "candidate_raw": candidate[1],
        "gained": [hex(item) for item in gained],
        "lost": [hex(item) for item in lost],
        "matched_windows": f"{candidate[0]} / 1035",
        "matched_percent": round(100 * candidate[0] / 1035, 2),
    }
    print(json.dumps(report, indent=2))
    assert baseline[0] == 990 and baseline[1] == 166, report
    assert candidate[0] == 991 and candidate[1] == 164, report
    assert gained == [GAIN] and lost == [], report
    assert (HERE / "source.patch").read_text().count("tokens_for_quote") == 1


if __name__ == "__main__":
    main()
