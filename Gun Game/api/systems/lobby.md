# Lobby, teleporters and the gun range

Where players start, buy skins and queue. In the lobby players carry **no guns**, and most actions are refused.

!!! abstract "Source"

    `Systems.Lobby.LobbyService`, `Systems.Lobby.Teleporters`, `Systems.Showcase.GunShowcase`. Guides: [Lobby](../../LOBBY.md), [Gun animation range](../../GUN_SHOWCASE.md).

## How the lobby works

- A player's **first** character of the session spawns at `Workspace.Lobby.LobbySpawnPoint` and is in the lobby. Later characters spawn at the arena SpawnLocations.
- Touching `Lobby.ArenaPortal.PortalTrigger` sends a lobby player to the arena; `Workspace.ArenaReturnPortal.PortalTrigger` sends them back. Portals have a cooldown, need a living character, and the server checks the distance, not just the touch.
- Being in the lobby is the server-set Player attribute **`InLobby`**. `LoadoutService` takes guns away while it's true; `SkinShopService` only serves requests while it's true.
- On Siege match servers, `SiegeService` answers `Lobby.PreventFirstSpawn` so players skip the lobby.

If `Workspace.Lobby` or its spawn point is missing, the service warns once and does nothing.

## `LobbyService` API

```lua
local LobbyService = require(game.ServerScriptService.Modules.Systems.Lobby.LobbyService)
```

### `LobbyService.IsInLobby(player) → boolean`

Same as the `InLobby` attribute (which clients can read directly).

```lua
if LobbyService.IsInLobby(player) then
	return false, "Not in the lobby."
end
```

### `LobbyService.SendToArena(player) → boolean`

What the arena portal does: moves a lobby player to a random enabled arena spawn (for their `SelectedMap`) and takes them out of the lobby. `false` on cooldown, dead, or not in the lobby. **Handy in tests**, since the lobby refuses most actions.

```lua
LobbyService.SendToArena(player) -- then give guns, spawn NPCs, etc.
```

### `LobbyService.SendToLobby(player) → boolean`

What the return portal does.

```lua
LobbyService.SendToLobby(player)
```

### `LobbyService.Release(player)`

Out of the lobby **without moving them**, and their next character spawns outside it. For a game mode that places its own players.

```lua
LobbyService.Release(player)
player:LoadCharacter()
```

### `LobbyService.Readmit(player)`

The next character spawns in the lobby like the first. Call it **before** `LoadCharacter` when a mode sends players back to this same server's lobby (Siege in Studio). Without it the new character counts as an arena spawn and gets the match loadout in the lobby.

```lua
LobbyService.Readmit(player)
player:LoadCharacter()
```

### `LobbyService.SelectMap(player, mapId) → (ok, message)`

The lobby hub's map pick (the `SelectedMap` attribute); what `Packets.Lobby.SelectMap` calls.

```lua
local ok, message = LobbyService.SelectMap(player, "Original")
```

| Point | Kind | Arguments |
| --- | --- | --- |
| `Lobby.PreventFirstSpawn` | Any | player (true skips the lobby for their first character) |

## Teleporters

Data only: tag a part **`Teleporter`** and give it a **`TeleportTo`** attribute naming its destination part (anywhere in Workspace). A character touching it lands 3 studs above the destination, with a 1 second cooldown so nobody bounces between pads. Parts tagged later work too.

```lua
-- Edit mode (command bar), making a new pad:
local CollectionService = game:GetService("CollectionService")
CollectionService:AddTag(workspace.TeleportA, "Teleporter")
workspace.TeleportA:SetAttribute("TeleportTo", "TeleportBox")
```

## The gun range: `GunShowcase`

`workspace.GunShowcase` has one rig per gun and animation (each rig's `ShowcaseGun`, `ShowcaseAnim`, `ShowcaseStart`, `ShowcaseEnd` attributes). On start every rig is armed (`GunService.GiveNPC`), tagged `GunShowcase`, and runs its animation for real: `Idle`, `Walk`, `Sprint`, `Aim`, `Shoot` (real bullets through `GunService.FireAs`) or `Reload`. The rigs can't be hurt.

Get there with the `range` command. Use it to check a new gun's third-person poses.

```lua
-- Add a rig: copy one in workspace.GunShowcase.Rigs and set its attributes
rig:SetAttribute("ShowcaseGun", "AssaultRifle")
rig:SetAttribute("ShowcaseAnim", "Shoot")
```
