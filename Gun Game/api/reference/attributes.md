# Attributes, tags and collision groups

Much of the game's state is **attributes** the server sets and clients read with `:GetAttribute`. The server sets them unless marked *you set* (a map or Studio setting) or *client*.

!!! warning "A player's class is never an attribute"

    Classes are secret from the other team. Use `ClassService.ClassOf(player)` on the server.

## Player

| Attribute | Meaning |
| --- | --- |
| `Team` | A `Content.Match.Teams` Id (`Attackers`, `Defenders`, …). Our own team system, not Roblox Teams |
| `InLobby` | In the lobby: no guns, most actions refused |
| `Level`, `TotalWins`, `WinStreak` | Account level (queue `MinLevel`), saved wins (lobby leaderboard), the streak above the head |
| `ConsumableId`, `ConsumableCount` | Carried consumable and how many are left this life |
| `DronesReady`, `DroneNextReady`, `DronesMax`, `DroneControlling` | Drone charges, next charge (server time), max out at once, looking through one |
| `DronesEnabled`, `DroneLockedIn`, `DroneLost` | No drone at all (false) / held in the drone's view / drone gone for good |
| `CameraViewing` | The CameraId they look through |
| `Reloading`, `Stunned`, `CantDoAnything`, other states | From `Handlers.StateHandler` |
| `MoveState`, `MoveSpeedMultiplier`, `MoveViolations`, `MoveCorrections` | The server's checked movement; speed violations; moves undone by the position check |
| `LeoSpottedUntil`, `LeoSpottedMessageUntil` | Caught moving by Leo's Motion Scanner (server time) |
| `DeadCallActive` | Being hacked by Caleb's Dead Call |
| `AimAssistPC` | Aim assist on mouse and keyboard (the `aimassistpc` command) |
| `<Gun>Skin` | Equipped skin per gun |
| `SelectedMap` | Lobby map pick |
| `Eliminated`, `MatchReturn` | Legacy match modes |
| `_ModulesLoaded` | The client's modules finished loading (ModuleLoader) |

## Character and Humanoid

| Attribute | On | Meaning |
| --- | --- | --- |
| `GunAiming` | Character, NPC model | Aiming down sights / at a target (third-person pose) |
| `Sprinting`, `Crouching`, `Sliding`, `Prone` | Character (client) | Local movement prediction |
| `StandHipHeight` | Character | Movement |
| `Shield` | Humanoid | Shield points (`Combat`) |
| `CountHits` | Humanoid | *You set*: every hit deals exactly 1 (training targets) |

## Guns and thrown things

| Attribute | On | Meaning |
| --- | --- | --- |
| `GunId`, `Ammo`, `Reserve`, `Slot`, `WeaponSkin` | Gun Tool | The gun, the server's ammo counts, its slot |
| `Reloading`, `ModelScale` | Gun Tool | Reloading (third-person), third-person scale |
| `ConsumableId`, `DetonateAt`, `Thrower` | Part in `workspace.Thrown` | What it is, server time it goes off, UserId or NPC name |

## Siege objects

| Attribute | On | Meaning |
| --- | --- | --- |
| `DroneOwner`, `DroneSlot`, `Team` | Drone | Owner UserId, which of their drones |
| `DroneLocked`, `ShieldedUntil` | Drone | Nobody may view or drive it / Drone Shield end (server time) |
| `CameraId`, `CameraName`, `Destroyed`, `Bulletproof`, `Team` | Camera in `workspace.SiegeCameras` | Camera state |
| `Gadget`, `GadgetOwner`, `Armed`, `Team` | Gadget in `workspace.SiegeGadgets` | Kind, owner UserId, a live mine |
| `Planted` | A bomb | A defuser is on it |
| `Detecting` | Proximity sensor | Someone is inside its volume |
| `LaserEmitter`, `LaserArmedAt`, `LaserDamage`, `LaserAlarmCooldown`, `LaserMarkTime` | Laser emitter | Laser gadget state and tuning |
| `ShieldRaised`, `ShieldDisabledUntil`, `ShieldPose`, `ShieldBashUntil`, `BallisticShieldOperator` | Character | The Shield class's ballistic shield |
| `LeoMotionScanStartsAt`, `LeoMotionScanEndsAt`, `LeoMotionScanWarningTextEndsAt` | Workspace | A Motion Scanner scan is running (server times) |
| `SiegeTestTeam` | Workspace (*you set*, Studio) | Puts everyone queued on that side |

## World

| Attribute | On | Meaning |
| --- | --- | --- |
| `BreakableType`, `Intact`, `Total`, `Health`, `MaxHealth`, `Complete`, `Reinforced` | Board model | Board state |
| `Broken` | Board piece | Hidden (broken) |
| `SoftWallHoleRadius`, `SoftWallSupport` | Soft wall part (*you set*) | Per-wall hole size and support |
| `Radius` | Smoke cloud | Its size |
| `NPCId`, `Profile`, `Team`, `NPCMode`, `GuardRoom`, `AimPitch` | NPC model | Identity, mode, guarded room, aim pitch |
| `TeleportTo` | Part tagged `Teleporter` (*you set*) | The part to send players to |

## Modules and workspace

| Attribute | On | Meaning |
| --- | --- | --- |
| `ClientOnly`, `ServerOnly`, `IgnoreLoader`, `LoaderPriority`, `Parallel` | ModuleScript (*you set*) | [How it loads](../foundations/modules.md#attributes-that-change-loading) |
| `ServerLoaded`, `ServerLoadedTimestamp` | Workspace | Server finished loading |
| `ScribeNoSave` | Workspace (*you set*, Studio, Edit mode) | Load profiles without ever saving |
| `PlaytestLock` | Workspace | A playtest script is running |
| `FixedKey` | ProximityPrompt (*you set*) | Keep its key: `PromptKeys` doesn't move it |
| `Tooltip` | GuiObject (*you set*) | Hover text |

## Tags

| Tag | Put it on | Effect |
| --- | --- | --- |
| `Board` / `DoorBoard` (and other breakable types) | A part or model | Becomes a breakable |
| `SoftWall` | A part | Bullets punch holes through it |
| `Camera` | A part or model in the map | A Siege security camera |
| `NPCSpawn` | A part | An NPC spawn (`Profile`; `Mode = "Guard"`, optional `Room`) |
| `NPCRoom` | A part covering a room | A room a Guard NPC keeps |
| `NPCSecure` | A part in a room | Idle NPCs go clear that room (optional `Team`) |
| `Teleporter` | A part | Sends players to its `TeleportTo` part |
| `ScribeFragment` | A ModuleScript | Adds player data fields |
| `SkinShopPrompt` | A ProximityPrompt | Opens the skin shop (lobby) |
| `FitScale` | A UIScale in a full-screen menu | Fit to the screen under the top bar |
| `SkinRainbow` (+ `RainbowOffset`) | Gun parts | Animated rainbow skin |
| Set by the game | | `NPC`, `SmokeCloud`, `SoftWallDebris`, `_BTree` |

## Collision groups

| Group | Who |
| --- | --- |
| `Player` | Every character part; doesn't collide with itself |
| `ProneBody` | The prone collision box |
| `Thrown` | Grenades, smoke, flashbangs; no collision with `Player` or each other |
| `SoftWallDebris` | Falling soft-wall pieces; no player collision |

## Runtime folders

`workspace.Enemies` (NPCs), `workspace.Drones`, `workspace.Thrown`, `workspace.SiegeCameras`, `workspace.SiegeGadgets`, `workspace.SiegeBombs`: made at runtime; don't place things in them by hand.
