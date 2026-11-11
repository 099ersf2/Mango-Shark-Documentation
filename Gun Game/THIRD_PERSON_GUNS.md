# Third-person gun animation

How other players and NPCs look while holding a gun: idle, walking and running, sprinting, aiming (following where they look), recoil on every shot, and reloading. It's done in code (`Client.Guns.ThirdPersonGuns`), not with animation assets, so it works for every gun, and for any gun added later, with nothing to upload.

First person (your own view) is separate: `Client.Guns.Viewmodel` already animates idle sway, walk bob, sprint, aiming in, recoil and the reload for every gun.

Built 2026-11-11. Before this, every gun's `Animations` slots were empty, so other characters held guns with Roblox's default one-arm pose and never aimed, reloaded or recoiled.

## Gun size and kind

The gun models are built big (a full-size rifle is 4.4 studs, the pump shotgun 5.8, while an R15 arm reaches about 1.7). So the **third-person Tool is scaled down** when it's made (`Systems.Guns.GunService`, `thirdPersonScale`):
- long guns come out about **2.2 studs** long (`LONG_GUN_LENGTH`), and pistols and revolvers about **1.15** (`SIDEARM_LENGTH`);
- a gun is never made bigger;
- the scale is stored as the Tool's `ModelScale` attribute, and `Content.Guns.Skins` scales skin sizes and offsets by it.

The first-person viewmodel, loadout previews and gameplay don't change: bullets come from the head, and the viewmodel has its own copy.

**Where the hand grips** (`GunService` `fitGrip`, on every equip): the Tool's `Grip` is set from the holder's own right hand. The top of the fist sits 0.03 studs under the gun's body (the top of its Handle), so the fist wraps the pistol grip from below. The plain grip put a big hand's middle on the middle of the grip, and the gun sank into the fist; it was worst on the scaled-down long guns, whose grips are short. Measured on the range: every gun's body now sits on top of the fist. The guns came up 0.24 to 0.41 studs relative to the hand.

A gun reaching more than 0.45 studs behind its Handle has a stock and is held as a **long gun**; anything else is a **sidearm**, revolvers included. Before 2026-11-11 the kind came from the muzzle's distance, which put the long-barreled Revolver in the rifle poses.

## What each pose does

| Pose | When | Gun placement (from the eyes) |
| --- | --- | --- |
| **Idle** (low ready) | Holding a gun, nothing else | Long guns: the hand at the right of the chest, the stock at the right shoulder, the muzzle 25 degrees down and a little across the body. Pistols: at chin height, muzzle 30 degrees down. Half of the aim pitch; walking adds a small bob |
| **Sprint** | Sprinting (the `Sprinting` / `MoveState` attribute), or an NPC moving faster than 19 studs/s | Long guns across the chest, muzzle up and to the left; pistols low by the hip, muzzle down |
| **Aim** | `GunAiming` on the character, or a shot in the last 0.8 s | Up at the eyes: a pistol's rear sight centered 1.2 studs out; a long gun's at eye level beside the right cheek. Follows the full aim pitch |
| **Shoot** | The tool's `Ammo` goes down | A recoil kick on top of the pose: pistols 13 degrees, shotguns 10, rifles 5, plus 0.1 studs back, springing back |
| **Reload** | The tool's `Reloading` attribute | Gun tilted to show the magazine well. The left hand goes to the magazine, down to the belt (a part named `Magazine` hides), back up with it, and onto the grip again, over the gun's `ReloadTime` |

Poses ease into each other. The waist leans with a quarter of the aim pitch and the head turns with 60% of it. The legs keep Roblox's own walk and run animations.

## How it works

Every frame, in `RunService.PreSimulation` (after the Animator), for each R15 character within 250 studs of the camera that holds a gun with `Aim` and `LeftGrip` attachments on its Handle:

1. **Placement:**
   - pistols, and long guns when aiming, have the gun's `Aim` attachment (the rear sight) placed in front of the eyes by the pose;
   - long guns' idle, sprint and reload place the grip (the Handle) instead, because the rear sight is in a different spot on every long gun (on a shotgun it is on the grip), while the grip is always where the hand is;
   - all poses are blended as sight placements, so they ease into each other alike. The pose is turned by the character's facing and its aim pitch:
   - **Players:** the relayed pitch (`UnreliablePackets.GunAimRelay`).
   - **NPCs:** the `AimPitch` attribute.
   - **Your own body:** your camera.
