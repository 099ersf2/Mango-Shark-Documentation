# Changelog

## 2026-11-09: Decisions round (shop stand, keys, recoil, bash, debris, Revolver)

Follows the answers in [docs/DECISIONS.md](docs/DECISIONS.md).

### Changed

- **Crouch is Left Ctrl, prone is C** (swapped). Saved keys still on an old default move on join, and swaps work both ways (`Client.Settings.Keybinds` `MOVED_DEFAULTS`).
- **The skin shop is a stand in the lobby** (`Workspace.Lobby.SkinShopStand`), opened with its prompt (Interact, E). The I key and the Skin shop button are gone.
- **Lobby camera fixed.** The shop no longer forces a free mouse every frame in the lobby, so the camera turns again.
- **Recoil doesn't drag the aim back down.** After a spray, the aim stays where recoil left it and the player pulls it back. The old ease-back is kept behind `Recoil.RecoverAim = true` (default `false`, in `Content.Guns.Registry`).
- **Shotgun kick lowered** (Shotgun and SiegeShotgun: Vertical 4.5 / 6, ViewFlip 9, Kick 0.2).
- **New gun bash animation.** A timed windup, a cross-body strike and a smooth return (0.5 s, `Viewmodel.Actions`), replacing the spring jab.
- **A bash cancels a reload** (client and server: `GunService.CancelReload`).
- **Per-gun soft-wall holes.** Each gun's `SoftWallConfig.Guns[Id].HoleRadius` applies (Pistol 0.15, LMG 0.25, SMG 0.18, Shotgun pellets 0.15, and so on). BurstRifle explosive rounds stop at soft walls (`Penetrates = false`).
- **Door board prompt** reads "Door board".
- **Old helpers tidied** to house style (headers, `--!strict`), with these fixes:
  - `Services.PlayerJoin` sets the Player collision group when parts are added instead of scanning every character each frame; only the UpperTorso rule still runs per frame.
  - `Client.Hud.HealthBillboards` no longer errors without `workspace.Enemies`, and its waits time out.
  - `Handlers.AnimationHandler.RemoveAnim` works with numeric ids; `Handlers.StateHandler.SetStun` finds the Humanoid on the character.
  - `Client.Combat.CharacterHurt` drops an unused camera shaker. `Main`, `UI`, `CharacterAdded`, `CmdrClient`, `CursorAim`, `TableHelpers`, `UIHelpers`, `SetCollisionGroup`, `CmdrSetup`, `TokenBucket`, `UnreliablePackets`, `PersonalHealth`, `HealthUI` and `config` got headers.

### Added

- **Visible debris.** A broken plank falls as a copy of itself; soft-wall holes and chunks throw small chips. These are client-only effect parts (`Content.Effects.Parts.Debris`), faded and removed after a few seconds.
- **Revolver** is a gun (`Content.Guns.Definitions.Revolver`: semi, 48 damage, 6 rounds), with a Handle and attachments on its model, and a **Gunslinger** loadout (Revolver, Pistol, Knife).
- **Crate refund.** Buying a crate with every skin owned gives 500 coins (`Skins.CRATE_REFUND_COINS`).

### Not done

