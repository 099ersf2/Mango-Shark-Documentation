# World: boards, soft walls and grenades

The map can be broken and rebuilt: **boards** on doors and windows break piece by piece and can be repaired, **soft walls** get holes punched through them, and **grenades and smoke** change the fight. All three are weapon-agnostic: any weapon calls the same functions with the part it hit.

!!! abstract "Source"

    `Systems.Breakables.BreakableService`, `Systems.Destruction.SoftWalls`, `Systems.Consumables.ConsumableService`, `Shared.Smoke`. Data: `Content.Breakables.*`, `Content.Destruction.SoftWallConfig`, `Content.Consumables.*`. Guides: [Breakables](../../BREAKABLES.md), [Soft walls](../../SOFTWALLS.md), [Consumables](../../CONSUMABLES.md).

## Boards: `BreakableService`

A breakable is a model whose pieces are placed in a fixed order and **broken in reverse**. Pieces `1..Intact` are up; the rest are hidden and block nothing, not even bullets. **Damage always goes to the top intact piece**, whatever part was hit.

On start, every BasePart tagged with a type's tag (`Board`, `DoorBoard`, …) is replaced by a copy of that type's model; a tagged Model is used as is. Parts tagged later are picked up too.

```lua title="From the BreakableService header"
BreakableService.Damage(part, 30, player, "Bullet")              -- damage dealt, 0 if part is not a breakable
BreakableService.DamageRadius(position, 8, 40, player, "Explosion", ignore?)
BreakableService.IsBreakable(part)                               -- true for any part of a breakable model
BreakableService.Get(part)                                       -- { Model, Type, Intact, Total, Health } or nil
BreakableService.Repair(part, player?, expectedPiece?)           -- places the next piece: (ok, reason)
BreakableService.Reset(part)                                     -- every piece back, full health, no effects
```

| Function | Notes |
| --- | --- |
| `Damage(target, amount, attacker?, source?)` | `target` is the model or any part in it. Leftover damage can spill to the next piece |
| `DamageRadius(position, radius, amount, attacker?, source?, ignore?)` | Returns how many breakables were hit |
| `RemoveCoating(target)` | Strips the spray paint only |
| `BeginRepairHold` / `CompleteRepairHold` / `EndRepairHold` / `CancelRepairHold(target, player)` | The hold-E repair prompt's steps |

**Attributes:** the model has `BreakableType`, `Intact`, `Total`, `Health` (of the top piece), `MaxHealth`, `Complete` (and `Reinforced` once a Reinforcement Expert covers it); each piece has `Broken`.

**Pathfinding:** every intact board piece carries a `PathfindingModifier` (PassThrough) that NPC paths price: most NPCs treat it as a wall, Siege attacker bots as a door that costs a little extra.

| Point | Kind | Arguments |
| --- | --- | --- |
| `Breakable.PreventDamage` | Any | who, model, amount, source |
| `Breakable.DamageMultiplier` | Product | who, model, source |
| `Breakable.PieceBroken` / `Breakable.Broken` | Fire | who, model, piece, source / who, model, source |
| `Breakable.PreventRepair` | Any | player, model, piece |
| `Breakable.Repaired` | Fire | player, model, piece |

!!! tip "A whole door or window rebuilt"

    `Breakable.Repaired` fires per piece. Check `model:GetAttribute("Complete") == true` to count only the piece that finishes it. Quests and the tutorial both do this.

## Soft walls: `SoftWalls`

Parts tagged `SoftWall` get holes punched where bullets, bashes and grenades meet them. Bullets carry on through with less damage.

| Function | Returns / does |
| --- | --- |
| `SoftWalls.Punch(target, position, direction?, radius?, attacker?, source?)` | Queues a hole; `true` if queued. Radius: the caller's, else `SoftWallConfig.Sources[source]`, else the wall's `SoftWallHoleRadius`, else the default |
| `SoftWalls.IsSoftWall(part)` / `SourceOf(part)` | Is this a soft wall or a piece of one / the original tagged wall |
| `SoftWalls.Reset(target)` / `ResetAll()` | Puts one wall / every wall back |
| `SoftWalls.Stats()` | Debug counters |
| `SoftWalls.SmokeOpenings(part)` | Openings smoke can drift through |

| Point | Kind | Arguments |
| --- | --- | --- |
| `SoftWall.PreventPunch` | Any | who, wall, source |
| `SoftWall.PieceFell` | Fire | who, wall, piece |

## Grenades and smoke: `ConsumableService`

Each player carries **one kind** (picked in the Loadout menu, saved) and gets `Consumables.PER_LIFE` of it every spawn. The kind and count are the Player attributes `ConsumableId` and `ConsumableCount`; the client only reads them and sends intent.

**A throw:** checks (not in the lobby, alive, not stunned, one left, past `THROW_COOLDOWN`, not stopped by `Consumable.PreventThrow`), then the server clones the model ahead of the head, in the `Thrown` collision group, owned by the server, and launches it. After `Fuse` seconds it detonates where it lies.

**Grenade:** every living humanoid within `Radius` in clear view takes `Damage` falling to `Damage * EdgeShare` at the edge, through `Combat.ApplyHit` with the thrower as Attacker. The thrower takes `SelfShare`. Boards take `BreakableDamage`; nearby soft walls get holes.

**Smoke:** an invisible cloud part tagged `SmokeCloud` with a `Radius` attribute. It blocks NPC sight and aim assist (`Shared.Smoke.Blocks(from, to)`) for `Duration` seconds.

| Function | Returns / does |
| --- | --- |
| `ConsumableService.Get(player)` | `(consumable?, countLeft)` |
| `ConsumableService.Refill(player)` | Back to `PER_LIFE` (done every spawn) |
| `ConsumableService.SetCount(player, count)` | Clamped to `0..PER_LIFE` |
| `ConsumableService.Throw(player, direction)` | Every check, then a throw; the projectile or `nil` |
| `ConsumableService.Detonate(id, position, attacker?)` | A blast or smoke cloud right there, no throw. `attacker` is a Player or NPC model |
| `ConsumableService.ThrowAs(model, id, start, velocity)` | A throw for a server-side thrower (NPCs), exact launch velocity |

| Point | Kind | Arguments |
| --- | --- | --- |
| `Consumable.PreventThrow` | Any | player, id |
| `Consumable.DamageMultiplier` | Product | attacker?, id, humanoid |
| `Consumable.Thrown` | Fire | player, id, projectile |
| `Consumable.Detonated` | Fire | attacker?, id, position |

Packets: `Consumable.Throw` (server time, look) and `Consumable.Pick` (consumable Id), both client → server.

## Example: an explosion anywhere

```lua
local Systems = game.ServerScriptService.Modules.Systems
local ConsumableService = require(Systems.Consumables.ConsumableService)
local BreakableService = require(Systems.Breakables.BreakableService)
local SoftWalls = require(Systems.Destruction.SoftWalls)

-- Full grenade: damage, boards, walls, effects; the player gets the kills
ConsumableService.Detonate("Grenade", position, player)

-- Just break boards around a point
local hit = BreakableService.DamageRadius(position, 12, 100, player, "Explosion")

-- Just a hole in the wall you're looking at
SoftWalls.Punch(wallPart, hitPosition, lookDirection, 0.3, player, "Trap")
```

More: [World: boards, soft walls and explosions](../../EXAMPLES.md#world-boards-soft-walls-and-explosions).
