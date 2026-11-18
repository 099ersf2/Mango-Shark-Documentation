# Security and lag pass (2026-11-18)

The owner asked for the game to be attacked like an exploiter would, so the holes can be patched and the server stays lag free. Every client-to-server entry point was read (Shared.Packets, Shared.UnreliablePackets, the Rappel remote, Scribe's transport, QuestAtlis, Cmdr), then attacked in Studio playtests from a client script, then patched and attacked again.

## What was found and fixed

| Hole | What an exploiter could do | Fix |
| --- | --- | --- |
| **Packet flood** (`Modules.Utilities.Packet`) | One message under 8 KB held thousands of packets. 1,333 store requests a frame made the server answer each: 1.6 MB of replies in 6 s and a 553 ms server freeze | At most 96 packets a player a server frame; an answered request (with a reply) counts 8, so 12 a frame. Unknown packet ids, non-buffers and non-table instance lists are dropped. After: 23 ms worst frame, replies down 4x and then halved again |
| **Unreliable spam** (`Shared.UnreliablePackets`) | No limit: every aim-pitch message is relayed to everyone nearby, so one client multiplied traffic to all; malformed ones errored in the server log | 30 messages a second per player per packet; bad messages dropped quietly (pcall) |
| **Teleport and CFrame speed hacks** (`Systems.Movement.MovementService`) | The speed check read the velocity the client reports, so moving the character by its CFrame passed: a 60-stud teleport was never noticed | Position check: the real distance since the last accepted place against what the allowed speed adds up to, re-anchored once a second. A jump of more than 12 studs past the allowance is undone at once, smaller excesses after 3 samples. Over time a cheat moves no faster on average than a sprint |
| **Fly and hover** (same) | Nothing checked height | Rising is held to the ground allowance plus a jump (8 studs). A character with no ground under it that isn't falling fast for 2 s is put back where it last stood |
| **Drone teleport** (`Systems.Drones.DroneService`) | The owner's client drives its drone, and the speed check read the reported velocity: a drone could be teleported into the enemy site to scan | The same position check for driven drones (boost speed x slack, a hop upward), anchor kept a second |
| **NaN and infinite vectors** (`GunService.Fire`/`FireAs`, `GunMelee.SwingAs`, `ConsumableService.Throw`) | `direction ~= direction` catches NaN but not infinity; `(inf, 0, 0).Unit` is NaN, so shots, bashes and throws ran with NaN (the bash skipped its facing check) | Every client vector must be finite (under 1e6 a component); the gun's timestamp and spread are type-checked |
| **Crate double-open** (`StoreService.OpenCrate`) | The crate count was checked before the transaction only | Checked again inside it (as `OpenWithBonus` does). Tested: three opens of one crate sent together give one skin |
| **Reinforce hold spam** (`ClassService`, `Packets.Class.Hold`) | Each start casts for a board and starts the hold sound, with no limit | One start per 0.2 s (letting go is never limited) |
| **Small leaks** | `Hacker` kept a request table per player forever | Cleared when the player leaves |
| **Debug print** (`Utilities.BehaviorTreeCreator`) | Printed the whole bot behaviour tree on every bot spawn | Removed |

The position and hover checks only skip moves the server makes itself: the server's own CFrame writes (spawns, portals, PivotTo, MoveTo, the rappel) fire the root's CFrame signal on the server, and a client's moves never do (tested). A server push (a `LinearVelocity`, like knockback), a seat, an anchored body or the server owning the body also skip it. Corrections are counted in the player attributes `MoveCorrections` and `DroneCorrections` and warned in the server log at most every `LogInterval`. Nobody is kicked.

## What held up already

- **Store, crates, battle pass, skins, settings, loadouts, lobby, tutorial, analytics, parties and queue:** type and length checks, rate limits (TokenBucket) and Scribe transactions. Prices come from Content, never the client.
- **Guns:** the server owns ammo, fire rate, spread and hits, and traces bullets itself. 60 shots sent in one frame fired one.
- **Cameras, drones' scans, Dead Call, hologram poses, classes:** ownership, team, phase and cooldown checks.
- **Cmdr:** every command (the defaults too) goes through the `BeforeRun` hook, which allows only `Classes.Admins`.
- **Scribe's own transport** has frame and size budgets.
- **Sword combat** was not changed (a standing rule); its knife aim is already range-checked on the server.

## Lag check

A 5v5 Siege match with 9 bots on Mansion, measured on the server every 2 s: 60 fps throughout (16.7 ms average frames), worst frames 20 to 68 ms with one 258 ms hitch at the round change (map and bots reset). The client held 60 fps, worst frame 35 ms. The server's instance count stayed flat over the round (no leak). Studio runs the server, client and editor in one process, so a live server should do better.

## Not covered

- **Speed hacks up to about sprint speed** pass on average (the allowance has to cover a real sprint and network bursts).
- **Noclip through walls** at a legal speed isn't checked.
- **Real input:** sprinting, sliding, the rappel and the pool ladder weren't played with a keyboard after the change (Studio was in the background). Watch `MoveCorrections` in the first real playtest; if honest players get corrections, raise `POSITION_SLACK` or `BAD_SAMPLES` in `MovementService`.
- **QuestAtlis** has an unthrottled `RequestData` remote function, but nothing requires QuestAtlis, so it has no handler.
- **Not published.**
