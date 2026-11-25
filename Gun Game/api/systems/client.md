# Client: menus, HUD and screens

Client code shows things and sends intent. It never decides the game. Everything here lives in `ReplicatedStorage.Modules.Client` and has the `ClientOnly` attribute.

!!! abstract "Source"

    `Client.Core.*`, `Client.Hud.*`. Related pages: [Settings and keybinds](settings.md), [Movement and camera](movement.md), [Guns (client modules)](guns.md#client-modules), [Drones and cameras (client)](drones-cameras.md#client), [Effects and sound](../foundations/effects.md). Guides: [UI](../../UI.md), [Music](../../MUSIC.md).

!!! warning "Build UI in Studio, not in code"

    UI is built by hand (or with execute Luau in Edit mode) under `StarterGui.Main`, or as templates in `Assets.UI.Templates`. Code only fills and shows it. `Main` uses Global ZIndex; anything drawn on a menu needs ZIndex 12 or higher.

```lua
local Core = game.ReplicatedStorage.Modules.Client.Core
local Menus = require(Core.Menus)
local Notice = require(Core.Notice)
local UIFeel = require(Core.UIFeel)
```

---

## `Menus`

One full-screen menu at a time. While one is open the mouse is free, the gun doesn't fire, and on touch screens Roblox's stick and jump button are hidden.

### `Menus.Register(name, frame)`

Adds a menu (its frame starts hidden). Each menu module registers its own frame.

```lua
Menus.Register("Settings", Main.Settings)
```

### `Menus.Open(name)` / `Menus.Close(name?)` / `Menus.Toggle(name)`

Opening one closes any other. `Close()` with no name closes whatever is open.

```lua
Menus.Open("Store")
Menus.Close()
Menus.Toggle("Settings") -- the P key
```

Registered names include `Settings`, `Store`, `Inventory`, `Modes`, `Party`, `Loadout`, `SkinShop`, `Career`.

### `Menus.IsOpen() → boolean`

Gameplay input should stand aside while it's true.

```lua
if Menus.IsOpen() then return end -- don't fire while a menu is up
```

### `Menus.Changed`

Signal: the open menu's name, or `nil` when all are closed. `AnalyticsClient` reports menus from it.

```lua
Menus.Changed:Connect(function(openName)
	print("menu:", openName)
end)
```

### `Menus.SetMouseIconAfterClose(enabled)`

Whether the mouse icon shows after the menu closes.

```lua
Menus.SetMouseIconAfterClose(false)
```

---

## Feedback

### `Notice.Show(title, text, sound?)` / `Notice.Hide()`

The `Main.Notice` popup with a 70% backdrop and an icon. `sound` defaults to `"Error"`.

```lua
Notice.Show("PARTY TOO BIG", "Your party is too big for 1V1. Pick a different mode.")
Notice.Show("GIFT SENT", "Your friend got it.", "Confirm")
```

### `Tooltip.Set(object, text?)`

A hover tooltip on a UI element (`nil` or `""` removes it). The `Tooltip` attribute on a GuiObject does the same with no code.

```lua
local Tooltip = require(Core.Tooltip)
Tooltip.Set(button, "Opens the Battle Pass")
```

### `UIFeel.Play(kind)` / `UIFeel.Pop(object)` / `UIFeel.Pulse(object)`

UI sounds (`Hover`, `Press`, `Open`, `Close`, `Confirm`, `Error`, `Tick`, `Notify`) / pop something in / a quick grow-and-settle. `Pop` and `Pulse` need a `UIScale` named `Feel` in the object.

```lua
UIFeel.Play("Confirm")
UIFeel.Pulse(coinLabel)
```

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

### `Peek.Cut(scroller, share?)`

A horizontal list shows part of its next card, so players see it scrolls.

```lua
require(Core.Peek).Cut(scrollingFrame)
```

Tag **`FitScale`** on a UIScale in a full-screen menu and `Client.Core.UI` scales it to fit under the top bar ([UI](../../UI.md#full-screen-menus-that-fit-fitscale)).

---

## Screens

| Function | Opens / does | Example |
| --- | --- | --- |
| `Store.Open(sectionId?)` | The Store | `require(Core.Store).Open()` |
| `Inventory.Open(tabId?)` | The Inventory | `require(Core.Inventory).Open()` |
| `BattlePass.Open(which?)` | The Battle Pass, `"Pass"` or `"Quests"` | `require(Core.BattlePass).Open("Quests")` |
| `Goals.Open(tabId?)` | The GOALS screen (streak, weekly, level, ranked) | `require(Core.Goals).Open()` |
| `GiftPicker.Open(key, itemName)` | Pick a player to gift a Robux item | `require(Core.GiftPicker).Open("Crate:Glacier", "Glacier Crate")` |
| `ItemDetails.Show(view)` | A detail page (`View.Class` / `GunId` show class or gun panels) | `require(Core.ItemDetails).Show(view)` |
| `ItemDetails.Spin(viewport, on)` / `Hover(viewport, on)` | Turn a gun preview | `ItemDetails.Spin(viewport, true)` |
| `SkinShop.Preview(skinId)` | Play the crate reel landing on a skin (testing; grants nothing) | `require(Core.SkinShop).Preview("GlacierRifle")` |
| `Music.Play(kind)` | Crossfade to a random `Background`, `Start`, `Panic` or `End` song | `require(Core.Music).Play("Panic")` |
| `Spectate.Cycle(direction)` | Next (1) / previous (-1) player to watch | `require(Core.Spectate).Cycle(1)` |
| `ClassPanel.Fill(panel, class, opts)` / `FillGun(panel, opts)` | Fill class and gun panels | `ClassPanel.Fill(panel, Classes.Get("Flash"), {})` |

`Music.CurrentSong` is the Sound playing now; `Music.Playlist` the background folder.

## HUD

| Function | Does | Example |
| --- | --- | --- |
| `Client.Hud.SiegeHud.UseAbility(completedHold?)` | Uses the class ability (T) | `SiegeHud.UseAbility()` |
| `Client.Hud.Nameplates.Refresh()` | Re-apply name/health displays (teammates shown, enemies hidden) | `Nameplates.Refresh()` |
| `Client.Hud.HealthBillboards.SetupBillboard(humanoid)` | A health bar over any humanoid | `HealthBillboards.SetupBillboard(npc.Humanoid)` |

No API (they run themselves): `SiegeSelect` (selection and reveal), `SiegeTopBar`, `Scoreboard` (Tab), `DeathScreen`, `Client.Combat.DamageFeedback`, `MenuAmbience` (blur while a menu is open), `CmdrClient` (F2 / the CMD button), `Client.Core.UI` (fits the HUD and touch layout).

## Theme

`Content.Theme`: `Void`, `Base`, `Panel`, `Raised`, `Card`, `Line`, `Accent` (+`Dim`, `Well`), `Highlight`, `Text`, `Muted`, `Faint`, `Ink`, `Danger`, `Success`, `FONT`, `FONT_BOLD`, `BLUR`, `Map(color)`, `IsBright(color)`. Use these instead of raw colors.

```lua
local Theme = require(game.ReplicatedStorage.Content.Theme)
label.TextColor3 = Theme.Muted
frame.BackgroundColor3 = Theme.Panel
```

More: [Client: settings, menus and feedback](../../EXAMPLES.md#client-settings-menus-and-feedback).
