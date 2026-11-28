# Game Template asset

The framework every Mango Shark game shares, packed as one folder you install into a new place. It has no game
rules: no rounds, maps, guns, store or progression. Those come from the game itself or from
[separate systems](../systems/index.md).

[Download GameTemplate.rbxm](GameTemplate.rbxm){ .md-button .md-button--primary }

## Install it in a new place

1. Open the new place in Studio (a Baseplate is fine) and make a Folder named `MangoShark` in `ServerStorage`.
2. Right-click that folder, **Insert from File…**, and pick `GameTemplate.rbxm`.
3. Open the command bar (**View → Command Bar**) in Edit mode and run:

    ```lua
    require(game.ServerStorage.MangoShark.GameTemplate.Install)()
    ```

4. Open `ReplicatedStorage.Modules.Shared.Data` and change `ProfileStoreIndex` to the new game's own DataStore name.
5. Save the place, then press Play. Output shows Scribe starting on the server and client with no errors. Don't set
   the workspace attribute `ScribeNoSave` in a place that was never published: with no saved data to read, that
   mode kicks the player.

The installer prints `added N items, kept M of yours`. Items the place already has are **never overwritten**: they
are listed as "kept yours" and the template's copy stays in `ServerStorage.MangoShark.GameTemplate` to compare by
hand. Ctrl+Z undoes the install.

## What is in it

Every item goes to the same path in the new place.

| Where | Items | Job |
| --- | --- | --- |
| `ReplicatedStorage.ModuleLoader` | ModuleLoader, ParallelModuleLoader, actors | Requires every ModuleScript in the containers, then runs each one's `Init`, then `Start` |
| `ReplicatedStorage.config` | Empty settings table | Game-wide settings (`Services.PlayerJoin` requires it) |
| `ReplicatedStorage.Modules.Packages` | Scribe (data on ProfileStore), UI | Third-party: don't edit |
| `ReplicatedStorage.Modules.Utilities` | Packet, Signal, FastCast2, Cmdr, Zone, CameraShaker, Shime, NumberSpinner, KeycodeImages, EasyRagdoll, FormatNumber | Third-party: don't edit |
| `ReplicatedStorage.Modules.Shared` | `Data`, `Packets`, `UnreliablePackets`, `Extensions`, `PlayerSettings`, `ReadOnly` | Player data, every network message, extension points, keybinds and options |
| `ReplicatedStorage.Modules.Handlers` / `Helpers` / `Classes` | `StateHandler`, `AnimationHandler`, `HitPopup`; `TableHelpers`, `UIHelpers`; `Admins`, `HealthUI` | Player states, animations, hit numbers, admin list |
| `ReplicatedStorage.Modules.Client` | `Effects`, `Audio` (sound groups, volumes), `Settings` (menu, keybinds, options), `Core` (`Menus`, `UI`, `UIFeel`, `Notice`, `Tooltip`, `Peek`), `Interact.CustomPrompts`, `Combat.DamageFeedback`, `Guns.Quality` | Client framework: effects playback, the settings screen, menus, notices, damage flash |
| `ReplicatedStorage.Content` | `Effects` (Registry and Parts), `Theme`, `Icons` | Data: effects, UI colors and fonts, icons |
| `ReplicatedStorage.Assets` | The sounds and particles the template's effects use; UI row templates (`KeybindRow`, `VolumeRow`, `SliderRow`, `ToggleRow`, `NavButton`, `PromptCard`, `PromptStack`) | Assets |
| `ServerScriptService.Start` | Script | Starts the loader on the server |
| `ServerScriptService.Modules.Services` | `PlayerJoin`, `SettingsService`, `CmdrSetup` (F2 command bar, with `Announce`) | Join setup, saving settings, admin commands |
| `ServerScriptService.Modules.Systems` | `Effects.EffectService`, `Combat.Combat`, `Combat.DamageLog` | Server effects, `Combat.ApplyHit` (damage, friendly fire, kill credit) |
| `ServerScriptService.Modules.Helpers` / `Utilities` | `TokenBucket`, `SetCollisionGroup`; `MuchachoHitbox`, `BehaviorTreeCreator` | Rate limits, collision groups, hitboxes, behavior trees |
| `StarterPlayer` | `StarterPlayerScripts.Start`, `StarterCharacterScripts.Health` | Starts the loader on the client; turns off default health regeneration |
| `ReplicatedFirst.UILoader` | LocalScript with the `Main` ScreenGui: `Settings`, `MenuButtons`, `Notice`, `NoticeBackdrop`, `Tooltip`, `Health`, `Mobile`, `HitPopup`, `DamageFX` | Moves the UI into PlayerGui |

