#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def run(*args):
    return subprocess.run(args, cwd=ROOT, text=True, capture_output=True)

errors = []
for command in ([sys.executable, 'pipeline/public_safety.py'], [sys.executable, 'pipeline/editorial_lint.py'], [sys.executable, 'pipeline/sourcebook_smoke.py']):
    proc = run(*command)
    if proc.returncode != 0:
        errors.append(f"{' '.join(command)}\n{proc.stdout}{proc.stderr}")

payload = json.loads((ROOT / 'src/data/editions/2026-08-02.json').read_text())
if len(payload['items']) < 5:
    errors.append('fixture edition is too sparse for a newspaper prototype')
css = (ROOT / 'src/styles/global.css').read_text()
for warm in ('#eee9dd', '#e3ddcf', '#faf8f1', '#d9d3c6', '#f6f1e7'):
    if warm.lower() in css.lower():
        errors.append(f'warm light-mode colour remains: {warm}')
publishable_text = []
for folder in (ROOT / 'src', ROOT / 'public'):
    for path in folder.rglob('*'):
        if path.is_file() and path.suffix.lower() in {'.astro', '.ts', '.json', '.css', '.html', '.svg'}:
            publishable_text.append(path.read_text(errors='ignore'))
if 'analytics' in '\n'.join(publishable_text).lower():
    errors.append('analytics reference found in publishable files')

if errors:
    print('\n'.join(errors), file=sys.stderr)
    raise SystemExit(2)
print('public tests: pass')
