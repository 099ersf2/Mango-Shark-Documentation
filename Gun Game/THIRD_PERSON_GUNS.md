# Third-person gun animation

How other players and NPCs look while holding a gun: idle, walking and running, sprinting, aiming (following where they look), recoil on every shot, and reloading. It's done in code (`Client.Guns.ThirdPersonGuns`), not with animation assets, so it works for every gun, and for any gun added later, with nothing to upload.

First person (your own view) is separate: `Client.Guns.Viewmodel` already animates idle sway, walk bob, sprint, aiming in, recoil and the reload for every gun.

Built 2026-11-11. Before this, every gun's `Animations` slots were empty, so other characters held guns with Roblox's default one-arm pose and never aimed, reloaded or recoiled.

## What each pose does

| Pose | When | Gun placement (from the eyes) |
| --- | --- | --- |
| **Idle** (low ready) | Holding a gun, nothing else | Lowered in front: muzzle about 30 degrees down (pistols 40), half of the aim pitch. Walking adds a small bob |
| **Sprint** | Sprinting (the `Sprinting` / `MoveState` attribute), or an NPC moving faster than 19 studs/s | Long guns across the chest, muzzle up and to the left; pistols low by the hip, muzzle down |
| **Aim** | `GunAiming` on the character, or a shot in the last 0.8 s | Up at the eyes: a pistol's rear sight 1.2 studs out, a long gun's 0.5 studs out with the stock in. Follows the full aim pitch |
| **Shoot** | The tool's `Ammo` goes down | A recoil kick on top of the pose: pistols 13 degrees, shotguns 10, rifles 5, plus 0.1 studs back, springing back |
| **Reload** | The tool's `Reloading` attribute | Gun tilted to show the magazine well. The left hand goes to the magazine, down to the belt (a part named `Magazine` hides), back up with it, and onto the grip again, over the gun's `ReloadTime` |

Poses ease into each other. The waist leans with a quarter of the aim pitch and the head turns with 60% of it. The legs keep Roblox's own walk and run animations.

## How it works

Every frame, in `RunService.PreSimulation` (after the Animator), for each R15 character within 250 studs of the camera that holds a gun with `Aim` and `LeftGrip` attachments on its Handle:

1. The gun's `Aim` attachment (the rear sight) is placed in front of the eyes by the pose. The pose is turned by the character's facing and its aim pitch:
   - **Players:** the relayed pitch (`UnreliablePackets.GunAimRelay`).
   - **NPCs:** the `AimPitch` attribute.
   - **Your own body:** your camera.
2. The right hand goes where the gun's grip needs it (the gun is welded to the right hand by `RightGrip`). The left palm goes on the gun's `LeftGrip`.
3. **Reach:** if either hand couldn't reach (a long gun's front grip is about 1.7 studs ahead of its handle), the whole gun slides back toward the body by exactly what's missing, up to 3 passes. So both hands stay on guns of any length.
4. Two-bone IK sets the shoulder, elbow and wrist joints' `Transform`. It works with both Motor6D and `AnimationConstraint` rigs.

Guns are sorted by shape: a muzzle within 1.3 studs of the grip is a **pistol**; a `Spherecast` gun or one named shotgun is a **shotgun**; anything else is a **rifle**.

What it skips (Roblox's animations hold these):
- R6 characters;
- melee tools (no `Aim` or `LeftGrip`);
- characters more than 250 studs from the camera;
- your own body while you're in first person. It is posed when the camera is away from your head, such as from a drone.

## Server side

| Attribute | On | Set by |
| --- | --- | --- |
| `GunAiming` | A player's character or an NPC model | `Systems.Guns.GunService` (a player's `Gun.Aim` packet; cleared on unequip), `Systems.NPC.NPCService` (an NPC with a target in sight or test-firing) |
| `Reloading` | The gun Tool | `GunService`: true from the start of a reload to its end or cancel |
| `AimPitch` | An NPC model | `NPCService`, every think when it changes by more than 0.03 radians |

Players' pitch was already relayed by `GunService` (`UnreliablePackets.GunAim` → `GunAimRelay`). The old waist tilt in `Client.Guns.GunEffects` that used it was removed; this system replaces it.

## Tuning

At the top of `Client.Guns.ThirdPersonGuns`:
- `POSES`: where each pose holds the gun, per pistol or rifle.
- `PITCH_SHARE`: how much of the aim pitch each pose follows.
- `KICK`: recoil degrees per kind.
- `POSE_SPEED`: how fast poses blend.
- `KICK_DECAY`, `AIM_AFTER_SHOT`, `WAIST_PITCH`, `NECK_PITCH`.
- `REACH_SHARE` and `REACH_PASSES`.
- `RANGE`.

## Tested (2026-11-11, Studio playtest, the test-area NPCs)

- **Aim (Soldier, pistol):** the rear sight sat 1.17 studs in front of the eyes, centered. The barrel was along its aim, with the left hand on the grip.
- **Idle (pistol, burst rifle and shotgun):** the left palm was 0.00 studs from each gun's front grip. Before the reach fix the long guns missed it by about 1 stud.
- **Reload (Grenadier, burst rifle):** the left palm went from the grip to the magazine (0.04), down to the belt with the magazine hidden (0.27), back to the well (0.25), then onto the grip (0.00).
- **Shoot (Breacher, shotgun):** its two shots kicked the barrel up to 10.9 degrees, then it reloaded.

Not yet checked: two real players watching each other (aim pitch relay, `GunAiming`, sprint), and how it looks from every angle. The numbers above are from measurements; tune `POSES` by eye if a hold looks off.
