# Consumables (grenade and smoke bomb)

Every player carries one kind of consumable: a **frag grenade** or a **smoke bomb**. They get **2 per life**, and the count refills when they respawn. They pick the kind in the Loadout menu, and the pick is saved.

## Controls

| Input | How |
| --- | --- |
| Keyboard | **G** (the rebindable `Consumable` action, "Throw grenade / smoke" in Settings > Controls) |
| Gamepad | **DPad Right** (fixed, `PlayerSettings.ConsumableGamepadKey`) |
| Touch | The **NADE / SMOKE** button (`Main.Mobile.ConsumableButton`), left of BASH; it shows the count |

A throw works with any weapon held, or none. It's refused in the lobby, while a menu is open, while `Stunned` or `CantDoAnything`, with none left, and within 0.8 s of the last throw.

## The two kinds

| | Frag grenade (`Grenade`) | Smoke bomb (`Smoke`) |
| --- | --- | --- |
| Throw | 70 studs/s along the look, plus 12 up | 65 studs/s, plus 10 up |
| Goes off | 3 s after the throw | 1.5 s after the throw |
| Landing | Heavy, barely bounces (`Bounce` 0.08); keeps half its speed on landing, then rolls about 2–4 studs to a stop | Same (`Bounce` 0.1) |
| Effect | Blast of 16 studs: 120 damage at the center, falling to 15% at the edge, with knockback | A cloud of 13 studs for 15 s |
| Thrower | Takes half damage from their own grenade | — |
| Cover | Only humanoids in clear view of the blast are hit | Blocks NPC sight and aim assist through its core; bullets still pass |
| World | Boards take 350 (`"Explosion"` source, 1.5× on boards): a blast 4 studs away strips a whole board. Up to 6 soft walls within 10 studs each get a 3.5-stud hole | — |
| Kill feed | Item "Frag grenade", thrower credited; hits give the thrower a hitmarker | — |

## Where things are

| What | Where |
| --- | --- |
| The definitions and every number | `ReplicatedStorage.Content.Consumables` (tagged `ScribeFragment`: saves the `Consumable` field) |
| Server: count, throw, blast, smoke | `ServerScriptService.Modules.Systems.Consumables.ConsumableService` |
| Client: input, HUD, button, picker | `ReplicatedStorage.Modules.Client.Guns.Consumables` (`ClientOnly`) |
| Smoke sight check | `ReplicatedStorage.Modules.Shared.Smoke` (`Smoke.Blocks(from, to)`) |
| Thrown models | `ReplicatedStorage.Assets.Models.Consumables.Grenade` / `SmokeBomb` (single parts, built in Studio) |
| Smoke particles | `ReplicatedStorage.Assets.Vfx.SmokeCloud` (emitters `Core` and `Haze`) |
| Effects | `Explosion` (the blast), `SmokePop`, `ConsumableThrow` in `Content.Effects.Registry` |
| Packets | `Packets.Consumable.Throw(serverTime, lookDirection)` and `Packets.Consumable.Pick(id)` |
| HUD | `Main.Consumable` (`ItemName`, `Count`), above the ammo box; hidden on touch, where the button shows the count |
| Picker | `Main.Loadout.Body.Consumables` (`Options.Grenade`, `Options.Smoke`), above the loadout cards |

## How a throw works

1. **Client** (`Client.Guns.Consumables.Throw`) checks the count, the lobby, menus and the cooldown, sends `Packets.Consumable.Throw` and plays the whoosh at once.
2. **Server** (`ConsumableService.Throw`) checks again: the timestamp (±2 s), alive, not in the lobby, not stunned, one left, 80% of the cooldown passed, and `Consumable.PreventThrow`.
3. It takes one off `ConsumableCount` and clones the model 1.5 studs ahead of the head (closer if a wall is right in front). The part goes in the `Thrown` collision group, so it never hits players, and is owned by the server. It launches with the throw speed plus half the thrower's own velocity. It's heavy and barely bounces. On its first landing it keeps `LandingKeep` (0.5) of its sideways speed and spin, then `RollDrag` (1.8) slows it to a stop, so it stays near where it lands.
4. After the fuse, `ConsumableService.Detonate` runs where the part lies. One that fell out of the world does nothing.

The projectile is server-made, so other players see the same throw, and the thrower sees it after their ping.

## Count and death reset

The server keeps two **player attributes**: `ConsumableId` (the kind) and `ConsumableCount` (left this life).

