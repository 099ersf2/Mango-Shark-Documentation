# Classes

In Siege every player picks a class: a default loadout, the guns they may swap to, and one ability. A class can be held by one player per team, so each team has five. Built 2026-11-11. See [SIEGE.md](SIEGE.md) for the mode.

## Where things are

| What | Where |
| --- | --- |
| Every class and every number | `ReplicatedStorage.Content.Classes` |
| Assignment, loadouts, charges, cooldowns, every ability check | `ServerScriptService.Modules.Systems.Classes.ClassService` |
| One module per ability | `Systems.Classes.Abilities.<AbilityId>` |
| Shared gadget code (aim, place, blast, enemies) | `Systems.Classes.Gadgets` |
| Gadget models | `ReplicatedStorage.Assets.Models.Siege` (`BreachCharge`, `TrapMine`, `HealingStation`, `GadgetCamera`, `Flashbang`) |
| Effects | `GadgetPlace`, `GadgetDestroyed`, `Flashbang`, `AbilityPulse` in `Content.Effects.Registry` (placeholder sounds) |
| Class pick UI | `Client.Core.SiegeSelect` → `StarterGui.SiegeSelect` |
| Ability HUD | `Client.Hud.SiegeHud` → `Main.SiegeHUD.Ability`, `Main.Mobile.AbilityButton` |
| Packets | `Packets.Class.Use`, `Class.State`, `Class.Flash` |

## The classes

### Attackers

| Class | Guns (default; may swap to) | Ability | Charges, cooldown | What it does |
| --- | --- | --- | --- | --- |
| **Breacher** | Shotgun, Pistol (Shotgun or SMG) | Breach Charge | 2, 6 s | Sticks to the surface you look at (9 studs). After 2.5 s it blows: boards within 9 studs take 400, a soft wall gets a 4.5 stud hole, humanoids within 7 studs take up to 70. A defender can shoot it off first (15 health) |
| **Flash Specialist** | SMG, Pistol (SMG or Rifle) | Flashbang | 3, 8 s | Thrown; pops after 1.4 s. Anyone within 30 studs with a clear line is blinded: 3.5 s close and facing it, 0.6 s at the edge or facing away. Your own team gets half |
| **Recon** | Rifle, Pistol (Rifle or SMG) | Recon Pulse | 2, 20 s | Marks where every defender within 45 studs stands, for the team, for 10 s. The marks don't follow, and don't reveal classes |
| **Drone Operator** | BurstRifle, Pistol (Rifle or LMG) | Drone Shield | 2, 25 s | Your drone takes no damage for 8 s. Usable in Prep, from the drone |
| **Smoker** | LMG, Pistol (LMG or Rifle) | Smoke Screen | 3, 12 s | A smoke cloud where you look, up to 40 studs |

### Defenders

| Class | Guns (default; may swap to) | Ability | Charges, cooldown | What it does |
| --- | --- | --- | --- | --- |
| **Warden** | Rifle, Pistol (Rifle or SMG) | Bulletproof Camera | 1, 3 s | A camera on the surface you look at. Every defender can use it. Bullets do nothing to it; a bash or an explosion breaks it (60 health) |
| **Trapper** | Shotgun, Pistol (Shotgun or SMG) | Trap Mine | 2, 4 s | A mine on the surface you look at. Live after 1.5 s; blows when an attacker is within 6 studs: up to 80 within 10 studs. Attackers can shoot it (10 health) |
| **Reinforcement Expert** | LMG, Pistol (LMG or Rifle) | Reinforce | 3, 4 s | Rebuilds the board you look at and reinforces it for the match: it takes 25% damage (50% from explosions) |
| **Medic** | SMG, Pistol (SMG or Shotgun) | Healing Station | 1, 30 s | A station that heals defenders within 12 studs by 8 a second for 25 s. Attackers can destroy it (60 health) |
| **Anchor** | BurstRifle, Revolver (Rifle or LMG) | Stim | 2, 15 s | Heals you 50 at once. Refused at full health |

Sidearm slots may swap between Pistol and Revolver. Defender gadget abilities work in Prep and Action; Stim and the attackers' abilities in Action only (Drone Shield also in Prep).

The spec asked for four classes a side. Each side has five, because a team has up to five players and a class is one per team: Smoker and Anchor are the extras.

## Rules

