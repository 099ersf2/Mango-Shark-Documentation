# NPCs and bots

NPCs pick up the same guns as players and fight like them: **every NPC shot goes through `GunService.FireAs`**, so damage, abilities, effects and sounds are the players' own, with no per-gun NPC code.

!!! abstract "Source"

    `Systems.NPC.NPCService`, `Brain`, `Tactics`, `Tasks.*`; `Systems.Games.Siege.SiegeBots`, `BotDrones`. Data: `Content.NPC.Profiles.*`, `Content.Games.SiegeBots`. Guides: [Adding NPCs](../../ADDING_NPCS.md), [Siege bots](../../SIEGE_BOTS.md).

## How an NPC thinks

```text
NPCService (one Heartbeat)
 ├─ decision ticks: THINKS_PER_FRAME NPCs per frame, round-robin, each ~THINK_INTERVAL s
 │    ├─ Tactics reflexes first: dodge grenades, vault windows, fortify, pursue, breach, throw
 │    └─ behavior tree (ServerStorage.NPC.Trees.<Profile tree>): Tasks.FindTarget, AimAndShoot, Chase...
 ├─ every frame for awake NPCs: path following, turning, the gun's firing rhythm
 └─ NPCs farther than WAKE_RANGE from every player sleep: no thinking, moving or shooting
```

- **Spawning:** one NPC per part tagged `NPCSpawn` (its `Profile` attribute, or Soldier) when the server starts, respawned `RespawnDelay` s after death. The rig is a copy of `ServerStorage.NPC.Templates.<Template>` in `workspace.Enemies`, tagged `NPC`, server-owned.
- **On death:** the tree is aborted (the running task's `finish` runs), the gun state is dropped (`GunService.RemoveShooter`), the body is removed after `CORPSE_TIME`.
- **No friendly fire between NPCs:** `Gun.DamageMultiplier` and `Consumable.DamageMultiplier` handlers make an NPC's bullets and grenades do nothing to its own team. Players still hurt everyone.

## Modes

| Mode | Behavior |
| --- | --- |
| `"Roam"` (default) | Hunts, chases and secures rooms anywhere |
| `"Guard"` | Stays inside one room (a part tagged `NPCRoom`), patrols it, watches its doors and windows, rebuilds damaged boards, never chases out. Fighting always comes first |

An `NPCSpawn` with `Mode = "Guard"` spawns a guard for the `NPCRoom` it stands in, or the one named by its `Room` attribute. The model's `NPCMode` attribute shows the mode.

## `NPCService` API

| Function | Returns / does |
| --- | --- |
| `NPCService.Spawn(profileId, where, spawnPart?, ignoreCap?, options?)` | The NPC's model, or `nil` at the `MAX_NPCS` cap or with a bad profile. `spawnPart`: where it respawns. `ignoreCap`: for modes that place their own NPCs (Clear House). `options`: `Team` (instead of the profile's), `Name`, `Gun` (instead of a random one of the profile's), `AlwaysAwake`, `BreakThrough` (paths may go through boards it breaks) |
| `NPCService.SetMode(model, mode, room?)` | `"Guard"` (room: an `NPCRoom` part; `nil`: the one it stands in) or `"Roam"`; `true` if set |
| `NPCService.AgentOf(model)` | The live agent of an NPC model, or `nil` |
| `NPCService.Agents()` | The live agents, read only (tests, debug) |
| `NPCService.Count()` / `ProfileNames()` | How many are alive / profile names |
| `NPCService.Clear()` | Removes every NPC |

## Behavior pieces

| Module | What's in it |
| --- | --- |
| `Brain` | Helpers tasks share: `CanSee` (through windows), `SeeThrough`, `ShootThrough`, `BreachPoint`, `FindEntry`, `FindExit`, `FindFortify`, `Blocked` (soft walls and boards aren't cover), `AimPoint`, `MoveTo`, `MoveDirect`, `Stop`, `NewPath`, `AdvancePath`, `SetLastKnown`, … and the shared blackboard `"NPCWorld"` |
| `Tactics` | Reflexes around the tree: `Danger`, `Vault`, `Fortify`, `Pursue`, `Suspicion`, `Breach`, `TryGrenade(agent, now)`, `OnHurt(agent, attacker)` |
| `Tasks.*` | `FindTarget`, `HasLineOfSight`, `InRange`, `LowHealth`, `NeedsReload`, `MoveToCover`, `Reload`, `AimAndShoot`, `Strafe`, `Chase`, `Patrol`: each has `run(agent)`, some `start` / `finish` |

NPCs **hear** through extension points: `Gun.Fired` (shots) and `Drone.Noise` (driving drones).

## Siege bots

Bots fill Siege teams (admins add them to parties; Recruit Training uses one). A bot has a **negative UserId**, counts toward team sizes, and is never waited for or teleported.

| Function | What it does |
| --- | --- |
| `SiegeBots.Pick(entry, team, info, teamEntries)` / `Spawn(entry, cframe)` / `Despawn(entry)` / `Update(context)` | Selection picks and the bot's body |
| `SiegeBots.IsBot(userId)` / `IsBotModel(model)` | Is this a bot |
| `SiegeBots.Scout(entry, cframe)` / `SiteFound()` / `Reset()` / `NewMatch()` | Scouting and lifecycle |
| `BotDrones.Deploy(userId, team, cframe)` / `Of(userId)` / `Drive(model, goal?)` / `State(model)` / `Prepare(map)` / `Clear()` | Bot scout drones (through wall vents) |

## Example

```lua
local NPCService = require(game.ServerScriptService.Modules.Systems.NPC.NPCService)

-- A guard for a room, ignoring the NPC cap
local npc = NPCService.Spawn("Soldier", spawnPart.CFrame, spawnPart, true)
if npc then
	NPCService.SetMode(npc, "Guard", roomPart) -- roomPart: a part tagged NPCRoom
end

print(NPCService.Count(), table.concat(NPCService.ProfileNames(), ", "))
NPCService.Clear()
```

Commands: `spawnnpc <profile> [count]`, `clearnpcs`. More: [NPCs](../../EXAMPLES.md#npcs).
