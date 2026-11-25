# Drones and cameras

Attackers scout with **drones**; defenders watch with **security cameras**. Both can **scan** an enemy, which marks where they stood for the team and (in Siege) reveals their class.

!!! abstract "Source"

    `Systems.Drones.DroneService`, `Systems.Cameras.CameraService`; client `Client.Gadgets.DroneController`, `Client.Gadgets.CameraController`, `Client.Gadgets.FeedInfo`. Data: `Content.Drones`, `Content.Cameras`. Guide: [Scout drones](../../DRONES.md).

```lua
local Systems = game.ServerScriptService.Modules.Systems
local DroneService = require(Systems.Drones.DroneService)
local CameraService = require(Systems.Cameras.CameraService)
```

## Drones: how they work

| | Owner |
| --- | --- |
| Throwing, health, charges, speed checks, scans | **Server** |
| Driving (physics) | The **owner's client**, after the drone lands |

1. **Checks:** alive, not in the lobby, not Stunned or CantDoAnything, a charge ready, a free slot, past `THROW_COOLDOWN`, not stopped by `Drone.PreventDeploy`.
2. **Throw:** clones `Assets.Models.Gadgets.Drone` ahead of the head (never through a wall) into `workspace.Drones` with `DroneOwner`, `Team` and `DroneSlot`. The server flies it; when it stops, it hands the physics to the owner's client.
3. **Health:** the drone's Humanoid takes damage from every weapon through `Combat.ApplyHit`; its team can't hurt it. At 0 it's destroyed and its charge comes back after `RESPAWN_COOLDOWN`.
4. **Anti-cheat:** every 0.25 s, a drone below the world dies; one going faster than `BOOST_SPEED × SPEED_SLACK` three checks in a row is stopped and the server takes its physics back.
5. **Scanning** (once per `SPOT_COOLDOWN`): the enemy nearest the crosshair within `SPOT_ANGLE`° and `SPOT_RANGE` studs, in clear view, gets a **static** mark for the team for `SPOT_TIME` s. Room volumes, triggers and other characters don't block a scan.

!!! note "Why `Died` never fires"

    Drones, cameras and gadgets have Humanoids with the state machine off (it would fight their physics). Destruction is `HealthChanged` reaching 0.

Charges show on the Player as `DronesReady`, `DroneNextReady` (server time) and `DronesMax`. A new match clears every drone and refills everyone; drones stay when their owner dies.

---

## `DroneService`

### `DroneService.Deploy(player, look) → Model?`

Every check, then throws one along the unit look. What `Packets.Drone.Deploy` calls.

```lua
local drone = DroneService.Deploy(player, player.Character.Head.CFrame.LookVector)
```

### `DroneService.Place(player, cframe)`

Puts the player's drone down there with no throw (Siege gives each attacker one at their spawn in Prep).

```lua
DroneService.Place(player, spawnPart.CFrame + Vector3.new(0, 1, 0))
```

### `DroneService.Spot(player, drone, look) → boolean`

Scans from that drone along the look; `true` if an enemy was marked. What `Packets.Drone.Scan` calls.

```lua
local scanned = DroneService.Spot(player, drone, look)
```

### `DroneService.Mark(players, key, position, seconds)`

Shows these players a static mark. One mark per `key`; a new one replaces it. Recon Pulse, the proximity sensor and Leo's scan all use this.

```lua
DroneService.Mark(SiegeService.Players("Attackers"), "Intel", Vector3.new(10, 3, 40), 10)
```

### `DroneService.SetEnabled(player, on)`

`false`: no drone at all (Siege defenders).

```lua
DroneService.SetEnabled(defender, false)
```

### `DroneService.SetLockedIn(player, on)`

`true`: held in the drone's view with no body (Siege Prep). The client refuses to leave unless forced.

```lua
DroneService.SetLockedIn(attacker, true)
```

### `DroneService.Lock(player)`

Their drones stay in the world but nobody views or drives them again (a dead attacker).

```lua
DroneService.Lock(deadAttacker)
```

### `DroneService.CanView(player) → boolean`

May they look through their drone now.

```lua
if not DroneService.CanView(player) then return false end
```

### `DroneService.AddCharge(player)`

One more drone (a slot and a charge) until the next refund. Siege gives attackers a second one in Action.

```lua
DroneService.AddCharge(player)
```

### `DroneService.Clear(player?, refund?)`

Removes a player's drones (`nil`: everyone's). `refund` gives the charges back now instead of starting their cooldown.

```lua
DroneService.Clear(nil, true) -- new round: everyone's drones gone, charges back
```

### `DroneService.Of(player) → { [slot]: Model }` / `DroneService.All() → { Model }`

A player's living drones / every living drone, external ones included (NPCs read it to shoot drones).

```lua
for slot, drone in DroneService.Of(player) do print(slot, drone:GetPivot().Position) end
print(#DroneService.All(), "drones out")
```

### `DroneService.AddExternal(model)`

