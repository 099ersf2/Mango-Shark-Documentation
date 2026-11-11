# Team deathmatch rounds

## What it is and how it plays

Two balanced teams, Red and Blue, compete in three-minute rounds. The team with the most credited player kills wins; equal totals are a draw. A round waits for two players outside the lobby. A ten-second intermission precedes each round.

The top HUD shows team totals and the ten highest-kill players, ordered by kills. Each entry includes a profile thumbnail. When a player dies during a round, a death screen appears and the camera follows the credited killer until the player respawns.

## Controls

No new controls. Spectating starts automatically on death and ends on respawn.

## Where things are

| What | Where |
| --- | --- |
| Match rules and tuning | `ReplicatedStorage.Content.Round` |
| Server match logic | `ServerScriptService.Modules.Systems.Round.RoundService` |
| HUD and spectating | `ReplicatedStorage.Modules.Client.Hud.RoundHud` (`ClientOnly`) |
| HUD instances | `StarterGui.Main.RoundHUD` |
| Network packets | `ReplicatedStorage.Modules.Shared.Packets.Round` |
| Kill attribution hook | `ServerScriptService.Modules.Systems.Combat.KillFeed` |

## How it works

- The server balances arena players between Red and Blue at round start. Arena players who join mid-round are added to the smaller team.
- For the selected map, enabled spawn pads are sorted by Z. The first half is Red's spawn group; the second half is Blue's. If a group is empty, the available pads are used.
- `Combat.PreventFriendlyFire` blocks damage between teammates only during an active round. Self-damage is unchanged.
- `KillFeed` reports the killer before clearing `DamageLog`. The round service awards only credited enemy-player kills to both the player's round total and their team's total.
- Server snapshots contain the phase, server-time deadline, team scores, winner, and the ten highest-kill players. The client only renders that data.
- The death packet carries the killer's user ID and display name. The client follows that player's Humanoid and restores its own camera on `CharacterAdded`.

## API and extension points

| API | Direction | Purpose |
| --- | --- | --- |
| `RoundService.OnPlayerDeath(victim, killer)` | Server internal | Records a player death while a round is active |
| `Packets.Round.State` | Server to clients | Sends a match snapshot |
| `Packets.Round.Death` | Server to victim | Shows the death screen and spectates a killer |
| `Packets.Round.RequestState` | Client to server | Requests the current snapshot; rate-limited by the server |
| `Combat.PreventFriendlyFire(attacker, victimCharacter, victimHumanoid)` | Server extension | Returns `true` to block teammate damage |

Player attributes set by the server: `RoundTeam` (`"Red"` or `"Blue"`) and `RoundActive` (boolean). The existing `InLobby` attribute remains owned by `LobbyService`.

## How to add more

Change round duration, intermission, minimum player count, leaderboard length, or team colors in `Content.Round`. Do not add a Script or LocalScript. New HUD elements must be created in Studio under `StarterGui.Main.RoundHUD` and accessed with `WaitForChild`.

## Testing

- Luau source compilation passed for the new modules and edited packet/combat/kill-feed modules.
- Solo Studio startup produced no new console errors. The waiting state was verified with one lobby player.
- A temporary one-player test setting was used and restored. It verified team assignment, an active three-minute match HUD, one leaderboard entry, the no-killer death screen, and hiding that screen after respawn.
- Not verified: kill scoring against another player, spectating a different player, or multiplayer balance. Studio's available play control exposed only a solo test.

## Limits

- The leaderboard shows at most ten players.
- Spawn sides assume each map's Z-sorted spawn pads are arranged at opposing ends.
- Round scoring uses the existing kill-feed damage-credit window.
- The Studio experience itself was not published.
