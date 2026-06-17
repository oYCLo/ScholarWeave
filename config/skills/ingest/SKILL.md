---
name: ingest
description: >
  Convert one source (PDF/web/docx) into a per-paper folder under
  vault/10-literature/<citekey>/ with a structured note. Uses MarkItDown.
  Triggers on "/ingest", "ingest this paper", "把这篇论文入库", "process inbox".
allowed-tools: Read Write Edit Glob Bash
---

# ingest

Process exactly **one** source at a time (parallelize across agents, not within).

Steps:
1. Convert to Markdown and scaffold the folder:
   `scholarweave ingest <file> --title "..." --authors "Last, First; ..." --year 2024`
   This creates `vault/10-literature/<citekey>/` with note.md, meta.yaml,
   highlights.md, extracted.md, paper.pdf.
2. Read `extracted.md` (only this one file), then fill `note.md`:
   one-liner, problem, method core, setup, **falsifiable conditions & limits**,
   relation to my work. Add `[[links]]` to existing concepts/entities.
3. Pull 3–7 key quotes into `highlights.md`.
4. Update `vault/index.md` with the new `[[citekey]]`.

Return only the citekey + a one-line summary to the orchestrator. Keep
`extracted.md` out of the orchestrator's context.
