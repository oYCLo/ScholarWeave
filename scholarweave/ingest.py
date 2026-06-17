"""Ingest a source (stage 2).

Converts a file in vault/00-inbox/ (or any path) to Markdown via MarkItDown,
then scaffolds a per-paper folder vault/10-literature/<citekey>/ containing:
  note.md (structured, from template) · meta.yaml · highlights.md ·
  extracted.md (raw conversion) · paper.pdf (the original, copied in).
"""
from __future__ import annotations

import shutil
from pathlib import Path

from .util import (fill_template, load_template, make_citekey, repo_root,
                   write_if_absent)

DEFAULT_NOTE = """---
citekey: {{citekey}}
title: "{{title}}"
authors: [{{authors}}]
year: {{year}}
venue:
doi:
citations:
retracted: false
tags: []
status: to-read
priority: medium
---

# {{title}}

## One-liner / 一句话

## Problem & motivation / 解决的问题

## Method core / 方法核心

## Setup & datasets / 实验设置

## Falsifiable conditions & limits / 可证伪条件与局限

## Relation to my work / 与我的关系
- links: [[ ]]

## Key excerpts / 关键摘录
- see highlights.md
"""

DEFAULT_META = """citekey: {{citekey}}
title: "{{title}}"
authors: [{{authors}}]
year: {{year}}
source_file: "{{source_file}}"
doi:
url:
citations:
retracted: false
"""


def _to_markdown(src: Path) -> str:
    if src.suffix.lower() in {".md", ".markdown", ".txt"}:
        return src.read_text(encoding="utf-8", errors="ignore")
    try:
        from markitdown import MarkItDown  # type: ignore
    except ImportError as e:  # pragma: no cover
        raise SystemExit(
            "MarkItDown is not installed. Run:\n"
            "  pip install 'scholarweave[ingest]'   (or: pip install 'markitdown[all]')"
        ) from e
    return MarkItDown().convert(str(src)).text_content


def run(src: str, citekey: str | None = None, title: str | None = None,
        authors: str | None = None, year: str | None = None,
        root: Path | None = None) -> Path:
    root = root or repo_root()
    src_path = Path(src)
    if not src_path.is_absolute():
        # try as-is, then relative to inbox
        cand = root / "vault" / "00-inbox" / src
        src_path = src_path if src_path.exists() else cand
    if not src_path.exists():
        raise SystemExit(f"Source not found: {src}")

    text = _to_markdown(src_path)
    title = title or src_path.stem.replace("_", " ").replace("-", " ").title()
    authors = authors or ""
    year = year or ""
    citekey = citekey or make_citekey([authors] if authors else [], year, title)

    folder = root / "vault" / "10-literature" / citekey
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "assets").mkdir(exist_ok=True)

    vals = {
        "citekey": citekey, "title": title,
        "authors": ", ".join(a.strip() for a in authors.split(";") if a.strip()),
        "year": year, "source_file": src_path.name,
    }
    note_tpl = load_template(root, "paper.md", DEFAULT_NOTE)
    meta_tpl = load_template(root, "meta.yaml", DEFAULT_META)

    write_if_absent(folder / "note.md", fill_template(note_tpl, vals))
    write_if_absent(folder / "meta.yaml", fill_template(meta_tpl, vals))
    write_if_absent(folder / "highlights.md", f"# Highlights · {citekey}\n\n- \n")
    (folder / "extracted.md").write_text(text, encoding="utf-8")

    # keep the original alongside the note (gitignored)
    if src_path.suffix.lower() == ".pdf":
        shutil.copy2(src_path, folder / "paper.pdf")

    return folder
