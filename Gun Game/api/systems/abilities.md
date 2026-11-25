# Class abilities

Every ability in `Systems.Classes.Abilities`, what it does, the tuning it reads, and how to hook into it. Each module has `Use(context) → (ok, message?)` and is called by [`ClassService.Use`](classes.md#what-use-checks-in-order) after every check; see [Classes and abilities](classes.md) for the context and for writing a new one.

!!! abstract "Source"

    `ServerScriptService.Modules.Systems.Classes.Abilities.*`, data in `Content.Classes.Definitions.*` (each class's `Ability.Tuning`).

## Which class has which ability

| Class file | Team | Ability module |
| --- | --- | --- |
| `Breacher` | Attackers | [`BreachCharge`](#breachcharge) |
| `Flash` (Luca) | Attackers | [`Flashbang`](#flashbang) |
| `Recon` | Attackers | [`ReconPulse`](#reconpulse) |
| `Operator` | Attackers | [`DroneShield`](#droneshield) |
| `Smoker` | Attackers | [`SmokeScreen`](#smokescreen) |
| `Sheild` | Attackers | [`Shield`](#shield) |
| `Hacker` (Caleb) | Attackers | [`Hacker`](#hacker-dead-call) |
| `Motion_Scanner` (Leo) | Attackers | [`Motion Scanner`](#motion-scanner) |
| `Fin` | Attackers | [`StoneBarrier`](#stonebarrier) |
| `Trapper` | Defenders | [`TrapMine`](#trapmine) |
| `Ironwall` | Defenders | [`Reinforce`](#reinforce) |
| `Medic` | Defenders | [`HealingStation`](#healingstation) |
| `Anchor` | Defenders | [`Stim`](#stim) |
| `BulletproofCamera` (Warden) | Defenders | [`BulletproofCamera`](#bulletproofcamera) |
| `Proximity Sensor` | Defenders | [`ProximitySensor`](#proximitysensor) |
| `lasors` | Defenders | [`Laser`](#laser) |
| `Hologram` | Defenders | [`Hologram`](#hologram) |
| `C4` | Defenders | [`C4`](#c4) |

!!! tip "Calling an ability from your own code"

    Don't call `Ability.Use` directly: go through `ClassService.Use(player, workspace:GetServerTimeNow(), head.Position, look)` so charges, cooldowns and every check apply. To change an ability's numbers, edit its class file's `Tuning`.

---

## Attackers

### BreachCharge

Sticks a charge to the surface the player looks at. After `Fuse` seconds it blows: boards within `BoardRadius` take `BoardDamage` (hatches count one charge), a soft wall it sits on gets a `WallRadius` hole, and humanoids within `BlastRadius` take up to `BlastDamage`. A defender can shoot it off (`Health`) first; then nothing happens. Kill feed item: `"Breach Charge"`.

| Point | Kind | Arguments |
| --- | --- | --- |
| `Classes.BreachDetonated` | Fire | player, position |

```lua
Extensions.Add("Classes.BreachDetonated", function(player, position)
	print(player.Name, "breached at", position)
end)
```

### Flashbang

Throws a flashbang along the look; after `Fuse` it pops. Everyone within `Radius` with a clear line is blinded: `FullTime` up close and facing it, down to `MinTime` at the edge or facing away; the thrower's team gets `SelfShare`. Full walkthrough in [Classes](classes.md#writing-an-ability-the-flashbang-walked-through).

| Point | Kind | Arguments |
| --- | --- | --- |
| `Classes.PreventFlash` | Any | thrower, victim |
| `Classes.FlashTimeMultiplier` | Product | thrower, victim |
| `Classes.Flashed` | Fire | thrower, victim, seconds |

```lua
-- Teammates are never blinded
Extensions.Add("Classes.PreventFlash", function(thrower, victim)
	return thrower:GetAttribute("Team") == victim:GetAttribute("Team")
end)
```

### ReconPulse

Marks where every living enemy within `Radius` stands, for the player's team, for `MarkTime` seconds, using the same static marks as a drone scan (`DroneService.Mark`). Unlike a drone scan it does **not** reveal a defender's class.

| Point | Kind | Arguments |
| --- | --- | --- |
| `Classes.PreventPulseMark` | Any | player, target |
| `Classes.Pulsed` | Fire | player, count |

```lua
Extensions.Add("Classes.Pulsed", function(player, count)
	AnalyticsService.Custom(player, "ReconPulse", count)
end)
```

### DroneShield

The player's drone takes no damage for `Duration` seconds. Works through `Combat.BlockHit`: while the drone's `ShieldedUntil` attribute (server time) is in the future, every hit is cancelled. Refused with no living drone. It's the only ability marked `Bodiless = true` (the `Operator` class file), so it works from the drone's view during Prep, before attackers have a body; Siege vouches for it through `Classes.AllowBodiless`.

```lua
-- Client: show a shield icon while it's up
local shieldedUntil = drone:GetAttribute("ShieldedUntil") or 0
icon.Visible = workspace:GetServerTimeNow() < shieldedUntil
```

### SmokeScreen

Pops a smoke cloud where the player looks, up to `Range` away (in the air at `Range` when they look at nothing). It's the consumables' own smoke (`ConsumableService.Detonate` with `Tuning.Consumable`), so it blocks NPC sight and aim assist the same way.

```lua
-- The same cloud from your own code:
ConsumableService.Detonate("Smoke", position, player)
```

### Shield

A ballistic shield carried with the sidearm (slot 2). Rules shared with the client are in `Shared.BallisticShield` (`Pose`, `CanFire`: only prone or aiming). It's disabled for `ShieldRecovery` seconds after a defender's melee. `ClassService.Arm` equips it; `Shield.Clear(player)` removes it.

Character attributes: `ShieldRaised`, `ShieldDisabledUntil`, `ShieldPose`, `ShieldBashUntil`, `BallisticShieldOperator`.

```lua
local disabled = character:GetAttribute("ShieldDisabledUntil") or 0
if workspace:GetServerTimeNow() < disabled then
	-- shield is down after a bash
end
```

### Hacker (Dead Call)

Caleb's phone: pick a scanned defender to "call". The hacked defender must hold to unhack (`UnhackTime`) or be revealed. Uses its own packets: `DeadCall.Phone` (`"List"` / `"Hack"` + UserId, answered), `DeadCall.State` (to the hacked defender) and `DeadCall.Control` (holding). Player attribute while hacked: `DeadCallActive`. Resets on `Siege.Ended`.

```lua
-- Client: list the defenders Caleb can call
local result = Packets.DeadCall.Phone:Fire("List", 0)
for _, target in result.Targets do print(target) end
```

### Motion Scanner

Leo's map-wide motion scan (attackers only). After a safe lead-in (`SafeTimedown`, default 2 s) the scan runs until `Countdown` (default 5 s): every defender (player or defender NPC) who **moves** in that window (walking, crouching, jumping, being pushed) is marked **for Leo** for `MarkedTimedown` seconds (default 10), the mark following them every ~0.15 s. Standing still is safe. Defenders are warned: workspace attributes `LeoMotionScanStartsAt`, `LeoMotionScanEndsAt`, `LeoMotionScanWarningTextEndsAt`; a caught player gets `LeoSpottedUntil` and `LeoSpottedMessageUntil`. Client warning: `Client.Gadgets.LeoMotionWarning`.

```lua
-- Client (defender): is a scan running right now?
local starts = workspace:GetAttribute("LeoMotionScanStartsAt")
local ends = workspace:GetAttribute("LeoMotionScanEndsAt")
local now = workspace:GetServerTimeNow()
local scanning = starts and ends and now >= starts and now < ends
```

### StoneBarrier

Places a 6×6×1 stud barrier on flat ground where the player looks (refused on walls, slopes or if anything is in the way). Removed at `Siege.RoundEnded`.

---

## Defenders

### TrapMine

Places a mine where the player looks. After `ArmTime` it's live (`Armed` attribute); every `Check` seconds the server measures the distance to each living enemy (never `Touched`) and blows it when one is within `TriggerRadius`. Blast: up to `BlastDamage` within `BlastRadius`, credited as `"Trap Mine"`. An attacker can shoot it (`Health`); a destroyed mine doesn't blow.

| Point | Kind | Arguments |
| --- | --- | --- |
| `Classes.PreventMineTrigger` | Any | owner, victim, model |
| `Classes.MineDetonated` | Fire | owner, victim, position |

```lua
-- Crouch-walking past a mine doesn't set it off
Extensions.Add("Classes.PreventMineTrigger", function(owner, victim, model)
	return MovementService.IsCrouched(victim)
end)
```

### Reinforce

Replaces the board or door board the player looks at with its **reinforced** version for the rest of the match (`ReinforcedBoard` / `ReinforcedDoor` breakable types, tougher pieces). The original waits in ServerStorage and comes back whole when the match ends. Needs a **hold** (`Class.Hold`, `HoldDuration`, default 1.5 s) before `Class.Use` completes it; a reinforced wall can be picked up again for a refund. If the look hits no board (an unbuilt door frame), the nearest board to the line of sight within `Range` is used. Model attribute: `Reinforced = true`. Fires `Classes.Reinforced(player, model)`.

```lua
Extensions.Add("Classes.Reinforced", function(player, model)
	print(player.Name, "reinforced", model.Name)
end)
```

### HealingStation

Places a station. For `Duration` seconds, every `Tick`, each living teammate within `Radius` gains `HealPerSecond × Tick` health (never above max). An attacker can destroy it (`Health`).

| Point | Kind | Arguments |
| --- | --- | --- |
| `Classes.HealMultiplier` | Product | owner, patient |
| `Classes.Healed` | Fire | owner, patient, amount |

```lua
-- Half healing for anyone who was hit in the last 3 seconds
Extensions.Add("Classes.HealMultiplier", function(owner, patient)
	local attacker = DamageLog.Last(patient, 3) -- a Player (or an NPC model), not a Humanoid
	return if attacker then 0.5 else 1
end)
```

### Stim

Heals the player by `Heal` at once (never above max). Refused at full health so a charge isn't wasted. Uses the **same** `Classes.HealMultiplier` / `Classes.Healed` points as the Healing Station.

```lua
Extensions.Add("Classes.Healed", function(owner, patient, amount)
	if owner == patient then print(owner.Name, "stimmed for", amount) end
end)
```

### BulletproofCamera

Sticks a camera to a surface, facing out. It joins the defenders' cameras (`CameraService.Add`), so every defender can view and cycle to it. Bullets do 0 (`CameraService` answers `Gun.DamageMultiplier` with 0); a bash or explosion still breaks it. Health: `Content.Cameras.BULLETPROOF_HEALTH`.

```lua
-- Same thing from code:
CameraService.Add(model, `{player.Name}'s camera`, "Defenders", true)
```

### ProximitySensor

A surface-mounted detector. After `ArmTime` it's `Armed`; every `Check` seconds any living enemy inside the model's `Hitbox` volume, with no solid wall between, is marked for the owner and their team for `MarkTime` (at most once per `AlertCooldown` per enemy) and the sensor beeps. Model attribute `Detecting` is `true` while someone is inside. It can be destroyed (`Health`).

```lua
-- Client: light up a sensor while it detects
sensor:GetAttributeChangedSignal("Detecting"):Connect(function()
	light.Enabled = sensor:GetAttribute("Detecting") == true
end)
```

### Laser

A surface-mounted emitter (`Range` default 9). `Systems.Lasers.LaserLinks` automatically connects placed emitters that can see each other with a beam; an enemy crossing it takes `Damage` and is marked (`MarkTime`), with an `AlertCooldown`. Emitter attributes: `LaserEmitter`, `LaserArmedAt`, `LaserDamage`, `LaserAlarmCooldown`, `LaserMarkTime`.

```lua
-- Message the player sees after placing one:
-- "Laser placed. Place another emitter to connect them."
```

### Hologram

A frozen decoy of the player in their current pose and gun (the client sends `Class.HologramPose` just before the use). Bullets don't hurt it: a hit **reveals the attacker** instead and the hologram glitches (`Class.HologramGlitch` to all clients, reason `"Shot"` or `"Walk"`).

### C4

One sticky, indestructible charge, thrown. Pressing the ability again (even in flight) arms its remote fuse; `HasActive(player)` is true while it's out, so the second press spends no charge. `C4.Clear(player)` removes it.

```lua
local Abilities = game.ServerScriptService.Modules.Systems.Classes.Abilities
local C4 = require(Abilities.C4)
print(C4.HasActive(player)) -- a charge is out and not yet detonating
```
