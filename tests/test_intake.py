#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipeline import collect_public

ids = [101, 202, 303]
items = {
    101: {'id': 101, 'title': 'Linked article', 'url': 'https://example.com/article', 'time': 1_700_000_000, 'score': 90, 'descendants': 12},
    202: {'id': 202, 'title': 'Discussion only', 'time': 1_700_000_100, 'score': 40, 'descendants': 5},
    303: {'id': 303, 'title': 'Third item', 'url': 'https://example.com/third', 'time': 1_700_000_200, 'score': 20, 'descendants': 2, 'dead': True},
}

original = collect_public.fetch_json

def fake_fetch_json(url: str):
    if url.endswith('/topstories.json'):
        return ids
    return items[int(url.rstrip('/').split('/')[-1].split('.')[0])]

collect_public.fetch_json = fake_fetch_json
try:
    feed = {
        'url': 'https://hacker-news.firebaseio.com/v0/topstories.json',
        'item_url': 'https://hacker-news.firebaseio.com/v0/item/{id}.json',
    }
    records = list(collect_public.parse_hn_top(feed, 3))
finally:
    collect_public.fetch_json = original

assert len(records) == 2, f'expected dead items to be excluded, got {len(records)}'
assert records[0]['hn_rank'] == 1
assert records[0]['url'] == 'https://example.com/article'
assert records[0]['discussion_url'] == 'https://news.ycombinator.com/item?id=101'
assert records[1]['url'] == 'https://news.ycombinator.com/item?id=202'
assert records[1]['hn_rank'] == 2

feeds = json.loads((ROOT / 'pipeline/feeds.public.json').read_text(encoding='utf-8'))
config = {feed['id']: feed for feed in feeds}
assert config['hacker-news-top100']['collector'] == 'hacker-news-top'
assert config['hacker-news-top100']['limit'] == 100
assert config['reddit-artificial']['kind'] == 'reddit'

print('intake tests: pass')
