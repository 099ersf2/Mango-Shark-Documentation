# Clear House (Arcade)

Added 2026-11-14. Up to five players against NPC guards in a house (Mansion or Bank, voted). Every door and window is boarded up. The players breach in and clear every room. No bombs, no defenders' cameras, one round.

## Where things are

| What | Where |
| --- | --- |
| Category and mode | `Content.Matchmaking`: category `Arcade`, mode `ClearHouse` (`Kind = "ClearHouse"`, `Maps = { "Mansion", "Bank" }`, `TeamSize = { Attackers = 5, Defenders = 0 }`) |
| Numbers | `Content.Games.ClearHouse` (phase times, guard counts, profiles, room finder settings, texts) |
| End reasons | `Content.Games.Siege.REASONS`: `HouseCleared`, `HouseHeld` |
| The match | `Systems.Games.Siege.SiegeService`: the Siege flow with a `clearHouse` flag |
| Doors, windows, rooms, guards | `Systems.Games.ClearHouse.ClearHouse` |
| Guard behavior | `Systems.NPC.NPCService` Guard mode (existing): stays in its `NPCRoom` box, patrols it and rebuilds its boards |
| Client | `Client.Core.SiegeSelect` (HOUSE GUARDS in the roster), `Client.Hud.SiegeHud` (objective with guards left, no bomb chips, only the players' result column) |

## How a match goes

1. **Queue.** A party of 1 to 5 queues for CLEAR HOUSE (ARCADE card in the Game Modes panel).
    - A full squad of 5 starts at once.
    - Otherwise, whoever is queued starts after `MaxWait` (20 s).
    - Parties are never split. `Matchmaking.PartyLimit(mode)` allows 5 here, since the other side is empty.
2. **Selection** (its own `SELECTION_TIME`, 30 s, in `Content.Games.ClearHouse`; Siege's is 40 s since 2026-11-25):
    - **Map vote** (the first page): every map of the mode's `Maps` that exists in `ReplicatedStorage.Maps`, with its votes (the `"Map"` pick). No map is loaded yet.
    - **Class:** the attackers' classes only. The roster's enemy section reads HOUSE GUARDS.
3. **Map load** (when Selection ends, `loadHouse` in SiegeService):
    - The map with the most votes wins; a tie is drawn among the tied maps (no votes: all are tied). `record.Map` and `ActiveSiegeMap` are set to it.
    - Each player gets a random free attacker spawn of that map.
    - In its own thread, `ClearHouse.Prepare` puts every breakable back to whole (`BreakableService.Reset`, including Siege's empty `DoorBoardBuild` door frames) and finds the rooms (below); then `Populate` places the guards.
4. **Reveal** (15 s): the spawn and the team. The guards are placed meanwhile.
5. **No Prep.** Reveal goes straight to Action.
6. **Action** (`ACTION_TIME`, 480 s): players spawn at their spawns, with their drones.
7. **End.** The result screen shows VICTORY or DEFEAT, "x / y guards down", and your team. The guards' stats are not shown (2026-11-15). Then everyone returns to the lobby.

## Winning and losing

| Result | When | Reason key |
| --- | --- | --- |
| Players win | Every guard is dead | `HouseCleared` |
| Players lose | Every player is dead | `AttackersDead` |
| Players lose | Every player left | `AttackersLeft` |
| Players lose | The Action clock ran out | `HouseHeld` |

The clock is a safety net, so a guard stuck somewhere can't keep a server running forever. Raise or lower `ACTION_TIME` as you like.

## Wins in their own category and mode

`StatsService` saves every result under `Stats["Mode:ClearHouse"]` and `Stats["Category:Arcade"]` (wins, losses, streak, best streak), apart from Siege's `Mode:5v5`, `Mode:1v1` and `Category:Siege`. The overall `Wins` / `Losses` totals (and the lobby leaderboard's `TotalWins`) still count every mode, Clear House included. Coins are the usual `REWARDS.Win` / `Loss`.

## Finding the rooms

There are no hand-placed room parts. `ClearHouse.Prepare` finds them, with every board already up so doors and windows act as walls:

1. **Grid.** A grid of points `CELL` (4) studs apart covers the map's parts. Parts wider than `MAX_PART_SPAN` (ground, water) are left out of the bounds.
2. **Floors.** Under each point, rays straight down find every floor, one storey after another (up to `FLOORS_PER_COLUMN`).
3. **Standing points.** A floor point counts if nothing is within `HEAD` (5.5) studs above it, and it has a ceiling within `CEILING` (40) studs. That leaves out roofs, lawns and the street.
4. **Joining neighbors.** Two neighbor points are joined when:
    - their floors are within `STEP` (0.75) studs of each other, and
    - a ray between them at waist height (`WAIST`, 3) hits nothing.

    Walls and boards stop that ray. Stair steps are too far apart in height, so they're never joined.
5. **Rooms.** Each joined group (union-find) of `MIN_ROOM_CELLS` to `MAX_ROOM_CELLS` points is a room. It becomes an invisible box tagged `NPCRoom` in the map's `ClearHouseRooms` folder, covering its points from floor to ceiling.
6. **Guard spots.** Points joined on all four sides are the room's spots, where guards stand away from the walls.

Rays only hit the map's collidable parts (`RespectCanCollide`), so room volumes, spawn markers and board roots don't count as walls. The finder waits a frame every `RAYS_PER_YIELD` raycasts. On the Mansion it finds 26 rooms in about 0.2 s; on Bank, 29 rooms in about 2.3 s (during Reveal).

**Hand-drawn rooms instead:** put parts in a `Rooms` folder in the map. They're used as they are, with no grid.

## Placing the guards

- **Maps with `ClearHouseSpawnRooms` (Mansion and Bank, since 2026-11-15, by another developer):** guards come in floor waves: Main 6, Upstairs 4, Basement 6 (16 in all). The next floor's wave is placed when every guard of the last one is down; guards still to come count as left. Each room of the floor gets one (the basement's biggest rooms take the extra).
- **Other maps, how many:** 2/3 of every room found, rounded up (`ROOM_SHARE`, 2026-11-15), plus `GUARDS_PER_PLAYER` (2) for each player after the first; one per room first, so at least 2/3 of the rooms hold a guard.
- **Indoors only:** a guard stands only on an indoor spot: nothing over its head, a ceiling above, and walls at waist and head height in at least 6 of 8 directions. A map with an `NPCIndoorVolumes` folder also keeps its guards inside those parts. (Bomb rooms no longer count as the only indoor rooms.)
- **Which rooms:** storey by storey, starting with the floor the attackers enter on (`MainFloorY` on the map, or the attacker spawns' floor). Rooms are drawn at random, bigger ones more often, one guard per room first; then up to `MAX_PER_ROOM` (3) each, biggest first. Any guards still left go to free indoor spots anywhere. A warning is printed if the spots run out.
- **Patrol:** the guard is kept inside its indoor volume (or its found room on a map without volumes). It walks to a spot at least 45% of the room's size away when it can (`GUARD_SPREAD` in `Tasks.Patrol`), stands 0.6 to 1.8 s watching a door or window, and walks again. Guards farther than 350 studs from every player sleep (`NPCService` `WAKE_RANGE`).
- **Profiles:** drawn from `PROFILES` by weight: Soldier 3, Breacher 1. (No Grenadier since 2026-11-15.)
- **Spawning:** `NPCService.Spawn(profile, cframe, nil, true)`. The fourth argument passes the `MAX_NPCS` cap, which is 0 today. The guard is then put in Guard mode for its room.
- **No respawns:** guards never come back. The model carries the `ClearHouseGuard` attribute.

## Tested (2026-11-14, Studio, one player)

- **Room finder.** It ran on a copy of the Mansion in edit mode and found 26 rooms in 0.2 s. Every Siege bomb room (`Sites`) falls 90 to 100% inside one found room.
- **Win:**
    - Queued CLEAR HOUSE alone; the match formed after the short Studio wait.
    - Selection showed 5 spawns and the attacker classes.
    - All 32 doors and windows were fully boarded.
    - 6 guards were placed in Guard mode, each inside its own room box.
    - In Action the objective read "CLEAR THE HOUSE · 6 guards left", with no bomb chips.
    - The guards were killed from a test script, one after another, and the count went down to "1 guard left".
    - The last kill ended the match: VICTORY, "6 / 6 guards down · Every guard is down", YOUR TEAM "House cleared", and HOUSE GUARDS with 6 rows.
    - The win was saved under `Mode:ClearHouse` and `Category:Arcade`.
- **Loss.** A second match: the player died in Action, giving DEFEAT, "0 / 6 guards down · Every attacker was eliminated".
- **Test data undone.** Both test results were removed from the saved data: coins, wins, losses and both stats entries. `LastMode` was set to `5v5`, since the value before the test wasn't recorded.

### Tested again (2026-11-14, map vote and no prep)

- The Selection's first page read "Vote for the map" with MANSION and BANK. A vote for Bank showed "1 vote" and the outline.
- The attacker classes were offered; the match loaded Bank, gave a spawn, and went from Reveal straight to Action (no Prep).
- 29 rooms were found on Bank in 2.3 s and 15 guards placed.
- A guard shot the idle test player: DEFEAT, "0 / 15 guards down · Every attacker was eliminated", and the HOUSE GUARDS column showed that guard's kill and 102 damage.
- The loss was removed from the saved data (coins, losses, both stats entries; `LastMode` back to `5v5`).

### Tested again (2026-11-15, guard count)

- `Prepare` and `Populate` on both maps in a playtest: Mansion 13 guards (1 player) and 21 (5 players); Bank 15 and 23. Every guard had an indoor room.

### Not tested

- Real fighting on the players' side: kill credit to players, and guards rebuilding boards.
- A full squad of 5 on live servers.
- How hard it is.
