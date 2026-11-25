# Drones and cameras

Attackers scout with **drones**; defenders watch with **security cameras**. Both can **scan** an enemy, which marks where they stood for the team and (in Siege) reveals their class.

!!! abstract "Source"

    `Systems.Drones.DroneService`, `Systems.Cameras.CameraService`; client `Client.Gadgets.DroneController`, `Client.Gadgets.CameraController`, `Client.Gadgets.FeedInfo`. Data: `Content.Drones`, `Content.Cameras`. Design guide: [Scout drones](../../DRONES.md).

## Drones

### Who owns what

| | Owner |
| --- | --- |
| Throwing, health, charges, speed checks, scans | **Server** |
| Driving (physics) | The **owner's client**, after the drone lands |

A throw, step by step (from the `DroneService` header):

1. **Checks:** alive, not in the lobby, not Stunned or CantDoAnything, a charge ready, a free slot, past `THROW_COOLDOWN`, and not stopped by `Drone.PreventDeploy`.
2. **Throw:** clones `Assets.Models.Gadgets.Drone` just ahead of the head (never through a wall) into `workspace.Drones` with `DroneOwner`, `Team` and `DroneSlot`. The server flies it; when it skids to a stop, the server hands its physics to the owner's client.
3. **Health:** the drone's Humanoid takes damage from every weapon through `Combat.ApplyHit`. Its team can't hurt it. At 0 it's destroyed and its charge starts coming back after `RESPAWN_COOLDOWN`.
4. **Anti-cheat:** every 0.25 s, a drone below the world dies; one faster than `BOOST_SPEED * SPEED_SLACK` three checks in a row is stopped and the server takes its physics back.

!!! note "Why the Humanoid never fires `Died`"

    Drones, cameras and gadgets have Humanoids with the state machine off (it would fight their physics), so `Died` never fires. Destruction is `HealthChanged` reaching 0.

### Scanning

`Packets.Drone.Scan` (at most once every `SPOT_COOLDOWN` s): from the drone's camera along the look, the enemy nearest the crosshair within `SPOT_ANGLE`° and `SPOT_RANGE` studs, in clear view. Invisible or non-collidable parts (room volumes, triggers) and other characters don't block a scan. The team gets `Packets.Drone.Marked`: a **static** mark where the enemy stood, for `SPOT_TIME` s. It never follows them; scanning again replaces it.

### `DroneService` API

| Function | What it does |
| --- | --- |
| `DroneService.Deploy(player, look)` | Every check, then throws one; returns the drone or `nil` |
| `DroneService.Place(player, cframe)` | Puts their drone down there, no throw (a game mode's drone) |
| `DroneService.Spot(player, drone, look)` | Scans the enemy the drone looks at; `true` if anyone was marked |
| `DroneService.Mark(players, key, position, seconds)` | Shows these players a static mark (one per key) |
| `DroneService.SetEnabled(player, on)` | `false`: no drone at all (Siege defenders) |
| `DroneService.SetLockedIn(player, on)` | `true`: held in the drone's view with no body (Siege Prep) |
| `DroneService.Lock(player)` | Their drones stay but nobody views or drives them again (a dead attacker) |
| `DroneService.CanView(player)` | May they look through their drone now |
| `DroneService.AddCharge(player)` | One more drone (slot and charge) until the next refund; Siege gives attackers a second one in Action |
| `DroneService.Clear(player?, refund?)` | Removes a player's drones (`nil`: everyone's); `refund` gives charges back now |
| `DroneService.Of(player)` / `All()` | A player's living drones / every living drone (NPCs read it) |
| `DroneService.AddExternal(model)` | A drone the server drives itself (a bot's); only listed in `All` |

Charges show on the Player as `DronesReady`, `DroneNextReady` (server time) and `DronesMax`. A new match (`Match.Started`) clears every drone and refills everyone; drones stay when their owner dies.

### Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Drone.PreventDeploy` | Any | player |
| `Drone.PreventRespawn` / `Drone.PreventView` | Any | player |
| `Drone.Deployed` | Fire | player, drone |
| `Drone.Destroyed` | Fire | player, drone, killer? |
| `Drone.Noise` | Fire | drone, position, share (of an NPC's hearing range) |
| `Drone.Spotted` | Fire | player, target, position |

---

## Security cameras

A game mode hands `CameraService` the map's cameras when a match starts. Each becomes a model in `workspace.SiegeCameras`: an invisible hit box with a Humanoid, pivoted exactly on the source, so **its pivot is where the camera looks**. Because it has a Humanoid, every gun, bash and explosion damages it with no gun-code changes.

### Damage rules, all through extension points

| Point | Rule |
| --- | --- |
| `Combat.PreventFriendlyFire` | The camera's own team can't hurt it |
| `Camera.PreventDamage` | Anything else may refuse a hit |
| `Gun.DamageMultiplier` | Bullets do 0 to a `Bulletproof` camera (a bash or explosion still hurts it) |

At 0 health it stays listed but is `Destroyed`: looking through it shows NO SIGNAL.

### `CameraService` API

| Function | What it does |
| --- | --- |
| `CameraService.Setup(sources, team)` | `sources`: parts or models (the map's Cameras folder, things tagged `Camera`) |
| `CameraService.Add(model, name, team, bulletproof)` | A camera placed during the match (a class gadget) |
| `CameraService.List()` | Every camera model, in order |
| `CameraService.Stop(player)` | They stop looking through a camera |
| `CameraService.Clear()` | Removes every camera (match end) |

Viewing (`Packets.Camera.View`) checks the cooldown, that the camera exists, that the player is alive and on its team, and `Camera.PreventView`, then sets the player's `CameraViewing` attribute. The client moves its own camera.

### Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Camera.PreventView` | Any | player, model (also gates scans) |
| `Camera.PreventDamage` | Any | attacker, model |
| `Camera.Viewed` | Fire | player, model? (`nil`: stopped) |
| `Camera.Scanned` | Fire | spotter, target (Siege uses it to reveal classes) |
| `Camera.Destroyed` | Fire | model, killer? |

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

## Client

| Function | What it does |
| --- | --- |
| `DroneController.Exit(force?)` | Leave the drone; refused while `DroneLockedIn` unless forced |
| `DroneController.Cycle(direction)` | Next (1) / previous (-1) living drone |
| `CameraController.Use()` / `View(model)` / `Cycle(direction)` / `Scan()` / `Exit(tellServer?)` | Security cameras |

## Example

```lua
local DroneService = require(game.ServerScriptService.Modules.Systems.Drones.DroneService)
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

-- Give a player a drone at a spot, no throw
DroneService.Place(player, CFrame.new(0, 5, 0))

-- Show two teammates a mark for 10 seconds
DroneService.Mark({ a, b }, "Intel", Vector3.new(10, 3, 40), 10)

-- React to scans
Extensions.Add("Drone.Spotted", function(player, target, position)
	print(player.Name, "scanned", target.Name, "at", position)
end)
```
