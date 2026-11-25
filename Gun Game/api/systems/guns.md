# Guns

The server owns ammo, fire rate, spread limits, hits and damage. The client only sends **intent** and plays a cosmetic copy of its own shot at once, so shooting feels instant.

!!! abstract "Source"

    Server: `Systems.Guns.GunService`, `LoadoutService`, `AbilityRunner`, `Systems.Combat.GunMelee`. Shared: `Shared.Guns.Ballistics`, `Spread`, `Abilities`, `Spring`. Client: `Client.Guns.*`. Data: `Content.Guns.*`. Design guides: [Gun system](../../GUN_SYSTEM.md), [Adding guns](../../ADDING_GUNS.md).

## A shot, end to end

Straight from the `GunService` header:

1. `Client.Guns.GunController` sends `Packets.Gun.Fire` with a server timestamp, origin, aim direction, **seed** and the spread it used, and plays its own cosmetic shot at once.
2. `GunService.Fire` checks the timestamp, then the shared checks: the held gun, the shooter's state, movement (no shots while sprinting or within the gun's `SprintOutTime` after), `Gun.PreventFire`, the fire rate (a minimum interval plus a TokenBucket per gun) and the ammo. It **clamps the origin to near the head** and checks line of sight to it from the HumanoidRootPart, and clamps the spread to the gun's range.
3. The pellets are **rebuilt from the seed**, so client and server agree on every pellet without sending them. Hitscan guns trace at once; others fly with the gun's FastCast2 caster. Headshots and falloff are worked out here.
4. Every humanoid hit goes through `Combat.ApplyHit` (via `AbilityRunner`) and `Gun.Hit` fires. Board pieces are damaged through `BreakableService`; soft walls get a hole and the bullet carries on with less damage.
5. Nearby clients get the muzzle effect through `EffectService` and a cosmetic copy of the shot through `UnreliablePackets.GunFired`.

**NPCs** fire with `FireAs`, which skips only the client checks (timestamp, origin clamp) and keeps every other rule.

!!! note "Not handled: lag compensation"

    Targets are hit where the server sees them when the shot arrives.

## `GunService` API

A gun is a **Tool** with a `GunId` attribute; its `Ammo` and `Reserve` attributes are the server's counts. "Who" is a Player, a character, or an NPC model.

| Function | Returns / does |
| --- | --- |
| `GunService.Give(player, gunId)` | The Tool (in the backpack, full ammo, next free `Slot`), or `nil` and a warning |
| `GunService.GiveNPC(model, gunId)` | Arms an NPC; it shoots through the same path |
| `GunService.ShooterOf(who)` | `{ Character, Player, Id }`. An NPC gets a unique negative `Id` and an `NPCId` attribute |
| `GunService.GetHeld(who)` | The held gun's state, or `nil` |
| `GunService.Fire(player, timestamp, origin, direction, seed, spread)` | A player's trigger pull (what `Packets.Gun.Fire` calls) |
| `GunService.FireAs(shooter, origin, direction, seed, spread)` | Fire for any shooter, skipping client checks |
| `GunService.Reload(player)` / `ReloadAs(shooter)` | Start a reload |
| `GunService.CancelReload(who)` | `true` if a reload was cancelled (the magazine keeps what it had) |
| `GunService.RemoveShooter(model)` | Forget an NPC's gun state when it dies |

```lua title="Systems.Guns.GunService.Give"
function GunService.Give(player: Player, gunId: string): Tool?
	local gun = Registry[gunId]
	local tool = gun and makeTool(gun)
	if not tool then
		warn(`GunService.Give: no gun named {gunId}`)
		return nil
	end
	-- The next free weapon slot; LoadoutService sets its own. Client.Guns.WeaponSlots switches by it
	local owned = 0
	for _, container in { player:FindFirstChildOfClass("Backpack"), player.Character } do
		for _, other in if container then container:GetChildren() else {} do
			if other:IsA("Tool") and other:GetAttribute("GunId") then
				owned += 1
			end
		end
	end
	tool:SetAttribute("Slot", owned + 1)
	tool.Parent = player:FindFirstChildOfClass("Backpack") or player.Character
	return tool
end
```