2. The right hand goes where the gun's grip needs it (the gun is welded to the right hand by `RightGrip`). The left palm goes on the gun's `LeftGrip`.
3. **Settle** (up to 5 rounds):
   - the gun slides straight back, level, by what the left arm is short of the front grip, at most 0.45 studs in all (`MAX_SLIDE`). Without the cap, a gun held out to the side met no body to stop it, and slid back until its stock was over the shoulder; that was the shotgun idles. It is never pulled down or sideways, so it keeps the pose's height. An earlier version pulled it toward the left shoulder, which dragged long guns down to the waist;
   - it moves forward out of the head and torso, checking every corner of its outline (a stock may rest 0.15 studs into the chest, the shoulder pocket);
   - it comes back toward the right shoulder if the right arm is short (the gun is welded to that hand).

   If the front grip is still out of reach, the left hand holds as far along the gun toward it as it can.
4. Two-bone IK sets the shoulder, elbow and wrist joints' `Transform`. It works with both Motor6D and `AnimationConstraint` rigs.

Guns are sorted by shape: a muzzle within 1.3 studs of the grip is a **pistol**; a `Spherecast` gun or one named shotgun is a **shotgun**; anything else is a **rifle**.

What it skips (Roblox's animations hold these):
- R6 characters;
- melee tools (no `Aim` or `LeftGrip`);
- characters more than 250 studs from the camera;
- your own body while you're in first person. It is posed when the camera is away from your head, such as from a drone.

See every gun's poses side by side at the gun range ([GUN_SHOWCASE.md](GUN_SHOWCASE.md), the `range` command).

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

## Checking the fit

`ThirdPersonGuns.Report()` (client) returns each posed character's gun kind, how deep the gun still goes into the body (`Clip`), and how far each hand is off (`RightMiss`, `LeftMiss`). The gun range ([GUN_SHOWCASE.md](GUN_SHOWCASE.md)) is the place to read it for every gun at once.

**Heights on the range (2026-11-11, after raising the guns), measured from the head center:**

| Pose | Rear sight | Right hand |
| --- | --- | --- |
| Aim, long guns | Eye level (+0.10), beside the right cheek (+0.31) | Chest (-0.5 to -0.9) |
| Aim, pistols | Eye level (+0.04), centered | -0.8 |
| Idle, long guns | Chin/shoulder (-0.31), muzzle down 20 degrees | Upper chest (about -1.0) |
| Idle, pistols | Chin (-0.55), muzzle down 30 degrees | -1.1 to -1.4 |
| Sprint | Carried lower across the body (-0.6 to -1.0) | -1.4 to -1.9 |

Clipping was 0.02 studs at most, the right hand always reached, and the left hand averaged 0.5 studs from the front grip, holding along the gun body.

**On the range, all 72 rigs (2026-11-11, earlier fit check):**
- **Clipping:** at most 0.10 studs into the body. Before, whole stocks went through heads.
- **Right hand:** always on the grip.
- **Left hand:** on average 0.19 studs from the front grip, about 0.4 at worst on the long rifles when aimed.
- **Kinds:** Revolver and SiegePistol are held as sidearms.

## Tested (2026-11-11, Studio playtest, the test-area NPCs)

- **Aim (Soldier, pistol):** the rear sight sat 1.17 studs in front of the eyes, centered. The barrel was along its aim, with the left hand on the grip.
- **Idle (pistol, burst rifle and shotgun):** the left palm was 0.00 studs from each gun's front grip. Before the reach fix the long guns missed it by about 1 stud.
- **Reload (Grenadier, burst rifle):** the left palm went from the grip to the magazine (0.04), down to the belt with the magazine hidden (0.27), back to the well (0.25), then onto the grip (0.00).
- **Shoot (Breacher, shotgun):** its two shots kicked the barrel up to 10.9 degrees, then it reloaded.

Not yet checked: two real players watching each other (aim pitch relay, `GunAiming`, sprint), and how it looks from every angle. The numbers above are from measurements; tune `POSES` by eye if a hold looks off.
