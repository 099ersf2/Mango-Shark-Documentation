# Admin commands (Cmdr)

Open the command bar with **F2**, or the **CMD** button on touch screens (shown only to admins in `Modules.Classes.Admins`). The server checks `Classes.Admins` again for every command (`CmdrSetup.Hooks.BeforeRun`).

!!! abstract "Source"

    `ServerScriptService.Modules.Services.CmdrSetup` (`Commands`, `Hooks`, `Types`).

## Commands

| Command | Arguments | What it does |
| --- | --- | --- |
| `givegun` | player, gunId | Gives a gun from `Content.Guns.Registry` with full ammo |
| `spawnnpc` | profile, count? | Spawns NPCs in front of you (no respawn) |
| `clearnpcs` | — | Removes every NPC |
| `softwallpunch` (`swpunch`) | radius?, ring? | Holes the wall you look at; a ring knocks a disc out |
| `softwallreset` (`swreset`) | all? | Restores the wall you look at, or every wall |
| `nuke` | player | A warned strike that damages players, NPCs and boards nearby |
| `announce` | text | A banner for everyone (the example command) |
| `range` (`showcase`) | — | Takes you to the gun animation range ([Gun showcase](../../GUN_SHOWCASE.md)) |
| `movedebug` | — | Toggles the movement readout |
| `aimassistpc` (`aapc`) | player, on? | Controller aim assist on mouse and keyboard, for testing; leave out `on` to toggle |
| `givedevskins` / `takedevskins` | players | Give or take the Developer skin pack (`StoreService.GiveSkins`) |

!!! note "Removed"

    `match`, `matchmode` and `matchset` were archived with the old match modes. Siege matches are controlled by `SiegeService.ForceEnd` and the queue.

## Adding a command

A command is **two ModuleScripts** in `CmdrSetup.Commands`: a definition `<Name>` and its server half `<Name>Server`. The real `givegun`:

```lua title="CmdrSetup.Commands.GiveGun"
return {
	Name = "givegun",
	Aliases = {},
	Description = "Gives a player a gun from Content.Guns, with a full magazine and reserve. For testing guns.",
	Group = "Admin",
	Args = {
		{ Type = "player", Name = "player", Description = "Who gets the gun" },
		{ Type = "gun", Name = "gunId", Description = "An Id in Content.Guns.Registry, like AssaultRifle" },
	},
}
```

```lua title="CmdrSetup.Commands.GiveGunServer"
local ServerScriptService = game:GetService("ServerScriptService")
local GunService = require(ServerScriptService.Modules.Systems.Guns.GunService)

-- The return value is the reply shown in the command bar
return function(_context, player: Player, gunId: string)
	local tool = GunService.Give(player, gunId)
	if not tool then
		return `No gun named {gunId}`
	end
	return `Gave {player.Name} a {tool.Name}`
end
```

1. Copy both files, rename to your command.
2. Keep `Group = "Admin"`.
3. Custom argument types (`CmdrSetup.Types.Gun`, used as `Type = "gun"`, and `Types.NpcProfile`) give autocomplete over the game's own Ids; add one there for yours.
4. Call real services from the server half; don't put game logic in the command.
5. Add it to the table above.
