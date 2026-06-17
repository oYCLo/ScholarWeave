---
name: search-papers
description: >
  Turn a project description into search keywords and a triaged paper hit-list.
  Uses arXiv (via `scholarweave search` or an arXiv MCP) and snowballs from seed
  papers. Triggers on "/search-papers", "find papers on X", "搜论文", "literature
  search for X".
allowed-tools: Read Write Edit Glob WebSearch WebFetch Bash
---

# search-papers

Goal: from a one-paragraph direction, produce `vault/90-search/<project>.md` with
keywords + a triaged hit-list; do **not** dump full papers into context.

Steps:
1. Read the project description (ask the user to fill the template if missing):
   一句话方向 / 要解决的问题 / 种子论文 / 约束。
2. Expand into keywords: core concepts (3–5), synonyms, method terms,
   task/dataset terms, and combined query strings (arXiv & Semantic Scholar).
3. Run the search. Easiest path:
   `scholarweave search "<query>" --project <name> -n 25`
   (or call an arXiv / paper-search MCP if connected).
4. Snowball: for each seed paper, follow 1 hop of citations / references.
5. Triage: keep the most relevant, mark `[x]`. Hand kept PDFs to the ingest agent.

Output only the markdown file path + a 3-line summary back to the orchestrator.
