#!/usr/bin/env python3
"""Reject private or personalised material from publishable paths."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_ROOTS = [ROOT / 'src' / 'data', ROOT / 'src' / 'components', ROOT / 'src' / 'pages', ROOT / 'public', ROOT / 'dist']
TEXT_EXTENSIONS = {'.json', '.astro', '.ts', '.js', '.css', '.html', '.xml', '.svg', '.md', '.txt'}

DENIED_KEYS = {
    'private_note', 'personal_note', 'private_notes', 'personal_notes',
    'internal_score', 'private_score', 'source_origin', 'feed_origin',
    'saved_at', 'account_id', 'user_id', 'session_id', 'api_key',
    'access_token', 'refresh_token', 'cookie', 'connection_string'
}
DENIED_PATTERNS = [
    re.compile(r'(?i)(?:/root/|/home/[^/]+/|\\Users\\)'),
    re.compile(r'(?i)\b(?:api[_ -]?key|access[_ -]?token|refresh[_ -]?token)\s*[:=]'),
    re.compile(r'(?i)\b(?:bearer\s+|sk-[a-z0-9]{12,}|ghp_[a-z0-9]{20,})'),
    re.compile(r'(?i)\b(?:selected\s+for\s+you|based\s+on\s+your\s+interests|from\s+my\s+feed|your\s+saved)\b'),
    re.compile(r'(?i)\b(?:personalised|personalized)\s+(?:recommendation|brief|edition|feed)\b'),
    re.compile(r'(?i)[\w.+-]+@[\w-]+\.[\w.-]+'),
]


def iter_files():
    seen = set()
    for root in PUBLIC_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob('*'):
            if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS and path not in seen:
                seen.add(path)
                yield path


def walk_keys(value, path=''):
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in DENIED_KEYS:
                yield f'{path}.{key}'.lstrip('.')
            yield from walk_keys(child, f'{path}.{key}'.lstrip('.'))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_keys(child, f'{path}[{index}]')


def main() -> int:
    errors = []
    for path in iter_files():
        text = path.read_text(encoding='utf-8', errors='replace')
        rel = path.relative_to(ROOT)
        for pattern in DENIED_PATTERNS:
            if pattern.search(text):
                errors.append(f'{rel}: disallowed public pattern {pattern.pattern}')
        if path.suffix == '.json':
            try:
                payload = json.loads(text)
            except json.JSONDecodeError as exc:
                errors.append(f'{rel}: invalid JSON: {exc}')
                continue
            for key in walk_keys(payload):
                errors.append(f'{rel}: disallowed metadata key {key}')
    if errors:
        print('\n'.join(sorted(set(errors))), file=sys.stderr)
        return 2
    print('public safety: pass')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
