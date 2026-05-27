# Repository Structure

`cn-patent` keeps the repository root installable as a skill. This makes installation simple: clone the repository into a host `skills/` directory and restart the host.

## Runtime Files

| Path | Role |
| --- | --- |
| `SKILL.md` | skill entrypoint, trigger metadata, workflow map |
| `agents/openai.yaml` | Codex UI metadata |
| `prompts/` | step-specific instructions loaded only when needed |
| `references/` | longer domain guidance loaded only when needed |
| `tools/` | deterministic helpers for Office extraction, CNIPA search, diagram rendering, Word export, and revision logs |

## Human-Facing Files

| Path | Role |
| --- | --- |
| `README.md` | primary GitHub entrypoint |
| `INSTALL.md` | host-specific installation and dependency guide |
| `docs/` | product notes, screenshots, generated visual assets |
| `examples/` | synthetic cases for first-run and regression testing |
| `tests/` | offline contract and smoke tests |

## Output Policy

Generated user deliverables should go under:

```text
outputs/<case-name>/
```

The repository ignores `outputs/` so private drafts do not get committed accidentally.

Every delivered disclosure should use:

```text
案件名_YYYYMMDDHHmmss.md
案件名_YYYYMMDDHHmmss.docx
```

Iterative revision work should append one entry to:

```text
交底书修订对话记录.md
```

## Naming

The public repository, skill folder, skill name, install path, and default invocation should all be `cn-patent`.

## Validation

Run before releasing:

```bash
python tests/test_skill_contract.py
python -m py_compile tools/*.py tests/*.py
python tools/md_to_docx.py -i examples/quickstart-case/expected/minimal-disclosure.md -o /tmp/cn-patent-smoke.docx
```

For Codex-compatible metadata:

```bash
python ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```
