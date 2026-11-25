# Task-based code examples

Copy-and-adapt Luau for common jobs, built only from the documented game APIs. Each example says **where the code runs**, gives the code, and lists the **gotchas** that usually cause bugs.

!!! abstract "How to use these examples"

    - **Short snippets** assume they are inside a loaded module's `Start` (or a function it calls), with `player` or `humanoid` already in scope.
    - **Full modules** start with `--!strict` and a header comment. Drop them into the folder named above the code; ModuleLoader loads them, so there is nothing to wire up.
    - **Server code** goes under `ServerScriptService.Modules`. **Client code** goes under `ReplicatedStorage.Modules.Client` and needs the `ClientOnly` attribute set to `true`.
    - Tuning numbers belong in a `ReplicatedStorage.Content` module. The examples keep them as `UPPER_CASE` constants at the top so they are easy to move.
    - Studio's command bar gets its **own copy** of every module. To try a snippet against the running game, paste it into a temporary `Script` (server) or `LocalScript` in `PlayerGui` (client) during a playtest, then delete it. See the [AI coding guide](AI_CODING_GUIDE.md#3-how-loading-works) for the full loading rules.

## Module skeleton

Every full example below follows this shape. `Init` sets up state; `Start` connects events. Public functions use a dot, `Init`/`Start` use a colon.

```lua
--!strict
--[[
	Systems.MyFeature.MyFeatureService

	One paragraph: what this does and who decides what (the server decides X; the client only shows Y).
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")

local Shared = ReplicatedStorage.Modules.Shared
local Systems = ServerScriptService.Modules.Systems

local Extensions = require(Shared.Extensions)
local GunService = require(Systems.Guns.GunService)

local MyFeatureService = {}

function MyFeatureService:Init()
	-- State, folders, collision groups. Don't rely on another module's Start here.
end

function MyFeatureService:Start()
	-- Connect events, packets and extension handlers here.
end

return MyFeatureService
```

---

## Guns and loadouts

### Give a player a gun

**Runs on:** server. Use it after your game flow has decided the player may have the weapon.

```lua
local GunService = require(game.ServerScriptService.Modules.Systems.Guns.GunService)

GunService.Give(player, "Rifle") -- full magazine and reserve
```

To give **exactly** a set of guns (plus the knife) instead of adding one, use `LoadoutService.Arm`. To restore the player's saved loadout, use `LoadoutService.Apply`.

```lua
local LoadoutService = require(game.ServerScriptService.Modules.Systems.Guns.LoadoutService)

LoadoutService.Arm(player, { "Rifle", "Pistol" }) -- replaces whatever they held
LoadoutService.Apply(player)                       -- back to their saved loadout
```

!!! warning "Gotchas"

    - The gun Id must exist in `Content.Guns.Registry`. Test a new one with the `givegun <player> <gunId>` command first.
    - A player in the lobby (`InLobby` attribute true) is meant to have no guns; `LoadoutService.Apply` takes them away there.

### Check what a player is holding

**Runs on:** server. Gun Tools carry their state in attributes, so read them from the equipped Tool.

```lua
local character = player.Character
local tool = character and character:FindFirstChildOfClass("Tool")
if tool and tool:GetAttribute("GunId") then
	print(tool:GetAttribute("GunId"), tool:GetAttribute("Ammo"), tool:GetAttribute("Reserve"), tool:GetAttribute("Slot"))
end
```

Ammo attributes are written **only by the server**. A client reading them sees the last synced value; between shots it predicts its own. `GunService.GetHeld(player)` returns the server's record of the held gun (definition and tool), or `nil`.

### Block shooting under a rule

**Runs on:** server. `Gun.PreventFire` is an **Any** point: if any handler returns `true`, the shot is refused. Here, no one can shoot while a `Frozen` player attribute is set (for example during a countdown).

```lua
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

Extensions.Add("Gun.PreventFire", function(who, gunId, tool)
	-- `who` is a Player or, for NPCs, the NPC's Model. Attributes work on both.
	return who:GetAttribute("Frozen") == true
end)
```

The same pattern stops other actions: `Gun.PreventMelee` (gun bash), `Movement.PreventSprint`, `Consumable.PreventThrow`, `Drone.PreventDeploy`. See [extension points](api/foundations/extensions.md).

---

## Damage and combat

### Deal damage with kill credit

**Runs on:** server. `Combat.ApplyHit` is **the** way to hurt someone: it handles shields, knockback, the kill feed, the damage log and `Gun.Killed`-style credit.

