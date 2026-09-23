# PubMed sync tool

`pubmed_sync.py` keeps `content/publication/` in sync with the lab's PubMed citations.
It works in two reviewable steps (`search` then `sync`), plus a `fix-dates` helper for
correcting publication dates on already-synced entries.

## Setup

```sh
cd scripts
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run all commands below from the `scripts/` directory with the venv activated.

## 1. `search` — find candidate PMIDs

```sh
python3 pubmed_sync.py search [--query "..."] [--out pubmed_review.tsv] [--api-key KEY]
```

- `--query` defaults to the contents of [pubmed_query.txt](pubmed_query.txt) (the lab's
  fixed PubMed search term) if omitted.
- Queries PubMed and writes a TSV (default `pubmed_review.tsv`, gitignored) with columns
  `pmid, title, year, journal, doi, status`, where `status` is `NEW` or
  `EXISTS:<folder-name>` if it matches an entry already in `content/publication/`.
- This step only writes the TSV — no content files are touched.

**Review the TSV by hand** before proceeding: delete/comment out (`#`) rows for anything
that isn't actually a lab publication.

## 2. `sync` — create/update content from the reviewed TSV

```sh
python3 pubmed_sync.py sync [--in pubmed_review.tsv] [--dry-run] [--api-key KEY]
```

- Reads the PMIDs remaining in the TSV (column 1).
- For each PMID, matches against existing entries by DOI/PMID:
  - already fully synced → skipped
  - matched but missing a `pmid:` field → patches just that field in
  - no match → creates `content/publication/<slug>/index.md` and `cite.bib`
- Use `--dry-run` first to preview what would be created/updated without writing anything.

## `fix-dates` — correct dates on already-synced entries

```sh
python3 pubmed_sync.py fix-dates [--dry-run] [--api-key KEY]
```

Re-fetches every entry that has a `pmid:` field and rewrites its `date:` line to PubMed's
actual publication month/day (instead of a hardcoded `-01-01`). Only the `date:` field is
touched. Use `--dry-run` to preview changes first.

## Notes

- `--api-key` raises the NCBI E-utilities rate limit from 3 to 10 requests/second.
- `pubmed_review.tsv` is gitignored — it's an ephemeral working file, not a record of truth.
- `pubmed_query.txt` is committed and holds the lab's stable PubMed search term.
