#!/usr/bin/env python3
"""Materialize source only from an exact parent source directory; no network/build/VM."""
from pathlib import Path
import argparse
import json
from source_tools import materialize
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parent-source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(materialize(Path(__file__).resolve().parent, args.parent_source, args.output), sort_keys=True))
