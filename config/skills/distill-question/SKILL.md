---
name: distill-question
description: >
  Distill a concrete, falsifiable scientific question (with importance and
  significance) from a set of paper notes. Optionally uses Co-STORM / gpt-researcher
  for multi-perspective coverage. Triggers on "/distill-question", "凝练科学问题",
  "what's the research question", "frame the problem".
allowed-tools: Read Write Edit Glob Grep WebSearch
---

# distill-question

Input: a few notes in `vault/10-literature/`. Output: `vault/40-questions/Q<n>-<slug>.md`
from `config/templates/question.md`.

Steps:
1. Read 3–8 relevant `note.md` files (not full papers).
2. Identify the gap: what do existing methods fail at? cite with `[[citekey]]`.
3. Write ONE sentence question, then **why it matters** and **significance**.
4. State a **falsifiable expectation** (what result would confirm/deny it).
5. Optionally run Co-STORM / gpt-researcher for related-work breadth, file extra
   findings as concepts.

Return the question id + one-line statement to the orchestrator.
