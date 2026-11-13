# Siege

Siege is the game's only mode since 2026-11-11. Two teams of up to five. The **defenders'** two bombs are already in place at one site; the **attackers** must plant a defuser on both. The defenders only have to keep them away from the bombs until the clock runs out. Nobody plants a bomb: only defusers are planted. One match is one round, and everyone has one life.

Players reach a match through matchmaking ([MATCHMAKING.md](MATCHMAKING.md)): every match is played on its own reserved server. Classes and their abilities are in [CLASSES.md](CLASSES.md). Team Deathmatch, Free-for-All and Elimination are archived (`ServerStorage.Archive.OldMatchModes`).

## The rules that are easy to get wrong

| Rule | What it means |
| --- | --- |
| **Killing every defender does not end the round** | The attackers must still plant both defusers. If the clock runs out first, the defenders win, even with all of them dead |
| **A team only loses by "leaving" when its players leave the server** | Being eliminated is not leaving. "Every defender left the game" and "every attacker left the game" are about players who are no longer on the server |
| **Dead attackers cannot use drones** | When an attacker dies their drone stays in the world and can still be destroyed, but nobody can view or drive it again |
| **A tied site vote is drawn among the tied sites only** | A site with fewer votes is never picked. With no votes at all, every site is tied |
| **One drone per attacker per match** | A destroyed drone is never replaced. Trying it again shows NO SIGNAL |
| **A defender's class is hidden from attackers** | Until a drone scan of that defender. The server never sends it before then |

## Where things are

| What | Where |
| --- | --- |
| Numbers and names | `ReplicatedStorage.Content.Siege` |
| The mode entry (an `External` mode) | `Content.Match.Modes.Siege` |
| The match (phases, picks, spawning, the bombs, defusers, discovery, win rules) | `ServerScriptService.Modules.Systems.Siege.SiegeService` |
| Finding and checking the map | `Systems.Siege.SiegeMap` |
| Spectating after death | `Systems.Siege.SpectateService`, `Client.Core.Spectate` |
| Defender cameras | `Systems.Cameras.CameraService`, `Client.Gadgets.CameraController`, `Content.Cameras` |
| Drones (reworked) | `Systems.Drones.DroneService`, `Client.Gadgets.DroneController` ([DRONES.md](DRONES.md)) |
| Selection screens | `Client.Core.SiegeSelect` → `StarterGui.SiegeSelect` |
| HUD | `Client.Hud.SiegeHud` → `StarterGui.Main.SiegeHUD` |
| Scoreboard | `Client.Hud.Scoreboard` → `StarterGui.Main.SiegeScoreboard` |
| Camera feed | `StarterGui.CameraFeed` |
| Templates | `SiegeOption`, `SiegeClassCard`, `SiegeTeamCard`, `SiegeBoardRow`, `SiegeBoardTeam`, `SiegeKillRow`, `BombMarker` in `Assets.UI.Templates` |
| Packets | `Packets.Siege` (`State`, `Pick`, `Plant`, `Board`, `RequestState`), `Packets.Camera.View`, `Packets.Spectate` (`Next`, `Mode`) |
| Teams | `Attackers` and `Defenders` in `Content.Match.Teams` |

## The map

**The map is whatever is in Workspace.** There is no map loading. `SiegeMap` uses `Workspace.CurrentMap` (then `Workspace.Map`); if neither exists, the first Folder or Model in Workspace (by name) that has a `Sites` or `Bombs` folder. If more than one could be the map, a warning names them and the one used.

The map must hold:

```
<Map>
├─ Bombs
│   └─ <SiteName>
│       ├─ BombA                 a part or model: the bomb (the red A mark goes here)
│       └─ BombB                 (the blue B mark)
├─ Sites
│   └─ <SiteName>
│       ├─ BombA                 a part, or a folder of parts: the room an attacker stands in to plant a defuser on bomb A
│       └─ BombB
├─ DefenseSpawnLocations
│   └─ <SiteName>                a part, or a folder of parts. One is picked at random; every defender spawns there
├─ AttackerSpawnLocations
│   └─ <any name>                parts, at least 5 (one attacker each; attackers pick by name)
└─ Cameras
    └─ <any name>                parts or models; or tag anything in the map "Camera"
```

