# Gun Game

The home page for the FPS place's gun system docs. Start with **Adding guns** to make a new gun, read **Gun system** to see how a shot works, and check the **Changelog** for what shipped.

| Doc | Read it when |
| --- | --- |
| [Adding guns](Gun%20Game/ADDING_GUNS.md) | You are adding a gun or ability, or something isn't working |
| [Gun system](Gun%20Game/GUN_SYSTEM.md) | You need the shot flow, packets or state behind the system |
| [Changelog](Gun%20Game/CHANGELOG.md) | You want what changed in the place, newest first |

## At a glance

- **A gun is one definition file plus one model.** Definitions live in `ReplicatedStorage.Content.Guns.Definitions`, models in `ReplicatedStorage.Assets.Models.Guns`.
- **The server decides every hit.** Clients send a trigger pull with a seed, and the server rebuilds the same bullets from it.
- **Abilities add behavior without core edits.** Scope, Ricochet, Burst, ExplosiveRounds and ShotgunSpread ship as examples in `Content.Guns.Abilities`.
- **Aiming uses iron sights.** Every starter gun aims down a rear notch and front sight, and the crosshair hides while aiming. Scope is kept for a future sniper.
- **Hits sound different.** Your own hits play a body-hit sound, and headshots play a distinct headshot sound.
- **Players pick a loadout.** Four loadouts of up to three guns; the menu opens on join and with `B`, and the pick is saved.
- **No hotbar.** Switch guns with 1, 2, 3, the mouse wheel, gamepad L1/R1, or the slots on the right side of the screen.
- **Settings menu (`P`).** Rebind every key and set Master, Effects, Music and Interface volume; both are saved.
- **Test a gun in game** with the Cmdr command `givegun <player> <gunId>`.

## Starter guns

| Gun | Fire mode | Bullets | Ability |
| --- | --- | --- | --- |
| Rifle | Auto, 600 RPM | Simulated, raycast | None (iron sights) |
| Pistol | Semi, 420 RPM | Simulated, raycast | Ricochet |
| Shotgun | Semi, 75 RPM | Hitscan, 8 spherecast pellets | ShotgunSpread |
| BurstRifle | 3-round burst | Simulated blockcast with bullet drop | Burst, ExplosiveRounds |
