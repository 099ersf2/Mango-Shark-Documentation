# Matches, modes and teams

> **Since 2026-11-12 the only mode is Siege**, and it does not run the way this page describes. Read [SIEGE.md](SIEGE.md) and [MATCHMAKING.md](MATCHMAKING.md) first.
>
> - Siege is an **External** mode (`External = true` in `Content.Match.Modes.Siege`): `Systems.Siege.SiegeService` runs its phases, teams, spawning and win rules. For an External mode `MatchService` never starts a match, shuffles teams, respawns anyone or ends a round by itself. It keeps kills and deaths, friendly fire, the `Eliminated` attribute and the snapshot the HUD's top bar shows.
> - New calls for the owner of an External mode: `MatchService.BeginExternal(id, endsAt)`, `SetClock(endsAt)`, `Finish(winner?)`, `Reset()`, `Kills(player)`, `Refresh()`.
> - **Archived** in `ServerStorage.Archive.OldMatchModes` (nothing deleted): Team Deathmatch, Free-for-All, Elimination; the admin Match menu and `Packets.Match.Admin`; the `match`, `matchmode`, `matchset` commands; the Match key (M); the old scoreboard (now `Client.Hud.Scoreboard`).
> - Teams gained `Attackers` and `Defenders` (`Content.Match.Teams`).
>
> The rest of this page describes self-run modes: the phases, settings and hooks still work for a mode without `External`, but no such mode is in the place.

The match system runs the game's matches. It's modular:
- **A mode** is one data module.
- **Settings** are adjustable per match, by admins, from a menu or Cmdr.
- **Teams** are our own system, not Roblox `Teams`, so they can be customized freely.

It replaced the fixed Red vs Blue `Systems.Round.RoundService` on 2026-11-11.

## Where things are

| What | Where |
| --- | --- |
| Modes | `ReplicatedStorage.Content.Match.Modes.*`: one ModuleScript per mode (TeamDeathmatch, FreeForAll, Elimination) |
| Settings and their ranges | `Content.Match.Settings` (also `DEFAULT_MODE`) |
| Teams | `Content.Match.Teams` |
| The match loop | `ServerScriptService.Modules.Systems.Match.MatchService` |
| The team system | `Systems.Match.TeamService` |
| HUD, scoreboard | `Client.Hud.MatchHud` → `StarterGui.Main.MatchHUD` |
| Death screen, spectating | `Client.Hud.DeathScreen` → `StarterGui.Main.DeathScreen`, `Systems.Combat.DeathCamService` ([DEATH_SCREEN.md](DEATH_SCREEN.md)) |
| Admin match menu | `Client.Core.MatchMenu` → `StarterGui.Main.MatchMenu`, opened with `MenuButtons.MatchButton` or **M** |
| Templates | `Assets.UI.Templates.MatchTeamScore`, `ScoreboardRow`, `ScoreboardTeam`. The menu reuses `LoadoutCard`, `SliderRow` and `ToggleRow` |
| Packets | `Packets.Match.State`, `Death`, `RequestState`, `Admin` |
| Cmdr | `match start\|end\|restart`, `matchmode <mode>`, `matchset <setting> <value>` |

## How a match runs

| Phase | What happens | Next |
| --- | --- | --- |
| **Waiting** | Fewer than `MinPlayers` in the arena (not `InLobby`) | Intermission when enough join |
| **Intermission** | Counts down `Intermission` seconds. Back to Waiting if players leave (unless an admin started it) | Active |
| **Active** | The match (or a round) runs for `TimeLimit`. Kills score through the mode | Ended (or RoundEnd) |
| **RoundEnd** | Round modes only: 5 s showing the round's result | Active (next round) |
| **Ended** | Shows the winner and the scoreboard for `Intermission` seconds | Intermission or Waiting |

These things happen when a match starts:
1. **Teams:** the mode's teams are set (`TeamCount` of them, from `Content.Match.Teams`), and arena players are shuffled and dealt onto the smallest team each time, so teams are even.
2. **Scores:** scores reset.
3. **Respawn time:** `Players.RespawnTime` becomes the mode's `RespawnDelay`.
4. **Spawning:** everyone respawns at their team's spawns. The same applies to every respawn.

**Joining mid-match:** a player who enters the arena mid-match joins the smallest team.

