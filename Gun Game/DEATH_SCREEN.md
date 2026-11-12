# Death screen and spectating

When you die you see who killed you and with what, and the camera follows your killer until you respawn. If your killer dies, you follow whoever killed them, and so on. If there is nobody left to watch, the camera stays on your body. When you respawn the camera goes back to you.

Built 2026-11-11. It replaced the death screen that was part of the match HUD (`Main.MatchHUD.DeathScreen`, `Packets.Match.Death`), which only worked for player killers and followed them in first person.

> **2026-11-12, Siege.** A dead player has one life, so after 4 s of the normal death camera `Systems.Siege.SpectateService` takes over who the camera follows: living teammates, then living enemies ([SIEGE.md](SIEGE.md#spectating)). It uses this same camera (render priority Camera + 4) and the same `Death.Spectate` packet. Two additions to `DeathCamService`: the `Death.PreventSpectate(viewer)` extension point (Any: true and this service sends that viewer no new target) and `DeathCamService.Release(player)`.

## How it plays

| | |
| --- | --- |
| The card (top) | "ELIMINATED", **Killed by NAME** (a player or an NPC), **with WEAPON**, and the killer's avatar for a player. "You died" with no killer (a fall, your own grenade) |
| Spectating | A third-person camera 10 studs behind and 3 above the one you watch, easing after them and never through a wall. The bottom line says **SPECTATING NAME** |
| Chain | The one you watch dies: you move on to their killer (the camera glides over). Up to 6 steps; a chain that comes back to you, or has no killer, ends it |
| Nobody to watch | No killer, or the chain ran out: no spectating, the camera stays on your body, the SPECTATING line hides |
| Countdown | "Respawning in N" (from `Players.RespawnTime`, which matches set from `RespawnDelay`), or "Out until the next round" in a no-respawn mode (`Eliminated`) |
| Respawn | The screen hides and the camera goes back to your new character |

## Files

| Where | What |
| --- | --- |
| `ServerScriptService.Modules.Systems.Combat.DeathCamService` | Who killed whom, and who each dead player watches |
| `ReplicatedStorage.Modules.Client.Hud.DeathScreen` (ClientOnly) | The screen and the follow camera |
| `StarterGui.Main.DeathScreen` | The UI: `Shade` (darkened edges), `Card` (`Accent`, `Avatar`, `Text.Title`, `Text.Killer`, `Text.Weapon`), `Bottom.Spectating` (`Label`, `Name`), `Bottom.Respawn`. ZIndex 9 to 10: over the HUD, under the menus |
| `Shared.Packets` `Death` group | `Killed` and `Spectate` |
| `Systems.Combat.KillFeed` | Fires the `Combat.Death` extension point on every death |

## How it works

1. `KillFeed.ReportDeath` (every player death, and every NPC death that `NPCService` reports) fires **`Combat.Death(victim, attacker?, item?)`** before it clears the damage log. The attacker is the last one in `Combat.DamageLog` within 10 s, never the victim.
2. `DeathCamService` records `killedBy[victim] = attacker` (weak keys, so dead NPC models can go).
3. For a player victim it sends `Death.Killed` (killer name, killer UserId or 0, weapon, seconds to respawn or -1). Then it resolves who to watch: the killer if alive, else their killer, and so on. It sends `Death.Spectate` (the model or nil, and a name).
4. Every dead player watching the one who just died gets a new `Death.Spectate` from that one's killer. So does anyone watching a player who leaves.
5. A dead player's `CharacterAdded` clears what they watch. On the client, `CharacterAdded` hides the screen, stops the follow camera and puts the camera back on the new humanoid.

The follow camera runs at render priority Camera + 4 (after MovementCamera, Viewmodel and the drone camera) with a Scriptable camera.

```lua
local DeathCamService = require(ServerScriptService.Modules.Systems.Combat.DeathCamService)
DeathCamService.KillerOf(victim)   -- the last recorded killer of a player or NPC model
DeathCamService.Watching(player)   -- who a dead player is spectating, or nil
```

## Tested (2026-11-11, Studio playtest)

With `Players.RespawnTime` raised so the steps fit before the respawn:

1. The Soldier killed the player: "Killed by Soldier", "with Rifle", no avatar (an NPC), "SPECTATING Soldier", "Respawning in 30". The camera followed 10 studs behind the Soldier.
2. The Breacher killed the Soldier: the camera moved to the Breacher, and the card still said "Killed by Soldier".
3. The Breacher died with no killer: SPECTATING hid and the camera went back to the player's body, still counting down.
4. Respawn: the screen hid and the camera was on the new character.

Not yet checked: a player killer (the avatar) with two players, and Elimination's "Out until the next round".
