# Gun system architecture

A short map of how guns work. For adding guns and abilities, see [ADDING_GUNS.md](ADDING_GUNS.md).

## Principles

- **Data-driven.** A gun is a definition in `Content.Guns.Definitions` plus a model in `Assets.Models.Guns`. Behavior beyond stats lives in ability modules (`Content.Guns.Abilities`) made of hooks.
- **Server-authoritative.** Clients send intent only: fire (server timestamp, origin, direction, seed, spread), reload, aim and ability key. The server owns ammo, fire rate, the spread floor, hits, headshots and damage.
- **Same shot everywhere.** `Shared.Guns.Ballistics` builds a shot from a seed. The shooter, the server and other clients run the same `OnFire` hooks with `Random.new(seed)` and get the same pellets.
- **Built on the existing framework.** Modules load through `ModuleLoader`; networking goes through `Shared.Packets` and `Shared.UnreliablePackets`; damage through `Combat.ApplyHit`; effects through `Content.Effects.Registry` with `EffectService` and `Client.Effects`; states through `StateHandler`; rules through `Shared.Extensions`.

## Shot flow

| Step | Where | What happens |
| --- | --- | --- |
| 1 | `Client.Guns.GunController` | The Heartbeat fire loop checks the fire mode, interval, state and predicted ammo |
| 2 | `Shared.Guns.Ballistics` | Builds the shot from the camera with a new seed, runs `OnFire`, fills the pellet directions |
| 3 | `GunController` | Sends `Packets.Gun.Fire`, then plays the shot locally (`GunEffects`) and kicks the camera (`Viewmodel`) |
| 4 | `Systems.Guns.GunService` | Checks the held Tool, state (`Stunned`, `CantDoAnything`, `Reloading`), `Gun.PreventFire`, the minimum interval and `TokenBucket`, the timestamp and ammo |
| 5 | `GunService` | Clamps the origin to 4 studs from the head with line of sight, and the spread to `[Spread.MinAngle, Spread.Max]` |
| 6 | `GunService` + `Ballistics` | Rebuilds the pellets. Hitscan: `Ballistics.Trace` with the same pierce rule. Projectile: the gun's server FastCast2 caster |
| 7 | `Systems.Guns.AbilityRunner` | Per bullet: falloff, headshot, `Gun.DamageMultiplier`, `OnHit`, then `Combat.ApplyHit` (shotgun pellets on one humanoid are added up into one hit), then `Gun.Hit` and `Packets.Gun.HitConfirm` |
| 8 | `GunService` | `EffectService.Play(GunFire_<Id>)` to nearby players except the shooter; `UnreliablePackets.GunFired` so they draw the tracers |

## State

| Where | What |
| --- | --- |
| `Tool` attributes `GunId`, `Ammo`, `Reserve` | Server-owned. The client predicts ammo between shots and resyncs from `Ammo` |
| `StateHandler` `Reloading` | Set on the server while reloading; the client's reload bar follows it |
| `StateHandler` `Firing` | On while shots keep arriving, off 0.15 s after the last one |
| `Held` table in `GunService` | Equipped gun, last shot time, aiming, reload token |

## Networking

| Packet | Direction | Payload |
| --- | --- | --- |
| `Packets.Gun.Fire` | Client → server | F64 time, Vector3 origin, Vector3 direction, U32 seed, F32 spread |
| `Packets.Gun.Reload` | Client → server | none |
| `Packets.Gun.Aim` | Client → server | Boolean |
| `Packets.Gun.AltFire` | Client → server | Boolean (only for server-side `OnAltFire`) |
| `Packets.Gun.HitConfirm` | Server → shooter | Boolean headshot, Boolean killed |
| `UnreliablePackets.GunFired` | Server → nearby clients | UserId, gun Id, origin, direction, seed, spread |
| `UnreliablePackets.GunAim` | Client → server | Aim pitch, at 10 Hz |
| `UnreliablePackets.GunAimRelay` | Server → nearby clients | UserId, pitch (tilts the right arm on R6, the waist on R15) |

## Client frame

- **RenderStep at Camera + 1** (`Viewmodel`): applies the change in camera recoil and CameraShaker shake since last frame, then places the 45%-scale rig: hip/ADS blend, sway from camera turn speed, walk bob, recoil spring, sprint pose, equip raise. In first person it hides the character's arms and the third-person Tool locally.
- **Heartbeat** (`GunController`): fire loop, bloom recovery, reload tracking, aim pitch, crosshair gap and its size (half size while aiming).

Aiming lines each gun's `Aim` attachment up with the camera, so you look down its iron sights; only a gun with the `Scope` ability gets a scope overlay.

Both exist only while a gun is held. The camera is locked to first person while a gun is held.

## Known limits

- **No lag compensation.** The server hits targets where it sees them when the shot arrives.
- **No animations ship.** `Animations` ids are empty; motion comes from springs. Ids put in a definition play on the viewmodel rig through `AnimationHandler`.
- **No sprint system.** The sprint pose reads a `Sprinting` player attribute, or moving faster than 19 studs/s. A future sprint script only needs to set that attribute.
- **Spare ammo is lost on respawn.** Tools are given into the Backpack, which Roblox clears when the character respawns.
