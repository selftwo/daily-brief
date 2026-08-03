# The Daily Brief

A public, source-grounded newspaper of signals, papers, essays, podcasts, and field notes.

The site is deliberately static. Public pages contain neutral editorial copy, canonical source links, dated editions, and no personal feed metadata, private notes, analytics, or account identity.

## Local development

```bash
npm install
npm run dev
```

## Build and verify

```bash
npm test
npm run build
npm run preview
```

The build runs three publication gates before Astro renders the site:

1. `pipeline/public_safety.py` rejects private paths, secrets, and disallowed metadata.
2. `pipeline/editorial_lint.py` checks public copy for personalisation, filler, unsupported item shape, and missing deep links.
3. `pipeline/sourcebook_smoke.py` runs the vendored sourcebook ship gate against its synthetic, public-safe fixture.

## Content model

Public editions live in `src/data/editions/*.json`. Private candidate intake is intentionally outside this repository. Public RSS, Hacker News, arXiv, podcast, and article sources can be normalised into an edition after editorial review. Run `npm run ingest:public` to collect current public RSS/Atom candidates into the ignored `pipeline/candidates/` directory; candidates are not published automatically. A later private studio layer can supply manually selected links from a bookmark repository without exposing the origin of the selection.

## Deployment

GitHub Pages is currently published from the `gh-pages` branch for the first public prototype, because the available repository token cannot create workflow files. The reviewed Actions workflow is preserved at `deployment/pages.yml`; after granting the `workflow` scope, it can be moved to `.github/workflows/pages.yml` for automatic deployment. The site itself is configured as a project Pages site at `/daily-brief/`.

## Attribution and licensing

The sourcebook kit under `pipeline/sourcebook/` is vendored under its original Apache-2.0 terms. Generated or sourced assets must be recorded in `assets/credits.json`. No image is treated as evidence.
