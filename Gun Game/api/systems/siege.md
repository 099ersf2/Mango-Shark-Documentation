# Siege match

Siege is the game's active mode: attackers try to plant defusers on both bombs of a site, defenders keep them out. One reserved server runs exactly one match, then sends everyone back to the lobby.

!!! abstract "Source"

    `Systems.Matchmaking.ServerRole`, `Systems.Games.Siege.SiegeService`, `SiegeMap`, `SpectateService`, `TutorialService`, `Systems.Games.ClearHouse.ClearHouse`, `Systems.Matchmaking.MatchHost`. Numbers: `Content.Games.Siege`. Design guide: [Siege](../../SIEGE.md).

## Which server am I on? `ServerRole`

The place has one place and two kinds of server. Check the role before doing lobby-only or match-only work.

```lua title="Systems.Matchmaking.ServerRole"
local kind: Kind = if RunService:IsStudio()
	then "Studio"
	elseif game.PrivateServerId ~= "" and game.PrivateServerOwnerId == 0 then "Match"
	else "Lobby"
```

```lua
local ServerRole = require(game.ServerScriptService.Modules.Systems.Matchmaking.ServerRole)
if ServerRole.IsLobby() then
	-- parties, queue, shop
end
if ServerRole.IsMatch() then
	-- Siege hooks
end
print(ServerRole.Kind(), ServerRole.JobId())
```

| Function | Lobby | Match | Studio |
| --- | :-: | :-: | :-: |
| `ServerRole.Kind()` | `"Lobby"` | `"Match"` | `"Studio"` |
| `ServerRole.IsLobby()`: parties, queue, matchmaker | ✔ | | ✔ |
| `ServerRole.IsMatch()`: may host a Siege match | | ✔ | ✔ |
| `ServerRole.IsLocal()`: MemoryStore/teleports replaced by local stand-ins | | | when `Content.Matchmaking.STUDIO_LOCAL` |
| `ServerRole.JobId()` | `game.JobId` | `game.JobId` | a made-up `Studio-<guid>` |

Studio is **both** a lobby and a match server, so a match forms on the same server you queue from.

## The match lifecycle

```text
Idle ─▶ WaitingForPlayers ─▶ Selection ─▶ Reveal ─▶ Prep ─▶ Action ─▶ RoundEnd ─┐
                                 ▲                                               │ next round
                                 └───────────────────────────────────────────────┘
                                                              (last round) ─▶ End ─▶ lobby
```

| Phase | What happens |
| --- | --- |
| `Idle` | Nothing running. Every lobby server is always Idle |
| `WaitingForPlayers` | The match record arrived; waits for every expected player or `WAITING_TIMEOUT`. No-shows are simply not in the match |
| `Selection` | One timer. Defenders vote a site; attackers pick a spawn; everyone picks a class (one per team, first come first served) and guns. When everyone is **Ready**, the rest of the clock is skipped. Unpicked → random |
| `Reveal` | Defenders see the site; attackers see their spawns and classes |
| `Prep` | Defenders spawn and prepare. Attackers have **no body**: each gets a drone and is held in its view |
| `Action` | Attackers spawn. Drones stay where they were left |
| `RoundEnd` | The round result for `ROUND_END_TIME`, then the map is rebuilt and the next Selection starts (sides swap) |
| `End` | The match result, then `MatchHost.ReturnAll()` |

### Win rules

| Attackers win | Defenders win |
| --- | --- |
| Both bombs have a defuser (`BombsPlanted`) | Every attacker is dead (`AttackersDead`) |
| Every defender **left the server** (`DefendersLeft`) | Every attacker left (`AttackersLeft`) |
| | The Action clock ran out before both defusers (`TimeUp`) |

!!! warning "Killing every defender does not win the round"

    Attackers must still plant. If the clock runs out, defenders win even with all of them dead. "Left" means left the server, never "was eliminated".

**Planting:** an attacker who stays inside `Sites/<site>/BombA` (or `BombB`) for `PLANT_TIME` seconds plants that bomb's defuser. The server checks with `GetPartBoundsInBox` every `PLANT_CHECK` seconds (never `Touched`). Leaving the room or dying resets progress.

**Site discovery:** the first time an attacker's drone is inside any part of `Sites/<site>`, attackers are told "Site located" and get the site and bomb positions in their snapshot.

**Rounds:** a match is `Content.Games.Siege.ROUNDS[mode]` rounds (1v1: 3, 5v5: 5). Players keep a side group for the match ("A" started attacking); groups swap sides every round; the group with a majority of round wins takes the match.

### What each team is told

The server builds a separate snapshot (`Packets.Siege.State`, `Packets.Siege.Board`) **per team**. The other team's votes, spawns and classes are never in it. During Selection a team only learns who is on the other team and whether they're Ready. A defender's class reaches attackers only after a drone or camera scan of that defender (`SiegeService.Reveal`).

