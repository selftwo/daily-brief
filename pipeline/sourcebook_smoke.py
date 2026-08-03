#!/usr/bin/env python3
"""Run the vendored sourcebook verification gate against a public-safe fixture."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'pipeline' / 'sourcebook' / 'scripts' / 'sb.py'
WORKSPACE = ROOT / 'pipeline' / 'fixtures' / 'sourcebook-demo'

proc = subprocess.run(
    [sys.executable, str(CLI), '--dir', str(WORKSPACE), 'verify', '--json'],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
if proc.returncode != 0:
    print(proc.stdout, end='')
    print(proc.stderr, end='', file=sys.stderr)
    raise SystemExit(proc.returncode)
try:
    result = json.loads(proc.stdout)
except json.JSONDecodeError as exc:
    print(f'sourcebook smoke: invalid JSON output: {exc}', file=sys.stderr)
    raise SystemExit(2)
if not result.get('pass'):
    print(json.dumps(result, indent=2), file=sys.stderr)
    raise SystemExit(2)
print('sourcebook smoke: pass')