```lua
local Combat = require(game.ServerScriptService.Modules.Systems.Combat.Combat)

Combat.ApplyHit(targetHumanoid, 30, {
	Attacker = player,                   -- Player or NPC Model; gets the kill
	Item = "Trap",                       -- the weapon name in the kill feed
	KnockbackDirection = Vector3.new(0, 0.3, -1).Unit,
	KnockbackSpeed = 40,
})
```

For environmental damage with **no** credit (fall damage, the map), use `Combat.DealDamage(humanoid, 30)`. Pass `true` as the third argument to skip shields.

!!! warning "Gotchas"

    - Teammates are protected by `Combat.PreventFriendlyFire` unless friendly fire is on; `ApplyHit` respects it, `DealDamage` does not.
    - Never set `humanoid.Health` directly for combat damage: there is no kill credit, no shield and no hit effects.

### A damage trap (full module)

**Runs on:** server. **File:** `ServerScriptService.Modules.Systems.Traps.SpikeTrap`.

Any part tagged `SpikeTrap` hurts players who touch it. A `TokenBucket` limits each player to one hit per second, so standing on the trap doesn't fire `Touched` damage dozens of times.

```lua
--!strict
--[[
	Systems.Traps.SpikeTrap

	Parts tagged SpikeTrap damage the players who touch them, at most once per HIT_WINDOW
	seconds per player. The kill feed shows "Spike trap"; no player gets credit.
]]

local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")
local ServerScriptService = game:GetService("ServerScriptService")

local Modules = ServerScriptService.Modules
local Combat = require(Modules.Systems.Combat.Combat)
local TokenBucket = require(Modules.Helpers.TokenBucket)

local TAG = "SpikeTrap"
local DAMAGE = 25
local HIT_WINDOW = 1 -- Seconds between two hits on the same player

local SpikeTrap = {}

local limiter = TokenBucket.new(1, HIT_WINDOW)

local function onTouched(hit: BasePart)
	local character = hit.Parent
	local player = character and Players:GetPlayerFromCharacter(character)
	local humanoid = character and character:FindFirstChildOfClass("Humanoid")
	if not player or not humanoid or humanoid.Health <= 0 then
		return
	end
	if player:GetAttribute("InLobby") == true or not limiter:allow(player.UserId) then
		return
	end
	Combat.ApplyHit(humanoid, DAMAGE, { Item = "Spike trap" })
end

local function watch(part: Instance)
	if part:IsA("BasePart") then
		part.Touched:Connect(onTouched)
	end
end

function SpikeTrap:Start()
	for _, part in CollectionService:GetTagged(TAG) do
		watch(part)
	end
	CollectionService:GetInstanceAddedSignal(TAG):Connect(watch)
	Players.PlayerRemoving:Connect(function(player)
		limiter:remove(player.UserId)
	end)
end

return SpikeTrap
```

### Change gun damage

**Runs on:** server. `Gun.DamageMultiplier` is a **Product** point: every handler's number is multiplied together, so always return `1` when your rule doesn't apply.

```lua
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

-- Rifles hit NPCs 25% harder.
Extensions.Add("Gun.DamageMultiplier", function(who, gunId, humanoid, hit)
	local target = humanoid.Parent
	if gunId == "Rifle" and target and target:GetAttribute("NPCId") ~= nil then
		return 1.25
	end
	return 1
end)
```

`hit` is `nil` for ability damage and gun bashes, so check it before reading `hit.Instance` or similar fields.

### Spawn protection (full module)

**Runs on:** server. **File:** `ServerScriptService.Modules.Systems.Combat.SpawnProtection`.

For a few seconds after spawning a player can't be hurt and can't shoot. It combines a veto on incoming hits (`Combat.BlockHit`) with a veto on firing (`Gun.PreventFire`), and keeps the state in an attribute so the client can show it.

```lua
--!strict
--[[
	Systems.Combat.SpawnProtection

	For PROTECT_TIME seconds after a character spawns, the player takes no hits and cannot
	fire. The server sets the SpawnProtected attribute; the client may only read it.
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Extensions = require(ReplicatedStorage.Modules.Shared.Extensions)

local PROTECT_TIME = 3
local ATTRIBUTE = "SpawnProtected"

local SpawnProtection = {}

local function isProtected(who: Instance?)
	: boolean
	return who ~= nil and who:IsA("Player") and who:GetAttribute(ATTRIBUTE) == true
end

local function onCharacter(player: Player)
	player:SetAttribute(ATTRIBUTE, true)
	task.delay(PROTECT_TIME, function()
		if player.Parent then
			player:SetAttribute(ATTRIBUTE, nil)
		end
	end)
end

function SpawnProtection:Start()
	Extensions.Add("Combat.BlockHit", function(humanoid: Humanoid, _damage: number)
		local player = Players:GetPlayerFromCharacter(humanoid.Parent)
		return isProtected(player)
	end)

	Extensions.Add("Gun.PreventFire", function(who, _gunId, _tool)
		return isProtected(who)
	end)

	Players.PlayerAdded:Connect(function(player)
		player.CharacterAdded:Connect(function()
			onCharacter(player)
		end)
	end)
end

return SpawnProtection
```