## `SiegeService` API

```lua title="Systems.Games.Siege.SiegeService (public API)"
-- The players in the match.
-- @param team Only this side (nil: both)
-- @param aliveOnly True to leave out the dead
function SiegeService.Players(team: string?, aliveOnly: boolean?): { Player }
	local list = {}
	for _, entry in humans(present(team)) do
		if not aliveOnly or entry.Alive then
			table.insert(list, entry.Player)
		end
	end
	return list
end
```

```lua
local Siege = game.ServerScriptService.Modules.Systems.Games.Siege
local SiegeService = require(Siege.SiegeService)
```

### `SiegeService.Phase() → string`

`Idle`, `WaitingForPlayers`, `Selection`, `Reveal`, `Prep`, `Action`, `RoundEnd` or `End`.

```lua
if SiegeService.Phase() ~= "Action" then
	return false, "Only during Action."
end
```

### `SiegeService.IsPlaying(player) → boolean`

In the running match.

```lua
if not SiegeService.IsPlaying(player) then return end
```

### `SiegeService.TeamOf(player) → string?`

`"Attackers"`, `"Defenders"` or `nil`. (In most code you can also read the `Team` attribute.)

```lua
local side = SiegeService.TeamOf(player)
```

### `SiegeService.IsAlive(player) → boolean`

In the match and not dead this round.

```lua
local alive = SiegeService.IsAlive(player)
```

### `SiegeService.Players(team?, aliveOnly?) → { Player }`

Human players in the match (bots are left out). `team` nil: both sides.

```lua
local livingDefenders = SiegeService.Players("Defenders", true)
print(#livingDefenders, "defenders left")
```

### `SiegeService.Site() → string?`

The chosen site's name, `nil` before the vote ends.

```lua
print("Defending", SiegeService.Site() or "(not chosen yet)")
```

### `SiegeService.Round() → number`

The round being played (1..), `0` before the first.

```lua
if SiegeService.Round() == 1 then showTutorialHints() end
```

### `SiegeService.IsTutorial() → boolean`

`true` while the running match is Recruit Training.

```lua
if SiegeService.IsTutorial() then return end -- no stats from training
```

### `SiegeService.Reveal(defender)`

Shows that defender's class to the attackers from now on (what a drone scan does). Only then is it ever sent to them.

```lua
-- (Siege already does this for drone and camera scans; shown as the pattern)
Extensions.Add("Drone.Spotted", function(player, target, position)
	local victim = Players:GetPlayerFromCharacter(target)
	if victim then SiegeService.Reveal(victim) end
end)
```

### `SiegeService.ForceEnd(winner?, reasonKey)`

Ends the round now, for admins and tests. `winner` is `"Attackers"`, `"Defenders"` or `nil`; `reasonKey` a `Content.Games.Siege.REASONS` key or any text.

```lua
SiegeService.ForceEnd("Attackers", "BombsPlanted")
```

### `SiegeMap.Find()` / `SiegeMap.Check(map)` / `SiegeMap.Load()`

The Workspace map / its problems / its info, or `nil` after warning **every** problem (missing sites, bombs, spawns…). Run `Load()` after building a map.

```lua
local SiegeMap = require(Siege.SiegeMap)
local info = SiegeMap.Load()
if info then print("Map OK") end
```

## Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Siege.PhaseChanged` | Fire | phase |
| `Siege.PreventPlant` | Any | player, bombName |
| `Siege.PlantTimeMultiplier` | Product | player, bombName |
| `Siege.Planted` | Fire | player, bombName |
| `Siege.SiteLocated` | Fire | player? (`nil` when shown at Action, or found by a bot) |
| `Siege.SelectionEnded` | Fire | `{ Round, Mode, Map, Site, Picks }` (`Picks`: Player, Team, Class, Spawn, Random) |
| `Siege.RoundEnded` | Fire | winner?, reasonKey, round, `{ Mode, Map, Site, Final }` |
| `Siege.Ended` | Fire | winner?, reasonKey, `{ Mode, Map, Rounds, ScoreA, ScoreB, Draw, Players }` |

`Siege.Ended`'s `Players` lines carry each player's result (`Player`, `Won`, `Left`, `Damage`, …). `QuestService` reads them:

