# NPCs and bots

NPCs pick up the same guns as players and fight like them: **every NPC shot goes through `GunService.FireAs`**, so damage, abilities, effects and sounds are the players' own, with no per-gun NPC code.

!!! abstract "Source"

    `Systems.NPC.NPCService`, `Brain`, `Tactics`, `Tasks.*`; `Systems.Games.Siege.SiegeBots`, `BotDrones`. Data: `Content.NPC.Profiles.*` (`Soldier`, `SiegeBot`, `TutorialBot`, …), `Content.Games.SiegeBots`. Guides: [Adding NPCs](../../ADDING_NPCS.md), [Siege bots](../../SIEGE_BOTS.md).

```lua
local NPCService = require(game.ServerScriptService.Modules.Systems.NPC.NPCService)
```

## How an NPC thinks

```text
NPCService (one Heartbeat)
 ├─ decision ticks: THINKS_PER_FRAME NPCs per frame, round-robin, each ~THINK_INTERVAL s
 │    ├─ Tactics reflexes first: dodge grenades, vault windows, fortify, pursue, breach, throw
 │    └─ behavior tree (ServerStorage.NPC.Trees.<tree>): Tasks.FindTarget, AimAndShoot, Chase...
 ├─ every frame for awake NPCs: path following, turning, the gun's firing rhythm
 └─ NPCs farther than WAKE_RANGE from every player sleep: no thinking, moving or shooting
```

- **Spawning:** one NPC per part tagged `NPCSpawn` (its `Profile` attribute, or Soldier) at server start, respawned `RespawnDelay` s after death. The rig is a copy of `ServerStorage.NPC.Templates.<Template>` in `workspace.Enemies`, tagged `NPC`, server-owned.
- **On death:** the tree is aborted, the gun state dropped (`GunService.RemoveShooter`), the body removed after `CORPSE_TIME`.
- **No friendly fire between NPCs** (`Gun.DamageMultiplier` and `Consumable.DamageMultiplier` handlers). Players still hurt everyone.
- **Hearing:** through `Gun.Fired` (shots) and `Drone.Noise` (driving drones).

| Mode | Behavior |
| --- | --- |
| `"Roam"` (default) | Hunts, chases and secures rooms anywhere |
| `"Guard"` | Stays in one room (a part tagged `NPCRoom`), patrols it, watches its doors and windows, rebuilds damaged boards, never chases out. Fighting comes first |

---

## `NPCService`

### `NPCService.Spawn(profileId, where, spawnPart?, ignoreCap?, options?) → Model?`

Spawns one NPC. Returns its model, or `nil` at the `MAX_NPCS` cap or with a bad profile.

| Argument | Meaning |
| --- | --- |
| `profileId` | A profile in `Content.NPC.Profiles` |
| `where` | Its CFrame |
| `spawnPart` | The `NPCSpawn` it respawns at after dying (omit for no respawn) |
| `ignoreCap` | Spawn past `MAX_NPCS` (modes that place their own, like Clear House) |
| `options` | `Team` (instead of the profile's), `Name`, `Gun` (instead of a random one of the profile's), `AlwaysAwake`, `BreakThrough` (paths may go through boards it breaks) |

```lua
-- A one-off enemy in front of a player
local root = player.Character.HumanoidRootPart
local npc = NPCService.Spawn("Soldier", root.CFrame * CFrame.new(0, 0, -15))

-- A game mode's own defender, with a fixed gun, never sleeping
NPCService.Spawn("SiegeBot", spawnCFrame, nil, true, { Team = "Defenders", Gun = "SiegeSMG", AlwaysAwake = true })
```

### `NPCService.SetMode(model, mode, room?) → boolean`

`"Guard"` (room: an `NPCRoom` part; `nil`: the one it stands in) or `"Roam"`. Sets `NPCMode` and `GuardRoom`.

```lua
NPCService.SetMode(npc, "Guard", roomPart) -- roomPart: a part tagged NPCRoom
NPCService.SetMode(npc, "Roam")
```

An `NPCSpawn` with `Mode = "Guard"` (and optional `Room`) spawns a guard with no code.

