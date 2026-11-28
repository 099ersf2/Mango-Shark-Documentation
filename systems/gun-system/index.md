# Gun System asset

Gun Game's first-person gun system as one drop-in asset, **without weapon skins**. The server owns ammo, fire rate,
spread, hits and damage; clients only send intent. Players and NPCs shoot through the same rules.

[Download GunSystem.rbxm](GunSystem.rbxm){ .md-button .md-button--primary }

**Needs:** the [Game Template](../../game-templates/game-template.md) installed first. The guns use its loader, packets,
player data, effects, settings, `Combat.ApplyHit`, `StateHandler` and `TokenBucket`.

## Install it

1. In a place that has the Game Template, right-click `ServerStorage.MangoShark`, **Insert from File…**, and pick
   `GunSystem.rbxm`.
2. Command bar, Edit mode:

    ```lua
    require(game.ServerStorage.MangoShark.GunSystem.Install)()
    ```

3. Save the place and press Play. You spawn with the default loadout from `Content.Guns.Loadouts`, a knife in the
   next slot, the gun HUD, crosshair and weapon slots. Open the loadout menu from the menu buttons to switch.

The installer merges into the template's folders and never overwrites: anything the place already has is listed as
"kept yours" and stays in the asset folder.

## What it does

- **Guns:** hitscan and projectile (FastCast2) guns, fire modes, seeded shotgun pellets the server rebuilds, damage
  falloff, headshots, piercing, reloads with a reload bar, aiming down the iron sights, scopes.
- **Feel:** a recoil pattern per gun on a spring camera, gun kick and sway, procedural reload, inspect and bash
  animations, moving parts (slides, cylinders, pumps), muzzle flash, shells, tracers, impacts and bullet holes.
- **Loadouts:** saved per player (the `Loadout` data root), three gun slots plus the knife, switched with number keys,
  the mouse wheel, L1/R1 or the slot strip.
- **Melee:** the knife and a gun bash, checked on the server (`Systems.Combat.GunMelee`).
- **Others see it:** third-person arms aim where the player aims, shots and tracers play for nearby players.
- **Aim assist** for gamepad and touch.
- **Movement and camera:** sprint, crouch, slide, prone and lean with a server check, footsteps by material, and the
  camera the recoil runs in. It ships here because the guns can't work without it.

How each part works is explained on Gun Game's pages: [Gun system](../../Gun%20Game/GUN_SYSTEM.md),
[Adding guns](../../Gun%20Game/ADDING_GUNS.md), [Third-person guns](../../Gun%20Game/THIRD_PERSON_GUNS.md),
[Aim assist](../../Gun%20Game/AIM_ASSIST.md), [Movement and camera](../../Gun%20Game/MOVEMENT.md) and the
[Guns API](../../Gun%20Game/api/systems/guns.md). Ignore their parts about skins.

## What is in it

