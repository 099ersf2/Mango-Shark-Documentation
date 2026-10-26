# Kits, Abilities & Items

A data-driven framework for kits, abilities, items and effects in a Roblox game.

- **Definitions:** kits and items are plain definition modules. Abilities are small server modules with optional client specs. Effects are entries in one registry.
- **Kit state:** all player kit state lives in a shared [Scribe](https://scribe.ericplane.dev/) store. The server writes it and the client reads it.
- **HUD:** the HUD builds itself from the definitions, so adding content never requires editing HUD code.
- **Effects:** the server never creates sounds or visuals. It sends an effect name, and every client plays it.

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
- [Guides](#guides)
  - [Adding a Kit](#adding-a-kit)
  - [Adding an Item](#adding-an-item)
  - [Adding an Ability](#adding-an-ability)
  - [Adding an Effect](#adding-an-effect)
  - [Custom UI](#custom-ui)
  - [Setting a Player's Kits](#setting-a-players-kits)
- [Effects & Sound](#effects--sound)
  - [Effect Registry](#effect-registry)
  - [Playing Effects](#playing-effects)
  - [Replication](#replication)
  - [Sound Groups](#sound-groups)
  - [Volume Settings](#volume-settings)
  - [Writing a New Visual Kind](#writing-a-new-visual-kind)
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
| **Effect** | A named sound, visual and/or animation, played on clients | `Classes.Effects` (registry) + `Client.Effects` (player) |

Key rules:

- **Kit abilities** are granted by a player's active kits.
- **Item abilities** are granted by the **held** item, and work with **no kit equipped**.
- A player can have **several kits at once**.
- The server is the only writer of kit state. The client's view is **read-only** and errors on writes.
- The server **never** creates, plays or tweens effects. It calls `EffectService.Play`, and clients play the effect.
- Every client sound sits in a **sound group** under `SoundService.Master`.

---

## Project Layout

```text
ReplicatedStorage
├── Assets
│   ├── Sounds                        Effect sounds (Hit, Swing, SwordUpgrade, Werewolf…)
│   ├── Vfx                           Particle Attachments (HitFX, SwingR, SwingL, Heal)
│   ├── Music/Primary                 Background songs
│   └── Models
│       ├── Items/<Item>              Tool models, named after the item definition
│       ├── CapsuleSplashModels       Capsule puddle parts (Fire/Poison/Speed/ShockSplash)
│       └── GolemBoulder
├── Inputs
│   └── Default                       InputContext: Ability1–Ability5 slot keys
└── Modules
    ├── Classes
    │   ├── Kits/<Kit>                Kit definitions
    │   ├── Items/<Item>              Item definitions
    │   ├── Effects                   Effect registry: every sound and visual
    │   └── SwordLevels               Barbarian rage levels
    ├── Shared
    │   ├── Data                      Scribe template (Kits + Abilities session roots)
    │   ├── KitState                  Active kits and kit state
    │   ├── Items                     Item helper (definitions + item ability wiring)
    │   └── Packets                   Every network packet
    ├── Handlers
    │   └── AnimationHandler          Loads and tracks animations (used by the Animation part)
    └── Client
        ├── Core
        │   ├── Abilities             Client ability framework
        │   ├── Inputs                Slot keys and key labels
        │   ├── Music                 Background music (plays through the Music effect)
        │   └── ToolSync              Server-side equip sync
        ├── Effects                   Client effect player: Play / Stop
        │   ├── Context               One playing effect: placement, timing, cleanup
        │   └── Parts/<Kind>          Sound, Animation and visual parts
        ├── Audio
        │   ├── SoundGroups           Group lookup and assignment
        │   └── AudioSettings         Group volumes (Store = saved values)
        ├── Abilities/Library/<Ability>   Client ability specs
        ├── Hud
        │   ├── KitPanel              Kit information panel
        │   ├── AbilityBar            Ability buttons
        │   ├── ItemPanel             Held item information panel
        │   ├── InfoRows              Shared row renderer
        │   └── CustomUI              Hand-made UI support
        ├── Kits/<Kit>                Kit-only client code (overlays, highlights)
        └── Items/<Item>              Item-only client code (aim arcs)

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
        ├── Abilities
        │   ├── AbilityService        Validates and runs ability requests
        │   └── Library/<Ability>     Server ability modules
        ├── Effects
        │   └── EffectService         Sends effects to clients
        └── Werewolf
            ├── Appearance            Claw models, werewolf body and head
            └── Claws                 Overview + Config, Session, Rest, Moon, Hunt,
                                      Attack, Lunge, Hit, Effects

SoundService
└── Master                            Master sound group
    ├── Music
    ├── Abilities
    ├── Effects
    ├── UI
    └── Ambient

StarterGui
└── Main
    ├── KitPanel                      Kit info panel  (restyle via its Templates folder)
    ├── AbilityBar                    Ability bar     (restyle via its Templates folder)
    ├── ItemPanel                     Item info panel (restyle via its Templates folder)
    ├── Rage                          Custom UI for the Barbarian
    └── DashCharge                    Custom UI for the Dash ability

ServerStorage
├── README                            In-Studio copy of these docs (disabled Script)
├── WerewolfClaws                     Claw and eye models (server welds them on)
├── UIBackup                          Backups of the original UI
└── EffectsBackup_2026_10_25          Scripts and assets from before the effects rework
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
4. **Add its effects** — see [Adding an Effect](#adding-an-effect).
5. **Add kit-only client code** *(optional)* — `Client.Kits.Ninja/...`

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

3. **Grant it** by listing it in a kit's or item's `Abilities`.

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
| `Variants` | `{ [any]: fields }` | — | Fields that replace the ones above when played with that `Variant` (e.g. a combo step or capsule type) |

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
| `Shards` | `Count`, `Size = { min, max }`, `Color`, `Material`, `Time`, `Lifetime` | Small parts that fly out and fade |
| `JointSwing` | `Joint`, `Keys = { { At, Time, Angles } }` | Swings one joint through rotations (degrees from rest) |
| `ClawSwing` | — | The werewolf combo swipe. `Variant` = combo step, `Speed` = attack speed, `Tool` = claws |
| `SleepSymbols` | `Interval`, `MaxDistance` | Zs rising from the head until stopped |
| `ColorFade` | `Time` | Fades body parts using `Data.Colors = { [partName] = { From, To } }` |
| `SamuraiPose` | `Phase = "Charge" \| "Release"` | IK sword pose. `Tool` = sword. Stop with `{ Instant = true }` to snap back |

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
| `Nearby` | Clients whose character is within `Range` studs | `SwordSwing` (200), `WerewolfClawSwing` (300), `WerewolfHuntHowl` (150), `GolemThrow` (300), `GolemShatter` (300) |
| `Local` | Not sent — only the client plays it | `SwordSlash`, `ButtonHover`, `ButtonClick`, `Music` |

Why each one:

- **All:** persistent effects and effects with gameplay meaning (players must see a capsule puddle to avoid it).
- **Nearby:** short sounds and motion that can't be seen or heard much further away.
- **Local:** the owner's own animations (they replicate through the Animator), UI sounds and music.

### Sound Groups

```text
SoundService
└── Master
    ├── Music        background music
    ├── Abilities    ability sounds: swings, claw swipes, howls, snore
    ├── Effects      hits and impacts (also the default group)
    ├── UI           button hover and click
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

#### `EffectService` — `Systems.Effects.EffectService`

| Function | Description |
|---|---|
| `.Play(name, options?)` | Send an effect to the clients its `Replicate` names. `Local` effects warn and are not sent |
| `.Stop(name, target?, data?)` | Stop an effect on every client, e.g. a persistent one. `data` is passed to the parts' stop functions |

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

---

## Packets

All packets live in `Shared.Packets`.

| Packet | Direction | Payload | Purpose |
|---|---|---|---|
| `Effects.Play` | S → clients | `name, options` | Play an effect (All or Nearby clients) |
| `Effects.Stop` | S → all | `name, { Target, Data }` | Stop an effect |
| `Abilities.Use` | C → S | `name, x, y, z` | Use any kit or item ability |
| `Items.Equip` | C → S | `tool` | Equip a Backpack Tool on the server |
| `Items.Unequip` | C → S | — | Put away the held Tool |
| `Combat.Hit` | S → all | `character, damage` | Hit feedback (damage popups, health bars) |
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

### Effects

| Effect | Group | Replicate | Parts | Played by |
|---|---|---|---|---|
| `Hit` | Effects | All | Sound, Highlight, Particles | `Combat.ApplyHit` |
| `SwordSwing` | Abilities | Nearby 200 | Sound, Particles | `SwordCombat:Attack` |
| `SwordUpgrade` | Abilities | All | Sound | `Rage.Gain` |
| `SwordSlash` | — | Local | Animation (2 Variants) | `Client.Abilities.Library.Slash` |
| `WerewolfClawSwing` | Abilities | Nearby 300 | ClawSwing, Sound (3 Variants) | `Claws.Attack` |
| `WerewolfSleep` | Abilities | All, persistent | Sound, SleepSymbols | `Claws` rest |
| `WerewolfTransform` | — | All | ColorFade | `Claws` transform |
| `WerewolfTransformHowl` | Abilities | All | Sound (global) | `Claws` transform |
| `WerewolfHuntHowl` | Abilities | Nearby 150 | Sound | `Claws.Hunt` |
| `GolemThrow` | — | Nearby 300 | JointSwing | `Rocks.Throw` |
| `GolemShatter` | — | Nearby 300 | Shards | `Rocks.Throw` impact |
| `CapsuleSplash` | — | All | Template (4 Variants) | `Capsules:Throw` landing |
| `SamuraiCharge` | — | All, persistent | SamuraiPose | `SwordPose.Begin` |
| `SamuraiRelease` | — | All | SamuraiPose | `SwordPose.Release` |
| `ButtonHover` / `ButtonClick` | UI | Local | Sound | `Packages.UI.ButtonHover` |
| `Music` | Music | Local | Sound | `Client.Core.Music` |

---

## Notes & Gotchas

- **Equips go through the server.** Client-side `Humanoid:EquipTool` (used by custom hotbars like NeoHotbar) doesn't replicate in this place, so `Client.Core.ToolSync` sends `Items.Equip` / `Items.Unequip` and the server equips for real. Without it, the server sees empty hands and refuses item abilities.
- **Item abilities need the item held on the server.** If an item ability "does nothing", check that the server's character has the Tool, not just the client's.
- **Kit state is session data.** It resets when the player leaves. Persisted data belongs elsewhere in the Scribe template.
- **Knockback vs. reach.** Sword hits knock targets ~2 studs back; the sword reaches 7 studs, so keep moving forward in a fight.
- **Custom UI starts hidden.** Elements named in any `CustomUI` table are hidden when the HUD starts, then shown only while in use.
- **Multiple kits.** Stats take the highest value; appearances apply in list order; abilities fill slot keys in order.
- **Gameplay stays on the server.** Body-scale growth (Werewolf moon, Golem rocks, the hunt), the werewolf lunge, knockback, and the thrown capsule and boulder are gameplay, so the server still runs them. Only cosmetic effects moved to clients.
- **Capsule puddles have no server part.** The server keeps a `{ Position, Radius, Expires }` table for damage and speed; clients draw the puddle with `CapsuleSplash`. The puddle timings (5s fade delay, 2s fade, 7s lifetime) are in both `Capsules` and the registry — change both together.
- **Late joiners miss running effects.** A player who joins while a persistent effect is running (a sleeping werewolf, a charging Samurai) won't see it until it plays again.
- **Claws are shown by the client.** The server keeps claw parts hidden; `ClawSwing` shows them locally during a swipe, using each part's `VisibleTransparency` attribute (set by the server for the hunt look).
- **The old handlers are gone.** `SoundHandler` and `VisualEffectsHandler` were removed. `AnimationHandler` is unchanged and is used by the Animation part.