### `NPCService.AgentOf(model) → Agent?`

The live agent (brain state) of an NPC model.

```lua
local agent = NPCService.AgentOf(npc)
if agent then print(agent.Root.Position, agent.Blackboard) end
```

### `NPCService.Agents() → { Agent }`

Every live agent, read only (tests, debug tools).

```lua
print(#NPCService.Agents(), "agents thinking")
```

### `NPCService.Count() → number` / `NPCService.ProfileNames() → { string }`

```lua
print(NPCService.Count(), "alive;", table.concat(NPCService.ProfileNames(), ", "))
```

### `NPCService.Clear()`

Removes every NPC (also `clearnpcs`).

```lua
NPCService.Clear()
```

---

## Behavior pieces

| Module | What's in it |
| --- | --- |
| `Brain` | Helpers tasks share: `CanSee` (through windows; smoke blocks), `SeeThrough`, `ShootThrough`, `BreachPoint`, `FindEntry`, `FindExit`, `FindFortify`, `Blocked` (soft walls and boards aren't cover), `AimPoint`, `Eye`, `MoveTo`, `MoveDirect`, `Stop`, `IsMoving`, `NewPath`, `AdvancePath`, `SetLastKnown`, `Ammo`, `IsReloading`, `FlatDistance`, `Ground`, … and the shared blackboard `"NPCWorld"` |
| `Tactics` | Reflexes around the tree: `Danger`, `Vault`, `Fortify`, `Pursue`, `Suspicion`, `Breach`, `TryGrenade(agent, now)`, `OnHurt(agent, attacker)` |
| `Tasks.*` | `FindTarget`, `HasLineOfSight`, `InRange`, `LowHealth`, `NeedsReload`, `MoveToCover`, `Reload`, `AimAndShoot`, `Strafe`, `Chase`, `Patrol`: each has `run(agent)`, some `start` / `finish` |

A task is a ModuleScript in `Systems.NPC.Tasks` with `start`, `run` and `finish` (only `run` is required). `run` gets the agent and returns `Brain.SUCCESS`, `Brain.FAIL` or `Brain.RUNNING` (which pauses the tree on this task until a later tick). Most tasks finish in one tick; shooting itself runs every frame in `NPCService`, not in the tree.

```lua title="A task, from Adding NPCs (TakeHigherGround.run)"
local Brain = require(script.Parent.Parent.Brain)

function TakeHigherGround.run(agent: Brain.Agent): number
	local goal = agent.Blackboard.HighGround
	if not goal or Brain.FlatDistance(goal, agent.Root.Position) <= ARRIVED then
		return Brain.SUCCESS
	end
	Brain.MoveTo(agent, goal)
	return Brain.RUNNING
end
```

See [Adding NPCs](../../ADDING_NPCS.md) for trees and profiles.

## Siege bots

Bots fill Siege teams (admins add them to parties; Recruit Training uses one). A bot has a **negative UserId**, counts toward team sizes, and is never waited for or teleported.

| Function | Does |
| --- | --- |
| `SiegeBots.Pick(entry, team, info, teamEntries)` | A bot's Selection picks |
| `SiegeBots.Spawn(entry, cframe)` / `Despawn(entry)` | The bot's body |
| `SiegeBots.Update(context)` | One tick of every bot |
| `SiegeBots.IsBot(userId)` / `IsBotModel(model)` | Is this a bot |
| `SiegeBots.Scout(entry, cframe)` / `SiteFound()` | Bot scouting |
| `SiegeBots.Reset()` / `NewMatch()` | Lifecycle |
| `BotDrones.Deploy(userId, team, cframe)` / `Of(userId)` / `Drive(model, goal?)` / `State(model)` / `Prepare(map)` / `Clear()` | Bot scout drones (through wall vents) |

```lua
local SiegeBots = require(game.ServerScriptService.Modules.Systems.Games.Siege.SiegeBots)
if SiegeBots.IsBotModel(victimModel) then
	-- don't count bot kills toward ranked
end
```

Commands: `spawnnpc <profile> [count]`, `clearnpcs`. More: [NPCs](../../EXAMPLES.md#npcs).
