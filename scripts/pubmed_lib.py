"""Shared helpers for syncing content/publication/ with PubMed.

Used by pubmed_sync.py's `search` and `sync` subcommands.
"""
from __future__ import annotations

import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
PUBLICATION_DIR = REPO_ROOT / "content" / "publication"

EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
ESEARCH_URL = f"{EUTILS_BASE}/esearch.fcgi"
EFETCH_URL = f"{EUTILS_BASE}/efetch.fcgi"

# NCBI E-utilities rate limits: 3 req/s without an API key, 10 req/s with one.
_DEFAULT_RATE = 3.0
_API_KEY_RATE = 10.0


_MONTH_NAMES = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12",
}


def _normalize_month(month: str) -> str:
    month = month.strip().lower()
    if month.isdigit():
        return f"{int(month):02d}"
    return _MONTH_NAMES.get(month[:3], "01")


@dataclass
class PubMedRecord:
    pmid: str
    title: str
    authors: List[str] = field(default_factory=list)
    journal: str = ""
    issn: str = ""
    year: str = ""
    month: str = "01"
    day: str = "01"
    doi: str = ""
    abstract: str = ""

    @property
    def date_str(self) -> str:
        return f"{self.year or '0000'}-{self.month}-{self.day}"


class EUtilsClient:
    """Thin, rate-limited wrapper around the NCBI E-utilities used here."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self._min_interval = 1.0 / (_API_KEY_RATE if api_key else _DEFAULT_RATE)
        self._last_request = 0.0

    def _throttle(self):
        elapsed = time.monotonic() - self._last_request
        wait = self._min_interval - elapsed
        if wait > 0:
            time.sleep(wait)
        self._last_request = time.monotonic()

    def _get(self, url: str, params: dict) -> requests.Response:
        if self.api_key:
            params = {**params, "api_key": self.api_key}
        self._throttle()
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp

    def esearch_all_pmids(self, query: str, page_size: int = 200) -> List[str]:
        """Return every PMID matching `query`, paging through esearch results."""
        pmids: List[str] = []
        retstart = 0
        while True:
            resp = self._get(
                ESEARCH_URL,
                {
                    "db": "pubmed",
                    "term": query,
                    "retmode": "json",
                    "retstart": retstart,
                    "retmax": page_size,
                },
            )
            data = resp.json()["esearchresult"]
            ids = data.get("idlist", [])
            pmids.extend(ids)
            total = int(data.get("count", len(pmids)))
            retstart += len(ids)
            if not ids or retstart >= total:
                break
        return pmids

    def efetch_records(self, pmids: List[str], batch_size: int = 100) -> List[PubMedRecord]:
        """Fetch full PubMed records (title/authors/journal/year/doi/abstract) for pmids."""
        records: List[PubMedRecord] = []
        for i in range(0, len(pmids), batch_size):
            batch = pmids[i : i + batch_size]
            resp = self._get(
                EFETCH_URL,
                {
                    "db": "pubmed",
                    "id": ",".join(batch),
                    "retmode": "xml",
                    "rettype": "abstract",
                },
            )
            records.extend(_parse_efetch_xml(resp.content))
        return records


def _parse_efetch_xml(xml_bytes: bytes) -> List[PubMedRecord]:
    root = ET.fromstring(xml_bytes)
    records = []
    for article in root.findall(".//PubmedArticle"):
        pmid_el = article.find(".//MedlineCitation/PMID")
        pmid = pmid_el.text.strip() if pmid_el is not None and pmid_el.text else ""

        title_el = article.find(".//Article/ArticleTitle")
        title = "".join(title_el.itertext()).strip().rstrip(".") if title_el is not None else ""

        authors = []
        for author_el in article.findall(".//Article/AuthorList/Author"):
            last = author_el.findtext("LastName")
            fore = author_el.findtext("ForeName")
            collective = author_el.findtext("CollectiveName")
            if last and fore:
                authors.append(f"{fore} {last}")
            elif last:
                authors.append(last)
            elif collective:
                authors.append(collective)

        journal = article.findtext(".//Article/Journal/Title") or ""
        issn = article.findtext(".//Article/Journal/ISSN") or ""

        pub_date_el = article.find(".//Article/Journal/JournalIssue/PubDate")
        year, month, day = "", "01", "01"
        if pub_date_el is not None:
            year = pub_date_el.findtext("Year") or ""
            month_text = pub_date_el.findtext("Month")
            day_text = pub_date_el.findtext("Day")
            if not year:
                medline_date = pub_date_el.findtext("MedlineDate", "")
                match = re.match(r"(\d{4})(?:[\s-]+([A-Za-z]{3}))?", medline_date)
                if match:
                    year = match.group(1)
                    month_text = match.group(2) or month_text
            if month_text:
                month = _normalize_month(month_text)
            if day_text and day_text.isdigit():
                day = f"{int(day_text):02d}"

        doi = ""
        for id_el in article.findall(".//ArticleIdList/ArticleId"):
            if id_el.get("IdType") == "doi" and id_el.text:
                doi = id_el.text.strip()
                break

        abstract_parts = [
            "".join(el.itertext()) for el in article.findall(".//Abstract/AbstractText")
        ]
        abstract = " ".join(part.strip() for part in abstract_parts if part.strip())

        records.append(
            PubMedRecord(
                pmid=pmid,
                title=title,
                authors=authors,
                journal=journal,
                issn=issn,
                year=year,
                month=month,
                day=day,
                doi=doi,
                abstract=abstract,
            )
        )
    return records


def normalize_doi(doi: str) -> str:
    doi = doi.strip().lower()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi)
    return doi


_FRONTMATTER_FIELD_RE = re.compile(r"^(doi|pmid):\s*['\"]?([^'\"\n]+)", re.MULTILINE)


def build_existing_index() -> Dict[str, Dict[str, str]]:
    """Scan content/publication/*/index.md, return {'doi': {doi: folder}, 'pmid': {pmid: folder}}."""
    by_doi: Dict[str, str] = {}
    by_pmid: Dict[str, str] = {}
    for index_path in sorted(PUBLICATION_DIR.glob("*/index.md")):
        folder = index_path.parent.name
        text = index_path.read_text(encoding="utf-8")
        front_matter = text.split("---", 2)[1] if text.startswith("---") else text
        for match in _FRONTMATTER_FIELD_RE.finditer(front_matter):
            field_name, value = match.group(1), match.group(2).strip()
            if field_name == "doi":
                by_doi[normalize_doi(value)] = folder
            elif field_name == "pmid":
                by_pmid[value] = folder
    return {"doi": by_doi, "pmid": by_pmid}