- **On every spawn** `ConsumableService.Refill` sets the count back to 2 and the kind to the saved pick. So dying resets the count.
- **Picking a new kind** changes it right away but keeps the count, so switching never refills.

## Smoke and sight

A cloud is an anchored, invisible part named `SmokeCloud` in `workspace.Thrown`, tagged `SmokeCloud`, with a `Radius` attribute and the particle emitters. `Shared.Smoke.Blocks(from, to)` is true when the line passes within 85% of a cloud's radius of its center.

- **NPCs:** `Systems.NPC.Brain.CanSee` returns false through smoke, so NPCs lose sight of you.
- **Aim assist:** `Client.Guns.AimAssist` ignores targets behind smoke.
- **Players:** only the particles hide you.

The emitters stop 6 s before the end so the cloud thins out. The tag comes off at 15 s, and the part is removed 4 s later.

## API

```lua
local ConsumableService = require(game.ServerScriptService.Modules.Systems.Consumables.ConsumableService)

ConsumableService.Get(player)                     -- consumable definition (or nil), count left
ConsumableService.Refill(player)                  -- back to 2 with the saved kind (yields until data loads)
ConsumableService.SetCount(player, 5)             -- clamped to 0..PER_LIFE
ConsumableService.Throw(player, direction)        -- every check, then a throw; returns the part or nil
ConsumableService.Detonate("Grenade", position, player?)   -- a blast or a cloud right there, no throw
```

Client (`Client.Guns.Consumables`): `Throw()` and `Pick(id)`.

**Extension points** (`Shared.Extensions`):

| Point | Kind | Arguments | Use |
| --- | --- | --- | --- |
| `Consumable.PreventThrow` | Any | player, id | Stop a throw |
| `Consumable.DamageMultiplier` | Product | attacker?, id, humanoid | Scale grenade damage (friendly fire, perks) |
| `Consumable.Thrown` | Fire | player, id, projectile | After a throw |
| `Consumable.Detonated` | Fire | attacker?, id, position | After a blast or a smoke pop |

## Adding a consumable

1. Add an entry to `LIST` in `Content.Consumables` with a new `Id`, a `Kind` (`"Grenade"` or `"Smoke"`) and its numbers. `Bounce`, `LandingKeep` and `RollDrag` set how it lands and rolls.
2. Add its model (one part) to `Assets.Models.Consumables`, named as `Model`.
3. Add a TextButton named after the Id to `Main.Loadout.Body.Consumables.Options` (copy one of the two).

A new kind of behavior (a flashbang, say) needs a branch in `ConsumableService.Detonate`.

## Testing

Checked in a Studio playtest on 2026-11-10:

- **Spawn:** `Grenade` ×2 on spawn, HUD "Frag grenade [G]  x2", button "NADE 2".
- **Grenade throw:** the throw landed on the floor and the count went to 1.
- **Blast:** a dummy 4 studs away dropped to 7 health and one 13 studs away to 63. The thrower, about 10 studs from their own grenade, lost 12.
- **Smoke:** picking it switched the kind with the count kept at 1. The throw used the last one, the HUD read x0, and the cloud blocked a line through it but not one 20 studs to the side.
- **Death:** the count went from 0 back to 2, and the pick stayed Smoke.
- **G key:** bound (G and DPad Right). Studio's input tool couldn't deliver key presses to the game, so it hasn't been pressed by hand yet.

Retuned on 2026-11-10 (it rolled like a light ball, and walls barely broke):

- **Roll:** with the old settings it rolled far. Now: landing keep 0.3 / drag 3 rolled 0.5–1.3 studs (too little); 0.45 / 2 rolled 1.1–2.7; 0.55 / 1.6 rolled 4.5–5.3. Set to 0.5 / 1.8 in between, about 2–4 studs.
- **Boards:** a blast 4 studs from a 6-piece board took off 2 pieces with the old 80 damage, and all 6 with 350.
- **Soft walls:** a blast 2 studs from a wall removed 2.0 cubic studs of wall with the old 1.6-stud hole, and 9.0 with the new 3.5-stud hole.

Not yet tried: a real phone or gamepad, against real NPCs, or with other players.

## Limits

- No cooking (holding to shorten the fuse) and no throw animation on the viewmodel.
- No bounce sound.
- No team rule: grenades hurt everyone in range. Use `Consumable.DamageMultiplier` for friendly fire.