!!! tip "Removing a handler"

    `Extensions.Add` returns a function that removes the handler. Keep it when a rule should only last a while:

    ```lua
    local removeSlow = Extensions.Add("Movement.SpeedMultiplier", function(target, _gunId)
    	return if target == slowedPlayer then 0.6 else 1
    end)
    task.delay(5, removeSlow) -- back to normal speed after 5 s
    ```

### React to kills and deaths

**Runs on:** server. Use **`Gun.Killed`** for gun and bash kills (with headshot info), and **`Combat.Death`** for *every* death, including traps, grenades and NPCs.

```lua
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)
local StoreService = require(game.ServerScriptService.Modules.Systems.Store.StoreService)

local HEADSHOT_BONUS = 10

-- Bonus coins for a headshot kill by a player.
Extensions.Add("Gun.Killed", function(who, victimHumanoid, gunId, headshot)
	if headshot and typeof(who) == "Instance" and who:IsA("Player") then
		StoreService.Give(who, "Coins", HEADSHOT_BONUS, "Headshot")
	end
end)

-- Log every death, credited or not.
Extensions.Add("Combat.Death", function(victim, attacker, item)
	print(victim.Name, "died to", attacker and attacker.Name or "the world", item or "")
end)
```

!!! warning "Gotchas"

    - `who` / `attacker` can be an **NPC Model**, not a Player. Check `who:IsA("Player")` before player-only calls.
    - `Gun.Killed` fires once per death, on the hit that took health from above 0 to 0 or below. Don't also count the same kill from `Gun.Hit`.

---

## World: boards, soft walls and explosions

### An explosion that hurts people, boards and walls

**Runs on:** server. The simplest route is `ConsumableService.Detonate`, which runs the real grenade blast (damage, boards, effects, credit). Pass a `"Smoke"` id instead for a smoke cloud.

```lua
local ConsumableService = require(
	game.ServerScriptService.Modules.Systems.Consumables.ConsumableService
)

ConsumableService.Detonate("Grenade", position, player) -- player gets the kills
```

For a **custom** blast, combine the building blocks yourself:

```lua
local Systems = game.ServerScriptService.Modules.Systems
local BreakableService = require(Systems.Breakables.BreakableService)
local SoftWalls = require(Systems.Destruction.SoftWalls)

local RADIUS = 12
local BOARD_DAMAGE = 100

-- Boards: returns how many were hit.
local boardsHit = BreakableService.DamageRadius(position, RADIUS, BOARD_DAMAGE, player, "Explosion")

-- A soft wall the blast touched: punch a hole where it hit.
if SoftWalls.IsSoftWall(wallPart) then
	SoftWalls.Punch(wallPart, position, direction, 1.5, player, "Explosion")
end
```

### Reset the map between rounds

**Runs on:** server.

```lua
local Systems = game.ServerScriptService.Modules.Systems
local SoftWalls = require(Systems.Destruction.SoftWalls)
local BreakableService = require(Systems.Breakables.BreakableService)
local NPCService = require(Systems.NPC.NPCService)
local DroneService = require(Systems.Drones.DroneService)

SoftWalls.ResetAll()          -- every punched soft wall back
for _, board in myBoards do       -- the board models your mode broke
	BreakableService.Reset(board) -- whole again
end
NPCService.Clear()            -- every NPC gone
DroneService.Clear(nil, true) -- everyone's drones, charges refunded
```

---

## NPCs

### Spawn NPCs and keep them from hurting each other

**Runs on:** server. Profiles live in `Content.NPC.Profiles` (Soldier, Breacher, Grenadier); see [Adding NPCs](ADDING_NPCS.md) to make a new one.

```lua
local NPCService = require(game.ServerScriptService.Modules.Systems.NPC.NPCService)

-- The fourth argument ignores MAX_NPCS (0 today), as game modes with their own guards do.
NPCService.Spawn("Soldier", spawnPart.CFrame, spawnPart, true)

print(NPCService.Count(), "NPCs alive")
```

