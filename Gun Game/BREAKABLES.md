# Breakables

Breakable objects are models made of pieces that weapons knock off one at a time and players put back. The first type is the **Board**: planks nailed across a window, with a coat of spray paint on top.

The server owns every breakable. Clients only see the result: pieces are shown or hidden through replicated part properties, and the state is in attributes.

## Where things are

| What | Where |
| --- | --- |
| Server system | `ServerScriptService.Modules.Systems.Breakables.BreakableService` |
| Types (data) | `ReplicatedStorage.Content.Breakables.Registry`, one file per type in `Content.Breakables.Definitions` (`Board`) |
| Models | `ReplicatedStorage.Assets.Models` (`Board`) |
| Prompt keys (client) | `ReplicatedStorage.Modules.Client.Interact.PromptKeys` |
| Effects | `BoardBreak` and `BoardPlace` in `Content.Effects.Registry`; sounds `BoardBreak`, `BoardPlace` and `SprayPaint` in `Assets.Sounds`, dust `Assets.Vfx.BoardDust` (pooled by the Dust part) |
| Gun hook | `Systems.Guns.AbilityRunner.Hit` (bullets), `ShotContext.DamageBreakables` (explosive rounds) |

## How boards work

1. **Placing boards on the map.** Put a part where the board goes, the size of the board (4 x 5 x 0.24 studs), and give it the tag `Board`. Anchor it. When the server starts, `BreakableService` replaces every part with that tag with a copy of `Assets.Models.Board`. The copy's `BasePart` (its PrimaryPart) sits exactly on the tagged part's CFrame, and the tagged part is destroyed. Parts tagged later, while the game runs, are replaced too. A `Model` with the tag is used as it is, without being copied.
2. **Breaking.** Damage always goes to the top piece that is still up, whatever part was hit. The spray paint goes first, then the planks from the highest number down: Plank5, Plank4, ... Plank1. A piece that runs out of health is hidden: Transparency 1, and CanCollide, CanQuery and CanTouch off. A hidden piece blocks nothing, not even bullets. Damage left over after a piece breaks carries on to the next one (`CarryOverflow`).
3. **Bullets.** An intact piece is a normal solid part, so it stops bullets like a wall (unless the gun pierces). Every gun bullet that hits a piece damages the board: hitscan, simulated, each shotgun pellet, and ricochets. Explosive rounds also damage boards within their radius. Once a board is fully broken, bullets go through the window.
4. **Repairing.** While a piece is missing, the board shows a prompt (Hold E). Each completed hold places the next missing piece back at full health, in placing order: Plank1 up to Plank5, then the spray paint last. The prompt hides when the board is complete.

The server checks every repair: the player must be alive, within `MaxDistance` + 3 studs of the board, and past their `Cooldown`. The piece is always the server's own next piece. A caller that names a piece (`expectedPiece`) is refused if that piece is not next.

## The model the system expects

```
Board (Model, PrimaryPart = BasePart)
├─ BasePart     Part. Lines up with the tagged part. Made invisible and non-blocking; holds RepairPrompt
├─ Planks       Folder
│  ├─ Plank1    Placed first, broken last
│  ├─ ...
│  └─ PlankN    Placed last of the planks, broken first of the planks
└─ Spraypaint   BasePart (a union). Placed last, broken first
```

- Plank order comes from the number in the name (`^Plank(%d+)$`), not from the child order or position, so Plank10 comes after Plank9.
- Parts do not need to be anchored or welded. The system anchors every part when the board is made.
- Decals and Textures on a piece are hidden and shown with it.
- The model is not scaled to the tagged part. Make the tagged part the size of the model's `BasePart`.

Attributes the server sets (read them on the client):

| On | Attribute | Meaning |
| --- | --- | --- |
| Model | `BreakableType` | `"Board"` |
| Model | `Intact`, `Total` | Pieces up, and all pieces |
| Model | `Health`, `MaxHealth` | Health of the top intact piece |
| Model | `Complete` | True when every piece is up |
| Piece | `Broken` | True while hidden |

## Config fields

`Content.Breakables.Definitions.Board`:

