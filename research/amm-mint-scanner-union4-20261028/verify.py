#!/usr/bin/env python3
"""Score the union4 AMM after composing the recovered mint scanner.

Candidate windows are complete symbol bodies. Original windows are the union4
inventory. Call immediates and relocated lddw immediates are masked by
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
ORIGINAL = ROOT / "evidence/original/pump_amm/deployed.so"
BASELINE = ROOT / "research/claude-amm-union4-20261028/builds/a/symbols.so.gz"
CANDIDATE = HERE / "builds/unstripped.so.gz"
MEASUREMENT = ROOT / "research/claude-amm-union4-20261028/measurement.json"


def open_elf(path):
    if path.suffix == ".gz":
        data = gzip.decompress(path.read_bytes())
        temporary = tempfile.NamedTemporaryFile(suffix=".so", delete=False)
        temporary.write(data)
        temporary.close()
        return Elf(Path(temporary.name))
    return Elf(path)


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
    raw_hits = set()
    for addr, size, _symbol, _flag in windows:
        start = int(addr, 16)
        body = original.b[start : start + size]
        norm = original.normalized[start : start + size]
        matches = found.get((size, hashlib.sha256(norm).digest()), [])
        if matches:
            normalized += 1
            hits.add(addr)
            if body in matches:
                raw += 1
                raw_hits.add(addr)
    return normalized, raw, hits, raw_hits


def main():
    original = Elf(ORIGINAL)
    windows = json.loads(MEASUREMENT.read_text())["windows_detail"]
    assert len(windows) == 785
    baseline = score(open_elf(BASELINE), windows, original)
    candidate = score(open_elf(CANDIDATE), windows, original)
    gained = sorted(candidate[2] - baseline[2])
    lost = sorted(baseline[2] - candidate[2])
    raw_gained = sorted(candidate[3] - baseline[3])
    raw_lost = sorted(baseline[3] - candidate[3])
    report = {
        "baseline_normalized": baseline[0],
        "baseline_raw": baseline[1],
        "candidate_normalized": candidate[0],
        "candidate_raw": candidate[1],
        "gained": gained,
        "lost": lost,
        "raw_gained": raw_gained,
        "raw_lost": raw_lost,
        "matched_percent": round(100 * candidate[0] / 785, 2),
    }
    print(json.dumps(report, indent=2))
    assert baseline[0] == 769 and baseline[1] == 160, report
    assert candidate[0] == 770 and candidate[1] == 163, report
    assert gained == ["0xf28b8"] and lost == [], report
    assert raw_gained == ["0x111360", "0xf28a8", "0xf28b8"] and raw_lost == [], report
    assert "0xf28b8" in candidate[3]


if __name__ == "__main__":
    main()
