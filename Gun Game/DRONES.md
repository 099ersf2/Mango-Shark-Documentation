# Scout drones

Small ground drones in the style of Rainbow Six Siege's. You throw one out and look through its camera at once. You drive it fast and low, hop over things, boost, and spot enemies for your team. Drones are fragile: a couple of bullets, one shot to the camera, or any grenade destroys one. A destroyed drone comes back after a 30 s cooldown. You have one drone out at a time: 5 takes you into it (or throws one) and out again; X only takes you out. NPCs see, hear and shoot drones.

Built 2026-11-11. It replaced an older drone system (a loose `DroneService` Script, a `DroneController` LocalScript and `DroneRemote`), which is kept, disabled, in `ServerStorage.Archive.OldDroneSystem` for reference.

## Changed on 2026-11-12 (Siege)

Where this section and the rest of the page disagree, this section is right.

**Scanning replaced spotting.** Fire in a drone scans the enemy in the crosshair (same range, angle and clear view as before):
- The team gets a **static mark** where the enemy stood at that moment (`Packets.Drone.Marked`: a key, a position, seconds). It does not follow them.
- It lasts 30 s (`SPOT_TIME`). Scanning the same enemy again replaces it.
- The cooldown is 5 s (`SPOT_COOLDOWN`), and the server enforces all of it (`Packets.Drone.Scan`).
- The highlight and the following marker are gone (`SpotHighlight` is archived in `ServerStorage.Archive.OldDroneSpot`; `Packets.Drone.Spot` and `Spotted` no longer exist).

