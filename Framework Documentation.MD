# Client/Server Framework

A reusable Roblox client/server framework, kept in `ServerStorage.Framework`. It has no game content: it's the
plumbing every game needs, so a new game starts from working systems instead of an empty place.

- **Loading:** one loader requires every module and runs `Init` then `Start`, on both sides.
- **Data:** saved player data and shared server state with [Scribe](https://scribe.ericplane.dev/), declared once.
- **Networking:** every packet in one file, built on the Packet library.
- **Effects:** the server names an effect, every client plays it. Sounds sit in volume groups.
- **Combat:** hitboxes, damage, shields, knockback, kill credit, swords, damage numbers and health bars.
- **Extension points:** content changes core behaviour without core naming it.
- **Admin commands:** Cmdr, limited to admins.

---

## Table of Contents

- [Installing](#installing)
- [Layout](#layout)
- [Core Rules](#core-rules)
- [ModuleLoader](#moduleloader)
- [Data](#data)
- [Packets](#packets)
- [Extension Points](#extension-points)
- [Effects](#effects)
- [Audio](#audio)
- [Combat](#combat)
- [Admin Commands](#admin-commands)
- [Handlers & Helpers](#handlers--helpers)
- [Libraries](#libraries)
- [Guides](#guides)
- [Notes & Gotchas](#notes--gotchas)

---

## Installing

1. Copy each folder's children in `ServerStorage.Framework` into the service of the same name:
   `ReplicatedStorage`, `ServerScriptService`, `StarterPlayer`, `StarterGui`.
2. Enable the two `Start` scripts (`ServerScriptService.Start` and `StarterPlayerScripts.Start`). They are disabled
   inside the framework folder so nothing runs twice in the place it lives in.
3. Add your user id to `ReplicatedStorage.Modules.Classes.Admins`.
4. Set `ProfileStoreIndex` in `Shared.Data` to your game's DataStore name.
5. Play. The output should print `[Example] Server got "hello". Coins: 1`.
6. When that works, delete `Services.Example`, `Client.Core.Example` and the `Example` group in `Shared.Packets`.

---

## Layout

```text
ReplicatedStorage
├── ModuleLoader                      Loads every module: Init, then Start
├── config                            Your game-wide settings (empty table)
├── Modules                           CORE: systems that work for any game
│   ├── Packages                      Scribe, UI (AnimatedBar, ButtonHover, BounceEffects…), QuestAtlis
│   ├── Utilities                     Cmdr, Packet, Signal, Zone, CameraShaker, Shime, NumberSpinner,
│   │                                 KeycodeImages, EasyRagdoll, FormatNumber
│   ├── Helpers                       TableHelpers, UIHelpers
│   ├── Handlers                      AnimationHandler, StateHandler, HitPopup
│   ├── Classes                       Admins, HealthUI
│   ├── Shared
│   │   ├── Data                      Scribe bundle: player data + server store
│   │   ├── Packets                   Every reliable packet
│   │   ├── UnreliablePackets         Packets that may drop (positions, frequent updates)
│   │   ├── ReadOnly                  Read-only client views of server data
│   │   └── Extensions                Extension points
│   ├── Client
│   │   ├── Effects (+ Context)       Plays effects
│   │   ├── Audio                     SoundGroups, AudioSettings
│   │   ├── Core                      Main, UI, CharacterAdded, CmdrClient, Music, Example
│   │   ├── Combat                    SwordInput, CharacterHurt
│   │   └── Hud                       HealthBillboards, PersonalHealth
│   └── Templates
├── Content                           CONTENT: your game's own things
│   └── Effects
│       ├── Registry                  Every effect, by name
│       └── Parts/<Kind>              Sound, Animation, Particles, Highlight, Shards, JointSwing, Template,
│                                     ColorFade, Banner
└── Assets                            Sounds, Vfx, Music/Primary, Models

ServerScriptService
├── Start                             Starts the loader (+ ServerScriptService.Content if you add one)
└── Modules
    ├── Services
    │   ├── CmdrSetup                 Hooks/BeforeRun, Types, Commands (announce example)
    │   ├── PlayerJoin                Waits for data; Player collision group
    │   └── Example
    ├── Systems
    │   ├── Effects/EffectService     Sends effects to clients
    │   └── Combat                    Combat, SwordCombat, DamageLog
    ├── Helpers                       TokenBucket, Rarity, SetCollisionGroup, WebHook
    ├── Utilities                     MuchachoHitbox, WebhookServices
    └── Packages                      r6Blocky

StarterPlayer/StarterPlayerScripts/Start   Client loader start
StarterGui/Main                            ScreenGui: Mobile, Health, HitPopup template
```

**Core vs Content.** `Modules` holds systems that work for any game. `Content` holds what makes your game yours
(effects to begin with; add kits, items, abilities and so on as you go). Core never names content. Add a
`ServerScriptService.Content` folder for server-only content; `Start` loads it automatically.

---

## Core Rules

- **The server decides.** Damage, cooldowns, data and purchases are checked on the server. Clients ask and display.
- **Server code stays in ServerScriptService.** Anything in ReplicatedStorage can be read by exploiters.
- **The server never makes effects.** It calls `EffectService.Play`; clients play the effect.
- **Every packet lives in `Shared.Packets`.** Never build a packet anywhere else.
- **Core never names content.** When content must change core behaviour, use an [extension point](#extension-points).

---

## ModuleLoader

`ReplicatedStorage.ModuleLoader` (crusherfire's Module Loader). The `Start` scripts pass it the containers to load:

```lua
-- ServerScriptService.Start
ModuleLoader.Start(ReplicatedStorage.Modules, ReplicatedStorage.Content, ServerScriptService.Modules)
-- StarterPlayerScripts.Start
ModuleLoader.Start(ReplicatedStorage.Modules, ReplicatedStorage.Content)
```

It finds every ModuleScript in the containers whose ancestors up to the container are **all Folders**, requires
them, calls every module's `Init` (in priority order), then every module's `Start` (each in its own thread).

```lua
local MyService = {}

function MyService:Init()   -- runs first; set up state other modules read. Don't yield long
end

function MyService:Start()  -- runs after every Init; connect events, start loops
end

return MyService
```

Both are optional. A module with neither is just a library (like `Combat`).

**Module attributes**

| Attribute | Effect |
|---|---|
| `ClientOnly` | Only loaded on the client. Set it on every client module in shared containers |
| `ServerOnly` | Only loaded on the server |
| `IgnoreLoader` | Never loaded (still requirable) |
| `LoaderPriority` (number) | Higher loads first |
| `Parallel` | Required inside its own Actor, for parallel Luau |
| `RelocateToServerScriptService` | Moved to ServerScriptService at runtime, leaving a pointer, to hide server code |

**Loader settings** (attributes on ModuleLoader, or `ModuleLoader.ChangeSettings`):

| Setting | Default | Description |
|---|---|---|
| `FolderSearchDepth` / `FOLDER_SEARCH_DEPTH` | 5 in Start | How many folders deep to look |
| `ClientWaitForServer` / `WAIT_FOR_SERVER` | `true` | Client starts only after the server finished |
| `YieldThreshold` | `10` | Seconds before warning about a module that yields |
| `VerboseLoading` | `false` | Print each step |
| `UseCollectionService` / `LoaderTag` | `true` / `LOAD_MODULE` | Also load modules tagged with this tag anywhere |

When a client finishes loading, the player gets the `_ModulesLoaded` attribute. `EffectService` waits for it before
sending effects.

---

## Data

`Shared.Data` returns a [Scribe](https://scribe.ericplane.dev/) bundle with `.Server` and `.Client`.

```lua
-- Shared.Data
local template = {
	Coins = Scribe.Int(0, { Min = 0 }),                    -- saved
	Settings = Scribe.Session({                            -- this session only, never saved
		Music = Scribe.Number(1, { Min = 0, Max = 1 }),
	}),
}
local serverStore = {                                      -- one per server, never saved, every client reads it
	Round = { Number = Scribe.Int(0) },
}
```

```lua
-- Server
local Data = require(ReplicatedStorage.Modules.Shared.Data).Server
local data = Data.WaitForData(player)       -- nil if they left first
data.Coins.Increment(10)
data.Coins.Set(0)
print(data.Coins.Get())

-- Client
local Data = require(ReplicatedStorage.Modules.Shared.Data).Client
Data.WaitForData()
Data.Coins.Observe(function(coins) label.Text = tostring(coins) end)
```

- **Template** roots are saved per player through ProfileStore (`ProfileStoreIndex`, `ProfileKeyPrefix`).
- **`Scribe.Session({...})`** roots belong to the player but are never saved.
- **ServerStore** roots are one per server and replicate to everyone.
- **Drop-in systems** add their own roots: tag a ModuleScript `ScribeFragment` and return
  `{ Template = { ... }?, ServerStore = { ... }? }`. A root name may only be used once.
- **Read-only on the client:** Scribe lets a client write its own copy. Wrap client views so writes error instead of
  silently diverging:

  ```lua
  local coins = ReadOnly.Wrap(Data.Client.Coins, "Coins")
  coins.Get()     -- fine
  coins.Set(5)    -- error: Coins is read-only on the client: Set was rejected
  ```

> Don't name a field after a Scribe accessor method (`Get`, `Set`, `Count`, `Remove`, …). Scribe errors with
> `API_NAME_COLLISION`.

---

## Packets

`Shared.Packets` holds every packet, grouped by feature. Both sides require it, so both build the same packets.

```lua
return {
	Effects = { Play = ..., Stop = ... },
	Combat = {
		Hit = Packet("Hit", Packet.Instance, Packet.NumberF32),
		Swing = Packet("SwordSwing"),
	},
	Shop = {
		Buy = Packet("ShopBuy", Packet.String),                     -- add your own groups
	},
}
```

```lua
Packets.Shop.Buy:Fire("Sword")                                      -- client -> server
Packets.Shop.Buy.OnServerEvent:Connect(function(player, id) end)
Packets.Combat.Hit:Fire(character, 10)                              -- server -> all clients
Packets.Combat.Hit:FireClient(player, character, 10)                -- server -> one client
Packets.Combat.Hit.OnClientEvent:Connect(function(character, damage) end)
```

Types used so far: `Packet.String`, `Packet.Boolean8`, `Packet.NumberU8`, `Packet.NumberF32`, `Packet.NumberF64`,
`Packet.Vector3S16`, `Packet.CFrameF32U16`, `Packet.Instance`, `Packet.Any`, and `{ Type }` for arrays (the Packet
module lists the rest). Names must be unique.

`Shared.UnreliablePackets` builds packets on an `UnreliableRemoteEvent` (may drop or arrive out of order), for
frequent updates like positions. Add entries to its table; usage is the same.

---

## Extension Points

`Shared.Extensions` lets content change core behaviour without core code naming it. Core asks a named point;
content answers by adding a handler.

| Function | Description |
|---|---|
| `.Add(point, handler) -> remove` | Add a handler. Call the result to remove it |
| `.Fire(point, ...)` | Call every handler |
| `.Any(point, ...) -> boolean` | `true` if any handler returns `true` (a veto) |
| `.Product(point, ...) -> number` | Every handler's number multiplied, starting at 1 (a multiplier) |

```lua
-- Core
if Extensions.Any("Combat.BlockHit", humanoid, damage) then return end
damage *= Extensions.Product("Combat.Damage", attacker)
Extensions.Fire("Combat.Hit", attacker, humanoid)

-- Content
Extensions.Add("Combat.BlockHit", function(humanoid, damage)
	return humanoid:GetAttribute("Invulnerable") == true
end)
```

- Nothing is registered: a point exists once something asks it.
- With no handlers, `Any` is `false`, `Product` is `1` and `Fire` does nothing.
- A handler that errors is warned and skipped.
- Handlers are global: check the player has the thing before acting.

Points the framework's combat asks: see [Combat → Extension points](#extension-points-1).

---

## Effects

An effect is a named entry in `Content.Effects.Registry`. The same registry is read by both sides:

- **Server:** `EffectService.Play(name, options)` sends the name and options to the right clients.
- **Client:** `Effects.Play(name, options)` plays it, because the server asked or locally (UI, music).

Each play gets a **Context** that places the effect, times it, and destroys everything it made when it ends: when
its parts finish, it's stopped, its `Target` leaves the game, or its `Tool` leaves the target.

### Registry fields

| Field | Default | Description |
|---|---|---|
| `Group` | `"Effects"` | Sound group: `Music`, `Abilities`, `Effects`, `UI`, `Ambient` |
| `Replicate` | `"All"` | `All` clients, `Nearby` (within `Range`), or `Local` (client only, never sent) |
| `Range` | `200` | Studs, for `Nearby` |
| `Persistent` | `false` | Runs until stopped. Playing again on the same target restarts it |
| `Sound` | — | A sound part or list |
| `Visual` | — | A visual part or list. `Kind` names a module in `Content.Effects.Parts` |
| `Animation` | — | Played through `AnimationHandler` |
| `Variants` | — | `{ [variant] = fields }` that replace the above when played with that `Variant` |

**Sound part:** `Asset` (a Sound in `Assets.Sounds`) or `Id`; `Volume`; `Pitch` (number or `{ min, max }`);
`RollOff = { Min, Max, Mode }`; `Looped`; `Attach` (a part name in the target); `Global`; `Delay`; `Lifetime`.
Without `Asset` or `Id`, the `Sound` in the play options is used.

**Animation part:** `Id`, `Type`, `Markers`, `Looped`, `FadeTime`.

**Visual kinds included:**

| Kind | Fields | What it does |
|---|---|---|
| `Particles` | `Asset`, `Count`, `Lifetime` | Copies an Attachment from `Assets.Vfx` and bursts every emitter |
| `Highlight` | `FillColor`, `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `DepthMode`, `Lifetime`, `PreferChild` | Flashes a Highlight on the target |
| `Template` | `Folder`, `Asset`, `FadeDelay`, `FadeTime`, `Lifetime` | Places a copy of a model from `Assets.Models` and fades it |
| `Shards` | `Count`, `Size`, `Color`, `Material`, `Time`, `Lifetime` | Small parts that fly out and fade |
| `JointSwing` | `Joint`, `Keys` | Swings one joint through rotations |
| `ColorFade` | `Time` | Fades body part colours from `Data.Colors` |
| `Banner` | `Lifetime` | A screen banner from `Data.Title`, `Data.Text`, `Data.Color` |

**Effects included:** `Hit`, `SwordSwing`, `Announcement` (a banner), `ButtonHover`, `ButtonClick`, `Music`.

### Playing

```lua
-- Server
EffectService.Play("Hit", { Target = character })
EffectService.Play("Announcement", { Data = { Title = "Round 2", Text = "Fight!", Color = Color3.new(1, 0.8, 0) } })
EffectService.Stop("Burning", character)

-- Client
local handle = Effects.Play("Music", { Sound = song, OnFinished = nextSong })
handle:Stop()
Effects.Stop("Burning", character)
```

| Option | Description |
|---|---|
| `Target` | Character, model or part the effect is on. Ends if it leaves |
| `Parent` | Where sounds and particles go, instead of the target's root |
| `Position` / `CFrame` | Where it plays, for effects without a target |
| `Tool` | Ends when this Tool leaves the target |
| `Variant` | Picks a `Variants` entry |
| `Speed` | Timing multiplier (`2` = twice as fast); every `Delay` is divided by it |
| `Sound` | The sound for sound parts without `Asset`/`Id` |
| `Data` | Anything else a part reads |
| `OnMarker(name, track)` / `OnFinished()` | Client only |

Options sent from the server must be plain values (instances, numbers, strings, vectors, CFrames, colours, tables).

### A new visual kind

Add a ModuleScript to `Content.Effects.Parts`, named after the kind:

```lua
local Ring = {}
function Ring.Play(spec, context)
	local part = Instance.new("Part")
	part.Anchored, part.CanCollide = true, false
	part.CFrame = context.CFrame
	part.Parent = workspace
	context:Add(part, spec.Lifetime or 1)   -- destroyed after 1s, or when the effect stops
end
return Ring
```

**Context:** `Target`, `Parent`, `CFrame`, `Speed`, `Variant`, `Data`, `Alive`, `:Delay(s, fn)`, `:Add(instance, lifetime?)`,
`:Keep(s)`, `:Hold() -> release`, `:OnStop(fn)`, `:Anchor()`, `:Group()`. A part that errors is warned once and never
breaks the others.

---

## Audio

```text
SoundService.Master
├── Music        background music
├── Abilities    ability sounds
├── Effects      hits and impacts (also the default)
├── UI           buttons and menus
└── Ambient      world ambience
```

- `Client.Audio.SoundGroups` creates these if missing and puts any sound without a group into `Effects`, so nothing
  escapes `Master`. `Get(name)`, `Assign(sound, name)`, `Master()`.
- `Client.Audio.AudioSettings` is ready for a settings menu:

  ```lua
  AudioSettings.Set("Music", 0.4)
  AudioSettings.Get("Master")          --> 1
  AudioSettings.GetAll()
  AudioSettings.Changed:Connect(function(group, volume) end)
  ```

  Saved values go through `AudioSettings.Store` (`Load()` / `Save(volumes)`); today it keeps them for the session.
  To save them, change `Store` only, e.g. to a `Scribe.Session` root in `Shared.Data`.
- `Client.Core.Music` plays a random song from `Assets.Music.Primary` through the `Music` effect, forever.

---

## Combat

### Swords

A sword is **any Tool with a `Damage` number attribute**. `Cooldown` (seconds) is optional; default 0.5.

1. The player clicks; `Client.Combat.SwordInput` sends `Packets.Combat.Swing`.
2. `SwordCombat:Attack(player)` checks the player is alive, holding a sword, not `Swinging`/`Stunned`/`CantDoAnything`
   (StateHandler), and not stopped by `Combat.PreventSwing`. It reads damage and cooldown from the Tool.
3. A hitbox opens in front of the character; every humanoid it touches gets `Combat.ApplyHit` with knockback away from
   the attacker. The attacker has a 1 in 3 chance of 5 shield.
4. `SwordSwing` plays; `Combat.SwordHit` fires for each hit.

Call `SwordCombat:Attack(player)` from any code (an NPC, an ability) for the same swing.

### Combat library — `Systems.Combat.Combat`

| Function | Description |
|---|---|
| `CreateHitbox(character, { Size?, Offset?, Lifetime? }?)` | A MuchachoHitbox cube in front of the character (default 7 studs, 0.1s). Never hits its owner. Call `:Start()`; listen on `.Touched(hit, humanoid)` |
| `DealDamage(humanoid, damage, bypassShield?)` | `Shield` attribute absorbs first, rest to health. Returns `true` if `Combat.BlockHit` blocked it |
| `TryGiveShield(humanoid, chance, amount)` | Adds shield points with a chance |
| `Knockback(character, direction, speed)` | A short LinearVelocity push with a little lift |
| `PlayHitEffects(character)` | Plays `Hit` |
| `ApplyHit(humanoid, damage, options?)` | All of it: kill-credit record, damage, knockback, effect, `Combat.Hit` packet |

`ApplyHit` options: `KnockbackDirection`, `KnockbackSpeed` (default 10), `BypassShield`, `Attacker` (Player, for kill
credit), `Item` (name, for a kill feed).

```lua
local hitbox = Combat.CreateHitbox(character, { Size = 10 })
hitbox.Touched:Connect(function(_, humanoid)
	Combat.ApplyHit(humanoid, 25, { KnockbackDirection = root.CFrame.LookVector, KnockbackSpeed = 30, Attacker = player, Item = "Slam" })
end)
hitbox:Start()
```

### Kill credit — `Systems.Combat.DamageLog`

| Function | Description |
|---|---|
| `Record(humanoid, attacker?, item?)` | Called by `ApplyHit`. Ignores self-hits and non-players |
| `Last(victim, window) -> (Player?, string?)` | Last attacker and item within `window` seconds |
| `Clear(victim)` | Forget |

```lua
humanoid.Died:Connect(function()
	local killer, item = DamageLog.Last(player, 10)
end)
```

### Client side

| Module | Does |
|---|---|
| `Client.Combat.SwordInput` | Click with a sword → `Combat.Swing`. Add a swing animation here |
| `Client.Combat.CharacterHurt` | On `Combat.Hit`: a health billboard on the victim and a damage number |
| `Client.Hud.HealthBillboards` | Health bars over characters (shield shown in blue) |
| `Client.Hud.PersonalHealth` | Your own bar, `StarterGui.Main.Health` |
| `Handlers.HitPopup` | Floating damage numbers from the `StarterGui.Main.HitPopup` template |
| `Classes.HealthUI` | The animated bar these use |

### Extension points

| Point | Kind | Asked by |
|---|---|---|
| `Combat.BlockHit(humanoid, damage)` | Any: `true` cancels the hit | `DealDamage` |
| `Combat.PreventSwing(player)` | Any: `true` stops a swing | `SwordCombat` |
| `Combat.SwordHit(player, victimHumanoid)` | Fire, after each landed sword hit | `SwordCombat` |
| `Combat.WeaponScale(tool)` | Product: grows the sword's hitbox | `SwordCombat` |

---

## Admin Commands

Press **F2** for the [Cmdr](https://eryn.io/Cmdr/) bar. Only user ids in `Classes.Admins` can run commands
(`CmdrSetup.Hooks.BeforeRun`). Cmdr's default commands are registered too.

```text
announce "Round starting!"
```

**Adding a command** — two modules in `CmdrSetup.Commands`:

```lua
-- Commands/Heal
return {
	Name = "heal", Aliases = {}, Description = "Heals players.", Group = "Admin",
	Args = { { Type = "players", Name = "players", Description = "Who to heal" } },
}

-- Commands/HealServer
return function(context, players)
	for _, player in players do
		local humanoid = player.Character and player.Character:FindFirstChildOfClass("Humanoid")
		if humanoid then humanoid.Health = humanoid.MaxHealth end
	end
	return `Healed {#players}`      -- shown in the command bar
end
```

New argument types go in `CmdrSetup.Types` as `function(registry)`; types load before commands.

---

## Handlers & Helpers

**`Handlers.StateHandler`** — timed per-player states:

```lua
StateHandler.SetState(player, "Swinging", true, 0.5)   -- clears itself after 0.5s
StateHandler.GetState(player, "Stunned")
StateHandler.SetStun(player, true, 1, 4)               -- stun for 1s at WalkSpeed 4
StateHandler.RemoveStates(player, "Swinging")
StateHandler.ReturnStates(player)
```

**`Handlers.AnimationHandler`** — loads and tracks animations per character:
`LoadAnim(char, type, id, keyframeCallback?, keyframes?, looped?, delay?)`, `StopAnim`, `GetAnims`, `IsAnim`,
`RemoveAnim`, `PreloadAnimations(char, list)`, `PlayAnimationEveryone`, `StopAnimationEveyone`.

**Server helpers:**
- `TokenBucket.new(capacity, seconds)` → `:allow(userId)` / `:remove(userId)`. Rate-limit any remote.
- `Rarity.CreateLootTable(t)`, `Roll(table, luck?)`, `MultiRoll(table, count, luck?)`, `PercentChance`, `FractionChance`.
- `SetCollisionGroup`, `WebHook`.

**Shared helpers:** `TableHelpers.TableLength`, `CreateWatchedTable(data, onChanged)`;
`UIHelpers:GetPlayerThumbnailIcon(player)`, `UIHelpers:ConvertToMMSS(seconds)`.

**Client core:** `CharacterAdded` (a place for per-character client setup), `UI` (shows `Main.Mobile` buttons on
touch devices), `CmdrClient` (F2), `Main` (empty starting point).

---

## Libraries

| Library | Where | For |
|---|---|---|
| Scribe | Packages | Player data, replication, ProfileStore |
| UI | Packages | AnimatedBar, ButtonHover (plays ButtonHover/ButtonClick), BounceEffects |
| QuestAtlis | Packages | Quests |
| Packet | Utilities | Networking (used by Shared.Packets) |
| Signal | Utilities | Events |
| Cmdr | Utilities | Command bar |
| Zone | Utilities | Region enter/leave |
| CameraShaker | Utilities | Camera shake |
| Shime | Utilities | UI shine |
| NumberSpinner | Utilities | Counting number labels |
| KeycodeImages | Utilities | Key icons |
| EasyRagdoll | Utilities | Ragdolls |
| FormatNumber | Utilities | Number formatting (1.2K, 3M) |
| MuchachoHitbox | Server Utilities | Hitboxes (used by Combat) |
| r6Blocky | Server Packages | R6 blocky rig |

---

## Guides

### A server system with a client half

1. `ServerScriptService.Modules.Systems.Round` — a module with `Init`/`Start`.
2. `ReplicatedStorage.Modules.Client.Round` — set the `ClientOnly` attribute.
3. Add a `Round` group to `Shared.Packets`, or a `ServerStore` root to `Shared.Data` for state everyone reads.
4. Done — the loader finds both.

### A new effect

1. Put assets in `Assets.Sounds` / `Assets.Vfx` / `Assets.Models`.
2. Add an entry to `Content.Effects.Registry`:

   ```lua
   Explosion = {
   	Replicate = "Nearby", Range = 300,
   	Sound = { Asset = "Boom", Volume = 1 },
   	Visual = { { Kind = "Particles", Asset = "BoomFX", Count = 30 }, { Kind = "Shards", Count = 12 } },
   },
   ```

3. `EffectService.Play("Explosion", { Position = position })`.

### A new weapon

- A sword: a Tool with a `Damage` attribute. Done.
- Anything else: a server module that makes a hitbox and calls `Combat.ApplyHit`, triggered by your own packet.

### Blocking damage (shields, invulnerability)

```lua
Extensions.Add("Combat.BlockHit", function(humanoid)
	return humanoid:GetAttribute("Invulnerable") == true
end)
```

---

## Notes & Gotchas

- **Set `ClientOnly` on client modules.** Without it the server's loader runs them too.
- **Only Folders between a container and a module.** A module inside another ModuleScript isn't loaded on its own;
  its parent requires it.
- **Helpers that shouldn't run on load** must not be named `Init`/`Start` (use `Build`, `Setup`).
- **Always require `Shared.Packets`.** Never build a packet with the same name elsewhere, even in the command bar —
  a second copy of the packet library can't decode the real one's traffic.
- **Effects only reach loaded clients** (`_ModulesLoaded`), so players joining mid-game never get packets they can't
  read yet. A player who joins during a persistent effect won't see it until it plays again.
- **Session data resets on leave.** Only Template roots outside `Scribe.Session` are saved.
- **Swords need the Tool held on the server.** If swings do nothing, check the server's character has the Tool.
- **Studio's F shortcut** (Zoom To) can steal F from ProximityPrompts in play tests: turn off "Respect Studio
  shortcuts when game has focus" in Studio Settings.
- **Delete the examples** (`Services.Example`, `Client.Core.Example`, `Packets.Example`) when you start a game.
