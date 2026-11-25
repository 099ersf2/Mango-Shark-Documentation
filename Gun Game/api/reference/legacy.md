# Legacy APIs

These systems are from the game before Siege (Team Deathmatch, Free-for-All, Elimination). Some still run because other code leans on them (`TeamService.TeamOf`, the `Team` attribute), but **don't build new features on the match-mode parts**.

!!! warning "Not current"

    For the active game flow use [Siege match](../systems/siege.md). Background: [Matches, modes, and teams](../../MATCH.md), [Team deathmatch rounds](../../ROUND_SYSTEM.md).

## Still used: `TeamService`

`ClassService.Assign` uses `TeamService.TeamOf(player)` to check a class is on the player's team, so the team helpers are live.

| Function | What it does |
| --- | --- |
| `TeamService.TeamOf(who)` | A player's, character's or NPC's team Id (the `Team` attribute) |
| `TeamService.AreAllies(a, b)` | Same team? |
| `TeamService.Members(id, arenaOnly?)` / `Smallest()` / `Balance()` | Team lookups |
| `TeamService.Setup(ids)` / `Active()` / `Assign(player, id?)` / `Remove(player)` / `SpawnFor(player)` | Old match setup |

## Old match flow: `MatchService`

| Function | What it did |
| --- | --- |
| `MatchService.SetMode(id)` / `SetSetting(name, value)` | The next match's mode and settings |
| `MatchService.StartNow()` / `EndNow()` / `Restart()` | Admin controls |
| `MatchService.AddScore(teamIdOrPlayer, amount)` | Objective points |
| `MatchService.Phase()` / `Mode()` / `Setting(name)` / `ModeIds()` | The running match |
| `MatchService.BeginExternal(id, endsAt?)` / `SetClock` / `Finish(winner?)` / `Reset` / `Kills` / `Refresh` | For a service running an `External` mode (Siege's entry `Content.Match.Modes.Siege` has `External = true`) |

Content: `Content.Match.Modes.*`, `Content.Match.Settings`, `Content.Match.Teams`. Extension points: `Match.Started`, `Match.RoundStarted`, `Match.Scored`, `Match.Ended`, `Team.Changed`. Client: `Client.Hud.MatchHud`, `Client.Core.MatchMenu` (no API).

## Old lobby flow: `LobbyService`

| Function | What it does |
| --- | --- |
| `LobbyService.IsInLobby(player)` | Same as the `InLobby` attribute |
| `LobbyService.SendToArena(player)` / `SendToLobby(player)` | Moves the player and gives/takes guns. Still handy in tests |
| `LobbyService.Readmit(player)` / `Release(player)` | Next spawn in the lobby / out of the lobby without moving |
| `LobbyService.SelectMap(player, mapId)` | Lobby hub map pick |

## Removed

| Thing | Replaced by |
| --- | --- |
| `Packets.Match.Admin`, commands `match` / `matchmode` / `matchset` | Archived in `ServerStorage.Archive.OldMatchModes` |
| `Packets.Drone.Spot` / `Drone.Spotted` (follow-the-enemy highlight) | `Drone.Scan` / `Drone.Marked` (a static mark), 2026-11-11 |
| Keys `Match`, `Loadout`, `GameMode` | `Play` (K), `Party` (L), `ClassAbility` (T) |
| `Combat.Damage` extension point | Never called; use `Gun.DamageMultiplier` / `Consumable.DamageMultiplier` |
| `Tokens` currency | Unused since 2026-11-15 |
