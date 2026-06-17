"""Shared helpers: paths, slugify, citekey, template filling."""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

# ---- Vault layout (single source of truth) -------------------------------
VAULT_DIRS = [
    "00-inbox",
    "10-literature",
    "20-entities",
    "30-concepts",
    "40-questions",
    "50-ideas",
    "60-experiments",
    "70-synthesis",
    "80-archive",
    "90-search",
]
TOP_DIRS = ["config/agents", "config/skills", "config/templates", "code", "outputs"]

STOPWORDS = {
    "a", "an", "the", "of", "for", "and", "or", "to", "in", "on", "with",
    "using", "via", "is", "are", "via", "by", "from", "towards", "toward",
}


def repo_root(start: Path | None = None) -> Path:
    """Find the project root by walking up until we see a vault/ or pyproject."""
    p = (start or Path.cwd()).resolve()
    for cand in [p, *p.parents]:
        if (cand / "vault").is_dir() or (cand / "pyproject.toml").is_file():
            return cand
    return p


def slugify(text: str, max_words: int = 6) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    text = re.sub(r"[^a-zA-Z0-9\s-]", " ", text).lower()
    words = [w for w in text.split() if w]
    return "-".join(words[:max_words]) or "untitled"


def make_citekey(authors, year, title) -> str:
    """authorYEARkeyword, e.g. vaswani2017attention."""
    surname = "anon"
    if authors:
        first = authors[0] if isinstance(authors, (list, tuple)) else str(authors)
        # handle "First Last" or "Last, First"
        first = str(first)
        surname = (first.split(",")[0] if "," in first else first.split()[-1]) if first.strip() else "anon"
    surname = re.sub(r"[^a-zA-Z]", "", surname).lower() or "anon"
    yr = re.sub(r"[^0-9]", "", str(year))[:4] or "0000"
    kw = "paper"
    for w in slugify(title or "").split("-"):
        if w and w not in STOPWORDS:
            kw = w
            break
    return f"{surname}{yr}{kw}"


def fill_template(template: str, values: dict) -> str:
    """Replace {{key}} placeholders; leave unknown ones blank-friendly."""
    def repl(m):
        key = m.group(1).strip()
        v = values.get(key, "")
        return str(v) if v is not None else ""
    return re.sub(r"\{\{\s*([\w.-]+)\s*\}\}", repl, template)


def load_template(root: Path, name: str, default: str = "") -> str:
    f = root / "config" / "templates" / name
    if f.is_file():
        return f.read_text(encoding="utf-8")
    return default


def write_if_absent(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return False
    path.write_text(content, encoding="utf-8")
    return True