- A site must be complete in `Bombs`, `Sites` and `DefenseSpawnLocations`, under the same unique name.
- A camera looks along its own front (its pivot's look direction).
- The site volumes are only used for server spatial queries; make them invisible, with `CanCollide` off.

When a match starts the map is checked, and every problem is warned in plain words, for example `Site "MainFloor": missing site volume Workspace.CurrentMap.Sites.MainFloor.BombA`. **A map with any problem cannot host a match**: the round ends at once with "The map is not set up for Siege".

**The map in the place does not pass yet.** The folders and names are now right (four sites: Basement, MainFloor, UpstairsBedroom, UpstairsStage). On the last check (2026-11-12) 13 things were still empty: seven of the eight bomb-room folders in `Sites` have no parts (only `UpstairsBedroom.BombA` has), the four `DefenseSpawnLocations/<site>` folders have no parts, `AttackerSpawnLocations` has 4 parts and needs 5, and there are no cameras. See [NEXT_STEPS.md](NEXT_STEPS.md).

## Phases

All times are in `Content.Siege`.

| Phase | Time | What happens |
| --- | --- | --- |
| **WaitingForPlayers** | up to 45 s | The server reads its match record and waits for everyone in it. It starts as soon as all have arrived, or when the time is up with whoever is there. Players who never arrive are not in the match. Too few players (a side below its minimum) ends it: "Not enough players arrived" |
| **Selection** | 30 s, one timer | Defenders vote a site. Attackers pick a spawn: one each, first come, first served. Everyone picks a class: one per team, first come, first served, and may swap guns the class allows. Picks can be changed until the clock runs out |
| **Reveal** | 10 s | Defenders see the site. Attackers see their spawn and their team's spawns and classes |
| **Prep** | 40 s | Defenders spawn at one random spawn of the site and prepare (boards, class gadgets). Attackers have no body: each gets a drone at their spawn and is held in its view |
| **Action** | 5:00 | Attackers spawn at their spawns. Drones stay where they were left |
| **End** | 12 s | The winner, the reason, everyone's kills. Then everyone goes back to a lobby server, each party together |

**When the Selection clock runs out:**
- An attacker without a spawn gets a random free one.
- A player without a class gets a random free class of their team.
- The site with the most votes wins. A tie is drawn at random among the tied sites only.

**Who is told what:** every snapshot is built for the team of the player it goes to. Votes, spawn picks and class picks are only sent to the team that made them. Attackers are not sent the site until one of their drones finds it.

## Selection: ready, the team list, the consumable (2026-11-12)

> **Not run.** Written on 2026-11-12 with no playtest (by request). The scripts compile and the UI parts the code waits for exist; none of it has been seen working.

- **Ready.** The Class page's READY button sends the pick `Ready` = `"1"`; "Change picks" on the Waiting page sends `"0"`. Being ready does not lock anything: what is still unpicked when Selection ends is filled in at random, as before.
- **The clock is skipped** when every player still in the match, on both teams, is ready (`everyoneReady` in the match tick). Alone in Studio, your own READY ends Selection.
- **The ready list** (`SiegeSelect.Screen.Content.Roster`) stands down the right side all through Selection, in two sections: **YOUR TEAM**, then **ENEMY TEAM · ATTACKERS** (or DEFENDERS) under a red heading, with red names on dark red rows so it can't be read as teammates. Each row is a player's picture, name, and READY (green, outlined) or PICKING; each heading counts its ready players. Templates: `SiegeReadyHeader`, `SiegeReadyRow`. Your team's rows come from the snapshot's `Cards` (which carry `Ready`); the enemy's from `Others` and `OtherTeam`, sent only during Selection and holding only UserId, Name and Ready. **Their picks are never sent.** A Ready pick is sent to both teams.
- **Consumable.** The Class page's loadout panel has a Consumable row (grenade or smoke bomb). It sends the existing `Packets.Consumable.Pick`, which saves the choice; nothing in Siege's own rules changed for it.

Since another developer's change, attackers get a body during Prep, parked at the lobby spawn (`startPrep`), while they drive their drone; they are spawned again at their spawn when Action starts.

## Winning

| Winner | Reason | When |
| --- | --- | --- |
| Attackers | Both defusers planted | The second defuser is planted |
| Attackers | Every defender left the game | No defender is on the server any more |
| Defenders | Every attacker was eliminated | No attacker is alive |
| Defenders | Every attacker left the game | No attacker is on the server any more |
| Defenders | Time ran out | The Action clock reached zero before both defusers were planted |

## The bombs

**Nobody plants a bomb.** The two bombs are the defenders' and are already in place when the round begins.

- When Prep starts, the server stands a copy of the bomb model on `Bombs/<site>/BombA` and `BombB` of the chosen site, in `workspace.SiegeBombs`. Each copy is anchored, turned like the map's bomb part, and sits with its base on that part's base.
- The model is `Content.Siege.BOMB_MODEL` (`"Bomb"`): looked for in `Assets.Models.Siege` first, then as a model of that name in Workspace. Today it is `Workspace.Bomb`.
- The bombs are removed when the match ends. Only the chosen site gets bombs.
- **Defenders have nothing to plant or defuse.** Their job is to keep the attackers out of the two bomb rooms until the clock runs out.

## Defusers

The only thing that is planted is a **defuser**, and only attackers plant it. An attacker plants a defuser on a bomb by staying inside that bomb's room (`Sites/<site>/BombA` or `BombB`) for 8 seconds (`PLANT_TIME`).

- A room is a part, or a folder of parts when one box doesn't fit the room.
- The server checks who is inside every 0.15 s with a spatial query (`GetPartBoundsInBox`); `Touched` is not used. A player is inside when their `HumanoidRootPart` is.
- The progress bar shows only while the attacker is inside.
- **Leaving the room resets the progress to zero. So does dying.** There is no partial progress to come back to.
- Each attacker has their own progress; the first to finish plants the defuser.
- Each bomb takes one defuser. Everyone sees "Defuser planted on Bomb A" (the `Announcement` effect).
- The second defuser ends the round at once.

## Drones in Siege

See [DRONES.md](DRONES.md) for the drone itself.

- Each attacker gets one drone, placed by the server at their spawn when Prep starts. Defenders get none.
- In Prep the attacker is held in the drone's view. In Action they go in and out with the Drone key (5), DPad Left, or the touch DRONE button.
- A destroyed drone is gone for the match: the NO SIGNAL screen shows at once, and again for 2.5 s whenever the attacker tries the drone later.
- **Scan** (Fire in the drone, every 5 s): marks where the defender in the crosshair stands, for all attackers, for 30 s. The mark does not follow the defender; a new scan of the same defender replaces it. The first scan of a defender also reveals their class to the attackers for the rest of the match.
- **Site located**: the first time any attacker's drone is inside any part of `Sites/<site>`, the attackers are told "Site located" and get a red A and a blue B mark on the bombs. Once per match.
- A dead attacker's drone is locked: the server takes its physics back and refuses every view and scan.

## Defender cameras

- Every part or model in the map's `Cameras` folder, and anything tagged `Camera`, is a camera.
- A living defender opens the cameras with the Drone key (5; a defender has no drone), DPad Left, or the touch CAMS button. Fire is the next camera, Aim the previous one, and 5 or X leaves. The view turns up to 55° each way.
- The feed shows the camera's name and LIVE or OFFLINE.
- Attackers can destroy a camera (20 health). A destroyed camera stays in the list and shows NO SIGNAL.
- Cameras are damaged through the normal combat path: each has a hit box with a Humanoid, so guns, bashes and explosions hurt it with no change to the gun system. Defenders can't hurt them.
- The Warden's gadget camera is bulletproof: bullets do nothing, a bash or an explosion still breaks it.

### Destroyed cameras (2026-11-12)

A destroyed camera shows nothing of the world: its NO SIGNAL screen is fully opaque (it was 4% see-through). It keeps the controls on its bottom line and has its own PREV, NEXT and EXIT touch buttons, so a defender can still move to the next camera or leave. Not run.

## Spectating

1. The normal death screen and death camera (your killer).
2. After 4 s (`DEATH_CAM_TIME`), spectating: living teammates. Fire is the next one, Aim the previous.
3. With no teammate alive: living enemies.
4. With nobody to watch, the camera stays on your body.

**Camera priority.** Spectating adds no camera. It uses the death camera (`Client.Hud.DeathScreen`, render priority Camera + 4) and only changes who it follows. The security-camera view runs at Camera + 3, the drone camera's slot; a player is never in both.

| Priority | Camera |
| --- | --- |
| Camera + 1 | MovementCamera |
| Camera + 2 | Viewmodel |
| Camera + 3 | Drone camera, security-camera view |
| Camera + 4 | Death camera, spectating |

## Scoreboard

Hold Tab (the Scoreboard key), or the touch SCORE button. Columns: Player, Status (ALIVE / DEAD), Kills, Class.

- A defender sees every class.
- An attacker sees their own team's classes, and a defender's class only after a drone scan revealed it. Otherwise `?`.
- The server builds each player's rows; a hidden class is never sent.

## API

```lua
local SiegeService = require(ServerScriptService.Modules.Systems.Siege.SiegeService)
SiegeService.Phase()                     -- "Idle", "WaitingForPlayers", "Selection", "Reveal", "Prep", "Action", "End"
SiegeService.IsPlaying(player)
SiegeService.TeamOf(player)              -- "Attackers", "Defenders" or nil
SiegeService.IsAlive(player)
SiegeService.Players(team?, aliveOnly?)
SiegeService.Site()                      -- the chosen site, or nil before the vote ends
SiegeService.Reveal(defender)            -- shows a defender's class to the attackers
SiegeService.ForceEnd(winner?, reason)   -- ends the round now (tests)
```

| Extension point | Kind | Arguments | Use |
| --- | --- | --- | --- |
| `Siege.PhaseChanged` | Fire | phase | A phase started |
| `Siege.PreventPlant` | Any | player, bombName | Stop a player's plant progress |
| `Siege.PlantTimeMultiplier` | Product | player, bombName | Scale the plant time |
| `Siege.Planted` | Fire | player, bombName | A defuser was planted |
| `Siege.SiteLocated` | Fire | player | A drone found the site |
| `Siege.Ended` | Fire | winner?, reasonKey | The round ended |
| `Camera.PreventView` / `Camera.PreventDamage` | Any | player, model / attacker, model | Refuse a view / protect a camera |
| `Camera.Viewed` / `Camera.Destroyed` | Fire | player, model? / model, killer? | |
| `Spectate.Changed` | Fire | viewer, model?, mode | A spectator's target changed |

SiegeService changes other systems only through their extension points: `Loadout.PreventApply`, `Lobby.PreventFirstSpawn`, `Drone.PreventDeploy`, `Drone.PreventRespawn`, `Drone.PreventView`, `Queue.PreventJoin`, `Classes.PreventAbility`, `Classes.AllowBodiless`, `Death.PreventSpectate`.

## Testing in Studio

Studio has no reserved servers, so a match forms on the Studio server itself ([MATCHMAKING.md](MATCHMAKING.md#studio)). One tester can start a match alone:

1. Set the workspace attribute `SiegeTestTeam` to `Attackers` or `Defenders` to choose a side.
2. Open the Play menu (K) and press Find match. The match forms after about 5 s.
3. The map must pass the check above.

## Tested (2026-11-11 and 2026-11-12, Studio, one player)

The map in the place fails the check, so for these tests a temporary script added the missing folders at runtime, in the playtest only. The place's map was not changed.

| Check | Result |
| --- | --- |
| Map check on the real map | 14 problems listed; no match can start |
| Phases in order, as attacker | WaitingForPlayers → Selection → Reveal → Prep → Action → End → Idle |
| Refused picks | An attacker voting a site, an unknown spawn, the other team's class, a gun the class does not allow, wrong types: all ignored |
| Attacker in Prep | No body, one drone 0.9 studs from the spawn, held in its view (the client went in by itself) |
| Attacker in Action | Body at the chosen spawn (0.0 studs off, 3.9 above), class guns in hand |
| Defuser progress reset | Entered room A, left after 1 s, came back: no defuser 1.5 s later, defuser planted after a full 2 s (test value) |
| A defuser on both bombs | Round ended: Attackers, "Both defusers planted" |
| Bombs in place (2026-11-12) | In Reveal: 0 bombs. One second into Prep: 2 at the chosen site, 6 of 6 parts anchored and visible, 0.00 studs off the bomb part's center, base on its base. After the match: 0 |
| Only defender dead | 3 s later the phase was still Action. At time up: Defenders, "Time ran out" |
| Only attacker dead | Round ended: Defenders, "Every attacker was eliminated" |
| Drone destroyed in Prep | `DroneLost` set, no new drone, `Place` and `Deploy` refused, NO SIGNAL shown and kept until Prep ended |
| Camera | View request accepted; own team's hit did 0 damage; an enemy hit destroyed it (`Destroyed` attribute true) |
| Client screens | Selection, Reveal, HUD objective, 2 bomb marks for a defender, ability slot, End panel ("DEFENDERS WIN", "Time ran out") |
| Output | No errors or warnings from this code, server or client |

**Not verified:**
- Anything with two or more players: spawn and class conflicts between teammates, vote ties, team-only visibility as seen by a second client, drone scans and class reveal, spectating teammates then enemies, mid-match leaves.
- The camera views (drone, security camera, spectate) and the free mouse on the selection screens: Studio was not rendering frames during the tests (`RenderStepped` fired 0 times), so nothing driven by a render step could be observed.
- Real clicks, keys, gamepad and touch.
- A live reserved server.

## Limits

- One round per match.
- Late arrivals (after WaitingForPlayers) are not in the match.
- In Studio, `Players.CharacterAutoLoads` is off for the whole server while a match runs.
- A class's guns are visible in the world and in a player's Backpack, which replicates to every client. A modified client could guess a defender's class from their guns. Only the class itself is hidden.
- While an attacker is in the drone view, `Main` is hidden, so the Siege HUD (objective, ability slot) is too.
