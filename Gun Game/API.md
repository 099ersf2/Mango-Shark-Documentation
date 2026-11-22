[Documentation home](index.md) / Gun Game

# API reference

A searchable reference for internal developers working on the Gun Game Roblox place. It covers functions, packets, content modules, commands, attributes, tags and collision groups.

> **Current-game note:** Siege is the active mode. The pages below distinguish current APIs from mixed or historical references; when behavior matters, follow the linked system guide and its verification notes.

## Choose a reference

| Work area | Start here |
| --- | --- |
| Current Siege, matchmaking, classes, cameras and drones | [Current Siege APIs](API_SIEGE.md) |
| Server services and combat | [Server-side APIs](API_SERVER.md) |
| Shared modules, data, extension points and packets | [Shared APIs](API_SHARED.md) |
| Client modules, effects, guns, movement and menus | [Client APIs](API_CLIENT.md) |
| Content modules, Cmdr, attributes, tags and collision groups | [Content and metadata](API_CONTENT.md) |
| General task recipes | [Common API recipes](API_RECIPES.md) |
| A focused example for a specific task | [Task-based code examples](EXAMPLES.md) |

## Runtime paths

| Short name | Full path | Runs on |
| --- | --- | --- |
| `Systems.*`, `Services.*`, `Helpers.*` (server) | `ServerScriptService.Modules.*` | Server only |
| `Shared.*`, `Handlers.*`, `Helpers.*`, `Classes.*` | `ReplicatedStorage.Modules.*` | Both |
| `Client.*` | `ReplicatedStorage.Modules.Client.*` (`ClientOnly` attribute) | Client only |
| `Content.*` | `ReplicatedStorage.Content.*` | Both; most modules return data tables |

Every module loads through ModuleLoader (`Init`, then `Start`). Require modules from your own module's `Init` or `Start`, or at the top. A loose `Script` or Studio command bar gets its **own copy** of a module, not the running one; test from a module or a temporary `Script`.

```lua
-- Server
local GunService = require(game.ServerScriptService.Modules.Systems.Guns.GunService)
-- Shared
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)
-- Client
local Effects = require(game.ReplicatedStorage.Modules.Client.Effects)
```

## Historical references

[Matches, modes and teams](MATCH.md) and [Team deathmatch rounds](ROUND_SYSTEM.md) describe replaced systems. Some legacy entries remain in the general API pages for searchability; do not treat them as current implementation guidance.