## Loadouts: `LoadoutService`

| Function | What it does |
| --- | --- |
| `LoadoutService.Arm(player, guns)` | **Replaces** a living player's guns with exactly these (by slot, up to `Loadouts.MAX_SLOTS`; `"None"` skips a slot), adds the knife in the next slot, applies skins, equips slot 1. `true` if armed |
| `LoadoutService.Apply(player)` | Gives their saved loadout, or takes guns away in the lobby. Skipped if `Loadout.PreventApply` says so |

Use `GunService.Give` to **add** one gun; use `LoadoutService.Arm` to **set** the whole loadout. In Siege, `ClassService.Arm` calls `LoadoutService.Arm` with the class's guns.

## Defining a gun

One ModuleScript per gun in `Content.Guns.Definitions`. Leave a field out to use its default (`Content.Guns.Registry` fills them in). A real one:

```lua title="Content.Guns.Definitions.SiegePistol"
return {
	Id = "SiegePistol",
	DisplayName = "TacticalPistol",
	Model = "SiegePistol",
	FireMode = "Semi",
	FireRate = 400,                -- rounds per minute
	Damage = 38,
	HeadshotMultiplier = 5,
	Falloff = { Start = 40, End = 110, Min = 0.5 },
	MagSize = 15,
	ReserveAmmo = 75,
	ReloadTime = 1.6,
	SprintOutTime = 0.1,           -- no shots this long after sprinting
	MoveSpeedMultiplier = 1.05,
	EquipTime = 0.25,
	Projectile = { CastType = "Raycast", Speed = 700, Gravity = 0, MaxDistance = 600, Pierce = 0, Hitscan = false },
	Spread = { Hip = 1.5, ADS = 0.3, Move = 1, PerShot = 0.6, Recovery = 8, Max = 6 },
	Recoil = { Vertical = 2.4, Horizontal = 0.35, FirstShot = 1, ResetTime = 0.3, MaxClimb = 12, --[[ ... ]] },
	Viewmodel = { Offset = CFrame.new(0.55, -1.35, -2.6), Sway = 1.2, Bob = 1 },
	Effects = { Fire = "GunFire_Pistol", Tracer = "Tracer" },
	Abilities = {},
}
```

Every field is explained in [Adding guns](../../ADDING_GUNS.md). The model's Handle needs `Muzzle`, `Aim`, `RightGrip` and `LeftGrip` attachments; check new guns with the `range` command.

## Gun abilities

`Content.Guns.Abilities.*` are hook tables a gun lists in `Abilities`: `ModifyStats`, `OnFire`, `OnHit`, `CanPierce`, `OnAltFire`, `OnEquip`, `OnUnequip`, `OnReload`. Shipped: Scope, Ricochet, Burst, ExplosiveRounds, PumpShotgunSpread, SiegeShotgunSpread. The server runs them through `AbilityRunner`:

| Function | What it does |
| --- | --- |
| `AbilityRunner.ApplyHit(ctx, humanoid, damage, headshot?)` | Ability damage with credit, hitmarker and `Gun.Killed` |
| `AbilityRunner.Hit(ctx, hit, bullet, deal?)` | The normal bullet-hit path (falloff, headshots, soft walls, boards) |
| `AbilityRunner.PlayEffect(name, options?)` | An effect for everyone |
| `AbilityRunner.Equip` / `Unequip` / `Reload(ctx)`, `AltFire(ctx, active, source)` | Run the matching hooks |

