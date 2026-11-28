# Mango Shark Documentation

Developer documentation for Mango Shark Studio's Roblox games, the template every new game starts from, and the
systems that can be dropped into any of them.

## Games

| Game | What it is | Start here |
| --- | --- | --- |
| **Gun Game** (SiegeBlox) | A first-person tactical shooter based on Rainbow Six Siege: 1v1 and 5v5 Siege, Ranked, Clear House, Recruit Training, bots, a lobby with parties | [Gun Game overview](Gun%20Game/index.md) |

New games get their own folder at the top of this repository; [New game docs](game-templates/new-game-docs.md) says how.

## Build a new game

1. Install the [Game Template asset](game-templates/game-template.md) into a new place: the module loader, networking,
   player data, effects, settings and combat that every Mango Shark game shares.
2. Add the [separate systems](systems/index.md) the game needs, such as the [Gun System](systems/gun-system/index.md).
3. Start the game's docs from [New game docs](game-templates/new-game-docs.md).

## Downloads

| File | What it is | Page |
| --- | --- | --- |
| [GameTemplate.rbxm](game-templates/GameTemplate.rbxm) | The framework every game starts from | [Game Template asset](game-templates/game-template.md) |
| [GunSystem.rbxm](systems/gun-system/GunSystem.rbxm) | First-person guns, loadouts, movement and camera, no skins | [Gun System asset](systems/gun-system/index.md) |

Both are also kept, ready to save again, in the Gun Game place under `ServerStorage.MangoShark`.

## How this site is organized

| Section | Folder in the repository | Holds |
| --- | --- | --- |
| Home | `home/` | This page |
| Gun Game | `Gun Game/` | Everything about one game: its rules for AI agents (`CLAUDE.md`), code map, system guides, API, changelog |
| Game templates | `game-templates/` | The Game Template asset, and the docs layout a new game copies |
| Separate systems | `systems/` | Drop-in assets that work in any game built on the template |

!!! note "For AI agents"

    Work on a game starts with that game's `CLAUDE.md` and `AI_CODING_GUIDE.md` (for Gun Game:
    [CLAUDE.md](Gun%20Game/CLAUDE.md)). Work on a template or a separate system starts with its page here. The site is
    built from several folders by `hooks/multi_root.py`; add a new top-level folder there and in `nav`.
