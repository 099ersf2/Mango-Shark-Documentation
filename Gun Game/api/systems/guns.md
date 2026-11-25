# Guns

The server owns ammo, fire rate, spread limits, hits and damage. The client only sends **intent** and plays a cosmetic copy of its own shot at once, so shooting feels instant.

!!! abstract "Source"

    Server: `Systems.Guns.GunService`, `LoadoutService`, `AbilityRunner`, `Systems.Combat.GunMelee`. Shared: `Shared.Guns.Ballistics`, `Spread`, `Abilities`, `Spring`. Client: `Client.Guns.*`. Data: `Content.Guns.*`. Design guides: [Gun system](../../GUN_SYSTEM.md), [Adding guns](../../ADDING_GUNS.md).

```lua
local Guns = game.ServerScriptService.Modules.Systems.Guns
local GunService = require(Guns.GunService)
local LoadoutService = require(Guns.LoadoutService)
```

## A shot, end to end

Straight from the `GunService` header:

1. `Client.Guns.GunController` sends `Packets.Gun.Fire` with a server timestamp, origin, aim direction, **seed** and the spread it used, and plays its own cosmetic shot at once.
2. `GunService.Fire` checks the timestamp, then the shared checks: the held gun, the shooter's state, movement (no shots while sprinting or within the gun's `SprintOutTime` after), `Gun.PreventFire`, the fire rate (a minimum interval plus a TokenBucket per gun) and the ammo. It **clamps the origin to near the head** and checks line of sight to it from the HumanoidRootPart, and clamps the spread to the gun's range.
3. The pellets are **rebuilt from the seed**, so client and server agree on every pellet without sending them. Hitscan guns trace at once; others fly with the gun's FastCast2 caster. Headshots and falloff are worked out here.
4. Every humanoid hit goes through `Combat.ApplyHit` (via `AbilityRunner`) and `Gun.Hit` fires. Board pieces are damaged through `BreakableService`; soft walls get a hole and the bullet carries on with less damage.
5. Nearby clients get the muzzle effect through `EffectService` and a cosmetic copy of the shot through `UnreliablePackets.GunFired`.

**NPCs** fire with `FireAs`, which skips only the client checks (timestamp, origin clamp) and keeps every other rule. Not handled: lag compensation (targets are hit where the server sees them when the shot arrives).

A gun is a **Tool** with a `GunId` attribute; its `Ammo` and `Reserve` attributes are the server's counts. "Who" below is a Player, a character, or an NPC model.

---

## `GunService`

### `GunService.Give(player, gunId) → Tool?`

Gives a gun Tool in the backpack with a full magazine and reserve, in the next free `Slot`. `nil` (and a warning) for an unknown Id.

```lua
local tool = GunService.Give(player, "Revolver")
print(tool and tool:GetAttribute("Ammo"))
```

```lua title="GunService.Give (how the slot is picked)"
local owned = 0
for _, container in { player:FindFirstChildOfClass("Backpack"), player.Character } do
	for _, other in if container then container:GetChildren() else {} do
		if other:IsA("Tool") and other:GetAttribute("GunId") then
			owned += 1
		end
	end
end
tool:SetAttribute("Slot", owned + 1)
```

### `GunService.GiveNPC(model, gunId)`

Arms an NPC model (equipped). It then shoots through the same path as players.

```lua
GunService.GiveNPC(npcModel, "SiegeSMG")
```

### `GunService.ShooterOf(who) → Shooter?`

`{ Character, Player, Id }` for `FireAs` / `ReloadAs`. An NPC gets a unique negative `Id` for its life (and an `NPCId` attribute so clients can match its shots). `nil` for a player with no character.

```lua
local shooter = GunService.ShooterOf(npcModel)
print(shooter.Id) -- e.g. -3
```

### `GunService.GetHeld(who) → Held?`

The gun a player or NPC is holding (its definition in `.Gun`, its Tool in `.Tool`), or `nil`.

```lua
local held = GunService.GetHeld(player)
if held then
	print(held.Gun.Id, held.Tool:GetAttribute("Ammo"))
end
```

