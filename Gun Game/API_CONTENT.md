[Documentation home](index.md) / [API reference](API.md)

# Content and metadata reference

> **Scope:** Game data, Cmdr commands, attributes, tags and collision groups. Entries for older match modes are historical; consult the active system guide before using them.

## Content (data you edit)

| Module | What it holds / API |
| --- | --- |
| `Content.Guns.Definitions.*` | One file per gun (see [ADDING_GUNS.md](ADDING_GUNS.md)) |
| `Content.Match.Modes.*` | One file per match mode ([MATCH.md](MATCH.md)) |
| `Content.Match.Settings` | Every match setting and its range; `List`, `Get`, `Clean`, `Describe`, `DEFAULT_MODE` |
| `Content.Match.Teams` | Every team (Red, Blue, Green, Yellow); `List`, `Get` |
| `Content.Drones` | Every drone setting and attribute name ([DRONES.md](DRONES.md)) |
| `Content.Guns.Registry` | Every gun by Id, with defaults filled in: `Registry[gunId]` |
| `Content.Guns.Loadouts` | The loadouts; `Loadouts.Get(id)` |
| `Content.Guns.Skins.Skins` | `List`, `CRATE_PRICE` (499), `CRATE_REFUND_COINS` (500); `Get(id)`, `ForWeapon`, `Weapons`, `Choices`, `EquipField`, `Apply(model, skinId?, weaponId?)` |
| `Content.Guns.Melee` | Bash numbers; `Melee.For(gunId)` |
| `Content.Consumables.Consumables` | Loaded from one file per consumable in `Content.Consumables.Definitions`; `List`, `Get(id)`, `PER_LIFE` (2), `DEFAULT`, `THROW_COOLDOWN` |
| `Content.Guns.Abilities.*` | Ability hooks: `ModifyStats`, `OnFire`, `OnHit`, `CanPierce`, `OnAltFire`, `OnEquip`, `OnUnequip`, `OnReload`. Shipped: Scope, Ricochet, Burst, ExplosiveRounds, PumpShotgunSpread, SiegeShotgunSpread |
| `Content.Effects.Registry` | Every effect by name |
| `Content.Breakables.Registry` / `Definitions` | Board types (`Board`, `DoorBoard`) |
| `Content.Destruction.SoftWallConfig` | Soft wall settings and `Guns[Id]` (hole radius, penetration) |
| `Content.Movement.Config` | Speeds, heights, camera feel |
| `Content.NPC.Profiles` | NPC profiles (Soldier, Breacher, Grenadier) |

---

## Cmdr commands

Open the bar with **F2**, or the **CMD** touch button (shown only to admins in `Classes.Admins.UserIds`). The server checks `Classes.Admins` again for every command.

| Command | Arguments | What it does |
| --- | --- | --- |
| `givegun` | player, gunId | Gives a gun with full ammo |
| `spawnnpc` | profile, count? | Spawns NPCs in front of you (no respawn) |
| `clearnpcs` | — | Removes every NPC |
| `softwallpunch` (`swpunch`) | radius?, ring? | Holes the wall you look at; a ring knocks a disc out |
| `softwallreset` (`swreset`) | all? | Restores the wall you look at, or all |
| `nuke` | player | A warned strike that damages players, NPCs and boards nearby |
| `announce` | text | A banner for everyone (the example command) |
| `match` | start / end / restart | Starts the next match now, ends the running one, or restarts with the next setup |
| `matchmode` | mode | The next match's mode (TeamDeathmatch, FreeForAll, Elimination, …) |
| `range` (`showcase`) | — | Takes you to the gun animation range ([GUN_SHOWCASE.md](GUN_SHOWCASE.md)) |
| `matchset` | setting, value | One of the next match's settings: a number, or on/off |
| `movedebug` | — | Toggles the movement readout |
| `aimassistpc` (`aapc`) | player, on? | Turns controller aim assist on or off for that player on mouse and keyboard, for testing; leave out `on` to toggle |

Add a command: a `<Name>` definition and a `<Name>Server` module in `Services.CmdrSetup.Commands`.

---

## Attributes

Read them anywhere with `:GetAttribute`; the **server** sets them unless noted.

