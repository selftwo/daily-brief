#!/usr/bin/env python3
"""Small, intentionally strict copy and item-shape gate for public editions."""
from __future__ import annotations

import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDITION_DIR = ROOT / 'src' / 'data' / 'editions'
COPY_FIELDS = ('kicker', 'title', 'dek', 'summary', 'deskNote')
FORBIDDEN = [
    re.compile(r'(?i)\b(?:this\s+article|this\s+piece|this\s+edition)\b'),
    re.compile(r'(?i)\b(?:game[- ]?changing|revolutionary|seamless|groundbreaking|unprecedented)\b'),
    re.compile(r'(?i)\b(?:why\s+you\s+should|you\s+need\s+to|for\s+you|your\s+feed|my\s+feed|saved\s+for)\b'),
    re.compile(r'(?i)\b(?:in\s+today[\'’]s\s+rapidly\s+changing\s+world|it\s+is\s+not\s+just)\b'),
    re.compile(r'(?m)\s[—–]\s'),
]
PERSONAL_PRONOUN = re.compile(r'(?i)\b(?:you|your|we|our|i|my)\b')
URL_RE = re.compile(r'^(?:https?://|/)')


def main() -> int:
    errors = []
    files = sorted(EDITION_DIR.glob('*.json'))
    if not files:
        errors.append('no public editions found')
    for path in files:
        try:
            edition = json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            errors.append(f'{path.name}: invalid JSON: {exc}')
            continue
        for key in ('date', 'issue', 'title', 'subtitle', 'items'):
            if not edition.get(key):
                errors.append(f'{path.name}: missing edition field {key}')
        try:
            date.fromisoformat(edition['date'])
        except (TypeError, ValueError):
            errors.append(f'{path.name}: date must be ISO YYYY-MM-DD')
        items = edition.get('items', [])
        if not isinstance(items, list) or not items:
            errors.append(f'{path.name}: edition has no items')
            continue
        seen = set()
        for index, item in enumerate(items, 1):
            label = f'{path.name} item {index}'
            for key in ('id', 'section', 'kind', 'title', 'dek', 'summary', 'deskNote', 'source', 'sourceUrl', 'published', 'status', 'links'):
                if not item.get(key):
                    errors.append(f'{label}: missing {key}')
            if item.get('id') in seen:
                errors.append(f'{label}: duplicate id {item.get("id")}')
            seen.add(item.get('id'))
            try:
                date.fromisoformat(item.get('published', ''))
            except ValueError:
                errors.append(f'{label}: published must be ISO YYYY-MM-DD')
            if not URL_RE.match(item.get('sourceUrl', '')):
                errors.append(f'{label}: sourceUrl must be absolute HTTP(S) or site-relative')
            links = item.get('links', [])
            if not isinstance(links, list) or not links:
                errors.append(f'{label}: at least one deep link is required')
            for link in links:
                if not link.get('label') or not URL_RE.match(link.get('url', '')):
                    errors.append(f'{label}: invalid deep link')
            for field in COPY_FIELDS:
                text = str(item.get(field, ''))
                for pattern in FORBIDDEN:
                    if pattern.search(text):
                        errors.append(f'{label}.{field}: forbidden copy pattern {pattern.pattern}')
                if PERSONAL_PRONOUN.search(text):
                    errors.append(f'{label}.{field}: personal pronoun in public editorial copy')
    if errors:
        print('\n'.join(sorted(set(errors))), file=sys.stderr)
        return 2
    print(f'editorial copy: pass ({len(files)} edition(s))')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