NPC bullets never hurt their own team. To protect a VIP NPC from players too, veto the hit:

```lua
Extensions.Add("Combat.BlockHit", function(humanoid, _damage)
	return humanoid.Parent ~= nil and humanoid.Parent:GetAttribute("VIP") == true
end)
```

---

## Player data, coins and progression

### Give coins

**Runs on:** server. Prefer **`StoreService.Give`**: it saves the coins, fires `Store.Given`, and shows the reward to the player.

```lua
local StoreService = require(game.ServerScriptService.Modules.Systems.Store.StoreService)

StoreService.Give(player, "Coins", 100, "Daily login")
```

Only write to saved data directly when no service owns the field. `WaitForData` returns `nil` if the player leaves before their profile loads:

```lua
local Data = require(game.ReplicatedStorage.Modules.Shared.Data)

local data = Data.Server.WaitForData(player)
if not data then
	return -- player left
end
if not data.WeaponSkins.Has("Rifle_Gold") then
	-- ...
end
```

### Show saved data on the client

**Runs on:** client. The client can read and observe data, never write it.

```lua
local Data = require(game.ReplicatedStorage.Modules.Shared.Data)

local playerGui = game.Players.LocalPlayer:WaitForChild("PlayerGui")
local label = playerGui:WaitForChild("Main"):WaitForChild("Kills") -- UI is built in Studio, not in code

Data.Client.WaitForData()
Data.Client.Kills.Observe(function(kills)
	label.Text = tostring(kills)
end)
```

### Count something toward a quest

**Runs on:** server. `QuestService.Add` counts toward any quest whose stat matches. Here, drone spots count toward quests with the stat `"DroneSpots"` (add the quest to `Content.Quests`).

```lua
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)
local QuestService = require(game.ServerScriptService.Modules.Systems.BattlePass.QuestService)

Extensions.Add("Drone.Spotted", function(player, _target, _position)
	QuestService.Add(player, "DroneSpots")
end)
```

### Double battle pass XP on weekends

**Runs on:** server. `BattlePass.XPMultiplier` is a **Product** point.

```lua
Extensions.Add("BattlePass.XPMultiplier", function(_player, _reason)
	local weekday = os.date("!*t").wday -- 1 = Sunday, 7 = Saturday (UTC)
	return if weekday == 1 or weekday == 7 then 2 else 1
end)
```

---

## Networking: a new client request

A full round trip: the client asks the server to do something, the server checks everything, and answers. This example lets a player ask to "ping" a position for their team.

=== "1. Declare the packet"

    In `Shared.Packets`, add a feature group. This is the **only** place a `Packet(...)` may be built.

    ```lua
    Ping = {
    	-- Client -> server, answered. Server time and the world position. Answer: ok, message.
    	Request = Packet("PingRequest", Packet.NumberF64, Packet.Vector3F32)
    		:Response(Packet.Boolean8, Packet.String),
    	-- Server -> teammates. Who pinged and where.
    	Show = Packet("PingShow", Packet.Instance, Packet.Vector3F32),
    },
    ```

=== "2. Server: check and answer"

    **File:** `ServerScriptService.Modules.Systems.Ping.PingService`

    ```lua
    --!strict
    --[[
    	Systems.Ping.PingService

    	Checks a player's ping request (alive, in a match, clock, range, rate) and shows it
    	to their team. The client only asks.
    ]]

    local Players = game:GetService("Players")
    local ReplicatedStorage = game:GetService("ReplicatedStorage")
    local ServerScriptService = game:GetService("ServerScriptService")

    local Packets = require(ReplicatedStorage.Modules.Shared.Packets)
    local TokenBucket = require(ServerScriptService.Modules.Helpers.TokenBucket)
    local SiegeService = require(ServerScriptService.Modules.Systems.Games.Siege.SiegeService)

    local MAX_CLOCK_DRIFT = 2 -- Seconds the client's timestamp may be off
    local MAX_RANGE = 300     -- Studs from the player's head

    local PingService = {}

    local limiter = TokenBucket.new(3, 5) -- 3 pings per 5 seconds

    local function check(player: Player, timestamp: any, position: any)
    	: (boolean, string)
    	if type(timestamp) ~= "number" or typeof(position) ~= "Vector3" then
    		return false, "Bad request"
    	end
    	if math.abs(workspace:GetServerTimeNow() - timestamp) > MAX_CLOCK_DRIFT then
    		return false, "Out of sync"
    	end
    	if not limiter:allow(player.UserId) then
    		return false, "Too many pings"
    	end
    	if not SiegeService.IsAlive(player) then
    		return false, "You are not in play"
    	end
    	local head = player.Character and player.Character:FindFirstChild("Head") :: BasePart?
    	if not head or (head.Position - position).Magnitude > MAX_RANGE then
    		return false, "Too far"
    	end
    	return true, ""
    end

    function PingService:Start()
    	Packets.Ping.Request.OnServerInvoke = function(player: Player, timestamp: any, position: any)
    		local ok, message = check(player, timestamp, position)
    		if ok then
    			local team = SiegeService.TeamOf(player)
    			for _, mate in SiegeService.Players(team) do
    				Packets.Ping.Show:FireClient(mate, player, position)
    			end
    		end
    		return ok, message
    	end
    	Players.PlayerRemoving:Connect(function(player)
    		limiter:remove(player.UserId)
    	end)
    end

    return PingService
    ```

