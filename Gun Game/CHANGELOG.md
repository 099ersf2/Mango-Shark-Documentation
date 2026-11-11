# Changelog

## 2026-11-11: Shotgun idles fixed

### Fixed

- **Both shotgun idles** (Shotgun, SiegeShotgun) held the gun too far back, with the stock up over the shoulder.
  - **Cause:** the gun slides back when the left hand can't reach the front grip. Held out to the side, a shotgun met no body to stop it.
  - **Slide limit:** the slide is now capped at 0.45 studs.
- **One idle for every long gun:** the long-gun idle, sprint and reload are now placed by the grip, not the rear sight, which sits in a different spot on every gun (on a shotgun it's on the grip). Every long gun now idles in the same low ready: the hand at the right of the chest, the stock at the right shoulder, the muzzle 25 degrees down and a little across the body.

Checked on the gun range:
- **Shotguns:** both are in the low ready, seen from the side.
- **Fit, all 72 rigs:** clipping 0.01 studs at most, and the right hand always on the grip.

## 2026-11-11: Guns held higher

### Fixed

- **Long guns were still held too low** (around the waist when aiming). The step that brings the left hand to the front grip was pulling the gun down toward the left shoulder. It now only slides the gun straight back, level, and the left hand holds as far along the gun as it reaches.
- **The poses are higher:** long guns aim with the sights at eye level beside the right cheek, idle and reload sit at chest height, and the pistol idle is higher.

Measured on the gun range, all 72 rigs:
- **Long guns aiming:** the sight sits at eye level (+0.10 from the head center); before, it was at -0.25 and 0.38 studs to the wrong side.
- **Long guns at idle:** chin/shoulder height.
- **Fit:** clipping 0.02 studs at most, and the right hand always on the grip.

## 2026-11-11: Guns no longer sit low in the hand

### Fixed

- **Long guns** (Rifle, BurstRifle, LMG, Shotgun, SiegeShotgun, Tactical_Bullpup_1, SiegeCarbine) **sat too low in the hand.** The hand gripped the middle of the gun's short pistol grip, so the gun sank into the fist. `GunService` now sets each gun's grip on equip from the holder's own hand size, so the top of the fist sits just under the gun body (`fitGrip`). This applies to every gun and every avatar's hands.

Measured on the gun range: every gun's body sits on top of the fist (0.03 studs above it) in all 72 rigs. The guns moved up 0.24 to 0.41 studs relative to the hand. The other fit checks held: clipping at most 0.15 studs, and the left hand 0.16 studs from the front grip on average.

## 2026-11-11: Third-person guns fixed: no more guns through heads, revolvers fixed

See [docs/THIRD_PERSON_GUNS.md](docs/THIRD_PERSON_GUNS.md).

### Fixed

- **Guns stuck out of characters' heads and bodies.** The gun models are far bigger than an R15 character can hold (a full rifle is 4.4 studs; an arm reaches 1.7). Third-person guns are now scaled to fit: long guns about 2.2 studs, pistols and revolvers about 1.15. The first-person view and gameplay are unchanged. The poses also keep every part of the gun out of the head and torso; a stock may rest slightly into the shoulder.
- **Revolver animations were wrong.** Their long barrel made them count as rifles (sight half a stud from the face, rifle sprint carry). Guns are now sorted by whether they have a stock, so revolvers use the pistol poses.
- **The left hand on long guns** now goes as far toward the front grip as it can reach instead of dragging the gun into the body.

### Changed

- `Content.Guns.Skins` scales skins by a gun's `ModelScale`, so skins fit the smaller third-person guns.
- `ThirdPersonGuns.Report()` gives each character's gun fit, for checking.

Measured on the gun range, all 72 rigs:
- **Clipping:** at most 0.10 studs into the body.
- **Right hand:** always on the grip.
- **Left hand:** 0.19 studs from the front grip on average.

## 2026-11-11: Gun animation range

See [docs/GUN_SHOWCASE.md](docs/GUN_SHOWCASE.md).

### Added

- **A gun range with 72 rigs** (`workspace.GunShowcase`, east of the map): one per gun (12) and animation (idle, walk, sprint, aim, shoot, reload), each doing only that one, for real.
  - **Shoot:** fire real bullets at their lane's target in the gun's own rhythm and reload when empty.
  - **Reload:** reload on a loop.
  - **Walk and Sprint:** pace their lanes.
  - **Aim:** aim at their target.
- **Driver:** `Systems.Showcase.GunShowcase` runs them; the rigs can't be hurt.
- **The `range` command** (alias `showcase`) takes you there.

### Changed

- `Client.Guns.ThirdPersonGuns` treats only an Ammo drop of at most 3 rounds as a shot. It also poses `GunShowcase`-tagged rigs; `Client.Guns.GunEffects` draws their tracers.

Tested in a playtest:
- **Guns:** all 72 rigs were armed.
- **Shooters:** every one fired and reloaded.
- **Lanes:** the walk and sprint rigs moved.
- **Visible:** muzzle flashes and tracers showed.
- **Errors:** none.

## 2026-11-11: Third-person gun animation for every gun

See [docs/THIRD_PERSON_GUNS.md](docs/THIRD_PERSON_GUNS.md).

### Added

- **Other players and NPCs now hold, aim, shoot and reload guns properly** in third person, for all guns (`Client.Guns.ThirdPersonGuns`). Before, every gun's animation slots were empty and characters used Roblox's one-arm hold.
  - **Idle:** a two-handed low ready, with a walk bob.
  - **Sprint:** long guns are carried across the chest, pistols held low.
  - **Aim:** the sights come up to the eyes and follow where they look, with the waist and head following too.
  - **Shoot:** a recoil kick on every shot (pistols 13 degrees, shotguns 10, rifles 5).
  - **Reload:** the left hand goes to the magazine, down to the belt and back, with the magazine hidden while it's out.
  - **Lower body:** the legs keep the normal walk and run.
- It is code, not animation files: each gun is posed from its own sight and grip attachments with IK, so new guns work with nothing to upload. Long guns slide back toward the body until both hands reach their grips.
- New shared state: `GunAiming` (characters), `Reloading` (gun tools), `AimPitch` (NPCs).

### Changed

- The old third-person aim tilt in `Client.Guns.GunEffects` is replaced by the new system.

Tested in a playtest on the test-area NPCs:
- **Pistol aim:** the sight sat 1.17 studs in front of the eyes, on the aim line.
- **Idle:** the left hand sat on the front grip (0.00 studs) for the pistol, burst rifle and shotgun.
- **Reload:** the full magazine path.
- **Shotgun shots:** they kicked the barrel to about 11 degrees.

## 2026-11-11: Pistol shoot animation (Rig2)

### Added

- **A "Pistol Shoot" animation** for the R15 rig `Workspace.Enemies.Rig2` and the Pistol it holds, saved as `ServerStorage.RBX_ANIMSAVES.Rig2."Pistol Shoot"` (open it in the Animation Editor). It is 0.3 s, plays once, priority Action, and moves only the upper body (waist, neck, both arms), so it layers over walking:
  - 0 s: an aimed two-handed stance: barrel level and straight ahead, the rear sight on the eye line 1.16 studs in front of the eyes, the support hand on the pistol's `LeftGrip` point.
  - 0.04 s: the kick: muzzle up 13.5 degrees and pulled 0.2 studs toward the face, hands still on the gun.
  - 0.12 s: settling (muzzle 2.7 degrees up), easing back.
  - 0.3 s: back on target.
- The poses were solved from the rig's real joints (its `AnimationConstraint`s and attachments) and the pistol's attachments, not hand-placed. The solved joint angles are kept on Rig2 as the `SolvedAimPose` and `SolvedKickPose` attributes (JSON) to build more pistol animations from.

Checked in a playtest: played on Rig2, the barrel pointed within 0.7 degrees of straight ahead at the aim frame and 13.5 degrees up at the kick frame (screenshots).

## 2026-11-11: Death screen and spectating the killer chain

See [docs/DEATH_SCREEN.md](docs/DEATH_SCREEN.md).

### Added

- **A new death screen** (`Main.DeathScreen`, `Client.Hud.DeathScreen`): who killed you (a player's avatar, or an NPC's name), the weapon, and the respawn countdown.
- **Spectating your killer** in a third-person camera that follows behind them smoothly and never goes through walls. **If your killer dies, you watch their killer**, and so on; **with nobody to watch, the camera stays on your body**. When you respawn, the camera goes back to you. Works for NPC killers and outside matches too (`Systems.Combat.DeathCamService`).
- The `Combat.Death` extension point: every death, credited or not, with its attacker and weapon.

### Changed

- The old death screen in the match HUD (`Main.MatchHUD.DeathScreen`, `Packets.Match.Death`), which only followed player killers in first person, is removed; `Packets.Death` replaces it.

Tested in a playtest: killed by the Soldier NPC, the camera followed it; when the Breacher killed the Soldier, it moved to the Breacher; when the Breacher died with no killer, it went back to the body; on respawn it went back to the new character.

## 2026-11-11: Quicker, smoother movement and faster slides

See [docs/MOVEMENT.md](docs/MOVEMENT.md) (Tuning).

### Changed

- **Faster movement**: walk 17, sprint 26, tactical sprint 31, crouch 9 studs/s (was 16 / 23 / 27 / 8). Speed changes ramp almost twice as fast (acceleration 80, deceleration 100), and air control is stronger, so starting, stopping and turning feel snappier.
- **Faster, longer slides**: a slide starts at 38 studs/s or 1.35 times your speed (up to 52), loses speed more slowly, and ends at 15 instead of 11. A full slide now lasts about 1.1 s and covers about 29 studs (was about 0.8 s and 20). It steers better and can be used again after 0.45 s (was 0.75). A slide-jump keeps 90% of its speed.
- **A slide that ends in a sprint keeps its speed**, instead of the sprint ramping up again from crouch speed (the slow part after a slide).
- The camera drops into a slide or crouch and its field of view changes a little quicker.
- The server's speed check allows slide speed for 2 s after a slide (was 0.6 s), to cover the longer slides.

Measured in a playtest: a full slide lasted 1.1 s, peaked at 37 studs/s and covered 29 studs, then went straight back into a sprint.

## 2026-11-11: Siege-style scout drones

See [docs/DRONES.md](docs/DRONES.md).

### Changed

- **The drone system is rebuilt from scratch**, modeled on Rainbow Six Siege's drones, in the framework's structure: `Content.Drones` (settings), `Systems.Drones.DroneService` (server), `Client.Gadgets.DroneController` (client), with a new UI built in Studio (`StarterGui.DroneFeed`, `Main.DroneSlot`, mobile buttons). The old system (`DroneService` Script, `DroneController` LocalScript, `DroneRemote`, its model) is archived, disabled, in `ServerStorage.Archive.OldDroneSystem`.

### Added

- **Throw a drone with 5 and look through it at once**; 5 or X leaves it.
- **Fast, smooth driving**: 24 studs/s, quick to start and stop, the drone turns with your look. **Hop** (Space), **boost** (Shift, 36 studs/s, an empty bar locks for 6 s), a camera that eases landings and leans into turns.
- **Spotting**: the Fire button marks the enemy in the crosshair for your team for 8 s (red outline and marker).
- **Drones have health (30)** and can be shot or blown up by anyone but the owner's team. A destroyed drone shows "SIGNAL LOST" and **comes back after 30 s**.
- **NPCs deal with drones**: they see them up close (55 studs, players first), hear them driving, are woken by them, and shoot them down.
- Your body stays where you left it; taking damage drops you out of the drone. Gamepad (DPad Left / Down) and touch controls.

### Changed the same day, after your playtest

- **One drone out at a time; 5 goes in and out, X goes out**: 5 takes you into your drone where you left it while it lives, and throws a new one only when it is gone and the cooldown is done. In the drone, 5 or X takes you back to your body. X never puts you in. The touch CAMS button is gone (DRONE goes in, the feed's EXIT leaves).
- **The respawn cooldown is 30 s** (was 18).
- **Fixed: X put you straight back into the drone** (and 5 threw a new one) when you used it to leave: the same key press reached the on-foot key too.
- **Your body stays visible** while you look through the drone (first person was hiding it).
- Q / E (switch drones) and the touch NEXT button are gone, since there is only one drone.

Tested in a Studio playtest: a throw lands and is handed to the client, the feed opens with the HUD and gun viewmodel hidden, the HUD count and cooldown work, and NPCs shot drones down. Fixed during the test: destroyed drones were never removed (a Humanoid without a state machine never fires `Died`), a thrown drone slid 100 studs while its physics changed hands, and the gun viewmodel drew over the drone camera.

## 2026-11-11: Modular matches and our own teams

See [docs/MATCH.md](docs/MATCH.md).

### Changed

- **The round system is rebuilt as a modular match system** (`Systems.Match.MatchService`), replacing the fixed Red vs Blue `Systems.Round.RoundService`, `Content.Round` and `Client.Hud.RoundHud`. A mode is one ModuleScript in `Content.Match.Modes` (data plus optional hooks); three ship: **Team Deathmatch**, **Free-for-All** and **Elimination** (rounds, no respawns).
- **Our own team system** (`Systems.Match.TeamService`, `Content.Match.Teams`) replaces Roblox `Teams`: a player's team is the `Team` attribute. Red, Blue, Green and Yellow; up to 4 teams a match; team spawns from a SpawnLocation `Team` attribute or an automatic split of the arena. NPCs, aim assist, NPC hearing and friendly fire read it.
- **The match UI is redone in the style of the other menus:** a top bar with a score chip per team, a status line and result banner, a Tab scoreboard (replacing Roblox's player list), the death screen, and teammate outlines.

### Added

- **Match settings an admin can adjust** (`Content.Match.Settings`): time limit, score limit, rounds to win, number of teams, respawn delay, friendly fire, auto-balance, players to start, intermission. Each mode picks which it uses and its defaults; the server cleans every value.
- **The Match menu** (M, `Main.MatchMenu`, admins only): pick the next mode, adjust its settings, start, end or restart a match. Also Cmdr: `match start|end|restart`, `matchmode`, `matchset`.
- `MatchService.AddScore` for objectives, and extension points `Match.Started`, `Match.RoundStarted`, `Match.Scored`, `Match.Ended`, `Team.Changed`.
- Keys: **Scoreboard** (Tab) and **Match setup** (M) in Settings > Controls.

Tested in a Studio playtest with one player: waiting, admin start, team assignment and team spawns, the score limit ending Team Deathmatch and Free-for-All, an Elimination round ending and the next starting, setting cleaning, the admin packet, the HUD and the menu.

## 2026-11-10: Team deathmatch rounds

See [Team deathmatch rounds](ROUND_SYSTEM.md). *Replaced on 2026-11-11 by the modular match system ([docs/MATCH.md](docs/MATCH.md)); Team Deathmatch is now one of its modes.*

### Added

- **Three-minute Red vs. Blue rounds.** The server balances arena players, tracks credited enemy-player kills, and awards the round to the team with the higher kill total (ties are draws). Rounds require two arena players and have a ten-second intermission.
- **Match HUD and death spectating.** The HUD displays team totals and the ten highest-kill players with profile thumbnails. On death, the victim sees a death screen and follows the credited killer until respawn.
- **Friendly-fire protection during active rounds.** Teammate damage is blocked by the server; self-damage remains unchanged.

### Changed

- The kill-feed death hook now reports a credited player death to the round service before clearing its damage record.

### Fixed

- None.

## 2026-11-10: NPCs board up doors and windows

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics, Board up).

### Added

- **NPCs rebuild broken door and window boards when they need to hide or hold.** When their health is low and they know where you are, or you hit them from out of sight, they board up a broken door or window between you and them (on their floor, within 25 studs). When they hold a room they secured, they seal its broken doors and windows. They walk to the inside, face the board and put a piece back every 0.6 s (`BreakableService.Repair`), stopping at once to fight if they can see and shoot you. Tested: a wounded Soldier boarded a fully broken door back up in 4-5 s; a healthy one with no threat left it alone; one holding a room sealed both of its doors.

### Fixed

- NPCs marked a door or board as unreachable when an older, unrelated path failed just after they picked it; now only a failed path to that door counts.

## 2026-11-10: NPCs stop shooting glass and come for you

### Fixed

- **NPCs shot at you through unbreakable see-through walls.** Their "can a bullet reach" check counted a hit within 2 studs of you, and glass right in front of you is that close. At a person they now only fire when the bullet reaches that person; behind glass they go after you instead.
- **NPCs couldn't walk while they saw a target.** Turning set the root's CFrame every frame, which stopped them walking. They now turn with an `AlignOrientation`, so they face you and move at the same time.
- **Paths to a person failed.** Path goals were the person's root, inside their body, which pathfinding refuses. Paths now go to the floor under the goal (`Brain.Ground`).
- **NPCs didn't find the door into your room** when it was round a corner. They now check the nearest doors, boards, soft walls and windows by pathfinding from just inside each to you (`Brain.Connected`) and break the first that leads in.
- Trapped NPCs look for a way into the target's room before breaking out of their own; a failed search retries after 4 s (was 10).

Tested: a Soldier facing the test Rig behind the glass held fire, went round, cut through a soft wall and was in the room shooting the Rig 4.5 s later.

## 2026-11-10: NPCs move, hunt and get around

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics).

### Fixed

- **NPCs stood still.** They wandered only near their spawn, and froze or walked into walls when a path failed, and some were shut in rooms with no path anywhere. Now: wander points 20-90 studs away on their own floor, paths through corridors about 3 studs wide, the closest reachable path when there's no full one, faster re-pathing when stuck, and **breaking out** of rooms they're shut in (through a board, soft wall or window). Live: NPCs moved in 30-37 of 40 samples (was 21 for the Grenadier), and a Grenadier trapped upstairs broke a window board, climbed out and dropped down.
- **NPCs stared through glass.** Seeing a target they can't shoot, they now go after it and break in if they must.
- **NPCs walked into boards.** A board or soft wall right ahead on their path is broken on the spot.
- **Shooting at hidden players** is shorter: 1.2 s after the last reason (was 2.5), 1.5 s after losing sight (was 3). NPC bullets only pass soft walls and boards, like players' (0 of 14 logged hits went through anything solid).

### Added

- **NPCs turn toward where a hit came from** when they can't see the shooter, and hunt there.
- **NPCs hear boards being rebuilt** (`Breakable.Repaired`) within 60% of their hearing range.
- **NPCs climb through windows**, including after breaking a window's board, and drop from upper floors.

## 2026-11-10: NPCs decide to break in

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics).

