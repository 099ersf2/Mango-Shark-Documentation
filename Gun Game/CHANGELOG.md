# Changelog

## 2026-11-08: Movement, camera feel and FOV

### Added

- **Movement states.** Walk, Sprint, TacticalSprint (double-tap sprint), Crouch, Slide and Air.
  - Flags and the one transition table live in `Shared.Movement.States`.
  - Every tunable number lives in `Content.Movement.Config`.
- **`Client.Movement.MovementController`.** Runs the state machine on the client for instant response.
  - WalkSpeed ramps; HipHeight crouch with a headroom shapecast before standing.
  - A reused `LinearVelocity` drives slides (slope gain and loss, steering, cooldown) and carries slide-jump momentum with limited air control.
  - Footsteps run on a stride timer for this player and nearby others.
  - Keys come from Keybinds; the gamepad uses L3 and B; touch uses Sprint and Crouch buttons plus thumbstick auto-sprint.
- **`Client.Movement.MovementCamera`.** One RenderStep at Camera + 1, layered on the default camera.
  - Crouch and slide eye height on a spring, FOV kicks, strafe and slide tilt, a landing dip, and head bob tied to footsteps.
  - Gun recoil is in the same spring stack. CameraShaker is kept for impacts and explosions only.
- **`Systems.Movement.MovementService`.**
  - It checks each `Packets.Movement.SetState` against the transition table, cooldowns, grounded state and `Stunned` / `CantDoAnything`, and corrects with `Packets.Movement.Correct`.
  - It sets the `Sprinting`, `Crouching` and `Sliding` StateHandler states and attributes, plus `MoveState`, WalkSpeed and HipHeight.
  - It runs a 4 Hz speed check that logs and counts violations (`MoveViolations`) without kicking.
- **`Client.Movement.MovementPoses`.** Third-person crouch and slide leg poses for every character, from the replicated attributes. It uses `Config.Animations` ids through AnimationHandler when they're set, and works with Motor6D and AnimationConstraint joints.
- **Extension points.** `Movement.PreventSprint`, `Movement.PreventSlide` and `Movement.SpeedMultiplier`.
- **Settings.**
  - Actions `Sprint` (Left Shift), `Crouch` (C) and `CrouchAlt` (Left Ctrl).
  - `PlayerSettings.Options`, saved under `Settings.Options` through the new `Packets.Settings.Option`:
    - `Fov` (60–110, default 80) and `CameraBob` (0–100%);
    - `HoldSprint`, `HoldCrouch`, `MobileAutoSprint` and `SprintWhileReloading`.
  - `Client.Settings.Options` loads and applies them, previewing live while a slider is dragged.
  - Settings menu sections **Movement** and **Display**, with rows from the new `ToggleRow` and `SliderRow` templates.
- **`Client.Settings.Slider`.** The drag and snap logic shared by every settings slider; the volume sliders use it too.
- **Gun fields.** `SprintOutTime` (default 0.15) and `MoveSpeedMultiplier` (default 1), plus `Spread.Crouch` (0.7) and `Spread.Slide` (2).
  - Pistol: 0.1s and 1.05.
  - Shotgun: 0.2s and 0.95.
  - BurstRifle: 0.18s and 0.95.
- **Effects.**
  - Registry entries: `SlideStart`, `SlideLoop` (Persistent), `Land` and `Footstep` (variants Concrete, Grass, Soft, Wood and Metal).
  - A pooled `Dust` effect part.
  - Sounds in `Assets.Sounds` and the dust emitters `SlideDust`, `LandDust` and `StepDust` in `Assets.Vfx`.
- **UI.** `Main.Mobile.CrouchButton`, and the `SprintButton` wired with a label. The `MovementDebug` template.
- **Cmdr.** `movedebug` toggles an on-screen movement readout.
- **Docs.** `docs/MOVEMENT.md`.

### Changed

- **Viewmodel.**
  - It runs at Camera + 2, after MovementCamera, and no longer writes the camera's CFrame or FOV. Recoil, ADS zoom and scopes go through MovementCamera.
  - ADS FOV is `base × ADSFov / 70`, so zoom is the same at any FOV.
  - New crouch and slide poses.
  - At the hip, the gun's offset partly makes up for high FOV (`Config.ViewmodelFovCompensation`).
- **GunController.**
  - Sprinting blocks firing and aiming. The trigger or aim ends a sprint and waits `SprintOutTime` (×2 after a tactical sprint).
  - Spread uses the movement stance.
- **GunService.**
  - `tryShot` refuses a player's shot while sprinting or inside `SprintOutTime` (`MovementService.BlocksFire`).
  - The minimum spread accepts the crouch cone while the player is crouched.
