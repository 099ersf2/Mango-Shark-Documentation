# AI coding guide: Gun Game (FPS place)

Give this file to any AI agent before it writes code for the Roblox place **"FPS"** (Mango Shark Studios, placeId `80699390327837`, universe `10775243847`). It explains how the game is built and how new code must be written. Follow it exactly. When this file and your habits disagree, this file wins.

The other docs go deeper on each system: `API.md` (every function, packet, hook, attribute), `ADDING_GUNS.md`, `GUN_SYSTEM.md`, `MOVEMENT.md`, `ADDING_NPCS.md`, `CONSUMABLES.md`, `BREAKABLES.md`, `SOFTWALLS.md`, `SKINS.md`, `LOBBY.md`, `KILL_FEED.md`, `AIM_ASSIST.md`, `DECISIONS.md` (design answers already given). Read the doc for the system you touch before changing it.

---

## 1. Hard rules

Break none of these.

1. **Everything loads through `ReplicatedStorage.ModuleLoader`.** Never add a new `Script` or `LocalScript`. New code is a `ModuleScript` with `Init` and/or `Start` inside a loaded container (section 3).
2. **Client modules get the `ClientOnly` attribute** set to `true`. Without it they also run on the server and error.
3. **Never build UI in scripts.** UI is made in Studio under `StarterGui.Main` (or cloned from `ReplicatedStorage.Assets.UI.Templates`). Scripts only find existing UI with `WaitForChild` and change text, visibility and colors. Creating the UI once in Studio's Edit mode (by hand or with a Studio tool) counts as building it in Studio and is fine.
4. **HUD and menus use Scale**, so they fit phones. **Mobile touch buttons (`Main.Mobile`) do not**: they keep their original positioning, which has its own math. Copy a sibling button and place it the same way its siblings are placed.
5. **The server decides everything.** Clients send intent only (an action, an aim direction, a timestamp). The server checks every request: player alive, not in the lobby, not stunned, cooldowns, counts, timestamps, rate limits, types. Never trust a number from the client.
6. **All network traffic goes through `Shared.Packets`** (reliable) or `Shared.UnreliablePackets` (cosmetic). No `RemoteEvent` or `RemoteFunction` instances.
7. **Numbers live in `Content`**, not in system code. Tuning values (damage, speeds, cooldowns, radii) go in a `ReplicatedStorage.Content` module. Internal constants that aren't game design go in `UPPER_CASE` at the top of the module.
8. **Product and game pass ids live only in `Shared.ProductIds`.** Never type an id anywhere else.
9. **Don't change sword combat** (`Systems.Combat.SwordCombat`). Don't break existing gun, NPC, movement, settings or lobby behavior.
10. **Other developers edit this place too.** Keep what they built unless it's clearly a bug. If a design question comes up, ask the user instead of guessing, and record the answer in `DECISIONS.md`.
11. **Document every change** (section 12).

---

## 2. Where things live

```
ReplicatedStorage
  ModuleLoader                 the loader (do not edit)
  Modules/                     loaded on server AND client
    Shared/                    shared logic: Packets, UnreliablePackets, Data, Extensions, PlayerSettings,
                               ProductIds, Smoke, CursorAim, ReadOnly, Guns/ (Ballistics, Spread, Abilities...),
                               Movement/ (States)
    Handlers/                  StateHandler, AnimationHandler, HitPopup
    Helpers/                   TableHelpers, UIHelpers
    Classes/                   Admins, HealthUI
    Client/  (ClientOnly)      Effects, Audio/, Core/ (Menus...), Combat/, Hud/, Guns/, Settings/, Movement/, Interact/
    Packages/                  third-party (Scribe, UI...) - don't edit
    Utilities/                 third-party (Packet, Cmdr, FastCast2, Signal, Zone...) - don't edit
  Content/                     game data, loaded on both sides: Guns/, Effects/, NPC/, Movement/, Breakables/,
                               Destruction/, Consumables
  Assets/                      Models/, Vfx/, Sounds, UI/Templates (instances, not code)
ServerScriptService
  Start                        server bootstrap (do not edit)
  Modules/                     loaded on the server only
    Systems/                   game systems: Guns/, Combat/, NPC/, Movement/, Breakables/, Destruction/, Lobby/,
                               Consumables/, Effects/ (EffectService), SkinShopService
    Services/                  CmdrSetup (+ Commands), PlayerJoin, SettingsService
    Helpers/                   TokenBucket, SetCollisionGroup, Rarity, WebHook
    Utilities/                 third-party (BehaviorTreeCreator, MuchachoHitbox...)
StarterPlayer.StarterPlayerScripts.Start   client bootstrap (do not edit)
StarterGui.Main                all game UI
```