- **The 499 Robux crate product isn't created yet.** Creating it needs the Open Cloud `developer-product:write` permission, which this Studio connection doesn't have. See [the setup steps](docs/SKINS.md#setting-up-the-crate-product).

## 2026-11-09: Gun bash (melee)

### Added

- **Gun bash.** Press Q (rebindable "Melee" in Settings > Controls), click the mouse wheel, or press R3 on a gamepad to hit with any gun.
  - It deals 45 damage within 6 studs (35° cone) on a 0.9 s cooldown.
  - The Pistol is lighter and quicker; the Shotgun and LMG hit harder.
  - Scrolling the wheel still switches weapons.
- **Server-decided hits** (`Systems.Combat.GunMelee`).
  - Hits are credited like bullets: the kill feed shows "<Gun> bash", plus the hitmarker and DamageLog.
  - Each bash knocks one piece (the spray paint or a plank) off a board, and cuts a melee-sized hole in soft walls.
- **Animation.** A spring-based gun-jab in the viewmodel. It ends aiming, sprinting and inspecting, and isn't possible while reloading.
- **Config and hooks.**
  - Numbers and per-gun overrides live in `Content.Guns.Melee`.
  - New extension points `Gun.PreventMelee` and `Gun.MeleeHit`, and a new packet `Packets.Melee.Swing`.
- **Effects.**
  - New: `MeleeSwing`, `MeleeImpact`, and the soft-wall `SoftWallHole` and `SoftWallChunk` (stone knock, rubble and dust).
  - New sounds: `MeleeImpact`, `RockImpact`, `RubbleFall` (ProSoundEffects).

## 2026-11-09: Soft walls rebuilt

### Changed

- **Soft walls rebuilt (`Systems.Destruction.SoftWalls`).**
  - Every hit that lands on a wall while it waits or rebuilds is cut in one CSG pass, so a shotgun blast is one rebuild.
  - Caps limit rebuilds per frame, rebuilds in flight and cuts per rebuild. Nothing runs while idle.
- **Loose pieces fall as debris** instead of vanishing.
  - Debris doesn't collide with players, and bullets pass through it. It's removed after 8 s, with at most 20 pieces at once.
  - New support rule: `Auto`, `Bottom`, `Touching` or `All`, set per wall with the `SoftWallSupport` attribute.
- **Bullets lose damage through soft walls.** `PenetrationMultiplier` applies per wall and can be set per gun, up to 4 walls, without using up the gun's Pierce. Before this, the multiplier was never applied.
- **Square holes,** turned by a random angle (`HoleShape`, `HoleSpin`). Round holes cost about 10× more with the precise collision that holes need.
- **Melee and explosions.** Melee cuts 0.45-stud holes (source `"Melee"`). Explosions now damage boards whose planks have holes.
- **Config.** `Content.Destruction.SoftWallConfig` holds every soft wall number, with per-gun and per-source settings.

### Added

- **Cmdr commands** `softwallpunch [radius] [ring]` and `softwallreset [all]`.
- **Docs.** New `docs/SOFTWALLS.md`, plus updates to the shot flow in `GUN_SYSTEM.md`, a board note in `BREAKABLES.md` and a link in `GUN_GAME.md`.

## 2026-11-09: Gun recoil patterns, gun client refactor and Shotgun model fix

### Added

- **Recoil patterns.** Each gun has a learnable spray: the first shots climb straight, then the aim weaves side to side the same way every spray, with a small random part. The weave comes from a seeded curve or an authored `Recoil.Pattern`, and the spray starts over after `ResetTime`.
- **Camera and gun recoil are separate.** The camera (where you aim) and the gun in your hands (push-back, muzzle flip, twist, roll) each have their own spring. While you aim, the gun turns about its sights, so they stay centered.
- **Recovery respects your pull-down.** After firing, the aim returns only by the recoil you didn't already pull against, and never drags the view below where you put it.
- **Stance and fire rate.**
  - Multipliers for ADS, crouch (also used while sliding) and prone, plus a first-shot multiplier.
  - The springs stay fast enough that every shot of a fast gun still reads.
- **Per-gun feel.**
  - Rifle (steady), Pistol (snap), Shotgun (one big kick), Burst Rifle (tight burst), SMG (fast, jittery) and LMG (heavy, slow).
  - Every number is in the gun's `Recoil` table, with defaults in `Content.Guns.Registry`. See "Tuning recoil" in `docs/ADDING_GUNS.md`.
- **`Client.Guns.Recoil`.** Pure recoil math that can be tested from Studio's command bar.

### Changed

- **Viewmodel split.** `Client.Guns.Viewmodel` is now three documented parts:
  - the frame and API;
  - `Viewmodel.GunModel`: gun copies, skins, near guard;
  - `Viewmodel.Actions`: reload, inspect, knife swing.

  Behavior is unchanged.
- **House style.** SMG, LMG and Loadouts follow it now. The docs list the SMG and LMG, and the six loadouts with the knife slot.

### Fixed

- **Shotgun model.** The imported mesh had no Handle, so the Shotgun's viewmodel and muzzle were broken (boot warning "model Shotgun has no Handle part"). It now has an invisible Handle carrying Muzzle, Aim (on the sight line), RightGrip, LeftGrip (on the pump) and EjectionPort. The new look is unchanged.
- **Skins in first person** were drawn about three times too big. They're now applied at full size and scaled with the viewmodel.
- **Knife skin.** The knife no longer wears the Pistol's skin.
- **Skin changes** now update the viewmodel for every gun that has skins, not only the Rifle and Pistol.

## 2026-11-09: Skins, lobby and kill feed cleanup

### Changed

- **Lobby moved into the loader.** The loose `ServerScriptService.LobbySpawn` script is now `Systems.Lobby.LobbyService`, with the same behavior:
  - first spawn in the lobby;
  - the arena and return portals;
  - the `InLobby` attribute;
  - a 2-second portal cooldown.

  Portals now also check that the player is really next to them, and dying in the lobby gives your guns once on the next spawn instead of twice.
- **Skin shop uses Studio-built UI and packets.** The shop is `StarterGui.Main.SkinShop`, with `Main.SkinShopButton` and the `Assets.UI.Templates.SkinRow` template, instead of UI built by script. Requests go through `Packets.Skins.Equip` and `Packets.Skins.BuyCrate` instead of the runtime `SkinShopRemote`.
- **Skins are data.** `Content.Guns.Skins` describes each skin's colors, resized parts and detail parts. The saved `<Gun>Skin` fields and the shop are built from that list, so adding a skin is one entry.
- **Kill feed, Nuke and DoorBoard documented and tidied.** No behavior change. DoorBoard no longer shares tables with Board.

### Fixed

- **Skin shop on the server.** It no longer loads on the server (it had no `ClientOnly`).
- **Skin requests.** They're rate limited (4 per 2 s) and Ids are validated. Setting the crate product id mid-session no longer errors.
- **Cursor in the arena.** It no longer stays visible after you leave the lobby holding a gun.
- **Stale shop state.** The shop briefly showed the old "Equipped" state after equipping.
- **Music.** It stored the playlist folder as the "current song".

### Added

- **Docs.** `docs/SKINS.md`, `docs/LOBBY.md` and `docs/KILL_FEED.md`, plus a DoorBoard section in `docs/BREAKABLES.md`.

## 2026-11-08: Breakable boards and the Interact key

### Added

- **Breakable boards.**
  - At server start, every part tagged `Board` is replaced with `Assets.Models.Board`, positioned by its BasePart.
  - Damage removes the spray paint first, then planks from the highest number down (planks 60 HP, spray paint 25 HP).
  - Broken pieces hide and stop blocking players and bullets.
- **Board repair.**
  - Hold the Interact key on the board's prompt to place the next missing piece: planks 1 to N, then the spray paint last.
  - The server checks distance, cooldown and order.
  - Numbers are in `Content.Breakables.Definitions.Board`.
- **Guns damage boards.** Every bullet, including shotgun pellets and ricochets, damages the board piece it hits, and explosive rounds damage boards in their blast radius. Intact planks stop bullets like walls.
- **`Systems.Breakables.BreakableService`.** A weapon-agnostic API (`Damage`, `DamageRadius`, `Repair`, `Reset`, `IsBreakable`, `Get`) with `Breakable.*` extension points. New breakable types come from the data-driven `Content.Breakables` registry.
- **Interact keybind.** A rebindable Interact action (default E, gamepad DPad Up) in Settings > Controls. Every ProximityPrompt uses the player's Interact key and updates live when it is rebound (`Client.Interact.PromptKeys`).
- **Effects.** `BoardBreak` and `BoardPlace`, with ProSoundEffects wood-crack, hammer and spray-can sounds and a pooled `BoardDust` burst.
- **Docs.** New `docs/BREAKABLES.md`.

## 2026-11-08: Crouch on C, prone on Left Ctrl

### Changed

- **Controls.** C crouches (or slides while sprinting) and Left Ctrl goes prone; press Left Ctrl again to get up. Z no longer does anything by default.
- **Second crouch key removed.** `CrouchAlt` (Left Ctrl) is gone from `Shared.PlayerSettings`. The Settings menu now shows one "Crouch / slide" row (C) and "Prone" (LCtrl).
- **Saved keybinds move over.**
  - When keybinds load, `Client.Settings.Keybinds` moves a saved Prone still on the old default Z to Left Ctrl, and saves it through `Packets.Settings.Keybind`. It doesn't move it if the player already put another action on Left Ctrl.
  - Old profiles keep an unused `CrouchAlt` field, which Scribe loads without errors.
  - To move another default later, add its old key to `MOVED_DEFAULTS`.
- **Unchanged:** gamepad (B: tap crouch, hold prone) and touch (Crouch button: tap or hold).

### Fixed

- **Gun clipping into the camera.** Parts of the gun could come closer to the camera than its near clip plane, at high FOV and in the crouch and prone poses, which cut them off. When any part gets within `Config.ViewmodelNearClearance` (0.15), the viewmodel now eases forward along the view axis, never closer than `Config.ViewmodelNearMin` (0.11). Moving along the view axis keeps aimed sights centered. Built by an agent that was stopped before writing its report, so this hasn't had its full playtest yet.

## 2026-11-08: Prone, and viewmodel and tracer fixes

### Added

- **Prone.**
  - Lie down with Z (rebindable), hold gamepad B or hold the touch Crouch button. Press again, crouch, jump or sprint to get up; you stay down under anything too low to rise into.
  - Crawls at `ProneSpeed` (3.5). The eye is about 1.3 studs above the floor, and spread is best here (`Spread.Prone`, default 0.5).
  - No jumping and no footsteps. `ProneCooldown` applies between going down and getting up, on both client and server.
  - Sets the `Prone` attribute and StateHandler state, and adds the `Movement.PreventProne` extension point.
  - Third person: the body tips flat onto its front through `MovementPoses`, or plays `Config.Animations.Prone` if set. The viewmodel gets a braced prone pose.
  - The server registers the `ProneBody` collision group; the prone player's own body parts use it so the lowered torso can't lift the character.

### Fixed

- **Viewmodel disappearing or flickering while sliding and crouch-walking.** The viewmodel judged first person by the camera's distance to the head. The crouch and slide camera offsets and body poses pushed that past 1.5 studs. It now uses the camera mode and the camera's distance to its focus.
- **Shots starting at the camera.** Tracers and the muzzle flash now always start at the gun: the viewmodel muzzle while it's drawn, else the held Tool's muzzle. Before, they started at the camera whenever the viewmodel was hidden.
- **Stance changes read as falling.** Lowering the body (crouch, slide, prone) drops it onto the floor; that short fall no longer counts as the Air state.
- **Standing-up headroom check.** It now measures from the root part instead of the posed head.

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

### Fixed

- **Aim tilt on newer R15 rigs.** Other players' upper bodies follow their aim again on characters whose joints are `AnimationConstraint`s, the newer Roblox avatar joints this place uses. `GunEffects` turns the constraint's `Attachment0` there, and still turns `C0` on `Motor6D` joints. Before, it only handled `Motor6D` and did nothing on these rigs.

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