**Controls for a game mode** (`DroneService`; Siege uses all of them, see [SIEGE.md](SIEGE.md#drones-in-siege)):

| Call | What it does |
| --- | --- |
| `Place(player, cframe)` | Puts the player's drone down there, with no throw. It uses a charge and a slot; the owner drives it at once |
| `SetEnabled(player, on)` | `false`: no drone for this player. The slot and button hide, every drone action is refused (`DronesEnabled` attribute) |
| `SetLockedIn(player, on)` | `true`: held in the drone's view with no body. The client goes in by itself and can't leave (`DroneLockedIn`) |
| `Lock(player)` | Their drones stay in the world and can be destroyed, but the server takes their physics back and refuses every view and scan (`DroneLocked` on the drone) |
| `CanView(player)` | May this player look through their drone now |
| `Mark(players, key, position, seconds)` | Shows these players a static mark |

**In Siege:**
- One drone per attacker per match, placed by the server at their spawn. Throwing is refused (`Drone.PreventDeploy`).
- **A destroyed drone never comes back** (`Drone.PreventRespawn`). The player's `DroneLost` attribute is set and the client shows the **NO SIGNAL** screen (`StarterGui.DroneFeed.NoSignal`): at once if they are in the drone, and for 2.5 s (`NO_SIGNAL_TIME`) whenever they try the drone later.
- **A dead attacker cannot use their drone.** It is locked on death: it remains in the world, can still be destroyed, and cannot be viewed or controlled.
- Defenders have no drone.

**New extension points:** `Drone.PreventRespawn(player)` and `Drone.PreventView(player)` (Any). `Drone.Spotted` now also passes the position: `(player, target, position)`.

**Tested 2026-11-12 (Studio, one player):** a placed drone stood 0.9 studs from the spawn and the client went into it by itself while held; destroyed in the prep phase, `DroneLost` was set, no drone came back, `Place` and `Deploy` were refused, and NO SIGNAL showed and stayed until the hold ended. **Not verified:** a scan of a real enemy and its mark, the lock on death with a living drone, and the drone camera itself (Studio was not rendering frames).

## Changed on 2026-11-12 (fixes)

> **Not run.** Written on 2026-11-12 with no playtest (by request). The scripts compile and the UI parts the code waits for exist; none of it has been seen working.

| Problem | Cause | Now |
| --- | --- | --- |
| A scan found nobody | The line of sight was one ray that stopped at the first part it met. A defender stands inside the site's room volume (an invisible box), so the ray always stopped there. The aim also had to be within 6° of the torso's center, and a drone on the floor looks at legs | The ray passes through anything invisible or non-colliding, and through other characters; only a visible, solid part blocks. The body part nearest the crosshair counts (head, torso, legs, feet, arms). The mark, and in Siege the defender's class on the scoreboard, follow from a scan that lands |
| Touch could not drive | Driving read Roblox's default thumbstick, which is not reliable while the body is parked or missing | The feed has its own stick (`DroneFeed.Feed.Touch.Stick`, bottom left). A finger that goes down on it drives; any other finger looks |
| The camera looked through walls | It sits 0.85 studs ahead of the drone's body, so against a wall it was on the other side | A ray from the body to the lens; something solid there pulls the camera back to the body (`CAMERA_MARGIN`, 0.3 studs) |
| NO SIGNAL could not be left | Asking for a destroyed drone showed the screen for 2.5 s, and pressing the key again only restarted it | The Drone key, the DroneView key, B and the EXIT button close it. In the drone, a destroyed drone's NO SIGNAL now stays until you leave, with the leave controls on its bottom line (`NoSignal.Hints`, and `NoSignal.Exit` on touch) |

## Camera scans and feed UI (2026-11-12)

Where this section and earlier scan descriptions disagree, this section is current.

- A drone scan still prioritizes the player or NPC in its crosshair. If none is selected, it can instead find a live enemy security camera within the drone scan's angle and range, with clear line of sight. The server sends the normal `Drone.Marked` packet to the team using key `Camera:<CameraId>` and the camera's current position. This is a static mark, not a tracking highlight; it lasts `SPOT_TIME`. The client uses `CAMERA_MARK_COLOR`.
- A successful drone player scan still sends `Packets.Scan.Alert` to the scanned player. The camera service sends the same alert packet for a successful camera scan. `ScanAlert.Label` shows the red `SCANNED` notice for `SCANNED_ALERT_TIME` (2.5 s).
- Both `DroneFeed.Feed.Timer` and `DroneFeed.NoSignal.Timer` mirror `Main.SiegeHUD.Timer`, so the game timer stays visible in live and NO SIGNAL views. Camera feeds have the same pair of timer labels.
- The camera feed's touch `SCAN` button and Interact/DPad Up inputs are documented in [SIEGE.md](SIEGE.md#defender-cameras). A camera can be cycled away from immediately after it is destroyed.

The feed and alert ScreenGuis are built under `ReplicatedFirst.UILoader` and moved into `PlayerGui` by `UILoader`.

## Two drones and switching (2026-11-13)

- A player's drone limit is the `DronesMax` attribute (`Drones.CHARGES`, 1, unless a mode adds more). `DroneService.AddCharge(player)` adds a slot and a ready charge until the next refund (a new match, the lobby).
- In a drone, Aim (right mouse), LB / RB or the touch NEXT button switch to your other living drone. Scans go out from whichever drone you look through.
- A player held in their drone (`DroneLockedIn`) keeps it, and its view, even while their body is flagged `InLobby` (Siege prep).
- Siege: the prep drone stays, and `AddCharge` gives each attacker a second one at Action, thrown with the Drone key.

## Prep view and streaming (2026-11-13)

- Every drone is `ModelStreamingMode.Persistent`.
- While a player is held in their drone (`SetLockedIn`), `DroneService` points their `ReplicationFocus` at it (and clears it when the hold ends or the drone goes), so the world streams in around the drone, not the parked body.
- Held players always see the drone view, or NO SIGNAL if they have no living drone, until released.

## How it plays

| | |
| --- | --- |
| Drones | 1 per player (`CHARGES`; Siege gives 2). A destroyed drone comes back after 30 s (`RESPAWN_COOLDOWN`). A new match refills everyone; the lobby clears your drone |
| 5 (`Drone` key) | Go into your drone where you left it, if it is alive; otherwise throw a new one (once the cooldown is done). A throw flies from your head along your look, lands, skids to a stop, and you are looking through it. In a drone: back to your body, like X |
| X (`DroneView` key) | Leave the drone, back to your body. Does nothing on foot |
| Drive | WASD (or left stick, or the touch thumbstick). Mouse / right stick / touch drag looks and turns the drone. 24 studs/s, fast to start and stop |
| Hop | **Space**: about 2 studs up, every 1.1 s |
| Boost | **Shift**: 36 studs/s for 2.5 s of bar; it refills in 4 s, and an empty bar is locked for 6 s (Siege's rule) |
| Spot | **Fire** (left mouse / RT): the enemy nearest the crosshair (within 6°, 150 studs, in clear view) is marked for your team for 8 s: a red outline and a diamond over them |
| Your body | Stays where you left it, held still, and you can see it from the drone. Taking damage drops you out of the drone at once |
| Health | 30. Your own and your teammates' shots don't hurt it. Destroyed: a small pop, "SIGNAL LOST", then your next drone or your body |
| NPCs | Notice a drone within 55 studs, and prefer a player in view. They hear one driving within 30% of their hearing range (60% boosting), and come to look |

Gamepad: DPad Left is the 5 key (in and out); in a drone DPad Down or B also leaves, A hops, L3 boosts, RT spots. Touch: the DRONE button goes in or throws; in a drone HOP, SPOT, BOOST and EXIT buttons.

## Files

| Where | What |
| --- | --- |
| `ReplicatedStorage.Content.Drones` | Every setting (speeds, boost, hop, health, charges, cooldown, spotting, NPC sight and hearing) and the attribute names |
| `ServerScriptService.Modules.Systems.Drones.DroneService` | Server: throws, health and charges, the landing handover, speed checks, spotting, motor sound, noise for NPCs |
| `ReplicatedStorage.Modules.Client.Gadgets.DroneController` (ClientOnly) | Client: keys, driving, the camera, the feed UI, the HUD slot and mobile buttons, spot marks |
| `ReplicatedStorage.Assets.Models.Gadgets.Drone` | The model (see below) |
| `StarterGui.DroneFeed` | The camera feed UI |
| `StarterGui.Main.DroneSlot`, `Main.Mobile.DroneButton` | On-foot HUD and mobile button |
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

**Camera**: Scriptable, just in front of the lens, turned by your look (pitch ±70°), FOV 88 (96 while boosting). Its height eases after landings and it leans a little into turns. Main and the gun viewmodel (`Viewmodel.SetHidden`) are hidden while in a drone; `DroneFeed` and `Lighting.DroneFeed` are shown. The mouse is locked to the center. The other gun and movement keys are sunk, so nothing fires from your body. Your body and held gun stay visible to you: first person hides them locally every frame (Roblox's camera and the Viewmodel), and the drone camera, which runs after both, sets their `LocalTransparencyModifier` back to 0.

**Keys**: on foot only 5 is bound (go in or throw). In a drone, 5, X, gamepad DPad Left, DPad Down and B leave. The in-drone binding is removed while it handles the press that leaves, so Roblox hands that same press on to the on-foot bindings; that is what used to put you straight back in. X has no on-foot binding, and `Use` (the on-foot 5) ignores calls for `REENTRY_GUARD` (0.3 s) after leaving, so 5 leaves cleanly too.

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

Client: `DroneController.Use()` (go in or throw), `Throw()`, `View(drone)`, `Exit()`, `Hop()`, `Spot()`.

Extension points: `Drone.PreventDeploy(player)` (Any), `Drone.Deployed(player, drone)`, `Drone.Destroyed(player, drone, killer?)`, `Drone.Noise(drone, position, share)`, `Drone.Spotted(player, target)` (Fire).

## Tested (2026-11-11, Studio playtest, one player)

- A throw with 5 (through the live controller) lands about 30 studs out and skids to a stop. The server hands it over, and the client drives it (`ReceiveAge` 0, Drive on).
- The feed opens: DroneFeed on, Main off, Scriptable camera at FOV 88, no viewmodel in the camera. "1 of 1", with the next drone's countdown.
- The HUD slot shows "Drone [5] x2", then x1 and x0, dimmed at 0.
- NPCs shot two drones down (the Soldier, from the test area). Before a fix, a destroyed drone stayed at negative health: its Humanoid never fires `Died`, so the server now watches `HealthChanged`. The destroyed drone's charge then counted down.

**Tested with the final keys** (5 in and out, X out): in a drone, leaving is bound to X, 5, B, DPad Left and DPad Down, and the hint reads "5 / X leave". 5 threw and went in; 5 left and the same press reaching the on-foot 5 did not go back in; 5 went back into the same drone; X left.

**Tested before 5 also left** (5 in, X out): on foot only 5 / DPad Left is bound and the CAMS button is gone. In a drone, X / B / DPad Down leave and 5 is swallowed; the hint line reads "X leave". 5 went in, 5 in the drone did nothing, X left, 5 went back into the same drone, X left again.

**Tested after the earlier key changes** (NPCs held out of the test, since any hit on your body drops you out): 5 threw and went in, with your body fully visible (0 of 34 parts hidden). 5 left, even with the same press reaching the on-foot key again. 5 went back into the same drone without throwing a new one, and X did the same both ways. A destroyed drone was removed and the next was ready in 29 s.

Not yet checked by hand: how driving, hop and boost feel with real keys, and spotting a real enemy. Also gamepad and touch, and two players (team marks, friendly fire on drones). Studio's input injection doesn't reach the game, so the keys were tested through the controller's own functions. See [NEXT_STEPS.md](NEXT_STEPS.md).
