# Aim assist

Aim assist helps controller and touch players hit targets in the FPS place. Mouse players only get it when an admin turns it on for them with the `aimassistpc` command, for testing. It only changes how the camera turns: the server never reads it, and every bullet still goes where the camera points.

## Where things are

| What | Where |
| --- | --- |
| The logic | `ReplicatedStorage.Modules.Client.Guns.AimAssist` (`ClientOnly`) |
| Applied to the camera | `Client.Movement.MovementCamera`, inside its one camera step |
| PC testing command | `aimassistpc <player> [true/false]` (alias `aapc`) in `Services.CmdrSetup.Commands.AimAssistPC` / `AimAssistPCServer` |
| Told which gun is held | `Client.Guns.GunController` (`AimAssist.SetGun` on equip and unequip) |
| The setting | `Shared.PlayerSettings` option `AimAssist`, in Settings > Toggles as "Aim assist (controller, touch)". On by default |

## When it's active

All of these must be true:

- The player's preferred input is **Gamepad** or **Touch** (`UserInputService.PreferredInput`), **or** the player has the `AimAssistPC` attribute (set by the `aimassistpc` command).
- The **Aim assist** setting is on.
- A **gun** is held. The knife doesn't count.
- The player is **not in the lobby** (`InLobby`).

## What it does

| Part | What it does | Strength |
| --- | --- | --- |
| **Friction** | With the crosshair near an enemy, part of the player's own turn is taken out, so the aim slows over the target instead of sliding past | 50% of the turn at the hip, 70% fully aimed, at the target's center |
| **Pull** | While the player turns the stick or moves, the aim is drawn toward the target's chest, so it follows a strafing enemy | Closes 7 / s of the gap at the hip, 11 / s aimed; never faster than 120° per second |

- **The pull never moves the aim while the player is still** (not turning, and not moving faster than 1 stud per second), so the game never aims for you.
- **Both parts fade** from full strength on the target to nothing at the edge of the cone. The fade is squared (`1 - (angle / cone)²`), so they stay strong over most of the cone: three quarters strength halfway out.
- **Aiming down sights** blends both parts from the hip values to the aimed values.

## Targets

A target must be:

1. **Another player's character** (not a teammate when teams are used), **or a model inside `workspace.Enemies`**. Humanoids anywhere else in the map are ignored (the test rigs `Rig`, `Rig1` and `Rig2` were moved into `Enemies` on 2026-11-10). `NPCService` puts every NPC it spawns in `workspace.Enemies`, so real NPCs always count.
2. **Alive** (Humanoid health above 0).
3. **Within range:** the gun's `Range`, or 250 studs if the gun has none.
4. **Inside the cone:** 12° from the crosshair at the hip, 9° aimed. Close targets widen the cone to cover about 4 studs of body.
5. **In clear view:** a ray from the camera to the target must hit the target first.

The aim point is the first of `UpperTorso`, `Torso` or `HumanoidRootPart`. If several targets qualify, the one closest to the crosshair wins.

## How it fits with recoil

`MovementCamera` already owns every camera rotation (recoil, landing dip, tilt, bob), so aim assist runs in the same step:

1. It measures the player's own turn since last frame.
2. It calls `AimAssist.Update(dt, camera, turnPitch, turnYaw, aimAlpha)`, which returns the pitch and yaw to add.
3. It applies the assist as a lasting turn: yaw about world up, pitch about the camera's right, so the assist never adds roll.
4. The assist is left out of the turn recoil sees next frame, so recoil never treats the assist as the player pulling down.

## Tuning

Every number is a constant at the top of `Client.Guns.AimAssist`:

| Constant | Default | Meaning |
| --- | --- | --- |
| `CONE_HIP` / `CONE_ADS` | 12° / 9° | Half-angle of the cone |
| `TARGET_RADIUS` | 4 | Studs of body the cone covers on close targets |
| `DEFAULT_RANGE` | 250 | Range for guns without `Range` |
| `FRICTION_HIP` / `FRICTION_ADS` | 0.5 / 0.7 | Share of the player's turn removed on target |
| `PULL_HIP` / `PULL_ADS` | 7 / 11 | Share of the gap closed per second while turning or moving |
| `MAX_PULL_SPEED` | 120° / s | Fastest the pull may turn the aim |
| `FALLOFF_POWER` | 2 | Strength is `1 - (angle / cone) ^ FALLOFF_POWER`; higher stays strong further out (1 is a straight fade) |
| `TURN_THRESHOLD` | 2° / s | Player turn that counts as turning |
| `MOVE_THRESHOLD` | 1 | Studs per second that count as moving |
| `AIM_PARTS` | UpperTorso, Torso, HumanoidRootPart | The aim point, first found |

## API

```lua
local AimAssist = require(ReplicatedStorage.Modules.Client.Guns.AimAssist)

AimAssist.SetGun(gunDefinition)   -- on equip; nil on unequip (GunController does this)
local pitch, yaw = AimAssist.Update(dt, camera, turnPitch, turnYaw, aimAlpha)   -- radians to add this frame
```

`Update` returns `0, 0` whenever aim assist is off, the input is mouse, or there's no target.

## Testing

**On PC:** open Cmdr (F2) and run `aimassistpc <you>` (alias `aapc`). It toggles aim assist for that player on mouse and keyboard; `aimassistpc <you> true` or `false` sets it. It's a server-set player attribute, `AimAssistPC`, so only admins can turn it on, and it lasts until you leave or turn it off. The **Aim assist** setting must also be on (it is by default). Checked 2026-11-10 in a playtest: the command registered, set, toggled and cleared the attribute; on mouse input with it on, a target 3° off the crosshair gave a turn toward it, and with it off, nothing.

- **2026-11-10: strengthened** after play feedback that it was very weak: wider cone (7°/5° to 12°/9°), friction 0.35/0.5 to 0.5/0.7, pull 3/5 to 7/11 with a 120°/s cap (was 40°/s), and a squared fade. Not yet felt on a controller or phone after the change.

- Studio reports mouse input, so the assist stays off in a normal playtest. Use Studio's device emulator (a phone, or a connected gamepad) to feel it.
- To check the math in a playtest, require a copy of the module with the input check removed, call `SetGun({ Range = 300 })`, and call `Update` with a test `Camera` pointed a few degrees off a dummy in `workspace.Enemies`. This was checked on 2026-11-09: friction and pull inside the cone, nothing outside it, with no gun, or on mouse.
- Not yet tried on a real controller or phone.

## Limits

- Only players and `workspace.Enemies` count; tag-based or other NPC folders are not scanned.
- One target at a time, chosen fresh every frame.
- No snap-to-target on aiming down sights, by design.
