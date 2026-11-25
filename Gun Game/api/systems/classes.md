# Classes and abilities

Each Siege player picks a **class**: a default loadout, the gun categories they may swap to, and one **ability** (a flashbang, a breach charge, a camera…). A class can be taken by one player per team.

!!! abstract "Source"

    `Systems.Classes.ClassService`, `Systems.Classes.Gadgets`, `Systems.Classes.Abilities.*` (one module per ability). Data: `Content.Classes.Classes`, `Content.Classes.Definitions.*`. Design guide: [Siege classes](../../CLASSES.md).

## How the pieces fit

```text
Content.Classes.Definitions.Flash      ── data: loadout, Ability = { Id = "Flashbang", Cooldown, Charges, Tuning }
            │
SiegeService ──Assign/Arm──▶ ClassService ── holds class, charges, cooldown per player
                                  │  Packets.Class.Use (client presses T)
                                  │  every check ▶ builds a context ▶
                                  ▼
                 Systems.Classes.Abilities.Flashbang.Use(context) ── returns ok, message
                                  │ uses
                                  ▼
                 Gadgets (aim, place, blast, enemies) · Combat · EffectService
```

!!! info "A class is a secret"

    A player's class is **never** a replicated attribute. Only its owner is sent `Packets.Class.State`; other players learn classes only from the Siege snapshots their team is allowed to see.

## `ClassService` API

```lua
local ClassService = require(game.ServerScriptService.Modules.Systems.Classes.ClassService)
```

### `ClassService.Assign(player, classId, guns?) → boolean`

Gives a player a class. Refused if it isn't their team's (their `Team` attribute must be set) or a teammate already has it. Each gun in `guns` (by slot) must be one the class allows there, else the class default is used. Fires `Classes.Assigned`.

```lua
ClassService.Assign(player, "Breacher")                          -- default guns
ClassService.Assign(player, "Flash", { "AssaultRifle", "SMG" })  -- slot 2 swapped to an allowed SMG
```

```lua title="ClassService.Assign (one per team, allowed guns)"
for other, theirs in held do
	if other ~= player and theirs.Class.Id == classId and TeamService.TeamOf(other) == team then
		return false -- One per team
	end
end
local carried = {}
for slot, default in class.Loadout do
	local wanted = guns and guns[slot]
	carried[slot] = if type(wanted) == "string" and Classes.Allows(class, slot, wanted) then wanted else default
end
```

### `ClassService.ClassOf(player) → Class?`

The `Content.Classes` class table, or `nil`. **The only way to read a class**: it's never an attribute.

```lua
local class = ClassService.ClassOf(player)
if class then print(class.Name, class.Ability.Id) end
```

### `ClassService.Arm(player) → boolean`

Gives a living player their class's guns and the knife (`LoadoutService.Arm`), and equips the Shield class's shield.

```lua
player.CharacterAdded:Connect(function()
	task.defer(ClassService.Arm, player)
end)
```

### `ClassService.Charges(player) → (charges, readyAt)`

Charges left (`-1` unlimited, `0` with no class) and the server time the cooldown ends.

```lua
local charges, readyAt = ClassService.Charges(player)
local ready = charges ~= 0 and workspace:GetServerTimeNow() >= readyAt
```

### `ClassService.Use(player, timestamp, origin, look) → (ok, message)`

Every check, then the ability (below). What `Packets.Class.Use` calls.

```lua
local head = player.Character.Head
local ok, message = ClassService.Use(player, workspace:GetServerTimeNow(), head.Position, head.CFrame.LookVector)
```

### `ClassService.Clear(player)` / `ClassService.Reset()`