=== "3. Client: ask and react"

    **File:** `ReplicatedStorage.Modules.Client.Hud.PingController` (attribute `ClientOnly` = true)

    ```lua
    --!strict
    --[[
    	Client.Hud.PingController

    	Sends a ping for the spot under the crosshair and shows teammates' pings.
    	The server decides whether a ping happens.
    ]]

    local ReplicatedStorage = game:GetService("ReplicatedStorage")

    local Modules = ReplicatedStorage.Modules
    local Packets = require(Modules.Shared.Packets)
    local CursorAim = require(Modules.Shared.CursorAim)
    local Notice = require(Modules.Client.Core.Notice)

    local PingController = {}

    function PingController.Ping()
    	local origin, direction = CursorAim.Ray()
    	local result = workspace:Raycast(origin, direction * 300)
    	if not result then
    		return
    	end
    	-- Answered packets yield, so never call them straight from an input handler.
    	task.spawn(function()
    		local ok, message = Packets.Ping.Request:Fire(workspace:GetServerTimeNow(), result.Position)
    		if not ok then
    			Notice.Show("Can't ping", message)
    		end
    	end)
    end

    function PingController:Start()
    	Packets.Ping.Show.OnClientEvent:Connect(function(from: Player, position: Vector3)
    		-- Show a marker cloned from Assets.UI.Templates (never build UI in code).
    	end)
    end

    return PingController
    ```

!!! warning "Gotchas"

    - Validate **every** argument's type on the server; a client can send anything.
    - Keep cosmetic, high-frequency traffic (tracers, aim) in `Shared.UnreliablePackets`.
    - Bind the key through `Shared.PlayerSettings.Actions` so players can rebind it, instead of hard-coding `Enum.KeyCode`.

---

## Client: settings, menus and feedback

### Read and change a setting

**Runs on:** client. `Options` reads and writes the local player's options; `Save` sends the change to the server.

```lua
local Options = require(game.ReplicatedStorage.Modules.Client.Settings.Options)

local fov = Options.Get("Fov")      -- 60–110
if Options.IsOn("CameraBob") then
	-- ...
end

Options.Set("Fov", 90)              -- apply now
Options.Save("Fov")                 -- persist it
```

On the **server**, read a player's saved option with `SettingsService.GetOption(player, "AimAssist")`.

### Rebind a key

**Runs on:** client.

```lua
local Keybinds = require(game.ReplicatedStorage.Modules.Client.Settings.Keybinds)

Keybinds.Set("Prone", "C")
print(Keybinds.Label("Prone")) -- the text to show on a button hint
```

### Open a menu, show a notice, play UI feedback

**Runs on:** client. Only one menu is open at a time; opening one frees the mouse.

```lua
local Core = game.ReplicatedStorage.Modules.Client.Core
local Menus = require(Core.Menus)
local Notice = require(Core.Notice)
local UIFeel = require(Core.UIFeel)

Menus.Open("SkinShop")
-- later
Menus.Close()

Notice.Show("Not enough coins", "You need 500 coins for this crate.") -- Error sound by default
UIFeel.Play("Confirm")
UIFeel.Pop(button) -- needs a UIScale named Feel inside `button`
```

Menu names: `Loadout`, `Settings`, `SkinShop`, `Career`, `Backpack`, `MapSelection`, `Modes`, `Party`. See [UI](UI.md).

### Effects and camera shake

**Runs on:** client for the local player only, or server for everyone.

