# Player data and content

Two kinds of data drive the game: **player data** (saved per player, owned by the server) and **content** (the game's own tables of guns, classes, crates and numbers, read by both sides).

## Player data: `Shared.Data`

!!! abstract "Source"

    `ReplicatedStorage.Modules.Shared.Data`, built on the Scribe package (ProfileStore underneath).

`Shared.Data` declares every player's saved data and the server's shared state once. Require it from either side and use `.Server` or `.Client`:

```lua title="From the Shared.Data header"
local Data = require(ReplicatedStorage.Modules.Shared.Data)
local data = Data.Server.WaitForData(player)    -- server: the player's data, or nil if they left
data.Coins.Increment(10)                        -- server writes
Data.Client.WaitForData()                       -- client: waits for its own data
Data.Client.Coins.Observe(function(coins) end)  -- client reads (wrap in Shared.ReadOnly to block writes)
```

| Root | What it is |
| --- | --- |
| **Template** | Saved per player. Wrap a group in `Scribe.Session({ ... })` for per-session data that is never saved |
| **ServerStore** | One per server, never saved, replicated to every client. For shared world state |

### Fields you'll use most

| Field | Type | Meaning |
| --- | --- | --- |
| `Coins` | Int, min 0 | Soft currency |
| `Kills`, `Deaths` | Int | Career stats |
| `WeaponSkins` | Set of skin Ids | Owned skins |
| `<Gun>Skin` (`RifleSkin`, …) | Enum | The equipped skin per gun, or `"None"`; mirrored to the Player attribute of the same name |
| `CrateInventory` | `[crateId].Count` | Crates bought and not opened |
| `Settings.Keybinds.<Action>` / `Volumes.<Group>` / `Options.<Option>` | String / 0–1 / Number | Saved settings (`Shared.PlayerSettings`) |
| `Tokens`, `OwnedClasses`, `Wins`, `Losses`, `Stats`, `LastMode` | | Declared by `Content.Store.Store` (a ScribeFragment) |

### Adding your own fields without editing `Shared.Data`

Tag a ModuleScript **`ScribeFragment`** and return `{ Template = { ... }?, ServerStore = { ... }? }`. `Content.Store.Store` adds currencies and stats this way. Each root name may only be used once across all fragments.

### Testing without saving

In Studio, set the workspace attribute **`ScribeNoSave = true`** in Edit mode before Play: profiles load real data and nothing is ever written. Live servers ignore it.

### Migrations

`Shared.Data` runs numbered migrations once per profile, in order, when it loads. A migration never changes after it ships; add a new one instead. (Migration 2, 2026-11-17, removed retired crates and their skins.)

### Purchases

Robux products are declared from data: one product per crate (`Crate_<Id>`) and per store item (`Store_<Id>`), each only once its id in `Shared.ProductIds` is set (`0` means "not created"). Each product's `Grant` runs inside a Scribe transaction, so **it must not yield**. Coin and Token purchases use `Data.Purchase`, which takes the price and gives the item in one transaction, or neither. See [Progression and economy](../systems/progression.md).

---

## Content: data you edit

!!! abstract "Source"

    `ReplicatedStorage.Content.*`

Content modules hold the game's data and tuning numbers. Systems read them; they never write them. **To change a number, change it here.**

### The "one file per thing" pattern

Guns, classes, consumables, crates and store items each have a `Definitions` folder with **one ModuleScript per entry**, plus a loader module that reads the folder, sorts it and answers questions. You add a class by adding a file, never by editing a big list.

```lua title="Content.Classes.Definitions.Flash (the whole file)"
--!strict
--[[
	Luca (Flash), attackers: Blinds a room before the push.
	Every field is described in Content.Classes.Classes. Order is the class's place in the menu.
]]

local ACTION = { "Action" }

return {
	Order = 6,
	Id = "Flash",
	Name = "Luca",
	Team = "Attackers",
	Icon = "",
	Role = "Support",
	Difficulty = 1,
	Description = "Blinds a room before the push.",
	Loadout = { "Rifle", "Pistol" },
	Categories = { { "Rifle" }, { "Revolver", "SMG" } },
	Ability = {
		Id = "Flashbang",          -- the module Systems.Classes.Abilities.Flashbang
		Name = "Flashbang",
		Description = "Throw a flashbang. Anyone looking at it when it pops is blinded.",
		Cooldown = 8,
		Charges = 3,
		Phases = ACTION,
		Tuning = {                 -- read by the ability as context.Tuning
			ThrowSpeed = 55,
			ThrowLift = 8,
			Fuse = 1.4,
			Radius = 30,
			FullTime = 3.5,
			MinTime = 0.6,
			FacingDot = 0.2,
			SelfShare = 0.5,
		},
	},
}
```

The loader then gives you a small API:

```lua title="Content.Classes.Classes"
Classes.List                       -- every class, in menu order
Classes.Get("Breacher")            -- a class by Id, or nil
Classes.ForTeam("Attackers")       -- the classes of a team, in order
Classes.CategoryOf("Rifle")        -- a gun's category, or nil
Classes.Allows(class, slot, gunId) -- may this class carry this gun in this loadout slot
```

A file that fails to load, has no `Id`, or repeats an `Id` is warned about at start.

### Content modules

| Module | Holds | Guide |
| --- | --- | --- |
| `Content.Guns.Definitions.*` → `Content.Guns.Registry` | One file per gun; `Registry[gunId]` with defaults filled in | [Guns](../systems/guns.md) |
| `Content.Guns.Loadouts`, `Melee`, `KnifeStats`, `Abilities.*`, `Skins.*` | Loadouts, bash numbers, gun ability hooks, skins | [Guns](../systems/guns.md) |
| `Content.Classes.Definitions.*` → `Content.Classes.Classes` | One file per class | [Classes](../systems/classes.md) |
| `Content.Consumables.Definitions.*` → `Consumables` | Grenade and smoke; `PER_LIFE`, `DEFAULT`, `THROW_COOLDOWN` | [World](../systems/world.md) |
| `Content.Crates.*`, `Content.Store.*` | Crates and store items, one file each; `Store.Style` colors | [Progression](../systems/progression.md) |
| `Content.Games.Siege` | Phase times, plant time, rounds, texts, win reasons | [Siege](../systems/siege.md) |
| `Content.Games.ClearHouse`, `Tutorial`, `SiegeBots` | The other match kinds and the bots | [Siege](../systems/siege.md), [NPCs](../systems/npcs.md) |
| `Content.Matchmaking` | Party and team sizes, queue `MODES`, waits, MemoryStore names | [Matchmaking](../systems/matchmaking.md) |
| `Content.Drones`, `Content.Cameras` | Drone and camera numbers and attribute names | [Drones and cameras](../systems/drones-cameras.md) |
| `Content.Breakables.*`, `Content.Destruction.SoftWallConfig` | Board types and stats; soft wall settings per gun | [World](../systems/world.md) |
| `Content.NPC.Profiles.*` | NPC profiles | [NPCs](../systems/npcs.md) |
| `Content.Movement.Config` | Speeds, heights, camera feel | [Client](../systems/client.md) |
| `Content.Effects.Registry`, `Effects.Parts.*` | Every effect by name | [Effects](effects.md) |
| `Content.BattlePass`, `Quests`, `Progress`, `Analytics` | Season, quests, streaks, analytics names | [Progression](../systems/progression.md) |
| `Content.Theme`, `Icons`, `Music` | UI colors and fonts, icons, music | [Client](../systems/client.md) |

```lua title="Reading content anywhere"
local Content = game.ReplicatedStorage.Content
local Registry = require(Content.Guns.Registry)
local rifle = Registry.Rifle                -- defaults filled in
print(rifle.DisplayName, rifle.Damage, rifle.MagSize)
```
