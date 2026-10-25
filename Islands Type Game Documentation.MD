# Kits, Abilities & Items

A data-driven framework for kits, abilities and items in a Roblox game. Kits and items are plain definition modules; abilities are small server modules with optional client specs; all player kit state lives in a shared [Scribe](https://scribe.ericplane.dev/) store that the server writes and the client reads. The HUD builds itself from those definitions, so adding content never requires editing HUD code.

---

## Table of Contents

- [Overview](#overview)
- [Project Layout](#project-layout)
- [Core Concepts](#core-concepts)
  - [Kits](#kits)
  - [Items](#items)
  - [Abilities](#abilities)
  - [Kit State](#kit-state)
- [Guides](#guides)
  - [Adding a Kit](#adding-a-kit)
  - [Adding an Item](#adding-an-item)
  - [Adding an Ability](#adding-an-ability)
  - [Custom UI](#custom-ui)
  - [Setting a Player's Kits](#setting-a-players-kits)
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
| **Item** | A Tool with a definition: abilities, held-item HUD info, server hooks | `Classes.Items.<Item>` |
| **Ability** | Server behaviour plus an optional client spec | `Systems.Abilities.Library.<Ability>` + `Client.Abilities.Library.<Ability>` |
| **Kit state** | Per-player, per-kit data replicated to the owning client | `Shared.KitState` (built on Scribe) |

Key rules:

- **Kit abilities** are granted by a player's active kits.
- **Item abilities** are granted by the **held** item, and work with **no kit equipped**.
- A player can have **several kits at once**.
- The server is the only writer of kit state. The client's view is **read-only** and errors on writes.

---

## Project Layout

```text
ReplicatedStorage
├── Assets
│   └── Models
│       ├── Items/<Item>              Tool models, named after the item definition
│       └── GolemBoulder
├── Inputs
│   └── Default                       InputContext: Ability1–Ability5 slot keys
└── Modules
    ├── Classes
    │   ├── Kits/<Kit>                Kit definitions
    │   ├── Items/<Item>              Item definitions
    │   └── SwordLevels               Barbarian rage levels
    ├── Shared
    │   ├── Data                      Scribe template (Kits + Abilities session roots)
    │   ├── KitState                  Active kits and kit state
    │   ├── Items                     Item helper (definitions + item ability wiring)
    │   └── Packets                   Every network packet
    └── Client
        ├── Core
        │   ├── Abilities             Client ability framework
        │   ├── Inputs                Slot keys and key labels
        │   └── ToolSync              Server-side equip sync
        ├── Abilities/Library/<Ability>   Client ability specs
        ├── Hud
        │   ├── KitPanel              Kit information panel
        │   ├── AbilityBar            Ability buttons
        │   ├── ItemPanel             Held item information panel
        │   ├── InfoRows              Shared row renderer
        │   └── CustomUI              Hand-made UI support
        ├── Kits/<Kit>                Kit-only client code (visuals, overlays)
        └── Items/<Item>              Item-only client code (aim arcs, effects)

ServerScriptService
└── Modules
    └── Systems
        ├── Kits
        │   ├── KitService            Sets kits, stats, items, hooks
        │   ├── Appearance            Applies kit rig looks
        │   └── Hooks/<Kit>           Per-kit server hooks
        ├── Items
        │   ├── ItemService           Gives items, runs item hooks, server-side equips
        │   └── Hooks/<Hook>          Per-item server hooks
        └── Abilities
            ├── AbilityService        Validates and runs ability requests
            └── Library/<Ability>     Server ability modules

StarterGui
└── Main
    ├── KitPanel                      Kit info panel  (restyle via its Templates folder)
    ├── AbilityBar                    Ability bar     (restyle via its Templates folder)
    ├── ItemPanel                     Item info panel (restyle via its Templates folder)
    ├── Rage                          Custom UI for the Barbarian
    └── DashCharge                    Custom UI for the Dash ability

ServerStorage
├── README                            In-Studio copy of these docs (disabled Script)
└── UIBackup                          Backups of the original UI
```

---

## Core Concepts

### Kits

A kit is a ModuleScript in `ReplicatedStorage.Modules.Classes.Kits` that returns a table:

| Field | Type | Required | Description |
|---|---|---|---|
| `DisplayName` | `string` | ✅ | Shown to players |
| `Description` | `string` | ✅ | Shown to players |
| `MaxHealth` | `number` | ✅ | Applied on kit set and every spawn. With several kits, the highest wins |
| `WalkSpeed` | `number` | ✅ | Same as `MaxHealth` |
| `Items` | `{ string }` | ✅ | Item names given on kit set and every spawn |
| `Abilities` | `{ string }` | ✅ | Abilities this kit grants |
| `State` | `{ [string]: Scribe field }` | ❌ | Kit state, declared with Scribe |
| `Info` | `{ InfoRow }` | ❌ | Rows for the kit panel |
| `CustomUI` | `{ [string]: (gui, state) -> boolean? }` | ❌ | Hand-made UI in `StarterGui.Main` |

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
| `DisplayName` | `string` | ✅ | Shown to players |
| `Image` | `string` | ❌ | Icon for the HUD |
| `Abilities` | `{ string }` | ✅ | Abilities granted while held. **The first one is the click action** |
| `Info` | `{ InfoRow }` | ❌ | Rows for the item panel. No rows = panel hidden |
| `CustomUI` | `{ [string]: (gui, context) -> boolean? }` | ❌ | Hand-made UI shown while held |
| `Hooks` | `string` | ❌ | Name of a module in `Systems.Items.Hooks` |
| *anything else* | `any` | ❌ | Item data, e.g. `Damage`, `Cooldown`, `Capsule`, `HealAmount` |

Item hooks (`Systems.Items.Hooks.<Hook>`, all optional):

| Hook | When it runs |
|---|---|
| `OnGiven(player, tool)` | Every time the item is given |
| `Start()` | Once, by ModuleLoader |

### Abilities

An ability has two halves:

**Server** — `Systems.Abilities.Library.<Ability>`:

| Field | Type | Description |
|---|---|---|
| `Name` | `string` | Matches the name in a kit's or item's `Abilities` |
| `Cooldown` | `number?` | Seconds between uses, per player |
| `Activate` | `(player, aim, tool?) -> (false \| number \| any)` | Runs the ability. `tool` is set when the held item grants it |
| `Passive` | `boolean?` | `true` for abilities with no `Activate` (e.g. Rage) |

`Activate` return values:

| Return | Effect |
|---|---|
| `false` | Nothing happened — no cooldown starts |
| a `number` | Use this as the cooldown instead of `Cooldown` |
| anything else | Success — `Cooldown` applies |

A request runs only if the ability exists, the **held item or an active kit** grants it, and its cooldown has passed. Cooldowns replicate to the client automatically.

**Client** (optional) — `Client.Abilities.Library.<Ability>` calls `Abilities:Register(name, spec)` in `Init`. Every field is optional:

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

> ⚠️ Don't name a state field after a Scribe accessor method (`Active`, `Get`, `Set`, `Count`, `Remove`, …). The method shadows the field.

---

## Guides

### Adding a Kit

1. **Create the definition** — `Classes.Kits.Ninja`:

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

2. **Add server hooks** *(optional)* — `Systems.Kits.Hooks.Ninja`:

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

3. **Add each new ability** — see [Adding an Ability](#adding-an-ability).
4. **Add kit-only client code** *(optional)* — `Client.Kits.Ninja/...`

No HUD changes are needed: the kit panel reads `Info`, and the ability bar reads `Abilities`.

### Adding an Item

1. **Add the Tool** to `ReplicatedStorage.Assets.Models.Items`, named after the item.
2. **Create the definition** — `Classes.Items.Smoke Bomb`:

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

3. **Add a server hook** *(optional)* — `Systems.Items.Hooks.<Name>` with `OnGiven(player, tool)`, and set `Hooks = "<Name>"` in the definition.
4. **Give it** with `ItemService.Give(player, "Smoke Bomb")`, or list it in a kit's `Items`.

### Adding an Ability

1. **Server** — `Systems.Abilities.Library.Vanish`:

   ```lua
   --!strict
   return {
   	Name = "Vanish",
   	Cooldown = 8,
   	Activate = function(player: Player, aim: Vector3, tool: Tool?)
   		-- return false if nothing happened, or a number to set the cooldown
   	end,
   }
   ```

2. **Client** *(optional)* — `Client.Abilities.Library.Vanish`:

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

3. **Grant it** by listing it in a kit's or item's `Abilities`.

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

The function runs **every frame**. **Return `false` to hide** the element for that frame — useful for UI that only appears while something is happening:

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
```

The client sees changes through `KitState.ObserveKits(player, fn)`.

When kits change:

- Removed kits run `OnRemoved` and lose their items.
- Added kits get stats, items and `OnGranted`.
- If a removed kit changed the character's look, the character respawns.

---

## HUD

| Panel | Element | Shows | Driven by |
|---|---|---|---|
| **Kit panel** | `Main.KitPanel` | Each active kit's name and `Info` rows | Kit definitions + kit state |
| **Ability bar** | `Main.AbilityBar` | One round button per usable ability, with key label, cooldown and disabled state | `Core.Abilities` usable list + specs |
| **Item panel** | `Main.ItemPanel` | The held item's name and `Info` rows. Hidden if it has none | Item definition |
| **Custom UI** | any `Main.<Element>` | Whatever your function draws | `CustomUI` tables |

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

- Kit abilities take slots first, in the order kits and their `Abilities` are listed; then the held item's other abilities.
- The held item's **first** ability is its click action and has no slot.
- Touch players tap the ability bar.
- Passive abilities never appear on the bar.

---

## API Reference

### Server

#### `KitService` — `Systems.Kits.KitService`

| Method | Description |
|---|---|
| `:SetKits(player, { kitName })` | Replace the player's active kits |
| `:SetKit(player, kitName?)` | Set one kit, or `nil` for none |
| `:GetKits(player) -> { string }` | Active kits, in order |
| `:HasKit(player, kitName) -> boolean` | Is the kit active |
| `:HasAbility(player, abilityName) -> boolean` | Does any active kit grant it |
| `:GiveItem(player, kitName, itemName) -> Tool?` | Give an item on behalf of a kit (removed with the kit) |
| `:GrantItems(player, kitName)` | Give the kit's missing items |
| `:ApplyStats(player)` | Apply the highest `MaxHealth` / `WalkSpeed` of the active kits |

#### `ItemService` — `Systems.Items.ItemService`

| Method | Description |
|---|---|
| `.Give(player, itemName) -> Tool?` | Build the Tool, put it in the Backpack, run `OnGiven` |

#### `AbilityService` — `Systems.Abilities.AbilityService`

| Method | Description |
|---|---|
| `:Use(player, abilityName, aim)` | Validate and run an ability |
| `:GetCooldown(player, abilityName) -> number` | Seconds left |
| `:SetCooldown(player, abilityName, seconds)` | Start or replace a cooldown (replicates to the client) |

### Shared

#### `KitState` — `Shared.KitState`

| Function | Side | Description |
|---|---|---|
| `.Of(player, kitName)` | both | State accessor for a kit (read-only on the client) |
| `.Get(player, kitName)` | both | State snapshot table |
| `.GetKits(player)` | both | Active kit names |
| `.HasKit(player, kitName)` | both | Is the kit active |
| `.HasAbility(player, abilityName)` | both | Does any active kit grant it |
| `.ObserveKits(player, fn) -> disconnect` | both | Call `fn(kits)` now and on every change (yields for data) |
| `.Definition(kitName)` | both | The kit's definition table |
| `.WaitForData(player) -> boolean` | both | Wait for the player's data |
| `.SetKits(player, kits)` | server | Low-level write. Use `KitService:SetKits` instead |

> On the client, `player` must be the `LocalPlayer` — each client only receives its own state.

#### `Items` — `Shared.Items`

| Function | Description |
|---|---|
| `.Get(itemName)` | Definition, or `nil` |
| `.Of(tool)` | Definition for a Tool, or `nil` |
| `.Grants(tool, abilityName)` | Does the Tool's item grant the ability |
| `.Create(itemName)` | New Tool from the model (caller parents it) |
| `.Count(player, itemName)` | How many the player carries |
| `.WireAbilities(player, use)` | Client: clicking an item Tool calls `use(abilityName, tool)` |

### Client

#### `Abilities` — `Client.Core.Abilities`

| Member | Description |
|---|---|
| `:Register(name, spec)` | Give an ability its client behaviour and look |
| `:GetSpec(name)` / `:GetSpecs()` | Registered spec(s) |
| `:GetUsable() -> { Usable }` | Abilities usable right now |
| `:GetSlot(slot) -> Usable?` | The ability on a slot key |
| `:Press(name)` / `:Release(name)` | Use an ability |
| `:IsEnabled(name)` | Usable and enabled |
| `:GetCooldown(name) -> (remaining, total)` | Cooldown for the bar |
| `:Request(name, aim?)` | Ask the server directly |
| `:GetAim() -> Vector3` | Mouse hit point, or a point in front of the character |
| `.Changed` | Signal: the usable list changed |

#### `Inputs` — `Client.Core.Inputs`

| Member | Description |
|---|---|
| `:GetKeyLabel(slot?) -> string` | Key text for a slot on the current device (`nil` = click action) |

---

## Packets

All packets live in `Shared.Packets`.

| Packet | Direction | Payload | Purpose |
|---|---|---|---|
| `Abilities.Use` | C → S | `name, x, y, z` | Use any kit or item ability |
| `Items.Equip` | C → S | `tool` | Equip a Backpack Tool on the server |
| `Items.Unequip` | C → S | — | Put away the held Tool |
| `Combat.Hit` | S → all | `character, damage` | Hit feedback |
| `Werewolf.Rest` | C → S | `boolean` | Set resting directly (wake on move) |
| `Werewolf.HuntTargets` | S → C | `tool, { targets }, expires` | Highlight hunt targets |
| `Golem.ConsumeStone` | C → S | `stone` | Eat an ancient stone |
| `Samurai.Charge` | C → S | `boolean` | Begin (`true`) or cancel (`false`) a dash charge |
| `Cauldron.BrewingState` | C → S | `cauldron, holding` | Brew prompt held |

> Always require `Shared.Packets` — never call `Packet("Name", ...)` from the command bar. A second copy of the packet library can't decode the real one's traffic.

---

## Built-in Content

### Kits

| Kit | Items | Abilities | State | HUD |
|---|---|---|---|---|
| Barbarian | Wooden Sword | Rage *(passive)* | `Rage`, `SwordLevel` | Custom UI: `Rage` |
| Golem | — | RockThrow | `Rocks`, `Scale` | Info: Rocks, Size |
| Samurai | Wooden Sword | Dash | `Charging`, `ChargeStartedAt` | Dash's custom UI: `DashCharge` |
| Scientist | — | Brew *(passive)* | — | — |
| Stew Boy | — | SummonCauldron, Brew *(passive)* | — | — |
| Werewolf | Werewolf Claws | Rest, Hunt | `MoonCharge`, `Resting`, `RestStartedAt`, `HuntingUntil`, `Transformed`, `Transforming`, `Combo` | Info: Moon, Bonus, Lifesteal, Charge, Hunting |

### Items

| Item | Abilities | Notes |
|---|---|---|
| Wooden / Stone / Iron / Diamond Sword, Rageblade | Slash | `Damage`, `Cooldown`; Rage upgrades through these |
| Fire / Poison / Speed / Shock Capsule | Throw | `Capsule` effect; Info: Carried; brewable |
| Meat, Ham | Consume | `HealAmount`; brewable |
| Eye | Consume | `RevealDuration`; brewable |
| Werewolf Claws | Claw | Hook: `WerewolfClaws`; Info: Combo |

### Abilities

| Ability | Granted by | Type | Cooldown |
|---|---|---|---|
| Rage | Barbarian | Passive | — |
| Brew | Scientist, Stew Boy | Passive (unlocks the cauldron) | — |
| RockThrow | Golem | Hold to aim, release to throw | 5s after a throw |
| Rest | Werewolf | Tap | 0.5s |
| Hunt | Werewolf | Tap (full moon only) | Hunt duration + 45s |
| Dash | Samurai | Hold to charge (or RMB), release to dash | 0.4s |
| SummonCauldron | Stew Boy | Tap | 1s |
| Slash | Swords | Click | Sword `Cooldown` |
| Throw | Capsules | Click | 0.3s |
| Claw | Werewolf Claws | Click | 0.55s (faster while hunting) |
| Consume | Meat, Ham, Eye | Click | 0.3s |

---

## Notes & Gotchas

- **Equips go through the server.** Client-side `Humanoid:EquipTool` (used by custom hotbars like NeoHotbar) doesn't replicate in this place, so `Client.Core.ToolSync` sends `Items.Equip` / `Items.Unequip` and the server equips for real. Without it, the server sees empty hands and refuses item abilities.
- **Item abilities need the item held on the server.** If an item ability "does nothing", check that the server's character has the Tool, not just the client's.
- **Kit state is session data.** It resets when the player leaves. Persisted data belongs elsewhere in the Scribe template.
- **Knockback vs. reach.** Sword hits knock targets ~2 studs back; the sword reaches 7 studs, so keep moving forward in a fight.
- **Custom UI starts hidden.** Elements named in any `CustomUI` table are hidden when the HUD starts, then shown only while in use.
- **Multiple kits.** Stats take the highest value; appearances apply in list order; abilities fill slot keys in order.
