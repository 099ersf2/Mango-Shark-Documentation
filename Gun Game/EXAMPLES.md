[Documentation home](index.md) / Gun Game

# Task-based code examples

These short Luau examples show common tasks using the documented game APIs. They are snippets, not standalone scripts. Put server code in a loaded server `ModuleScript`, and client code in a loaded `ClientOnly` module. See the [AI coding guide](AI_CODING_GUIDE.md) for module placement and loading rules.

## Give a player a gun

Use this in server code after the game flow has authorized the player to receive a weapon. For a saved loadout, use `LoadoutService.Apply(player)` instead.

```lua
local GunService = require(
	game.ServerScriptService.Modules.Systems.Guns.GunService
)

GunService.Give(player, "Rifle")
```

See [Adding guns](ADDING_GUNS.md) for gun definitions and assets.

## Apply damage with kill credit

Call `Combat.ApplyHit` on the server when a game system damages a target and should credit the attacker in the kill feed and damage log. Confirm that the target is valid for the current game state before calling it.

```lua
local Combat = require(
	game.ServerScriptService.Modules.Systems.Combat.Combat
)

Combat.ApplyHit(targetHumanoid, 30, {
	Attacker = player,
	Item = "Trap",
})
```

For damage without attacker credit, use `Combat.DealDamage(targetHumanoid, 30)`.

## Award coins after loading player data

`WaitForData` can return `nil` if the player leaves before their profile is ready. Check the result before changing data.

```lua
local Data = require(
	game.ReplicatedStorage.Modules.Shared.Data
)

local data = Data.Server.WaitForData(player)
if data then
	data.Coins.Increment(100)
end
```

See [Store, currencies, crates, and stats](STORE.md) for the game's economy rules.

## Add a gun damage multiplier

Register an extension from loaded server code. Return `1` for the default damage; return a different multiplier only for the gun or rule you want to affect.

```lua
local Extensions = require(
	game.ReplicatedStorage.Modules.Shared.Extensions
)

Extensions.Add("Gun.DamageMultiplier", function(who, gunId, humanoid, hit)
	if gunId == "Rifle" then
		return 1.25
	end

	return 1
end)
```

See the [shared API reference](API_SHARED.md) for the complete extension-point list.

## Read a player setting on the server

Use `SettingsService` when server code needs a player's saved option.

```lua
local SettingsService = require(
	game.ServerScriptService.Modules.Services.SettingsService
)

local aimAssistEnabled = SettingsService.GetOption(player, "AimAssist")
```

## Open a menu on the client

Call menu APIs from a loaded client module. The menu name must already exist in the UI.

```lua
local Menus = require(
	game.ReplicatedStorage.Modules.Client.Core.Menus
)

Menus.Open("SkinShop")
```

See [UI](UI.md) for menu names and interface structure.
