# Lobby

Players start each session in the lobby, a separate area with no guns, where they can open the skin shop. A portal takes them to the arena, and a return portal in the arena brings them back.

> **2026-11-12.** With matchmaking, players leave a lobby server through the queue ([MATCHMAKING.md](MATCHMAKING.md)), and Siege is played on reserved servers. Two additions to `LobbyService`: `LobbyService.Release(player)` takes a player out of the lobby without moving them (a game mode places them), and the `Lobby.PreventFirstSpawn(player)` extension point (Any) skips the move to the lobby for a first character (match servers). **The lobby is currently off in the place**: `Lobby.ArenaPortal` and `ArenaReturnPortal` are missing, so the service warns and players spawn on the map with guns. The portals are still required; `findParts` has a marked line to require only `Lobby` and `LobbySpawnPoint` when that is wanted.

## Where things are

| What | Where |
| --- | --- |
| Server | `ServerScriptService.Modules.Systems.Lobby.LobbyService` (replaces the old loose `ServerScriptService.LobbySpawn` script) |
| Map | `Workspace.Lobby` with `LobbySpawnPoint` and `ArenaPortal.PortalTrigger`; `Workspace.ArenaReturnPortal.PortalTrigger` |
| State | The Player attribute `InLobby` (set by the server only) |
| Skin shop | `Workspace.Lobby.SkinShopStand`: a counter, sign and display gun facing the spawn. `Counter.ShopPrompt` (tagged `SkinShopPrompt`) opens the shop |
| Uses it | `Systems.Guns.LoadoutService` (no guns), `Systems.SkinShopService` (shop requests), `Client.Core.SkinShop` (the shop stand's prompt) |

## How it works

1. **Join.** `InLobby` is set to true as soon as the player joins, before their first character loads, so `LoadoutService` never hands them guns.
2. **First spawn.** The first character of the session spawns at a normal arena `SpawnLocation`, then is moved to `LobbySpawnPoint` once its `HumanoidRootPart` loads.
3. **To the arena.** Touching `Lobby.ArenaPortal.PortalTrigger` moves the player to a random enabled `SpawnLocation` outside the lobby (3 studs up) and sets `InLobby` to false. `LoadoutService` gives their loadout.
4. **Back to the lobby.** Touching `ArenaReturnPortal.PortalTrigger` moves them to `LobbySpawnPoint` and sets `InLobby` to true. `LoadoutService` takes their guns and knife.
5. **Camera.** The lobby uses the normal camera; nothing forces the mouse free (that used to stop the camera turning).
6. **Respawns.** Every later character spawns in the arena and is not in the lobby. Dying in the lobby sets `InLobby` to false at once, so the next spawn gets its guns once.

The server checks each portal use: the player must be alive, on the right side, past the 2-second cooldown, and with their root within the trigger's size plus 8 studs of it (a fake touch from across the map is refused).

`LobbyService` hooks players in `Init`, the earliest point the loader offers, so the timing matches the old script.

## API

```lua
local LobbyService = require(ServerScriptService.Modules.Systems.Lobby.LobbyService)
LobbyService.IsInLobby(player)
LobbyService.SendToArena(player)  -- what the arena portal does; returns whether they moved
LobbyService.SendToLobby(player)  -- what the return portal does
```

Constants at the top of the module: `TELEPORT_COOLDOWN`, `ARENA_SPAWN_HEIGHT`, `PORTAL_REACH`, and the part names.

## Map rules

- Don't put a `SpawnLocation` inside `Workspace.Lobby`: players are moved there by script. Any `SpawnLocation` outside it counts as an arena spawn, including ones added while the game runs.
- If `Lobby`, `LobbySpawnPoint` or either `PortalTrigger` is missing, the service warns once and turns off: players spawn in the arena with guns as normal.

## Limits

- The lobby isn't a safe zone. Nothing stops damage there (for example a `nuke` near it).
- Exploiters control their own character's position, so they can walk or teleport into the arena. The server only checks portal touches.
