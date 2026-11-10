# Soft walls

A soft wall is a part that weapons cut real holes through. Bullets pass through it with less damage and can still hit whatever is behind. The holes are physical: players see through them, shoot through them, and walk through them once they are big enough. Holes that cut a piece loose from everything holding it up (a ring of shots, say) make that piece fall out of the wall.

The server owns every wall. Clients only see the result: the pieces the wall is rebuilt from are ordinary replicated parts.

## Where things are

| What | Where |
| --- | --- |
| Server system | `ServerScriptService.Modules.Systems.Destruction.SoftWalls` |
| Every number | `ReplicatedStorage.Content.Destruction.SoftWallConfig` |
| Penetration (both sides) | `Shared.Guns.Ballistics` (`decidePierce`, `Ballistics.IsSoftWall`) |
| Gun hook | `Systems.Guns.GunService` (`punchSoftWall`, passed to Ballistics as `ctx.Data.SoftWallPunch`) |
| Damage after a wall | `Systems.Guns.AbilityRunner.Hit` (multiplies by `bullet.Data.SoftWallMultiplier`) |
| Melee hook | `Systems.Combat.SwordCombat` (source `"Melee"`) |
| Boards | `Systems.Breakables.BreakableService` resets a plank's holes when it is hidden or placed back |
| Cosmetic bullets | `Client.Guns.GunEffects` (no impact effect on soft walls; they pass through like the real bullet) |
| Test commands | `softwallpunch`, `softwallreset` in `CmdrSetup.Commands` |

## Making a wall

