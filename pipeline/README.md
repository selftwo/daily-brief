# Public intake

`collect_public.py` is the first adapter layer. It reads `feeds.public.json`, fetches public RSS/Atom feeds, and writes a candidate snapshot outside the published site:

```bash
python3 pipeline/collect_public.py
```

The current public lanes are Hacker News and arXiv categories. Newsletter and podcast feeds can be added as public URLs when their source list is available. Candidates are not automatically published: each selected URL still needs sourcebook collection, evidence review, copy lint, and an edition entry.

A later private studio can add manually selected bookmark/X links without changing the public renderer or exposing the origin of selection.