### Added

- **NPCs decide when boards and soft walls must be broken to get in.** Going after a hidden enemy, or a room they're securing, they breach when there's no path, they're stuck, or the way round is much longer than going through (over 1.8x + 20 studs). They pick the door-height board or soft wall that opens onto the room on the shortest trip, walk to it (lobbing a grenade when the arc is clear), and **bash** or **shoot** it until a person fits, then walk in. Tested: the Breacher broke in through a door board with one shotgun blast and secured the room in 2 s; the Grenadier bashed it open and was in within 8 s.
- **Secure rooms.** Tag a part `NPCSecure` inside a room and idle NPCs go clear it (breaking in if they must), hold it a few seconds, and move on. A fight interrupts them; they go back after.

### Fixed

- **NPCs stood still when told to face a spot while walking a path.** Facing set the root's CFrame every frame, which stopped the walk; they now face where they walk until they stop.
- NPCs no longer pick a window as a way in; entrances must reach from near the floor to above head height.

## 2026-11-10: Smarter NPCs

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics).

### Added

- **Every NPC hears gunshots** (new `Hearing`, 150 studs, through the new `Gun.Fired` extension point). If it can't see the shooter it turns to the sound and hunts there.
- **Shoot to test.** An NPC that just lost sight of you, or heard you, fires at that spot through soft walls, soft floors, boards or smoke (never into open air or solid walls), and keeps firing while it keeps hearing you.
- **Breaching.** When an NPC has no path to where you are (a sealed room) and a board or soft wall is in the way, it shoots it open, then walks in once pathfinding finds the opening.
- **NPCs see through windows** (glass, or parts at least 0.3 transparent). They only fire when a bullet can actually reach you; otherwise they look for a way in.
- **NPC grenades.** Every NPC carries a frag grenade (`Grenades` 1, the Grenadier 3). It throws when you hide (1–8 s) or peek with only your head over cover (2.5 s), solving an arc that clears walls, never inside its own blast or near a teammate. Tested: a Soldier behind a 9-stud wall threw over it (peak 15.5 studs) and the grenade went off 0.6 studs from the hidden spot; it held its grenade for a spot 10 studs away, a spot by a teammate, and one 80 studs away.
- **NPCs dodge grenades.** Any NPC within a live grenade's blast (+4 studs) with no solid cover runs straight away, still shooting what it can see. Tested: two NPCs 4.5 studs from a grenade got 21–23 studs away before it went off and took no damage.
- `ConsumableService.ThrowAs(model, id, start, velocity)`, `NPCService.Agents()`, `Brain.SeeThrough` / `Penetrable` / `ShootThrough` / `BreachPoint`, and a `DetonateAt` attribute on thrown parts.