### `GunService.Fire(player, timestamp, origin, direction, seed, spread)`

A player's trigger pull, with every check. This is what `Packets.Gun.Fire` calls; you rarely call it yourself.

```lua
Packets.Gun.Fire.OnServerEvent:Connect(GunService.Fire)
```

### `GunService.FireAs(shooter, origin, direction, seed, spread)`

Fires for any shooter, skipping only the client checks. Fire rate, ammo, reloads, state and `Gun.PreventFire` still apply. How NPCs and the gun range shoot.

```lua
local shooter = GunService.ShooterOf(npcModel)
local head = npcModel.Head.Position
GunService.FireAs(shooter, head, (target.Position - head).Unit, math.random(1, 2^31), 1.5)
```

### `GunService.Reload(player)` / `GunService.ReloadAs(shooter)`

Starts a reload (player request / any shooter).

```lua
GunService.ReloadAs(GunService.ShooterOf(npcModel))
```

### `GunService.CancelReload(who) → boolean`

Stops a reload in progress; the magazine keeps what it had and the reserve is untouched. `true` if one was running. The gun bash uses this.

```lua
if GunService.CancelReload(player) then
	print("reload cancelled")
end
```

### `GunService.RemoveShooter(model)`

Forgets an NPC's gun state (NPCService does this when an NPC dies).

```lua
humanoid.HealthChanged:Connect(function(health)
	if health <= 0 then GunService.RemoveShooter(npcModel) end
end)
```

---

## `LoadoutService`

### `LoadoutService.Arm(player, guns) → boolean`

**Replaces** a living player's guns with exactly these (by slot, up to `Loadouts.MAX_SLOTS`; `"None"` skips a slot), adds the knife in the next slot, applies their skins, and equips slot 1. `false` if they have no living character.

```lua
LoadoutService.Arm(player, { "AssaultRifle", "SiegePistol" }) -- slot 1, slot 2, knife in slot 3
LoadoutService.Arm(player, { "None", "Revolver" })            -- sidearm only
```

### `LoadoutService.Apply(player)`

Gives the player's saved loadout, or takes their guns away while `InLobby`. Skipped when a `Loadout.PreventApply` handler says so (Siege does, and arms classes itself).

```lua
LoadoutService.Apply(player)
```

`GunService.Give` **adds** one gun; `LoadoutService.Arm` **sets** the whole loadout. In Siege, `ClassService.Arm` calls `LoadoutService.Arm` with the class's guns.

---

## Defining a gun

One ModuleScript per gun in `Content.Guns.Definitions`; leave a field out to use its default (`Content.Guns.Registry` fills them in). A real one:

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

Read any gun with defaults filled in:

```lua
local Registry = require(game.ReplicatedStorage.Content.Guns.Registry)
print(Registry.AssaultRifle.Damage, Registry.AssaultRifle.MagSize)
```

Every field is explained in [Adding guns](../../ADDING_GUNS.md). The model's Handle needs `Muzzle`, `Aim`, `RightGrip` and `LeftGrip` attachments; check new guns with the `range` command.

---

## Gun abilities and `AbilityRunner`

`Content.Guns.Abilities.*` are hook tables a gun lists in `Abilities`: `ModifyStats`, `OnFire`, `OnHit`, `CanPierce`, `OnAltFire`, `OnEquip`, `OnUnequip`, `OnReload`. Shipped (one module each in the folder): Scope, Ricochet, Burst, ExplosiveRounds, PumpShotgunSpread, SawedOffShotgun and the rest of `Content.Guns.Abilities`. The server runs them through `AbilityRunner`; abilities normally reach these through the `ctx` they're given.

### `AbilityRunner.ApplyHit(ctx, humanoid, damage, headshot?)`

Ability damage with kill credit, hitmarker and `Gun.Killed`.

```lua
-- Inside an ability's OnHit (server):
AbilityRunner.ApplyHit(ctx, humanoid, 20, false)
```

### `AbilityRunner.Hit(ctx, hit, bullet, deal?)`

The normal bullet-hit path (falloff, headshots, soft walls, boards) for an extra bullet an ability makes (Ricochet does this).

