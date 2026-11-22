[Documentation home](index.md) / [API reference](API.md)

# Client API reference

> **Scope:** Client modules and UI-facing APIs. For the current Siege selection and HUD flow, see [API_SIEGE.md](API_SIEGE.md) and [UI.md](UI.md).

## Client

### Effects and audio

| Function | What it does |
| --- | --- |
| `Client.Effects.Play(name, options?)` / `Effects.Stop(name, target?, data?)` | Plays a `Content.Effects.Registry` effect locally (options: `Target`, `CFrame`, `Variant`, `Data`, …) |
| `Client.Guns.GunEffects.Play(name, options?)` / `LocalShot(ctx, directions, muzzle?)` | Gun effects; your own shot's tracers and flash |
| `Client.Guns.Quality.Scale()` / `Count(n)` | The effect quality factor and a particle count scaled by it |
| `Client.Audio.AudioSettings.Get(group)` / `GetAll()` / `Set(group, volume)` | Volumes |
| `Client.Audio.SoundGroups.Get(name?)` / `Assign(sound, name?)` / `Master()` | Sound groups |

Effect parts (`Content.Effects.Parts.*`), each `Play(spec, context)`: `Animation`, `Banner`, `ColorFade`, `Debris`, `Dust`, `Highlight`, `Impact`, `JointSwing`, `MuzzleFlash`, `Particles`, `PooledSound`, `Shards`, `Shell`, `Sound`, `Template`. Inside a part, `context` has `Add(instance, lifetime?)`, `Delay(seconds, fn)`, `Hold()`, `Keep(seconds)`, `OnStop(fn)`, `Anchor()`, `Group()`, `Stop(data?)` and `context.Data`.

### Guns (client)

| Function | What it does |
| --- | --- |
| `Viewmodel.Equip(gun, tool, modelName?, melee?)` / `Unequip()` | First-person gun |
| `Viewmodel.SetAiming(bool)` / `AimAlpha()` / `SetFov(fov?)` / `SetHidden(bool)` / `IsFirstPerson()` / `Ready()` | Aim and view state |
| `Viewmodel.Kick(recoil, rng?, stance?)` / `Muzzle()` | A shot's kick / the muzzle attachment |
| `Viewmodel.Inspect()` / `Bash()` / `Swing()` / `Reloading()` / `FinishReloading()` and `IsInspecting()` / `IsBashing()` | Actions |
| `Viewmodel.SetSkin()` | Re-applies the equipped skin |
| `Viewmodel.GunModel.*` | `Get`, `ApplySkin`, `SkinOf`, `Bounds`, `Scaled`, `MakeLocal`, `NearPush` |
| `GunHud.Show(gun)` / `ShowMelee()` / `Hide()` / `SetAmmo(ammo, reserve)` / `SetReloading(bool)` / `Crosshair(spread, aimAlpha)` / `Hitmarker(headshot, killed)` / `SetAimToggle(bool)` / `MobileButtons()` | The gun HUD. `MobileButtons()` returns Fire, Aim, Reload and Bash |
| `WeaponSlots.Equip(index)` / `Cycle(step)` | Switch weapons |
| `LoadoutMenu.Pick(id)` | Picks a loadout |
| `Client.Guns.Consumables.Throw()` / `Pick(id)` | Throws one (G) / picks grenade or smoke |
| `AimAssist.SetGun(gun?)` / `Update(dt, camera, turnPitch, turnYaw, aimAlpha)` | See [AIM_ASSIST.md](AIM_ASSIST.md) |
| `Recoil.ShotKick` / `Scale`, and `Recoil.Pattern` / `Camera` / `View` classes | Recoil math (see [ADDING_GUNS.md](ADDING_GUNS.md#recoil-fields)) |

### Movement and camera (client)

| Function | What it does |
| --- | --- |
| `MovementController.State()` / `Stance()` / `IsSprinting()` / `IsForcedCrouch()` | The local movement state |
| `MovementController.CancelSprint()` / `SprintEndedAt()` / `SprintOutScale()` | Sprint control |
| `MovementController.SetGunBlock(bool)` / `SetReloading(bool)` | Tell movement a gun is busy |
| `MovementCamera.Shake(magnitude, roughness, fadeIn, fadeOut)` | Camera shake |
| `MovementCamera.SetAim(alpha, gunAdsFov?)` / `SetFovOverride(fov?)` / `ScaledFov(fov)` | FOV control |
| `MovementCamera.ConfigureRecoil(gun)` / `AddRecoil(pitch, yaw)` / `Recoil(impulse)` / `SetRecoilSpeed(s)` / `RecoilSpeed()` / `ShotKick(roll, rng)` / `Offset()` | Recoil and camera offsets |
| `MovementDebug.Toggle()` | The movement readout (`movedebug`) |

### Menus, settings, input (client)

| Function | What it does |
| --- | --- |
| `Menus.Register(name, frame)` / `Open(name)` / `Close(name?)` / `Toggle(name)` / `IsOpen()` / `SetMouseIconAfterClose(bool)` | One menu at a time, frees the mouse. Names: `Loadout`, `Settings`, `Match`, `SkinShop`, `Career`, `Backpack`, `MapSelection` |
| `Client.Hud.MatchHud` | No API: the match HUD, scoreboard (Tab), result banner, teammate outlines |
| `Client.Hud.DeathScreen` | No API: the death screen and spectate camera ([DEATH_SCREEN.md](DEATH_SCREEN.md)) |
| `Client.Guns.ThirdPersonGuns` | Third-person gun poses for every character holding a gun ([THIRD_PERSON_GUNS.md](THIRD_PERSON_GUNS.md)). `Report()`: each posed character's gun kind and fit, for checking |
| `Client.Core.MatchMenu` | No API: the admin Match menu (M) |
| `Keybinds.Get(action)` / `KeyName(action)` / `Label(action)` / `Set(action, keyName)` / `Reset()` | Key bindings |
| `Options.Get(name)` / `IsOn(name)` / `Set(name, value, previewOnly?)` / `Save(name)` | Options |
| `Slider.Bind(bar, onChange)` / `Slider.Show(row, alpha, text)` | Settings sliders |
| `PromptKeys.Key()` | The current Interact key (ProximityPrompts follow it) |
| `HealthBillboards.SetupBillboard(humanoid)` | Shows a health billboard |
| `Client.Core.UI` | No API: fits the HUD to the screen and the touch layout |
| `Client.Core.CmdrClient` | No API: F2 opens Cmdr; on touch, admins (`Classes.Admins`) get a CMD button (`Main.Mobile.CmdrButton`) |

---