| Attribute | On | Meaning |
| --- | --- | --- |
| `InLobby` | Player | In the lobby (no guns) |
| `NPCMode`, `GuardRoom` | NPC model | `"Roam"` or `"Guard"` / the guarded `NPCRoom`'s name (`NPCService.SetMode`) |
| `Team` | Player, NPC model, SpawnLocation (you set) | A `Content.Match.Teams` Id: the player's team (our team system), an NPC's side, or which team a spawn belongs to |
| `GunAiming` | Player character, NPC model | Aiming down sights (players) or aiming at a target (NPCs); the third-person aim pose ([THIRD_PERSON_GUNS.md](THIRD_PERSON_GUNS.md)) |
| `Reloading` | Gun Tool | True while the gun reloads (the third-person reload) |
| `ModelScale` | Gun Tool | The third-person gun's scale (`GunService`); `Content.Guns.Skins.Skins` scales skins by it |
| `AimPitch` | NPC model | Where the NPC aims, radians up (the third-person aim pitch) |
| `DronesReady`, `DroneNextReady`, `DroneControlling` | Player | Drones ready to throw / server time the next comes back (0 for none) / looking through a drone (MovementController holds the body) |
| `DroneOwner`, `DroneSlot` (and `Team`) | Drone model | The owner's UserId / which of their drones |
| `Eliminated`, `MatchReturn` | Player | Sitting out a round (no-respawn modes) / sent to the lobby for it, back next round |
| `AimAssistPC` | Player | True gives aim assist on mouse and keyboard (the `aimassistpc` command) |
| `ConsumableId`, `ConsumableCount` | Player | The carried consumable and how many are left this life |
| `ConsumableId`, `DetonateAt`, `Thrower` | Thrown part in `workspace.Thrown` | What it is, the server time it goes off, who threw it (UserId or NPC name) |
| `SelectedMap` | Player | The map picked in the lobby hub |
| `<Gun>Skin` | Player | Equipped skin per gun |
| `Reloading`, `Stunned`, other states | Player | From `StateHandler` |
| `MoveState`, `MoveSpeedMultiplier`, `MoveViolations`, `StandHipHeight` | Player / character | Checked movement (`MovementService`) |
| `Sprinting`, `Crouching`, `Sliding`, `Prone` | Character (client) | The local movement prediction |
| `Shield` | Humanoid | Shield amount (`Combat`) |
| `GunId`, `Ammo`, `Reserve`, `Slot`, `WeaponSkin` | Gun Tool | The gun, its ammo and its slot |
| `NPCId`, `Profile`, `Team` | NPC model | NPC identity |
| `BreakableType`, `Health`, `MaxHealth`, `Intact`, `Total`, `Broken`, `Complete`, `Building`, `BuildProgress`, `KnifeHits`, `BulletHoles` | Board model | Board state |
| `SoftWallHoleRadius`, `SoftWallSupport` | Soft wall part (you set) | Per-wall hole size and support rule |
| `ClientOnly` | ModuleScript (you set) | ModuleLoader loads it on the client only |
| `PlaytestLock` | Workspace | Set while a playtest script is running |

## Tags

| Tag | Put it on | Effect |
| --- | --- | --- |
| `Board` / `DoorBoard` | A board part or model | Becomes a breakable board |
| `SoftWall` | A part | Bullets punch holes through it |
| `SoftWallDebris` | (set by the game) | Falling soft-wall pieces |
| `SkinShopPrompt` | A ProximityPrompt | Opens the skin shop (lobby only) |
| `NPC` | (set by the game) | Spawned NPCs |
| `NPCSpawn` | A part | An NPC spawn point. Attributes: `Profile`; `Mode = "Guard"` and optional `Room` (an `NPCRoom` part's name) spawn a room guard |
| `NPCRoom` | A part covering a room | A room a Guard-mode NPC keeps: it stays inside, patrols, and rebuilds the boards on or near its walls |
| `ScribeFragment` | A ModuleScript | Adds player data fields |
| `SmokeCloud` | (set by the game) | A live smoke cloud part, with a `Radius` attribute |
| `NPCSecure` | A part inside a room | Idle NPCs go clear that room, breaking in through boards or soft walls if they must; optional `Team` attribute |

## Collision groups

| Group | Who |
| --- | --- |
| `Player` | Every character part; doesn't collide with itself |
| `ProneBody` | The prone collision box |
| `SoftWallDebris` | Falling soft-wall pieces and debris chips; no player collision |
| `Thrown` | Thrown grenades and smoke bombs; no collision with `Player` or each other |