### Changed

- **Soft walls, soft floors and boards are no longer cover** for NPCs: bullets get through them.
- `ConsumableService.Detonate` takes an NPC model as the attacker (kill feed credit). NPC grenades don't hurt the thrower's teammates.

## 2026-11-10: Grenade lands heavy and breaks more

### Changed

- **Grenades and smoke bombs stay near where they land.** They're heavy and barely bounce, keep half their speed on landing, then roll about 2–4 studs to a stop (`Bounce`, `LandingKeep`, `RollDrag` in `Content.Consumables`). They used to roll away like a light ball.
- **Grenades remove more of boards and soft walls.** Board damage 80 → 350: a blast 4 studs from a board strips all 6 pieces (it took 2). Soft walls: hole 1.6 → 3.5 studs, reach 6 → 10 studs, up to 6 walls (was 3); a blast 2 studs from a wall removed 9.0 cubic studs of it (2.0 before). Player damage is unchanged. See [docs/CONSUMABLES.md](docs/CONSUMABLES.md).

## 2026-11-10: SMG sound and a new gun bash

### Fixed

- **The SMG's gunfire sound was silent.** The `RifleFire` sound file starts with about 0.3 s of silence. The SMG fires every 0.07 s with 4 pooled copies, so each copy restarted before it reached the bang. Gunfire now skips that silence (`Start = 0.3` on `GunFire_Rifle`; `PooledSound` takes a new `Start` field) and keeps 6 copies per muzzle. Checked: at SMG speed there was sound in 89 of 91 frames (0 of 61 before). This also removes a 0.3 s delay between the shot and the sound for every gun using `GunFire_Rifle` (Rifle, SMG, LMG and others).

