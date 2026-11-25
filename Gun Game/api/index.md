# API guide

This is the developer guide to the code in the **SiegeBlox** place (the Gun Game codebase). Every page explains what a system does, how its pieces fit together, and shows the real code that runs it. **Every public function has its own entry with what it returns and a code example**, so you can copy the call and adapt it.

!!! tip "New to the codebase? Read these three pages first"

    1. [Modules and loading](foundations/modules.md): where code lives and how it starts.
    2. [Extension points](foundations/extensions.md): how systems talk to each other without hard-wiring.
    3. [Networking with Packets](foundations/packets.md): how the client and server talk.

    Everything else in the game is built from these three ideas.

## How the code is organized

The game follows four rules. Once you know them, most of the code reads the same way.

| Rule | What it means in practice |
| --- | --- |
| **The server decides** | Clients only send *intent* ("I pulled the trigger", "I want to queue"). The server checks every request and owns ammo, damage, health, charges, timers and saved data. |
| **Content is data** | Numbers, guns, classes, crates and modes live in `ReplicatedStorage.Content` as plain tables. Change a number there, not in system code. |
| **Systems don't name each other's features** | A system asks an [extension point](foundations/extensions.md) ("may this player plant?") and any module can answer. That is how quests, analytics and the tutorial hook into Siege without Siege knowing they exist. |
| **One module, one job** | Each ModuleScript is a service or library with a doc comment at the top. That comment is the contract; this site expands on it. |

```text
          Client (LocalPlayer)                                Server
 ┌─────────────────────────────────┐            ┌─────────────────────────────────────┐
 │ Client.* modules                │  Packets   │ Systems.* services                  │
 │  input, HUD, menus, viewmodel   │ ─────────▶ │  check the request, change state    │
 │  plays effects it is sent       │ ◀───────── │  send snapshots / effects back      │
 └─────────────────────────────────┘            └─────────────────────────────────────┘
                 ▲                                              │
                 │      Shared.* (both sides)  Content.* (data) │
                 └──────────────────────────────────────────────┘
                       Extensions · Packets · Data · Ballistics · Smoke
```

## Where code lives

| Short name used in these docs | Full path | Runs on |
| --- | --- | --- |
| `Systems.*`, `Services.*`, `Helpers.*` (server) | `ServerScriptService.Modules.*` | Server only |
| `Shared.*`, `Handlers.*`, `Helpers.*`, `Classes.*` | `ReplicatedStorage.Modules.*` | Both |
| `Client.*` | `ReplicatedStorage.Modules.Client.*` (`ClientOnly` attribute) | Client only |
| `Content.*` | `ReplicatedStorage.Content.*` | Both: data tables |

## Find the right page

### Foundations

| Page | Read it when you… |
| --- | --- |
| [Modules and loading](foundations/modules.md) | add a new service or wonder why `Init`/`Start` run in a certain order |
| [Extension points](foundations/extensions.md) | want to react to, veto or scale something another system does |
| [Networking with Packets](foundations/packets.md) | need the client to ask the server for something, or the server to tell clients |
| [Player data and content](foundations/data-and-content.md) | save something per player, or add a gun, class, crate or mode as data |
| [Effects and sound](foundations/effects.md) | need a sound or visual to play for one player or everyone |
| [Handlers and helpers](foundations/helpers.md) | need player states, animations, rate limits, retries, loot rolls, product ids |

### Game systems

| Page | Covers |
| --- | --- |
| [Siege match](systems/siege.md) | `ServerRole`, `SiegeService` phases and win rules, rounds, spectating, Recruit Training, Clear House |
| [Matchmaking and parties](systems/matchmaking.md) | `PartyService`, `QueueService`, `MatchHost`, queue modes, how a match is formed |
| [Classes and abilities](systems/classes.md) | `ClassService`, the ability context, `Gadgets`, writing a new ability |
| [Class abilities](systems/abilities.md) | All 18 shipped abilities: what each does, its tuning and hooks |
| [Drones and cameras](systems/drones-cameras.md) | `DroneService`, `CameraService`, scans and marks |
| [Guns](systems/guns.md) | `GunService` shot pipeline, loadouts, gun abilities, gun bash, gun definitions |
| [Movement and camera](systems/movement.md) | `MovementService` checks, movement states, `MovementController`, `MovementCamera` |
| [Combat and damage](systems/combat.md) | `Combat.ApplyHit`, shields, kill credit, kill feed, death camera |
| [World: boards, soft walls, grenades](systems/world.md) | `BreakableService`, `SoftWalls`, `ConsumableService`, smoke |
| [NPCs and bots](systems/npcs.md) | `NPCService`, behavior trees, guard mode, Siege bots |
| [Lobby, teleporters and gun range](systems/lobby.md) | `LobbyService`, teleport pads, the gun animation range |
| [Progression and economy](systems/progression.md) | Store, currencies, crates, skins, stats, battle pass, quests |
| [Progress, leaderboards, analytics](systems/progress-analytics.md) | Flame streak, weekly goal, levels, badges, leaderboards, reminders, `AnalyticsService` |
| [Settings and keybinds](systems/settings.md) | `PlayerSettings`, `SettingsService`, `Keybinds`, `Options` |
| [Client: menus, HUD, screens](systems/client.md) | `Menus`, notices, tooltips, UI feel, screens, HUD, theme |

### Reference

| Page | Use it to look up… |
| --- | --- |
| [Cookbook](cookbook.md) | "I want to…" one-liners for common tasks |
| [All extension points](reference/extension-points.md) | every point in the game, its kind and arguments |
| [All packets](reference/packets.md) | every network packet, its direction and arguments |
| [Attributes, tags and collision groups](reference/attributes.md) | what an attribute or tag means and who sets it |
| [Admin commands (Cmdr)](reference/commands.md) | the F2 command bar, and how to add a command |
| [Legacy APIs](reference/legacy.md) | replaced systems you may still see in old code |

!!! info "How these pages were written"

    Every signature and code excerpt on these pages was read from the place's source in Studio (2026-11-24). Each section names its source module, so if something looks wrong, open that module: its top comment is the source of truth. When you change a module's public API, update its page in the same change.