See [Gun abilities](../../EXAMPLES.md#gun-abilities) for a full worked ability.

## Gun bash: `GunMelee`

| Function | What it does |
| --- | --- |
| `GunMelee.Swing(player, timestamp, direction)` | A player's bash with every check (what `Packets.Melee.Swing` calls). Cancels a reload |
| `GunMelee.SwingAs(who, direction)` | A bash for anyone, skipping client checks |
| `GunMelee.Query(character, origin, direction, settings)` | What a bash would hit, without hitting it |

## Shared gun math (`Shared.Guns.*`)

| Function | What it does |
| --- | --- |
| `Ballistics.NewShot(...)`, `Prepare`, `Fire`, `Trace` | Build a shot context; pellet directions; simulated bullets; hitscan |
| `Ballistics.Falloff(gun, distance)` | Damage multiplier at a distance |
| `Ballistics.IsHeadshot(part)` / `HumanoidOf(part)` / `IsSoftWall(part)` | Hit helpers |
| `Spread.Angle(gun, aiming, moveAlpha, bloom, stance?)` | The spread cone |
| `Spring.new(speed, damper)` → `:Update(dt)`, `:Impulse(v)`, `:Reset(pos?)` | The spring behind recoil and camera |

## Extension points

"who" is the Player, or the NPC's model.

| Point | Kind | Arguments |
| --- | --- | --- |
| `Gun.PreventFire` | Any | who, gunId, tool |
| `Gun.DamageMultiplier` | Product | who, gunId, humanoid, hit (`nil` for ability damage) |
| `Gun.Hit` | Fire | who, humanoid, hit, gunId |
| `Gun.Killed` | Fire | who, victimHumanoid, gunId, headshot |
| `Gun.Reloaded` | Fire | who, tool, gunId |
| `Gun.Fired` | Fire | who, gunId, origin (NPCs hear shots through it) |
| `Gun.PreventMelee` | Any | who, gunId, tool |
| `Gun.MeleeHit` | Fire | who, kind (`Humanoid`/`Breakable`/`SoftWall`/`Surface`), instance, humanoid?, gunId |
| `Loadout.PreventApply` | Any | player |

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Gun.Fire` | Client → server | server time, origin, direction, seed, spread |
| `Gun.Reload` / `Gun.Aim` / `Gun.AltFire` | Client → server | — / aiming / pressed |
| `Gun.HitConfirm` | Server → shooter | headshot, killed |
| `Gun.Loadout` | Client → server | loadout Id |
| `Melee.Swing` | Client → server | server time, look |
| `UnreliablePackets.GunFired` | Server → nearby | UserId, gunId, origin, direction, seed, spread |

Ammo and reload state are **attributes** (`Tool.Ammo`, `Tool.Reserve`, `Tool.Reloading`, `Player.Reloading`), not packets.

## Client modules

| Module | Key functions |
| --- | --- |
| `Viewmodel` | `Equip(gun, tool, modelName?, melee?)`, `Unequip()`, `SetAiming(bool)`, `AimAlpha()`, `SetFov(fov?)`, `Kick(recoil, rng?, stance?)`, `Inspect()`, `Bash()`, `SetSkin()` |
| `GunHud` | `Show(gun)`, `Hide()`, `SetAmmo(ammo, reserve)`, `Crosshair(spread, aimAlpha)`, `Hitmarker(headshot, killed)`, `MobileButtons()` |
| `WeaponSlots` | `Equip(index)`, `Cycle(step)` |
| `Consumables` | `Throw()`, `Pick(id)` |
| `AimAssist` | `SetGun(gun?)`, `Update(dt, camera, turnPitch, turnYaw, aimAlpha)`: see [Aim assist](../../AIM_ASSIST.md) |
| `ThirdPersonGuns` | Poses every character's gun; `Report()` for checking ([Third-person guns](../../THIRD_PERSON_GUNS.md)) |

## Example

```lua
local Guns = game.ServerScriptService.Modules.Systems.Guns
local GunService = require(Guns.GunService)
local LoadoutService = require(Guns.LoadoutService)
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

GunService.Give(player, "Revolver")                     -- add one gun
LoadoutService.Arm(player, { "SiegeCarbine", "SiegePistol" }) -- exactly these + knife

-- Headshot bonus for one gun (always return 1 otherwise)
Extensions.Add("Gun.DamageMultiplier", function(who, gunId, humanoid, hit)
	return if gunId == "Revolver" and hit and hit.Name == "Head" then 1.2 else 1
end)
```

More: [Guns and loadouts](../../EXAMPLES.md#guns-and-loadouts).
