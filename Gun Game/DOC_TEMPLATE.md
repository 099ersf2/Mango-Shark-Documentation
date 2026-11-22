[Documentation home](index.md) / Internal developers

# Documentation authoring

Use this template when adding or substantially revising an internal developer guide. Copy the sections that apply; remove unused headings rather than leaving empty sections.

## Status labels

Use a short status note near the top of a guide when readers could mistake implementation history for current behavior:

- **Current** — describes the active implementation.
- **Historical** — kept for context; do not use as implementation guidance.
- **Mixed** — current guidance includes clearly marked historical details.

For verification, state the date, test environment, and limits. Use **Not verified** when a behavior has not been exercised. Do not infer that a dated unchecked item is still open without checking it against the current build.

## Page outline

```markdown
[Documentation home](index.md) / [System]

# [System name]

One sentence explaining what the system does and who changes it.

> **Status:** Current / Historical / Mixed.
> **Last verified:** YYYY-MM-DD, environment/device; or Not verified.

## At a glance

| Concern | Details |
| --- | --- |
| Runtime | Server, client, or both |
| Code and assets | The paths developers should edit |
| Dependencies | Related systems or setup |

## Common tasks

Link the most common implementation and debugging workflows.

## How it works

Explain the current flow and key interfaces.

## Verify changes

List reproducible checks and distinguish verified behavior from assumptions.

## Limits and history

Record known gaps and link to dated history where it helps.
```

## Maintenance rules

- Write for developers changing and testing the game, not players.
- Put current implementation guidance before history.
- Link to the focused API page and related system guides; use [API.md](API.md) as the API entry point.
- Keep detailed dated change records in [CHANGELOG.md](CHANGELOG.md). Keep [NEXT_STEPS.md](NEXT_STEPS.md) limited to actionable work still confirmed to be open.
- Add each published page to the navigation in `mkdocs.yml` and the relevant section of [index.md](index.md).
- Run `mkdocs build --strict` before submitting. It validates navigation, local links, and anchors.
