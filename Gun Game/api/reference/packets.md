# All packets

Every packet in `Shared.Packets`, in the order the module declares them. "Answered" packets return values to the client's `:Fire` (see [Networking](../foundations/packets.md#answered-requests-response)).

| Group | Packet | Direction | Arguments → answer |
| --- | --- | --- | --- |
| **Effects** | `Play` | Server → clients | effect name, options |
| | `Stop` | Server → all | effect name, `{ Target, Data }` |
| **Combat** | `Hit` | Server → all | character hit, damage (0 when blocked) |
| | `Hurt` | Server → the player hit | damage, where it came from |
| | `KillFeed` | Server → all | killer name, victim name, item |
| | `Swing` | Client → server | sword aim origin, direction |
| **Scan** | `Alert` | Server → the scanned player | — |
| **Gun** | `Fire` | Client → server | server time, origin, unit direction, seed, spread |
| | `Reload` | Client → server | — |
| | `Aim` | Client → server | aiming |
| | `AltFire` | Client → server | pressed |
| | `HitConfirm` | Server → shooter | headshot, killed |
| | `Loadout` | Client → server | loadout Id |
| **Melee** | `Swing` | Client → server | server time, unit look |
| **Consumable** | `Throw` | Client → server | server time, unit look |
| | `Pick` | Client → server | consumable Id |
| **Store** | `Buy` | Client → server, answered | key, currency → ok, message, skinId |
| | `Open` | Client → server, answered | crateId → opened, message, skinId |
| | `OpenMany` | Client → server, answered | crateId, count → opened, message, skinIds, outcomes |
| | `Gift` | Client → server, answered | key, recipient UserId → ok, message |
| | `Reward` | Server → one client | amount, currency, reason |
| **DeadCall** | `State` | Server → one client | `{ Phase, Id, EndsAt, HoldStarted, SlowAt, UnhackTime }` |
| | `Control` | Client → server | call Id, holding |
| | `Phone` | Client → server, answered | `"List"` or `"Hack"`, UserId → `{ Targets, Charges, ReadyAt, Ok?, Message? }` |
| **BattlePass** | `Claim` | Client → server, answered | rewardId or `"ALL"` → claimed, message |
| | `Progress` | Server → one client | amount, reason, level |
| **Progress** | `Board` | Client → server, answered | board Id → rows, own `{ Rank?, Value }` |
| | `Seen` | Client → server | `"Streak"`, `"Level"`, `"Weekly"` or `"Ranked"` |
| | `Asked` | Client → server | `"Favorite"` or `"Notify"` |
| | `Zone` | Client → server | UTC offset in minutes |
| | `Earned` | Server → one client | kind, line, reward line |
| **Skins** | `Equip` | Client → server, answered | skinId → ok, message |
| | `BuyCrate` | Client → server, answered | — → ok, message |
| **Lobby** | `SelectMap` | Client → server, answered | map Id → ok, message |
| **Match** (legacy) | `State` | Server → clients | match snapshot |
| | `RequestState` | Client → server | — |
| **Death** | `Killed` | Server → the player who died | killer name, killer UserId, weapon, seconds to respawn (-1: out) |
| | `Spectate` | Server → a dead player | model or `nil`, name |
| **Drone** | `Deploy` | Client → server | unit look |
| | `View` | Client → server | looking through a drone |
| | `Scan` | Client → server, answered | drone, unit look → scanned |
| | `Marked` | Server → scanner's team | key, position, seconds |
| **Party** | `Request` | Client → server, answered | action, argument → ok, message |
| | `State` | Server → one client | `{ Id, Leader, Max, Members }` or `nil` |
| | `Invite` | Server → one client | PartyId, leader name, leader UserId, seconds |
| | `InviteClosed` | Server → one client | PartyId |
| **Queue** | `Request` | Client → server, answered | `Join`/`Private`/`Tutorial`/`Leave`, mode Id → ok, message |
| | `State` | Server → one client | `{ Queued, Since, Status, Size, Mode }` |
| **Siege** | `State` | Server → one client | the match as their team may see it |
| | `Pick` | Client → server | kind, value |
| | `Plant` | Server → one attacker | bomb, server time started, seconds |
| | `Board` | Server → one client | scoreboard rows |
| | `RequestState` | Client → server | — |
| **Class** | `Use` | Client → server, answered | server time, camera position, unit look → ok, message |
| | `Hold` | Client → server | active, origin, look |
| | `HologramPose` | Client → server | pose, aiming |
| | `HologramGlitch` | Server → all | hologram model, reason |
| | `State` | Server → owner only | `{ ClassId, Charges, ReadyAt, Guns, ActiveGadget }` or `nil` |
| | `Flash` | Server → one client | seconds blinded |
| **Camera** | `View` | Client → server, answered | CameraId or `""` → ok |
| | `Scan` | Client → server, answered | CameraId → scanned |
| | `Look` | Client → server | CameraId, yaw, pitch |
| **Spectate** | `Next` | Client → server | 1 or -1 |
| | `Mode` | Server → one client | `"Team"`, `"Enemy"` or `""` |
| **Settings** | `Keybind` | Client → server | action, key name |
| | `Volume` | Client → server | group, 0–1 |
| | `Option` | Client → server | option, value |
| **Movement** | `SetState` | Client → server | state |
| | `Correct` | Server → one client | state to go back to |
| **Analytics** | `MenuOpened` | Client → server | a name in `Content.Analytics.MENUS` |
| **Tutorial** | `Request` | Client → server, answered | `"Start"` or `"Skip"` → ok, message |
| | `Progress` | Server → recruit | `{ Round, Phase, Done, Missed, Counts }` |
| | `Learned` | Server → recruit | goal Id |
| | `Finished` | Server → recruit | gave the Recruit Crate |
| **Example** | `Ping` / `Pong` | Client → server / server → client | text (delete with `Services.Example`) |

## Unreliable

| Packet | Direction | Arguments |
| --- | --- | --- |
| `UnreliablePackets.GunFired` | Server → nearby | UserId, gunId, origin, direction, seed, spread |
| `UnreliablePackets.GunAim` / `GunAimRelay` | Client → server / server → others | aim pitch |

!!! note "Removed"

    `Match.Admin` (archived with the old match modes), `Drone.Spot` and `Drone.Spotted` (replaced by `Drone.Scan` and `Drone.Marked` on 2026-11-11).