- **One player per class per team**, first come, first served. `ClassService.Assign` refuses a class a teammate holds.
- **Loadout:** each slot starts as the class's default and may be swapped to any gun in that slot's categories (`Classes.Allows`). Categories are in `Content.Classes.GunCategories`. `ClassService.Arm` gives the guns and the knife; the normal loadout is not given during a match (`Loadout.PreventApply`).
- **A class is never a replicated attribute.** Only its owner is sent `Packets.Class.State`. Other players learn classes through the Siege snapshots their team is allowed ([SIEGE.md](SIEGE.md#scoreboard)).
- **Charges** are per match. **Cooldown** starts after each use.

## Using an ability

Key **T** (the `ClassAbility` action, rebindable), gamepad **DPad Down**, or the touch **ABILITY** button. The client sends server time, the camera position and the look direction (`Packets.Class.Use`); the server answers with whether it worked and a message.

The server refuses unless:

| Check | |
| --- | --- |
| Types | A number and two finite vectors; the look about unit length |
| Clock | The timestamp within 2 s of the server's |
| Rate | At most 4 requests in 2 s |
| Class | The player has one |
| Body | Alive, unless the ability is `Bodiless` and something vouches (`Classes.AllowBodiless`: an attacker in Prep) |
| State | Not in the lobby, not Stunned, not CantDoAnything |
| Charges and cooldown | A charge left, and past the cooldown |
| Game mode | `Classes.PreventAbility` (Siege refuses the wrong phase and dead players) |

The server uses the character's own head as the origin, not the client's position. A use that fails inside the ability ("Aim at a wall") costs no charge.

## Gadgets

A placed gadget is a model in `workspace.SiegeGadgets` with the attributes `Gadget`, `GadgetOwner` and `Team`. One with a Humanoid can be damaged by every weapon through `Combat.ApplyHit`, like a drone; its own team can't hurt it. The Humanoid runs no state machine, so destruction is `HealthChanged` reaching 0. All gadgets are removed when the match ends.

## Extension points

| Point | Kind | Arguments | Use |
| --- | --- | --- | --- |
| `Classes.PreventAbility` | Any | player, classId, ability | Refuse a use |
| `Classes.AllowBodiless` | Any | player, classId | Let a player with no body use a `Bodiless` ability |
| `Classes.CooldownMultiplier` | Product | player, classId, abilityId | Scale the cooldown |
| `Classes.AbilityUsed` | Fire | player, classId, abilityId | After an ability ran |
| `Classes.Assigned` | Fire | player, classId | A player got a class |
| `Classes.GadgetPlaced` / `Classes.GadgetDestroyed` | Fire | player, kind, model / owner?, kind, model, killer? | |
| `Classes.BreachDetonated` | Fire | player, position | |
| `Classes.PreventFlash` / `Classes.FlashTimeMultiplier` / `Classes.Flashed` | Any / Product / Fire | thrower, victim (/ seconds) | |
| `Classes.PreventPulseMark` / `Classes.Pulsed` | Any / Fire | player, target / player, count | |
| `Classes.PreventMineTrigger` / `Classes.MineDetonated` | Any / Fire | owner, victim, model / owner, victim, position | |
| `Classes.HealMultiplier` / `Classes.Healed` | Product / Fire | owner, patient (/ amount) | Healing Station and Stim |

How the abilities reach other systems, without editing them:

| Ability | Through |
| --- | --- |
| Breach Charge | `BreakableService.DamageRadius`, `SoftWalls.Punch` (found by name, in a `pcall`), `Combat.ApplyHit` |
| Drone Shield | `Combat.BlockHit` |
| Smoke Screen | `ConsumableService.Detonate` (found by name, in a `pcall`) |
| Recon Pulse | `DroneService.Mark` |
| Bulletproof Camera | `CameraService.Add`; `Gun.DamageMultiplier` returns 0 for bullets |
| Reinforce | `BreakableService.Reset`, `Breakable.DamageMultiplier` |

## Adding a class

1. Add an entry to `Content.Classes` (Id, Name, Team, Icon, Description, Loadout, Categories, Ability).
2. For a new ability, add a ModuleScript named after `Ability.Id` to `Systems.Classes.Abilities`:

```lua
--!strict
local MyAbility = {}

-- context: Player, Character, Humanoid, Root, Origin (the head), Look (unit), Team, Class, Ability, Tuning
function MyAbility.Use(context: any)
	: (boolean, string?)
	-- return false, "why" to refuse without spending a charge
	return true, nil
end

-- Optional: MyAbility.Reset() runs when a match ends; MyAbility:Start() may add extension handlers
return MyAbility
```

`Icon` is empty for every class for now (the card shows the first letter).

## Tested (2026-11-11 and 2026-11-12, Studio, one player)

| Check | Result |
| --- | --- |
| Class and guns | Picked Trapper with the primary swapped to SMG: spawned with SMG, Pistol, Knife |
| A gun the class doesn't allow | Recon asking for a Shotgun: ignored |
| The other team's class | Ignored |
| Trap Mine | Placed (`GadgetPlaced`, `AbilityUsed`); charges 2 → 1 |
| Cooldown | A second use at once: "Not ready yet." |
| Bad requests | A timestamp 30 s old, and a NaN look: both refused |
| No body | Drone Shield from a player with no body was refused before the `Bodiless` change (the change itself is not re-tested) |
| Unassigned class | With no pick, a random free class was given (Anchor, then Medic) and shown in the HUD |

**Not verified:** every ability's actual effect in play (the breach blast and holes, the flash, the pulse marks, the shield, smoke, the mine going off, healing, reinforcing, the gadget camera), class conflicts between two teammates, and the ability key, gamepad button and touch button with real input.

## Limits

- Reinforce does not slow bullets through a board's planks: the shipped planks are soft walls that break by hole count, a path that doesn't ask `Breakable.DamageMultiplier`. Bashes and explosions are slowed.
- "Facing" a flashbang uses the character's head direction.
- A class's guns can be seen by other clients (see [SIEGE.md](SIEGE.md#limits)).
- Sounds are placeholders made from existing sounds.