## How it differs from Gun Game

| Module | Change in the template |
| --- | --- |
| `Shared.Data` | Only `Coins`, `Kills`, `Deaths` and the fragments. No skins, crates, store products or migrations. Skips ScribeFragment modules inside `ServerStorage`, so an asset waiting to be installed never adds data |
| `Shared.Packets` | Only the `Effects`, `Combat`, `Settings` and `Example` groups. Merges child ModuleScripts (see below) |
| `Shared.UnreliablePackets` | Empty. Merges child ModuleScripts |
| `Content.Effects.Registry` | 12 general effects (`Hit`, `Explosion`, `Announcement`, the UI sounds, `Music`). Merges child ModuleScripts |
| `Services.CmdrSetup` | Only the `Announce` command. Gun commands come with the Gun System |
| Left out | Siege, matchmaking, lobby, classes, drones, NPCs, store, battle pass, progress, analytics, music, skins, breakables, soft walls |

## Adding systems without editing the template

A drop-in system adds to the template instead of changing it:

| To add | Do this | Example |
| --- | --- | --- |
| Packets | A child ModuleScript of `Shared.Packets` that returns `{ GroupName = { Name = Packet(...) } }` | `Shared.Packets.Guns` adds `Packets.Gun`, `Packets.Melee`, `Packets.Movement` |
| Unreliable packets | A child ModuleScript of `Shared.UnreliablePackets` that returns `{ Name = Packet(...) }` | `Shared.UnreliablePackets.Guns` |
| Effects | A child ModuleScript of `Content.Effects.Registry` that returns `{ EffectName = { ... } }` | `Content.Effects.Registry.Guns` |
| Saved data | A ModuleScript tagged `ScribeFragment` that returns `{ Template = { ... } }` | `Content.Guns.Loadouts` adds `Loadout` |
| Rules between systems | `Shared.Extensions` points (`Any`, `Product`, `Fire`) | `Gun.PreventFire`, `Gun.Killed` |

Children are read in name order. A packet group, packet or effect name may only be used once: a repeat stops the
game at load with a message naming both.

## Rules every game keeps

These come from Gun Game's [AI coding guide](../Gun%20Game/AI_CODING_GUIDE.md) and apply to every game on the
template:

- **One loader.** Everything is a ModuleScript under a Folder in a loaded container. No new Scripts or LocalScripts.
- **The server decides.** Clients send intent through `Shared.Packets`; server systems check it and own the state.
- **Content is data.** Tuning numbers live in `ReplicatedStorage.Content`.
- **UI is built in Studio.** Scripts find and change UI, they don't build it. Every feature works with keyboard and
  mouse, gamepad and touch.
- **Systems don't name each other** when an extension point will do.

## Updating the template

The template was taken from Gun Game on 2026-11-27 and lives in that place at
`ServerStorage.MangoShark.GameTemplate`. When a shared module changes in Gun Game:

1. Copy the changed module over the template's copy at the same path.
2. Right-click `ServerStorage.MangoShark.GameTemplate`, **Save to File…**, and save `GameTemplate.rbxm`.
3. Replace `game-templates/GameTemplate.rbxm` in this repository and add a line to [Changes](#changes).

!!! warning "Keep tags parked"

    CollectionService tags inside the asset are stored in a `MangoSharkTags` attribute instead of as real tags, so the
    running game never finds the copies (Gun Game's own `Shared.Data` would add a tagged `ScribeFragment` copy twice
    and stop). When you copy a tagged module into the asset, move its tags into that attribute. `Install` puts them back.

## Changes

| Date | Change |
| --- | --- |
| 2026-11-27 | First version, taken from Gun Game. 268 scripts; every one compiles. Installed from `GameTemplate.rbxm` into an empty Baseplate with the Gun System and played: player data loads, no errors in Output |
