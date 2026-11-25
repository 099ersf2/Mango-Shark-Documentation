# Settings, keybinds and options

Every setting a player can change lives in **`Shared.PlayerSettings`**: rebindable actions, volume groups and options. Add one there and it gets a saved field and a row in the Settings menu, with no menu code to write.

!!! abstract "Source"

    Shared: `Shared.PlayerSettings` (a `ScribeFragment`). Server: `Services.SettingsService`. Client: `Client.Settings.Keybinds`, `Options`, `Slider`, `SettingsMenu`, `Client.Interact.PromptKeys`.

## How saving works

```text
Client                                   Server
Keybinds.Set / Options.Save  ──Packets.Settings.Keybind/Volume/Option──▶  SettingsService
                                                                         checks name + value, rate limit
                                                                         writes data.Settings.*
```

Clients never write their own settings. `SettingsService` checks every name and value (and clamps and snaps option values to their step), with a TokenBucket of 30 writes per 10 s per player, since a dragged slider sends many.

```lua title="Services.SettingsService (the option handler)"
local function onOption(player: Player, optionName: string, value: number)
	if type(optionName) ~= "string" then
		return
	end
	local clean = PlayerSettings.CleanOption(optionName, value)
	if clean == nil or not bucket:allow(player.UserId) then
		return
	end
	local data = Data.WaitForData(player) :: any
	if data then
		data.Settings.Options[optionName].Set(clean)
	end
end
```

## `Shared.PlayerSettings`

| Member | What it is |
| --- | --- |
| `Actions` | Ordered rebindable actions `{ Name, Label, Default }` |
| `VolumeGroups` | Sound groups shown as sliders |
| `Options` | Sliders (`Min`, `Max`, `Step`, `Section`) and toggles (0/1 with Off/On text): `Fov`, `CameraBob`, `HoldSprint`, `HoldCrouch`, `MobileAutoSprint`, `SprintWhileReloading`, `AimAssist`, … |
| `ToInput(keyName)` | The `Enum.KeyCode` or `Enum.UserInputType` a saved key name means |
| `DefaultKey(action)` / `GetOption(name)` / `CleanOption(name, value)` / `IsVolumeGroup(name)` | Lookups and validation |
| `InteractGamepadKey`, `MeleeMouseButton`, `MeleeGamepadKey`, `ConsumableGamepadKey` | Fixed extra inputs |

```lua
local PlayerSettings = require(game.ReplicatedStorage.Modules.Shared.PlayerSettings)
print(PlayerSettings.DefaultKey("Reload"))        -- "R"
print(PlayerSettings.ToInput("MouseButton2"))     -- Enum.UserInputType.MouseButton2
print(PlayerSettings.CleanOption("Fov", 500))     -- clamped to the slider's Max
```

**Default keys:** Fire (MouseButton1), Aim (MouseButton2), Reload (R), Ability (F), Inspect (V), Melee (Q), Consumable (G), Crouch (LeftControl), Prone (C), Interact (E), Drone (5), DroneView (X), Play (K), Party (L), ClassAbility (T), Scoreboard (Tab), Settings (P). Keys are saved by name (`"R"`, `"One"`, `"MouseButton1"`); gamepad buttons are fixed.

**Adding an action or option:** add a row to `ACTIONS` or `OPTIONS` in `Shared.PlayerSettings`. Existing profiles get the new field with its default.

## Server: `SettingsService`

### `SettingsService.GetOption(player, optionName) → number`

A player's saved option, for server rules that depend on a setting. The option's default until their data loads; `0` for an unknown option.

```lua
local SettingsService = require(game.ServerScriptService.Modules.Services.SettingsService)
if SettingsService.GetOption(player, "SprintWhileReloading") == 1 then
	-- allow sprinting during a reload
end
```

## Client: `Keybinds`

```lua
local Keybinds = require(game.ReplicatedStorage.Modules.Client.Settings.Keybinds)
```

| Function | Returns / does | Example |
| --- | --- | --- |
| `Get(action)` | The bound `KeyCode`/`UserInputType` | `if input.KeyCode == Keybinds.Get("Reload") then reload() end` |
| `KeyName(action)` | The saved key name | `print(Keybinds.KeyName("Prone")) -- "C"` |
| `Label(action)` | Text for a key hint | `hint.Text = "[" .. Keybinds.Label("Interact") .. "] Repair"` |
| `Set(action, keyName)` | Rebinds and saves it; an action already on that key takes the old one. `false` if the key can't be bound | `if not Keybinds.Set("Prone", "Z") then warn("can't bind") end` |
| `Reset()` | Every key back to default | `Keybinds.Reset()` |
| `.Changed` | Signal: `(action, keyName)` | `Keybinds.Changed:Connect(function(action) refreshHints() end)` |

## Client: `Options`

```lua
local Options = require(game.ReplicatedStorage.Modules.Client.Settings.Options)
```

| Function | Returns / does | Example |
| --- | --- | --- |
| `Get(name)` | The current value | `camera.FieldOfView = Options.Get("Fov")` |
| `IsOn(name)` | A toggle is 1 | `if Options.IsOn("HoldSprint") then ... end` |
| `Set(name, value, previewOnly?)` | Applies it at once (cleaned like the server cleans it) **and saves it**, unless `previewOnly` | `Options.Set("Fov", 90)` |
| `Save(name)` | Sends it to the server if it changed since the last save | `Options.Save("Fov")` |
| `.Changed` | Signal: `(name, value)` | `Options.Changed:Connect(function(name, v) if name == "Fov" then apply(v) end end)` |

```lua
-- A slider: preview while dragging, save on release
Slider.Bind(row.Bar, function(alpha, released)
	local fov = 60 + alpha * 50
	Options.Set("Fov", fov, not released)
	if released then Options.Save("Fov") end
end)
```

`Slider.Bind(bar, onChange)` and `Slider.Show(row, alpha, text)` drive the Settings sliders. `PromptKeys.Key()` is the current Interact key; every ProximityPrompt follows it (a prompt with the `FixedKey` attribute keeps its own).

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Settings.Keybind` | Client → server | action, key name |
| `Settings.Volume` | Client → server | group, 0–1 |
| `Settings.Option` | Client → server | option, value |
