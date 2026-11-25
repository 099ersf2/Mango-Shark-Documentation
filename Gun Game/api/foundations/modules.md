# Modules and loading

Every piece of game code is a **ModuleScript** loaded by `ReplicatedStorage.ModuleLoader`. There are no loose Scripts or LocalScripts for game logic. This page explains how loading works so your module starts at the right time and can find the modules it needs.

!!! abstract "Source"

    `ReplicatedStorage.ModuleLoader` (off limits: don't edit it). Containers: `ServerScriptService.Modules` (server), `ReplicatedStorage.Modules` (both; client modules marked `ClientOnly`).

## The lifecycle: load, Init, Start

The loader runs three passes over every module it finds, in this order:

| Pass | What happens | Put here |
| --- | --- | --- |
| **Load** | `require(module)` for every module | Constants, local state, `require` of other modules |
| **Init** | `module:Init()` on every module that has one, one after another | Setting up your own state. Don't call other services yet: they may not have run `Init` |
| **Start** | `module:Start()` on every module that has one | Connecting packets, `Extensions.Add`, `PlayerAdded`, loops |

Every module is loaded before any `Init` runs, and every `Init` runs before any `Start`. When the server finishes, it sets the workspace attribute `ServerLoaded`; each client sets `_ModulesLoaded` on its Player when it finishes (servers use this to avoid sending packets a client can't read yet).

From the loader itself:

```lua title="ReplicatedStorage.ModuleLoader (start)"
local modules = getModules(containers)
for _, module in modules do
	loadModule(module)          -- require
end
for _, module in modules do
	if tracker.Load[module] then
		initializeModule(tracker.Load[module], module)   -- :Init()
	end
end
for _, module in modules do
	if tracker.Load[module] then
		startModule(tracker.Load[module], module)        -- :Start()
	end
end
```

Each step runs in `xpcall`, so one module's error is warned (`>> Failed to start module X`) and the others still load. A module that yields too long gets a `taking a while!` warning every 5 seconds.

## Attributes that change loading

Set these on a ModuleScript:

| Attribute | Effect |
| --- | --- |
| `ClientOnly` | Loaded on clients only. **Every module under `Modules.Client` needs it.** |
| `ServerOnly` | Loaded on the server only |
| `IgnoreLoader` | Never loaded automatically (a library you `require` yourself) |
| `LoaderPriority` (number) | Loaded earlier: higher numbers first. Modules without it come after |
| `Parallel` | Required inside its own Actor (parallel Luau) |
| `RelocateToServerScriptService` | Moved to SSS at start, leaving a pointer, to hide server code |

A module is only found if every parent between it and the container is a **Folder**. A ModuleScript inside another ModuleScript (like `Abilities` under `ClassService`) is not loaded by the loader: its parent requires it.

## A service, start to finish

This is the shape every service follows. `ClassService` is a good real example: constants at the top, state, public functions with doc blocks, then `Start` wires packets and events.

```lua title="Systems.Classes.ClassService (trimmed)"
--!strict
--[[
	Systems.Classes.ClassService
	The Siege classes, server side ... (purpose, usage, extension points)
]]

local Packets = require(Modules.Shared.Packets)
local Extensions = require(Modules.Shared.Extensions)

local MAX_CLOCK_DRIFT = 2 -- Seconds a request's timestamp may be off the server clock
local USES_PER_WINDOW = 4 -- Ability requests a player may send...
local USE_WINDOW = 2      -- ...in this many seconds

local ClassService = {}
local held: { [Player]: Held } = {}

-- The player's class, or nil
function ClassService.ClassOf(player: Player)
	: Classes.Class?
	local mine = held[player]
	return if mine then mine.Class else nil
end

function ClassService:Start()
	Packets.Class.Use.OnServerInvoke = function(player, timestamp, origin, look)
		return ClassService.Use(player, timestamp, origin, look)
	end
	Players.PlayerRemoving:Connect(function(player)
		held[player] = nil
		bucket:remove(player.UserId)
	end)
end

return ClassService
```

### A new service, checklist

1. Add a ModuleScript under `ServerScriptService.Modules.Systems.<Area>` (or `ReplicatedStorage.Modules.Client.<Area>` with `ClientOnly`).
2. Start with `--!strict` and the `--[[ ]]` header: path, what it does, the public API, its extension points.
3. Put tuning numbers in `ReplicatedStorage.Content`, not in the module.
4. Connect packets and `Extensions.Add` handlers in `Start`.
5. Clean up per-player state on `Players.PlayerRemoving`.

See [Module skeleton](../../EXAMPLES.md#module-skeleton) for a copy-paste template.

## Requiring other modules

```lua
-- Server systems
local GunService = require(game.ServerScriptService.Modules.Systems.Guns.GunService)
-- Shared (both sides)
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)
-- Client only
local Effects = require(game.ReplicatedStorage.Modules.Client.Effects)
-- Content (data)
local Classes = require(game.ReplicatedStorage.Content.Classes.Classes)
```

Inside a system, the code usually walks from `script` instead (`local Systems = script.Parent.Parent`), which survives the place being renamed.

!!! warning "Testing from the command bar gets a different copy"

    Studio's command bar and execute-Luau run in their own environment, so `require` there gives a **fresh copy** of a module, not the one the game is running. `SiegeService.Phase()` from the command bar will say `Idle` even mid-match. To reach the live modules, use a temporary Script in ServerScriptService (or a LocalScript in PlayerGui) and delete it afterwards.

## Loader helpers

`require(ReplicatedStorage.ModuleLoader)` also returns:

| Function | Returns |
| --- | --- |
| `IsServerLoaded()` | `true` once the server finished all three passes |
| `IsClientLoaded(player)` | `true` once that player's client finished |
| `WaitForLoadedClient(player)` | Yields until the client loaded; `false` if they left first |
| `GetServerLoadedTimestamp()` | The server time loading finished (errors before it has) |
