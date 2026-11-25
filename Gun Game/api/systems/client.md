# Client modules

Client code shows things and sends intent. It never decides the game. Everything here lives in `ReplicatedStorage.Modules.Client` and has the `ClientOnly` attribute.

!!! abstract "Source"

    `Client.Core.*`, `Client.Hud.*`, `Client.Settings.*`, `Client.Movement.*`, `Client.Interact.*`, `Client.Gadgets.*`. Shared: `Shared.PlayerSettings`. Guides: [UI](../../UI.md), [Movement and camera](../../MOVEMENT.md), [Music](../../MUSIC.md).

!!! warning "Build UI in Studio, not in code"

    UI is built by hand (or with execute Luau in Edit mode) under `StarterGui.Main`, or as templates in `Assets.UI.Templates`. Code only fills and shows it. `Main` uses Global ZIndex; anything drawn on a menu needs ZIndex 12 or higher.

## Menus: `Client.Core.Menus`

One full-screen menu at a time. While one is open the mouse is free, the gun doesn't fire, and on touch screens Roblox's own stick and jump button are hidden.

```lua title="From the Menus header"
Menus.Register("Settings", frame)   -- a frame in StarterGui.Main that holds the menu
Menus.Toggle("Settings")
Menus.IsOpen()                       -- true while any menu is open
Menus.Changed:Connect(function(openName) end)  -- the open menu's name, or nil
```

| Function | What it does |
| --- | --- |
| `Register(name, frame)` | Adds a menu; its frame starts hidden |
| `Open(name)` / `Close(name?)` / `Toggle(name)` | Opening one closes any other |
| `IsOpen()` / `.Changed` | Any menu open / fires with the open name or `nil` |
| `SetMouseIconAfterClose(bool)` | Mouse icon once closed |

Gameplay input should check `Menus.IsOpen()` and stand aside.

## Notices, tooltips, feel

| Function | What it does |
| --- | --- |
| `Client.Core.Notice.Show(title, text, sound?)` / `Hide()` | The `Main.Notice` popup (sound defaults to `Error`) |
| `Client.Core.Tooltip.Set(object, text?)` / attribute `Tooltip` | A hover tooltip (`nil` or `""` removes it) |
| `Client.Core.UIFeel.Play(kind)` / `Pop(object)` / `Pulse(object)` | UI sounds and motion. Needs a `UIScale` named `Feel` in the object |
| `Client.Core.Peek.Cut(scroller, share?)` | A horizontal list shows part of its next card |
| Tag `FitScale` on a UIScale | `Client.Core.UI` scales a full-screen menu to fit, under the top bar |

The real pattern from the queue button: an answered request, then feedback.

```lua title="Client.Core.Matchmaking"
local ok, text = Packets.Queue.Request:Fire(action, modeId)
if ok == true then
	UIFeel.Play("Confirm")
elseif type(text) == "string" and string.find(text, "too big", 1, true) then
	Notice.Show("PARTY TOO BIG", text) -- The server's own size check
else
	UIFeel.Play("Error")
	say(if ok == nil then "The server did not answer. Try again." else text)
end
```

## Screens

| Module | API |
| --- | --- |
| `Client.Core.Store.Open(section?)`, `Inventory.Open(tab?)`, `ItemDetails.Show(view)`, `StoreViews` | Store, Inventory, detail page |
| `Client.Core.BattlePass.Open(tab?)` | `"Pass"` or `"Quests"` |
| `Client.Core.SkinShop.Preview(skinId)` | Plays the crate reel landing on a skin, granting nothing (testing) |
| `Client.Core.Music.Play(kind)` / `.CurrentSong` / `.Playlist` | Crossfade to a random `Background`, `Start`, `Panic` or `End` song |
| `Client.Core.Spectate.Cycle(direction)` | Next / previous player to watch |
| `Client.Hud.Nameplates.Refresh()` | Re-apply name and health displays (teammates shown, enemies hidden) |
| `Client.Hud.SiegeHud.UseAbility()` | Uses the class ability |
| No API (self-running) | `SiegeSelect`, `SiegeTopBar`, `Scoreboard`, `DeathScreen`, `DamageFeedback`, `MenuAmbience`, `FeedInfo`, `CmdrClient` |

## Settings and input

`Shared.PlayerSettings` lists every rebindable **action** and default key, every **option** and the volume groups. Add an option there and the Settings menu shows it.

| Function | What it does |
| --- | --- |
| `Client.Settings.Keybinds.Get(action)` / `KeyName` / `Label` / `Set(action, keyName)` / `Reset()` | Key bindings |
| `Client.Settings.Options.Get(name)` / `IsOn(name)` / `Set(name, value, previewOnly?)` / `Save(name)` | Options (`Save` sends it to the server) |
| `Client.Interact.PromptKeys.Key()` | The current Interact key (ProximityPrompts follow it) |
| `SettingsService.GetOption(player, name)` (server) | A player's saved option |

Key actions include Fire, Aim, Reload, Ability, Inspect (V), Melee (Q), Consumable (G), Sprint, Crouch (LeftControl), Prone (C), Slot1–4, Interact (E), Settings (P), Scoreboard (Tab), Drone (5), DroneView (X), **Play (K), Party (L), ClassAbility (T)**. Every feature must work on keyboard and mouse, gamepad and touch.

```lua
local Client = game.ReplicatedStorage.Modules.Client
local Options = require(Client.Settings.Options)
local Keybinds = require(Client.Settings.Keybinds)

Options.Set("Fov", 90)
Options.Save("Fov")
Keybinds.Set("Prone", "C")
print(Keybinds.Label("Prone"))     -- text for a key hint
```

## Movement and camera

The client predicts movement at once and tells the server (`Packets.Movement.SetState`), which checks it and may send `Movement.Correct`. Nothing is sent per frame.

| Function | What it does |
| --- | --- |
| `MovementController.State()` / `Stance()` / `IsSprinting()` / `CancelSprint()` | Local movement state |
| `MovementController.SetGunBlock(bool)` / `SetReloading(bool)` | Tell movement a gun is busy |
| `MovementCamera.Shake(magnitude, roughness, fadeIn, fadeOut)` | Camera shake |
| `MovementCamera.SetAim(alpha, gunAdsFov?)` / `SetFovOverride(fov?)` | FOV |
| `MovementService.GetState(player)` / `IsCrouched(player)` / `BlocksFire(player, gun)` (server) | The checked state |
| `MovementDebug.Toggle()` | The movement readout (`movedebug`) |

| Point (server) | Kind | Arguments |
| --- | --- | --- |
| `Movement.PreventSprint` | Any | player, state |
| `Movement.PreventSlide` / `Movement.PreventProne` | Any | player |
| `Movement.SpeedMultiplier` | Product | player, gunId? (sent to the client as `MoveSpeedMultiplier`) |

Camera render priority: MovementCamera Camera+1, Viewmodel +2, drone camera +3, death camera +4.

## Theme

`Content.Theme`: Void, Base, Panel, Raised, Card, Line, Accent (+Dim, Well), Highlight, Text, Muted, Faint, Ink, Danger, Success, `FONT`, `FONT_BOLD`, `BLUR`, `Map(color)`, `IsBright(color)`. Use these instead of raw colors.

More: [Client: settings, menus and feedback](../../EXAMPLES.md#client-settings-menus-and-feedback).
