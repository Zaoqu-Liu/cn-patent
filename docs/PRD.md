# cn-patent Product Notes

## Purpose

`cn-patent` turns project evidence into a Chinese invention disclosure draft that can be reviewed by inventors, IP teams, and patent attorneys.

It focuses on:

- Chinese technical disclosure structure.
- CNIPA-first prior-art search.
- Technical problem / technical solution / technical effect reasoning.
- Source-grounded drafting from project materials.
- Markdown + Word delivery.
- Traceable revision rounds.

It does not provide legal conclusions, filing strategy, or attorney-reviewed claims.

## User Journey

```text
Install skill
  -> point the agent at project materials
  -> convert Office files when needed
  -> scan and summarize evidence
  -> mine candidate patent points
  -> run CNIPA-first prior-art search
  -> draft disclosure
  -> render diagrams and export Word
  -> self-check quality gates
  -> revise in new timestamped files when new material appears
```

## Product Principles

1. **Evidence first**: every technical claim should trace back to source material, prior-art search, or explicit user input.
2. **Chinese patent fit**: keep the T-P-E chain visible and check software/AI/data-processing cases for concrete technical means.
3. **User control**: do not overwrite earlier drafts unless explicitly asked.
4. **Graceful degradation**: if CNIPA tooling or Playwright is unavailable, continue with public web search and clearly state the degraded path.
5. **Reviewability**: write Markdown, Word, rendered diagrams, and revision logs to stable paths.

## Core Deliverables

| Deliverable | Rule |
| --- | --- |
| Markdown disclosure | `案件名_YYYYMMDDHHmmss.md` |
| Word disclosure | same stem as Markdown, `.docx` |
| Diagrams | mermaid source during drafting, PNG in final Markdown/Word |
| Revision log | append to `交底书修订对话记录.md` during merge/correction |
| Prior-art entries | verified public URL for each item in chapter 1.1 |

## Quality Gates

The workflow should reject weak patent points when they lack:

- a technical problem grounded in prior art or engineering constraints;
- a concrete technical solution;
- a technical effect that follows from that solution;
- implementation support in chapter 3 or chapter 6;
- a prior-art distinction that is not defined with hindsight.

See [references/cn-patent-quality.md](../references/cn-patent-quality.md).

## Failure Modes To Surface

- Office conversion dependencies missing.
- CNIPA search dependency or browser missing.
- CNIPA site unavailable or returns irrelevant/empty results.
- Mermaid rendering fails.
- Word export fails.
- Public source URL cannot be verified.
- User asks for legal conclusion rather than technical disclosure drafting.

The agent should continue only when a safe fallback exists and should tell the user which path was used.