1. Put a `Part` where the wall goes and anchor it. A block works best; its thinnest axis is the thickness. Unions work too (the boards' spray paint is one). MeshParts may be refused by CSG: then bullets still pass through, but no hole is cut (a warning names the part once).
2. Give it the tag `SoftWall`.
3. Optional attributes:

| Attribute | Type | Meaning |
| --- | --- | --- |
| `SoftWallHoleRadius` | number | Hole radius for hits that do not set their own |
| `SoftWallSupport` | string | `"Auto"`, `"Bottom"`, `"Touching"` or `"All"` (see below). Default `Config.Support` (`"Auto"`) |

Nothing happens to a wall until it is first hit, so untouched walls cost nothing.

## How a hit becomes a hole

1. **The hit.** A server bullet that hits a soft wall calls `GunService`'s `punchSoftWall` (through `ctx.Data.SoftWallPunch`), which calls `SoftWalls.Punch` with the gun's hole radius. A sword swing calls it with source `"Melee"`. `Punch` only queues the cut and returns.
2. **The batch.** Every Heartbeat, up to `MaxRebuildStartsPerFrame` walls with queued cuts start a rebuild, with at most `MaxRebuildsInFlight` running across the map. A rebuild takes up to `MaxCutsPerRebuild` queued cuts at once, so the 8 pellets of a shotgun blast are one rebuild. Hits that arrive during a rebuild wait for the next one.
3. **The cut.** Each cut is a cutter through the whole thickness of the wall, along its normal, at the hit point, `2 x radius` wide. Its shape is `HoleShape`: a square (one box, turned by a random angle with `HoleSpin`, the default), an octagon (two boxes) or round (a cylinder). Only the pieces the cutters overlap are cut: one `GeometryService:SubtractAsync(piece, cutters, { SplitApart = true })` call per piece, which runs off the main thread and returns one solid per connected region.
4. **Support.** Each region that still reaches a holding edge (below) stays as an anchored piece. The others fall.
5. **The template.** The tagged part itself is never destroyed. The first rebuild hides it (Transparency 1; CanCollide, CanQuery and CanTouch off; its decals hidden) and keeps it to restore on `Reset`. The pieces are in a `SoftWallPieces` folder inside it, tagged `SoftWallPiece`, with the wall's color, material, transparency and collision.

A hole appears about 2 to 4 frames after the shot (the time `SubtractAsync` takes). The bullet does not wait: it passes through at once.

## The support rule

Each of the 4 edges of the wall's face is split into segments about `SupportSegment` (2) studs long. "Up" is the face axis closest to world up, so the bottom edge is the one facing down. Which segments hold the wall up depends on the mode:

| Mode | Holding segments |
| --- | --- |
| `"Auto"` (default) | The bottom edge, plus any segment touching other anchored, collidable geometry within `SupportProbe` (0.2) studs: a floor, a pillar, a ceiling, another wall |
| `"Bottom"` | The bottom edge only (the devs' first rule) |
| `"Touching"` | Only segments touching other geometry. For a wall hanging between two pillars |
| `"All"` | Every edge. A piece falls only once it is cut free of the wall's outline |

Support is worked out once, on the wall's first hit. If a mode finds no holding segment at all, the bottom edge holds the wall, so a whole wall never drops at once.

A piece stays while its bounds reach a holding segment (within `EdgeTolerance`). A piece from `SplitApart` is one connected solid, so its bounds reach an edge exactly when the piece does. Pieces never hold each other up: a piece hanging only from another loose piece falls with it.

Example: on a wall standing on the floor, a ring of holes cuts out a disc. The disc reaches no edge, so it falls; the rest of the wall still reaches the bottom edge and stays. A line of holes from the top edge to the bottom splits the wall in two halves that both stand.

## Debris

A piece that falls is unanchored, put in `workspace.SoftWallDebris`, tagged `SoftWallDebris`, moved to the `SoftWallDebris` collision group, shrunk by `DebrisShrink` on each side so it does not snag on its hole, and pushed along the shot at `DebrisPush` studs per second. The server owns its physics (network owner nil).

- It does not collide with players (the `Player` and `ProneBody` groups) unless `DebrisCollidesWithPlayers` is true, so falling chunks never fling or trap anyone.
- Bullets pass through it without a hit, on the server and for cosmetic bullets.
- It is removed after `DebrisLifetime` (8 s). At most `MaxDebris` (20) pieces are alive map-wide; the oldest go first.
- Pieces with a bounding box under `MinDebrisVolume` just vanish.

## Bullets and penetration

`Shared.Guns.Ballistics` decides, for hitscan traces and simulated FastCast2 bullets, on the server and on clients alike:

1. A hit on falling debris is skipped: no `OnHit`, no impact, the bullet carries on.
2. A hit on a soft wall or a piece of one runs `OnHit` as usual (so boards count it), then, on the server, punches the hole. If the gun penetrates (`Guns[Id].Penetrates` is not false) and the bullet has passed fewer than `MaxWallsPerBullet` (4) walls, it carries on and keeps `PenetrationMultiplier` of its damage (the gun's own, else the default). The multipliers stack per wall, in `bullet.Data.SoftWallMultiplier`. A soft wall does not use up the gun's `Projectile.Pierce`.
3. Otherwise the usual rule: an ability's `CanPierce` (Ricochet bounces), then `Projectile.Pierce`.

After a soft wall the bullet ignores the whole wall (the tagged part and all its pieces), so it cannot hit the same wall twice on the way out. `AbilityRunner.Hit` multiplies humanoid and breakable damage by `SoftWallMultiplier`. With the Rifle (0.65), a 30-damage bullet does 19.5 through one wall and 12.7 through two.

Client cosmetic bullets run the same rule, so tracers go through the wall where the real bullet did, even before the hole has replicated. Soft walls get no impact effect or bullet-hole decal on clients: the hole itself is the impact.

## Boards

The board planks and spray paint (`Assets.Models.Board`, `DoorBoard`) are tagged `SoftWall` by the devs, so bullets pass through boards and cut holes in the planks. `AbilityRunner.Hit` keeps the devs' board rule on top of that: each bullet counts one hole per board (`BulletHoles`); a bullet that hits the intact spray paint removes it and punches the plank behind; the fifth hole breaks the whole board. `BreakableService` resets a plank's holes whenever it hides or places the plank, so a repaired plank comes back whole.

## Config

All in `Content.Destruction.SoftWallConfig`. Sizes are studs, times seconds.

| Field | Default | Meaning |
| --- | --- | --- |
| `Tag` | `"SoftWall"` | Tag that makes a part a soft wall |
| `PieceTag` | `"SoftWallPiece"` | Tag on the anchored pieces |
| `DebrisTag` | `"SoftWallDebris"` | Tag on falling pieces |
| `HoleRadius` | `0.235` | Default hole radius |
| `MinHoleRadius`, `MaxHoleRadius` | `0.05`, `4` | Any radius is clamped into this range |
| `HoleShape` | `"Square"` | `"Square"`, `"Octagon"` or `"Round"`. See [Hole shape and cost](#hole-shape-and-cost) |
| `HoleSpin` | `true` | Turn each square or octagon by a random angle about the normal |
| `PenetrationMultiplier` | `0.6` | Damage kept per wall passed |
| `MaxWallsPerBullet` | `4` | Soft walls one bullet may pass |
| `Guns` | Pistol 0.5, Rifle 0.65, BurstRifle 0.7, Shotgun 0.4 | Per gun Id: `HoleRadius`, `PenetrationMultiplier`, `Penetrates` |
| `Sources` | Melee `HoleRadius = 0.45` | Per `Punch` source: `HoleRadius` |
| `MaxRebuildStartsPerFrame` | `2` | Walls that may start a rebuild per Heartbeat |
| `MaxRebuildsInFlight` | `4` | Walls rebuilding at once |
| `MaxCutsPerRebuild` | `16` | Holes cut in one rebuild |
| `MaxPendingCuts` | `48` | Holes waiting on one wall; more are dropped (the bullet still passes) |
| `Support` | `"Auto"` | Default support mode |
| `SupportProbe`, `SupportSegment` | `0.2`, `2` | Touch probe depth and edge segment length |
| `BottomDot` | `0.7` | How far down an edge must face to be the bottom |
| `EdgeTolerance` | `0.05` | How close a piece's bounds must come to an edge |
| `MinDebrisVolume` | `0.02` | Smaller loose pieces vanish |
| `DebrisLifetime`, `MaxDebris` | `8`, `20` | Debris cleanup |
| `DebrisPush`, `DebrisShrink` | `4`, `0.02` | Debris push speed, shrink per side |
| `DebrisCollidesWithPlayers`, `DebrisCollisionGroup` | `false`, `"SoftWallDebris"` | Debris collisions |
| `HoleEffect`, `ChunkEffect` | `"SoftWallHole"`, `"SoftWallChunk"` | Registry effects, skipped while not in `Content.Effects.Registry` (none ship yet) |
| `HoleEffectInterval`, `MaxChunkEffects` | `0.06`, `2` | Effect rate limits |

Hole radius for a hit: the radius the caller passes (a gun's `Guns[Id].HoleRadius`), else `Sources[source].HoleRadius`, else the wall's `SoftWallHoleRadius`, else `HoleRadius`.

## API (for any weapon)

All on `Systems.Destruction.SoftWalls` (server). Every function takes the wall or any piece of it, so a weapon passes whatever it hit.

```lua
local SoftWalls = require(ServerScriptService.Modules.Systems.Destruction.SoftWalls)

-- Queue a hole. False if the part is not a soft wall, the wall's queue is full, CSG refused it, or it was prevented
SoftWalls.Punch(part, position, direction?, radius?, attacker?, source?): boolean

SoftWalls.Reset(part)         -- the wall back whole; queued holes dropped; debris left to expire
SoftWalls.ResetAll()          -- every punched wall, like at round start
SoftWalls.IsSoftWall(part)    -- a tagged wall or a piece of one
SoftWalls.SourceOf(piece)     -- the tagged wall a piece belongs to
SoftWalls.Stats()             -- { Walls, Pieces, Debris, Pending, InFlight }
```

A grenade, for example:

```lua
for _, part in workspace:GetPartBoundsInRadius(position, 6) do
	if SoftWalls.IsSoftWall(part) then
		SoftWalls.Punch(part, part:GetClosestPointOnSurface(position), nil, 1.5, player, "Explosion")
	end
end
```

Extension points (`Shared.Extensions`):

| Point | Kind | Arguments |
| --- | --- | --- |
| `SoftWall.PreventPunch` | Any | who, wall, source |
| `SoftWall.PieceFell` | Fire | who, wall, piece |

## Testing

With Cmdr (admins):

- `softwallpunch` cuts one hole where you look. `softwallpunch 0.3 ring` cuts a ring of holes that knocks a disc out. Prints the wall's counts.
- `softwallreset` puts the wall you look at back whole; `softwallreset all` every wall.

Measured on the 10 x 10 wall at (-24, 15, -129): a ring of 28 holes (two rebuilds of 16 and 12) took 80 to 100 ms; the disc fell 3.4 studs to the floor in 1.5 s and was removed after 8 s; a ray through the ring hits nothing, a ray through solid wall hits a piece. A shotgun blast (8 holes, one rebuild) took 33 to 50 ms; single holes took 65 to 85 ms once the wall had about 100. The wall stayed one anchored piece throughout, and no frame went over 20 ms.

## Why CSG and not a grid

Both were measured on a real 10 x 10 x 1 wall in Edit mode:

| | CSG (`SubtractAsync`, kept) | Grid + greedy mesh |
| --- | --- | --- |
| Parts after a ring of 28 holes | 1 wall + 1 disc | 20 to 40 |
| Parts after ~100 holes | 1 to 2 | 110 to 250 |
| Cost per rebuild | 16 to 70 ms, off the main thread (frames stayed at 17 ms) | 0.3 to 1.4 ms on the main thread (plus remaking the parts) |
| Hole shape | Any convex prism (square by default) | Stair-stepped squares of the cell size |
| Works on unions | Yes | No (boxes only) |

CSG keeps the part count flat, which matters most with many walls on the map, and its cost is off the main thread and bounded by the rebuild caps. The price is latency (a hole shows a few frames late) and a new union per rebuild that clients download. See the limits.

## Hole shape and cost

The holes need `PreciseConvexDecomposition` collision: with `Default` or `Box` fidelity, rays and players hit a filled-in hole (measured: a ray through the middle of a hole is blocked). The cost of precise decomposition grows fast with the cutter's triangles. Measured on a fresh 10 x 10 x 1 wall:

| `HoleShape` | 1 hole | 28 holes in one rebuild |
| --- | --- | --- |
| `"Square"` (default) | 15 ms | 50 ms |
| `"Octagon"` | 16 ms | 134 ms |
| `"Round"` | 32 ms | 533 ms |

Round holes made a wall with about 100 holes take over a second per rebuild, so squares are the default; `HoleSpin` turns each one so they do not line up in a grid.

## Limits

- **Rebuild cost grows with holes.** A square cut takes about 15 to 35 ms on a fresh wall and about 65 ms after 70 holes. Batching keeps a shotgun blast to one rebuild.
- **Replication.** Every rebuild replaces the cut piece with a new union, whose mesh clients download. Fine for a few walls being shot at once; not measured with many players.
- **Pieces hold only on the wall's own edges.** A piece resting on another loose piece is not held by it.
- **Holes go along the normal**, whatever angle the bullet came in at.
- **No lag compensation**, the same as the guns.
- Walls are not reset by anything yet. Call `SoftWalls.ResetAll()` from a round system.