### Changed

- **The gun bash is a long straight jab.** The gun pulls back toward the shoulder, then thrusts about 1.6 studs straight forward (full scale) with a slight cant, holds a beat, and snaps back. It stays on its own side of the screen instead of swinging across the middle. No camera shake. Tune the `BASH_*` constants in `Client.Guns.Viewmodel.Actions`. See [docs/ADDING_GUNS.md](docs/ADDING_GUNS.md).

## 2026-11-10: Tracers no longer come out of your face

### Fixed

- **Your own tracers start out at the barrel.** The viewmodel's muzzle sits about 1.2 studs from the eye (on the crosshair when aimed), so full-size tracers started there looked like they came out of your head. They now start on the same screen line but 4 studs out (`TRACER_START_DISTANCE` in `Client.Guns.GunEffects`), or just in front of a closer wall or target. Checked in a playtest: hip and aimed tracers first appear 4.0 studs out, at the barrel's spot on screen. Hits are unchanged (still from the camera). See [docs/ADDING_GUNS.md](docs/ADDING_GUNS.md).

## 2026-11-10: Stronger head aim assist

### Changed

- **Aim assist favors the head.** The head now wins about two thirds of the space between head and chest, gets 1.4× friction and 1.6× pull, and the assist sticks to the point it locked last frame so a small wobble doesn't drop it to the chest. Tuning: `HEAD_PREFERENCE`, `STICKY`, `HEAD_FRICTION_BOOST`, `HEAD_PULL_BOOST`, `MAX_FRICTION` in `Client.Guns.AimAssist`. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