- **`PooledSound`.** Supports `Looped` (until the effect stops) and a per-play `Data.Volume`.
- **`StarterPlayer.EnableMouseLockOption`.** Now off, since Left Shift is sprint.
- **Default Running sound.** Muted on every character, since footsteps replace it.

## 2026-11-08: Kill sounds and NPCs with guns

### Added

- **Kill sounds.** `Assets.Sounds.KillConfirm` (the headshot sound at 0.75 speed, lower with a longer tail) and `KillThump` (the body hit at 0.55, a heavy low thump). The `Hitmarker` effect gets `Kill` and `HeadshotKill` variants; `GunHud.Hitmarker` picks HeadshotKill, Kill, Headshot or body, one per hit.
- **`Gun.Killed` extension point.** Fires `(who, victimHumanoid, gunId, headshot)` once per kill, for players and NPCs.
- **NPCs.**
  - Profiles: `Content.NPC.Profiles` (Soldier, Breacher, Grenadier), typed by `Content.NPC.Types`.
  - Rig, tree and spawning: the rig is `ServerStorage.NPC.Templates.Soldier`. The behavior tree `ServerStorage.NPC.Trees.Soldier` is in the BTrees Editor format.
  - Code: `Systems.NPC.NPCService` (spawning, respawns, round-robin scheduler, sleeping, aiming and shooting) and `Systems.NPC.Brain` (shared helpers and the `NPCWorld` blackboard).
  - Tasks in `Systems.NPC.Tasks`: FindTarget, HasLineOfSight, InRange, LowHealth, NeedsReload, MoveToCover, Strafe, Chase, AimAndShoot, Reload and Patrol.
  - NPCs on the same team don't hurt each other.
- **Cmdr.** `spawnnpc <profile> [count]` and `clearnpcs`, with an `npcProfile` argument type.
- **Test area.** `Workspace.NPCTestArea` (three NPCSpawn parts and cover crates) and `Workspace.Enemies`. The Enemies folder also fixes the existing `HealthBillboards` startup error.
- **Docs.** `docs/ADDING_NPCS.md`.

### Changed

- **`GunService` serves players and NPCs.**
  - Held guns are keyed by character, and a `Shooter` type is `{ Character, Player?, Id }`.
  - New functions: `ShooterOf`, `GiveNPC`, `FireAs`, `ReloadAs` and `RemoveShooter`.
  - Players' `Fire` packet handler is unchanged; both paths share the same shot checks.
  - Extension points get the Player or the NPC model.
  - Ability damage through `ctx.ApplyHit` now applies `Gun.DamageMultiplier`.
- **Shot context.** `ShotContext` and `GunContext` have a `Character`, and `Player` can be nil for an NPC. `Ballistics.Filter` and `ExplosiveRounds` use the shooter's character.
- **`Combat.ApplyHit` and `DamageLog`.** They accept a `Player` or an NPC `Model` as `Attacker`, and `DamageLog` records NPC victims too.
- **`UnreliablePackets.GunFired`.** It carries a UserId or an NPC Id. `GunEffects` finds NPC shooters by their `NPC` tag and `NPCId` attribute.
- **Client tracer pool.** It starts larger (40 per gun), so crowds of NPCs don't make it grow.

### Fixed

- **Kill detection.** A kill is reported only on the hit that takes health from above 0 to 0 or below, so a corpse or a second pellet never plays a kill sound again.

## 2026-11-07: Loadouts, weapon switching and settings

### Added

- **Loadouts.** `Content.Guns.Loadouts` lists Assault, Breacher, Grenadier and Arsenal (up to three guns each). `Systems.Guns.LoadoutService` gives the picked loadout on every spawn with `Slot` attributes and equips slot 1. The Loadout menu (`Main.Loadout`, `Client.Guns.LoadoutMenu`) opens on join and with `B`; the pick is saved in player data.
- **Weapon switching.** `Client.Guns.WeaponSlots` replaces the Roblox hotbar: keys 1/2/3, the mouse wheel, gamepad L1/R1, and the slot strip on the right side (`Main.Weapons`).
- **Settings menu.** `Main.Settings` (`Client.Settings.SettingsMenu`, key `P`) rebinds every action and sets Master, Effects, Music and Interface volume. Keybinds (`Client.Settings.Keybinds`) and volumes are saved in player data through `Packets.Settings` and `Services.SettingsService`.
- **Menus.** `Client.Core.Menus` tracks the open menu, frees the mouse in first person and stops gun input while one is open.
- **UI.** `Main.MenuButtons` (Loadout, Settings) and templates `LoadoutCard`, `KeybindRow` and `VolumeRow` in `Assets.UI.Templates`.

### Changed

- `GunController` reads its keys from `Keybinds` and rebinds when they change.
- `GunService.Give` sets a `Slot` attribute on each Tool.
- `AudioSettings.Store` now loads and saves volumes from player data instead of keeping them for the session only.

