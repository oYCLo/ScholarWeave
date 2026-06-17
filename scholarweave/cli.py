"""ScholarWeave command-line interface.

Subcommands:
  init            scaffold the vault/config/code/outputs layout
  search QUERY    search arXiv -> vault/90-search/<project>.md
  ingest SRC      convert a source -> vault/10-literature/<citekey>/ (per-paper folder)
  new-experiment  scaffold code/<exp-id>/ + vault/60-experiments/<exp-id>/
  status          quick counts of what's in the vault
"""
from __future__ import annotations

import argparse
from pathlib import Path

from . import __version__
from .util import TOP_DIRS, VAULT_DIRS, repo_root


def cmd_init(args):
    root = Path(args.path).resolve()
    for d in VAULT_DIRS:
        p = root / "vault" / d
        p.mkdir(parents=True, exist_ok=True)
        (p / ".gitkeep").touch()
    for d in TOP_DIRS:
        p = root / d
        p.mkdir(parents=True, exist_ok=True)
        (p / ".gitkeep").touch()
    idx = root / "vault" / "index.md"
    if not idx.exists():
        idx.write_text("# ScholarWeave — Index (MOC)\n\n"
                       "- [[90-search]] searches\n- [[10-literature]] papers\n"
                       "- [[40-questions]] questions\n- [[50-ideas]] ideas\n"
                       "- [[60-experiments]] experiments\n- [[70-synthesis]] synthesis\n",
                       encoding="utf-8")
    print(f"Initialized ScholarWeave layout at {root}")


def cmd_search(args):
    from . import search
    out = search.run(args.query, project=args.project, max_results=args.n)
    print(f"Wrote {out}")


def cmd_ingest(args):
    from . import ingest
    folder = ingest.run(args.src, citekey=args.citekey, title=args.title,
                        authors=args.authors, year=args.year)
    print(f"Ingested -> {folder}")


def cmd_new_experiment(args):
    from . import experiment
    code_dir, vault_dir = experiment.run(args.name)
    print(f"Created {code_dir}\n        {vault_dir}")


def cmd_status(args):
    root = repo_root()
    v = root / "vault"
    def count(sub, pattern):
        d = v / sub
        return len([p for p in d.glob(pattern)]) if d.exists() else 0
    print(f"ScholarWeave @ {root}")
    print(f"  literature : {count('10-literature', '*/note.md')} papers")
    print(f"  questions  : {count('40-questions', '*.md')}")
    print(f"  ideas      : {count('50-ideas', '*.md')}")
    print(f"  experiments: {count('60-experiments', 'EXP-*')}")
    print(f"  searches   : {count('90-search', '*.md')}")


def build_parser():
    p = argparse.ArgumentParser(prog="scholarweave",
                                description="Local AI-driven research knowledge base.")
    p.add_argument("--version", action="version", version=f"scholarweave {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    pi = sub.add_parser("init", help="scaffold the project layout")
    pi.add_argument("path", nargs="?", default=".")
    pi.set_defaults(func=cmd_init)

    ps = sub.add_parser("search", help="search arXiv into vault/90-search")
    ps.add_argument("query")
    ps.add_argument("--project", default=None)
    ps.add_argument("-n", type=int, default=20, help="max results")
    ps.set_defaults(func=cmd_search)

    pg = sub.add_parser("ingest", help="convert a source into a per-paper folder")
    pg.add_argument("src", help="file in vault/00-inbox or any path")
    pg.add_argument("--citekey", default=None)
    pg.add_argument("--title", default=None)
    pg.add_argument("--authors", default=None, help="semicolon-separated")
    pg.add_argument("--year", default=None)
    pg.set_defaults(func=cmd_ingest)

    pe = sub.add_parser("new-experiment", help="scaffold a validation experiment")
    pe.add_argument("name")
    pe.set_defaults(func=cmd_new_experiment)

    pt = sub.add_parser("status", help="show vault counts")
    pt.set_defaults(func=cmd_status)
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    main()
