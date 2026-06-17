"""Paper search ring (stage 0).

Leans on the `arxiv` package when available. Produces a markdown hit-list in
vault/90-search/<project>.md so an AI agent (or you) can pick what to ingest.
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

from .util import repo_root, slugify


def _search_arxiv(query: str, max_results: int):
    try:
        import arxiv  # type: ignore
    except ImportError as e:  # pragma: no cover
        raise SystemExit(
            "The 'arxiv' package is not installed. Run:\n"
            "  pip install 'scholarweave[search]'   (or: pip install arxiv)"
        ) from e
    client = arxiv.Client(page_size=min(max_results, 100), delay_seconds=3)
    s = arxiv.Search(query=query, max_results=max_results,
                     sort_by=arxiv.SortCriterion.Relevance)
    hits = []
    for r in client.results(s):
        hits.append({
            "title": r.title.strip().replace("\n", " "),
            "authors": [a.name for a in r.authors],
            "year": r.published.year if r.published else "",
            "url": r.entry_id,
            "pdf": r.pdf_url,
            "summary": (r.summary or "").strip().replace("\n", " "),
            "primary": r.primary_category,
        })
    return hits


def run(query: str, project: str | None = None, max_results: int = 20,
        root: Path | None = None) -> Path:
    root = root or repo_root()
    project = project or slugify(query, max_words=5)
    hits = _search_arxiv(query, max_results)

    out = root / "vault" / "90-search" / f"{project}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    today = _dt.date.today().isoformat()

    lines = [
        f"# Search · {project}",
        "",
        f"- query: `{query}`",
        f"- source: arXiv",
        f"- date: {today}",
        f"- hits: {len(hits)}",
        "",
        "> Triage: mark `[x]` to keep, then `scholarweave ingest` the kept PDFs.",
        "",
        "## Hit list",
        "",
    ]
    for i, h in enumerate(hits, 1):
        authors = ", ".join(h["authors"][:3]) + (" et al." if len(h["authors"]) > 3 else "")
        lines += [
            f"### [ ] {i}. {h['title']} ({h['year']})",
            f"- authors: {authors}",
            f"- category: {h['primary']}",
            f"- url: {h['url']}",
            f"- pdf: {h['pdf']}",
            f"- abstract: {h['summary'][:400]}{'…' if len(h['summary']) > 400 else ''}",
            "",
        ]
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
