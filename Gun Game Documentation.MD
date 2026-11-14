# Gun Game

The home page for the FPS place's gun system docs. Start with **Adding guns** to make a new gun, read **Gun system** to see how a shot works, and check the **Changelog** for what shipped.

| Doc | Read it when |
| --- | --- |
| [Music](Gun%20Game/MUSIC.md) | You are adding songs, or changing when the music changes (match start, the last 30 seconds, the end) |
| [UI](Gun%20Game/UI.md) | You are adding or changing any UI: the look, the lobby's PLAY bar, button sounds and effects, touch sizes |
| [Siege](Gun%20Game/SIEGE.md) | You are working on the game mode: the phases, the map it needs, planting, cameras, spectating, the scoreboard |
| [Matchmaking and parties](Gun%20Game/MATCHMAKING.md) | You are working on the queue, parties, the matchmaker, or how players reach a reserved server and come back |
| [Classes](Gun%20Game/CLASSES.md) | You are adding or tuning a Siege class or its ability |
| [Gun animation range](Gun%20Game/GUN_SHOWCASE.md) | You want to see every gun's third-person animations side by side (the `range` command) |
| [Third-person gun animation](Gun%20Game/THIRD_PERSON_GUNS.md) | You are changing how other players and NPCs hold, aim, shoot and reload guns |
| [Death screen](Gun%20Game/DEATH_SCREEN.md) | You are working on what a player sees after dying, or spectating |
| [Scout drones](Gun%20Game/DRONES.md) | You are tuning the drones, their UI, or how NPCs deal with them |
| [Matches and teams](Gun%20Game/MATCH.md) | You are adding a game mode, a team, or changing match settings |
| [AI coding guide](Gun%20Game/AI_CODING_GUIDE.md) | You are giving the codebase to an AI agent: the rules, structure and code style it must follow |
| [API](Gun%20Game/API.md) | You want to control something from code: every function, hook, packet, command, attribute and tag |
| [Adding guns](Gun%20Game/ADDING_GUNS.md) | You are adding a gun or ability, or something isn't working |
| [Gun system](Gun%20Game/GUN_SYSTEM.md) | You need the shot flow, packets or state behind the system |
| [Adding NPCs](Gun%20Game/ADDING_NPCS.md) | You are adding an NPC type, a behavior-tree task or a kill sound |
| [Movement](Gun%20Game/MOVEMENT.md) | You are tuning sprint, crouch, slide or camera feel, adding a movement state, or working on the FOV setting |
| [Breakables](Gun%20Game/BREAKABLES.md) | You are working on boards or another breakable object, or a weapon that should damage them |
| [Soft walls](Gun%20Game/SOFTWALLS.md) | You are placing walls bullets punch holes through, tuning penetration, or making a weapon cut holes |
| [Store](Gun%20Game/STORE.md) | You are adding a crate, a store item, a game pass, a currency reward, or reading wins, losses and streaks |
| [Skins](Gun%20Game/SKINS.md) | You are adding a weapon skin, working on the skin shop, or setting up the skin crate product |
| [Lobby](Gun%20Game/LOBBY.md) | You are working on the lobby, its portals, first spawn or the `InLobby` attribute |
| [Consumables](Gun%20Game/CONSUMABLES.md) | You are tuning the grenade or smoke bomb, or adding a consumable |
| [Aim assist](Gun%20Game/AIM_ASSIST.md) | You are tuning aim assist for controller and touch, or checking what counts as a target |
| [Kill feed](Gun%20Game/KILL_FEED.md) | You want a weapon's kills in the kill feed, are restyling it, or are using `nuke` |
| [Design decisions](Gun%20Game/DECISIONS.md) | You want to know how a design question was answered (lobby, skins, guns, bash, walls) |
| [Changelog](Gun%20Game/CHANGELOG.md) | You want what changed in the place, newest first |

## At a glance

- **A gun is one definition file plus one model.** Definitions live in `ReplicatedStorage.Content.Guns.Definitions`, models in `ReplicatedStorage.Assets.Models.Guns`.
- **The server decides every hit.** Clients send a trigger pull with a seed, and the server rebuilds the same bullets from it.
- **Abilities add behavior without core edits.** Scope, Ricochet, Burst, ExplosiveRounds and ShotgunSpread ship as examples in `Content.Guns.Abilities`.
- **Aiming uses iron sights.** Every starter gun aims down a rear notch and front sight, and the crosshair hides while aiming. Scope is kept for a future sniper.
- **Hits sound different.** Your own hits play a body-hit sound, and headshots play a distinct headshot sound.
- **Loadouts.** Six loadouts of up to three guns plus a knife. The Loadout menu is not reachable since 2026-11-12 (no key, no lobby button); in Siege, guns come from the class.
- **No hotbar.** Switch guns with 1, 2, 3, the mouse wheel, gamepad L1/R1, or the slots on the right side of the screen.
- **Settings menu (`P`).** Rebind every key; set volumes, field of view (60–110) and camera bob; pick hold or toggle for sprint and crouch. All are saved.
- **Fast movement.** Sprint (Shift), double-tap for a short tactical sprint, crouch (Left Ctrl), go prone (C) to lie down, and slide by crouching mid-sprint, with a slide-jump that keeps momentum. Sprinting blocks firing until the gun's `SprintOutTime`, and the server checks every state and speed.
- **Camera feel.** Smooth crouch height, FOV kicks, strafe and slide tilt, landing dip and head bob, all in one spring stack with gun recoil. Aiming zoom scales with your FOV setting.
- **Learnable recoil.** Each gun has its own spray pattern: the first shots climb straight, then the aim weaves the same way every spray. The aim stays where the spray left it; there's no automatic pull-down (`Recoil.RecoverAim` turns it back on). Aiming, crouching and prone all steady it.
- **NPCs fight with the same guns.** Soldier, Breacher and Grenadier profiles run a behavior tree (find, chase, strafe, take cover, reload) and shoot through the same server path as players. Spawn them with `spawnnpc <profile> [count]`, remove them with `clearnpcs`.
- **Kills sound different.** A kill plays a heavier, lower kill sound; a headshot kill layers it after the headshot sound. One kill, one sound.
- **Aim assist on controller and touch.** Friction and a gentle pull near enemies, stronger when aimed; never on mouse. The HUD scales with the screen, with a touch layout for phones.
- **Grenade or smoke bomb.** Pick one in the Loadout menu; you get 2 per life (refilled on respawn) and throw with G, DPad Right or the touch button. Smoke blocks NPC sight.
- **Test a gun in game** with the Cmdr command `givegun <player> <gunId>`.

## Starter guns

| Gun | Fire mode | Bullets | Ability |
| --- | --- | --- | --- |
| Rifle | Auto, 600 RPM | Simulated, raycast | None (iron sights) |
| Pistol | Semi, 420 RPM | Simulated, raycast | Ricochet |
| Shotgun | Semi, 75 RPM | Hitscan, 8 spherecast pellets | ShotgunSpread |
| BurstRifle | 3-round burst | Simulated blockcast with bullet drop | Burst, ExplosiveRounds |
| SMG | Auto, 800 RPM | Simulated, raycast, 200 studs | None (iron sights) |
| LMG | Auto, 650 RPM, 100 rounds | Simulated, raycast | None (iron sights; slows you to 80%) |
| Revolver | Semi, 140 RPM, 6 rounds, 48 damage | Simulated, raycast | None |