def slugify_word(word: str) -> str:
    word = unicodedata.normalize("NFKD", word).encode("ascii", "ignore").decode("ascii")
    word = re.sub(r"[^a-zA-Z0-9]", "", word)
    return word.lower()


_STOPWORDS = {"a", "an", "the", "of", "on", "in", "for", "and", "to", "towards", "toward"}


def first_significant_title_word(title: str) -> str:
    for word in re.findall(r"[A-Za-z0-9]+", title):
        slug_word = slugify_word(word)
        if slug_word and slug_word not in _STOPWORDS:
            return slug_word
    return "paper"


def make_slug(record: PubMedRecord, existing_folders: Optional[set] = None) -> str:
    last_name = record.authors[0].split()[-1] if record.authors else "unknown"
    last_name = slugify_word(last_name) or "unknown"
    year = record.year or "0000"
    title_word = first_significant_title_word(record.title)
    base = f"{last_name}-{year}-{title_word}"

    existing_folders = existing_folders or set()
    slug = base
    suffix = 2
    while slug in existing_folders:
        slug = f"{base}-{suffix}"
        suffix += 1
    return slug


def existing_folder_names() -> set:
    return {p.name for p in PUBLICATION_DIR.iterdir() if p.is_dir()}


def _yaml_escape(value: str) -> str:
    return value.replace("'", "''")


def build_front_matter(record: PubMedRecord, now_date: str) -> str:
    authors_block = "\n".join(f"- {author}" for author in record.authors) or "- ' others'"
    doi_line = f"doi: {record.doi}\n" if record.doi else ""
    url_line = "" if record.doi else f"url_pdf: 'https://pubmed.ncbi.nlm.nih.gov/{record.pmid}/'\n"
    abstract = _yaml_escape(record.abstract)
    publication = _yaml_escape(record.journal)

    return f"""---
# Documentation: https://wowchemy.com/docs/managing-content/

title: '{_yaml_escape(record.title)}'
subtitle: ''
summary: ''
authors:
{authors_block}
tags: []
categories: []
date: '{record.date_str}'
lastmod: {now_date}
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ''
  focal_point: ''
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []
publishDate: '{now_date}'
publication_types:
- '2'
abstract: '{abstract}'
publication: '*{publication}*'
{doi_line}{url_line}pmid: '{record.pmid}'
---
"""


def build_cite_bib(record: PubMedRecord) -> str:
    first_author_last = record.authors[0].split()[-1].upper() if record.authors else "UNKNOWN"
    key = f"{first_author_last}{record.year or ''}"
    authors_bib = " and ".join(record.authors)
    lines = ["@article{" + key + ","]
    if record.abstract:
        lines.append(f" abstract = {{{record.abstract}}},")
    if authors_bib:
        lines.append(f" author = {{{authors_bib}}},")
    if record.doi:
        lines.append(f" doi = {{{record.doi}}},")
    if record.issn:
        lines.append(f" issn = {{{record.issn}}},")
    if record.journal:
        lines.append(f" journal = {{{record.journal}}},")
    lines.append(f" title = {{{record.title}}},")
    lines.append(f" url = {{https://pubmed.ncbi.nlm.nih.gov/{record.pmid}/}},")
    lines.append(f" month = {{{record.month}}},")
    lines.append(f" day = {{{record.day}}},")
    lines.append(f" year = {{{record.year}}}")
    lines.append("}")
    return "\n".join(lines) + "\n"
