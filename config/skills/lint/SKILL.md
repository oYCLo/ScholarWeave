---
name: lint
description: >
  Housekeeping pass over the vault: find duplicate concepts, broken [[links]],
  orphan notes, and missing frontmatter. Triggers on "/lint", "清理知识库",
  "check the vault", "find broken links".
allowed-tools: Read Edit Glob Grep Bash
---

# lint

Keep the knowledge graph clean so links stay meaningful.

Checks:
1. Broken `[[wikilinks]]` -> report or fix the target.
2. Duplicate/near-duplicate concept notes -> propose a merge.
3. Orphans (no inbound/outbound links) -> suggest where to link.
4. Missing/!malformed frontmatter vs the templates.
5. `scholarweave status` for a quick count sanity check.

Return only a change summary to the orchestrator; do not paste file contents.
