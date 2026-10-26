# Kits, Abilities, Items, Effects & Blocks

A data-driven framework for kits, abilities, items, effects and block building in a Roblox game.

- **Definitions:** kits, items and blocks are plain definition modules. Abilities are small server modules with optional client specs. Effects are entries in one registry.
- **Kit state:** all player kit state lives in a shared [Scribe](https://scribe.ericplane.dev/) store. The server writes it and the client reads it.
- **HUD:** the HUD builds itself from the definitions, so adding content never requires editing HUD code.
- **Effects:** the server never creates sounds or visuals. It sends an effect name, and every client plays it.
- **Blocks:** Bedwars-style building on a 3-stud grid. The server owns every block; clients only ask, then predict so building feels instant.
- **Admin commands:** Cmdr commands to give items, kits and abilities while testing.

---

## Table of Contents

- [Overview](#overview)
- [Project Layout](#project-layout)
- [Core Concepts](#core-concepts)
  - [Kits](#kits)
  - [Items](#items)
  - [Abilities](#abilities)
  - [Kit State](#kit-state)
  - [Effects](#effects)
  - [Blocks](#blocks)
- [Guides](#guides)
  - [Adding a Kit](#adding-a-kit)
  - [Adding an Item](#adding-an-item)
  - [Adding an Ability](#adding-an-ability)
  - [Adding an Effect](#adding-an-effect)
  - [Adding a Block](#adding-a-block)
  - [Adding a Special Block](#adding-a-special-block)
  - [Custom UI](#custom-ui)
  - [Setting a Player's Kits](#setting-a-players-kits)
- [Effects & Sound](#effects--sound)
  - [Effect Registry](#effect-registry)
  - [Playing Effects](#playing-effects)
  - [Replication](#replication)
  - [Sound Groups](#sound-groups)
  - [Volume Settings](#volume-settings)
  - [Writing a New Visual Kind](#writing-a-new-visual-kind)
- [Blocks & Building](#blocks--building)
  - [The Grid](#the-grid)
  - [Block Definitions](#block-definitions)
  - [Tool Types & Breaking](#tool-types--breaking)
  - [Placing](#placing)
  - [Map Blocks](#map-blocks)
  - [Block Hooks](#block-hooks)
  - [Generators, Beds & the Shop](#generators-beds--the-shop)
  - [Stack Items & Inventory](#stack-items--inventory)
  - [How a Request Flows](#how-a-request-flows)
  - [Grid Settings](#grid-settings)
- [Admin Commands](#admin-commands)
- [HUD](#hud)
- [Input](#input)
- [API Reference](#api-reference)
  - [Server](#server)
  - [Shared](#shared)
  - [Client](#client)
- [Packets](#packets)
- [Built-in Content](#built-in-content)
- [Notes & Gotchas](#notes--gotchas)

---

## Overview

| Concept | What it is | Where it lives |
|---|---|---|
| **Kit** | A loadout: stats, starting items, kit abilities, kit state, and HUD info | `Classes.Kits.<Kit>` |
| **Item** | A Tool with a definition: abilities, held-item HUD info, server hooks, block/tool data | `Classes.Items.<Item>` |
| **Ability** | Server behaviour plus an optional client spec | `Systems.Abilities.Library.<Ability>` + `Client.Abilities.Library.<Ability>` |
| **Kit state** | Per-player, per-kit data replicated to the owning client | `Shared.KitState` (built on Scribe) |
| **Effect** | A named sound, visual and/or animation, played on clients | `Classes.Effects` (registry) + `Client.Effects` (player) |
| **Block** | A grid block type: hardness, preferred tool, model, sounds, hooks | `Classes.Blocks.<Block>` + `Shared.Blocks` |
| **Tool type** | How an item breaks blocks: Pickaxe, Axe, Shovel, Sword, Hand | `Shared.ToolTypes` |
| **Stack item** | An item carried as a count (blocks, iron), shown as one Tool | `Shared.Inventory` |

Key rules:

- **Kit abilities** are granted by a player's active kits. Some abilities can also be **given on their own**, without a kit (see [Admin Commands](#admin-commands)).
- **Item abilities** are granted by the **held** item, and work with **no kit equipped**.
- A player can have **several kits at once**.
- The server is the only writer of kit state, inventory and block damage. Client views are **read-only** and error on writes.
- The server **never** creates, plays or tweens effects. It calls `EffectService.Play`, and clients play the effect.
- Every client sound sits in a **sound group** under `SoundService.Master`.
- The server is the **only** place blocks are placed, broken or changed. Clients send requests and draw predictions.

---

## Project Layout

```text
ReplicatedStorage
âââ Assets
â   âââ Sounds                        Effect sounds (Hit, Swing, BlockPlace, BlockBreak, Werewolfâ¦)
â   âââ Vfx                           Particle Attachments (HitFX, SwingR, SwingL, Heal)
â   âââ Music/Primary                 Background songs
â   âââ Models
â       âââ Items/<Item>              Tool models, named after the item definition
â       âââ Blocks/<Model>            Block parts and models, named by a block's Model
â       âââ CapsuleSplashModels       Capsule puddle parts (Fire/Poison/Speed/ShockSplash)
â       âââ GolemBoulder
âââ Inputs
â   âââ Default                       InputContext: Ability1âAbility5 slot keys
âââ Modules
    âââ Classes
    â   âââ Kits/<Kit>                Kit definitions
    â   âââ Items/<Item>              Item definitions
    â   âââ Blocks/<Block>            Block definitions
    â   âââ Effects                   Effect registry: every sound and visual
    â   âââ SwordLevels               Barbarian rage levels
    âââ Shared
    â   âââ Data                      Scribe template (Kits, Abilities, Inventory roots + ServerStore)
    â   âââ KitState                  Active kits, granted abilities and kit state
    â   âââ Items                     Item helper (definitions + item ability wiring)
    â   âââ Blocks                    Block helper: definitions, grid math, break rules
    â   â   âââ Config                Grid and building settings
    â   âââ ToolTypes                 Pickaxe, Axe, Shovel, Sword, Hand
    â   âââ BlockState                Block damage (ServerStore), read-only on clients
    â   âââ Inventory                 Stack item counts
    â   âââ ReadOnly                  Read-only wrapper for client Scribe views
    â   âââ Packets                   Every network packet
    âââ Handlers
    â   âââ AnimationHandler          Loads and tracks animations (used by the Animation part)
    âââ Utilities
    â   âââ Cmdr                      Cmdr command bar
    âââ Client
        âââ Core
        â   âââ Abilities             Client ability framework
        â   âââ Inputs                Slot keys and key labels
        â   âââ Music                 Background music (plays through the Music effect)
        â   âââ CmdrClient            Opens Cmdr with F2
        â   âââ ToolSync              Server-side equip sync
        âââ Effects                   Client effect player: Play / Stop
        â   âââ Context               One playing effect: placement, timing, cleanup
        â   âââ Parts/<Kind>          Sound, Animation and visual parts
        âââ Audio
        â   âââ SoundGroups           Group lookup and assignment
        â   âââ AudioSettings         Group volumes (Store = saved values)
        âââ Blocks
        â   âââ BlockMap              Client copy of the occupancy map
        â   âââ BlockInput            Mouse â break / place actions
        â   âââ Targeting             Hover target and predictive placement
        â   âââ BlockVisuals          Hover outline, preview, placeholders, cracks
        â   âââ BlockController       Ties the above together every frame
        â   âââ Hooks/<Hook>          Client block hooks (ShopKeeper)
        âââ Abilities/Library/<Ability>   Client ability specs
        âââ Hud
        â   âââ KitPanel              Kit information panel
        â   âââ AbilityBar            Ability buttons
        â   âââ ItemPanel             Held item information panel
        â   âââ InfoRows              Shared row renderer
        â   âââ CustomUI              Hand-made UI support
        âââ Kits/<Kit>                Kit-only client code (overlays, highlights)
        âââ Items/<Item>              Item-only client code (aim arcs)

ServerScriptService
âââ Modules
    âââ Services
    â   âââ CmdrSetup                 Registers Cmdr hooks, types and commands
    â       âââ Hooks/BeforeRun       Who may run commands
    â       âââ Types/<type>          item, kit, ability, currency
    â       âââ Commands/<Command>    Definition + <Command>Server
    âââ Systems
        âââ Kits
        â   âââ KitService            Sets kits, stats, items, hooks, granted abilities
        â   âââ Appearance            Applies kit rig looks
        â   âââ Hooks/<Kit>           Per-kit server hooks
        âââ Items
        â   âââ ItemService           Gives and takes items, runs item hooks, server-side equips
        â   âââ Hooks/<Hook>          Per-item server hooks
        âââ Abilities
        â   âââ AbilityService        Validates and runs ability requests
        â   âââ Library/<Ability>     Server ability modules
        âââ Effects
        â   âââ EffectService         Sends effects to clients
        âââ Blocks
        â   âââ BlockService          Places, breaks and changes blocks
        â   â   âââ World             Occupancy map: which block fills each cell
        â   â   âââ Rules             Build area, free cells, NoBuild, reach, players in the way
        â   â   âââ Damage            Break progress and healing
        â   âââ Hooks/<Hook>          Server block hooks (Generator, Bed, ShopKeeper)
        âââ Werewolf
            âââ Appearance            Claw models, werewolf body and head
            âââ Claws                 Overview + Config, Session, Rest, Moon, Hunt,
                                      Attack, Lunge, Hit, Effects

Workspace
âââ World                             Map blocks, tagged Block
âââ Generators                        Generator blocks, tagged Block
âââ PlacedBlocks                      Blocks placed by players (created by the server)

SoundService
âââ Master                            Master sound group
    âââ Music
    âââ Abilities
    âââ Effects
    âââ UI
    âââ Ambient

StarterGui
âââ Main
    âââ KitPanel                      Kit info panel  (restyle via its Templates folder)
    âââ AbilityBar                    Ability bar     (restyle via its Templates folder)
    âââ ItemPanel                     Item info panel (restyle via its Templates folder)
    âââ Rage                          Custom UI for the Barbarian
    âââ DashCharge                    Custom UI for the Dash ability

ServerStorage
âââ README                            In-Studio copy of these docs (disabled Script)
âââ WerewolfClaws                     Claw and eye models (server welds them on)
âââ UIBackup                          Backups of the original UI
âââ EffectsBackup_2026_10_25          Scripts and assets from before the effects rework
âââ BlocksBackup_2026_10_25           Scripts from before the block system
```

---

## Core Concepts

### Kits

A kit is a ModuleScript in `ReplicatedStorage.Modules.Classes.Kits` that returns a table:

| Field | Type | Required | Description |
|---|---|---|---|
| `DisplayName` | `string` | â | Shown to players |
| `Description` | `string` | â | Shown to players |
| `MaxHealth` | `number` | â | Applied on kit set and every spawn. With several kits, the highest wins |
| `WalkSpeed` | `number` | â | Same as `MaxHealth` |
| `Items` | `{ string }` | â | Item names given on kit set and every spawn |
| `Abilities` | `{ string }` | â | Abilities this kit grants |
| `State` | `{ [string]: Scribe field }` | â | Kit state, declared with Scribe |
| `Info` | `{ InfoRow }` | â | Rows for the kit panel |
| `CustomUI` | `{ [string]: (gui, state) -> boolean? }` | â | Hand-made UI in `StarterGui.Main` |

Server hooks go in `Systems.Kits.Hooks.<Kit>` (all optional):

| Hook | When it runs |
|---|---|
| `OnGranted(player)` | The kit is added |
| `OnSpawned(player)` | Every spawn while the kit is active |
| `OnRemoved(player)` | The kit is taken away |
| `Start()` | Once, by ModuleLoader (e.g. connect an equip prompt) |

### Items

An item is a ModuleScript in `ReplicatedStorage.Modules.Classes.Items`. Its Tool model is the Tool with the **same name** in `ReplicatedStorage.Assets.Models.Items`.

| Field | Type | Required | Description |
|---|---|---|---|
| `DisplayName` | `string` | â | Shown to players |
| `Image` | `string` | â | Icon for the HUD |
| `Abilities` | `{ string }` | â | Abilities granted while held. **The first one is the click action** |
| `Info` | `{ InfoRow }` | â | Rows for the item panel. No rows = panel hidden |
| `CustomUI` | `{ [string]: (gui, context) -> boolean? }` | â | Hand-made UI shown while held |
| `Hooks` | `string` | â | Name of a module in `Systems.Items.Hooks` |
| `Stack` | `boolean` | â | Carried as a count in `Shared.Inventory` (blocks, resources). See [Stack Items](#stack-items--inventory) |
| `Block` | `string` | â | The block in `Classes.Blocks` this item places |
| `ToolType` | `string` | â | `Pickaxe`, `Axe`, `Shovel` or `Sword`. No `ToolType` = held like an empty hand |
| `Speed` | `number` | â | Breaking speed multiplier, with `ToolType` |
| `CanBreakBlocks` | `boolean` | â | `false` for swords. With `ToolType` |
| *anything else* | `any` | â | Item data, e.g. `Damage`, `Cooldown`, `Capsule`, `HealAmount` |

Item hooks (`Systems.Items.Hooks.<Hook>`, all optional):

| Hook | When it runs |
|---|---|
| `OnGiven(player, tool)` | Every time the item is given |
| `Start()` | Once, by ModuleLoader |

### Abilities

An ability has two halves:

**Server** â `Systems.Abilities.Library.<Ability>`:

| Field | Type | Description |
|---|---|---|
| `Name` | `string` | Matches the name in a kit's or item's `Abilities` |
| `Cooldown` | `number?` | Seconds between uses, per player |
| `Activate` | `(player, aim, tool?) -> (false \| number \| any)` | Runs the ability. `tool` is set when the held item grants it |
| `Passive` | `boolean?` | `true` for abilities with no `Activate` (e.g. Rage) |

`Activate` return values:

| Return | Effect |
|---|---|
| `false` | Nothing happened â no cooldown starts |
| a `number` | Use this as the cooldown instead of `Cooldown` |
| anything else | Success â `Cooldown` applies |

A request runs only if the ability exists, the **held item, an active kit, or a granted ability** allows it, and its cooldown has passed. Cooldowns replicate to the client automatically.

**Client** (optional) â `Client.Abilities.Library.<Ability>` calls `Abilities:Register(name, spec)` in `Init`. Every field is optional:

| Field | Type | Description |
|---|---|---|
| `DisplayName` | `string` | Button label. Defaults to the ability name |
| `Icon` | `string` | Button image. Defaults to the held item's `Image`, then the first letter |
| `Passive` | `boolean` | Keep it off the ability bar |
| `Hold` | `boolean` | Press calls `Begin`, release calls `End` |
| `Activate(tool)` | function | Runs on press. Defaults to asking the server |
| `Begin(tool)` / `End(tool)` / `Cancel(tool)` | function | For `Hold` abilities. `Cancel` runs if it stops being usable while held (defaults to `End`) |
| `Enabled(tool)` | `-> boolean` | `false` greys the button and ignores presses |
| `Cooldown(tool)` | `-> (remaining, total)` | Defaults to the server cooldown |
| `CustomUI` | `{ [string]: (gui, context) -> boolean? }` | Hand-made UI shown while the ability is usable |

With no client spec, pressing the ability simply asks the server, sending the aim point.

#### Granted abilities

An ability can be given to a player **without a kit** with `KitService:GrantAbility(player, name)` (or the `giveability` command). Granted abilities count for `HasAbility`, show on the ability bar after the kit abilities, and last until the player leaves.

Only abilities that need **no item** can be granted (`KitState.Grantable()`). An ability qualifies when:

- at least one kit lists it,
- no item lists it, and
- every kit that lists it gives no items.

Today that's **Brew, ChickenRush, RockThrow and SummonCauldron**. Slash, Claw, Throw, Consume, Dash, Rage, Rest and Hunt need an item and are refused. New kits and items are picked up by the same rule automatically.

### Kit State

Kit state is declared in the kit's `State` table with Scribe field types and stored in a **session** (not saved) Scribe root. The server writes; the owning client gets a read-only view.

```lua
State = {
	Rocks = Scribe.Int(0, { Min = 0, Max = 100 }),
	Scale = Scribe.Number(1, { Min = 0, Max = 100 }),
},
```

```lua
-- Server
KitState.Of(player, "Golem").Rocks.Set(5)

-- Server and client
KitState.Of(player, "Golem").Rocks.Get()
KitState.Of(player, "Golem").Rocks.Observe(function(rocks) end)
KitState.Get(player, "Golem")          -- snapshot table

-- Client: writes are rejected
KitState.Of(player, "Golem").Rocks.Set(99)
--> error: KitState is read-only on the client: Set was rejected
```

The `Kits` session root also holds `Equipped` (active kits) and `Granted` (granted abilities).

> â ï¸ Don't name a state field after a Scribe accessor method (`Active`, `Get`, `Set`, `Count`, `Remove`, â¦). The method shadows the field.

### Effects

An effect is a named entry in `Classes.Effects`. It can have a sound, one or more visual parts, an animation, a sound group, and a replication rule. The same registry is read by both sides:

- **Server:** `EffectService.Play(name, options)` sends the name and options to the right clients.
- **Client:** `Effects.Play(name, options)` plays it, either because the server asked or locally (UI, music, own animations).

Each play gets a **Context** that places the effect, times it, and destroys everything it created when it ends. An effect ends when:

- all of its parts finish, or
- it is stopped, or
- its `Target` leaves the game, or
- its `Tool` leaves the `Target` (e.g. the claws are unequipped).

See [Effects & Sound](#effects--sound) for the full reference.

### Blocks

A block is a ModuleScript in `ReplicatedStorage.Modules.Classes.Blocks`. Blocks fill cells of a 3-stud grid. The server keeps an **occupancy map** of which block fills each cell, and every client keeps a copy.

- **Breaking** takes `Hardness / speed` seconds of holding the mouse with a breaking tool. Damage replicates to everyone and shows as cracks.
- **Placing** is predictive, like Bedwars: aim anywhere ahead and the next block goes at the end of your bridge.
- **Special blocks** (generators, beds, the shop keeper) are normal blocks with a `Hooks` module.

See [Blocks & Building](#blocks--building) for the full reference.

---

## Guides

### Adding a Kit

1. **Create the definition** â `Classes.Kits.Ninja`:

   ```lua
   --!strict
   local ReplicatedStorage = game:GetService("ReplicatedStorage")
   local Scribe = require(ReplicatedStorage.Modules.Packages.Scribe)

   return {
   	DisplayName = "Ninja",
   	Description = "Fast and sneaky.",
   	MaxHealth = 90,
   	WalkSpeed = 20,
   	Items = { "Wooden Sword" },
   	Abilities = { "Vanish" },
   	State = {
   		Smoke = Scribe.Int(3, { Min = 0, Max = 3 }),
   	},
   	Info = {
   		{
   			Label = "Smoke",
   			Bar = function(state) return state.Smoke / 3 end,
   			Text = function(state) return string.format("%d / 3", state.Smoke) end,
   		},
   	},
   }
   ```

2. **Add server hooks** *(optional)* â `Systems.Kits.Hooks.Ninja`:

   ```lua
   --!strict
   local KitService = require(script.Parent.Parent.KitService)

   local Ninja = {}

   function Ninja:OnGranted(player: Player) end
   function Ninja:OnSpawned(player: Player) end
   function Ninja:OnRemoved(player: Player) end

   function Ninja:Start()
   	-- e.g. connect an equip prompt that calls KitService:SetKit(player, "Ninja")
   end

   return Ninja
   ```

3. **Add each new ability** â see [Adding an Ability](#adding-an-ability).
4. **Add its effects** â see [Adding an Effect](#adding-an-effect).
5. **Add kit-only client code** *(optional)* â `Client.Kits.Ninja/...`

No HUD changes are needed: the kit panel reads `Info`, and the ability bar reads `Abilities`. The `givekit` command picks up the new kit automatically.

### Adding an Item

1. **Add the Tool** to `ReplicatedStorage.Assets.Models.Items`, named after the item.
2. **Create the definition** â `Classes.Items.Smoke Bomb`:

   ```lua
   --!strict
   return {
   	DisplayName = "Smoke Bomb",
   	Image = "rbxassetid://0",
   	Abilities = { "Throw" },        -- clicking the Tool uses this
   	Info = {
   		{
   			Label = "Carried",
   			Text = function(context) return tostring(context.Count) end,
   		},
   	},
   }
   ```

3. **Add a server hook** *(optional)* â `Systems.Items.Hooks.<Name>` with `OnGiven(player, tool)`, and set `Hooks = "<Name>"` in the definition.
4. **Give it** with `ItemService.Give(player, "Smoke Bomb")`, list it in a kit's `Items`, or use `give me "Smoke Bomb"` in Cmdr.

A block-breaking tool needs `ToolType`, `Speed` and `CanBreakBlocks`:

```lua
-- Classes.Items.Stone Pickaxe
return {
	DisplayName = "Stone Pickaxe",
	Abilities = {},
	ToolType = "Pickaxe",
	Speed = 1.5,                 -- 1.5x faster than a wooden pickaxe
	CanBreakBlocks = true,
}
```

### Adding an Ability

1. **Server** â `Systems.Abilities.Library.Vanish`:

   ```lua
   --!strict
   local EffectService = require(script.Parent.Parent.Parent.Effects.EffectService)

   return {
   	Name = "Vanish",
   	Cooldown = 8,
   	Activate = function(player: Player, aim: Vector3, tool: Tool?)
   		-- gameplay here, then ask clients for the visuals
   		EffectService.Play("NinjaVanish", { Target = player.Character })
   		-- return false if nothing happened, or a number to set the cooldown
   	end,
   }
   ```

2. **Client** *(optional)* â `Client.Abilities.Library.Vanish`:

   ```lua
   --!strict
   local RunService = game:GetService("RunService")
   local ReplicatedStorage = game:GetService("ReplicatedStorage")

   local Abilities = require(ReplicatedStorage.Modules.Client.Core.Abilities)

   local Vanish = {}

   function Vanish:Init()
   	if RunService:IsServer() then
   		return
   	end
   	Abilities:Register("Vanish", {
   		DisplayName = "Vanish",
   		Icon = "rbxassetid://0",
   	})
   end

   return Vanish
   ```

3. **Grant it** by listing it in a kit's or item's `Abilities`. If it needs no item, it can also be given with `giveability`.

### Adding an Effect

Adding an effect only needs an entry in `Classes.Effects`.

1. **Put its assets** in `ReplicatedStorage.Assets` â sounds in `Sounds`, particle Attachments in `Vfx`, models in `Models`.
2. **Add the entry**:

   ```lua
   -- Classes.Effects
   NinjaVanish = {
   	Group = "Abilities",                    -- sound group
   	Replicate = "Nearby",                   -- All, Nearby or Local
   	Range = 150,                            -- studs, for Nearby
   	Sound = { Asset = "Poof", Volume = 0.8, Pitch = { 0.9, 1.1 } },
   	Visual = {
   		{ Kind = "Particles", Asset = "SmokeFX", Count = 20, Lifetime = 1 },
   		{ Kind = "Highlight", FillTransparency = 0.5, Lifetime = 0.3 },
   	},
   },
   ```

3. **Play it** from the server with `EffectService.Play("NinjaVanish", { Target = character })`, or from the client with `Effects.Play(...)`.

If no existing visual kind fits, see [Writing a New Visual Kind](#writing-a-new-visual-kind).

### Adding a Block

1. **Add the model** â a part or model in `ReplicatedStorage.Assets.Models.Blocks`, sized to the block's cells (3 studs per cell).
2. **Create the definition** â `Classes.Blocks.Glass`:

   ```lua
   --!strict
   return {
   	DisplayName = "Glass",
   	Id = 14,                         -- unique, never reused once players have it
   	Hardness = 0.5,                  -- seconds with the preferred tool at Speed 1
   	PreferredTool = nil,             -- any breaking tool is full speed
   	Breakable = true,
   	Placeable = true,
   	Model = "Glass",
   	SoundCategory = "Stone",         -- Variant of the place/break/hit sounds
   	BreakEffect = "BlockBreak",
   	PlaceEffect = "BlockPlace",
   }
   ```

3. **Make it placeable by players** â add a stack item with `Block` pointing at it, and its Tool model in `Assets.Models.Items`:

   ```lua
   -- Classes.Items.Glass
   return {
   	DisplayName = "Glass",
   	Abilities = {},
   	Block = "Glass",
   	Stack = true,
   }
   ```

4. **Sell it** *(optional)* â add an entry to the shop keeper's `Shop` list.

`Shared.Blocks` checks every definition when it loads and **errors right away** on a missing or wrong field, or a duplicate `Id`.

### Adding a Special Block

1. Set `Hooks = "Trap"` on the block definition, plus any data the hook reads (e.g. `Damage = 10`).
2. **Server hook** â `Systems.Blocks.Hooks.Trap`:

   ```lua
   --!strict
   local Trap = {}

   function Trap.OnPlaced(block, player: Player?)
   	block.Data.Armed = true
   end

   function Trap.OnTick(block, dt: number)
   	-- runs every Config.TICK_INTERVAL
   end

   function Trap.CanBreak(block, player: Player): boolean
   	return block.Owner ~= player
   end

   return Trap
   ```

3. **Client hook** *(optional)* â `Client.Blocks.Hooks.Trap` with `OnHover(entry, hovering)` and/or `OnInteract(entry)`.
4. **A prompt** *(optional)* â `Interact = { ActionText = "Arm" }` on the definition gives the block a ProximityPrompt that runs `OnInteract`.

See [Block Hooks](#block-hooks) for every hook.

### Custom UI

Use your own hand-made UI instead of (or as well as) info rows. Kits, items and abilities all support it.

1. Build the element in `StarterGui.Main` (it's hidden automatically in play, so you can leave it visible while editing).
2. Name it in a `CustomUI` table with an update function:

```lua
CustomUI = {
	-- StarterGui.Main.Rage
	Rage = function(gui, state)
		gui.RageBar.Bar.Size = UDim2.fromScale(state.Rage / 100, 1)
	end,
},
```

| Defined on | Shown while | Function receives |
|---|---|---|
| Kit | the kit is active | the kit's state snapshot |
| Item | the item is held | an item `Context` |
| Ability spec | the ability is usable | an ability `Context` |

The function runs **every frame**. **Return `false` to hide** the element for that frame â useful for UI that only appears while something is happening:

```lua
-- Dash ability: the charge bar only shows while charging
DashCharge = function(gui, context)
	local state = context.State("Samurai")
	if not state or not state.Charging then
		return false
	end
	local charge = math.clamp((workspace:GetServerTimeNow() - state.ChargeStartedAt) / 2, 0, 1)
	gui.Track.Fill.Size = UDim2.fromScale(charge, 1)
	return true
end,
```

A function that errors is warned once and hides its element; it never breaks the HUD.

### Setting a Player's Kits

```lua
local KitService = require(ServerScriptService.Modules.Systems.Kits.KitService)

KitService:SetKits(player, { "Golem", "Werewolf" })   -- several at once, in order
KitService:SetKit(player, "Golem")                     -- one, replacing the others
KitService:SetKit(player, nil)                         -- none

KitService:GrantAbility(player, "ChickenRush")         -- one ability, no kit
KitService:RevokeAbility(player, "ChickenRush")
```

The client sees changes through `KitState.ObserveKits(player, fn)` and `KitState.ObserveGranted(player, fn)`.

When kits change:

- Removed kits run `OnRemoved` and lose their items.
- Added kits get stats, items and `OnGranted`.
- If a removed kit changed the character's look, the character respawns.

---

## Effects & Sound

### Effect Registry

`ReplicatedStorage.Modules.Classes.Effects` returns a table of effects by name. It's the **only** place to add, change or remove an effect, or to choose its sound group.

| Field | Type | Default | Description |
|---|---|---|---|
| `Group` | `string` | `"Effects"` | Sound group: `Music`, `Abilities`, `Effects`, `UI`, `Ambient` |
| `Replicate` | `"All" \| "Nearby" \| "Local"` | `"All"` | How the server sends it. See [Replication](#replication) |
| `Range` | `number` | `200` | Studs, for `Nearby` |
| `Persistent` | `boolean` | `false` | Runs until stopped (e.g. a looping snore). Playing it again on the same target restarts it |
| `Sound` | part or `{ part }` | â | Sound part(s) |
| `Visual` | part or `{ part }` | â | Visual part(s). `Kind` names a module in `Client.Effects.Parts` |
| `Animation` | part | â | Animation part, played through `AnimationHandler` |
| `Variants` | `{ [any]: fields }` | â | Fields that replace the ones above when played with that `Variant` (e.g. a combo step, capsule type, or block sound category) |

All `Delay` and timing values are divided by the `Speed` the effect is played at.

#### Sound part

| Field | Description |
|---|---|
| `Asset` | Name of a Sound in `Assets.Sounds`. Without `Asset` or `Id`, the `Sound` in the play options is used |
| `Id` | A sound id, instead of `Asset` |
| `Volume` | Sound volume |
| `Pitch` | A `PlaybackSpeed`, or `{ min, max }` for a random one |
| `RollOff` | `{ Min = studs, Max = studs, Mode = Enum.RollOffMode }` |
| `Looped` | Loop the sound |
| `Attach` | Name of a part in the target to play from, e.g. `"Head"`. Defaults to the root part |
| `Global` | Play without a position, heard the same everywhere |
| `Delay` | Seconds before it plays |
| `Lifetime` | Seconds before it's removed. Defaults to when the sound ends |

#### Animation part

| Field | Description |
|---|---|
| `Id` | Animation id |
| `Type` | The `AnimationHandler` type. Defaults to the effect's name |
| `Markers` | Marker names that call the play options' `OnMarker` |
| `Looped` | Loop until the effect stops |
| `FadeTime` | Fade-in time |

#### Visual kinds

| Kind | Fields | What it does |
|---|---|---|
| `Particles` | `Asset`, `Count`, `Lifetime` | Copies an Attachment from `Assets.Vfx` and bursts every emitter once |
| `Highlight` | `FillColor`, `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `DepthMode`, `Lifetime` | Flashes a Highlight on the target |
| `Template` | `Folder`, `Asset`, `FadeDelay`, `FadeTime`, `Lifetime` | Places a copy of a part or model from `Assets.Models` at the effect's CFrame, then fades it |
| `Shards` | `Count`, `Size = { min, max }`, `Color`, `Material`, `Time`, `Lifetime` | Small parts that fly out and fade. `Data.Color` / `Data.Material` override (used by `BlockBreak`) |
| `JointSwing` | `Joint`, `Keys = { { At, Time, Angles } }` | Swings one joint through rotations (degrees from rest) |
| `ClawSwing` | â | The werewolf combo swipe. `Variant` = combo step, `Speed` = attack speed, `Tool` = claws |
| `SleepSymbols` | `Interval`, `MaxDistance` | Zs rising from the head until stopped |
| `ColorFade` | `Time` | Fades body parts using `Data.Colors = { [partName] = { From, To } }` |
| `SamuraiPose` | `Phase = "Charge" \| "Release"` | IK sword pose. `Tool` = sword. Stop with `{ Instant = true }` to snap back |

### Playing Effects

**Client** â `ReplicatedStorage.Modules.Client.Effects`:

```lua
local Effects = require(ReplicatedStorage.Modules.Client.Effects)

Effects.Play("Hit", { Target = character })
Effects.Play("GolemShatter", { Position = position })

local handle = Effects.Play("Music", { Sound = song, OnFinished = nextSong })
handle:Stop()

Effects.Stop("WerewolfSleep", character)
```

**Server** â `ServerScriptService.Modules.Systems.Effects.EffectService`:

```lua
local EffectService = require(ServerScriptService.Modules.Systems.Effects.EffectService)

EffectService.Play("WerewolfClawSwing", { Target = character, Tool = claws, Variant = combo, Speed = 1.5 })
EffectService.Play("CapsuleSplash", { CFrame = cframe, Variant = "Fire" })
EffectService.Stop("SamuraiCharge", character, { Instant = true })
```

#### Play options

| Option | Type | Description |
|---|---|---|
| `Target` | `Instance?` | The character, model or part the effect is on. It ends if the target leaves the game |
| `Parent` | `Instance?` | Where sounds and particles go, instead of the target's root part |
| `Position` | `Vector3?` | Where it plays, for effects without a target |
| `CFrame` | `CFrame?` | Position and rotation, e.g. a puddle on a slope |
| `Tool` | `Tool?` | The effect ends when this Tool leaves the target |
| `Variant` | `any?` | Picks one of the effect's `Variants` |
| `Speed` | `number?` | Timing multiplier. `2` plays twice as fast |
| `Sound` | `Sound?` | The sound for sound parts with no `Asset` or `Id` |
| `Data` | `table?` | Anything else a part reads |
| `OnMarker` | `(name, track) -> ()` | Animation marker callback. **Client only** |
| `OnFinished` | `() -> ()` | Runs when the effect ends. **Client only** |

> Options sent from the server must be plain values: instances, numbers, strings, booleans, vectors, CFrames, colors and tables of them. Callbacks aren't sent.

### Replication

Who receives a server-sent effect comes from its `Replicate` field:

| Replicate | Sent to | Used for |
|---|---|---|
| `All` | Every client | `Hit`, `SwordUpgrade`, `WerewolfSleep`, `WerewolfTransform`, `WerewolfTransformHowl`, `CapsuleSplash`, `SamuraiCharge`, `SamuraiRelease` |
| `Nearby` | Clients whose character is within `Range` studs | `SwordSwing` (200), `WerewolfClawSwing` (300), `WerewolfHuntHowl` (150), `GolemThrow` (300), `GolemShatter` (300), `BlockPlace` (150), `BlockBreak` (150), `BlockHit` (80), `GeneratorSpawn` (80) |
| `Local` | Not sent â only the client plays it | `SwordSlash`, `ButtonHover`, `ButtonClick`, `Music` |

Why each one:

- **All:** persistent effects and effects with gameplay meaning (players must see a capsule puddle to avoid it).
- **Nearby:** short sounds and motion that can't be seen or heard much further away.
- **Local:** the owner's own animations (they replicate through the Animator), UI sounds and music.

Effects are only sent to clients that have finished loading (the `_ModulesLoaded` player attribute), so players joining mid-game never get packets they can't decode yet.

### Sound Groups

```text
SoundService
âââ Master
    âââ Music        background music
    âââ Abilities    ability sounds: swings, claw swipes, howls, snore
    âââ Effects      hits, impacts and block sounds (also the default group)
    âââ UI           button hover and click
    âââ Ambient      reserved for world ambience
```

- SoundGroups **nest** in Roblox: a sound's volume is multiplied by its group's volume, then by `Master`'s. Changing `Master` scales everything.
- `Client.Effects` puts every sound it plays into the effect's `Group` automatically.
- `Client.Audio.SoundGroups` also puts any sound that appears **without** a group into `Effects`. This covers Roblox's character sounds and sounds placed in the map, so no sound is left out of `Master`.
- Every group starts at volume `1`, so current loudness is unchanged. New SoundGroups default to `0.5`.

### Volume Settings

`Client.Audio.AudioSettings` is ready for a settings menu:

```lua
local AudioSettings = require(ReplicatedStorage.Modules.Client.Audio.AudioSettings)

AudioSettings.Get("Music")              --> 1
AudioSettings.Set("Music", 0.4)         -- heard right away
AudioSettings.Set("Master", 0.8)        -- scales every group
AudioSettings.GetAll()                  --> { Master = 0.8, Music = 0.4, ... }
AudioSettings.Changed:Connect(function(group, volume) end)
```

Volumes go from `0` to `1`. `Set` changes the SoundGroup's `Volume` directly.

Saved values come from `AudioSettings.Store`, which only has `Load()` and `Save(volumes)`. Today it keeps them for the session. To save volumes in player data, change `Store` only â `AudioSettings` and `Client.Effects` need no changes.

### Writing a New Visual Kind

Add a ModuleScript to `Client.Effects.Parts`, named after the kind, with `Play(spec, context)`:

```lua
--!strict
-- Client.Effects.Parts.Ring
local Ring = {}

function Ring.Play(spec: any, context: any)
	local ring = Instance.new("Part")
	ring.Anchored = true
	ring.CanCollide = false
	ring.CFrame = context.CFrame
	ring.Parent = workspace
	context:Add(ring, spec.Lifetime or 1)   -- destroyed after 1s, or when the effect stops
end

return Ring
```

Then use it from the registry: `Visual = { Kind = "Ring", Lifetime = 0.5 }`.

#### Context API

| Member | Description |
|---|---|
| `Target`, `Parent`, `CFrame` | Where the effect is |
| `Speed`, `Variant`, `Data`, `Options` | How it was played |
| `Alive` | `false` once it has ended |
| `:Delay(seconds, fn)` | Run `fn` later unless the effect stopped. Seconds are divided by `Speed` |
| `:Add(instance, lifetime?)` | Destroy the instance after `lifetime`, or when the effect stops |
| `:Keep(seconds)` | Keep the effect running at least this long |
| `:Hold() -> release` | Keep it running until `release()` is called |
| `:OnStop(fn)` | Run `fn(data)` when it ends (e.g. restore joints) |
| `:Anchor()` | An Attachment at `CFrame`, for effects with only a position |
| `:Group()` | The effect's SoundGroup |

A part that errors is warned once; it never breaks the other parts.

---

## Blocks & Building

### The Grid

- Every block fills whole **cells** of `CELL_SIZE` (3) studs.
- Cell `(0, 0, 0)` starts at `GRID_ORIGIN` = `(0, 0, 2)`, which matches the map (its blocks start at Z = 2 on a 3-stud grid).
- A block is identified by the **key of its lowest cell**, a string `"x,y,z"` (`Blocks.Key(cell)` / `Blocks.FromKey(key)`).
- Blocks bigger than one cell set `Size` in cells, e.g. `Vector3.new(2, 1, 1)` for a bed. Placed blocks turn with the player.
- Blocks can only be placed inside a `BUILD_AREAS` box.

```lua
local Blocks = require(ReplicatedStorage.Modules.Shared.Blocks)

local cell = Blocks.CellOf(position)      -- Vector3 cell
local center = Blocks.CenterOf(cell)      -- world position of the cell's center
local key = Blocks.Key(cell)              -- "x,y,z"
```

### Block Definitions

| Field | Type | Required | Description |
|---|---|---|---|
| `DisplayName` | `string` | â | Shown to players |
| `Id` | `number` | â | Unique. Keep it the same once used; never reuse an old one |
| `Hardness` | `number` | â | Seconds to break with the preferred tool at `Speed` 1 |
| `Breakable` | `boolean` | â | `false` for blocks that can be hovered but never broken |
| `Placeable` | `boolean` | â | Whether players can place it. Placeable blocks need a `Model` |
| `Model` | `string` | when placeable | A part or model in `Assets.Models.Blocks` |
| `SoundCategory` | `string` | â | `Variant` for the place/break/hit effects: `Wool`, `Wood`, `Stone`, `Dirt`, `Generic` |
| `BreakEffect` / `PlaceEffect` | `string` | â | Effect names in `Classes.Effects` |
| `PreferredTool` | `string` | â | `Pickaxe`, `Axe` or `Shovel`. `nil` = every breaking tool is full speed |
| `Size` | `Vector3` | â | Cells it fills. Default `1 Ã 1 Ã 1` |
| `HealDelay` | `number` | â | Seconds without a hit before damage resets. Off by default |
| `Interact` | `{ ActionText, HoldDuration? }` | â | Gives the block a prompt that runs its `OnInteract` hooks |
| `Hooks` | `string` | â | Module name in `Systems.Blocks.Hooks` and `Client.Blocks.Hooks` |
| *anything else* | `any` | â | Block data for its hooks, e.g. `Resource` on generators, `Shop` on the shop keeper |

### Tool Types & Breaking

`Shared.ToolTypes` defines every kind of tool once:

| ToolType | Breaks blocks |
|---|---|
| `Pickaxe` | â |
| `Axe` | â |
| `Shovel` | â |
| `Sword` | â |
| `Hand` (no tool, or an item with no `ToolType`) | â |

Break time:

```text
speed = tool.Speed                      if the block has no PreferredTool, or the tool is the PreferredTool
speed = tool.Speed * SLOW_MULTIPLIER    otherwise (0.3)
time  = Hardness / speed
```

- Hold the mouse with a breaking tool to break. The client sends a hit every `HIT_INTERVAL`; the **server clock** decides progress, and one hit adds at most `MAX_HIT_GAP` seconds.
- Breaking reach is `REACH` (8 studs) from the root part to the closest point of the block.
- Blocks are only outlined while you hold a breaking tool.
- Damage is stored in `Shared.BlockState` and drawn as `CRACK_STAGES` crack stages on every client.

### Placing

Placement works like Bedwars, so bridging needs no exact aim (`Client.Blocks.Targeting`):

1. The block you stand on sets your **level**.
2. The aim ray is taken to where it meets that level.
3. The path is walked cell by cell **from under your feet toward that point**, then on in the aim's direction, over blocks that are already there.
4. The **first open cell** on the path gets the block.

So aiming anywhere ahead â even into the void â puts the next block at the end of the bridge, toward the mouse.

In order, the block goes:

1. Against the face the aim hit, unless that face is the top of an edge block on your level (that's bridging) or it doesn't fit.
2. On the bridge path above. Aiming at an edge only bridges, and places nothing when the next cell is out of reach.
3. Against the face the ray hit, if it fits.
4. In the first cell that fits along the ray, from where it passes the player.

Other rules:

- **Pillaring:** look almost straight down at your own block. A block placed in your feet **lifts you onto it**.
- **Reach:** `PLACE_REACH` (8 studs). Out of reach, **no preview** shows.
- **Touching:** a placed block must touch an existing block, so players build out from what exists.
- **Speed:** a click places one block at once. Holding past 0.25s places one every `PLACE_INTERVAL` (0.08s).
- **Prediction:** each placement shows a solid placeholder until the server's block arrives, so building never waits on the server. Placeholders clear after 1.2s if the server refused.
- The server also refuses cells that are filled, tagged `NoBuild`, outside the build area, or where **another** player stands.

### Map Blocks

- Tag a part or model **`Block`** to make it part of the grid.
- Give it a **`BlockType`** attribute to make it a named block (e.g. `Stone`), or leave it out for `MapBlock`, which can be hovered but never broken.
- Tag a part **`NoBuild`** to block placement in its cells.
- Map blocks live in `workspace.World` and `workspace.Generators`. Placed blocks go in `workspace.PlacedBlocks`.
- On start, typed blocks load first. A map block that overlaps one already loaded is skipped, with one warning that counts them.

### Block Hooks

**Server** â `Systems.Blocks.Hooks.<Hook>` (all optional):

| Hook | When it runs |
|---|---|
| `CanPlace(player, definition, origin, size) -> (boolean, reason?)` | Before a placement. Return `false` to refuse |
| `OnPlaced(block, player?)` | After the block is added. `player` is `nil` for map blocks |
| `CanBreak(block, player) -> boolean` | Before each hit. Return `false` to refuse |
| `OnBroken(block, player)` | Before the block is removed |
| `OnInteract(block, player) -> boolean?` | A player used its prompt. Return `false` to skip the client hook |
| `OnPurchase(block, player, index)` | A player bought entry `index` from it |
| `OnTick(block, dt)` | Every `TICK_INTERVAL` |

`block` is a `World.Block`:

| Field | Description |
|---|---|
| `Key` | Key of its lowest cell |
| `Origin` / `Size` | Lowest cell and size in cells |
| `Definition` | Its `Classes.Blocks` definition |
| `Instance` | The part or model in the world |
| `Owner` | The player who placed it, or `nil` |
| `Damage` | Break progress, 0 to 1 |
| `Data` | A table for the hook's own state |

**Client** â `Client.Blocks.Hooks.<Hook>` (all optional):

| Hook | When it runs |
|---|---|
| `OnHover(entry, hovering)` | The player started or stopped aiming at the block |
| `OnInteract(entry)` | The server allowed an interaction with the block's prompt |

`entry` is a `BlockMap.Entry`: `Key`, `Origin`, `Size` and `Definition`.

### Generators, Beds & the Shop

| Block | Hook | Behaviour |
|---|---|---|
| Iron / Diamond / Emerald Generator | `Generator` | Every `Interval` seconds, adds one `Resource` to a **single falling drop** that stacks up to `Limit`, so a full generator is one part, not dozens. Touching the drop picks up the whole stack. Each add plays `GeneratorSpawn` |
| Bed | `Bed` | One bed per player; you can't break your own. Map beds have no owner, so anyone can break them |
| Shop Keeper | `ShopKeeper` | Its prompt opens the shop on the client. The server checks every purchase: the entry exists, the player is in reach, and they can pay |

Shop entries are the shop keeper's `Shop` field:

```lua
Shop = {
	{ Item = "Red Wool", Amount = 16, Currency = "Iron", Price = 4 },
	{ Item = "Iron Sword", Amount = 1, Currency = "Diamond", Price = 4 },
},
```

> **Still to do** (marked `HOOK POINT` in the Bed hook): teams owning beds, respawning only while your team's bed stands, and ending the match when one team is left. The shop still needs categories, team upgrades, a designed UI, item images, and a purchase result sent back to the client.

### Stack Items & Inventory

Items with `Stack = true` (blocks, iron, diamonds, emeralds) are a **count** in `Shared.Inventory`, not a pile of Tools:

- The player holds **one Tool** while the count is above 0.
- `ItemService.Give(player, "Iron", 10)` adds to the count, and makes the Tool only if they have none.
- `ItemService.Take(player, "Iron", 4)` removes from the count, and removes the Tool at 0.
- The Tool comes back on respawn while the count is above 0.
- Placing a block takes one from the count.

### How a Request Flows

**Placing**

1. The client finds the cell (`Targeting`), shows a placeholder, and sends `Blocks.Place(cell, turned)`.
2. The server checks: the held item is a block item the player has, the build area, free and `NoBuild` cells, reach, touching, players in the way, the hook's `CanPlace`, and the rate limit.
3. The server builds the block in `workspace.PlacedBlocks`, takes one item, lifts the placer if the block is in their feet, runs `OnPlaced`, plays `PlaceEffect`, and sends `Blocks.Placed` to every client.

**Breaking**

1. While the mouse is held with a breaking tool, the client sends `Blocks.Hit(cell)` every `HIT_INTERVAL`.
2. The server checks reach, `Breakable`, `CanBreakBlocks`, the hook's `CanBreak`, and the rate limit, then adds damage to `Shared.BlockState`.
3. At full damage it runs `OnBroken`, removes the block, plays `BreakEffect`, and sends `Blocks.Removed` to every client.

**Joining**

The client sends `Blocks.Sync` once it is listening, and the server answers with a `Blocks.Snapshot` of every block. Block packets only go to clients that have synced.

### Grid Settings

All in `Shared.Blocks.Config`:

| Setting | Value | Description |
|---|---|---|
| `CELL_SIZE` | `3` | Studs per cell side |
| `GRID_ORIGIN` | `(0, 0, 2)` | Where cell `(0, 0, 0)` starts |
| `BUILD_AREAS` | one box | `{ Min, Max }` boxes in studs that blocks must fit inside |
| `REACH` | `8` | Studs to break or use a block |
| `PLACE_REACH` | `8` | Studs to place a block |
| `PLACE_INTERVAL` | `0.08` | Seconds between placements while held |
| `SLOW_MULTIPLIER` | `0.3` | Speed multiplier for the wrong tool |
| `HIT_INTERVAL` | `0.2` | Seconds between break hits while held |
| `MAX_HIT_GAP` | `0.35` | Most break time one hit can add |
| `PLACE_RATE` / `HIT_RATE` | `20` / `12` | Requests per second before the server ignores them |
| `CRACK_STAGES` | `5` | Crack overlay stages |
| `TICK_INTERVAL` | `0.25` | Seconds between `OnTick` calls |
| `BLOCK_TAG` / `NO_BUILD_TAG` | `"Block"` / `"NoBuild"` | CollectionService tags |
| `TYPE_ATTRIBUTE` / `MAP_BLOCK` | `"BlockType"` / `"MapBlock"` | Map block type attribute and default |

---

## Admin Commands

Press **F2** in game to open the [Cmdr](https://eryn.io/Cmdr/) command bar. Only the user ids in `Services.CmdrSetup.Hooks.BeforeRun` can run commands.

| Command | Alias | Arguments | Description |
|---|---|---|---|
| `give` | `giveitem` | `<players> <item> [amount]` | Give any item in `Classes.Items`. Stack items add `amount`; other items give one Tool each |
| `givekit` | `kit` | `<players> <kit> [replace]` | Add a kit to the player's kits. `replace = true` removes their other kits first |
| `giveability` | `ability` | `<players> <ability>` | Give an ability without a kit. Only [grantable](#granted-abilities) abilities are listed |
| `GiveCurrency` | `giveCurrency` | `<players> <currency> <amount>` | Add to a leaderstats currency |

Examples:

```text
give me "Blue Wool" 64
give me "Wooden Pickaxe"
give all Iron 50
givekit me Golem
givekit me Werewolf true
giveability me ChickenRush
```

- Item and kit names autocomplete. **Names with spaces need quotes.**
- The `item`, `kit` and `ability` types read `Classes.Items`, `Classes.Kits` and `KitState.Grantable()`, so new content shows up with no command changes.

**Adding a command:** put a definition module (`Name`, `Aliases`, `Description`, `Group`, `Args`) and a `<Name>Server` module returning `function(context, ...)` in `CmdrSetup.Commands`. New argument types go in `CmdrSetup.Types` as `function(registry)`. Types are registered before commands.

---

## HUD

| Panel | Element | Shows | Driven by |
|---|---|---|---|
| **Kit panel** | `Main.KitPanel` | Each active kit's name and `Info` rows | Kit definitions + kit state |
| **Ability bar** | `Main.AbilityBar` | One round button per usable ability, with key label, cooldown and disabled state | `Core.Abilities` usable list + specs |
| **Item panel** | `Main.ItemPanel` | The held item's name and `Info` rows. Hidden if it has none | Item definition |
| **Custom UI** | any `Main.<Element>` | Whatever your function draws | `CustomUI` tables |

Building has no popups: no "can't break" or progress messages. The hover outline, preview, placeholders and cracks are drawn by `Client.Blocks.BlockVisuals`.

### Info rows

Used by kit and item `Info` tables:

| Field | Type | Description |
|---|---|---|
| `Label` | `string` | Row label |
| `Text` | `(value) -> string` | Right-hand text |
| `Bar` | `(value) -> number` | Fill from 0 to 1 (shows a bar under the row) |
| `Icon` | `(value) -> string` | Image next to the label |
| `Visible` | `(value) -> boolean` | Hide the row when `false` |
| `Color` | `Color3` | Bar fill color |

`value` is the kit's state snapshot (kit panel) or an item `Context` (item panel).

### Contexts

**Item context** (`Shared.Items.Context`):

| Field | Description |
|---|---|
| `Tool` | The held Tool |
| `Player` | The local player |
| `Count` | How many of this item the player carries |
| `State(kitName)` | A kit state snapshot, or `nil` |

**Ability context** (`Core.Abilities.Context`):

| Field | Description |
|---|---|
| `Name` | Ability name |
| `Tool` | The held Tool, or `nil` |
| `Player` | The local player |
| `Enabled` | Result of the spec's `Enabled` |
| `Remaining` / `Total` | Cooldown seconds left / full length |
| `State(kitName)` | A kit state snapshot, or `nil` |

---

## Input

| Slot | Keyboard | Gamepad |
|---|---|---|
| `Ability1` | `Q` | `X` |
| `Ability2` | `E` | `Y` |
| `Ability3` | `R` | `B` |
| `Ability4` | `F` | `LB` |
| `Ability5` | `G` | `RB` |
| Item click action | `LMB` | `RT` |
| Break (breaking tool held) | hold `LMB` | â |
| Place (block item held) | click or hold `LMB` | â |
| Command bar | `F2` | â |

- Kit abilities take slots first, in the order kits and their `Abilities` are listed; then granted abilities; then the held item's other abilities.
- The held item's **first** ability is its click action and has no slot.
- Touch players tap the ability bar.
- Passive abilities never appear on the bar.
- Block input is read only in `Client.Blocks.BlockInput`. Touch and controller building go there later.

---

## API Reference

### Server

#### `KitService` â `Systems.Kits.KitService`

| Method | Description |
|---|---|
| `:SetKits(player, { kitName })` | Replace the player's active kits |
| `:SetKit(player, kitName?)` | Set one kit, or `nil` for none |
| `:GetKits(player) -> { string }` | Active kits, in order |
| `:HasKit(player, kitName) -> boolean` | Is the kit active |
| `:HasAbility(player, abilityName) -> boolean` | Does any active kit, or a grant, give it |
| `:GrantAbility(player, abilityName) -> boolean` | Give a [grantable](#granted-abilities) ability without a kit. `false` if refused |
| `:RevokeAbility(player, abilityName)` | Take back a granted ability. Kit abilities stay |
| `:GiveItem(player, kitName, itemName) -> Tool?` | Give an item on behalf of a kit (removed with the kit) |
| `:GrantItems(player, kitName)` | Give the kit's missing items |
| `:ApplyStats(player)` | Apply the highest `MaxHealth` / `WalkSpeed` of the active kits |

#### `ItemService` â `Systems.Items.ItemService`

| Method | Description |
|---|---|
| `.Give(player, itemName, amount?) -> Tool?` | Build the Tool, put it in the Backpack, run `OnGiven`. Stack items add `amount` (default 1) |
| `.Take(player, itemName, amount?) -> boolean` | Take from a stack item. Nothing is taken if they carry fewer |

#### `AbilityService` â `Systems.Abilities.AbilityService`

| Method | Description |
|---|---|
| `:Use(player, abilityName, aim)` | Validate and run an ability |
| `:GetCooldown(player, abilityName) -> number` | Seconds left |
| `:SetCooldown(player, abilityName, seconds)` | Start or replace a cooldown (replicates to the client) |

#### `EffectService` â `Systems.Effects.EffectService`

| Function | Description |
|---|---|
| `.Play(name, options?)` | Send an effect to the clients its `Replicate` names. `Local` effects warn and are not sent |
| `.Stop(name, target?, data?)` | Stop an effect on every client, e.g. a persistent one. `data` is passed to the parts' stop functions |

#### `BlockService` â `Systems.Blocks.BlockService`

| Function | Description |
|---|---|
| `.Place(player, origin, turned)` | Validate and place the held block with its lowest cell at `origin` |
| `.Remove(block, player?)` | Remove a block, running `OnBroken` and sending `Removed` |
| `.Hit(player, cell)` | One break hit on the block filling `cell` |
| `.Get(key) -> Block?` | The block whose lowest cell has this key |
| `.All() -> { Block }` | Every block |

`BlockService.Rules`:

| Function | Description |
|---|---|
| `.CanPlace(player, definition, origin, size) -> (boolean, lift?)` | Every placement check. `lift` is how far to raise the placer |
| `.InReach(player, origin, size, reach?) -> boolean` | Is the block within reach |
| `.OverlapsPlayer(origin, size, except?) -> boolean` | Is any other player in those cells |

#### `Claws` â `Systems.Werewolf.Claws`

| Function | Description |
|---|---|
| `.Setup(player, tool)` | Wire up a claws Tool (called by the `WerewolfClaws` item hook) |
| `.Remove(player)` | Take the claws away (called when the Werewolf kit is removed) |
| `.Attack(player) -> number \| false` | One swipe (the Claw ability) |
| `.ToggleRest(player) -> boolean` | Lie down or get up (the Rest ability) |
| `.Hunt(player) -> number \| false` | Start a hunt (the Hunt ability) |

Each claws Tool gets a session (`Claws.Session`), and each child module adds its part:

| Module | Job |
|---|---|
| `Config` | Tuning constants and `MoonStats(charge)` |
| `Session` | Shared state for one Tool, `:IsActive()`, `:MoonActive()`, `:Charge()`, `:OnDispose(fn)` |
| `Rest` | Lying down, waking on damage, sleep effect |
| `Moon` | Moon speed, growth, the full-moon transform, passive charge |
| `Hunt` | The full-moon hunt and its cooldown |
| `Attack` | The three-swipe combo and damage |
| `Lunge` | The double swipe's forward dash |
| `Hit` | Strike-frame hit detection, lifesteal, charge on hit |
| `Effects` | Every claw effect request, through `EffectService` |

### Shared

#### `KitState` â `Shared.KitState`

| Function | Side | Description |
|---|---|---|
| `.Of(player, kitName)` | both | State accessor for a kit (read-only on the client) |
| `.Get(player, kitName)` | both | State snapshot table |
| `.GetKits(player)` | both | Active kit names |
| `.HasKit(player, kitName)` | both | Is the kit active |
| `.HasAbility(player, abilityName)` | both | Does any active kit, or a grant, give it |
| `.GetGranted(player)` | both | Abilities given without a kit |
| `.Grantable()` | both | Abilities that can be given without a kit, sorted |
| `.ObserveKits(player, fn) -> disconnect` | both | Call `fn(kits)` now and on every change (yields for data) |
| `.ObserveGranted(player, fn) -> disconnect` | both | Call `fn(abilities)` now and on every change (yields for data) |
| `.Definition(kitName)` | both | The kit's definition table |
| `.WaitForData(player) -> boolean` | both | Wait for the player's data |
| `.SetKits(player, kits)` | server | Low-level write. Use `KitService:SetKits` instead |
| `.SetGranted(player, abilities)` | server | Low-level write. Use `KitService:GrantAbility` instead |

> On the client, `player` must be the `LocalPlayer` â each client only receives its own state.

#### `Items` â `Shared.Items`

| Function | Description |
|---|---|
| `.Get(itemName)` | Definition, or `nil` |
| `.Of(tool)` | Definition for a Tool, or `nil` |
| `.Grants(tool, abilityName)` | Does the Tool's item grant the ability |
| `.Create(itemName)` | New Tool from the model (caller parents it) |
| `.Count(player, itemName)` | How many the player carries (stack items read `Inventory`) |
| `.WireAbilities(player, use)` | Client: clicking an item Tool calls `use(abilityName, tool)` |

#### `Blocks` â `Shared.Blocks`

| Function | Description |
|---|---|
| `.Get(name)` / `.ById(id)` / `.All()` | Definitions |
| `.Of(tool)` | The block a held block item places, or `nil` |
| `.ToolOf(tool)` | How a held item breaks blocks. `nil` = empty hand |
| `.BreakTime(definition, tool)` | Seconds to break, or `nil` if the tool can't |
| `.CellOf(position)` / `.CenterOf(cell)` | World â cell |
| `.Key(cell)` / `.FromKey(key)` | Cell â `"x,y,z"` |
| `.SizeOf(definition, turned?)` | Size in cells, turned a quarter turn if `true` |
| `.Cells(origin, size)` | Every cell a block fills |
| `.Bounds(origin, size)` | World min and max corners |
| `.FootprintOf(instance)` | Origin and size of a map part or model |
| `.DistanceTo(position, origin, size)` | Studs from a point to the closest point of a block |
| `.LiftOnto(character, origin, size)` | How far a character must rise to stand on a block |
| `.Touches(origin, size, filled)` | Does a block touch a filled cell |
| `.InBuildArea(origin, size)` | Does it fit in a `BUILD_AREAS` box |

#### `ToolTypes` â `Shared.ToolTypes`

| Member | Description |
|---|---|
| `.KINDS` | Every tool kind and whether it breaks blocks |
| `.HAND` | The empty-hand tool |
| `.Of(definition, itemName?)` | An item's tool (`ToolType`, `Speed`, `CanBreakBlocks`). Errors on bad fields |

#### `BlockState` â `Shared.BlockState`

| Function | Side | Description |
|---|---|---|
| `.Damage(key) -> number` | both | Break progress, 0 to 1 |
| `.SetDamage(key, damage)` | server | Set it. `0` clears it |
| `.Observe(fn)` | both | `fn({ [key]: damage })` now and on every change |

#### `Inventory` â `Shared.Inventory`

| Function | Side | Description |
|---|---|---|
| `.Count(player, itemName)` | both | How many of a stack item |
| `.Add(player, itemName, amount)` | server | Change the count. Use `ItemService.Give` / `Take` instead |
| `.Observe(player, itemName, fn)` | both | `fn(count)` now and on every change |

#### `ReadOnly` â `Shared.ReadOnly`

| Function | Description |
|---|---|
| `.Wrap(node, label)` | A read-only view of a Scribe accessor. Any write errors with `label` |

### Client

#### `Abilities` â `Client.Core.Abilities`

| Member | Description |
|---|---|
| `:Register(name, spec)` | Give an ability its client behaviour and look |
| `:GetSpec(name)` / `:GetSpecs()` | Registered spec(s) |
| `:GetUsable() -> { Usable }` | Abilities usable right now (kits, then grants, then the held item) |
| `:GetSlot(slot) -> Usable?` | The ability on a slot key |
| `:Press(name)` / `:Release(name)` | Use an ability |
| `:IsEnabled(name)` | Usable and enabled |
| `:GetCooldown(name) -> (remaining, total)` | Cooldown for the bar |
| `:Request(name, aim?)` | Ask the server directly |
| `:GetAim() -> Vector3` | Mouse hit point, or a point in front of the character |
| `.Changed` | Signal: the usable list changed |

#### `Inputs` â `Client.Core.Inputs`

| Member | Description |
|---|---|
| `:GetKeyLabel(slot?) -> string` | Key text for a slot on the current device (`nil` = click action) |

#### `Effects` â `Client.Effects`

| Function | Description |
|---|---|
| `.Play(name, options?) -> Handle?` | Play an effect on this client. `nil` if the name isn't in the registry |
| `.Stop(name, target?, data?)` | Stop every running copy of an effect on a target |
| `handle:Stop(data?)` | Stop one play |

#### `AudioSettings` â `Client.Audio.AudioSettings`

| Member | Description |
|---|---|
| `.Get(group) -> number` | A group's volume, 0 to 1. `"Master"` is a group name too |
| `.Set(group, volume)` | Set and save a group's volume. Heard right away |
| `.GetAll() -> { [string]: number }` | Every group's volume, including Master |
| `.Changed` | Signal: `(group, volume)` |

#### `SoundGroups` â `Client.Audio.SoundGroups`

| Member | Description |
|---|---|
| `.Get(name?) -> SoundGroup` | A group by name. Unknown names warn once and return `Effects` |
| `.Assign(sound, name?)` | Put a sound in a group |
| `.Master() -> SoundGroup` | The Master group (created with its children if missing) |
| `.NAMES` / `.DEFAULT` | The child group names / the default group |

#### Blocks â `Client.Blocks`

| Module | Job |
|---|---|
| `BlockMap` | The client's occupancy map, from `Snapshot`, `Placed` and `Removed`. `InstanceOf(entry)` finds a streamed-in block |
| `BlockInput` | Turns the mouse into break and place actions |
| `Targeting` | The hovered block and the predictive placement cell |
| `BlockVisuals` | Hover outline, placement preview, placeholders and cracks |
| `BlockController` | Runs every frame: targeting, preview, sending requests, client hooks |

---

## Packets

All packets live in `Shared.Packets`.

| Packet | Direction | Payload | Purpose |
|---|---|---|---|
| `Effects.Play` | S â clients | `name, options` | Play an effect (All or Nearby clients) |
| `Effects.Stop` | S â all | `name, { Target, Data }` | Stop an effect |
| `Abilities.Use` | C â S | `name, x, y, z` | Use any kit or item ability |
| `Items.Equip` | C â S | `tool` | Equip a Backpack Tool on the server |
| `Items.Unequip` | C â S | â | Put away the held Tool |
| `Blocks.Sync` | C â S | â | Ask for the snapshot, once listening |
| `Blocks.Snapshot` | S â C | `{ { Key, Id, Size } }` | Every block |
| `Blocks.Placed` | S â synced | `{ Key, Id, Size }` | A block was placed |
| `Blocks.Removed` | S â synced | `key` | A block was removed |
| `Blocks.Place` | C â S | `cell, turned` | Place the held block |
| `Blocks.Hit` | C â S | `cell` | One break hit |
| `Blocks.Interacted` | S â C | `key` | Run the block's client `OnInteract` |
| `Blocks.Purchase` | C â S | `key, index` | Buy a shop entry |
| `Combat.Hit` | S â all | `character, damage` | Hit feedback (damage popups, health bars) |
| `Werewolf.Rest` | C â S | `boolean` | Set resting directly (wake on move) |
| `Werewolf.HuntTargets` | S â C | `tool, { targets }, expires` | Highlight hunt targets |
| `Golem.ConsumeStone` | C â S | `stone` | Eat an ancient stone |
| `Samurai.Charge` | C â S | `boolean` | Begin (`true`) or cancel (`false`) a dash charge |
| `Cauldron.BrewingState` | C â S | `cauldron, holding` | Brew prompt held |

Cmdr uses its own `CmdrFunction` / `CmdrEvent` remotes.

> Always require `Shared.Packets` â never call `Packet("Name", ...)` from the command bar. A second copy of the packet library can't decode the real one's traffic.

---

## Built-in Content

### Kits

| Kit | Items | Abilities | State | HUD |
|---|---|---|---|---|
| Animal Whisperer | â | ChickenRush | â | â |
| Barbarian | Wooden Sword | Rage *(passive)* | `Rage`, `SwordLevel` | Custom UI: `Rage` |
| Golem | â | RockThrow | `Rocks`, `Scale` | Info: Rocks, Size |
| Samurai | Wooden Sword | Dash | `Charging`, `ChargeStartedAt` | Dash's custom UI: `DashCharge` |
| Scientist | â | Brew *(passive)* | â | â |
| Stew Boy | â | SummonCauldron, Brew *(passive)* | â | â |
| Werewolf | Werewolf Claws | Rest, Hunt | `MoonCharge`, `Resting`, `RestStartedAt`, `HuntingUntil`, `Transformed`, `Transforming`, `Combo` | Info: Moon, Bonus, Lifesteal, Charge, Hunting |

### Items

| Item | Abilities | Notes |
|---|---|---|
| Wooden / Stone / Iron / Diamond Sword, Rageblade | Slash | `Damage`, `Cooldown`; `ToolType = "Sword"`, can't break blocks; Rage upgrades through these |
| Wooden Pickaxe / Axe / Shovel | â | `ToolType`, `Speed = 1`, `CanBreakBlocks = true` |
| Red / Blue / Purple / Green Wool, Wood, Planks, Stone, Dirt, Concrete, Black Stone | â | Block items: `Block`, `Stack` |
| Bed, Shop Keeper | â | Block items for the special blocks |
| Iron, Diamond, Emerald | â | Resources: `Stack`. Dropped by generators, spent at the shop |
| Fire / Poison / Speed / Shock Capsule | Throw | `Capsule` effect; Info: Carried; brewable |
| Meat, Ham | Consume | `HealAmount`; brewable |
| Eye | Consume | `RevealDuration`; brewable |
| Werewolf Claws | Claw | Hook: `WerewolfClaws`; Info: Combo |

### Abilities

| Ability | Granted by | Type | Cooldown | Grantable |
|---|---|---|---|---|
| Rage | Barbarian | Passive | â | â |
| Brew | Scientist, Stew Boy | Passive (unlocks the cauldron) | â | â |
| RockThrow | Golem | Hold to aim, release to throw | 5s after a throw | â |
| ChickenRush | Animal Whisperer | Tap: a chicken stampede, 35 damage per target | 8s | â |
| Rest | Werewolf | Tap | 0.5s | â |
| Hunt | Werewolf | Tap (full moon only) | Hunt duration + 45s | â |
| Dash | Samurai | Hold to charge (or RMB), release to dash | 0.4s | â |
| SummonCauldron | Stew Boy | Tap | 1s | â |
| Slash | Swords | Click | Sword `Cooldown` | â |
| Throw | Capsules | Click | 0.3s | â |
| Claw | Werewolf Claws | Click | 0.55s (faster while hunting) | â |
| Consume | Meat, Ham, Eye | Click | 0.3s | â |

### Blocks

| Id | Block | Hardness | Preferred tool | Breakable | Placeable | Size | Hook |
|---|---|---|---|---|---|---|---|
| 1 | MapBlock | â | â | â | â | 1Ã1Ã1 | â |
| 2â5 | Red / Blue / Purple / Green Wool | 0.8 | any | â | â | 1Ã1Ã1 | â |
| 6 | Wood | 2 | Axe | â | â | 1Ã1Ã1 | â |
| 7 | Planks | 1.5 | Axe | â | â | 1Ã1Ã1 | â |
| 8 | Stone | 3 | Pickaxe | â | â | 1Ã1Ã1 | â |
| 9 | Dirt | 1 | Shovel | â | â | 1Ã1Ã1 | â |
| 10 | Grass | 1.2 | Shovel | â | â | 1Ã1Ã1 | â |
| 11 | Soil | 1 | Shovel | â | â | 1Ã1Ã1 | â |
| 12 | Concrete | 4 | Pickaxe | â | â | 1Ã1Ã1 | â |
| 13 | Black Stone | 6 | Pickaxe | â | â | 1Ã1Ã1 | â |
| 20 | Bed | 2 | any | â | â | 2Ã1Ã1 | Bed |
| 21 | Shop Keeper | â | â | â | â | 2Ã2Ã1 | ShopKeeper |
| 22 | Iron Generator | â | â | â | â | 1Ã2Ã1 | Generator: Iron every 1.5s, up to 100 |
| 23 | Diamond Generator | â | â | â | â | 1Ã2Ã1 | Generator: Diamond every 30s, up to 10 |
| 24 | Emerald Generator | â | â | â | â | 1Ã2Ã1 | Generator: Emerald every 60s, up to 4 |

### Effects

| Effect | Group | Replicate | Parts | Played by |
|---|---|---|---|---|
| `Hit` | Effects | All | Sound, Highlight, Particles | `Combat.ApplyHit` |
| `SwordSwing` | Abilities | Nearby 200 | Sound, Particles | `SwordCombat:Attack` |
| `SwordUpgrade` | Abilities | All | Sound | `Rage.Gain` |
| `SwordSlash` | â | Local | Animation (2 Variants) | `Client.Abilities.Library.Slash` |
| `WerewolfClawSwing` | Abilities | Nearby 300 | ClawSwing, Sound (3 Variants) | `Claws.Attack` |
| `WerewolfSleep` | Abilities | All, persistent | Sound, SleepSymbols | `Claws` rest |
| `WerewolfTransform` | â | All | ColorFade | `Claws` transform |
| `WerewolfTransformHowl` | Abilities | All | Sound (global) | `Claws` transform |
| `WerewolfHuntHowl` | Abilities | Nearby 150 | Sound | `Claws.Hunt` |
| `GolemThrow` | â | Nearby 300 | JointSwing | `Rocks.Throw` |
| `GolemShatter` | â | Nearby 300 | Shards | `Rocks.Throw` impact |
| `CapsuleSplash` | â | All | Template (4 Variants) | `Capsules:Throw` landing |
| `SamuraiCharge` | â | All, persistent | SamuraiPose | `SwordPose.Begin` |
| `SamuraiRelease` | â | All | SamuraiPose | `SwordPose.Release` |
| `BlockPlace` | Effects | Nearby 150 | Sound (Variant per `SoundCategory`) | `BlockService.Place` |
| `BlockBreak` | Effects | Nearby 150 | Shards, Sound (Variant per `SoundCategory`) | `BlockService.Remove` |
| `BlockHit` | Effects | Nearby 80 | Sound (Variant per `SoundCategory`) | `BlockService.Hit` |
| `GeneratorSpawn` | Effects | Nearby 80 | Sound | Generator hook |
| `ButtonHover` / `ButtonClick` | UI | Local | Sound | `Packages.UI.ButtonHover` |
| `Music` | Music | Local | Sound | `Client.Core.Music` |

---

## Notes & Gotchas

- **Equips go through the server.** Client-side `Humanoid:EquipTool` (used by custom hotbars like NeoHotbar) doesn't replicate in this place, so `Client.Core.ToolSync` sends `Items.Equip` / `Items.Unequip` and the server equips for real. Without it, the server sees empty hands and refuses item abilities.
- **Item abilities need the item held on the server.** If an item ability "does nothing", check that the server's character has the Tool, not just the client's.
- **Kit state, inventory and granted abilities are session data.** They reset when the player leaves. Persisted data belongs elsewhere in the Scribe template.
- **Block damage is server data.** It lives in Scribe's `ServerStore` (one per server, never saved, replicated to everyone). The Scribe package was **patched** to accept the `ServerStore` option â re-apply the patch if you update Scribe.
- **Client Scribe views are wrapped by `Shared.ReadOnly`.** Scribe lets a client write its own mirror; the wrapper makes those writes error instead of silently diverging.
- **ModuleLoader calls `Init` and `Start` on every module** whose ancestors are all Folders. Helper modules that shouldn't start on their own use another name (e.g. `BlockVisuals.Build`). Use the `ClientOnly`, `ServerOnly` and `IgnoreLoader` attributes to control loading.
- **Packets wait for loaded clients.** Effects go only to players with `_ModulesLoaded`, and block packets only to clients that sent `Blocks.Sync`. Sending earlier causes decode errors at join.
- **Map blocks can stream out.** `StreamingEnabled` is on, so the client's `BlockMap` never depends on instances. Use `BlockMap.InstanceOf(entry)` when you need the part.
- **Overlapping map blocks are skipped.** On start the server warns with a count of map blocks that overlap another. Light-source parts are untagged so they don't hide generators.
- **Knockback vs. reach.** Sword hits knock targets ~2 studs back; the sword reaches 7 studs, so keep moving forward in a fight.
- **Custom UI starts hidden.** Elements named in any `CustomUI` table are hidden when the HUD starts, then shown only while in use.
- **Multiple kits.** Stats take the highest value; appearances apply in list order; abilities fill slot keys in order.
- **Gameplay stays on the server.** Body-scale growth (Werewolf moon, Golem rocks, the hunt), the werewolf lunge, knockback, the thrown capsule and boulder, and generator drops are gameplay, so the server runs them. Only cosmetic effects run on clients.
- **Capsule puddles have no server part.** The server keeps a `{ Position, Radius, Expires }` table for damage and speed; clients draw the puddle with `CapsuleSplash`. The puddle timings (5s fade delay, 2s fade, 7s lifetime) are in both `Capsules` and the registry â change both together.
- **Late joiners miss running effects.** A player who joins while a persistent effect is running (a sleeping werewolf, a charging Samurai) won't see it until it plays again.
- **Claws are shown by the client.** The server keeps claw parts hidden; `ClawSwing` shows them locally during a swipe, using each part's `VisibleTransparency` attribute (set by the server for the hunt look).
- **The old handlers are gone.** `SoundHandler` and `VisualEffectsHandler` were removed. `AnimationHandler` is unchanged and is used by the Animation part.
- **Not yet tested with several players.** Building is verified in single-player play tests; multi-client bridging and fights over blocks still need a test.