```lua title="Systems.BattlePass.QuestService"
local function onSiegeEnded(_team: any, _reason: any, info: any)
	local record = publicMatch()
	if not record or type(info) ~= "table" then
		return
	end
	for _, line in info.Players or {} do
		local player = asPlayer(line.Player)
		if not player or player.Parent ~= Players or line.Left then
			continue
		end
		QuestService.Add(player, "MatchesPlayed")
		if line.Won then
			QuestService.Add(player, "MatchesWon")
		end
		if (line.Damage or 0) > 0 then
			QuestService.Add(player, "Damage", line.Damage)
		end
	end
end
```

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Siege.State` | Server → one client | The match as their team may see it (phase, clock, picks, site once known, bombs, marks, result). During Selection also `Others`/`OtherTeam`. `Map`: the map name in `ReplicatedStorage.Maps` |
| `Siege.Pick` | Client → server | kind (`Site`, `Spawn`, `Class`, `Gun`, `Ready`, `Map`), value (`Gun`: `"slot:gunId"`; `Ready`: `"1"`/`"0"`) |
| `Siege.Plant` | Server → one attacker | bomb (`""` for none), server time started, seconds |
| `Siege.Board` | Server → one client | Scoreboard rows `{ UserId, Name, Team, Alive, Kills, Class }`; an enemy's Class is `"?"` until revealed |
| `Siege.RequestState` | Client → server | — (once, when the HUD starts; rate limited) |

## Spectating, the host, other match kinds

### `SpectateService.Begin(player, delay, choices)`

Starts spectating after the death camera, after `delay` seconds. `choices(player)` returns `({ Choice }, mode)`: who they may watch and `"Team"` or `"Enemy"`.

```lua
local SpectateService = require(Siege.SpectateService)
SpectateService.Begin(player, 3, function(viewer)
	return teammatesAlive(viewer), "Team"
end)
```

### `SpectateService.Stop(player)` / `StopAll()` / `Watching(player)`

Stop one / everyone; who they watch now.

```lua
SpectateService.StopAll() -- round over
```

### `MatchHost.Record() → MatchRecord?`

The match server's record `{ Id, Mode, Teams, Map, Private?, Expected, Parties, … }`. **Teams come from here, never from the client.**

```lua
local MatchHost = require(game.ServerScriptService.Modules.Systems.Matchmaking.MatchHost)
local record = MatchHost.Record()
if record and record.Private then return end -- private matches count for nothing
```

### `MatchHost.TeamOf(userId) → string?`

```lua
print(MatchHost.TeamOf(player.UserId)) -- "Attackers"
```

### `MatchHost.ReturnAll()` / `MatchHost.Clear()`

Send everyone back to the lobby (end of match) / forget the record.

```lua
MatchHost.ReturnAll()
```

### `TutorialService.Progress(player) → Progress?`

The recruit's training progress `{ Round, Phase, Done, Missed, Counts }` (tests). Fires `Tutorial.Finished(player, rewarded)` at the end.

```lua
local TutorialService = require(Siege.TutorialService)
print(TutorialService.Progress(player))
```

### Clear House

`Systems.Games.ClearHouse.ClearHouse`: attackers vs NPC guards, one round, no bombs. See [Clear House](../../CLEAR_HOUSE.md).

| Function | Does |
| --- | --- |
| `ClearHouse.Prepare(map)` | Boards every door and window, finds the rooms |
| `ClearHouse.Populate(players)` | Places the guards (counts from `Content.Games.ClearHouse`) |
| `ClearHouse.Left()` / `Total()` | Guards alive / placed |
| `ClearHouse.GuardOf(model)` / `Rows()` / `Rooms()` | Guard records / room list |
| `ClearHouse.Clear()` | Removes it all |

```lua
local ClearHouse = require(game.ServerScriptService.Modules.Systems.Games.ClearHouse.ClearHouse)
print(ClearHouse.Left(), "/", ClearHouse.Total(), "guards left")
```

**Recruit Training** (mode Kind `Tutorial`): one player vs one easy bot, two rounds (attack, then defend). Selection is auto-filled and ends at once; the snapshot carries `Tutorial = true`. See [Recruit Training](../../TUTORIAL.md).

## Common tasks

```lua
local Systems = game.ServerScriptService.Modules.Systems
local SiegeService = require(Systems.Games.Siege.SiegeService)
local ServerRole = require(Systems.Matchmaking.ServerRole)
local ClassService = require(Systems.Classes.ClassService)
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

-- Only on servers that can host a match
if ServerRole.IsMatch() then
	-- Halve plant time for one class (always return 1 otherwise)
	Extensions.Add("Siege.PlantTimeMultiplier", function(player, bombName)
		local class = ClassService.ClassOf(player)
		return if class and class.Id == "Breacher" then 0.5 else 1
	end)

	-- Do something at the start of Action
	Extensions.Add("Siege.PhaseChanged", function(phase)
		if phase == "Action" then
			print("Defenders alive:", #SiegeService.Players("Defenders", true))
		end
	end)
end
```

!!! tip "Test a match alone in Studio"

    Set the workspace attribute `SiegeTestTeam` to `Attackers` or `Defenders`, then press PLAY (K). Everyone queued goes on that side.

More: [Siege examples](../../EXAMPLES.md#siege).