## 2026-11-10: Aim assist holds headshots

### Changed

- **Aim assist sticks to the head or the chest, whichever is nearer the crosshair.** It used to know only the chest, so aiming at a head got pulled down to the body. Now aiming near the head holds the head. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

## 2026-11-10: Aim assist on PC for testing

### Added

- **`aimassistpc <player> [true/false]`** (alias `aapc`), an admin Cmdr command that gives a player controller aim assist on mouse and keyboard, so it can be tried on PC. With no true/false it toggles. It sets the server-side player attribute `AimAssistPC`, which `Client.Guns.AimAssist` reads; the Aim assist setting must also be on. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

## 2026-11-10: AI coding guide

### Added

- **[docs/AI_CODING_GUIDE.md](docs/AI_CODING_GUIDE.md):** one file to give any AI agent before it codes in the FPS place: the hard rules, where code lives, how ModuleLoader loads it, the module template and code style, the shared building blocks (packets, extension points, Scribe data, effects, states, input, Cmdr, products), world conventions, a feature walkthrough, testing and docs standards, and a done checklist.

### Fixed

- `API.md` said `Content` isn't loaded by ModuleLoader. It is, on both sides; most Content modules just return a table.

## 2026-11-10: Stronger aim assist

See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

### Changed

- **Aim assist is stronger** (controller and touch). Cone 12° at the hip and 9° aimed (was 7° / 5°), covering 4 studs of body up close (was 2.2). Friction 50% / 70% (was 35% / 50%). Pull 7 / 11 per second (was 3 / 5), up to 120° per second (was 40°). The fade toward the cone's edge is now squared, so it stays strong over most of the cone. It still never moves the aim while the player is still.
- **Test rigs count as enemies.** `Rig`, `Rig1` and `Rig2` moved into `workspace.Enemies`, so they get health bars and aim assist.

