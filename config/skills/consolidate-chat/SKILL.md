---
name: consolidate-chat
description: >
  Distill a long AI co-construction chat into a deduplicated, archive-grade note
  (conclusions, decisions, open threads) rather than leaving it as scattered Q&A.
  Pairs well with basic-memory (MCP -> Markdown). Triggers on "/consolidate-chat",
  "凝练归档这段对话", "archive this conversation", "save what we figured out".
allowed-tools: Read Write Edit Glob
---

# consolidate-chat

Input: the current conversation. Output: `vault/80-archive/YYYY-MM-DD-<topic>.md`.

Steps:
1. Extract only durable value: conclusions reached, decisions made, rejected
   options (+why), and open questions. Drop the back-and-forth.
2. Deduplicate against existing archive/ and ideas/ notes; link, don't repeat.
3. Promote anything reusable: a conclusion -> `50-ideas` or `40-questions`;
   a fact -> `30-concepts`.
4. If basic-memory MCP is connected, let it persist the note so the next session
   starts with this context.

Target: "archive-grade", not "chat log". Return the archive path + 3 bullet TL;DR.