**Deaths:** `Systems.Combat.KillFeed` reports each player death to `MatchService.OnPlayerDeath(victim, killer)`.
- **Stats:** kills and deaths are counted. A kill on a teammate doesn't count.
- **Hooks:** the mode's `OnKill` and `OnDeath` run.
- **Death screen:** the victim gets it, spectating their killer (and their killer's killer when they die); see [DEATH_SCREEN.md](DEATH_SCREEN.md). It works in and out of matches.

**Time up:** the mode's `OnTimeUp` runs. Without one, the leader wins, and a tie is a draw. In round modes, the team with the most players alive wins the round.

**Friendly fire:** a `Combat.PreventFriendlyFire` handler blocks damage between players on the same team unless the match's `FriendlyFire` setting is on. This covers bullets, bashes, grenades and anything else that goes through `Combat.ApplyHit`.

## Adjusting a match (admins)

Admins are the users in `Classes.Admins.UserIds`. Only they see the **Match [M]** button, and the server checks every request again.

The **Match menu** works like the Settings menu:
- **Now playing:** the running match, its phase and time left, and how many players are in the arena. The buttons are **Start now** (skips waiting and the intermission, even below `MinPlayers`), **End match** (the leader wins) and **Restart with next setup**.
- **Next match: mode:** a card per mode. **Select** makes it the next match's mode, with its default settings.
- **Next match: settings:** a row per setting the chosen mode uses. Numbers are sliders that snap to the setting's step and are sent when you let go. On/off settings are buttons.

Changes apply to the **next** match, or right away with **Restart**. The server cleans every value (`Settings.Clean`): it's clamped to the range and snapped to the step, and a setting the mode doesn't use is refused.

**Cmdr** (F2) does the same:

```
matchmode FreeForAll
matchset TimeLimit 600
matchset FriendlyFire on
match restart
```

## Settings

| Setting | Range | Default | Meaning |
| --- | --- | --- | --- |
| `TimeLimit` | 60–1800 s, step 30 | 300 | Length of a match, or of a round in round modes |
| `ScoreLimit` | 0–250, step 5 (0 = no limit) | 50 | First team or player to reach it wins |
| `RoundsToWin` | 1–10 | 3 | Round modes: rounds needed to win |
| `TeamCount` | 2–4 | 2 | Teams in play: the first N of `Content.Match.Teams` |
| `RespawnDelay` | 0–15 s | 3 | Seconds before a dead player respawns |
| `FriendlyFire` | on/off | off | Teammates can hurt each other |
| `AutoBalance` | on/off | on | Players join the smallest team |
| `MinPlayers` | 1–16 | 2 | Arena players needed to start |
| `Intermission` | 5–60 s, step 5 | 10 | Seconds between matches |

A mode sets its own defaults for the settings it uses (below).

## The modes

| Mode | Teams | Rules | Defaults |
| --- | --- | --- | --- |
| **Team Deathmatch** | 2–4 | Every enemy kill is a point for your team. First to `ScoreLimit`, or most when time runs out, wins | 5:00, 50 points |
| **Free-for-All** | None | Every kill is a point for you. Same win rules | 5:00, 25 points, 2 s respawn |
| **Elimination** | 2–4 | Rounds with no respawns. The last team with players alive wins the round (or the most alive when time runs out). First to `RoundsToWin` | 2:00 rounds, 3 to win |

In Elimination, a dead player waits in the lobby and comes back at the next round (attribute `Eliminated`, then `MatchReturn`).

## Adding a mode

Add a ModuleScript to `Content.Match.Modes`. That's all: `MatchService` loads every module there, and the Match menu shows it.

```lua
--!strict
--[[
	Content.Match.Modes.KingOfTheHill
	...
]]

return {
	Id = "KingOfTheHill",           -- unique; matchmode uses it
	DisplayName = "King of the Hill",
	Order = 4,                      -- menu order
	Description = "Hold the hill to score.",
	Teams = true,                   -- false for free-for-all
	Rounds = false,                 -- true: rounds, a round win counts toward RoundsToWin
	Respawn = true,                 -- false: dead players sit out until the next round
	-- The settings this mode uses (only these show in the menu) and their defaults
	Settings = { TimeLimit = 300, ScoreLimit = 100, TeamCount = 2, RespawnDelay = 3, FriendlyFire = false, AutoBalance = true, MinPlayers = 2, Intermission = 10 },

	-- Hooks (all optional). match is MatchService's match API
	OnStart = function(match) end,                     -- the match started
	OnRoundStart = function(match) end,                -- a round (or the match) started
	OnKill = function(match, killer, victim) end,      -- a player killed a player
	OnDeath = function(match, victim, killer) end,     -- any player death, after OnKill
	OnTimeUp = function(match) end,                    -- the clock ran out (default: the leader wins)
}
```

**The match API** for hooks:

| Call | What it does |
| --- | --- |
| `match.Mode`, `match.Settings` | The mode and its resolved settings |
| `match:TeamOf(player)` | A team Id, or nil |
| `match:AddScore(teamIdOrPlayer, amount)` | Adds points. Reaching `ScoreLimit` (when above 0) wins |
| `match:Score(teamIdOrPlayer)` | Current points |
| `match:Leader()` | The team Id or Player ahead, or nil on a tie |
| `match:TeamsAlive()` / `match:MostAlive()` | Teams with a living player / the team with the most (nil on a tie) |
| `match:Players()` | Players in the match (the arena) |
| `match:End(winner?)` | Ends the match (nil is a draw) |
| `match:EndRound(team?)` | Ends the round (nil is a drawn round) |

**Scoring from other systems:** use `MatchService.AddScore(teamIdOrPlayer, amount)`, for example for an objective. It also wins at `ScoreLimit`.

## Teams

Teams are data in `Content.Match.Teams`: `Id`, `DisplayName`, `Short` (the HUD tag) and `Color`. **Red, Blue, Green and Yellow** are there; add an entry for more.

A player's team is the server-set player attribute **`Team`** (a team Id), nil in free-for-all and between matches. Everything reads it:

| Reader | What it does with it |
| --- | --- |
| HUD | Shows the player's team |
| Teammate outlines | `MatchHud` gives teammates a `Highlight` outline in the team color |
| Friendly fire | Blocks damage between teammates unless `FriendlyFire` is on |
| NPC targeting | `NPCService` uses the attribute as the player's team; no team means the shared `Players` side |
| NPC hearing | `Tactics` uses it to tell whose shots it heard |
| Aim assist | Never targets a teammate |

**NPC models** have their own `Team` attribute (`Hostile`), so `TeamService.AreAllies` works for players and NPCs alike.

**Team spawns:**
1. **Team-marked spawns:** give a SpawnLocation a `Team` attribute (for example `Red`) and it belongs to that team.
2. **Without marked spawns:** the arena's enabled SpawnLocations are split into one block per team along the arena's longest side, in team order. Spawns on the player's `SelectedMap` are used first; `Workspace.Lobby` is never used.
3. **Free-for-all:** the spawn farthest from every other living player is used.

| `TeamService` call | What it does |
| --- | --- |
| `Setup({ ids })` | Sets the teams of a match and clears everyone's team |
| `Active()` | The teams in play |
| `Assign(player, id?)` | Puts a player on a team (nil means the smallest) |
| `Remove(player)` | Takes a player off their team |
| `TeamOf(who)` | A player's, character's or NPC's team |
| `Members(id, arenaOnly?)` | The players on a team |
| `Smallest()` | The team with the fewest players |
| `Balance()` | Evens team sizes out |
| `AreAllies(a, b)` | True if both are on the same team |
| `SpawnFor(player)` | Where the player should spawn |

## HUD and scoreboard

- **Top bar** (scaled; under the menu buttons):
  - **Content:** the mode's name, the clock, and a score chip per team around it (`MatchTeamScore`, in the team color).
  - **Round modes:** chips show rounds won and players alive ("RED · 3").
  - **Free-for-all:** your score and the leader's.
- **Status line:** waiting for players (x/needed), the countdown to the next match, the round number, or the result.
- **Banner:** "RED WIN", "RED WIN THE ROUND", "DRAW", for 4 seconds.
- **Scoreboard:** hold **Tab** (rebindable as "Scoreboard"), or tap the top bar on touch.
  - **Layout:** team headers with totals, then each player's kills, deaths and score (your own row highlighted, dead players dimmed).
  - **When it shows by itself:** while a match has ended.
  - **Roblox player list:** it replaces it, which used Tab too.
- **Death screen:** who killed you and with what; the camera follows them until you respawn, moving on to their killer if they die. In Elimination it says "Out until the next round". See [DEATH_SCREEN.md](DEATH_SCREEN.md).

## Extension points

| Point | Kind | Arguments | When |
| --- | --- | --- | --- |
| `Match.Started` | Fire | modeId | A match started |
| `Match.RoundStarted` | Fire | modeId, round | A round started (round 1 too) |
| `Match.Scored` | Fire | target, amount | A team (Id) or player scored |
| `Match.Ended` | Fire | modeId, winner? | A match ended (team Id, Player, or nil for a draw) |
| `Team.Changed` | Fire | player, oldTeam?, newTeam? | A player's team changed |
| `Combat.PreventFriendlyFire` | Any | attacker, victimCharacter, humanoid | Used by MatchService; add your own to block more |

## Testing

Checked in a Studio playtest on 2026-11-11 (one player, so matches were started by an admin):

- **Waiting:** with 1 of 2 players the match waited.
- **Settings cleaning:** `TimeLimit` 61 became 60, `ScoreLimit` 999 became 250, and `RoundsToWin` was refused for Team Deathmatch.
- **Team Deathmatch:** **Start now** gave Red and Blue, put me on Red, and respawned me at a Red spawn. Score limit 10: +9 kept it running, +1 more ended it with Red winning.
- **Free-for-All:** I had no team; at the score limit of 5 I won.
- **Elimination:** dying as the only player ended round 1 (drawn), and after the 5 s break round 2 started with me back in.
- **HUD and menu:**
  - The HUD showed the mode, clock and team chips.
  - The scoreboard showed team headers and my row.
  - An admin request from the client set the time limit to 10:00.
  - The menu showed 3 mode cards and the chosen mode's setting rows.
  - Requests closer together than 0.15 s are refused ("Too fast").

Not yet tried: real kills between two players, a 3- or 4-team match, a phone, and a gamepad.
