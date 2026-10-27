# Kits, Abilities, Items, Effects, Blocks & Matches

A data-driven framework for kits, abilities, items, effects, block building and Bedwars-style matches in a Roblox game.

- **Definitions:** kits, items and blocks are plain definition modules. Abilities are small server modules with optional client specs. Effects are entries in one registry.
- **Kit state:** all player kit state lives in a shared [Scribe](https://scribe.ericplane.dev/) store. The server writes it and the client reads it.
- **Inventory:** every player has 36 slots, the first 9 are the hotbar. One server API (`ItemService`) gives, takes and moves items; the client only asks.
- **HUD:** the HUD builds itself from the definitions, so adding content never requires editing HUD code.
- **Effects:** the server never creates sounds or visuals. It sends an effect name, and every client plays it.
- **Blocks:** Bedwars-style building on a 3-stud grid. The server owns every block; clients only ask, then predict so building feels instant.
- **Matches:** a drop-in match system (`ReplicatedStorage.Match`): lobby, sky platform, teams, beds, generators, an item shop, team upgrades, kill feed, tab list and timed or random events.
- **Admin commands:** Cmdr commands to give items, kits and abilities and move teams, plus a `/shop` chat command.

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
  - [Matches](#matches)
- [Guides](#guides)
  - [Adding a Kit](#adding-a-kit)
  - [Adding an Item](#adding-an-item)
  - [Adding an Ability](#adding-an-ability)
  - [Adding an Effect](#adding-an-effect)
  - [Adding a Block](#adding-a-block)
  - [Adding a Special Block](#adding-a-special-block)
  - [Adding a Shop Entry](#adding-a-shop-entry)
  - [Adding a Team Upgrade](#adding-a-team-upgrade)
  - [Adding a Mode, Team, Event or Currency](#adding-a-mode-team-event-or-currency)
  - [Custom UI](#custom-ui)
  - [Setting a Player's Kits](#setting-a-players-kits)
- [Inventory & Hotbar](#inventory--hotbar)
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
  - [Generators, Beds & Shop Keepers](#generators-beds--shop-keepers)
  - [How a Request Flows](#how-a-request-flows)
  - [Grid Settings](#grid-settings)
- [Matches](#matches-1)
  - [Dropping It Into a Place](#dropping-it-into-a-place)
  - [Lifecycle](#lifecycle)
  - [Bedwars Rules](#bedwars-rules)
  - [Deaths & Kill Credit](#deaths--kill-credit)
  - [The Item Shop](#the-item-shop)
  - [Team Upgrades](#team-upgrades)
  - [Events](#events)
  - [Match HUD](#match-hud)
  - [Match State](#match-state)
  - [Mode Rules](#mode-rules)
  - [Match Settings](#match-settings)
- [Admin Commands](#admin-commands)
- [HUD](#hud)
- [Input](#input)
- [API Reference](#api-reference)
  - [Server](#server)
  - [Shared](#shared)
  - [Client](#client)
  - [Match](#match)
- [Packets](#packets)
- [Built-in Content](#built-in-content)
- [Notes & Gotchas](#notes--gotchas)

---

## Overview

| Concept | What it is | Where it lives |
|---|---|---|
| **Kit** | A loadout: stats, starting items, kit abilities, kit state, HUD info and shop changes | `Classes.Kits.<Kit>` |
| **Item** | A Tool with a definition: abilities, HUD info, server hooks, block/tool data, death rules | `Classes.Items.<Item>` |
| **Ability** | Server behaviour plus an optional client spec | `Systems.Abilities.Library.<Ability>` + `Client.Abilities.Library.<Ability>` |
| **Kit state** | Per-player, per-kit data replicated to the owning client | `Shared.KitState` (built on Scribe) |
| **Inventory** | 36 slots of `{ Item, Count }`, the first 9 are the hotbar | `Shared.Inventory` + `Systems.Items.ItemService` |
| **Effect** | A named sound, visual and/or animation, played on clients | `Classes.Effects` (registry) + `Client.Effects` (player) |
| **Block** | A grid block type: hardness, preferred tool, model, sounds, hooks | `Classes.Blocks.<Block>` + `Shared.Blocks` |
| **Tool type** | How an item breaks blocks: Pickaxe, Axe, Shovel, Sword, Hand | `Shared.ToolTypes` |
| **Match** | Lifecycle, teams, deaths, shop, upgrades, events and the match HUD | `ReplicatedStorage.Match` |
| **Mode** | A match's data (teams, upgrades, events) plus its rules module | `Classes.Modes.<Mode>` + `Match.Server.Modes.<Rules>` |
| **Currency** | A stack item spent at the shop (Iron, Diamond, Emerald) | `Classes.Currencies` |
| **Upgrade** | A team upgrade sold in tiers by the upgrade keeper | `Classes.Upgrades` |

Key rules:

- **Kit abilities** are granted by a player's active kits. Some abilities can also be **given on their own**, without a kit (see [Granted abilities](#granted-abilities)).
- **Item abilities** are granted by the **held** item, and work with **no kit equipped**.
- A player can have **several kits at once**.
- The server is the only writer of kit state, the inventory, block damage and match state. Client views are **read-only** and error on writes.
- The server **never** creates, plays or tweens effects. It calls `EffectService.Play`, and clients play the effect.
- Every client sound sits in a **sound group** under `SoundService.Master`.
- The server is the **only** place blocks are placed, broken or changed. Clients send requests and draw predictions.
- Every purchase is checked on the server. Clients never build shop listings.

---

## Project Layout

```text
ReplicatedStorage
├── Assets
│   ├── Sounds                        Effect sounds (Hit, Swing, BlockPlace, BlockBreak, Werewolf…, ChickenClucking)
│   ├── Vfx                           Particle Attachments (HitFX, SwingR, SwingL, Heal, ChickenFeathers)
│   ├── Music/Primary                 Background songs
│   └── Models
│       ├── Items/<Item>              Tool models, named after the item definition
│       ├── Blocks/<Model>            Block parts and models, named by a block's Model (ShopKeeper, UpgradeKeeper…)
│       ├── CapsuleSplashModels       Capsule puddle parts (Fire/Poison/Speed/ShockSplash)
│       ├── GolemBoulder, ChickenStampede, TurtleShield, OwlVision, SatelliteHack
├── Inputs
│   └── Default                       InputContext: Ability1–Ability5, Swing and Sprint
├── Match                             The match system (see below)
└── Modules
    ├── Classes
    │   ├── Kits/<Kit>                Kit definitions
    │   ├── Items/<Item>              Item definitions
    │   ├── Blocks/<Block>            Block definitions
    │   ├── Effects                   Effect registry: every sound and visual
    │   ├── Modes/<Mode>              Match modes (Bedwars)
    │   ├── MatchEvents               Shared timed and random match events
    │   ├── Currencies                Shop currencies
    │   ├── Shop                      The default shop listing
    │   ├── Upgrades                  Team upgrades and their tiers
    │   ├── Admins                    User ids that may run Cmdr and /shop
    │   ├── SwordLevels               Barbarian rage levels
    │   └── GolemConfig, HealthUI
    ├── Shared
    │   ├── Data                      Scribe template (Kits, Abilities, Inventory roots + ServerStore + ScribeFragments)
    │   ├── KitState                  Active kits, granted abilities and kit state
    │   ├── Items                     Item helper (definitions + item ability wiring)
    │   ├── Inventory                 Inventory slots, unlocks and death categories
    │   ├── Blocks                    Block helper: definitions, grid math, break rules
    │   │   └── Config                Grid and building settings
    │   ├── ToolTypes                 Pickaxe, Axe, Shovel, Sword, Hand
    │   ├── BlockState                Block damage (ServerStore), read-only on clients
    │   ├── ReadOnly                  Read-only wrapper for client Scribe views
    │   ├── Packets                   Every network packet (UnreliablePackets for footprints)
    │   └── ChickenRushConfig, OwlVisionConfig, SatelliteHackConfig, BoulderPath
    ├── Handlers
    │   ├── AnimationHandler          Loads and tracks animations (used by the Animation part)
    │   └── HitPopup, StateHandler
    ├── Utilities
    │   ├── Cmdr                      Cmdr command bar
    │   └── Packet, Signal, Zone, CameraShaker…
    └── Client
        ├── Core
        │   ├── Abilities             Client ability framework
        │   ├── Inputs                Slot keys and key labels
        │   ├── Music                 Background music (plays through the Music effect)
        │   ├── CmdrClient            Opens Cmdr with F2
        │   └── ToolSync              Server-side equip sync
        ├── Effects                   Client effect player: Play / Stop
        │   ├── Context               One playing effect: placement, timing, cleanup
        │   └── Parts/<Kind>          Sound, Animation and visual parts
        ├── Audio
        │   ├── SoundGroups           Group lookup and assignment
        │   └── AudioSettings         Group volumes (Store = saved values)
        ├── Blocks
        │   ├── BlockMap              Client copy of the occupancy map
        │   ├── BlockInput            Mouse → break / place actions
        │   ├── Targeting             Hover target and predictive placement
        │   ├── BlockVisuals          Hover outline, preview, placeholders, cracks
        │   ├── BlockController       Ties the above together every frame
        │   ├── GeneratorBillboards   Generator billboards: what each drops and how fast
        │   └── Hooks/<Hook>          Client block hooks (ShopKeeper)
        ├── Abilities/Library/<Ability>   Client ability specs
        ├── Hud
        │   ├── Hotbar                Hotbar slots, kit info line, currency balances
        │   ├── Inventory             Full inventory window (E)
        │   ├── ItemIcon              Item icons: image, model view or initials
        │   ├── AbilityBar            Ability buttons
        │   ├── KitUI / ItemUI        Kit and held-item CustomUI
        │   ├── CustomUI              Hand-made UI support
        │   ├── InfoRows              Info row renderer
        │   └── PersonalHealth, HealthBillboards
        ├── Kits/<Kit>                Kit-only client code (overlays, highlights)
        └── Items/<Item>              Item-only client code (aim arcs)

ReplicatedStorage.Match
├── Shared                            Config, Deps (paths to the place's systems), Store (Scribe roots), State, Packets
├── Server                            Core, Events, Shop, Commands, Integrations, Modes/<Rules>
│                                     (moved into ServerScriptService as MatchServer by Match.Start)
├── Client                            Main, Hud, TabList, KillFeed, Shop, Upgrades, Spectate, Messages, Icons, Ui
│   └── Gui                           UI templates: MatchTop, MatchResult, KillFeed, TabList, MatchShop,
│                                     MatchUpgrades, Spectating, TabButton
└── ClientLoader                      Installed in StarterPlayerScripts by Match.Start

ServerScriptService
├── MatchSetup                        require(ReplicatedStorage.Match).Start("Bedwars")
└── Modules
    ├── Services
    │   └── CmdrSetup                 Registers Cmdr hooks, types and commands
    │       ├── Hooks/BeforeRun       Who may run commands (Classes.Admins)
    │       ├── Types/<type>          item, kit, ability, team…
    │       └── Commands/<Command>    Definition + <Command>Server
    └── Systems
        ├── Kits
        │   ├── KitService            Sets kits, stats, items, hooks, granted abilities
        │   ├── Appearance            Applies kit rig looks
        │   └── Hooks/<Kit>           Per-kit server hooks
        ├── Items
        │   ├── ItemService           The inventory API, hotbar Tools, item hooks, server-side equips
        │   └── Hooks/<Hook>          Per-item server hooks
        ├── Abilities
        │   ├── AbilityService        Validates and runs ability requests
        │   └── Library/<Ability>     Server ability modules
        ├── Effects
        │   └── EffectService         Sends effects to clients
        ├── Combat                    Combat (hits, knockback), SwordCombat, DamageLog (kill credit)
        ├── Blocks
        │   ├── BlockService          Places, breaks and changes blocks
        │   │   ├── World             Occupancy map: which block fills each cell
        │   │   ├── Rules             Build area, free cells, NoBuild, reach, players in the way
        │   │   └── Damage            Break progress and healing
        │   └── Hooks/<Hook>          Server block hooks (Generator, Bed, ShopKeeper, HackerConnection)
        ├── Hacker                    HackService (leo's satellite hack), ResourceDrops
        ├── AnimalWhisperer           TurtleShield
        ├── Brewing, Golem, Samurai, Player, Enemies
        └── Werewolf
            ├── Appearance            Claw models, werewolf body and head
            └── Claws                 Overview + Config, Session, Rest, Moon, Hunt,
                                      Attack, Lunge, Hit, Effects

Workspace
├── World                             Map blocks, tagged Block (beds, shop keepers, upgrade keepers…)
├── Generators                        Generator blocks, tagged Block
└── PlacedBlocks                      Blocks placed by players (created by the server)

SoundService
└── Master                            Master sound group
    ├── Music
    ├── Abilities
    ├── Effects
    ├── UI
    └── Ambient

StarterGui
└── Main
    ├── Hotbar                        Hotbar slots, kit info line, balances (restyle via its Templates folder)
    ├── Inventory                     Inventory window
    ├── AbilityBar                    Ability bar (restyle via its Templates folder)
    ├── Rage, DashCharge, MoonPower,  Custom UI used by kits and abilities
    │   SatelliteTargets
    └── Health, HitPopup, KitSelect, Mobile, WerewolfHuntTint, RestDarkness
    (the match adds MatchTop, KillFeed, TabList, MatchShop, MatchUpgrades… at runtime)

ServerStorage
├── README                            In-Studio copy of these docs (disabled Script)
├── WerewolfClaws                     Claw and eye models (server welds them on)
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
| `Items` | `{ string }` | ✅ | Item names given on kit set and every spawn (unlocked for the match) |
| `Abilities` | `{ string }` | ✅ | Abilities this kit grants |
| `Icon` | `string` | ❌ | Image shown next to the player in the tab list. Without one, the kit's initials |
| `State` | `{ [string]: Scribe field }` | ❌ | Kit state, declared with Scribe |
| `Info` | `{ InfoRow }` | ❌ | Rows shown on the hotbar's kit line |
| `Shop` | `{ Add?, Remove?, Price? }` | ❌ | Changes to this kit's players' match shop |
| `CustomUI` | `{ [string]: (gui, state) -> boolean? }` | ❌ | Hand-made UI in `StarterGui.Main` |

Server hooks go in `Systems.Kits.Hooks.<Kit>` (all optional):

| Hook | When it runs |
|---|---|
| `OnGranted(player)` | The kit is added |
| `OnSpawned(player)` | Every spawn while the kit is active |
| `OnRemoved(player)` | The kit is taken away |
| `ShopChanges(player) -> change?` | The match shop is rebuilt for this player: shop changes that depend on the player |
| `Start()` | Once, by ModuleLoader (e.g. connect an equip prompt) |

### Items

An item is a ModuleScript in `ReplicatedStorage.Modules.Classes.Items`. Its Tool model is the Tool with the **same name** in `ReplicatedStorage.Assets.Models.Items`.

| Field | Type | Required | Description |
|---|---|---|---|
| `DisplayName` | `string` | ✅ | Shown to players |
| `Image` | `string` | ❌ | Its icon. Without one, the UI shows a small view of its model, then its initials. Generator billboards need it for a real picture |
| `Abilities` | `{ string }` | ✅ | Abilities granted while held. **The first one is the click action** |
| `Info` | `{ InfoRow }` | ❌ | Rows in the inventory's item details |
| `CustomUI` | `{ [string]: (gui, context) -> boolean? }` | ❌ | Hand-made UI shown while held |
| `Hooks` | `string` | ❌ | Name of a module in `Systems.Items.Hooks` |
| `Stack` | `boolean` | ❌ | Piles into one inventory slot with no stack limit (blocks, resources). Anything else takes one slot each |
| `KeepOnDeath` | `"Sword" \| "Tool" \| "KitGear"` | ❌ | Its death category. Unlocked items in a kept category survive death in a match |
| `Block` | `string` | ❌ | The block in `Classes.Blocks` this item places |
| `ToolType` | `string` | ❌ | `Pickaxe`, `Axe`, `Shovel` or `Sword`. No `ToolType` = held like an empty hand |
| `Speed` | `number` | ❌ | Breaking speed multiplier, with `ToolType` |
| `CanBreakBlocks` | `boolean` | ❌ | `false` for swords. With `ToolType` |
| `RequiredKit` | `string` | ❌ | Only players with this kit can buy it at the match shop |
| `MaxOwned` | `number` | ❌ | The shop refuses to sell more than this many |
| *anything else* | `any` | ❌ | Item data, e.g. `Damage`, `Cooldown`, `Capsule`, `HealAmount`, `Brewed` |

Item hooks (`Systems.Items.Hooks.<Hook>`, all optional):

| Hook | When it runs |
|---|---|
| `OnGiven(player, tool)` | Every time the item's hotbar Tool is made |
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

A request runs only if the ability exists, the **held item, an active kit, or a granted ability** allows it, and its cooldown has passed. Cooldowns are stored in the `Abilities` session root (`ReadyAt`, server time) and replicate to the client automatically.

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

#### Granted abilities

An ability can be given to a player **without a kit** with `KitService:GrantAbility(player, name)` (or the `giveability` command). Granted abilities count for `HasAbility`, show on the ability bar after the kit abilities, and last until the player leaves.

Only abilities that need **no item** can be granted (`KitState.Grantable()`). An ability qualifies when:

- at least one kit lists it,
- no item lists it, and
- every kit that lists it gives no items.

Today that's **Brew, ChickenRush, OwlVision, RockThrow, SatelliteHack and SummonCauldron**. Slash, Claw, Throw, Consume, Dash, Rage, Rest and Hunt need an item and are refused. New kits and items are picked up by the same rule automatically.

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

> ⚠️ Don't name a state field after a Scribe accessor method (`Active`, `Get`, `Set`, `Count`, `Remove`, …). The method shadows the field, and Scribe errors with `API_NAME_COLLISION`.

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
- **Placing** is predictive, like Bedwars: aim anywhere ahead and the next block goes at the end of your bridge. Auto clickers work.
- **Special blocks** (generators, beds, shop keepers, upgrade keepers, leo's Hacker Connection) are normal blocks with a `Hooks` module.

See [Blocks & Building](#blocks--building) for the full reference.

### Matches

`ReplicatedStorage.Match` is a self-contained match system. One line starts it:

```lua
-- ServerScriptService.MatchSetup
require(game:GetService("ReplicatedStorage"):WaitForChild("Match")).Start("Bedwars")
```

- **Generic core, mode rules:** `Server.Core` runs the lifecycle, teams, deaths, time and win checks for any mode. A mode is data in `Classes.Modes.<Mode>` plus a rules module in `Match.Server.Modes.<Rules>`.
- **Server-authoritative:** match state lives in Scribe's `ServerStore` (`Match` root) and each player's `MatchShop` session root. Clients only read them.
- **Uses the place's systems when present:** items, kits, blocks, effects and the HUD are optional dependencies, found through `Match.Shared.Config.Paths`.

See [Matches](#matches-1) for the full reference.

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
   	Icon = "rbxassetid://0",          -- tab list icon (optional)
   	State = {
   		Smoke = Scribe.Int(3, { Min = 0, Max = 3 }),
   	},
   	Info = {
   		{
   			Label = "Smoke",
   			Text = function(state) return string.format("%d / 3", state.Smoke) end,
   		},
   	},
   	Shop = {                           -- optional match shop changes
   		Price = { ["Stone Sword"] = { Iron = 15 } },
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
4. **Add its effects** — see [Adding an Effect](#adding-an-effect).
5. **Add kit-only client code** *(optional)* — `Client.Kits.Ninja/...`

No HUD changes are needed: the hotbar's kit line reads `Info`, the ability bar reads `Abilities`, and the tab list reads `Icon`. The `givekit` command picks up the new kit automatically.

### Adding an Item

1. **Add the Tool** to `ReplicatedStorage.Assets.Models.Items`, named after the item.
2. **Create the definition** — `Classes.Items.Smoke Bomb`:

   ```lua
   --!strict
   return {
   	DisplayName = "Smoke Bomb",
   	Image = "rbxassetid://0",
   	Abilities = { "Throw" },        -- clicking the Tool uses this
   	Stack = true,                   -- piles into one slot
   	Info = {
   		{
   			Label = "Carried",
   			Text = function(context) return tostring(context.Count) end,
   		},
   	},
   }
   ```

3. **Add a server hook** *(optional)* — `Systems.Items.Hooks.<Name>` with `OnGiven(player, tool)`, and set `Hooks = "<Name>"` in the definition.
4. **Give it** with `ItemService.Give(player, "Smoke Bomb", 3)`, sell it in `Classes.Shop`, list it in a kit's `Items`, or use `give me "Smoke Bomb"` in Cmdr.

A block-breaking tool needs `ToolType`, `Speed` and `CanBreakBlocks`. Give it `KeepOnDeath = "Tool"` so players keep it after dying, and so the shop sells it only once a match:

```lua
-- Classes.Items.Stone Pickaxe
return {
	DisplayName = "Stone Pickaxe",
	Abilities = {},
	ToolType = "Pickaxe",
	Speed = 1.5,                 -- 1.5x faster than a wooden pickaxe
	CanBreakBlocks = true,
	KeepOnDeath = "Tool",
}
```

### Adding an Ability

1. **Server** — `Systems.Abilities.Library.Vanish`:

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

3. **Grant it** by listing it in a kit's or item's `Abilities`. If it needs no item, it can also be given with `giveability`.

### Adding an Effect

Adding an effect only needs an entry in `Classes.Effects`.

1. **Put its assets** in `ReplicatedStorage.Assets` — sounds in `Sounds`, particle Attachments in `Vfx`, models in `Models`.
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

1. **Add the model** — a part or model in `ReplicatedStorage.Assets.Models.Blocks`, sized to the block's cells (3 studs per cell).
2. **Create the definition** — `Classes.Blocks.Glass`:

   ```lua
   --!strict
   return {
   	DisplayName = "Glass",
   	Id = 27,                         -- unique, never reused once players have it
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

3. **Make it placeable by players** — add a stack item with `Block` pointing at it, and its Tool model in `Assets.Models.Items`:

   ```lua
   -- Classes.Items.Glass
   return {
   	DisplayName = "Glass",
   	Abilities = {},
   	Block = "Glass",
   	Stack = true,
   }
   ```

4. **Sell it** *(optional)* — add an entry to `Classes.Shop` (see [Adding a Shop Entry](#adding-a-shop-entry)).

`Shared.Blocks` checks every definition when it loads and **errors right away** on a missing or wrong field, or a duplicate `Id`.

### Adding a Special Block

1. Set `Hooks = "Trap"` on the block definition, plus any data the hook reads (e.g. `Damage = 10`).
2. **Server hook** — `Systems.Blocks.Hooks.Trap`:

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

   function Trap.OnReset(block)
   	-- a match reset: put block.Data back as it started
   	block.Data.Armed = true
   end

   return Trap
   ```

3. **Client hook** *(optional)* — `Client.Blocks.Hooks.Trap` with `OnHover(entry, hovering)` and/or `OnInteract(entry)`.
4. **A prompt** *(optional)* — `Interact = { ActionText = "Arm" }` on the definition gives the block a ProximityPrompt (on **F**) that runs `OnInteract`.

See [Block Hooks](#block-hooks) for every hook.

### Adding a Shop Entry

Add a line to `Classes.Shop.Entries`:

```lua
{ Item = "Glass", Category = "Blocks", Amount = 16, Price = { Iron = 12 } },
{ Item = "Stone Pickaxe", Category = "Tools", Price = { Iron = 30, Diamond = 1 } },
```

| Field | Description |
|---|---|
| `Item` | An item in `Classes.Items`, or a block in `Classes.Blocks` (sold as the item that places it). `"{Team}"` in it is the buyer's team name: `"{Team} Wool"` is Red Wool for the Red team |
| `Id` | Unique in the listing. Defaults to `Item` (set it when `Item` uses `{Team}`, e.g. `Id = "Wool"`) |
| `DisplayName` | Defaults to the item's |
| `Icon` | Defaults to the item's `Image`; without one the shop shows the item's model |
| `Category` | One of `Classes.Shop.Categories`: `Blocks`, `Combat`, `Tools`, `Items` |
| `Amount` | How many one purchase gives. Default 1 |
| `Price` | `{ [currency id] = amount }`, in one or more currencies |

Kits and modes change the listing with **changes**: `{ Add = { entries }, Remove = { ids }, Price = { [id] = { [currency] = amount } } }` (see [The Item Shop](#the-item-shop)).

### Adding a Team Upgrade

1. Add it to `Classes.Upgrades`:

   ```lua
   Haste = {
   	DisplayName = "Haste",
   	Icon = "",             -- image id; without one the Glyph shows
   	Glyph = "💨",
   	Order = 5,             -- card position in the upgrades window
   	Tiers = {
   		{ Price = { Diamond = 4 }, Text = "+10% speed" },
   		{ Price = { Diamond = 8 }, Text = "+20% speed" },
   	},
   },
   ```

2. List its id in the mode's `Upgrades` (`Classes.Modes.Bedwars.Upgrades`).
3. Make it do something in the mode rules' `OnUpgrade(match, teamId, upgradeId, level)`.

The upgrade keeper sells it one tier at a time, the upgrades window gets a card for it, and the tab list shows it with its level in roman numerals. Nothing else needs editing.

### Adding a Mode, Team, Event or Currency

| To add | Do this |
|---|---|
| **A mode** | `Classes.Modes.<Mode>` (fields are described in `Modes.Bedwars`) and `Match.Server.Modes.<Rules>` with the [rules](#mode-rules) it needs. Start it with `Match.Start("<Mode>")` |
| **A team** | `{ Id, DisplayName, Color }` in the mode's `Teams`. The map needs one bed per team for Bedwars |
| **A timed event** | `{ At = seconds, Title, Text, Color, Info?, Pause?, Hook? }` in `Classes.MatchEvents.Timed` (list its name in the mode's `Events.Timed`), or inline in the mode |
| **A random event** | `{ Window = { from, to }, Weight, Cooldown, Condition?, Title, Text, Color, Info?, Hook? }` in `Classes.MatchEvents.Random`, listed in the mode's `Events.Random` |
| **A currency** | `Classes.Currencies.<Id> = { DisplayName, Item, Icon, Color, Order }`. `Item` is a stack item; the balance is the player's inventory count of it |

An event's `Hook` names a function in the mode rules' `Events` table, called as `Hook(match, event)`.

### Custom UI

Use your own hand-made UI instead of (or as well as) info rows. Kits, items and abilities all support it.

1. Build the element in `StarterGui.Main` (it's hidden automatically when the HUD starts, so you can leave it visible while editing).
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

KitService:GrantAbility(player, "ChickenRush")         -- one ability, no kit
KitService:RevokeAbility(player, "ChickenRush")
```

The client sees changes through `KitState.ObserveKits(player, fn)` and `KitState.ObserveGranted(player, fn)`. The match hears about them through its `KitAssigned` hook and rebuilds that player's shop.

When kits change:

- Removed kits run `OnRemoved` and lose their items.
- Added kits get stats, items (unlocked for the match) and `OnGranted`.
- If a removed kit changed the character's look, the character respawns.

---

## Inventory & Hotbar

Every player has `Inventory.SLOTS` (36) slots of `{ Item, Count }`. The first `Inventory.HOTBAR` (9) are the hotbar.

- **Stack items** (`Stack = true`: blocks, iron, diamonds, emeralds) pile into one slot with **no stack limit** (only the store's 9999 per slot). Any other item, like a sword, takes one slot each.
- A block is carried as the item that places it.
- The inventory lives in the `Inventory` **session** root of the store (`Slots` and `Unlocked`), so nothing is saved. The server owns it; each client reads its own through a read-only view.
- **Tools are only a view of the hotbar.** `ItemService.SyncTools` makes one Tool per filled hotbar slot after every change (each Tool carries an `InventorySlot` value). Roblox's own backpack is off.
- **Unlocked** items are the ones a player bought at the shop, got from their kit, or started with this match. The match's death rules keep unlocked items in a kept `KeepOnDeath` category.

**One API** — `Systems.Items.ItemService` is the only place the inventory changes. The shop, kits, the match and blocks all use it:

```lua
ItemService.Give(player, "Iron", 10)                         -- returns how many fit
ItemService.Give(player, "Stone Sword", 1, { Unlock = true }) -- also unlocked for the match
ItemService.Take(player, "Iron", 4)                          -- all or nothing
ItemService.Consume(player, tool)                            -- one from the held Tool's slot (placing a block)
ItemService.CanFit(player, "Wool", 16)
ItemService.Clear(player, keep?)                             -- keep(slot, index) -> boolean
```

Read it from either side:

```lua
Inventory.Slots(player)          -- { { Item, Count } }, 36 long
Inventory.Count(player, "Iron")  -- total over every slot
Inventory.Observe(player, fn)    -- fn(slots) now and on every change
Inventory.IsUnlocked(player, "Stone Sword")
Inventory.KeepOnDeath("Wooden Pickaxe") --> "Tool"
```

**UI**

| Element | What it does |
|---|---|
| `Hud.Hotbar` (`Main.Hotbar`) | The 9 hotbar slots with icons and counts. Keys **1–9** or a click use a slot: the server equips it, or puts it away if it's held. Above the slots, the **kit line** shows your kits' `Info` rows, and **Balances** show your currencies |
| `Hud.Inventory` (`Main.Inventory`) | **E** opens the full grid. Click an item, then a slot, to move it (same items merge, others swap). Right-click splits a stack. The details show the item's name, `Info` rows, and its death rule. E does nothing while the item shop or upgrades window is open |
| `Hud.ItemIcon` | Draws an item's icon everywhere (hotbar, inventory, shop, kill feed): its `Image`, else a small 3D view of its model, else its initials |

Clients only ask: `Items.MoveSlot`, `Items.SplitSlot` and `Items.UseSlot` name the slot and the item the client saw there, and the server checks both before acting.

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
| `Sound` | part or `{ part }` | — | Sound part(s) |
| `Visual` | part or `{ part }` | — | Visual part(s). `Kind` names a module in `Client.Effects.Parts` |
| `Animation` | part | — | Animation part, played through `AnimationHandler` |
| `Variants` | `{ [any]: fields }` | — | Fields that replace the ones above when played with that `Variant` (e.g. a combo step, capsule type, or block sound category) |

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
| `ClawSwing` | — | The werewolf combo swipe. `Variant` = combo step, `Speed` = attack speed, `Tool` = claws |
| `SleepSymbols` | `Interval`, `MaxDistance` | Zs rising from the head until stopped |
| `ColorFade` | `Time` | Fades body parts using `Data.Colors = { [partName] = { From, To } }` |
| `SamuraiPose` | `Phase = "Charge" \| "Release"` | IK sword pose. `Tool` = sword. Stop with `{ Instant = true }` to snap back |
| `ChickenRush` | — | The Animal Whisperer's chicken stampede |
| `Banner` | — | A screen banner from `Data.Title`, `Data.Text` and `Data.Color` (match start, bed destroyed, wins) |
| `Satellite` | — | leo's satellite flying to the hacked team |
| `HackWarning` | — | The warning shown to a hacked team |

### Playing Effects

**Client** — `ReplicatedStorage.Modules.Client.Effects`:

```lua
local Effects = require(ReplicatedStorage.Modules.Client.Effects)

Effects.Play("Hit", { Target = character })
Effects.Play("GolemShatter", { Position = position })

local handle = Effects.Play("Music", { Sound = song, OnFinished = nextSong })
handle:Stop()

Effects.Stop("WerewolfSleep", character)
```

**Server** — `ServerScriptService.Modules.Systems.Effects.EffectService`:

```lua
local EffectService = require(ServerScriptService.Modules.Systems.Effects.EffectService)

EffectService.Play("WerewolfClawSwing", { Target = character, Tool = claws, Variant = combo, Speed = 1.5 })
EffectService.Play("CapsuleSplash", { CFrame = cframe, Variant = "Fire" })
EffectService.Play("BedDestroyed", { Data = { Title = "Red bed destroyed", Text = "by Player1", Color = color } })
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
| `All` | Every client | `Hit`, `SwordUpgrade`, `WerewolfSleep`, `WerewolfTransform`, `WerewolfTransformHowl`, `CapsuleSplash`, `SamuraiCharge`, `SamuraiRelease`, `ChickenRush`, `SatelliteHack`, `SatelliteHackWarning`, `MatchBanner`, `BedDestroyed`, `TeamEliminated`, `MatchWin` |
| `Nearby` | Clients whose character is within `Range` studs | `SwordSwing` (200), `WerewolfClawSwing` (300), `WerewolfHuntHowl` (150), `GolemThrow` (300), `GolemShatter` (300), `BlockPlace` (150), `BlockBreak` (150), `BlockHit` (80), `GeneratorSpawn` (80), `PlayerKilled` (250) |
| `Local` | Not sent — only the client plays it | `SwordSlash`, `ButtonHover`, `ButtonClick`, `Music`, `ShopPurchase`, `ShopDenied`, `InventoryOpen`, `InventoryClose`, `InventoryMove`, `TabListOpen` |

Why each one:

- **All:** persistent effects, match announcements, and effects with gameplay meaning (players must see a capsule puddle to avoid it).
- **Nearby:** short sounds and motion that can't be seen or heard much further away.
- **Local:** the owner's own animations (they replicate through the Animator), UI sounds and music.

Effects are only sent to clients that have finished loading (the `_ModulesLoaded` player attribute), so players joining mid-game never get packets they can't decode yet.

### Sound Groups

```text
SoundService
└── Master
    ├── Music        background music
    ├── Abilities    ability sounds: swings, claw swipes, howls, snore
    ├── Effects      hits, impacts and block sounds (also the default group)
    ├── UI           buttons, banners, shop, inventory and tab list sounds
    └── Ambient      reserved for world ambience
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

Saved values come from `AudioSettings.Store`, which only has `Load()` and `Save(volumes)`. Today it keeps them for the session. To save volumes in player data, change `Store` only — `AudioSettings` and `Client.Effects` need no changes.

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
| `DisplayName` | `string` | ✅ | Shown to players (and as the prompt's object text) |
| `Id` | `number` | ✅ | Unique. Keep it the same once used; never reuse an old one |
| `Hardness` | `number` | ✅ | Seconds to break with the preferred tool at `Speed` 1 |
| `Breakable` | `boolean` | ✅ | `false` for blocks that can be hovered but never broken |
| `Placeable` | `boolean` | ✅ | Whether players can place it. Placeable blocks need a `Model` |
| `Model` | `string` | when placeable | A part or model in `Assets.Models.Blocks` |
| `SoundCategory` | `string` | ✅ | `Variant` for the place/break/hit effects: `Wool`, `Wood`, `Stone`, `Dirt`, `Generic` |
| `BreakEffect` / `PlaceEffect` | `string` | ✅ | Effect names in `Classes.Effects` |
| `PreferredTool` | `string` | ❌ | `Pickaxe`, `Axe` or `Shovel`. `nil` = every breaking tool is full speed |
| `Size` | `Vector3` | ❌ | Cells it fills. Default `1 × 1 × 1` |
| `HealDelay` | `number` | ❌ | Seconds without a hit before damage resets. Off by default |
| `Interact` | `{ ActionText, HoldDuration? }` | ❌ | Gives the block a prompt (on F) that runs its `OnInteract` hooks |
| `Hooks` | `string` | ❌ | Module name in `Systems.Blocks.Hooks` and `Client.Blocks.Hooks` |
| *anything else* | `any` | ❌ | Block data for its hooks, e.g. `Resource`, `Interval`, `Limit` on generators, `Shop` on the shop keepers |

### Tool Types & Breaking

`Shared.ToolTypes` defines every kind of tool once:

| ToolType | Breaks blocks |
|---|---|
| `Pickaxe` | ✅ |
| `Axe` | ✅ |
| `Shovel` | ✅ |
| `Sword` | ❌ |
| `Hand` (no tool, or an item with no `ToolType`) | ❌ |

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

Placement works like Bedwars, in first or third person, so bridging needs no exact aim (`Client.Blocks.Targeting`). A black outline previews where the block will go (red where it can't); out of reach, nothing shows.

In order, the block goes:

1. **Against a side or bottom face you aim at** — so aiming under a block places under it.
2. **On your own level**, first along the path from under your feet toward the aim (so aiming anywhere ahead, even into the void, extends the bridge), then in the open cell nearest the aim.
3. Only then **on top of a block**.

Other rules:

- **Pillaring:** look down at the block under you. A block placed in your feet **lifts you onto it**.
- **Reach:** `PLACE_REACH` (24 studs, about 8 blocks). The server allows `PLACE_REACH_SLACK` (6) more, since it sees the character a little behind the client.
- **Touching:** a placed block must touch an existing block, so players build out from what exists.
- **Speed:** a click places one block at once. Holding past 0.25s, or clicking fast (an auto clicker works), places one every `PLACE_INTERVAL` (0.06s).
- **Prediction:** each placement shows a solid placeholder until the server's block arrives, so building never waits on the server. A placement the server refuses comes back as `Blocks.Rejected`, and its placeholder goes at once — no fake blocks.
- The server also refuses cells that are filled, tagged `NoBuild`, outside the build area, or where **another** player stands.

### Map Blocks

- Tag a part or model **`Block`** to make it part of the grid.
- Give it a **`BlockType`** attribute to make it a named block (e.g. `Stone`, `Bed`, `ShopKeeper`, `UpgradeKeeper`), or leave it out for `MapBlock`, which can be hovered but never broken.
- Tag a part **`NoBuild`** to block placement in its cells.
- Map blocks live in `workspace.World` and `workspace.Generators`. Placed blocks go in `workspace.PlacedBlocks`.
- On start, typed blocks load first. A map block that overlaps one already loaded is skipped, with one warning that counts them.
- `BlockService.Reset()` (run when a match resets) removes placed blocks, puts broken map blocks back, clears damage and runs every map block's `OnReset`.

### Block Hooks

**Server** — `Systems.Blocks.Hooks.<Hook>` (all optional):

| Hook | When it runs |
|---|---|
| `CanPlace(player, definition, origin, size) -> (boolean, reason?)` | Before a placement. Return `false` to refuse |
| `OnPlaced(block, player?)` | After the block is added. `player` is `nil` for map blocks |
| `CanBreak(block, player) -> boolean` | Before each hit. Return `false` to refuse |
| `OnBroken(block, player)` | Before the block is removed |
| `OnInteract(block, player) -> boolean?` | A player used its prompt. Return `false` to skip the client hook |
| `OnTick(block, dt)` | Every `TICK_INTERVAL` |
| `OnReset(block)` | `BlockService.Reset` ran: put `block.Data` back as it started |

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

Other systems can watch blocks with `BlockService.ObserveBroken(fn)`, which runs `fn(block, player?)` after any block is removed.

**Client** — `Client.Blocks.Hooks.<Hook>` (all optional):

| Hook | When it runs |
|---|---|
| `OnHover(entry, hovering)` | The player started or stopped aiming at the block |
| `OnInteract(entry)` | The server allowed an interaction with the block's prompt |

`entry` is a `BlockMap.Entry`: `Key`, `Origin`, `Size` and `Definition`.

### Generators, Beds & Shop Keepers

| Block | Hook | Behaviour |
|---|---|---|
| Iron / Diamond / Emerald Generator | `Generator` | Every `Interval` seconds, adds one `Resource` to a **single falling drop** that stacks up to `Limit`, so a full generator is one part, not dozens. Touching the drop picks up the whole stack. Each add plays `GeneratorSpawn`. A generator can drop several items, each with its own interval |
| Bed | `Bed` | A bed's team is `block.Data.Team`. Nobody can break their own team's bed. In a match, Bedwars gives each map bed to a team and paints its `Blanket` part in the team color |
| Shop Keeper | `ShopKeeper` (`Shop = "Items"`) | Its prompt (F) opens the **item shop**. One in every base |
| Upgrade Keeper | `ShopKeeper` (`Shop = "Upgrades"`) | Its prompt (F) opens the **team upgrades** window. One in every base |
| Hacker Connection | `HackerConnection` | leo's block. Only leo can place one (one at a time, during a match); it powers the satellite hack and stores taxed resources until collected or broken |

**Generator API** (`Systems.Blocks.Hooks.Generator`):

```lua
Generator.SetOutput(block, "Diamond", 30, 10)   -- also drop Diamond every 30s, up to 10 waiting
Generator.SetOutput(block, "Diamond", nil)      -- stop dropping Diamond
Generator.SetSpeed(block, 2)                    -- its own Resource drops twice as fast
Generator.SetTier(block, 3)                     -- the tier it publishes
```

**Generator billboards** (`Client.Blocks.GeneratorBillboards`): each generator's BillboardGui shows every item it drops as a picture with its **current time per drop**, like `1.5s`, or `Full` while that stack is full. The server publishes this in the generator's `Drops` attribute only when it changes. The `Title` label takes the generator's `TeamColor` attribute (set by Bedwars for team generators); the `Tier` label is hidden.

> 3D item views don't render inside a BillboardGui, so the picture is the item's `Image`. Until an item has one, it shows a badge with its initial in its currency color.

### How a Request Flows

**Placing**

1. The client finds the cell (`Targeting`), shows a placeholder, and sends `Blocks.Place(cell, turned)`.
2. The server checks: the held item is a block item the player has, the build area, free and `NoBuild` cells, reach, touching, players in the way, the hook's `CanPlace`, and the rate limit.
3. Accepted: the server builds the block in `workspace.PlacedBlocks`, takes one item (`ItemService.Consume`), lifts the placer if the block is in their feet, runs `OnPlaced`, plays `PlaceEffect`, and sends `Blocks.Placed` to every client.
4. Refused: the server sends `Blocks.Rejected(cell)` to that player, and their placeholder goes.

**Breaking**

1. While the mouse is held with a breaking tool, the client sends `Blocks.Hit(cell)` every `HIT_INTERVAL`.
2. The server checks reach, `Breakable`, `CanBreakBlocks`, the hook's `CanBreak`, and the rate limit, then adds damage to `Shared.BlockState`.
3. At full damage it runs `OnBroken`, removes the block, plays `BreakEffect`, sends `Blocks.Removed` to every client, and calls every `ObserveBroken` listener.

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
| `PLACE_REACH` | `24` | Studs to place a block (about 8 blocks) |
| `PLACE_REACH_SLACK` | `6` | Extra studs the server allows for lag |
| `PLACE_INTERVAL` | `0.06` | Seconds between placements while held or clicked fast |
| `SLOW_MULTIPLIER` | `0.3` | Speed multiplier for the wrong tool |
| `HIT_INTERVAL` | `0.2` | Seconds between break hits while held |
| `MAX_HIT_GAP` | `0.35` | Most break time one hit can add |
| `PLACE_RATE` / `HIT_RATE` | `30` / `12` | Requests per second before the server ignores them |
| `CRACK_STAGES` | `5` | Crack overlay stages |
| `TICK_INTERVAL` | `0.25` | Seconds between `OnTick` calls |
| `BLOCK_TAG` / `NO_BUILD_TAG` | `"Block"` / `"NoBuild"` | CollectionService tags |
| `TYPE_ATTRIBUTE` / `MAP_BLOCK` | `"BlockType"` / `"MapBlock"` | Map block type attribute and default |

---

## Matches

### Dropping It Into a Place

1. Copy `ReplicatedStorage.Match` into the place.
2. Add a Script in `ServerScriptService`:

   ```lua
   require(game:GetService("ReplicatedStorage"):WaitForChild("Match")).Start("Bedwars")
   -- or with overrides for Match.Shared.Config:
   require(game:GetService("ReplicatedStorage"):WaitForChild("Match")).Start("Bedwars", { MinPlayers = 4 })
   ```

`Start` turns off `Players.CharacterAutoLoads`, moves `Server` into `ServerScriptService` (so clients never get its code), installs `ClientLoader` in `StarterPlayerScripts`, and opens the lobby. It returns `Server.Core`, also reachable later with `Match.Server()`.

The place needs Scribe, the Packet library, a `Shared.Data` that adds the roots of every module tagged `ScribeFragment` (like `Match.Shared.Store`), and `Classes` with the match content. Items, inventory, kits, blocks, effects and the HUD are used when the place has them; their paths are in `Match.Shared.Config.Paths`, and `Match.Server.Integrations` is the only file that talks to them.

### Lifecycle

| Phase | What happens |
|---|---|
| **Lobby** | Players wait at the place's spawn. Once `MinPlayers` are in (`StudioMinPlayers`, 1, in Studio play tests), PreGame begins |
| **PreGame** | Teams are filled (balanced) and the mode's `Setup` runs. Everyone's first spawn is on a **sky platform** (`PlatformCFrame`, with a ForceField) for `StartCountdown` seconds. Too few players goes back to Lobby |
| **InProgress** | Everyone is teleported to their team's spawn and their kit and items are applied again; only then do the clock, events and respawns start. Later deaths respawn at the team spawn |
| **Ending** | The winner (or a draw) shows for `EndDuration` seconds |
| **Resetting** | Everything the match made is undone: placed blocks, broken map blocks, generators, kits, items, unlocks, teams and `/shop` changes. Then Lobby |

- The match **ends** when one team is left with players (it wins) or none (a draw). A match started by one team (a solo test) ends only when that team is out.
- The match spawns everyone itself. A character it didn't spawn is moved to where the player belongs.
- **Out** players and players who **join mid-match** spectate (`Client.Spectate`: the camera follows living players; click for the next one).
- The timer can be paused: `Match.Server().Pause()` and `Resume()`, or `Paused = true` in Config to start paused.

### Bedwars Rules

`Match.Server.Modes.Bedwars`, with its data in `Classes.Modes.Bedwars`:

- **Beds:** the map's beds are given to the teams in order of their angle around the map, so no map is named in code. Each bed's `Blanket` is painted in its team's color.
- **Spawns:** each team spawns `BedSpawnOffset` studs behind its bed, facing out over its island.
- **Respawning:** while a team's bed stands, its players respawn after `RespawnDelay` (5s). After it breaks (`BedDestroyed` banner), a player who dies is **out**, and a team with nobody left is eliminated (`TeamEliminated`).
- **Void:** falling `VoidDepth` (30) studs below the lowest spawn kills.
- **Team generators:** generators within 48 studs of a team's bed belong to it. Their billboard title is the team color, and `TeamGen` / `DiamondGen` upgrades speed them up and add diamonds and emeralds.
- **Events:** `SuddenDeath` breaks every standing bed; `LowGravity` lowers gravity for 30 seconds. `DiamondsII` and `IronRush` are hook points.
- **Starting items:** `StartingItems` (a Wooden Sword), given unlocked on every spawn when missing.

### Deaths & Kill Credit

For every mode (`Server.Core`):

1. **Kill credit:** the killer is whoever last hit the victim within `KillCreditWindow` (10) seconds, from `Systems.Combat.DamageLog` (`Combat.ApplyHit` records `{ Attacker, Item }`). Never the victim or a teammate. Falling into the void after a hit still credits the hitter.
2. **Currencies:** the victim's currencies go to the killer (`AwardCurrencies`), or are lost with no killer.
3. **Items:** the victim keeps only **unlocked** items whose `KeepOnDeath` category is kept (`KeepOnDeath = { Sword, Tool, KitGear }` in Config). Blocks, resources and consumables are lost. A player who is out loses everything.
4. **Kills** go up for the killer, and a **kill feed** entry is written (`FINAL` when the victim can't respawn).

### The Item Shop

The item shop keeper in each base opens `Client.Shop` (`MatchShop`). It never sells team upgrades.

**Listings** are built per player on the server, in layers; higher layers win:

| Layer | Source |
|---|---|
| 1. Default | `Classes.Shop` |
| 2. Mode | the mode's `Shop` field, and its rules' `ShopChanges(match, player)` |
| 3. Kit | each of the player's kits: the kit's `Shop` field, and its hook's `ShopChanges(player)` |
| 4. Command | `/shop add`, `remove` and `price` |

Each layer can add, remove or reprice entries, so taking a source away (like a kit) undoes exactly what it did. The finished listing goes to the player's own `MatchShop` store root.

- **Team colors:** `"{Team}"` in an entry's `Item` is the buyer's team name, so the one `Wool` entry sells each team its own color.
- **Once a match:** items whose `KeepOnDeath` category is in `OwnOnce` (tools) are sold once a match. Once owned or unlocked, the tile shows **Owned** and the server refuses it.
- **Buying:** one click selects an entry; a **double-click** (`DoubleClickWindow`, 0.4s), or the Purchase button, buys it. The window says what was bought or why not.

**Server checks** (`Server.Shop.Purchase`), in order: the entry is in the buyer's current listing; the match is in progress; the buyer is alive; they're within `ShopkeeperRange` of an **item shop keeper** (`RequireShopkeeper`); `RequiredKit`; `MaxOwned`; `OwnOnce`; every currency in the price; room in the inventory; `PurchaseRate`. Then the price is taken and the item is given **unlocked**. A failed give refunds the price.

### Team Upgrades

The upgrade keeper in each base opens `Client.Upgrades` (`MatchUpgrades`): one card per upgrade in the mode's `Upgrades`, ordered by `Order`, each with:

- its icon (`Icon`, or the `Glyph` emoji),
- every tier as `T1`, `T2`, `T3` with what it gives — a check on the tiers the team has, a lock on the rest,
- the next tier's price,
- a button: **BUY**, **NOT ENOUGH**, or **MAXED**. One click buys.

Upgrades are for the whole team. Levels are stored in the match store (`Teams[id].Levels`), shown in the tab list as icons with **roman numerals** (⚡ III), and applied by the mode's `OnUpgrade`. Buying needs an **upgrade keeper** within `ShopkeeperRange`.

Bedwars upgrades (`Classes.Upgrades`). Each tier describes the whole effect at that level:

| Upgrade | T1 | T2 | T3 | Effect today |
|---|---|---|---|---|
| Armor 🛡️ | 4 💎 +10% | 8 💎 +20% | 16 💎 +30% | Hook point |
| Damage ⚔️ | 5 💎 +5% | 10 💎 +10% | 20 💎 +20% | Hook point |
| Diamond Gen 💎 | 4 💎: diamonds every 30s | 8 💎: every 20s | 12 💎: every 15s | Team generators drop diamonds (`Adds`) |
| Team Gen ⚡ | 4 💎: +50% speed | 8 💎: +100% | 12 💎: +100% and emeralds every 40s | Team generators speed up (`Speed`, `Adds`) |

### Events

`Server.Events` builds a schedule when a match starts:

- **Timed** events fire at `At` seconds of play.
- **Random** events: for each `Window` the mode uses, one random time is picked inside it; at that time one event with that window is picked by `Weight`, skipping any on `Cooldown` or whose `Condition` is false. `Config.RandomSeed` repeats the same picks.

Firing an event plays the `MatchBanner` effect, sets its `Info` rows (shown in the tab list), pauses or resumes the timer if it says to, and calls its `Hook` in the mode's `Events` table. Events still to come are in the store's `Upcoming` list.

### Match HUD

| Element | Module | Shows |
|---|---|---|
| **Top bar** (`MatchTop`) | `Client.Hud` | The clock box (countdown, match time, respawning, "Bed destroyed") and one square per team: its color, alive players centred, and a bed icon that greys out when the bed is gone. An eliminated team's square turns grey (nothing says OUT). Your team is outlined |
| **Result** (`MatchResult`) | `Client.Hud` | The win or draw screen |
| **Kill feed** (`KillFeed`) | `Client.KillFeed` | Top right: killer, item icon, victim, in team colors, `FINAL` when the victim can't respawn. Entries fade |
| **Tab list** (`TabList`) | `Client.TabList` | Hold **Tab** (a Players button on touch). Teams in two columns: color, name, bed icon, upgrade icons with roman numerals, then each player's kit icon, name, 💀 (out) or "respawning", and kills. Then game info rows and upcoming events with countdowns. Roblox's player list is off |
| **Item shop** (`MatchShop`) | `Client.Shop` | See [The Item Shop](#the-item-shop) |
| **Upgrades** (`MatchUpgrades`) | `Client.Upgrades` | See [Team Upgrades](#team-upgrades) |
| **Spectating** | `Client.Spectate` | Who you're watching while out |

The templates live in `Match.Client.Gui`; restyle them there. `Match.Client.Ui` clones each into `StarterGui.Main` (or the match's own ScreenGui in a place without one).

### Match State

- **`ServerStore.Match`** (every client reads it): phase, server-time clock, `Players` (team, status, `Kills`, kit), `Teams` (status, `Info.Bed`, upgrade `Levels`), game `Info` rows, `Feed` (kill feed), `Upcoming` events, the last event.
- **`MatchShop`** (each player's own session root): their `Listing`.

Clients read both through `Match.Shared.State` (read-only), so every client's clock agrees. Banners and sounds go through `Classes.Effects`.

### Mode Rules

A mode's rules module (`Match.Server.Modes.<Rules>`). Every function is optional and gets the match (`Server.Core`) first:

| Rule | Purpose |
|---|---|
| `OnEnter(match, phase)` / `OnExit(match, phase)` | Phase changes |
| `Setup(match)` | Teams are filled; nobody has spawned yet |
| `SpawnFor(match, player) -> CFrame?` | Where a team player spawns |
| `PlatformCFrame(match) -> CFrame?` | Where the sky platform's floor goes |
| `SpectatorCFrame(match) -> CFrame?` | Where spectators float |
| `OnPlayerDied(match, player) -> number?` | Seconds until respawn, or `nil` for out |
| `OnPlayerSpawned(match, player, character)` | After a spawn |
| `OnBlockBroken(match, block, player?)` | A block was removed |
| `OnKitAssigned(match, player, kits)` | A player's kits changed |
| `OnTick(match, dt)` | While InProgress |
| `OnUpgrade(match, teamId, upgradeId, level)` | A team bought an upgrade |
| `ShopChanges(match, player) -> change?` | This player's mode layer of the shop |
| `JoinRule(match, player) -> "Spectate"` | A player joined mid-match |
| `AssignTeams(match, players) -> { [Player]: teamId }` | Custom team filling |
| `Cleanup(match)` | Resetting: undo what the mode made |
| `Events = { [hook] = function(match, event) }` | Event hooks |

**Hooks** — how the rest of the game tells the match what happened (`Match.Server().Hooks`). The match connects them itself: players through Roblox, `BlockBroken` through `BlockService.ObserveBroken`, `KitAssigned` through `KitState.ObserveKits`. They can also be called directly: `PlayerJoined`, `PlayerLeft`, `PlayerDied`, `PlayerSpawned(player, character)`, `BlockBroken(block, player?)`, `KitAssigned(player, kits)`.

### Match Settings

`Match.Shared.Config` (a mode's `Settings` and `Start` options override them):

| Setting | Default | Description |
|---|---|---|
| `MinPlayers` / `StudioMinPlayers` | `2` / `1` | Players needed to start (in Studio, 1) |
| `StartCountdown` | `10` | Seconds on the sky platform |
| `PlatformHeight` / `PlatformSize` | `120` / `48` | Platform height above spawn (when the mode doesn't place it) and size |
| `EndDuration` | `10` | Seconds the result shows |
| `LobbyRespawnDelay` / `RespawnDelay` | `3` / `5` | Respawn delays |
| `Paused` | `false` | Start matches with the timer paused |
| `RandomSeed` | `nil` | A number repeats the same random events |
| `KillCreditWindow` | `10` | Seconds a hit counts for kill credit |
| `AwardCurrencies` | `true` | The victim's currencies go to the killer |
| `KeepOnDeath` | `{ Sword, Tool, KitGear }` | Death categories kept, if unlocked |
| `OwnOnce` | `{ Tool }` | Death categories the shop sells once a match |
| `FeedSize` | `6` | Kill feed entries kept |
| `DoubleClickWindow` | `0.4` | Seconds between the clicks that buy |
| `RequireShopkeeper` / `ShopkeeperRange` | `true` / `16` | Buying needs the right keeper this close |
| `PurchaseRate` | `5` | Purchases per second |
| `CommandChangesPersist` | `false` | Keep `/shop` changes across resets (never saved) |
| `ChatCommand` | `"/shop"` | The admin chat command |

Bedwars' own settings (`Classes.Modes.Bedwars.Settings`): `MinPlayers = 2`, `RespawnDelay = 5`, `VoidDepth = 30`, `BedSpawnOffset = 6`.

---

## Admin Commands

Press **F2** in game to open the [Cmdr](https://eryn.io/Cmdr/) command bar. Only the user ids in `Classes.Admins` can run commands (checked by `Services.CmdrSetup.Hooks.BeforeRun`).

| Command | Alias | Arguments | Description |
|---|---|---|---|
| `give` | `giveitem` | `<players> <item> [amount]` | Give any item in `Classes.Items`, through `ItemService.Give` (as many as fit) |
| `givekit` | `kit` | `<players> <kit> [replace]` | Add a kit to the player's kits. `replace = true` removes their other kits first |
| `giveability` | `ability` | `<players> <ability>` | Give an ability without a kit. Only [grantable](#granted-abilities) abilities are listed |
| `setteam` | — | `<players> <team>` | Move players to a team in the running match |

Examples:

```text
give me "Blue Wool" 64
give me "Wooden Pickaxe"
give all Iron 50
givekit me Golem
givekit me Werewolf true
giveability me ChickenRush
setteam me Blue
```

- Item and kit names autocomplete. **Names with spaces need quotes.**
- The `item`, `kit` and `ability` types read `Classes.Items`, `Classes.Kits` and `KitState.Grantable()`, so new content shows up with no command changes.

**Adding a command:** put a definition module (`Name`, `Aliases`, `Description`, `Group`, `Args`) and a `<Name>Server` module returning `function(context, ...)` in `CmdrSetup.Commands`. New argument types go in `CmdrSetup.Types` as `function(registry)`. Types are registered before commands.

### The `/shop` chat command

Typed in chat by users in `Classes.Admins`, checked on the server. Replies go to the sender's chat.

| Command | Description |
|---|---|
| `/shop add <itemId> <currency> <price> [player]` | Add an entry, or set its price if it's listed |
| `/shop remove <itemId> [player]` | Remove an entry |
| `/shop price <itemId> <currency> <price> [player]` | Change one currency of a listed entry's price |
| `/shop list [player]` | Print a player's listing, or the base listing |
| `/shop clear [player]` | Undo `/shop` changes |

Without a player, a change is for everyone. Changes last until the match resets (unless `CommandChangesPersist`).

---

## HUD

| Element | `StarterGui.Main` | Shows | Driven by |
|---|---|---|---|
| **Hotbar** | `Hotbar` | 9 slots with icons and counts; the kit line (your kits' `Info` rows on one line); currency balances | Inventory, kit definitions, `Classes.Currencies` |
| **Inventory** | `Inventory` | The full grid (E) with item details and `Info` rows | Inventory, item definitions |
| **Ability bar** | `AbilityBar` | One round button per usable ability, with key label, cooldown and disabled state | `Core.Abilities` usable list + specs |
| **Custom UI** | any `<Element>` | Whatever your function draws | `CustomUI` tables (`Hud.KitUI`, `Hud.ItemUI`, ability specs) |
| **Health** | `Health` + billboards | Your health bar and health over other players | `Hud.PersonalHealth`, `Hud.HealthBillboards` |
| **Match HUD** | added at runtime | Top bar, kill feed, tab list, shop, upgrades, result, spectating | See [Match HUD](#match-hud) |

There are no side panels. Building has no popups: the hover outline, preview, placeholders and cracks are drawn by `Client.Blocks.BlockVisuals`.

### Info rows

Used by kit and item `Info` tables (`Hud.InfoRows`):

| Field | Type | Description |
|---|---|---|
| `Label` | `string` | Row label |
| `Text` | `(value) -> string` | Its text |
| `Visible` | `(value) -> boolean` | Hide the row when `false` |
| `Bar` / `Icon` / `Color` | | A fill (0 to 1), an image, and the bar color, where the row has room for them |

`value` is the kit's state snapshot (kit line) or an item `Context` (inventory details). A row whose function errors is hidden and warned once.

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

| Action | Keyboard | Gamepad |
|---|---|---|
| `Ability1` | `Q` | `X` |
| `Ability2` | `C` | `Y` |
| `Ability3` | `R` | `B` |
| `Ability4` | `B` | `LB` |
| `Ability5` | `G` | `RB` |
| Item click action / swing | `LMB` | `LT` |
| Sprint | `Left Shift` | `RT` |
| Hotbar slots | `1`–`9`, or click | — |
| Inventory | `E` | — |
| ProximityPrompts (shops, kit NPCs, cauldron…) | `F` | — |
| Tab list | hold `Tab` | — |
| Break (breaking tool held) | hold `LMB` | — |
| Place (block item held) | click or hold `LMB` | — |
| Command bar | `F2` | — |

- No two actions share a key: E is only the inventory, F only prompts.
- Kit abilities take slots first, in the order kits and their `Abilities` are listed; then granted abilities; then the held item's other abilities.
- The held item's **first** ability is its click action and has no slot.
- Touch players tap the ability bar and the hotbar.
- Passive abilities never appear on the bar.
- Block input is read only in `Client.Blocks.BlockInput`.

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
| `:HasAbility(player, abilityName) -> boolean` | Does any active kit, or a grant, give it |
| `:GrantAbility(player, abilityName) -> boolean` | Give a [grantable](#granted-abilities) ability without a kit. `false` if refused |
| `:RevokeAbility(player, abilityName)` | Take back a granted ability. Kit abilities stay |
| `:GiveItem(player, kitName, itemName)` | Give an item on behalf of a kit (removed with the kit) |
| `:GrantItems(player, kitName)` | Give the kit's missing items |
| `:ApplyStats(player)` | Apply the highest `MaxHealth` / `WalkSpeed` of the active kits |

#### `ItemService` — `Systems.Items.ItemService`

| Function | Description |
|---|---|
| `.Give(player, itemName, amount?, { Unlock = true }?) -> number` | Add items to free or matching slots. Returns how many fit. `Unlock` marks it unlocked for the match |
| `.Take(player, itemName, amount?, fromSlot?) -> boolean` | Take items. All or nothing |
| `.Consume(player, tool, amount?) -> boolean` | Take from the held Tool's slot |
| `.CanFit(player, itemName, amount?) -> boolean` | Would they fit |
| `.Clear(player, keep?)` | Empty the inventory, except slots where `keep(slot, index)` is true |
| `.ClearUnlocked(player)` | Forget this match's unlocks |
| `.Move(player, from, to, expected)` / `.Split(player, index, expected)` / `.Use(player, index, expected)` | What the client's slot requests run, after checking the slot holds `expected` |
| `.ToolFor(player, itemName) -> Tool?` | The hotbar Tool for an item |
| `.SlotOf(tool) -> number?` | A Tool's slot |
| `.SyncTools(player)` | Rebuild the hotbar Tools from the slots |

#### `AbilityService` — `Systems.Abilities.AbilityService`

| Method | Description |
|---|---|
| `:Use(player, abilityName, aim)` | Validate and run an ability |
| `:GetCooldown(player, abilityName) -> number` | Seconds left |
| `:SetCooldown(player, abilityName, seconds)` | Start or replace a cooldown (replicates to the client) |

#### `EffectService` — `Systems.Effects.EffectService`

| Function | Description |
|---|---|
| `.Play(name, options?)` | Send an effect to the clients its `Replicate` names. `Local` effects warn and are not sent |
| `.Stop(name, target?, data?)` | Stop an effect on every client, e.g. a persistent one. `data` is passed to the parts' stop functions |

#### `Combat` / `DamageLog` — `Systems.Combat`

| Function | Description |
|---|---|
| `Combat.ApplyHit(humanoid, damage, { Attacker?, Item?, ... }?)` | Damage, knockback and hit effects. Hits that name an `Attacker` are recorded for kill credit |
| `DamageLog.Record(humanoid, attacker?, itemName?)` | Record a hit |
| `DamageLog.Last(victim, window) -> (Player?, string?)` | The last attacker and item within `window` seconds |
| `DamageLog.Clear(victim)` | Forget who hit them |

#### `BlockService` — `Systems.Blocks.BlockService`

| Function | Description |
|---|---|
| `.Place(player, origin, turned) -> (boolean, reason?)` | Validate and place the held block with its lowest cell at `origin` |
| `.Remove(block, player?)` | Remove a block, running `OnBroken`, sending `Removed` and calling `ObserveBroken` listeners |
| `.Hit(player, cell)` | One break hit on the block filling `cell` |
| `.Get(key) -> Block?` | The block whose lowest cell has this key |
| `.All() -> { [key]: Block }` | Every block |
| `.ObserveBroken(fn) -> stop` | `fn(block, player?)` after any block is removed |
| `.Reset()` | Undo a round: placed blocks go, broken map blocks return, damage clears, `OnReset` runs |

`BlockService.Rules`:

| Function | Description |
|---|---|
| `.CanPlace(player, definition, origin, size) -> (boolean, lift?)` | Every placement check. `lift` is how far to raise the placer |
| `.InReach(player, origin, size, reach?) -> boolean` | Is the block within reach |
| `.OverlapsPlayer(origin, size, except?) -> boolean` | Is any other player in those cells |

#### `Claws` — `Systems.Werewolf.Claws`

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

#### `HackService` — `Systems.Hacker.HackService`

leo's satellite hack. One Hacker Connection per leo; from it, leo hacks one enemy team at a time until the connection breaks or they retarget. A hacked team pays `Inflation` (+25%) more at the shop (`DecorateListing`) and its generators run at `GeneratorRate` (85%). The extra is stored in the connection (`Settle`), collected by interacting with it, and dropped when it breaks. Tuning is in `Shared.SatelliteHackConfig`.

### Shared

#### `KitState` — `Shared.KitState`

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

> On the client, `player` must be the `LocalPlayer` — each client only receives its own state.

#### `Items` — `Shared.Items`

| Function | Description |
|---|---|
| `.Get(itemName)` | Definition, or `nil` |
| `.Of(tool)` | Definition for a Tool, or `nil` |
| `.Grants(tool, abilityName)` | Does the Tool's item grant the ability |
| `.Create(itemName)` | New Tool from the model (caller parents it) |
| `.Count(player, itemName)` | How many the player carries (reads `Inventory`) |
| `.WireAbilities(player, use)` | Client: clicking an item Tool calls `use(abilityName, tool)` |

#### `Inventory` — `Shared.Inventory`

| Member | Side | Description |
|---|---|---|
| `.SLOTS` / `.HOTBAR` / `.STACK_LIMIT` | both | `36` / `9` / `9999` |
| `.Slots(player)` | both | `{ { Item, Count } }`, `SLOTS` long |
| `.Count(player, itemName)` | both | Total over every slot |
| `.Observe(player, fn)` | both | `fn(slots)` now and on every change |
| `.IsUnlocked(player, itemName)` | both | Unlocked this match |
| `.MaxStack(itemName)` | both | `9999` for a Stack item, else `1` |
| `.KeepOnDeath(itemName)` | both | `"Sword"`, `"Tool"`, `"KitGear"` or `nil` |
| `.Write(player, slots)` / `.SetUnlocked(player, itemName?)` | server | Low-level writes. Use `ItemService` instead |

#### `Blocks` — `Shared.Blocks`

| Function | Description |
|---|---|
| `.Get(name)` / `.ById(id)` / `.All()` | Definitions |
| `.Of(tool)` | The block a held block item places, or `nil` |
| `.ToolOf(tool)` | How a held item breaks blocks. `nil` = empty hand |
| `.BreakTime(definition, tool)` | Seconds to break, or `nil` if the tool can't |
| `.CellOf(position)` / `.CenterOf(cell)` | World ↔ cell |
| `.Key(cell)` / `.FromKey(key)` | Cell ↔ `"x,y,z"` |
| `.SizeOf(definition, turned?)` | Size in cells, turned a quarter turn if `true` |
| `.Cells(origin, size)` | Every cell a block fills |
| `.Bounds(origin, size)` | Center CFrame and size in studs |
| `.FootprintOf(instance)` | Origin and size of a map part or model |
| `.DistanceTo(position, origin, size)` | Studs from a point to the closest point of a block |
| `.LiftOnto(character, origin, size)` | How far a character must rise to stand on a block |
| `.Touches(origin, size, filled)` | Does a block touch a filled cell |
| `.InBuildArea(origin, size)` | Does it fit in a `BUILD_AREAS` box |

#### `ToolTypes` — `Shared.ToolTypes`

| Member | Description |
|---|---|
| `.KINDS` | Every tool kind and whether it breaks blocks |
| `.HAND` | The empty-hand tool |
| `.Of(definition, itemName?)` | An item's tool (`ToolType`, `Speed`, `CanBreakBlocks`). Errors on bad fields |

#### `BlockState` — `Shared.BlockState`

| Function | Side | Description |
|---|---|---|
| `.Damage(key) -> number` | both | Break progress, 0 to 1 |
| `.SetDamage(key, damage)` | server | Set it. `0` clears it |
| `.Observe(fn)` | both | `fn({ [key]: damage })` now and on every change |

#### `ReadOnly` — `Shared.ReadOnly`

| Function | Description |
|---|---|
| `.Wrap(node, label)` | A read-only view of a Scribe accessor. Any write errors with `label` |

### Client

#### `Abilities` — `Client.Core.Abilities`

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

#### `Inputs` — `Client.Core.Inputs`

| Member | Description |
|---|---|
| `:GetKeyLabel(slot?) -> string` | Key text for a slot on the current device (`nil` = click action) |

#### `Effects` — `Client.Effects`

| Function | Description |
|---|---|
| `.Play(name, options?) -> Handle?` | Play an effect on this client. `nil` if the name isn't in the registry |
| `.Stop(name, target?, data?)` | Stop every running copy of an effect on a target |
| `handle:Stop(data?)` | Stop one play |

#### `AudioSettings` — `Client.Audio.AudioSettings`

| Member | Description |
|---|---|
| `.Get(group) -> number` | A group's volume, 0 to 1. `"Master"` is a group name too |
| `.Set(group, volume)` | Set and save a group's volume. Heard right away |
| `.GetAll() -> { [string]: number }` | Every group's volume, including Master |
| `.Changed` | Signal: `(group, volume)` |

#### `SoundGroups` — `Client.Audio.SoundGroups`

| Member | Description |
|---|---|
| `.Get(name?) -> SoundGroup` | A group by name. Unknown names warn once and return `Effects` |
| `.Assign(sound, name?)` | Put a sound in a group |
| `.Master() -> SoundGroup` | The Master group (created with its children if missing) |
| `.NAMES` / `.DEFAULT` | The child group names / the default group |

#### HUD — `Client.Hud`

| Member | Description |
|---|---|
| `Hotbar.Use(index)` | Use a hotbar slot (what keys 1–9 do) |
| `InventoryUI.Open()` / `.Close()` / `.IsOpen()` | The inventory window |
| `ItemIcon.Draw(frame, itemName, image?)` | Draw an item's icon into a frame |

#### Blocks — `Client.Blocks`

| Module | Job |
|---|---|
| `BlockMap` | The client's occupancy map, from `Snapshot`, `Placed` and `Removed`. `At(cell)`, `Get(key)`, `IsFree(origin, size)`, `InstanceOf(key)` |
| `BlockInput` | Turns the mouse into break and place actions |
| `Targeting` | The hovered block and the predictive placement cell |
| `BlockVisuals` | Hover outline, placement preview, placeholders and cracks |
| `BlockController` | Runs every frame: targeting, preview, sending requests, client hooks |
| `GeneratorBillboards` | Fills in generator billboards from their `Drops` and `TeamColor` attributes |

### Match

#### `Match` — `ReplicatedStorage.Match`

| Function | Side | Description |
|---|---|---|
| `.Start(modeName, options?) -> Core` | server | Start the match system in a mode |
| `.Server() -> Core?` | server | The running `Server.Core` |
| `.StartClient()` | client | Called by `ClientLoader` |
| `.OpenShop(source?)` | client | Open the item shop. Closes when the player walks away from `source` |
| `.OpenUpgrades(source?)` | client | Open the team upgrades window |

#### `Core` — `Match.Server().*`

| Function | Description |
|---|---|
| `.Phase()` / `.Elapsed()` | Current phase / seconds of play |
| `.Setting(name)` | A setting: Config, overridden by the mode's `Settings`, overridden by `Start` options |
| `.Status(player)` | `Lobby`, `Alive`, `Dead`, `Out` or `Spectating`, or `nil` |
| `.TeamOf(player)` / `.PlayersOn(teamId)` / `.Members()` | Teams and players |
| `.TeamIds()` / `.Team(teamId)` / `.TeamObject(teamId)` / `.TeamIdOf(team)` / `.TeamStatus(teamId)` | Team lookups |
| `.TeamLevel(teamId, upgradeId)` | A team's upgrade level |
| `.BuyUpgrade(player, upgradeId, level)` | Raise the player's team's upgrade and run `OnUpgrade` |
| `.SetInfo(key, label?, text?, order?)` | A game info row (tab list) |
| `.SetTeamInfo(teamId, key, text?)` | A team info value (e.g. `Bed`) |
| `.MoveToTeam(player, team)` | Move a player (the `setteam` command) |
| `.Spawn(player)` | Spawn a player where they belong |
| `.Pause()` / `.Resume()` | The match timer |
| `.Changed()` | Publish state changes |
| `.Hooks` | `PlayerJoined`, `PlayerLeft`, `PlayerDied`, `PlayerSpawned`, `BlockBroken`, `KitAssigned` |

#### `State` — `Match.Shared.State`

| Function | Description |
|---|---|
| `.Get()` | A snapshot of the match: `Phase`, `Players`, `Teams`, `Info`, `Feed`, `Upcoming`… |
| `.Elapsed(snapshot?)` / `.Remaining(snapshot?)` | Seconds of play / left in the countdown, from server time |
| `.PlayerEntry(player, snapshot?)` | The player's entry in `Players` |
| `.ShopRoot(player)` / `.Listing(player)` | The player's shop root / listing (on a client, only the local player's) |

---

## Packets

All packets live in `Shared.Packets` (the match's in `Match.Shared.Packets`).

| Packet | Direction | Payload | Purpose |
|---|---|---|---|
| `Effects.Play` | S → clients | `name, options` | Play an effect (All or Nearby clients) |
| `Effects.Stop` | S → all | `name, { Target, Data }` | Stop an effect |
| `Abilities.Use` | C → S | `name, x, y, z` | Use any kit or item ability |
| `Items.Equip` | C → S | `tool` | Equip a Backpack Tool on the server |
| `Items.Unequip` | C → S | — | Put away the held Tool |
| `Items.MoveSlot` | C → S | `from, to, item` | Move a slot's items onto another slot (merge or swap) |
| `Items.SplitSlot` | C → S | `slot, item` | Split half a stack into the first empty slot |
| `Items.UseSlot` | C → S | `slot, item` | Use a hotbar slot (equip or put away) |
| `Blocks.Sync` | C → S | — | Ask for the snapshot, once listening |
| `Blocks.Snapshot` | S → C | `{ { Key, Id, Size } }` | Every block |
| `Blocks.Placed` | S → synced | `{ Key, Id, Size }` | A block was placed |
| `Blocks.Removed` | S → synced | `key` | A block was removed |
| `Blocks.Place` | C → S | `cell, turned` | Place the held block |
| `Blocks.Rejected` | S → C | `cell` | The server refused that placement; drop its placeholder |
| `Blocks.Hit` | C → S | `cell` | One break hit |
| `Blocks.Interacted` | S → C | `key` | Run the block's client `OnInteract` |
| `Combat.Hit` | S → all | `character, damage` | Hit feedback (damage popups, health bars) |
| `Hacker.OpenConnection` | S → C | `key` | Open leo's connection panel |
| `Werewolf.Rest` | C → S | `boolean` | Set resting directly (wake on move) |
| `Werewolf.HuntTargets` | S → C | `tool, { targets }, expires` | Highlight hunt targets |
| `Golem.ConsumeStone` | C → S | `stone` | Eat an ancient stone |
| `Samurai.Charge` | C → S | `boolean` | Begin (`true`) or cancel (`false`) a dash charge |
| `Cauldron.BrewingState` | C → S | `cauldron, holding` | Brew prompt held |
| `Match.Purchase` | C → S | `entryId` | Buy an entry from the player's own listing (items or upgrades) |
| `Match.PurchaseResult` | S → C | `entryId, reason` | `""` when bought, or why not |
| `Match.Message` | S → C | `text` | A line for the player's chat (e.g. `/shop` replies) |

`Shared.UnreliablePackets` holds `FootPrint` on an UnreliableRemoteEvent. Cmdr uses its own `CmdrFunction` / `CmdrEvent` remotes.

> Always require `Shared.Packets` — never call `Packet("Name", ...)` from the command bar. A second copy of the packet library can't decode the real one's traffic.

---

## Built-in Content

### Kits

| Kit | Items | Abilities | State | HUD |
|---|---|---|---|---|
| Animal Whisperer | — | ChickenRush, OwlVision; passive Turtle Shield | — | — |
| Barbarian | Wooden Sword | Rage *(passive)* | `Rage`, `SwordLevel` | Custom UI: `Rage`; shop changes |
| Golem | — | RockThrow | `Rocks`, `Scale` | Info: Rocks, Size |
| leo | — | SatelliteHack | `ConnectionOwned`, `Earnings`, `HackActive`, `HackEndsAt`, `StoredResources`, `TargetTeam` | Info: Stored, Connection, Target, Hack, Earned; Custom UI: `SatelliteTargets`; can buy Hacker Connection |
| Samurai | Wooden Sword | Dash | `Charging`, `ChargeStartedAt` | Dash's custom UI: `DashCharge` |
| Scientist | — | Brew *(passive)* | — | — |
| Stew Boy | — | SummonCauldron, Brew *(passive)* | — | Shop changes |
| Werewolf | Werewolf Claws | Rest, Hunt | `MoonCharge`, `Resting`, `RestStartedAt`, `HuntingUntil`, `Transformed`, `Transforming`, `Combo` | Info: Moon, Bonus, Lifesteal, Charge, Hunting |

- **Turtle Shield** (Animal Whisperer, `Systems.AnimalWhisperer.TurtleShield`): blocks 2 hits, and recharges after 20 seconds without hits while broken.
- **leo**: buys and places one Hacker Connection (3 Emeralds), then hacks one enemy team at a time: their shop costs +25% and their generators run 15% slower. Taxed resources are stored in the connection; interact to collect. Breaking it ends the hack and drops what it stored.

### Items

| Item | Abilities | Notes |
|---|---|---|
| Wooden / Stone / Iron / Diamond Sword, Rageblade | Slash | `Damage` 10–30, `Cooldown`; `ToolType = "Sword"`, can't break blocks; `KeepOnDeath = "Sword"`; Rage upgrades through these |
| Wooden Pickaxe / Axe / Shovel | — | `ToolType`, `Speed = 1`, `CanBreakBlocks = true`; `KeepOnDeath = "Tool"` (sold once a match) |
| Red / Blue / Purple / Green Wool, Wood, Planks, Stone, Dirt, Concrete, Black Stone | — | Block items: `Block`, `Stack` |
| Bed, Shop Keeper | — | Block items for the special blocks |
| Hacker Connection | — | leo's block: `RequiredKit = "leo"`, `MaxOwned = 1`, `KeepOnDeath = "KitGear"` |
| Iron, Diamond, Emerald | — | Currencies: `Stack`. Dropped by generators, spent at the shop |
| Fire / Poison / Speed / Shock Capsule | Throw | `Capsule` effect; `Brewed` |
| Meat, Ham | Consume | `HealAmount` 25 / 50; `Brewed` |
| Eye | Consume | `RevealDuration` 25; `Brewed` |
| Werewolf Claws | Claw | Hook: `WerewolfClaws`; `KeepOnDeath = "KitGear"` |

### Abilities

| Ability | Granted by | Type | Cooldown | Grantable |
|---|---|---|---|---|
| Rage | Barbarian | Passive | — | ❌ |
| Brew | Scientist, Stew Boy | Passive (unlocks the cauldron) | — | ✅ |
| RockThrow | Golem | Hold to aim, release to throw | 5s after a throw | ✅ |
| ChickenRush | Animal Whisperer | Tap: a chicken stampede, 35 damage per target | 8s | ✅ |
| OwlVision | Animal Whisperer | Tap: reveals enemies through walls for 12s | 35s | ✅ |
| SatelliteHack | leo | Pick an enemy team to hack (needs a placed Hacker Connection) | — | ✅ |
| Rest | Werewolf | Tap | 0.5s | ❌ |
| Hunt | Werewolf | Tap (full moon only) | Hunt duration + 45s | ❌ |
| Dash | Samurai | Hold to charge (or RMB), release to dash | 0.4s | ❌ |
| SummonCauldron | Stew Boy | Tap | 1s | ✅ |
| Slash | Swords | Click | Sword `Cooldown` | ❌ |
| Throw | Capsules | Click | 0.3s | ❌ |
| Claw | Werewolf Claws | Click | 0.55s (faster while hunting) | ❌ |
| Consume | Meat, Ham, Eye | Click | 0.3s | ❌ |

### Blocks

| Id | Block | Hardness | Preferred tool | Breakable | Placeable | Size | Hook |
|---|---|---|---|---|---|---|---|
| 1 | MapBlock | — | — | ❌ | ❌ | 1×1×1 | — |
| 2–5 | Red / Blue / Purple / Green Wool | 0.8 | any | ✅ | ✅ | 1×1×1 | — |
| 6 | Wood | 2 | Axe | ✅ | ✅ | 1×1×1 | — |
| 7 | Planks | 1.5 | Axe | ✅ | ✅ | 1×1×1 | — |
| 8 | Stone | 3 | Pickaxe | ✅ | ✅ | 1×1×1 | — |
| 9 | Dirt | 1 | Shovel | ✅ | ✅ | 1×1×1 | — |
| 10 | Grass | 1.2 | Shovel | ✅ | ❌ | 1×1×1 | — |
| 11 | Soil | 1 | Shovel | ✅ | ❌ | 1×1×1 | — |
| 12 | Concrete | 4 | Pickaxe | ✅ | ✅ | 1×1×1 | — |
| 13 | Black Stone | 6 | Pickaxe | ✅ | ✅ | 1×1×1 | — |
| 20 | Bed | 2 | any | ✅ | ❌ | 2×1×1 | Bed |
| 21 | Shop Keeper | — | — | ❌ | ✅ | 2×2×1 | ShopKeeper (`Shop = "Items"`) |
| 22 | Iron Generator | — | — | ❌ | ❌ | 1×2×1 | Generator: Iron every 1.5s, up to 100 |
| 23 | Diamond Generator | — | — | ❌ | ❌ | 1×2×1 | Generator: Diamond every 30s, up to 10 |
| 24 | Emerald Generator | — | — | ❌ | ❌ | 1×2×1 | Generator: Emerald every 60s, up to 4 |
| 25 | Hacker Connection | 3 | Pickaxe | ✅ | ✅ (leo) | 1×2×1 | HackerConnection |
| 26 | Upgrade Keeper | — | — | ❌ | ❌ | 2×2×1 | ShopKeeper (`Shop = "Upgrades"`) |

### Match Content

**Bedwars** (`Classes.Modes.Bedwars`): teams Red, Blue, Green and Purple; upgrades Armor, Damage, Diamond Gen and Team Gen; starting item Wooden Sword; events Diamonds II (10:00), Sudden Death (20:00), and Iron Rush or Low Gravity between 3:00 and 6:00.

**Currencies**: Iron, Diamond, Emerald.

**Default shop** (`Classes.Shop`):

| Category | Entries |
|---|---|
| Blocks | Wool (your team's color) ×16 — 8 Iron; Planks ×12 — 24 Iron; Stone ×12 — 32 Iron; Concrete ×8 — 24 Iron; Black Stone ×4 — 2 Emerald |
| Combat | Stone Sword — 20 Iron; Iron Sword — 70 Iron; Diamond Sword — 4 Emerald |
| Tools | Wooden Pickaxe, Wooden Axe, Wooden Shovel — 10 Iron each (once a match) |
| Items | Meat — 6 Iron |

### Effects

| Effect | Group | Replicate | Parts | Played by |
|---|---|---|---|---|
| `Hit` | Effects | All | Sound, Highlight, Particles | `Combat.ApplyHit` |
| `SwordSwing` | Abilities | Nearby 200 | Sound, Particles | `SwordCombat:Attack` |
| `SwordUpgrade` | Abilities | All | Sound | `Rage.Gain` |
| `SwordSlash` | Effects | Local | Animation (2 Variants) | `Client.Abilities.Library.Slash` |
| `WerewolfClawSwing` | Abilities | Nearby 300 | ClawSwing, Sound (3 Variants) | `Claws.Attack` |
| `WerewolfSleep` | Abilities | All, persistent | Sound, SleepSymbols | `Claws` rest |
| `WerewolfTransform` | Effects | All | ColorFade | `Claws` transform |
| `WerewolfTransformHowl` | Abilities | All | Sound (global) | `Claws` transform |
| `WerewolfHuntHowl` | Abilities | Nearby 150 | Sound | `Claws.Hunt` |
| `GolemThrow` | Effects | Nearby 300 | JointSwing | `Rocks.Throw` |
| `GolemShatter` | Effects | Nearby 300 | Shards | `Rocks.Throw` impact |
| `CapsuleSplash` | Effects | All | Template (4 Variants) | `Capsules:Throw` landing |
| `SamuraiCharge` | Effects | All, persistent | SamuraiPose | `SwordPose.Begin` |
| `SamuraiRelease` | Effects | All | SamuraiPose | `SwordPose.Release` |
| `ChickenRush` | Abilities | All | Sound, ChickenRush | ChickenRush ability |
| `SatelliteHack` | Abilities | All | Satellite | `HackService` |
| `SatelliteHackWarning` | UI | All | HackWarning | `HackService` |
| `BlockPlace` | Effects | Nearby 150 | Sound (Variant per `SoundCategory`) | `BlockService.Place` |
| `BlockBreak` | Effects | Nearby 150 | Shards, Sound (Variant per `SoundCategory`) | `BlockService.Remove` |
| `BlockHit` | Effects | Nearby 80 | Sound (Variant per `SoundCategory`) | `BlockService.Hit` |
| `GeneratorSpawn` | Effects | Nearby 80 | Sound | Generator hook |
| `MatchBanner` | UI | All | Sound, Banner | Match start and events |
| `BedDestroyed` | UI | All | Sound, Banner | Bedwars |
| `TeamEliminated` | UI | All | Sound, Banner | `Server.Core` |
| `MatchWin` | UI | All | Sound, Banner | `Server.Core` |
| `PlayerKilled` | Effects | Nearby 250 | Sound | `Server.Core` deaths |
| `ShopPurchase` / `ShopDenied` | UI | Local | Sound | Shop and upgrades windows |
| `InventoryOpen` / `InventoryClose` / `InventoryMove` | UI | Local | Sound | `Hud.Inventory` |
| `TabListOpen` | UI | Local | Sound | `Client.TabList` |
| `ButtonHover` / `ButtonClick` | UI | Local | Sound | `Packages.UI.ButtonHover` |
| `Music` | Music | Local | Sound | `Client.Core.Music` |

---

## Notes & Gotchas

- **Equips go through the server.** Client-side `Humanoid:EquipTool` doesn't replicate in this place, so hotbar use goes through `Items.UseSlot` (and `Client.Core.ToolSync` sends `Items.Equip` / `Items.Unequip`) and the server equips for real. Without it, the server sees empty hands and refuses item abilities.
- **Item abilities need the item held on the server.** If an item ability "does nothing", check that the server's character has the Tool, not just the client's.
- **Kit state, inventory, unlocks and granted abilities are session data.** They reset when the player leaves. Persisted data belongs elsewhere in the Scribe template.
- **Block damage and match state are server data.** They live in Scribe's `ServerStore` (one per server, never saved, replicated to everyone). The Scribe package was **patched** to accept the `ServerStore` option — re-apply the patch if you update Scribe.
- **Client Scribe views are wrapped by `Shared.ReadOnly`.** Scribe lets a client write its own mirror; the wrapper makes those writes error instead of silently diverging.
- **Scribe field names can't be accessor names.** A slot's count is stored as `Quantity`, not `Count`, for this reason; `Shared.Inventory` maps it back to `Count`.
- **ModuleLoader calls `Init` and `Start` on every module** whose ancestors are all Folders. Helper modules that shouldn't start on their own use another name (e.g. `BlockVisuals.Build`). Use the `ClientOnly`, `ServerOnly` and `IgnoreLoader` attributes to control loading.
- **Packets wait for loaded clients.** Effects go only to players with `_ModulesLoaded`, and block packets only to clients that sent `Blocks.Sync`. Sending earlier causes decode errors at join.
- **Map blocks can stream out.** `StreamingEnabled` is on, so the client's `BlockMap` never depends on instances. Use `BlockMap.InstanceOf(key)` when you need the part.
- **Overlapping map blocks are skipped.** On start the server warns with a count of map blocks that overlap another. Light-source parts are untagged so they don't hide generators.
- **Every base needs its keepers.** Each base has an item shop keeper and an upgrade keeper (map blocks with `BlockType` `ShopKeeper` / `UpgradeKeeper`). A base without one can't buy there.
- **Billboards can't show 3D views.** ViewportFrames don't render inside a BillboardGui, so generator billboards need an item `Image` for a real picture (a colored badge until then).
- **F does nothing in a Studio play test?** Studio's "Respect Studio shortcuts when game has focus" setting lets Studio's own F shortcut (Zoom To) take the key. Turn it off in File → Studio Settings → Studio. Players in Roblox are not affected.
- **Knockback vs. reach.** Sword hits knock targets ~2 studs back; the sword reaches 7 studs, so keep moving forward in a fight.
- **Custom UI starts hidden.** Elements named in any `CustomUI` table are hidden when the HUD starts, then shown only while in use.
- **Multiple kits.** Stats take the highest value; appearances apply in list order; abilities fill slot keys in order.
- **Gameplay stays on the server.** Body-scale growth (Werewolf moon, Golem rocks, the hunt), the werewolf lunge, knockback, the thrown capsule and boulder, generator drops and resource drops are gameplay, so the server runs them. Only cosmetic effects run on clients.
- **Capsule puddles have no server part.** The server keeps a `{ Position, Radius, Expires }` table for damage and speed; clients draw the puddle with `CapsuleSplash`. The puddle timings (5s fade delay, 2s fade, 7s lifetime) are in both `Capsules` and the registry — change both together.
- **Late joiners miss running effects.** A player who joins while a persistent effect is running (a sleeping werewolf, a charging Samurai) won't see it until it plays again.
- **Claws are shown by the client.** The server keeps claw parts hidden; `ClawSwing` shows them locally during a swipe, using each part's `VisibleTransparency` attribute (set by the server for the hunt look).
- **Armor and Damage upgrades are hook points.** They're sold and shown, but nothing applies them in combat yet (`Bedwars.OnUpgrade`). The `DiamondsII` and `IronRush` events are hook points too.
- **Not yet tested with several players.** Building, the shop, upgrades and the match flow are verified in single-player play tests; four-team matches, kill credit between real players and multi-client bridging still need a test.