=== "Client (only me)"

    ```lua
    local Effects = require(game.ReplicatedStorage.Modules.Client.Effects)
    local MovementCamera = require(game.ReplicatedStorage.Modules.Client.Movement.MovementCamera)

    Effects.Play("Hitmarker", { Target = part })
    MovementCamera.Shake(3, 10, 0.1, 0.6) -- magnitude, roughness, fade in, fade out
    ```

=== "Server (everyone)"

    ```lua
    local EffectService = require(game.ServerScriptService.Modules.Systems.Effects.EffectService)

    EffectService.Play("BulletImpact", { CFrame = cf })
    EffectService.Play("BulletImpact", { CFrame = cf }, shooter) -- everyone except the shooter
    ```

Effect names come from `Content.Effects.Registry`; see [Adding effects](ADDING_GUNS.md#adding-effects-to-the-registry).

---

## Siege

### Run code only on match servers

**Runs on:** server. Lobby servers and match servers run the same place. Check the role before doing match-only work.

```lua
local ServerRole = require(game.ServerScriptService.Modules.Systems.Matchmaking.ServerRole)

if ServerRole.IsMatch() or ServerRole.IsLocal() then -- IsLocal: Studio
	-- start match-only systems
end
```

### Read the match and react to it

**Runs on:** server.

```lua
local SiegeService = require(game.ServerScriptService.Modules.Systems.Games.Siege.SiegeService)

print("Phase:", SiegeService.Phase())
print(player.Name, "is on", SiegeService.TeamOf(player))

local aliveDefenders = SiegeService.Players("Defenders", true)
print(#aliveDefenders, "defenders alive")

Extensions.Add("Siege.PhaseChanged", function(phase)
	print("Siege phase is now", phase)
end)

Extensions.Add("Siege.Ended", function(winner, reasonKey)
	print("Match over:", winner or "draw", reasonKey)
end)
```

### Tune the bomb plant

**Runs on:** server.

```lua
-- Breachers plant twice as fast.
local ClassService = require(game.ServerScriptService.Modules.Systems.Classes.ClassService)

Extensions.Add("Siege.PlantTimeMultiplier", function(player, _bombName)
	return if ClassService.ClassOf(player) == "Breacher" then 0.5 else 1
end)

-- No planting in the first 20 seconds of the Action phase.
local actionStartedAt = 0
Extensions.Add("Siege.PhaseChanged", function(phase)
	if phase == "Action" then -- check the phase names in Content.Games.Siege
		actionStartedAt = workspace:GetServerTimeNow()
	end
end)
Extensions.Add("Siege.PreventPlant", function(_player, _bombName)
	return workspace:GetServerTimeNow() < actionStartedAt + 20
end)
```

### Test a Siege match alone in Studio

No code needed: set the workspace attribute `SiegeTestTeam` to `Attackers` or `Defenders`, press Play, then press **K** to queue. Bots fill the other slots. See [Siege](SIEGE.md) and [Siege bots](SIEGE_BOTS.md).

---

## Gun abilities

Ability modules live in `Content.Guns.Abilities` and are turned on by naming them in a gun definition's `Abilities`. Full reference: [Writing an ability](ADDING_GUNS.md#writing-an-ability).

### Change a gun's stats

**Runs on:** both sides, once when the gun loads.

```lua
--!strict
--[[
	ExtendedMag: ten more rounds per magazine.
]]

local Types = require(game:GetService("ReplicatedStorage").Content.Guns.Types)

local ExtendedMag: Types.AbilityModule = {
	Name = "ExtendedMag",
}

function ExtendedMag.ModifyStats(stats)
	stats.MagSize += 10
end

return ExtendedMag
```

### Random critical shots

**Runs on:** both sides (shooter, server and other clients). Anything random in `OnFire` **must** come from `ctx.Random`, so every machine builds the same shot from the same seed.

```lua
--!strict
--[[
	CriticalRounds: 1 shot in 10 deals double damage.
]]

local Types = require(game:GetService("ReplicatedStorage").Content.Guns.Types)

local CHANCE = 0.1
local MULTIPLIER = 2

local CriticalRounds: Types.AbilityModule = {
	Name = "CriticalRounds",
}

function CriticalRounds.OnFire(ctx: Types.ShotContext)
	if ctx.Random:NextNumber() < CHANCE then -- never math.random here
		ctx.DamageMultiplier *= MULTIPLIER
	end
end

return CriticalRounds
```

Then turn it on in the gun's definition: `Abilities = { "CriticalRounds" }`.
