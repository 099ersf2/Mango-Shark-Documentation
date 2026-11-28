# Separate systems

Drop-in assets that work in any game built on the [Game Template](../game-templates/game-template.md). Each one is a
folder with an `Install` module and a `README`, saved as one `.rbxm` file.

| System | What it does | Status |
| --- | --- | --- |
| [Gun System](gun-system/index.md) | Server-authoritative first-person guns, loadouts, weapon slots, knife and bash, recoil, aim assist, plus the movement controller and camera | Packaged 2026-11-27 ([download](gun-system/GunSystem.rbxm)) |

## The most important systems to reuse

Ranked by how often another game would want them and how cleanly they come out of Gun Game. "Packaged" means it is
already in an asset; the others are candidates for the next assets.

| Rank | System | In Gun Game | Why it is worth reusing | Status |
| --- | --- | --- | --- | --- |
| 1 | Module loader, Packets, Extensions | `ModuleLoader`, `Shared.Packets`, `Shared.Extensions` | Every system is built on them | In the [Game Template](../game-templates/game-template.md) |
| 2 | Player data | `Shared.Data` (Scribe on ProfileStore) | Saving with session locks, fragments, migrations, products | In the Game Template |
| 3 | Effects | `Content.Effects.Registry`, `EffectService`, `Client.Effects` | Every sound and visual by name, pooled, replicated near or to all | In the Game Template |
| 4 | Settings and keybinds | `Shared.PlayerSettings`, `Client.Settings`, `SettingsService` | Rebinding, volumes and options on PC, gamepad and touch, saved | In the Game Template |
| 5 | Combat and damage | `Combat.ApplyHit`, `DamageLog` | Damage, friendly fire, kill credit, for players and NPCs | In the Game Template |
| 6 | Guns | `Systems.Guns`, `Client.Guns`, `Content.Guns` | The whole shooter core | [Packaged](gun-system/index.md) |
| 7 | Movement and camera | `MovementService`, `Client.Movement` | Sprint, crouch, slide, prone, lean, camera springs | Packaged inside the Gun System (recoil runs in its camera) |
| 8 | Parties and matchmaking | `PartyService`, `QueueService`, `TeamPacker`, `MatchHost` | Lobby to reserved match server and back, for any team game | Candidate. Needs `Content.Matchmaking` and the lobby UI split out |
| 9 | NPCs and behavior trees | `NPCService`, `Brain`, `Tactics` | Enemies and bots that use the same guns as players | Candidate. Uses the Gun System and Siege drones |
| 10 | Progress and badges | `ProgressService`, `LeaderboardService`, `Content.Progress` | Streaks, weekly goals, levels, badges, boards | Candidate. Hooks into Siege match results |
| 11 | Store and currencies | `StoreService`, `Content.Store`, `Shared.StoreGrants` | Robux products, passes, crates, gifting | Candidate. Tied to skins and Siege classes |
| 12 | Breakables and soft walls | `BreakableService`, `SoftWalls` | Boards, hatches and walls bullets break | Candidate. The Gun System already uses them when present |

## Making a new separate system

1. Build it in Gun Game under `ServerStorage.MangoShark.<Name>`, with one folder per service
   (`ReplicatedStorage`, `ServerScriptService`, ...) holding the items at their real paths.
2. Give it what it needs from the template through the merge points: a child of `Shared.Packets`, of
   `Content.Effects.Registry`, a `ScribeFragment` module ([Adding systems](../game-templates/game-template.md#adding-systems-without-editing-the-template)).
3. Copy the Gun System's `Install` and `README` modules and change the names in them.
4. Park every CollectionService tag in a `MangoSharkTags` attribute.
5. Save it to file, add it to this page with its own page and the `.rbxm`, and test it in an empty place with the
   template installed.
