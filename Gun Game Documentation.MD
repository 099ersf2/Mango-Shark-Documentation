# Gun Game

The home page for the FPS place's gun system docs. Start with **Adding guns** to make a new gun, read **Gun system** to see how a shot works, and check the **Changelog** for what shipped.

| Doc | Read it when |
| --- | --- |
| [Adding guns](Gun%20Game/ADDING_GUNS.md) | You are adding a gun or ability, or something isn't working |
| [Gun system](Gun%20Game/GUN_SYSTEM.md) | You need the shot flow, packets or state behind the system |
| [Adding NPCs](Gun%20Game/ADDING_NPCS.md) | You are adding an NPC type, a behavior-tree task or a kill sound |
| [Movement](Gun%20Game/MOVEMENT.md) | You are tuning sprint, crouch, slide or camera feel, adding a movement state, or working on the FOV setting |
| [Breakables](Gun%20Game/BREAKABLES.md) | You are working on boards or another breakable object, or a weapon that should damage them |
| [Soft walls](Gun%20Game/SOFTWALLS.md) | You are placing walls bullets punch holes through, tuning penetration, or making a weapon cut holes |
| [Skins](Gun%20Game/SKINS.md) | You are adding a weapon skin, working on the skin shop, or setting up the skin crate product |
| [Lobby](Gun%20Game/LOBBY.md) | You are working on the lobby, its portals, first spawn or the `InLobby` attribute |
| [Kill feed](Gun%20Game/KILL_FEED.md) | You want a weapon's kills in the kill feed, are restyling it, or are using `nuke` |
| [Changelog](Gun%20Game/CHANGELOG.md) | You want what changed in the place, newest first |

## At a glance

- **A gun is one definition file plus one model.** Definitions live in `ReplicatedStorage.Content.Guns.Definitions`, models in `ReplicatedStorage.Assets.Models.Guns`.
- **The server decides every hit.** Clients send a trigger pull with a seed, and the server rebuilds the same bullets from it.
- **Abilities add behavior without core edits.** Scope, Ricochet, Burst, ExplosiveRounds and ShotgunSpread ship as examples in `Content.Guns.Abilities`.
- **Aiming uses iron sights.** Every starter gun aims down a rear notch and front sight, and the crosshair hides while aiming. Scope is kept for a future sniper.
- **Hits sound different.** Your own hits play a body-hit sound, and headshots play a distinct headshot sound.
- **Players pick a loadout.** Six loadouts of up to three guns plus a knife; the menu opens on join and with `B`, and the pick is saved.
- **No hotbar.** Switch guns with 1, 2, 3, the mouse wheel, gamepad L1/R1, or the slots on the right side of the screen.
- **Settings menu (`P`).** Rebind every key; set volumes, field of view (60–110) and camera bob; pick hold or toggle for sprint and crouch. All are saved.
- **Fast movement.** Sprint (Shift), double-tap for a short tactical sprint, crouch (C), go prone (Left Ctrl) to lie down, and slide by crouching mid-sprint, with a slide-jump that keeps momentum. Sprinting blocks firing until the gun's `SprintOutTime`, and the server checks every state and speed.
- **Camera feel.** Smooth crouch height, FOV kicks, strafe and slide tilt, landing dip and head bob, all in one spring stack with gun recoil. Aiming zoom scales with your FOV setting.
- **Learnable recoil.** Each gun has its own spray pattern: the first shots climb straight, then the aim weaves the same way every spray. Pull against it and recovery won't undo your correction. Aiming, crouching and prone all steady it.
- **NPCs fight with the same guns.** Soldier, Breacher and Grenadier profiles run a behavior tree (find, chase, strafe, take cover, reload) and shoot through the same server path as players. Spawn them with `spawnnpc <profile> [count]`, remove them with `clearnpcs`.
- **Kills sound different.** A kill plays a heavier, lower kill sound; a headshot kill layers it after the headshot sound. One kill, one sound.
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