```lua
AbilityRunner.Hit(ctx, bounceResult, bullet)
```

### `AbilityRunner.PlayEffect(name, options?)`

An effect for everyone.

```lua
AbilityRunner.PlayEffect("Explosion", { Position = hitPosition })
```

### `AbilityRunner.Equip(ctx)` / `Unequip(ctx)` / `Reload(ctx)` / `AltFire(ctx, active, source)`

Run the matching hooks of every ability on the gun. `source` is `"Aim"` or `"Ability"`. Called by `GunService`.

See [Gun abilities](../../EXAMPLES.md#gun-abilities) for a full worked ability.

---

## Gun bash: `GunMelee`

### `GunMelee.Swing(player, timestamp, direction)`

A player's bash with every check (what `Packets.Melee.Swing` calls). Cancels a reload.

```lua
Packets.Melee.Swing.OnServerEvent:Connect(GunMelee.Swing)
```

### `GunMelee.SwingAs(who, direction)`

A bash for anyone, skipping the client checks (NPCs).

```lua
GunMelee.SwingAs(npcModel, npcModel.HumanoidRootPart.CFrame.LookVector)
```

### `GunMelee.Query(character, origin, direction, settings)`

What a bash would hit, without hitting it.

```lua
local Melee = require(game.ReplicatedStorage.Content.Guns.Melee)
local result = GunMelee.Query(character, head.Position, look, Melee.For("AssaultRifle"))
```

---

## Shared gun math (`Shared.Guns.*`)

### `Ballistics.Falloff(gun, distance) → number`

The damage multiplier at a distance (1 up to `Falloff.Start`, down to `Falloff.Min` at `Falloff.End`).

```lua
local damage = gun.Damage * Ballistics.Falloff(gun, (hit - origin).Magnitude)
```

### `Ballistics.IsHeadshot(part)` / `HumanoidOf(part)` / `IsSoftWall(part)` / `PlayerFromId(userId)`

```lua
local humanoid = Ballistics.HumanoidOf(result.Instance)
local headshot = Ballistics.IsHeadshot(result.Instance)
```

### `Ballistics.NewShot(...)`, `Prepare(ctx, out)`, `Fire(ctx, origin, direction, index, onHit)`, `Trace(...)`, `Caster(gun)`, `Filter(ctx)`, `Hit(result, origin)`

The shot pipeline: build a shot context, rebuild pellet directions from the seed, fly or trace each one. `GunService` and `GunController` use these; you'd only touch them to change how bullets work.

### `Spread.Angle(gun, aiming, moveAlpha, bloom, stance?) → number`

The spread cone in degrees. `stance` is `MovementController.Stance()` on the client.

```lua
local cone = Spread.Angle(gun, true, 0, 0, "Crouch")
```

`Spread.MinAngle`, `Direction`, `Fill` and `Recover` are the rest of the cone math.

### `Spring.new(speed, damper)` → `:Update(dt)`, `:Impulse(v)`, `:Reset(pos?)`

The spring behind recoil and camera kick.

```lua
local kick = Spring.new(20, 0.6)   -- speed, damper
kick:Impulse(Vector3.new(0, 2, 0)) -- a shot
-- every frame: kick:Update(dt), then read its position for the camera offset
```

### `Abilities.Call(gun, hook, isServer, ...)` / `Any` / `Runs` / `SideOf` / `CanPierce`

Run a gun's ability hooks from shared code.

---

## Extension points

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

```lua
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

-- Revolver headshots do 20% more (return 1 otherwise!)
Extensions.Add("Gun.DamageMultiplier", function(who, gunId, humanoid, hit)
	return if gunId == "Revolver" and hit and hit.Name == "Head" then 1.2 else 1
end)

-- Count headshot kills
Extensions.Add("Gun.Killed", function(who, victim, gunId, headshot)
	if headshot and typeof(who) == "Instance" and who:IsA("Player") then
		QuestService.Add(who, "Headshots")
	end
end)
```

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

---

## Client modules

```lua
local ClientGuns = game.ReplicatedStorage.Modules.Client.Guns
local Viewmodel = require(ClientGuns.Viewmodel)
local GunHud = require(ClientGuns.GunHud)
local WeaponSlots = require(ClientGuns.WeaponSlots)
```

### `Viewmodel` (first-person gun)

| Function | Does | Example |
| --- | --- | --- |
| `Equip(gun, tool, modelName?, melee?)` / `Unequip()` | Show / hide the first-person gun | `Viewmodel.Equip(Registry.Revolver, tool)` |
| `SetAiming(on)` / `AimAlpha()` | Aim down sights / 0..1 blend | `MovementCamera.SetAim(Viewmodel.AimAlpha())` |
| `SetFov(fov?)` | The viewmodel's own FOV | `Viewmodel.SetFov(70)` |
| `SetHidden(on)` / `IsHidden()` | Hide it (drone and camera views) | `Viewmodel.SetHidden(true)` |
| `IsFirstPerson()` / `Ready()` | In first person / finished equipping | `if not Viewmodel.Ready() then return end` |
| `Muzzle()` | The muzzle attachment | `Effects.Play("GunFire_Rifle", { Parent = Viewmodel.Muzzle() })` |
| `Kick(recoil, rng?, stance?)` | A shot's visual kick | `Viewmodel.Kick(gun.Recoil)` |
| `Inspect()` / `IsInspecting()` | The inspect animation (V) | `Viewmodel.Inspect()` |
| `Bash()` / `IsBashing()` / `Swing(duration?)` | Gun bash / knife swing | `Viewmodel.Bash()` |
| `Reloading()` / `FinishReloading()` | Reload animation start / end | `Viewmodel.Reloading()` |
| `SetSkin()` | Re-apply the equipped skin | `Viewmodel.SetSkin()` |

`Viewmodel.GunModel.*` (`Get`, `ApplySkin`, `SkinOf`, `Bounds`, `Scaled`, `MakeLocal`, `NearPush`) builds the gun model itself.

### `GunHud`

| Function | Does | Example |
| --- | --- | --- |
| `Show(gun)` / `ShowMelee()` / `Hide()` | The gun HUD for a gun / the knife / none | `GunHud.Show(gun)` |
| `SetAmmo(ammo, reserve)` | Ammo text | `GunHud.SetAmmo(tool:GetAttribute("Ammo"), tool:GetAttribute("Reserve"))` |
| `SetReloading(on)` | Reload indicator | `GunHud.SetReloading(true)` |
| `Crosshair(spread, aimAlpha)` | Size the crosshair | `GunHud.Crosshair(cone, Viewmodel.AimAlpha())` |
| `Hitmarker(headshot, killed)` | The hitmarker (from `Gun.HitConfirm`) | `Packets.Gun.HitConfirm.OnClientEvent:Connect(GunHud.Hitmarker)` |
| `SetAimToggle(on)` | Touch: aim button state | `GunHud.SetAimToggle(true)` |
| `MobileButtons()` | The touch Fire, Aim, Reload and Bash buttons | `local buttons = GunHud.MobileButtons()` |

### Others

| Function | Does | Example |
| --- | --- | --- |
| `WeaponSlots.Equip(index)` / `Cycle(step)` | Switch weapon | `WeaponSlots.Equip(2)` |
| `Client.Guns.Consumables.Throw()` / `Pick(id)` | Throw (G) / pick grenade or smoke | `Consumables.Pick("Smoke")` |
| `AimAssist.SetGun(gun?)` / `Update(dt, camera, pitch, yaw, aimAlpha)` | Controller aim assist ([Aim assist](../../AIM_ASSIST.md)) | `AimAssist.SetGun(gun)` |
| `ThirdPersonGuns.Report()` | Each posed character's gun kind and fit ([Third-person guns](../../THIRD_PERSON_GUNS.md)) | `print(ThirdPersonGuns.Report())` |
| `Recoil.ShotKick` / `Scale`, `Recoil.Pattern` / `Camera` / `View` | Recoil math ([Adding guns](../../ADDING_GUNS.md#recoil-fields)) | |

More: [Guns and loadouts](../../EXAMPLES.md#guns-and-loadouts).
