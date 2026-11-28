# New game docs

Every game gets one folder at the top of this repository, laid out like `Gun Game/`. AI agents and people find the
same pages in the same places in every game.

## Start the folder

1. Make the folder at the top of the repository, named after the game (for example `Racing Game/`).
2. Add the pages below. Copy the matching Gun Game page and replace its content, or start empty.
3. Add the folder to `ROOTS` in `hooks/multi_root.py`.
4. Add a section for it under the `Gun Game` entry in `nav` in `mkdocs.yml`, and add the folder to the `paths` lists in
   `.github/workflows/docs.yml`.
5. Add a row to the **Games** table on the [home page](../index.md).
6. Run `mkdocs build --strict` and fix every warning.

## Pages every game keeps

| Page | Holds | Gun Game's version |
| --- | --- | --- |
| `index.md` | What the game is, how to start, links to everything | [Overview](../Gun%20Game/index.md) |
| `CLAUDE.md` | Hard rules for AI agents: what not to touch, how to verify, when to ask | [CLAUDE.md](../Gun%20Game/CLAUDE.md) |
| `AI_CODING_GUIDE.md` | How code is written in this game | [AI coding guide](../Gun%20Game/AI_CODING_GUIDE.md) |
| `CODE_MAP.md` | Where every module lives and how they talk | [Code map](../Gun%20Game/CODE_MAP.md) |
| `DOC_TEMPLATE.md` | How a system page is written | [Documentation authoring](../Gun%20Game/DOC_TEMPLATE.md) |
| `NEXT_STEPS.md` | What is unverified or planned | [Next steps](../Gun%20Game/NEXT_STEPS.md) |
| `CHANGELOG.md` | Every change, newest first | [Changelog](../Gun%20Game/CHANGELOG.md) |
| `DECISIONS.md`, `SECURITY.md`, `PERFORMANCE.md` | Why things are the way they are; exploit and performance notes | [Decisions](../Gun%20Game/DECISIONS.md) |
| One page per system | The system's job, data, packets, extension points and limits | [Gun system](../Gun%20Game/GUN_SYSTEM.md) |
| `api/` | Module-by-module API | [API](../Gun%20Game/api/index.md) |

## What to write first

For a game built on the [Game Template](game-template.md):

1. `CLAUDE.md`: copy Gun Game's, keep the rules that come with the template (one loader, the server decides, content
   is data, UI built in Studio), and replace the game-specific ones.
2. `CODE_MAP.md`: start with the template's layout ([What is in it](game-template.md#what-is-in-it)) and add each
   system as it lands.
3. A page for each [separate system](../systems/index.md) the game installs only if the game changes it; otherwise
   link the system's page.