Take one player's class away / everyone's, and remove every gadget (each ability module's `Reset` runs too).

```lua
ClassService.Reset() -- new match
```

### What `Use` checks, in order

This is the real gatekeeper for every ability. Each check is a line:

```lua title="Systems.Classes.ClassService.Use (trimmed)"
if type(timestamp) ~= "number" or timestamp ~= timestamp or not finite(origin) or not finite(look) then
	return false, ""
end
if math.abs(now() - timestamp) > MAX_CLOCK_DRIFT or not bucket:allow(player.UserId) then
	return false, ""                                    -- stale or spammed
end
local mine = held[player]
if not mine then
	return false, "You have no class."
end
-- needs a living body, unless the ability is Bodiless and something vouches (Classes.AllowBodiless)
if player:GetAttribute("InLobby") == true or StateHandler.GetState(player, "Stunned") or StateHandler.GetState(player, "CantDoAnything") then
	return false, ""
end
if now() < mine.ReadyAt then
	return false, "Not ready yet."
end
if Extensions.Any("Classes.PreventAbility", player, mine.Class.Id, ability) then
	return false, "You can't use that now."              -- Siege refuses the wrong phase here
end
-- ...no charges left -> "No charges left."
local ran, ok, message, refund = pcall(module.Use, context)
-- on success: spend a charge, start the cooldown (scaled by Classes.CooldownMultiplier), push state,
Extensions.Fire("Classes.AbilityUsed", player, mine.Class.Id, ability.Id)
```

## The ability context

`Use` hands the ability module one table. **The origin is the server's view of the head, not the client's camera.**

```lua title="Systems.Classes.ClassService (Context type)"
-- Character, Humanoid and Root are nil for a Bodiless ability used with no body
export type Context = {
	Player: Player,
	Character: Model,
	Humanoid: Humanoid,
	Root: BasePart,
	Origin: Vector3,   -- The head's position (the server's, not the client's)
	Look: Vector3,     -- Unit
	Team: string?,
	Class: Classes.Class,
	Ability: Classes.Ability,
	Tuning: { [string]: any },   -- the class file's Ability.Tuning
}
```

## Writing an ability: the Flashbang, walked through

Every shipped ability is described in [Class abilities](abilities.md). An ability is a ModuleScript in `Systems.Classes.Abilities`, **named exactly the class's `Ability.Id`**, with `Use(context)` returning `(ok, message?)`. `ClassService` finds and requires it by name the first time it's used.

**1. The data** lives in the class file (see [the full Flash class](../foundations/data-and-content.md#the-one-file-per-thing-pattern)): `Ability = { Id = "Flashbang", Cooldown = 8, Charges = 3, Phases = { "Action" }, Tuning = { Fuse = 1.4, Radius = 30, ... } }`.

**2. `Use` throws it.** Note it reads every number from `context.Tuning` and never trusts the client's position:

```lua title="Systems.Classes.Abilities.Flashbang.Use"
function Flashbang.Use(context: any): (boolean, string?)
	local tuning = context.Tuning
	local template = ReplicatedStorage.Assets.Models.Siege:FindFirstChild("Flashbang")
	local body = template and template:IsA("Model") and template.PrimaryPart
	if not body then
		return false, "That didn't work."
	end
	-- Just ahead of the head, but never through a wall
	local start = context.Origin + context.Look * THROW_AHEAD
	local wall = Workspace:Raycast(context.Origin, context.Look * (THROW_AHEAD + 0.6), params)
	if wall then
		start = context.Origin + context.Look * math.max(0, wall.Distance - 0.6)
	end
	local part = body:Clone()
	part.CollisionGroup = THROWN_GROUP          -- doesn't hit players
	part.CFrame = CFrame.new(start)
	part.Parent = thrownFolder()
	part:SetNetworkOwner(nil)                    -- the server owns its physics
	part.AssemblyLinearVelocity = context.Look * tuning.ThrowSpeed + Vector3.yAxis * tuning.ThrowLift
	EffectService.Play("ConsumableThrow", { Target = context.Character }, context.Player)
	local thrower, team = context.Player, context.Team
	task.delay(tuning.Fuse, function()
		if not part.Parent then
			return
		end
		local position = part.Position
		part:Destroy()
		pop(thrower, team, position, tuning)
	end)
	return true, nil
end
```

**3. The effect is decided on the server** and exposes its own extension points, so other content can change it:

```lua title="Systems.Classes.Abilities.Flashbang (pop, trimmed)"
for _, victim in Players:GetPlayers() do
	-- skip the dead, the too-far, and anyone with a wall in the way (raycast)
	if Extensions.Any("Classes.PreventFlash", thrower, victim) then
		continue
	end
	local facing = distance < 0.5 or head.CFrame.LookVector:Dot(offset / distance) > tuning.FacingDot
	local seconds = tuning.MinTime
	if facing then
		seconds = tuning.FullTime + (tuning.MinTime - tuning.FullTime) * math.clamp(distance / tuning.Radius, 0, 1)
	end
	if team ~= nil and victim:GetAttribute("Team") == team then
		seconds *= tuning.SelfShare                 -- teammates get less
	end
	seconds *= Extensions.Product("Classes.FlashTimeMultiplier", thrower, victim)
	if seconds > 0.05 then
		Packets.Class.Flash:FireClient(victim, seconds)
		Extensions.Fire("Classes.Flashed", thrower, victim, seconds)
	end
end
```

### Optional hooks an ability module may have

| Function | Called by `ClassService` when |
| --- | --- |
| `Reset()` | `ClassService.Reset()` (a new match or its end) |
| `HasActive(player)` | Deciding if a use is "activating" something already placed (no charge spent), and in `Class.State.ActiveGadget` |
| `Clear(player)` | Used by `Shield` and `C4` when a player's class is cleared |

### Adding a class, checklist

1. Copy a file in `Content.Classes.Definitions`, change `Id`, `Name`, `Team`, `Order`.
2. Reuse an existing `Ability.Id`, or add `Systems.Classes.Abilities.<Id>` with `Use(context)`.
3. Put every number in `Ability.Tuning`; read it as `context.Tuning`.
4. List the ability's extension points in its header and in [All extension points](../reference/extension-points.md).

## `Gadgets`: what abilities share

A placed gadget is a model in `workspace.SiegeGadgets` with attributes `Gadget` (kind), `GadgetOwner` (UserId) and `Team`. A gadget with a Humanoid is damaged by every weapon through `Combat.ApplyHit`; its own team can't hurt it.

```lua
local Gadgets = require(game.ServerScriptService.Modules.Systems.Classes.Gadgets)
```

### `Gadgets.Aim(context, range) → RaycastResult?`

The surface the player looks at within `range`, or `nil`. Drones, thrown things and other gadgets are never a surface.

```lua
local hit = Gadgets.Aim(context, context.Tuning.Range)
if not hit then return false, "Aim at a surface in reach." end
```

### `Gadgets.Place(kind, context, hit, health?) → Model?`

Clones `Assets.Models.Siege.<kind>` onto the surface (front facing out), in `workspace.SiegeGadgets`, with `Gadget`, `GadgetOwner` and `Team`. With `health` it gets a Humanoid and can be shot. Fires `Classes.GadgetPlaced`.

```lua title="Systems.Classes.Abilities.Laser.Use"
local hit = Gadgets.Aim(context, tuning.Range or 9)
if not hit then return false, "Aim at a wall or other surface within reach." end
local model = Gadgets.Place("Laser", context, hit, tuning.Health or 30)
if not model or not model.PrimaryPart then return false, "Laser model is not ready." end
```

### `Gadgets.SurfaceCFrame(hit, thickness) → CFrame`

The CFrame that sits a part of that thickness flat on the hit surface (Laser and Proximity Sensor use it to re-orient flat models).

```lua
model:PivotTo(Gadgets.SurfaceCFrame(hit, base.Size.Y) * CFrame.Angles(-math.pi / 2, 0, 0) * offset)
```

### `Gadgets.OnDestroyed(model, function(killer?) end)`

Runs when its health reaches 0 (the model is removed right after). `killer` from the damage log.

```lua
Gadgets.OnDestroyed(model, function(killer)
	print(model.Name, "destroyed by", killer and killer.Name or "nobody")
end)
```

### `Gadgets.Remove(model)` / `Gadgets.IsLive(model) → boolean`

Remove without the destroyed effect / still standing.

```lua
while Gadgets.IsLive(model) do
	task.wait(tuning.Check)
end
```

### `Gadgets.Blast(position, radius, damage, attacker, item)`

Hurts every humanoid in the radius (falling to 25% at the edge) through `Combat.ApplyHit`.

```lua
Gadgets.Blast(model:GetPivot().Position, tuning.BlastRadius, tuning.BlastDamage, owner, "Trap Mine")
```

### `Gadgets.Enemies(team) → { Target }` / `Gadgets.Allies(team) → { Target }`

Living players not on / on that team, each `{ Player, Character, Root, Humanoid }`.

```lua
for _, enemy in Gadgets.Enemies(context.Team) do
	if (enemy.Root.Position - origin).Magnitude < tuning.Radius then
		DroneService.Mark({ context.Player }, tostring(enemy.Player.UserId), enemy.Root.Position, tuning.MarkTime)
	end
end
```

### `Gadgets.Clear()`

Removes every gadget (`ClassService.Reset` calls it).

## Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Classes.PreventAbility` | Any | player, classId, ability |
| `Classes.AllowBodiless` | Any | player, classId |
| `Classes.CooldownMultiplier` | Product | player, classId, abilityId |
| `Classes.AbilityUsed` / `Classes.Assigned` | Fire | player, classId, abilityId / player, classId |
| `Classes.GadgetPlaced` / `Classes.GadgetDestroyed` | Fire | player, kind, model / owner?, kind, model, killer? |
| `Classes.PreventFlash` / `Classes.FlashTimeMultiplier` / `Classes.Flashed` | Any / Product / Fire | thrower, victim (, seconds) |
| Other ability points | | `Classes.BreachDetonated`, `PreventPulseMark`, `Pulsed`, `PreventMineTrigger`, `MineDetonated`, `HealMultiplier`, `Healed`, `Reinforced`: see [Class abilities](abilities.md) |

```lua
-- Abilities can't be used in the first 5 seconds of Action
local actionStarted = 0
Extensions.Add("Siege.PhaseChanged", function(phase)
	if phase == "Action" then actionStarted = workspace:GetServerTimeNow() end
end)
Extensions.Add("Classes.PreventAbility", function(player, classId, ability)
	return SiegeService.Phase() == "Action" and workspace:GetServerTimeNow() - actionStarted < 5
end)

-- Medics recharge 20% faster
Extensions.Add("Classes.CooldownMultiplier", function(player, classId, abilityId)
	return if classId == "Medic" then 0.8 else 1
end)
```

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Class.Use` | Client → server, answered `(ok, message)` | server time, camera position, unit look |
| `Class.Hold` | Client → server | active, origin, look (the Reinforce hold; completion is `Class.Use`) |
| `Class.State` | Server → owner only | `{ ClassId, Charges, ReadyAt, Guns, ActiveGadget }` or `nil` |
| `Class.Flash` | Server → one client | seconds blinded |
| `Class.HologramPose` / `Class.HologramGlitch` | Client → server / server → all | pose, aiming / model, reason |
| `DeadCall.State` / `Control` / `Phone` | (Hacker) | see [All packets](../reference/packets.md) |

Client: `Client.Hud.SiegeHud.UseAbility()` uses the ability; `Client.Core.ClassPanel` fills class and gun panels.