## 2026-11-10: Grenade and smoke bomb

See [docs/CONSUMABLES.md](docs/CONSUMABLES.md).

### Added

- **Consumables.** Each player carries a frag grenade or a smoke bomb, picked in the Loadout menu (saved). They get 2 per life; the count refills on respawn, so it resets on death.
- **Throw with G** (rebindable, "Throw grenade / smoke"), gamepad DPad Right, or the NADE / SMOKE touch button (`Main.Mobile.ConsumableButton`, left of BASH, showing the count). A HUD line above the ammo box shows the name and count on keyboard and gamepad.
- **Frag grenade:** bounces, explodes after 3 s. 120 damage at the center falling to 15% at 16 studs, only through clear view, half damage to the thrower, kill feed credit and hitmarkers. It damages boards and holes nearby soft walls.
- **Smoke bomb:** pops after 1.5 s into a 13-stud cloud for 15 s. NPCs can't see through it and aim assist ignores targets behind it (`Shared.Smoke`).
- New: `Content.Consumables`, `Systems.Consumables.ConsumableService`, `Client.Guns.Consumables`, `Shared.Smoke`, the `Consumable` packets, the `Thrown` collision group, the `ConsumableThrow` and `SmokePop` effects, models in `Assets.Models.Consumables` and the `Assets.Vfx.SmokeCloud` particles.