| Field | Board value | Meaning |
| --- | --- | --- |
| `Id` | `"Board"` | Unique key |
| `Tags` | `{ "Board", "board" }` | CollectionService tags that place this type |
| `Model` | `"Board"` | Model in `Assets.Models` |
| `Pieces` | Plank (60 HP each), then Spraypaint (25 HP) | Groups in placing order. Each has `Kind`, `Folder` (optional), `Name` or `Pattern`, and `Health` |
| `CarryOverflow` | `true` | Leftover damage goes on to the next piece |
| `SourceMultipliers` | `{ Explosion = 1.5 }` | Damage multiplier by source |
| `Repair.Enabled` | `true` | Show the repair prompt |
| `Repair.HoldDuration` | `0.5` | Seconds to hold Interact per piece |
| `Repair.Cooldown` | `0.35` | Seconds between two repairs by the same player (server) |
| `Repair.MaxDistance` | `9` | Prompt range in studs. The server allows 3 more |
| `Repair.ObjectText` | `"Board"` | Prompt title; shows as `Board 3/6` |
| `Repair.ActionText` | `Plank = "Place plank"`, `Spraypaint = "Spray paint"` | Prompt action, by the next piece's Kind |
| `Effects.Break`, `Effects.Place` | `"BoardBreak"`, `"BoardPlace"` | Effects played for each piece, with `Variant` = the piece's Kind |

With these numbers a full board takes 325 damage: about 15 rifle bullets, 4 shotgun blasts at close range, or 12 pistol shots.

## Damage API (for any weapon)

All on `Systems.Breakables.BreakableService` (server). Every function takes **any part of a breakable** (or its model), so a weapon passes whatever it hit:

```lua
local BreakableService = require(ServerScriptService.Modules.Systems.Breakables.BreakableService)

-- Damage: returns the damage dealt; 0 if the part is not a breakable, the board is already broken, or it was refused
BreakableService.Damage(target: Instance, amount: number, attacker: (Player | Model)?, source: string?): number

-- Area damage, less toward the edge (25% at the edge). ignore skips the breakable that part belongs to
BreakableService.DamageRadius(position, radius, amount, attacker?, source?, ignore?): number

BreakableService.IsBreakable(target): boolean
BreakableService.Get(target): { Model, Type, Intact, Total, Health }?
BreakableService.Repair(target, player?, expectedPiece?): (boolean, reason?)
BreakableService.Reset(target)   -- every piece back, no effects (round start)
```

A gun melee ("gun punch") calls it with the part its hit found:

```lua
if BreakableService.IsBreakable(hitPart) then
	BreakableService.Damage(hitPart, MELEE_DAMAGE, player, "Melee")
end
```

Source names used so far: `"Bullet"` (every gun bullet) and `"Explosion"` (explosive rounds). A source name in a type's `SourceMultipliers` scales its damage.

Extension points (`Shared.Extensions`), where `who` is the Player, an NPC model or nil:

| Point | Kind | Arguments |
| --- | --- | --- |
| `Breakable.PreventDamage` | Any | who, model, amount, source |
| `Breakable.DamageMultiplier` | Product | who, model, source |
| `Breakable.PieceBroken` | Fire | who, model, piece, source |
| `Breakable.Broken` | Fire | who, model, source |
| `Breakable.PreventRepair` | Any | player, model, piece |
| `Breakable.Repaired` | Fire | player, model, piece |

## Adding a breakable type

1. Build the model and put it in `Assets.Models`. Give it a PrimaryPart (the root) and name its pieces so a `Name` or a `Pattern` finds them.
2. Add a file to `Content.Breakables.Definitions` that returns the type. Only `Id`, `Model` and `Pieces` are needed. List the piece groups in **placing** order; damage takes them off in reverse.
3. Add `Break` and `Place` effects to `Content.Effects.Registry`, with a `Variants` entry per piece `Kind` if they should sound different.
4. Tag parts on the map with the type's tag.

Example, a crate with three slats and a lid:

```lua
return {
	Id = "Crate",
	Tags = { "Crate" },
	Model = "Crate",
	Pieces = {
		{ Kind = "Slat", Pattern = "^Slat(%d+)$", Health = 40 },
		{ Kind = "Lid", Name = "Lid", Health = 30 },
	},
	Repair = { Enabled = false },
	Effects = { Break = "BoardBreak", Place = "" },
}
```

No server code changes: guns already damage anything the registry knows.

## Interact key

Prompts use the **Interact** action from `Shared.PlayerSettings` (default E, rebindable in Settings > Controls). `Client.Interact.PromptKeys` sets every ProximityPrompt in the workspace to that key, and to the fixed gamepad button DPad Up (`PlayerSettings.InteractGamepadKey`). It updates them when the key is rebound. Touch players tap the prompt. A prompt with the attribute `FixedKey = true` keeps its own key. Interact bound to a mouse button cannot drive a prompt, so prompts then use E.

## Limits

- The map's older window models named `Board` / `Board1` / `DoorBoard` are not tagged, so the system ignores them. Only parts tagged `Board` become breakable boards.
- No lag compensation, the same as the guns.
- Board state is not saved, and boards are not reset by anything yet. Call `BreakableService.Reset` from a round system.
