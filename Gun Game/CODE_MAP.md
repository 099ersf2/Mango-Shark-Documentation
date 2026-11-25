# Code map

One page that shows where every part of the Gun Game (SiegeBlox) code lives, what each module does, and how the
pieces talk to each other. Use it to find the module to open; the linked system pages have the full API.

!!! info "How this map was made"

    Built from this documentation site (API pages read from the place's source on 2026-11-24), not from a live
    Studio session. If a module here is missing or moved in the place, the module's own `--[[ ]]` header is the
    source of truth: fix this page in the same change.

## The big picture

```text
                          ReplicatedStorage.ModuleLoader
                     load (require) ─▶ Init ─▶ Start, every module
                                         │
        ┌────────────────────────────────┼──────────────────────────────────┐
        ▼                                ▼                                  ▼
 ServerScriptService.Modules     ReplicatedStorage.Modules          ReplicatedStorage.Content
 (server only)                   (both sides)                        (data and tuning, read-only)
  Systems.*   game services       Shared.*    Packets, Extensions,   Guns, Classes, Games.Siege,
  Services.*  join, settings,                 Data, gun math, smoke  Matchmaking, NPC, Store,
              Cmdr                Handlers.*  states, animations     Crates, BattlePass, Quests,
  Helpers.*   server helpers      Helpers.*   retry, rate limits     Progress, Effects, Theme …
                                  Classes.*   Admins, HealthUI
                                  Client.*    (ClientOnly) input,
                                              HUD, menus, viewmodel
```

| Rule | What it means for the code |
| --- | --- |
| One loader | No Scripts or LocalScripts: every module is a ModuleScript under `Folder`s in a loaded container |
| Server decides | Clients send intent through `Shared.Packets`; `Systems.*` validate and own the state |
| Extension points | Systems ask `Shared.Extensions` (`Any` veto, `Product` multiplier, `Fire` event) instead of naming each other |
| Content is data | Every number lives in `ReplicatedStorage.Content.*` |

Details: [Modules and loading](api/foundations/modules.md), [Extension points](api/foundations/extensions.md),
[Networking with Packets](api/foundations/packets.md).

## Two kinds of server

`Systems.Matchmaking.ServerRole` decides which code paths run.

| Role | Runs | Main modules |
| --- | --- | --- |
| **Lobby** | Parties, queue, matchmaker, store, lobby hub, gun range | `PartyService`, `QueueService`, `TeamPacker`, `LobbyService`, `Teleporters`, `GunShowcase`, `StoreService` |
| **Match** (reserved private server) | One Siege match, then everyone goes back | `MatchHost`, `SiegeService`, `SiegeMap`, `SpectateService`, `SiegeBots` |
| **Studio** | Both at once; MemoryStore and teleports replaced when `Content.Matchmaking.STUDIO_LOCAL` | all of the above |

```text
Lobby: PLAY ─▶ Queue.Request ─▶ QueueService ticket (MemoryStore) ─▶ matchmaker lease holder
       ─▶ TeamPacker.Pack ─▶ ReserveServer + match record ─▶ teleport { MatchId }
Match: MatchHost reads record ─▶ SiegeService phases ─▶ End ─▶ MatchHost.ReturnAll
Lobby: PartyService.Restore puts each party back together
```

## Server: `ServerScriptService.Modules`

### `Systems.*`

| Area | Modules | Job | Page |
| --- | --- | --- | --- |
| **Matchmaking** | `ServerRole`, `PartyService`, `QueueService`, `TeamPacker`, `MatchHost`, `Store` (MemoryStore wrapper) | Server role, parties, queue tickets, forming matches, hosting the record | [Matchmaking](api/systems/matchmaking.md) |
| **Games.Siege** | `SiegeService`, `SiegeMap`, `SpectateService`, `TutorialService`, `SiegeBots`, `BotDrones` | Match phases and win rules, map load and rebuild, spectating, Recruit Training, bots | [Siege match](api/systems/siege.md) |
| **Games.ClearHouse** | `ClearHouse` | Clear House mode | [Clear House](CLEAR_HOUSE.md) |
| **Classes** | `ClassService`, `Gadgets`, `Abilities.*` (18 modules, required by `ClassService`) | Class picks, charges and cooldowns, placed gadgets, every ability | [Classes](api/systems/classes.md), [Abilities](api/systems/abilities.md) |
| **Guns** | `GunService`, `LoadoutService`, `AbilityRunner` | Shot pipeline, ammo and reload, loadouts, per-gun ability hooks | [Guns](api/systems/guns.md) |
| **Combat** | `Combat`, `DamageLog`, `KillFeed`, `DeathCamService`, `GunMelee`, `SpawnProtection`, `SwordCombat` (off limits) | `ApplyHit`, friendly fire, shields, kill credit, kill feed, death camera, gun bash | [Combat](api/systems/combat.md) |
| **Drones** / **Cameras** | `DroneService`, `CameraService` | Scout drones, defender cameras, scans and marks | [Drones and cameras](api/systems/drones-cameras.md) |
| **Movement** | `MovementService` | Server check of movement states (sprint, crouch, prone, lean …) | [Movement](api/systems/movement.md) |
| **NPC** | `NPCService`, `Brain`, `Tactics`, `Tasks.*` | Enemies in `workspace.Enemies`, behavior trees, guard mode | [NPCs](api/systems/npcs.md) |
| **Breakables** / **Destruction** | `BreakableService`, `SoftWalls` | Boarded windows and doors, holes in soft walls | [World](api/systems/world.md) |
| **Consumables** | `ConsumableService` | Grenades and smoke | [World](api/systems/world.md) |
| **Lobby** / **Showcase** | `LobbyService`, `Teleporters`, `GunShowcase` | First spawn in the lobby, teleport pads, gun animation range | [Lobby](api/systems/lobby.md) |
| **Store** | `StoreService`, `StatsService`, `BotCoinService`, `PassCosmetics` | Purchases, crates, gifting, currencies, stats | [Progression](api/systems/progression.md) |
| **SkinShopService** | `SkinShopService` | Equip skins, buy skin crates | [Skins](SKINS.md) |
| **BattlePass** | `BattlePassService`, `QuestService` | Pass XP and rewards, quests | [Battle pass](BATTLE_PASS.md) |
| **Progress** | `ProgressService`, `LeaderboardService`, `NotifyService` | Flame streak, weekly goal, levels, badges, boards, reminders | [Progress](api/systems/progress-analytics.md) |
| **Analytics** | `AnalyticsService` | Funnels, events, journeys | [Analytics](ANALYTICS.md) |
| **Effects** | `EffectService` | Plays registered effects on clients | [Effects](api/foundations/effects.md) |
| **Other** | `Ping.PingService`, `Lasers.LaserLinks`, `Traps.SpikeTrap` | Pings, laser tripwires, spike traps | system guides |
| **Legacy** | `Match.MatchService`, `Match.TeamService`, `Round.RoundService` | Old match flow; `TeamService` (the `Team` attribute) is still used | [Legacy APIs](api/reference/legacy.md) |

### `Services.*` and `Helpers.*`

| Module | Job |
| --- | --- |
| `Services.PlayerJoin` | Player join setup |
| `Services.SettingsService` | Saves keybinds, volumes and options from `Packets.Settings.*` |
| `Services.CmdrSetup` (+ `Commands`) | Admin command bar (F2); each command is a `Name` + `NameServer` pair |
| `Services.Example` / `Systems.Example.ExampleService` | Example code (`Example.Ping`/`Pong`); safe to delete |
| `Helpers.*` (server) | Server-only helpers |

## Shared: `ReplicatedStorage.Modules`

| Module | Job |
| --- | --- |
| `Shared.Packets` / `Shared.UnreliablePackets` | Every network message ([All packets](api/reference/packets.md)) |
| `Shared.Extensions` | Extension points: `Any`, `Product`, `Fire`, `Add` ([All points](api/reference/extension-points.md)) |
| `Shared.Data` | Saved player data and shared server state (Scribe on ProfileStore) |
| `Shared.PlayerSettings` (`Actions`, `Options`) | Keybind actions and options (a Scribe fragment) |
| `Shared.Guns.*`: `Ballistics`, `Spread`, `Spring`, `Abilities` | Gun math both sides agree on: seeded pellets, falloff, spread, hooks |
| `Shared.Movement.States` | Movement state machine |
| `Shared.Smoke` (`Blocks`), `Shared.BallisticShield`, `Shared.CameraRig`, `Shared.CursorAim` | Smoke sight checks, shields, camera rig, cursor aim |
| `Shared.StoreGrants`, `Shared.ProductIds`, `Shared.ReadOnly` | Grant logic, product ids, frozen tables |
| `Handlers.StateHandler`, `AnimationHandler`, `HitPopup` | Player states, animations, hit numbers |
| `Helpers.Retry`, `TokenBucket`, `Rarity`, `SetCollisionGroup`, `TableHelpers`, `UIHelpers`, `CreateWatchedTable`, `TableLength` | Retries, rate limits, loot rolls, collision groups, table and UI utilities |
| `Classes.Admins`, `Classes.HealthUI` | Admin list, health UI class |
| `Utilities/`, `Packages/` | Third-party code (`Packet`, Scribe, FastCast2 …): off limits |

## Client: `ReplicatedStorage.Modules.Client` (`ClientOnly`)

| Folder | Modules | Job |
| --- | --- | --- |
| **Core** | `Menus`, `UI`, `Notice`, `Tooltip`, `UIFeel`, `Peek`, `MenuAmbience`, `Matchmaking`, `ModeMenu`, `LobbyHubUI`, `LobbyReset`, `SiegeSelect`, `Store`, `StoreViews`, `Inventory`, `ItemDetails`, `SkinShop`, `GiftPicker`, `BattlePass`, `Goals`, `Celebrate`, `DailyFlame`, `FlameFx`, `ClassPanel`, `CardIntro`, `Spectate`, `Music`, `AnalyticsClient`, `IconBinder`, `CoinIcon`, `Shine`, `AutoContrast`, `Readability`, `LazyPreviews`, `ViewHide`, `MatchMenu` (legacy) | Menus and screens, lobby and queue UI, store, inventory, pass, goals, music |
| **Hud** | `SiegeHud`, `SiegeTopBar`, `Scoreboard`, `RoundHud`, `DeathScreen`, `Nameplates`, `HealthBillboards`, `PersonalHealth`, `StreakTags`, `PingController`, `BotCallouts`, `Tutorial`, `TutorialCoach`, `MatchHud` (legacy) | In-match HUD |
| **Guns** | `GunController`, `Viewmodel` (+ `GunModel`), `GunHud`, `WeaponSlots`, `LoadoutMenu`, `GunEffects`, `GunMechanics`, `Recoil`, `AimAssist`, `ThirdPersonGuns`, `Consumables`, `SkinRainbow`, `Quality` | Firing intent, first- and third-person guns, recoil, aim assist |
| **Gadgets** | `DroneController`, `DroneBoost`, `CameraController`, `FeedInfo`, `LeoMotionWarning` | Drone and camera views |
| **Movement** | `MovementController`, `MovementCamera`, `MovementPoses`, `MovementDebug` | Movement input, camera, poses |
| **Combat** | `DamageFeedback`, `KillFeed`, `CharacterHurt`, `SwordInput` (off limits) | Hit feedback, kill feed |
| **Settings** | `Keybinds`, `Options`, `Slider`, `SettingsMenu` | Settings screen |
| **Interact** | `PromptKeys`, `CustomPrompts`, `ReinforcePrompt` | Proximity prompts |
| **Other** | `Effects` (+ `Context`), `Audio.AudioSettings`, `Kills.Observe`, `Coins.Observe`, `CmdrClient` | Effects playback, audio groups, observers, command bar |

Camera render priority: `MovementCamera` Camera+1, `Viewmodel` +2, drone camera +3, death camera +4.

## Content: `ReplicatedStorage.Content`

| Module | Holds |
| --- | --- |
| `Guns.*`: `Definitions`, `Registry`, `Types`, `Mechanics`, `Abilities`, `Loadouts`, `Melee`, `Skins`, `SeasonSkins` | Every gun, its numbers, loadouts and skins |
| `Classes.Classes`, `Classes.Definitions.*` | Every Siege class and its ability `Tuning` |
| `Games.Siege`, `Games.SiegeBots`, `Games.Tutorial`, `Games.ClearHouse` | Match timers, rounds, bomb, bots, training, Clear House |
| `Matchmaking` | Queue modes, categories, party limits, MemoryStore names, `STUDIO_LOCAL` |
| `NPC.Profiles.*`, `NPC.Types` | NPC profiles (`Soldier`, `SiegeBot`, `TutorialBot` …) |
| `Drones`, `Cameras` | Drone and camera numbers |
| `Movement.Config` | Movement speeds and camera |
| `Breakables.*`, `Destruction.SoftWallConfig`, `Consumables.*` | World objects and grenades |
| `Store.*`, `Crates.*`, `BattlePass`, `Quests`, `Progress`, `Analytics` | Economy, progression, analytics |
| `Effects.Registry`, `Effects.Parts.*`, `Music`, `Icons`, `Theme` | Effects, songs, icons, UI colors and fonts |
| `Match.*` | Legacy modes, settings, teams |

## How the main flows cross the code

| Flow | Path through the modules |
| --- | --- |
| **A shot** | `Client.Guns.GunController` ─ `Gun.Fire` ─▶ `GunService.Fire` (checks, `Gun.PreventFire`) ─▶ `Shared.Guns.Ballistics` (seeded pellets) ─▶ `AbilityRunner` ─▶ `Combat.ApplyHit` ─▶ `Combat.Death`; boards via `BreakableService`, walls via `SoftWalls`; others see it via `EffectService` + `UnreliablePackets.GunFired` |
| **An ability** | `Client.Hud.SiegeHud.UseAbility` ─ `Class.Use` ─▶ `ClassService.Use` (charges, `Classes.PreventAbility`) ─▶ `Abilities.<Name>.Use(context)` ─▶ `Gadgets` ─▶ `Class.State` back to the owner |
| **A round** | `SiegeService`: Selection (`Siege.Pick`) ─▶ Reveal ─▶ Prep (attackers in `DroneService`) ─▶ Action ─▶ RoundEnd (`SiegeMap` rebuild) ─▶ End ─▶ `MatchHost.ReturnAll` |
| **A death** | `Combat` ─▶ `KillFeed` (`Combat.KillFeed`) ─▶ `DeathCamService` / `SpectateService` ─▶ `Death.Killed` ─▶ `Client.Hud.DeathScreen` |
| **A purchase** | `Client.Core.Store` ─ `Store.Buy` (answered) ─▶ `StoreService` ─▶ `Shared.Data` ─▶ `Store.Reward` |
| **Rewards after a match** | `Siege.Ended` ─▶ `BattlePassService`, `QuestService`, `ProgressService`, `AnalyticsService` (all through extension points) |

## Things that differ from older notes

- The match is run by `SiegeService` on a reserved match server. `MatchService` and `RoundService` are legacy;
  only `TeamService` is still used.
- `Drone.Spot` / `Drone.Spotted` packets were replaced by `Drone.Scan` / `Drone.Marked` (2026-11-11).
- The `Tokens` currency is unused since 2026-11-15.
