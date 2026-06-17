---
name: build-idea
description: >
  Co-construct an idea / method draft from a scientific question and its supporting
  papers, filing it as a structured idea note. Triggers on "/build-idea",
  "构建 idea", "propose a method for this question", "brainstorm approaches".
allowed-tools: Read Write Edit Glob Grep
---

# build-idea

Input: one `vault/40-questions/Q*.md` + a few linked notes. Output:
`vault/50-ideas/I<n>-<slug>.md` from `config/templates/idea.md`.

Steps:
1. Read the question and 2–5 linked `note.md` files.
2. Draft the idea: the method, the intuition for why it could work, and the
   single cheapest **minimal test** that could validate or kill it.
3. List risks/unknowns honestly. Link provenance to `80-archive` if it came from chat.
4. Hand the minimal test to design-validation.

Return the idea id + one-line pitch to the orchestrator.
