# Movement and camera

Sprint, tactical sprint, crouch, slide and prone. The **client predicts** every change at once so movement feels instant; the **server checks** it and makes it official. Nothing is sent per frame.

!!! abstract "Source"

    Server: `Systems.Movement.MovementService`. Shared: `Shared.Movement.States`. Client: `Client.Movement.MovementController`, `MovementCamera`, `MovementPoses`, `MovementDebug`. Data: `Content.Movement.Config`. Guide: [Movement and camera](../../MOVEMENT.md).

## How a state change works

1. The client changes state locally and sends `Packets.Movement.SetState(state)`.
2. `MovementService` checks it, in order:
    1. the change is in `Shared.Movement.States`' transition table, from the state **the server has**;
    2. the player can act (not `Stunned` or `CantDoAnything`) for anything but `Walk` and `Air`;
    3. **Sprint:** not stopped by `Movement.PreventSprint`, not reloading (unless their `SprintWhileReloading` option is on), tactical sprint off cooldown;
    4. **Slide:** from a sprint (or the air), on the ground, off cooldown, not stopped by `Movement.PreventSlide`;
    5. **Prone:** on the ground, outside `ProneCooldown`, not stopped by `Movement.PreventProne`.
3. Refused → `Packets.Movement.Correct(serverState)` and the client snaps back. Accepted → the server sets the states (`Sprinting`, `Crouching`, `Sliding`, `Prone` via `StateHandler`), `MoveState`, WalkSpeed and HipHeight.

**Anti-cheat:** every sample the server compares each character's speed *and real distance travelled* with what its state allows. Moving too far is undone (counted in `MoveCorrections`); speed violations are counted in `MoveViolations`. Nobody is kicked. Server moves (spawns, portals, knockback) are recognised and skipped.

## States: `Shared.Movement.States`

Both sides read this one table, so they agree on what's legal.

| State | Sprinting | Crouched | Sliding | Prone | Grounded |
| --- | :-: | :-: | :-: | :-: | :-: |
| `Walk` | | | | | ✔ |
| `Sprint`, `TacticalSprint` | ✔ | | | | ✔ |
| `Crouch` | | ✔ | | | ✔ |
| `Slide` | | ✔ | ✔ | | ✔ |
| `Prone` | | | | ✔ | ✔ |
| `Air` | | | | | |

### `States.Can(from, to) → boolean`

```lua
local States = require(game.ReplicatedStorage.Modules.Shared.Movement.States)
print(States.Can("Sprint", "Slide")) -- true
print(States.Info.Slide.Crouched)    -- true
print(States.IsState("Dive"))        -- false
```

**Adding a state** (Dive, Mantle…): add it to `Info` with its flags, add a `TRANSITIONS` row (and add it to the rows that can enter it), then handle it in `MovementController` and any server rule in `MovementService`.

## Server: `MovementService`

```lua
local MovementService = require(game.ServerScriptService.Modules.Systems.Movement.MovementService)
```

### `MovementService.GetState(player) → string`

The state as the server has it (`"Walk"` with no character).

```lua
if MovementService.GetState(player) == "Prone" then
	-- prone players can't plant faster, etc.
end
```

### `MovementService.BlocksFire(player, gun) → boolean`

`true` while sprinting, and for the gun's `SprintOutTime` after (twice that after a tactical sprint). `GunService` calls this for every shot.

```lua
local Registry = require(game.ReplicatedStorage.Content.Guns.Registry)
if MovementService.BlocksFire(player, Registry.AssaultRifle) then
	return -- still coming out of a sprint
end
```

### `MovementService.IsCrouched(player) → boolean`

Crouched, sliding or prone now, or a moment ago. Used to accept the crouch spread.

```lua
local stance = if MovementService.IsCrouched(player) then "Crouch" else "Stand"
```

### Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Movement.PreventSprint` | Any | player, state (`Sprint` or `TacticalSprint`) |
| `Movement.PreventSlide` | Any | player |
| `Movement.PreventProne` | Any | player |
| `Movement.SpeedMultiplier` | Product | player, gunId? (the gun's own `MoveSpeedMultiplier` is applied on top; sent to the client as the `MoveSpeedMultiplier` attribute) |

```lua
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

-- No sprinting while carrying the LMG
Extensions.Add("Movement.PreventSprint", function(player, state)
	local character = player.Character
	local tool = character and character:FindFirstChildOfClass("Tool")
	return tool ~= nil and tool:GetAttribute("GunId") == "LMG"
end)

-- 10% faster for everyone on the attacking side
Extensions.Add("Movement.SpeedMultiplier", function(player, gunId)
	return if player:GetAttribute("Team") == "Attackers" then 1.1 else 1
end)
```

## Client: `MovementController`

```lua
local MovementController = require(game.ReplicatedStorage.Modules.Client.Movement.MovementController)
```

| Function | Returns / does | Example |
| --- | --- | --- |
| `State()` | The local state name | `if MovementController.State() == "Slide" then ... end` |
| `Stance()` | `"Crouch"`, `"Slide"` or `"Prone"` when the stance changes spread, else `nil` | `Spread.Angle(gun, aiming, move, bloom, MovementController.Stance())` |
| `IsSprinting()` | Sprint or tactical sprint | `if MovementController.IsSprinting() then return end` |
| `IsForcedCrouch()` | Held low by a ceiling | `if MovementController.IsForcedCrouch() then showHint() end` |
| `CancelSprint()` | Drops out of sprint (firing, aiming) | `MovementController.CancelSprint()` |
| `SprintEndedAt()` / `SprintOutScale()` | When sprint ended; ×2 after a tactical sprint | `local ready = os.clock() - MovementController.SprintEndedAt() > gun.SprintOutTime * MovementController.SprintOutScale()` |
| `SetGunBlock(on)` | The gun is busy (no sprint) | `MovementController.SetGunBlock(true)` |
| `SetReloading(on)` | Reloading (sprint follows the `SprintWhileReloading` option) | `MovementController.SetReloading(true)` |

## Client: `MovementCamera`

```lua
local MovementCamera = require(game.ReplicatedStorage.Modules.Client.Movement.MovementCamera)
```

### `MovementCamera.Shake(magnitude, roughness, fadeIn, fadeOut)`

```lua
MovementCamera.Shake(3, 10, 0.1, 0.6) -- a grenade nearby
```

### `MovementCamera.SetAim(alpha, gunAdsFov?)` / `SetFovOverride(fov?)` / `ScaledFov(fov) → number`

Blend to the aim FOV; force an FOV (scopes, cameras; `nil` clears); an FOV scaled by the player's FOV setting.

```lua
MovementCamera.SetAim(Viewmodel.AimAlpha())  -- every frame while a gun is held
MovementCamera.SetFovOverride(30)   -- scope in
MovementCamera.SetFovOverride(nil)  -- scope out
```

### Recoil: `ConfigureRecoil(gun)`, `AddRecoil(pitch, yaw)`, `Recoil(impulse)`, `SetRecoilSpeed(speed)`, `RecoilSpeed()`, `ShotKick(rollDegrees, rng)`, `Offset()`

Called by the gun controller per shot; see [Adding guns](../../ADDING_GUNS.md#recoil-fields) for the numbers.

```lua
MovementCamera.ConfigureRecoil(gun)               -- on equip
MovementCamera.AddRecoil(gun.Recoil.Vertical, 0)  -- per shot
```

### `MovementCamera.KnifeSwing(duration, side)` / `StopKnifeSwing()`

The camera sway of a knife swing.

```lua
MovementCamera.KnifeSwing(0.35, 1)
```

### `MovementDebug.Toggle()`

The on-screen movement readout (also the `movedebug` command).

Camera render priority: MovementCamera Camera+1, Viewmodel +2, drone camera +3, death camera +4.