## 2026-11-07: Iron sights

### Changed

- **Iron sights.** Rifle, Pistol and Shotgun have a rear notch and a front sight (`RearSightL`, `RearSightR`, `FrontSight`), and each `Aim` attachment sits on the line through them, so aiming looks down the sights.
- **No scope on the Rifle.** The Rifle no longer has the `Scope` ability; it stays in `Content.Guns.Abilities` for a sniper.
- **Crosshair while aiming.** It shrinks as you aim in and hides halfway (`GunHud.AIM_HIDE`), so you aim with the iron sights alone.
- **Hit sounds.** The `Hitmarker` effect now plays the hitmarker click plus a body hit (`BodyHit`), and its `Headshot` variant plays `HeadshotHit` instead. Both are non-positional and louder than before, so they cut through gunfire.

### Fixed

- **Gun parts hanging off the handle in first person.** The viewmodel now swaps a gun's `WeldConstraint`s for fixed `Weld`s before showing it, so the order joints turn on can't leave parts behind.
- **Crosshair not visible.** `Main.Crosshair` was 0×0, so converting it to scale gave its lines infinite sizes. It is now 48×48 with its lines placed from its center.

## 2026-11-07: Gun system

### Added

- **Data-driven guns.** `Content.Guns` holds `Registry` (definitions with defaults and load-time checks), `Types`, `Definitions` (Rifle, Pistol, Shotgun, BurstRifle) and `Abilities` (ShotgunSpread, Burst, ExplosiveRounds, Scope, Ricochet).
- **Server.** `Systems.Guns.GunService` handles giving guns, equips, server-owned ammo and reloads, fire-rate checks (a minimum interval plus a `TokenBucket` per gun), origin clamping with a line-of-sight check, spread clamping and server casts. `Systems.Guns.AbilityRunner` handles per-bullet damage and server ability hooks. All damage goes through `Combat.ApplyHit`.
- **Shared.** `Shared.Guns.Ballistics` (seeded shots, one FastCast2 Serial caster per gun per side, hitscan traces, the pierce/bounce rule), `Shared.Guns.Abilities` (hook runner), `Shared.Guns.Spread` and `Shared.Guns.Spring` (both `--!native`).
- **Client.** `Client.Guns.GunController` (KB/M, gamepad and touch input; fire loop; reload; ADS), `Viewmodel` (first-person arms and gun with sway, bob, recoil, ADS, sprint and equip poses), `GunEffects` (local and replicated cosmetic shots, aim pitch), `GunHud` and `Quality`.
- **Networking.** A `Packets.Gun` group (`Fire`, `Reload`, `Aim`, `AltFire`, `HitConfirm`), plus `UnreliablePackets.GunFired`, `GunAim` and `GunAimRelay`.
- **Extension points.** `Gun.PreventFire`, `Gun.DamageMultiplier`, `Gun.Hit` and `Gun.Reloaded`.
- **States.** `Reloading` and `Firing` through `StateHandler`.
- **Effects.**
  - Registry entries: `GunFire_Rifle`, `GunFire_Pistol`, `GunFire_Shotgun`, `BulletImpact`, `Reload`, `DryFire`, `Hitmarker` and `Explosion`.
  - Pooled effect kinds: `MuzzleFlash`, `PooledSound`, `Shell` and `Impact`.
- **Assets.**
  - Gun models (`Assets.Models.Guns`): Rifle, Pistol and Shotgun, each with `Handle`, `Muzzle`, `EjectionPort`, `Aim`, `RightGrip` and `LeftGrip`.
  - Viewmodel rig: `Assets.Models.Viewmodel`.
  - VFX: `MuzzleFlash`, `BulletImpact`, `BulletHole`, `ShellEject`, `Tracer`, `TracerRed` and `Explosion`.
  - Sounds: `RifleFire`, `PistolFire`, `ShotgunFire`, `Reload`, `DryFire`, `Explosion` and `Hitmarker`.
  - UI template: `ScopeOverlay`.
- **UI.**
  - `StarterGui.Main.Gun`: ammo, reserve, fire mode and reload bar.
  - `Main.Crosshair`: the gap follows the spread.
  - `Main.Hitmarker`.
  - `Main.Mobile` buttons: `FireButton`, `AimButton` and `ReloadButton`.
- **Cmdr.** `givegun <player> <gunId>`, with a `gun` argument type.
- **Docs.** `docs/ADDING_GUNS.md` and `docs/GUN_SYSTEM.md`.

### Changed

- **`EffectService.Play`.** Takes an optional third argument, `except`: a player not to send the effect to. Existing calls are unchanged.
- **`Shared.Extensions`.** The header now lists the gun extension points.
