#!/usr/bin/env python3
"""CLI for syncing content/publication/ with PubMed.

Usage:
    scripts/pubmed_sync.py search --query "..." [--out FILE] [--api-key KEY]
    scripts/pubmed_sync.py sync [--in FILE] [--dry-run]
    scripts/pubmed_sync.py fix-dates [--dry-run]

Workflow: run `search` to produce a TSV of candidate PMIDs, hand-review/trim
that file, then run `sync` to create/update content/publication/ entries.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import re
import sys
from pathlib import Path

import pubmed_lib as lib

SCRIPTS_DIR = Path(__file__).resolve().parent
DEFAULT_QUERY_FILE = SCRIPTS_DIR / "pubmed_query.txt"
DEFAULT_REVIEW_FILE = SCRIPTS_DIR / "pubmed_review.tsv"


def cmd_search(args: argparse.Namespace) -> int:
    query = args.query
    if not query:
        if DEFAULT_QUERY_FILE.exists():
            query = DEFAULT_QUERY_FILE.read_text(encoding="utf-8").strip()
        if not query:
            print(f"error: no --query given and {DEFAULT_QUERY_FILE} is missing/empty", file=sys.stderr)
            return 1

    client = lib.EUtilsClient(api_key=args.api_key)
    print(f"Searching PubMed for: {query}", file=sys.stderr)
    pmids = client.esearch_all_pmids(query)
    print(f"Found {len(pmids)} PMIDs, fetching details...", file=sys.stderr)
    records = client.efetch_records(pmids)

    index = lib.build_existing_index()

    out_path = Path(args.out)
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["pmid", "title", "year", "journal", "doi", "status"])
        for record in records:
            folder = index["doi"].get(lib.normalize_doi(record.doi)) or index["pmid"].get(record.pmid)
            status = f"EXISTS:{folder}" if folder else "NEW"
            writer.writerow([record.pmid, record.title, record.year, record.journal, record.doi, status])

    print(f"Wrote {len(records)} rows to {out_path}", file=sys.stderr)
    return 0


def _read_review_pmids(path: Path) -> list:
    pmids = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        header = next(reader, None)
        for row in reader:
            if not row or not row[0].strip() or row[0].strip().startswith("#"):
                continue
            pmids.append(row[0].strip())
    return pmids


def cmd_sync(args: argparse.Namespace) -> int:
    in_path = Path(args.infile)
    if not in_path.exists():
        print(f"error: review file not found: {in_path}", file=sys.stderr)
        return 1

    pmids = _read_review_pmids(in_path)
    if not pmids:
        print("No PMIDs to sync.", file=sys.stderr)
        return 0

    client = lib.EUtilsClient(api_key=args.api_key)
    records = client.efetch_records(pmids)
    index = lib.build_existing_index()
    existing_folders = lib.existing_folder_names()
    now_date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

    created = updated = skipped = 0

    for record in records:
        folder = index["doi"].get(lib.normalize_doi(record.doi)) or index["pmid"].get(record.pmid)

        if folder:
            index_path = lib.PUBLICATION_DIR / folder / "index.md"
            text = index_path.read_text(encoding="utf-8")
            if "\npmid:" in text or text.startswith("pmid:"):
                print(f"SKIP  {record.pmid} already synced -> {folder}")
                skipped += 1
                continue
            print(f"UPDATE {record.pmid} -> {folder} (add pmid field)")
            if not args.dry_run:
                patched = text.rstrip("\n")
                if patched.endswith("---"):
                    patched = patched[: -len("---")].rstrip("\n") + f"\npmid: '{record.pmid}'\n---\n"
                else:
                    patched = patched + f"\npmid: '{record.pmid}'\n"
                index_path.write_text(patched, encoding="utf-8")
            updated += 1
            continue

        slug = lib.make_slug(record, existing_folders)
        existing_folders.add(slug)
        pub_dir = lib.PUBLICATION_DIR / slug
        print(f"CREATE {record.pmid} -> {slug}")
        if not args.dry_run:
            pub_dir.mkdir(parents=True, exist_ok=False)
            (pub_dir / "index.md").write_text(lib.build_front_matter(record, now_date), encoding="utf-8")
            (pub_dir / "cite.bib").write_text(lib.build_cite_bib(record), encoding="utf-8")
        created += 1

    print(f"\ncreated={created} updated={updated} skipped={skipped}" + (" (dry run)" if args.dry_run else ""))
    return 0


_DATE_LINE_RE = re.compile(r"^date: '[0-9]{4}-[0-9]{2}-[0-9]{2}'\s*$", re.MULTILINE)
_PMID_LINE_RE = re.compile(r"^pmid: '([0-9]+)'\s*$", re.MULTILINE)


def cmd_fix_dates(args: argparse.Namespace) -> int:
    entries = []
    for index_path in sorted(lib.PUBLICATION_DIR.glob("*/index.md")):
        text = index_path.read_text(encoding="utf-8")
        match = _PMID_LINE_RE.search(text)
        if match:
            entries.append((index_path, match.group(1)))

    if not entries:
        print("No entries with a pmid field found.", file=sys.stderr)
        return 0

    client = lib.EUtilsClient(api_key=args.api_key)
    records = {r.pmid: r for r in client.efetch_records([pmid for _, pmid in entries])}

    fixed = skipped = 0
    for index_path, pmid in entries:
        record = records.get(pmid)
        if record is None:
            print(f"SKIP  {pmid} -> {index_path.parent.name} (no PubMed record returned)")
            skipped += 1
            continue
        text = index_path.read_text(encoding="utf-8")
        new_line = f"date: '{record.date_str}'"
        if not _DATE_LINE_RE.search(text):
            print(f"SKIP  {pmid} -> {index_path.parent.name} (no date field matched)")
            skipped += 1
            continue
        if f"date: '{record.date_str}'" in text:
            skipped += 1
            continue
        print(f"FIX   {pmid} -> {index_path.parent.name}: {new_line}")
        if not args.dry_run:
            index_path.write_text(_DATE_LINE_RE.sub(new_line, text), encoding="utf-8")
        fixed += 1

    print(f"\nfixed={fixed} skipped={skipped}" + (" (dry run)" if args.dry_run else ""))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_p = subparsers.add_parser("search", help="Query PubMed and write a review TSV")
    search_p.add_argument("--query", help=f"PubMed search term (default: read from {DEFAULT_QUERY_FILE})")
    search_p.add_argument("--out", default=str(DEFAULT_REVIEW_FILE), help="Output TSV path")
    search_p.add_argument("--api-key", help="NCBI API key (raises rate limit to 10 req/s)")
    search_p.set_defaults(func=cmd_search)

    sync_p = subparsers.add_parser("sync", help="Create/update content/publication/ from a reviewed TSV")
    sync_p.add_argument("--in", dest="infile", default=str(DEFAULT_REVIEW_FILE), help="Reviewed TSV path")
    sync_p.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files")
    sync_p.add_argument("--api-key", help="NCBI API key (raises rate limit to 10 req/s)")
    sync_p.set_defaults(func=cmd_sync)

    fix_p = subparsers.add_parser(
        "fix-dates", help="Re-fetch PubMed PubDate for synced entries and correct the date field"
    )
    fix_p.add_argument("--dry-run", action="store_true", help="Print planned changes without writing files")
    fix_p.add_argument("--api-key", help="NCBI API key (raises rate limit to 10 req/s)")
    fix_p.set_defaults(func=cmd_fix_dates)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