A drone the server drives itself (a Siege bot's, `BotDrones`). Only listed in `All`.

```lua
DroneService.AddExternal(botDrone)
```

| Point | Kind | Arguments |
| --- | --- | --- |
| `Drone.PreventDeploy` | Any | player |
| `Drone.PreventRespawn` | Any | player (then `DroneLost` is set: NO SIGNAL) |
| `Drone.PreventView` | Any | player |
| `Drone.Deployed` | Fire | player, drone |
| `Drone.Destroyed` | Fire | player, drone, killer? |
| `Drone.Noise` | Fire | drone, position, share (of an NPC's hearing range) |
| `Drone.Spotted` | Fire | player, target, position |

```lua
-- Only one drone throw per Prep phase
Extensions.Add("Drone.PreventDeploy", function(player)
	return SiegeService.Phase() == "Prep" and #DroneService.Of(player) > 0
end)
```

---

## Security cameras: `CameraService`

A game mode hands it the map's cameras when a match starts. Each becomes a model in `workspace.SiegeCameras`: an invisible hit box with a Humanoid, **pivoted exactly where the camera looks**. Because it has a Humanoid, every gun, bash and explosion damages it with no gun-code changes. State is attributes: `CameraId`, `CameraName`, `Team`, `Destroyed`, `Bulletproof`.

Damage rules, all through extension points: `Combat.PreventFriendlyFire` (its own team can't hurt it), `Camera.PreventDamage` (anything else may refuse), `Gun.DamageMultiplier` (bullets do 0 to a `Bulletproof` camera). At 0 health it stays listed but is `Destroyed`: looking through shows NO SIGNAL.

### `CameraService.Setup(sources, team)`

`sources`: parts or models (the map's Cameras folder, things tagged `Camera`).

```lua
CameraService.Setup(map.Cameras:GetChildren(), "Defenders")
```

### `CameraService.Add(model, name, team, bulletproof)`

A camera placed during the match (the Warden's gadget).

```lua
CameraService.Add(model, `{player.Name}'s camera`, "Defenders", true)
```

### `CameraService.List() → { Model }`

Every camera model, in order.

```lua
for _, camera in CameraService.List() do
	print(camera:GetAttribute("CameraName"), camera:GetAttribute("Destroyed"))
end
```

### `CameraService.Stop(player)`

They stop looking through a camera.

```lua
CameraService.Stop(player)
```

### `CameraService.Clear()`

Removes every camera (end of a match).

```lua
CameraService.Clear()
```

| Point | Kind | Arguments |
| --- | --- | --- |
| `Camera.PreventView` | Any | player, model (also gates scans) |
| `Camera.PreventDamage` | Any | attacker, model |
| `Camera.Viewed` | Fire | player, model? (`nil`: stopped) |
| `Camera.Scanned` | Fire | spotter, target (Siege reveals classes with it) |
| `Camera.Destroyed` | Fire | model, killer? |

```lua
-- Cameras can't be used during Selection
Extensions.Add("Camera.PreventView", function(player, model)
	return SiegeService.Phase() == "Selection"
end)
```

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Drone.Deploy` | Client → server | unit look |
| `Drone.View` | Client → server | looking through a drone |
| `Drone.Scan` | Client → server, answered `(scanned)` | drone, unit look |
| `Drone.Marked` | Server → scanner's team | key, position, seconds |
| `Camera.View` | Client → server, answered `(ok)` | CameraId, or `""` to stop |
| `Camera.Scan` | Client → server, answered `(scanned)` | CameraId |
| `Camera.Look` | Client → server | CameraId, yaw, pitch |
| `Scan.Alert` | Server → the scanned player | — |

---

## Client

```lua
local Gadgets = game.ReplicatedStorage.Modules.Client.Gadgets
local DroneController = require(Gadgets.DroneController)
local CameraController = require(Gadgets.CameraController)
```

| Function | Does | Example |
| --- | --- | --- |
| `DroneController.Use()` | The Drone key (5): into your drone, or throw one if none is out | `DroneController.Use()` |
| `DroneController.Throw()` | Throw a drone | `DroneController.Throw()` |
| `DroneController.View(drone)` | Look through one drone | `DroneController.View(myDrone)` |
| `DroneController.Exit(force?)` | Leave the drone; refused while `DroneLockedIn` unless forced | `DroneController.Exit(true)` |
| `DroneController.Cycle(direction)` | Next (1) / previous (-1) living drone | `DroneController.Cycle(1)` |
| `DroneController.Hop()` / `Spot()` | Hop (Space) / scan (Fire) | `DroneController.Spot()` |
| `DroneController.BindDriving()` | (Re)bind the driving controls | |
| `CameraController.Use()` | Open the cameras (a defender's Drone key) | `CameraController.Use()` |
| `CameraController.View(model)` / `Cycle(direction)` | Look through / switch camera | `CameraController.Cycle(-1)` |
| `CameraController.Scan()` | Scan the player in the crosshair | `CameraController.Scan()` |
| `CameraController.Exit(tellServer?)` | Leave the cameras | `CameraController.Exit(true)` |

`Client.Gadgets.FeedInfo` (no API) draws the objective, location and compass on both feeds.