## 2026-11-10: Touch buttons for bash and Cmdr

### Added

- **BASH touch button** (`Main.Mobile.BashButton`), above FIRE, shown with the other gun buttons; it does the same gun bash as Q.
- **CMD touch button** (`Main.Mobile.CmdrButton`) that opens the Cmdr bar, shown only to admins in `Classes.Admins`. The server still checks every command.

## 2026-11-10: API reference

### Added

- **[docs/API.md](docs/API.md)**: one page covering every public function, extension point, packet, Cmdr command, attribute, tag, data field and collision group, with recipes for common jobs.

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
- **`Shared.ProductIds`**: one module for every developer product and game pass id. The skin crate reads `Products.SkinCrate` from it instead of the old `SkinCrateProductId` attribute.
- **Crate refund.** Buying a crate with every skin owned gives 500 coins (`Skins.CRATE_REFUND_COINS`).

- **Aim assist for controller and touch** (`Client.Guns.AimAssist`): friction and a gentle pull toward enemies, stronger when aimed, never on mouse. Settings > Toggles turns it off. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).
- **The HUD scales with the screen.** Health, ammo, weapon slots and kill feed are sized in scale with aspect locks. On touch, the ammo box moves above the health bar, the weapon slots go top left, and small screens get a bigger HUD. The touch buttons keep their original pixel layout.

- **Skin crate product is live.** "Skin Crate", 499 Robux, product id `3730208338`, in `Shared.ProductIds`.

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
