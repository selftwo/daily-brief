#!/usr/bin/env python3
"""Collect public RSS/Atom candidates without writing them into the edition.

This is an intake helper, not a recommendation engine. It preserves the feed
item and source link so an editor can select, fetch, and sourcebook-verify it
before publication.
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ATOM = {'atom': 'http://www.w3.org/2005/Atom'}


def text(value):
    return re.sub(r'\s+', ' ', value or '').strip()


def date_value(value):
    value = text(value)
    if not value:
        return ''
    try:
        return parsedate_to_datetime(value).astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError, OverflowError):
        try:
            return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc).isoformat()
        except ValueError:
            return value


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'daily-brief-public-intake/0.1'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def parse_feed(feed):
    root = ET.fromstring(feed)
    if root.tag.endswith('feed'):
        for entry in root.findall('atom:entry', ATOM):
            link = next((item.get('href') for item in entry.findall('atom:link', ATOM) if item.get('rel', 'alternate') == 'alternate'), '')
            yield {
                'title': text(entry.findtext('atom:title', '', ATOM)),
                'url': link or text(entry.findtext('atom:id', '', ATOM)),
                'published': date_value(entry.findtext('atom:published', '', ATOM) or entry.findtext('atom:updated', '', ATOM)),
                'description': text(entry.findtext('atom:summary', '', ATOM)),
            }
        return
    channel = root.find('./channel')
    if channel is None:
        return
    for item in channel.findall('item'):
        yield {
            'title': text(item.findtext('title')),
            'url': text(item.findtext('link')),
            'published': date_value(item.findtext('pubDate') or item.findtext('{http://purl.org/dc/elements/1.1/}date')),
            'description': text(item.findtext('description')),
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', default='pipeline/candidates/public.json')
    parser.add_argument('--limit', type=int, default=12)
    args = parser.parse_args()
    feeds = json.loads((ROOT / 'pipeline/feeds.public.json').read_text(encoding='utf-8'))
    candidates = []
    failures = []
    for feed in feeds:
        try:
            entries = list(parse_feed(fetch(feed['url'])))[:args.limit]
            for entry in entries:
                entry.update({'feed_id': feed['id'], 'feed_kind': feed['kind'], 'feed_label': feed['label']})
                candidates.append(entry)
        except Exception as exc:  # feed failures are reported, not hidden
            failures.append({'feed_id': feed['id'], 'error': str(exc)})
    result = {
        'schema_version': 1,
        'collected_at': datetime.now(timezone.utc).isoformat(),
        'feeds': feeds,
        'candidates': candidates,
        'failures': failures,
    }
    output = ROOT / args.out
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'public intake: {len(candidates)} candidates from {len(feeds) - len(failures)} feeds; {len(failures)} failures')
    if failures:
        print(json.dumps(failures, indent=2))


if __name__ == '__main__':
    main()
