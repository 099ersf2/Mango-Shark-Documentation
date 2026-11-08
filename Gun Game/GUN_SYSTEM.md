# Gun system architecture

A short map of how guns work. For adding guns and abilities, see [ADDING_GUNS.md](ADDING_GUNS.md); for NPCs, [ADDING_NPCS.md](ADDING_NPCS.md).

## Principles

- **Data-driven.** A gun is a definition in `Content.Guns.Definitions` plus a model in `Assets.Models.Guns`. Behavior beyond stats lives in ability modules (`Content.Guns.Abilities`) made of hooks.
- **Server-authoritative.** Clients send intent only: fire (server timestamp, origin, direction, seed, spread), reload, aim and ability key. The server owns ammo, fire rate, the spread floor, hits, headshots and damage.
- **Players and NPCs are both shooters.** `GunService` keys held guns by character. A `Shooter` is `{ Character, Player?, Id }` (a UserId, or a negative NPC Id). Players fire through the packet handler `Fire`, which adds the timestamp and origin checks; NPCs fire through `FireAs`. Both pass the same `tryShot` checks (state, `Gun.PreventFire`, fire rate, ammo) and the same `shoot`.
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

## Loadouts and switching

1. On every spawn `Systems.Guns.LoadoutService` reads the player's saved `Loadout`, removes their old gun Tools, gives the loadout's guns through `GunService.Give` with `Slot` 1–3, and equips slot 1.
2. `Client.Guns.WeaponSlots` turns off Roblox's hotbar and equips Tools itself (`Humanoid:EquipTool` on the client) from the Slot keys, the mouse wheel, gamepad L1/R1 and the slot strip in `Main.Weapons`. `GunController` and `GunService` react to the equip as before.
3. Picking a loadout in `Client.Guns.LoadoutMenu` sends `Packets.Gun.Loadout`. The server saves it and gives it at once unless the player is firing or reloading; a `TokenBucket` stops it being used to refill ammo.

## Settings

Keybinds and volumes live in the player's Scribe data under `Settings` (declared by `Shared.PlayerSettings`, a ScribeFragment). The client loads them at start (`Client.Settings.Keybinds`, `Client.Audio.AudioSettings.Store`) and sends changes through `Packets.Settings`; `Services.SettingsService` checks the action, key or group name and writes it. A slider's changes are sent once it has been still for 0.5 s.

## State

| Where | What |
| --- | --- |
| `Tool` attributes `GunId`, `Ammo`, `Reserve` | Server-owned. The client predicts ammo between shots and resyncs from `Ammo` |
| `Tool` attribute `Slot` | The weapon slot (1–3), set by `LoadoutService`, or the next free slot by `GunService.Give` |
| Player data `Loadout`, `Settings.Keybinds.*`, `Settings.Volumes.*` | Saved with ProfileStore; written only by the server |
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
| `Packets.Gun.Loadout` | Client → server | Loadout Id |
| `Packets.Settings.Keybind` | Client → server | Action name, key name |
| `Packets.Settings.Volume` | Client → server | Sound group name, F32 volume |
| `UnreliablePackets.GunFired` | Server → nearby clients | UserId, gun Id, origin, direction, seed, spread |
| `UnreliablePackets.GunAim` | Client → server | Aim pitch, at 10 Hz |
| `UnreliablePackets.GunAimRelay` | Server → nearby clients | UserId, pitch (tilts the right arm on R6, the waist on R15) |

## Client frame

- **RenderStep at Camera + 1** (`Viewmodel`): applies the change in camera recoil and CameraShaker shake since last frame, then places the 45%-scale rig: hip/ADS blend, sway from camera turn speed, walk bob, recoil spring, sprint pose, equip raise. In first person it hides the character's arms and the third-person Tool locally.
- **Heartbeat** (`GunController`): fire loop, bloom recovery, reload tracking, aim pitch, crosshair gap, and hiding the crosshair while aiming.

Aiming lines each gun's `Aim` attachment up with the camera, so you look down its iron sights; only a gun with the `Scope` ability gets a scope overlay.

Both exist only while a gun is held. The camera is locked to first person while a gun is held.

## Kills

`AbilityRunner.ApplyHit` reads the victim's health before `Combat.ApplyHit` and reports a kill only when that hit took it from above 0 to 0 or below. A player shooter gets `Packets.Gun.HitConfirm(headshot, killed)`, which picks the hit sound (HeadshotKill, Kill, Headshot or body). Every kill fires `Gun.Killed(who, victimHumanoid, gunId, headshot)`. `Combat.DamageLog` records attackers and victims that are players or NPC models.

`UnreliablePackets.GunFired` carries the shooter's Id: a UserId, or an NPC's Id. NPC models are tagged `NPC` with an `NPCId` attribute, and `Client.Guns.GunEffects` looks them up so NPC tracers start at their gun's muzzle.

## Known limits

- **No lag compensation.** The server hits targets where it sees them when the shot arrives.
- **No animations ship.** `Animations` ids are empty; motion comes from springs. Ids put in a definition play on the viewmodel rig through `AnimationHandler`.
- **No sprint system.** The sprint pose reads a `Sprinting` player attribute, or moving faster than 19 studs/s. A future sprint script only needs to set that attribute.
- **Ammo resets on respawn.** The loadout is given fresh on every spawn, with full magazines and reserve.
- **Mouse can't click the HUD while a gun is held.** First person locks the cursor to the center; menus open with keys on PC and by tap on touch.
