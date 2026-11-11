# Scout drones

Small ground drones in the style of Rainbow Six Siege's. You throw one out and look through its camera at once. You drive it fast and low, hop over things, boost, and spot enemies for your team. Drones are fragile: a couple of bullets, one shot to the camera, or any grenade destroys one. A destroyed drone comes back after a cooldown. NPCs see, hear and shoot drones.

Built 2026-11-11. It replaced an older drone system (a loose `DroneService` Script, a `DroneController` LocalScript and `DroneRemote`), which is kept, disabled, in `ServerStorage.Archive.OldDroneSystem` for reference.

## How it plays

| | |
| --- | --- |
| Drones | 2 per player (`CHARGES`). A destroyed drone comes back after 18 s (`RESPAWN_COOLDOWN`). A new match refills everyone; the lobby clears your drones |
| Throw | **5** (`Drone` key). It flies from your head along your look, lands, skids to a stop, and you are looking through it. With none ready, 5 opens the cameras instead |
| Cameras | **X** (`DroneView` key) opens or closes the drone cameras. **Q / E** switch drones |
| Drive | WASD (or left stick, or the touch thumbstick). Mouse / right stick / touch drag looks and turns the drone. 24 studs/s, fast to start and stop |
| Hop | **Space**: about 2 studs up, every 1.1 s |
| Boost | **Shift**: 36 studs/s for 2.5 s of bar; it refills in 4 s, and an empty bar is locked for 6 s (Siege's rule) |
| Spot | **Fire** (left mouse / RT): the enemy nearest the crosshair (within 6°, 150 studs, in clear view) is marked for your team for 8 s: a red outline and a diamond over them |
| Your body | Stays where you left it, held still. Taking damage drops you out of the drone at once |
| Health | 30. Your own and your teammates' shots don't hurt it. Destroyed: a small pop, "SIGNAL LOST", then your next drone or your body |
| NPCs | Notice a drone within 55 studs, and prefer a player in view. They hear one driving within 30% of their hearing range (60% boosting), and come to look |

Gamepad: DPad Left throws (or opens the cameras), DPad Down opens and closes them; in a drone A hops, L3 boosts, RT spots, LB / RB switch, B leaves. Touch: the DRONE and CAMS buttons; in a drone HOP, SPOT, BOOST, NEXT and EXIT buttons.

## Files

| Where | What |
| --- | --- |
| `ReplicatedStorage.Content.Drones` | Every setting (speeds, boost, hop, health, charges, cooldown, spotting, NPC sight and hearing) and the attribute names |
| `ServerScriptService.Modules.Systems.Drones.DroneService` | Server: throws, health and charges, the landing handover, speed checks, spotting, motor sound, noise for NPCs |
| `ReplicatedStorage.Modules.Client.Gadgets.DroneController` (ClientOnly) | Client: keys, driving, the camera, the feed UI, the HUD slot and mobile buttons, spot marks |
| `ReplicatedStorage.Assets.Models.Gadgets.Drone` | The model (see below) |
| `StarterGui.DroneFeed` | The camera feed UI |
| `StarterGui.Main.DroneSlot`, `Main.Mobile.DroneButton`, `Main.Mobile.DroneViewButton` | On-foot HUD and mobile buttons |
| `Assets.UI.Templates.SpotMarker`, `SpotHighlight` | What a spotted enemy shows |
| `Lighting.DroneFeed` | A ColorCorrectionEffect for the feed's colder, flatter look (on only in a drone) |
| `Shared.Packets` `Drone` group, `Shared.PlayerSettings` `Drone` / `DroneView` actions | Network and keys |
| `Content.Effects.Registry` `DroneDestroyed` | The pop and metal bits |

## The model

`Assets.Models.Gadgets.Drone` (PrimaryPart `HumanoidRootPart`):

- `HumanoidRootPart`: the body. It holds the `Center` attachment, the **`Drive`** LinearVelocity (flat plane mode, world X and Z, MaxForce 1500), the **`Turn`** AlignOrientation (rigid, upright, yaw only) and the **`Motor`** sound (looped).
- `Head`: the camera housing. Hits there count as headshots, so most guns one-shot the drone through the camera.
- `LeftWheel` / `RightWheel`: cylinders that touch the ground, with **no friction**: the Drive constraint does all the moving and braking. That keeps driving crisp, and the drone slides along walls instead of catching.
- A `Humanoid` (MaxHealth 30) with `EvaluateStateMachine` off, so every gun, grenade and NPC damages it through `Combat.ApplyHit` like any target. With its state machine off it never fires `Died`, so the server watches `HealthChanged` for 0.

The motor sound is a placeholder: the game's slide loop pitched up. Swap `Motor.SoundId` for a real small-motor whir.

## How it works

**Throw** (`Packets.Drone.Deploy`, the unit look direction): the server checks the player is alive, out of the lobby, not Stunned or CantDoAnything, has a charge and a free slot, is past `THROW_COOLDOWN`, and `Drone.PreventDeploy` doesn't refuse. It clones the drone 1.6 studs ahead of the head (never through a wall) into `workspace.Drones` with the `DroneOwner`, `Team` and `DroneSlot` attributes, and throws it. **The server flies the throw** until it lands, then skids it to a stop through Drive (at most `MAX_SERVER_FLIGHT` 2 s, 0.6 s of skid). Only then does it give the drone's physics to the owner's client (`SetNetworkOwner`). Handing it over mid-flight made a frictionless drone slide 100 studs while ownership changed hands.

**Driving** (client, every frame, render priority Camera + 3, after MovementCamera and Viewmodel): only once the client simulates the drone (`ReceiveAge == 0`). The wanted direction comes from the default controls' move vector (the PlayerModule is in `StarterPlayer` in this place), turned by the drone's yaw. The drone's flat velocity moves toward it at `ACCELERATION` (or `BRAKING` with no input; in the air only with input, at `AIR_CONTROL`). It goes into `Drive.PlaneVelocity`; `Turn.CFrame` is the yaw. Drones you are not driving brake to a stop and wait.

**Camera**: Scriptable, just in front of the lens, turned by your look (pitch ±70°), FOV 88 (96 while boosting). Its height eases after landings and it leans a little into turns. Main and the gun viewmodel (`Viewmodel.SetHidden`) are hidden while in a drone; `DroneFeed` and `Lighting.DroneFeed` are shown. The mouse is locked to the center. The other gun and movement keys are sunk, so nothing fires from your body.

**Server checks** (every 0.25 s): a drone below the world dies. One going flat-out faster than `BOOST_SPEED * SPEED_SLACK` three checks in a row is stopped, and the server takes its physics back for 0.4 s. The `Motor` sound's volume and pitch follow its speed for everyone. A moving drone fires `Drone.Noise` every 0.5 s.

**Spotting** (`Packets.Drone.Spot`, answered): from the drone's `Head`, the enemy player character or NPC nearest the look within `SPOT_ANGLE`, `SPOT_RANGE` and in clear view. The owner's team (`TeamService.Members`), or just the owner with no team, gets `Packets.Drone.Spotted` (the target and `SPOT_TIME`). The spotter sees "ENEMY SPOTTED".

**Charges**: `DronesReady` and `DroneNextReady` (server time of the next return, 0 for none) on the player. A destroyed drone queues a return `RESPAWN_COOLDOWN` from now. `DroneService.Clear(player?, refund?)` removes drones: refund (a new match, the lobby, leaving) gives the charges back at once.

**Friendly fire**: `DroneService` adds a `Combat.PreventFriendlyFire` handler: the owner and anyone on the owner's `Team` can't hurt it (always, whatever the match's FriendlyFire setting).

## NPCs

- `NPCService.refreshWorld` adds every living drone to `Brain.World` with its `Team`, and `Combatant.Drone = true`. NPCs aim at it (`Brain.AimPoint` falls back to the root) and shoot it with their normal aim.
- `Tasks.FindTarget` notices a drone only within `SIGHT_RANGE` (55) and treats it as `TARGET_BIAS` (1.6) times farther, so a player in view comes first.
- `NPCService.checkAwake` counts drones, so a drone scouting near sleeping NPCs wakes them.
- `Tactics` hears `Drone.Noise`, like gunshots: an NPC that can't see the drone suspects that spot, turns, opens its vision cone and hunts there.

## Code API

```lua
local DroneService = require(ServerScriptService.Modules.Systems.Drones.DroneService)
DroneService.Deploy(player, look)       -- throw one (every check); returns the drone or nil
DroneService.Spot(player, drone, look)  -- spot for the team; true if someone was spotted
DroneService.Clear(player?, refund?)    -- remove a player's drones (nil: everyone's)
DroneService.Of(player)                 -- the player's living drones, by slot
DroneService.All()                      -- every living drone
```

Client: `DroneController.Use()`, `Throw()`, `ToggleView()`, `View(drone)`, `Exit()`, `Cycle(±1)`, `Hop()`, `Spot()`.

Extension points: `Drone.PreventDeploy(player)` (Any), `Drone.Deployed(player, drone)`, `Drone.Destroyed(player, drone, killer?)`, `Drone.Noise(drone, position, share)`, `Drone.Spotted(player, target)` (Fire).

## Tested (2026-11-11, Studio playtest, one player)

- A throw with 5 (through the live controller) lands about 30 studs out and skids to a stop. The server hands it over, and the client drives it (`ReceiveAge` 0, Drive on).
- The feed opens: DroneFeed on, Main off, Scriptable camera at FOV 88, no viewmodel in the camera. "1 of 1", with the next drone's countdown.
- The HUD slot shows "Drone [5] x2", then x1 and x0, dimmed at 0.
- NPCs shot two drones down (the Soldier, from the test area). Before a fix, a destroyed drone stayed at negative health: its Humanoid never fires `Died`, so the server now watches `HealthChanged`. The destroyed drone's charge then counted down.

Not yet checked by hand: how driving, hop and boost feel with real keys, and spotting a real enemy. Also gamepad and touch, and two players (team marks, friendly fire on drones). See [NEXT_STEPS.md](NEXT_STEPS.md).
