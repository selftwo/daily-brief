# Publication policy

The repository is a public rendering and edition store. Candidate intake may happen elsewhere; only reviewed, source-linked, public-safe material enters `src/data/editions/`.

The site never publishes private-feed labels, saved-note metadata, personal reactions, account identifiers, analytics, cookies, or credentials. Public sources can be attributed by their own publisher, author, or project name; that is source provenance, not reader profiling.

A build is rejected when it finds private paths, secrets, personalisation phrases, missing deep links, or ungrounded item shape. The vendored sourcebook fixture is a smoke test for the stronger citation and provenance gates that will be connected to real intake in the next phase.

## Source surfaces

- **Hacker News Top 100:** discovery pool only. Preserve the linked article/repository and the HN discussion as separate sources; rank is intake metadata, not a public editorial score.
- **Reddit:** public subreddit RSS is candidate intake. `hot`, `top`, and `new` are discovery views, not evidence of truth. Rate limits and empty results remain explicit feed failures.
- **X/Twitter AI:** manual review only. Keep the root post, attached article, quoted post, and replies as separate source-graph nodes. The public edition may cite a selected canonical post without exposing a private feed, saved reason, or ranking.

None of these collectors writes directly into a dated edition. Selection, canonical fetch, evidence capture, and public lint remain required.