| Where | Items |
| --- | --- |
| `ServerScriptService.Modules.Systems` | `Guns.GunService`, `Guns.LoadoutService`, `Guns.AbilityRunner`, `Movement.MovementService`, `Combat.GunMelee` |
| `ReplicatedStorage.Modules.Shared` | `Guns.Ballistics`, `Guns.Spread`, `Guns.Spring`, `Guns.Abilities`, `Movement.States`, `BallisticShield`, `Smoke`; `Packets.Guns` and `UnreliablePackets.Guns` (merged into the template's) |
| `ReplicatedStorage.Modules.Client` | `Guns.GunController`, `Viewmodel` (+ `GunModel`, `Actions`), `GunHud`, `GunPreview`, `WeaponSlots`, `LoadoutMenu`, `GunEffects`, `GunMechanics`, `Recoil`, `AimAssist`, `ThirdPersonGuns`; `Movement.*` (4); `Audio.SpatialFootsteps` |
| `ReplicatedStorage.Content` | `Guns.Definitions` (14 guns), `Guns.Abilities` (7), `Guns.Registry`, `Types`, `Loadouts`, `Melee`, `KnifeStats`, `Mechanics`; `Movement.Config`; `Destruction.SoftWallConfig`; `Effects.Registry.Guns` (16 effects) |
| `ReplicatedStorage.Assets` | `Models.Guns` (15 models), `Models.Viewmodel`, the gun and footstep sounds, muzzle flash, tracers, shells, impacts, bullet holes; UI templates `ScopeOverlay`, `LoadoutCard`, `MovementDebug` |
| `ReplicatedFirst.UILoader.Main` | `Gun`, `Crosshair`, `Hitmarker`, `Weapons`, `Loadout` frames |
| `StarterPack` | `Knife` |
| `ServerScriptService.Modules.Services.CmdrSetup` | Commands `GiveGun`, `MoveDebug`, `AimAssistPC`; type `Gun` |

Packets it adds: `Packets.Gun` (`Fire`, `Reload`, `Aim`, `AltFire`, `HitConfirm`, `Loadout` …), `Packets.Melee`,
`Packets.Movement`, and the unreliable `GunFired`, `GunAim`, `GunAimRelay`.

Extension points it fires and asks (`Shared.Extensions`): `Gun.PreventFire`, `Gun.DamageMultiplier`, `Gun.Hit`,
`Gun.Killed`, `Gun.Reloaded`, `Gun.Fired`, plus the loadout and movement points listed in the module headers.

## What was changed from Gun Game

| Change | Where |
| --- | --- |
| **No weapon skins.** No `Content.Guns.Skins`, `SkinShopService`, `SkinShotVfx`, `SkinRainbow`, `WeaponCharms`, skin data fields or the Obsidian effects. Guns always use their own model and effects | `Viewmodel`, `GunModel`, `GunController`, `GunHud`, `WeaponSlots`, `LoadoutMenu`, `GunEffects`, `GunService`, `LoadoutService` |
| The gun pictures in the HUD and weapon slots use a small new `Client.Guns.GunPreview` instead of the store's `ItemDetails` | `GunHud`, `WeaponSlots` |
| Boards, soft walls and the Siege Shield are **optional**: used when the game has `Systems.Breakables`, `Systems.Destruction.SoftWalls` or `Systems.Classes.Abilities.Shield`, skipped when it doesn't | `GunService`, `AbilityRunner`, `GunMelee` |
| Loadout picks are refused while the player's `InLobby` attribute is true (Gun Game also checked the matchmaking server role) | `LoadoutService` |
| Left out: grenades (`Client.Guns.Consumables`), the Shield view, sword combat, the kill feed | — |

## Add or change a gun

1. Put the model in `ReplicatedStorage.Assets.Models.Guns`, with a `Handle`, a `Muzzle` attachment and an `Aim`
   attachment on the sight line.
2. Add a definition ModuleScript in `Content.Guns.Definitions` (copy one close to it, like `AssaultRifle`).
3. Add its gunfire effect to `Content.Effects.Registry.Guns` if it needs a new sound.
4. Put it in a loadout in `Content.Guns.Loadouts`.

Every field is explained on [Adding guns](../../Gun%20Game/ADDING_GUNS.md).

## Verification

| Check | Result (2026-11-27) |
| --- | --- |
| Every script compiles | 75 of 75 |
| No skin code left | No reference to `Skins`, `SkinShotVfx`, `SkinShopService`, `WeaponCharms` or `ItemDetails` |
| Dry-run install of the template and this asset into a sandbox | 86 items added, 0 conflicts, 334 scripts installed, every `require` resolves and compiles |
| Installed from the two `.rbxm` files into an empty Baseplate | 86 items added, 0 kept, 334 scripts |
| Played there (keyboard and mouse) | No errors or warnings in Output. Spawned holding the Assault Rifle (30/150), Pistol in slot 2, Knife in slot 3. Viewmodel, crosshair, gun HUD and slot pictures show. A held click fired 8 rounds: the server's ammo went 30 to 22 and a test dummy went 100 to 0 health. R reloaded to 30/142; key 2 switched to the Pistol |
| Not tested yet | Gamepad, touch, aiming down sights, the knife and gun bash, the loadout menu, other guns |

## Changes

| Date | Change |
| --- | --- |
| 2026-11-27 | First version, taken from Gun Game without skins |
