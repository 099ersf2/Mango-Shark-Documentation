# World: boards, soft walls and grenades

The map can be broken and rebuilt: **boards** on doors and windows break piece by piece and can be repaired, **soft walls** get holes punched through them, and **grenades and smoke** change the fight. All three are weapon-agnostic: any weapon calls the same functions with the part it hit.

!!! abstract "Source"

    `Systems.Breakables.BreakableService`, `Systems.Destruction.SoftWalls`, `Systems.Consumables.ConsumableService`, `Shared.Smoke`. Data: `Content.Breakables.*`, `Content.Destruction.SoftWallConfig`, `Content.Consumables.*`. Guides: [Breakables](../../BREAKABLES.md), [Soft walls](../../SOFTWALLS.md), [Consumables](../../CONSUMABLES.md).

```lua
local Systems = game.ServerScriptService.Modules.Systems
local BreakableService = require(Systems.Breakables.BreakableService)
local SoftWalls = require(Systems.Destruction.SoftWalls)
local ConsumableService = require(Systems.Consumables.ConsumableService)
```

---

## Boards: `BreakableService`

A breakable is a model whose pieces are placed in a fixed order and **broken in reverse**. Pieces `1..Intact` are up; the rest are hidden and block nothing, not even bullets. **Damage always goes to the top intact piece**, whatever part was hit. On start every BasePart tagged with a type's tag (`Board`, `DoorBoard`, …) is replaced by that type's model; a tagged Model is used as is.

`target` below is the board model **or any part in it**. `attacker` is a Player, an NPC model, or `nil`.

### `BreakableService.Damage(target, amount, attacker?, source?) → number`

