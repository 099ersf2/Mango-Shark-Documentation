# Extension points

Extension points are how one system lets others change its behavior **without either one naming the other**. Siege doesn't know quests exist; quests just listen for `Siege.Ended`. A class ability doesn't patch the gun code; it answers `Gun.DamageMultiplier`.

!!! abstract "Source"

    `ReplicatedStorage.Modules.Shared.Extensions` (both sides). The full list of points is in [All extension points](../reference/extension-points.md).

## The idea in one picture

```text
  Core system asks a question                      Any module can answer
  ───────────────────────────                      ─────────────────────
  Extensions.Any("Siege.PreventPlant", p, bomb) ◀── Extensions.Add("Siege.PreventPlant", fn)
  Extensions.Product("Siege.PlantTimeMultiplier")◀── Extensions.Add("Siege.PlantTimeMultiplier", fn)
  Extensions.Fire("Siege.Planted", p, bomb)    ───▶ quests, analytics, tutorial listen
```

## The three kinds

| Kind | Core calls | Handler returns | With no handlers |
| --- | --- | --- | --- |
| **Any** (a veto) | `Extensions.Any(point, ...)` | `true` to stop it | `false`: nothing is stopped |
| **Product** (a multiplier) | `Extensions.Product(point, ...)` | a number; every handler's number is multiplied | `1`: no change |
| **Fire** (a notification) | `Extensions.Fire(point, ...)` | nothing | nothing happens |

So the core always works as if the extra content wasn't there. That is the whole module:

```lua title="Shared.Extensions"
function Extensions.Add(point: string, handler: (...any) -> ...any): () -> ()
	local list = points[point]
	if not list then
		list = {}
		points[point] = list
	end
	table.insert(list, handler)
	return function()                         -- call this to remove the handler
		local index = table.find(list, handler)
		if index then
			table.remove(list, index)
		end
	end
end

-- True if any handler returns true
function Extensions.Any(point: string, ...: any): boolean
	for _, handler in table.clone(points[point] or {}) do
		if call(point, handler, ...) == true then
			return true
		end
	end
	return false
end

-- The product of every handler's number, starting at 1. Handlers that return nothing count as 1
function Extensions.Product(point: string, ...: any): number
	local value = 1
	for _, handler in table.clone(points[point] or {}) do
		local result = call(point, handler, ...)
		if type(result) == "number" then
			value *= result
		end
	end
	return value
end
```

`call` wraps each handler in `pcall`: an erroring handler is warned (`Extensions: a <point> handler errored`) and skipped, never breaking the core.

## How the core asks: a real example

`SiegeService` checks two points every time it advances an attacker's plant progress:

```lua title="Systems.Games.Siege.SiegeService (plant check)"
if bombName and not entry.Bot and Extensions.Any("Siege.PreventPlant", player, bombName) then
	-- this player makes no progress
end
local duration = Siege.PLANT_TIME
	* (if entry.Bot then 1 else Extensions.Product("Siege.PlantTimeMultiplier", player, bombName))
-- ...when the defuser goes down:
Extensions.Fire("Siege.Planted", entry.Player, bombName)
```

## How content answers: real examples

`QuestService` counts quest progress by listening to points from five different systems, none of which knows about quests:

```lua title="Systems.BattlePass.QuestService:Start"
Extensions.Add("Combat.Death", onDeath)
Extensions.Add("Siege.Ended", onSiegeEnded)
Extensions.Add("Siege.Planted", inMatch("BombsPlanted"))
Extensions.Add("Drone.Spotted", inMatch("DroneScans"))
Extensions.Add("Breakable.Repaired", inMatch("BoardsBuilt"))
Extensions.Add("Classes.AbilityUsed", inMatch("AbilitiesUsed"))
```

`TutorialService` does the same to tick off Recruit Training goals, and guards each handler so it only acts during training:

```lua title="Systems.Games.Siege.TutorialService:Start"
if not ServerRole.IsMatch() then
	return -- Goals and the reward only happen where training is played
end
Extensions.Add("Breakable.Broken", function(attacker, _model, _source)
	reach(asPlayer(attacker), "BreakIn")
end)
Extensions.Add("Camera.Viewed", function(player, model)
	if model ~= nil then
		reach(asPlayer(player), "Cams")
	end
end)
```

## Writing your own handler

```lua
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

-- Any (veto): return true to stop it
Extensions.Add("Gun.PreventFire", function(who, gunId, tool)
	return typeof(who) == "Instance" and who:IsA("Player") and who:GetAttribute("Frozen") == true
end)

-- Product (multiplier): return 1 when your rule doesn't apply
Extensions.Add("Movement.SpeedMultiplier", function(player, gunId)
	return if gunId == "LMG" then 0.9 else 1
end)

-- Fire (notification): react, return nothing
local remove = Extensions.Add("Gun.Reloaded", function(who, tool, gunId)
	print(who.Name, "reloaded", gunId)
end)
remove() -- Add returns a function that removes the handler
```

### Rules for handlers

- **Handlers are global.** A `Gun.DamageMultiplier` handler runs for *every* shot by *everyone*. Check the player, gun or mode first and return `1` / `nil` when it doesn't apply.
- **"who" is often a Player *or* an NPC model.** Guns, combat, breakables and consumables pass whichever fired. Check with `who:IsA("Player")` before reading player-only things.
- **Don't yield** in `Any` or `Product` handlers: the core is waiting on your answer.
- **Add handlers in `Start`**, not at require time, so the systems you read from are initialized.
- **Remove handlers you no longer need** (for example at the end of a match) with the function `Add` returned.

## Adding a new point

There is nothing to register. In your system, call `Extensions.Any`, `Product` or `Fire` with a new dotted name (`"<System>.<What>"`), then:

1. List it in your module's header comment, with its kind and arguments.
2. Add it to [All extension points](../reference/extension-points.md) and your system's page.
3. Pass tables, not long argument lists, for things that may grow. `Siege.Ended` does this: its third argument is a summary table, so new fields never break old handlers.
