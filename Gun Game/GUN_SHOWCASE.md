# Gun animation range

A range east of the map (`workspace.GunShowcase`, around x 200 to 310, z -140 to -30) with **one rig per gun and animation, 72 in all**: 12 guns × idle, walk, sprint, aim, shoot and reload. Each rig does only its one animation, for real, so you can compare every gun's third-person animation ([THIRD_PERSON_GUNS.md](THIRD_PERSON_GUNS.md)) side by side.

Get there with the Cmdr command **`range`** (or `showcase`). It puts you on the blue viewing spot at the left of the rows.

## Layout

One lane per gun, left to right: Pistol, SiegePistol, Revolver, SMG, SiegeSMG, Rifle, BurstRifle, SiegeCarbine, Tactical_Bullpup_1, LMG, Shotgun, SiegeShotgun. Rows, from the target wall back:

| Row | What the rig does |
| --- | --- |
| **Shoot** (front) | Fires **real bullets** at its lane's target board through `GunService.FireAs`, in the gun's own rhythm: full-auto bursts of 5 to 9, semi-auto taps, or the gun's bursts. Reloads through `GunService.ReloadAs` when empty. Muzzle flash, sound, tracers and impacts all show |
| **Aim** | Aims at its target board (`GunAiming`, `AimPitch`) |
| **Reload** | Reloads for real on a loop: the magazine is emptied, then `GunService.ReloadAs` |
| **Idle** | Holds the gun |
| **Walk** | Paces its lane at 10 studs/s |
| **Sprint** (back) | Paces a longer lane at 24 studs/s, fast enough for the sprint carry |

Row names are on the black posts at the left. Each rig has a label with its gun and animation, shown within 28 studs.

## How it works

- **Built in Studio:** `workspace.GunShowcase` holds `Floor`, `LaneLine`s, `TargetWall` with a `Target_<gun>` board per lane, the `RowSign_*` posts, `ViewPoint`, and `Rigs`. The rigs are copies of `ServerStorage.NPC.Templates.Soldier`, which brings its own walk/run animation script. Each rig has the `ShowcaseGun`, `ShowcaseAnim`, `ShowcaseStart` and `ShowcaseEnd` (lanes) attributes.
- **`Systems.Showcase.GunShowcase` (server):** gives each rig its gun (`GunService.GiveNPC`), tags it `GunShowcase`, and runs its loop. Reserve ammo is topped up. The rigs can't be hurt (`Combat.PreventFriendlyFire`), so shooting them doesn't break the range.
- **`Client.Guns.ThirdPersonGuns`** poses `GunShowcase`-tagged rigs like NPCs, and `Client.Guns.GunEffects` finds their shots by that tag for tracers.
- **Shot detection:** `ThirdPersonGuns` counts only an `Ammo` drop of at most 3 rounds as a shot. The reload rigs emptying a magazine at once doesn't fake a recoil kick.

To add or change a rig, edit its attributes in Studio, or add a gun lane by copying a column of rigs and changing `ShowcaseGun` and the positions.

## Tested (2026-11-11, Studio playtest)

- **Guns:** all 72 rigs got their guns.
- **Shooters:** every shooter fired and reloaded. In 4 s, for example, the Rifle went 1 → 27 after its reload and the SMG 42 → 20 while firing.
- **Reload rigs:** 8 of them were mid-reload at the check.
- **Lanes:** 18 of the 24 lane rigs had moved more than 2 studs (the rest were turning around).
- **Visible:** muzzle flashes and tracers showed on the Shoot row.
- **Errors:** none in the output.