**Where to put a new module:**

| It is… | Put it in |
| --- | --- |
| Server game logic | `ServerScriptService.Modules.Systems.<Feature>.<Feature>Service` |
| Client logic | `ReplicatedStorage.Modules.Client.<Area>.<Name>`, with `ClientOnly` |
| Used by both sides | `ReplicatedStorage.Modules.Shared.<Name>` |
| Design data and tuning | `ReplicatedStorage.Content.<Feature>` |
| Models, particles, sounds | `ReplicatedStorage.Assets.Models` / `Vfx` / `Sounds` |

Short names in the docs: `Systems.X` = `ServerScriptService.Modules.Systems.X`, `Shared.X` / `Client.X` / `Handlers.X` = `ReplicatedStorage.Modules.…`, `Content.X` = `ReplicatedStorage.Content.X`.

---

## 3. How loading works

The `Start` scripts call `ModuleLoader.Start` with these containers:

- **Server:** `ReplicatedStorage.Modules`, `ReplicatedStorage.Content`, `ServerScriptService.Modules` (and `ServerScriptService.Content` if it exists).
- **Client:** `ReplicatedStorage.Modules`, `ReplicatedStorage.Content`. The client waits until the server has loaded.

For every `ModuleScript` found (up to 5 folders deep, and only through `Folder`s; a module inside another module isn't loaded):

1. **Require** every module.
2. **`Init`** every module that has it, in order. Set up state, collision groups and folders here. Don't depend on another module's `Start` having run.
3. **`Start`** every module that has it. Connect events, packets and `PlayerAdded` here.

Attributes on a ModuleScript: `ClientOnly`, `ServerOnly`, `IgnoreLoader`, `LoaderPriority` (a number; higher loads first). Data-only modules (most of `Content`) just return a table and need no `Init` or `Start`.

`Init` and `Start` are defined with a colon: `function MyService:Init()`. Other public functions use a dot: `function MyService.Do(player)`.

**A gotcha:** code run from the Studio command bar, or with a tool's "execute Luau", gets its **own copy** of every module, not the running one. To reach the live modules during a playtest, make a temporary `Script` in `ServerScriptService` (server) or a `LocalScript` in `PlayerGui` (client), then delete it.

---

## 4. Code style

Match the existing code exactly. Every module looks like this:

```lua
--!strict
--[[
	Systems.Example.ExampleService

	One paragraph: what this module does, and who owns which part (server decides X, the client only Y).

		ExampleService.Get(player)              -- what it returns
		ExampleService.Do(player, amount)       -- what it does

	Extension points (Shared.Extensions):
		Example.PreventDo(player)    Any: true stops it
		Example.Done(player, amount) Fire: after it happens
]]

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Modules = ReplicatedStorage.Modules
local Shared = Modules.Shared

local ExampleContent = require(ReplicatedStorage.Content.Example)
local Packets = require(Shared.Packets)
local Extensions = require(Shared.Extensions)
local EffectService = require(script.Parent.Parent.Effects.EffectService)

local MAX_CLOCK_DRIFT = 2 -- Seconds a request's timestamp may be off the server clock
local LOBBY_ATTRIBUTE = "InLobby"

local ExampleService = {}

local lastUse: { [Player]: number } = {}

-- Short comment for a private helper
local function canUse(player: Player)
	: boolean
	return player:GetAttribute(LOBBY_ATTRIBUTE) ~= true
end

--[[
	What the public function does, in one or two sentences.

	@param player The player
	@param amount How much
	@return True if it happened
]]
function ExampleService.Do(player: Player, amount: number)
	: boolean
	if not canUse(player) or Extensions.Any("Example.PreventDo", player) then
		return false
	end
	-- ...
	Extensions.Fire("Example.Done", player, amount)
	return true
end

function ExampleService:Init()
	-- state, collision groups, folders
end

function ExampleService:Start()
	Players.PlayerRemoving:Connect(function(player)
		lastUse[player] = nil
	end)
	Packets.Example.Do.OnServerEvent:Connect(function(player: Player, timestamp: number, amount: number)
		if type(timestamp) ~= "number" or math.abs(workspace:GetServerTimeNow() - timestamp) > MAX_CLOCK_DRIFT then
			return
		end
		ExampleService.Do(player, amount)
	end)
end

return ExampleService
```

The rules behind it:

- **`--!strict` first**, then the `--[[ ]]` header: the module's short path, what it does, a usage block, and its extension points.
- **Order:** services, then requires, then `UPPER_CASE` constants (each with a comment and its unit), then the module table, then state, private functions, public functions, `Init`, `Start`, `return`.
- **Typed everything:** parameters, returns (the return type goes on its own line after the parameters, as above), and tables (`{ [Player]: number }`). Export types from Content modules (`export type Consumable = {...}`).
- **Public functions get a `--[[ ]]` doc block** with `@param` and `@return`. Private helpers get a one-line `--` comment.
- **Names:** `PascalCase` for modules, public functions and UI instances; `camelCase` for locals and private functions; `UPPER_CASE` for constants.
- **Clean up per-player state** on `PlayerRemoving`.
- **Optional dependencies:** when calling a system that is being refactored or may be missing (for example `Systems.Destruction.SoftWalls`), find it with `FindFirstChild` and call it through `pcall`, so a change there can't break your feature.
- **No `wait()`, `spawn()` or `delay()`.** Use `task.wait`, `task.spawn`, `task.delay`.
- **Luau gotcha:** a line starting with `(` right after another statement is "ambiguous syntax". Assign to a local first.
- **Comments say why**, in plain English. No commented-out code.

---

## 5. The shared building blocks

Use these instead of writing your own.

### Networking: `Shared.Packets`

Add packets to a feature group in `Shared.Packets`. Each needs a unique name and typed arguments:

```lua
Example = {
	-- Client -> server. Server time and the unit look direction. The server checks everything.
	Do = Packet("ExampleDo", Packet.NumberF64, Packet.Vector3F32),
	-- Server -> one client. Whether it worked.
	Result = Packet("ExampleResult", Packet.Boolean8),
},
```

- **Sending:** the client calls `packet:Fire(...)`. The server calls `packet:FireClient(player, ...)` for one player, or `packet:Fire(...)` for all.
- **Receiving:** use `packet.OnServerEvent:Connect(function(player, ...) end)` or `packet.OnClientEvent:Connect(...)`.
- **Requests that need an answer:** use `:Response(...)` (see `Skins.BuyCrate`).
- **Cosmetic, high-frequency traffic** (tracers, aim pitch) goes in `Shared.UnreliablePackets`.
- **Server checks:** validate every argument's type and range, check timestamps against `workspace:GetServerTimeNow()`, and rate-limit spammable requests with `Helpers.TokenBucket`.
- **Never** build a `Packet(...)` anywhere but these two modules.

### Extension points: `Shared.Extensions`

This is how features change each other without editing each other's code.

- **Kinds:**
  - `Extensions.Any(point, ...)` is a veto: true if any handler returns true.
  - `Extensions.Product(point, ...)` is a multiplier: the handlers' numbers multiplied together, 1 with no handlers.
  - `Extensions.Fire(point, ...)` is a notification.
- **Adding a handler:** `Extensions.Add("Gun.DamageMultiplier", function(who, gunId, humanoid, hit) return 1.5 end)` returns a function that removes it.
- **In a new system,** offer `Prevent…` (Any), `…Multiplier` (Product) and after-the-fact (Fire) points where other features would want to hook in, and list them in the header and in `API.md`.
- **To change another system's behavior** (perks, team rules, modes), add a handler. Don't edit that system.

### Player data: Scribe (`Shared.Data`)

- **Reading and writing:** on the server, `local data = Data.Server.WaitForData(player)`, then `data.Coins.Increment(100)`, `data.Field.Get()` and `.Set(v)`. The client reads with `Data.Client.WaitForData()` and `.Observe(...)`.
- **Only the server writes.** Clients ask through a packet.
- **New saved fields:** don't edit `Shared.Data`. Make (or reuse) a module tagged **`ScribeFragment`** that returns `Template` (and optionally `ServerStore`), with Scribe types such as `Scribe.String("Grenade")`. Each root field name may be used only once in the whole game. See `Content.Consumables` and `Shared.PlayerSettings`.
- **Live per-life state** (counts, flags) goes in player attributes set by the server, not in saved data.

### Effects and sound: `Content.Effects.Registry`

- **Defining effects:** every sound and VFX is defined by name in `Content.Effects.Registry`, with its `Group`, `Replicate` (`All`, `Nearby` + `Range`, `Local`), `Sound`, `Visual` and `Animation` parts.
- **Server:** `EffectService.Play("Name", { Position = pos } / { Target = part } / { CFrame = cf }, exceptPlayer?)`.
- **Client (local feedback, instant):** `Effects.Play("Name", {...})`.
- **Pooling:** sounds and VFX are pooled by the effects system. Never `Instance.new("Sound")` in feature code. Sound assets go in `Assets.Sounds`.
- **Feel:** for instant feedback, the client plays its own effect right away and the server plays it for everyone else with `except = player`.

### States: `Handlers.StateHandler`

- `StateHandler.SetState(player, key, value, duration)` and `SetStun(...)` set player attributes such as `Stunned`, `Reloading` and `CantDoAnything`.
- Any action should refuse while `Stunned` or `CantDoAnything` is set, or while `InLobby` is true.

### Combat and damage

- `Combat.ApplyHit(humanoid, damage, { Attacker = player, Item = "Name" })`: damage with kill credit (kill feed, stats). `Item` is what the kill feed shows.
- `Combat.DealDamage(humanoid, damage)`: no credit.
- `Combat.Knockback(character, direction, speed)`.
- `Ballistics.HumanoidOf(part)`: finds the humanoid behind a hit part.
- **World damage:** `BreakableService.DamageRadius(pos, radius, amount, player, source)` for boards, and `SoftWalls.Punch(...)` for soft walls (through `pcall`).
- **Hitmarkers:** confirm a hit to the attacker with `Packets.Gun.HitConfirm:FireClient(player, headshot, killed)`.

### Input and settings: `Shared.PlayerSettings`

- **Rebindable keys:** add an entry to `PlayerSettings.Actions` (`{ Name, Label, Default }`), and Settings > Controls shows it automatically. Bind it on the client through `Client.Settings.Keybinds`, and rebind when the key changes.
- **Gamepad buttons** are fixed constants in `PlayerSettings` (for example `ConsumableGamepadKey`).
- **Touch:** a button in `Main.Mobile` (rule 4).
- **Every action must work on all three inputs**: keyboard and mouse, gamepad, and touch.
- **Options** (toggles and sliders) go in `PlayerSettings.Options`, and the Settings menu shows them.
  - Client: `Options.Get(name)`.
  - Server: `SettingsService.GetOption(player, name)`.
- **Menus:** open and close them with `Client.Core.Menus`. While a menu is open, gameplay input must be ignored.

### Admin commands: Cmdr

- **Adding a command:** put a `<Name>` definition and a `<Name>Server` module in `ServerScriptService.Modules.Services.CmdrSetup.Commands`. Copy `Announce` and `AnnounceServer`. A client-only command can use `ClientRun` and skip the server module (see `MoveDebug`).
- **Admins** are listed in `Classes.Admins`, and the server checks it on every command.

### Products

- Add the id to `Shared.ProductIds`, and handle the purchase through the existing Scribe receipt handling (see `docs/SKINS.md`).
- `ProductIds.IsSet(id)` is false for the `0` placeholder, so the feature must hide or disable itself until a real id is set.

---

## 6. World conventions

- **Characters:**
  - R15 with **AnimationConstraint** joints, not Motor6D. Joint code must handle both.
  - Character parts are in the `Player` collision group.
- **Collision groups:** register new ones in your module's `Init` with `PhysicsService` (check `IsCollisionGroupRegistered` first) and list them in `API.md`. Existing groups: `Player`, `ProneBody`, `SoftWallDebris`, `Thrown`.
- **Runtime objects:**
  - Put them in a named folder in `workspace` (for example `workspace.Thrown`), never loose.
  - Projectiles the server spawns get `SetNetworkOwner(nil)`.
  - Clean up with `task.delay` + `Destroy`.
- **NPCs:** spawned NPCs live in `workspace.Enemies` and are tagged `NPC`. Aim assist and health bars only look in `workspace.Enemies`. `NPCService`'s `MAX_NPCS` is `10`. NPC reflexes (hearing, shooting to test through soft walls and boards, breaching, grenades, dodging) live in `Systems.NPC.Tactics`; see `ADDING_NPCS.md`.
- **Tags:** use `CollectionService` tags for map objects (`Board`, `DoorBoard`, `SoftWall`, `NPCSpawn`, `SkinShopPrompt`). New tags go in `API.md`.
- **Lobby:** the `InLobby` player attribute is true in the lobby. Only a player's first spawn of a session is in the lobby. Weapons, consumables and abilities must be refused there.
- **Teams:**
  - There is no team system yet. Code that targets enemies must skip teammates when `player.Team` is set (see `Client.Guns.AimAssist`).
  - Friendly-fire rules go through a `…DamageMultiplier` extension point, not hardcoded checks.

---

## 7. A typical feature, end to end

Grenades and smoke bombs (`docs/CONSUMABLES.md`) are the reference example. Copy this shape:

1. **`Content.Consumables`:** the definitions and every number, an exported type, `Get(id)`, `List`, and constants such as `PER_LIFE`. Tagged `ScribeFragment` to save the player's pick.
2. **`Shared.Packets`:** a `Consumable` group with `Throw` (client → server: server time, look direction) and `Pick` (client → server: id).
3. **`Systems.Consumables.ConsumableService` (server):**
   - Holds the count in player attributes and refills it on `CharacterAdded`.
   - Validates every throw, spawns the projectile, and applies damage through `Combat.ApplyHit`.
   - Plays effects through `EffectService` and exposes extension points.
4. **`Client.Guns.Consumables` (client, `ClientOnly`):**
   - Binds the key, gamepad button and touch button, and sends intent.
   - Plays the local whoosh at once and updates the HUD from the attributes.
5. **UI built in Studio:** a HUD frame in `Main` (Scale), a button in `Main.Mobile` (copied from a sibling), and a picker in the Loadout menu.
6. **Effects** in `Content.Effects.Registry`, models in `Assets.Models.Consumables`, particles in `Assets.Vfx`.
7. **Docs:** a new `docs/CONSUMABLES.md`, plus updates to `API.md`, the controls table in `ADDING_GUNS.md`, `GUN_GAME.md` and `CHANGELOG.md`.

---

## 8. Working in Studio (for agents with Studio tools)

- **Editing scripts:** only works in **Edit mode**. Stop any playtest first.
- **Checks:**
  - Prefer checks in Edit mode, such as compiling a script with `loadstring(source)`.
  - Clean up any test copies you make; a timed-out tool call can leave a clone behind.
- **Playtests:**
  - The Loadout menu opens on join, and gameplay input is ignored while it's open.
  - Studio's input tools may not deliver key presses to the game. Drive the live modules from a temporary script instead (section 3).
  - Test server rules by firing a packet's `OnServerEvent:Fire(player, ...)` from a temporary server Script.
  - Write results to a `workspace` attribute and read them after.
- **When done:**
  - Read the console output: there should be no errors or warnings from your code.
  - Stop the playtest and delete temporary scripts.
- **Publishing:** never publish the place unless the user asks. Publishing makes it live for every player.

---

## 9. Testing standard

- **Verify with numbers.** "Dummy at 4 studs went from 100 to 7 health" is a check. "It should work" is not.
- **Test every input:** keyboard, gamepad and touch. If you can't test one (no device), say so.
- **Test the edge cases:** death and respawn, the lobby, leaving mid-action, spamming the packet, and an open menu.
- **Test as other players see it:** with 2+ players (Studio Test → Clients and Servers) when the feature is networked.
- **Report what you couldn't verify**, plainly.

---

## 10. Things that are off limits or already decided

- Sword combat: don't change it.
- `ModuleLoader`, both `Start` scripts, `Packages/` and `Utilities/` (third-party): don't edit them.
- Design questions already answered are in `DECISIONS.md` (crate price, crouch and prone keys, bash rules, soft wall holes, recoil recovery off, and more). Don't reopen them.
- Systems other developers made (lobby, skins and shop, kill feed, soft walls): keep their behavior and extend them through extension points.

---

## 11. Performance

- **No per-frame work on the server** unless needed. Prefer events, `task.delay` and attribute signals.
- **Client per-frame work** goes in one `RunService` connection per module (or the existing camera step for camera changes, see `Client.Movement.MovementCamera`).
- **Reuse `RaycastParams`** and other objects. Don't create them every frame.
- **Clean up** connections and instances you create. Lots of instances (debris, particles) need a lifetime.

---

## 12. Documentation (part of every change)

Docs are Markdown in `docs/`, plus `GUN_GAME.md` (home page) and `CHANGELOG.md`. They're pushed to the GitHub repo `099ersf2/Mango-Shark-Documentation` (folder `Gun Game/`).

- **New system:** write `docs/<SYSTEM>.md` with these sections:
  - What it is and how it plays
  - Controls
  - Where things are
  - How it works
  - API and extension points
  - How to add more
  - Testing (what was checked, with numbers, and what wasn't)
  - Limits

  Add a row for it in `GUN_GAME.md`.
- **`API.md`:** add every new public function, packet, extension point, data field, attribute, tag and collision group.
- **`CHANGELOG.md`:** add an entry at the top, `## YYYY-MM-DD: Title`, with **Added** / **Changed** / **Fixed** bullets.
- **`NEXT_STEPS.md`:** add checklist items for anything not yet verified (phone, gamepad, multiplayer).
- **Writing style:** plain, short sentences. Tables for reference. Say what you checked and what you didn't.

---

## 13. Before you say "done"

- [ ] `--!strict`, header block, typed functions, constants at the top, `ClientOnly` on client modules.
- [ ] No new Script or LocalScript; no UI built in code; no new RemoteEvents.
- [ ] The server validates every client request.
- [ ] Tuning numbers are in `Content`.
- [ ] Works on keyboard, gamepad and touch; refused in the lobby, while stunned and while dead.
- [ ] Per-player state cleaned up on leave; runtime instances cleaned up.
- [ ] Console clean in a playtest; temporary scripts and test copies deleted.
- [ ] Docs, `API.md` and `CHANGELOG.md` updated.
- [ ] Report: what changed (scripts and instances), what you tested with results, what you couldn't verify, and any decision the user must make.
