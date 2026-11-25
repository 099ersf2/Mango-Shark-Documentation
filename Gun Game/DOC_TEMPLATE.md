# Documentation authoring

Use this template when adding or substantially revising an internal developer guide. Copy the sections that apply; remove unused headings rather than leaving empty sections.

## Status labels

Use a short status note near the top of a guide when readers could mistake implementation history for current behavior:

- **Current** — describes the active implementation.
- **Historical** — kept for context; do not use as implementation guidance.
- **Mixed** — current guidance includes clearly marked historical details.

For verification, state the date, test environment, and limits. Use **Not verified** when a behavior has not been exercised. Do not infer that a dated unchecked item is still open without checking it against the current build.

## Page outline

````markdown
# [System name]

One sentence explaining what the system does and who changes it.

!!! info "Status"

    Current / Historical / Mixed. Last verified: YYYY-MM-DD, environment/device; or Not verified.

## At a glance

| Concern | Details |
| --- | --- |
| Runtime | Server, client, or both |
| Code and assets | The paths developers should edit |
| Dependencies | Related systems or setup |

## Common tasks

Link the most common implementation and debugging workflows.

## Examples

Show at least one real call for each common task. Say where it runs, then the code:

**Runs on:** server.

```lua
local MyService = require(game.ServerScriptService.Modules.Systems.MyFeature.MyService)

MyService.Do(player, 10)
```

## How it works

Explain the current flow and key interfaces.

## Verify changes

List reproducible checks and distinguish verified behavior from assumptions.

## Limits and history

Record known gaps and link to dated history where it helps.
````

## Formatting rules

The site is built with MkDocs (Python-Markdown), which is stricter than GitHub's preview. These rules keep pages rendering correctly:

- **Leave a blank line before every list**, or it renders as one run-on paragraph.
- **Indent nested list items by 4 spaces**, not 2, or they render flat.
- **Use admonitions for notes**, not blockquotes: `!!! info "Status"`, `!!! warning "Not verified"`, `!!! note "Updated YYYY-MM-DD"`, `!!! example "Title"`. Indent the body by 4 spaces.
- **Link text is the page or section name** (`[Adding guns](ADDING_GUNS.md)`), not the file name.
- **Don't add a breadcrumb line**; the theme draws one from the navigation.
- **Keep table cells short.** When a cell needs more than two or three sentences, use a list or a subsection instead. `<br><br>` can split a long cell into paragraphs.
- **Code blocks** are fenced with a language: ` ```lua `. Use tabs (`=== "Server"` / `=== "Client"`) when one task needs code on both sides.

## Maintenance rules

- Write for developers changing and testing the game, not players.
- Put current implementation guidance before history.
- Give every common task a code example, either on the page or in [Task-based code examples](EXAMPLES.md).
- Link to the focused API page and related system guides; use the [API guide](api/index.md) as the API entry point.
- Keep detailed dated change records in [Recent changes](CHANGELOG.md). Keep [Next steps](NEXT_STEPS.md) limited to actionable work still confirmed to be open.
- Add each published page to the navigation in `mkdocs.yml` and the relevant section of [index.md](index.md).
- Run `mkdocs build --strict` before submitting. It validates navigation, local links, and anchors.