Damages the top piece; leftover damage can spill to the next. Returns the damage dealt (`0` if `target` isn't a breakable).

```lua
local dealt = BreakableService.Damage(hitPart, 30, player, "Bullet")
```

### `BreakableService.DamageRadius(position, radius, amount, attacker?, source?, ignore?) → number`

Damages every breakable in a radius; returns how many were hit.

```lua
local count = BreakableService.DamageRadius(position, 12, 100, player, "Explosion")
```

### `BreakableService.IsBreakable(target) → boolean`

```lua
if BreakableService.IsBreakable(result.Instance) then
	BreakableService.Damage(result.Instance, damage, player, "Bullet")
end
```

### `BreakableService.Get(target) → { Model, Type, Intact, Total, Health }?`

```lua
local board = BreakableService.Get(part)
if board then print(board.Type, board.Intact, "/", board.Total) end
```

### `BreakableService.Repair(target, player?, expectedPiece?) → (ok, reason)`

Places the next missing piece, in order.

```lua
local ok, reason = BreakableService.Repair(board, player)
```

### `BreakableService.Reset(target)`

Every piece back at full health, no effects.

```lua
BreakableService.Reset(board)
```

### `BreakableService.RemoveCoating(target)`

Strips the spray paint only.

```lua
BreakableService.RemoveCoating(board)
```

### `BeginRepairHold` / `CompleteRepairHold` / `EndRepairHold` / `CancelRepairHold(target, player)`

The hold-E repair prompt's steps (the `RepairPrompt` on each board calls these). Call `CancelRepairHold` if something interrupts a player mid-repair.

```lua
BreakableService.CancelRepairHold(board, player)
```

**Attributes:** model `BreakableType`, `Intact`, `Total`, `Health` (top piece), `MaxHealth`, `Complete` (and `Reinforced`); each piece `Broken`. **Pathfinding:** every intact piece carries a `PathfindingModifier` NPC paths price as a wall (or, for Siege attacker bots, a door).

| Point | Kind | Arguments |
| --- | --- | --- |
| `Breakable.PreventDamage` | Any | who, model, amount, source |
| `Breakable.DamageMultiplier` | Product | who, model, source |
| `Breakable.PieceBroken` | Fire | who, model, piece, source |
| `Breakable.Broken` | Fire | who, model, source |
| `Breakable.PreventRepair` | Any | player, model, piece |
| `Breakable.Repaired` | Fire | player, model, piece |

```lua
-- Explosions do double damage to boards
Extensions.Add("Breakable.DamageMultiplier", function(who, model, source)
	return if source == "Explosion" then 2 else 1
end)

-- Count only the piece that finishes a door or window
Extensions.Add("Breakable.Repaired", function(player, model, piece)
	if model:GetAttribute("Complete") == true then
		QuestService.Add(player, "BoardsBuilt")
	end
end)
```

---

## Soft walls: `SoftWalls`

Parts tagged `SoftWall` get holes punched where bullets, bashes and grenades meet them; bullets carry on through with less damage.

### `SoftWalls.Punch(target, position, direction?, radius?, attacker?, source?) → boolean`

Queues a hole; `true` if queued. The radius is the caller's, else `SoftWallConfig.Sources[source]`, else the wall's `SoftWallHoleRadius`, else the default.

```lua
SoftWalls.Punch(wallPart, hitPosition, look, 0.3, player, "Trap")
```

### `SoftWalls.IsSoftWall(part) → boolean` / `SoftWalls.SourceOf(part) → BasePart?`

Is this a soft wall (or a piece of one) / the original tagged wall it came from.

```lua
if SoftWalls.IsSoftWall(hit) then
	local wall = SoftWalls.SourceOf(hit)
end
```

### `SoftWalls.Reset(target)` / `SoftWalls.ResetAll()`

Put one wall / every punched wall back (also the `softwallreset` command).

```lua
SoftWalls.ResetAll() -- between rounds
```

### `SoftWalls.Stats()` / `SoftWalls.SmokeOpenings(part)`

Debug counters (rebuilds, debris) / the openings smoke can drift through.

```lua
print(SoftWalls.Stats())
```

| Point | Kind | Arguments |
| --- | --- | --- |
| `SoftWall.PreventPunch` | Any | who, wall, source |
| `SoftWall.PieceFell` | Fire | who, wall, piece |

---

## Grenades and smoke: `ConsumableService`

Each player carries **one kind** (`Grenade` or `Smoke`, picked and saved) and gets `Consumables.PER_LIFE` of it every spawn. The Player attributes `ConsumableId` and `ConsumableCount` show it; the client only reads them and sends intent.

- **A throw:** checks (not in the lobby, alive, not stunned, one left, past `THROW_COOLDOWN`, not stopped by `Consumable.PreventThrow`), then a server-owned projectile in the `Thrown` collision group is launched from ahead of the head. After `Fuse` it detonates where it lies.
- **Grenade:** every living humanoid within `Radius` in clear view takes `Damage`, falling to `Damage × EdgeShare` at the edge, through `Combat.ApplyHit` (thrower gets credit, takes `SelfShare`). Boards take `BreakableDamage`; nearby soft walls get holes.
- **Smoke:** an invisible cloud tagged `SmokeCloud` with a `Radius` attribute; blocks NPC sight and aim assist (`Smoke.Blocks`) for `Duration`.

### `ConsumableService.Get(player) → (consumable?, count)`

```lua
local consumable, left = ConsumableService.Get(player)
print(consumable and consumable.Id, left)
```

### `ConsumableService.Refill(player)`

Back to `PER_LIFE` (done on every spawn).

```lua
ConsumableService.Refill(player)
```

### `ConsumableService.SetCount(player, count)`

Clamped to `0..PER_LIFE`.

```lua
ConsumableService.SetCount(player, 0) -- no grenades this round
```

### `ConsumableService.Throw(player, direction) → BasePart?`

Every check, then a throw. What `Packets.Consumable.Throw` calls.

```lua
ConsumableService.Throw(player, player.Character.Head.CFrame.LookVector)
```

### `ConsumableService.Detonate(id, position, attacker?) → boolean`

A blast or smoke cloud right there, no throw. `attacker` is a Player or NPC model (for credit).

```lua
ConsumableService.Detonate("Grenade", position, player)
ConsumableService.Detonate("Smoke", position)
```

### `ConsumableService.ThrowAs(model, id, start, velocity) → BasePart?`

A throw for a server-side thrower (NPCs), with an exact launch velocity and no player checks.

```lua
ConsumableService.ThrowAs(npcModel, "Grenade", npcModel.Head.Position, look * 50 + Vector3.yAxis * 15)
```

| Point | Kind | Arguments |
| --- | --- | --- |
| `Consumable.PreventThrow` | Any | player, id |
| `Consumable.DamageMultiplier` | Product | attacker?, id, humanoid |
| `Consumable.Thrown` | Fire | player, id, projectile |
| `Consumable.Detonated` | Fire | attacker?, id, position |

```lua
-- No grenades during Prep
Extensions.Add("Consumable.PreventThrow", function(player, id)
	return SiegeService.Phase() == "Prep"
end)
```

Packets: `Consumable.Throw` (server time, look) and `Consumable.Pick` (consumable Id), both client → server.

### Smoke from anywhere: `Shared.Smoke.Blocks(from, to) → boolean`

```lua
local Smoke = require(game.ReplicatedStorage.Modules.Shared.Smoke)
if Smoke.Blocks(eye, target) then return end -- hidden by smoke (bullets still pass)
```

More: [World: boards, soft walls and explosions](../../EXAMPLES.md#world-boards-soft-walls-and-explosions).
