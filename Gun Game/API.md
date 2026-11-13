# Gun Game API

Every function, hook, packet, command, attribute, tag and data field you can use to control the FPS place, in one page. Start with **Recipes** for common jobs, then look a module up by name. Signatures are copied from the code (2026-11-10). The other docs explain how each system works; this page is the reference.

**Paths used below:**

| Short name | Full path | Runs on |
| --- | --- | --- |
| `Systems.*`, `Services.*`, `Helpers.*` (server) | `ServerScriptService.Modules.*` | Server only |
| `Shared.*`, `Handlers.*`, `Helpers.*`, `Classes.*` | `ReplicatedStorage.Modules.*` | Both |
| `Client.*` | `ReplicatedStorage.Modules.Client.*` (attribute `ClientOnly`) | Client only |
| `Content.*` | `ReplicatedStorage.Content.*` (game data; loaded by ModuleLoader on both sides, most modules only return a table) | Both |

```lua
-- Server
local GunService = require(game.ServerScriptService.Modules.Systems.Guns.GunService)
-- Shared
local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)
-- Client
local Effects = require(game.ReplicatedStorage.Modules.Client.Effects)
```

Every module loads through ModuleLoader (`Init`, then `Start`). Require modules from your own module's `Init` or `Start`, or at the top. A loose `Script` or the Studio command bar gets its **own copy** of a module, not the running one, so test from a module or a temporary `Script`.

---

## Recipes

| I want to… | Do this (server unless noted) |
| --- | --- |
| Give a player a gun | `GunService.Give(player, "Rifle")`, or the command `givegun <player> <gunId>` |
| Give a player their loadout again | `LoadoutService.Apply(player)` |
| Give an NPC a gun | `GunService.GiveNPC(model, "Rifle")` |
| Fire a gun from code | `GunService.FireAs(GunService.ShooterOf(who), origin, direction, seed, spread)` |
| Cancel a reload | `GunService.CancelReload(player)` |
| Damage someone with kill credit | `Combat.ApplyHit(humanoid, 30, { Attacker = player, Item = "Trap" })` |
| Damage someone, no credit | `Combat.DealDamage(humanoid, 30)` |
| Knock someone back | `Combat.Knockback(character, direction, 60)` |
| Spawn NPCs | `NPCService.Spawn("Soldier", cframe)`, or `spawnnpc Soldier 3` |
| Make an NPC guard a room | Tag a part covering the room `NPCRoom`, then `NPCService.SetMode(npc, "Guard", roomPart)`, or give its `NPCSpawn` `Mode = "Guard"` |
| Remove every NPC | `NPCService.Clear()`, or `clearnpcs` |
| Break part of a board | `BreakableService.Damage(boardPartOrModel, 50, player, "Trap")` |
| Explosion damage to boards | `BreakableService.DamageRadius(position, 12, 100, player, "Explosion")` |
| Fix a board fully | `BreakableService.Reset(boardModel)` |
| Punch a hole in a soft wall | `SoftWalls.Punch(wallPart, hitPosition, direction, 0.3, player, "Trap")` |
| Put soft walls back | `SoftWalls.Reset(wall)` / `SoftWalls.ResetAll()`, or `softwallreset all` |
| Send a player to the arena / lobby | `LobbyService.SendToArena(player)` / `LobbyService.SendToLobby(player)` |
| Is a player in the lobby? | `LobbyService.IsInLobby(player)`, or the `InLobby` attribute (both sides) |
| Play a sound or effect for everyone | `EffectService.Play("BulletImpact", { CFrame = cf })` |
| Play an effect only for me (client) | `Effects.Play("Hitmarker", { Target = part })` |
| Block shots / bashes / sprint with a rule | `Extensions.Add("Gun.PreventFire", function(who, gunId, tool) return ... end)` (see **Extension points**) |
| Scale gun damage (perks, friendly fire) | `Extensions.Add("Gun.DamageMultiplier", function(who, gunId, humanoid, hit) return 1.5 end)` |
| React to a kill | `Extensions.Add("Gun.Killed", function(who, victimHumanoid, gunId, headshot) ... end)` |
| Change a player's move speed | `Extensions.Add("Movement.SpeedMultiplier", function(player, gunId) return 0.8 end)` |
| Give coins | `Data.Server` profile: `data.Coins.Increment(100)` (see **Player data**) |
| Read a player's setting on the server | `SettingsService.GetOption(player, "AimAssist")` |
| Read or change my setting (client) | `Options.Get("Fov")`, `Options.Set("Fov", 90)` then `Options.Save("Fov")` |
| Rebind a key (client) | `Keybinds.Set("Prone", "C")` |
| Open a menu (client) | `Menus.Open("SkinShop")`, `Menus.Close()` |
| Shake the camera (client) | `MovementCamera.Shake(3, 10, 0.1, 0.6)` |
| Use a product id | `ProductIds.Products.SkinCrate` (never type an id elsewhere) |
| Show a banner to everyone | the `announce <text>` command |
| Change the next match's mode or a setting | `MatchService.SetMode("FreeForAll")` / `MatchService.SetSetting("TimeLimit", 600)`, the Match menu (M, admins), or `matchmode` / `matchset` |
| Start, end or restart a match | `MatchService.StartNow()` / `EndNow()` / `Restart()`, or `match start\|end\|restart` |
| Give a team or player points | `MatchService.AddScore("Red", 1)` / `MatchService.AddScore(player, 1)` |
| A player's team / are two on the same team? | the `Team` attribute, `TeamService.TeamOf(player)` / `TeamService.AreAllies(a, b)` |
| Add a mode | a ModuleScript in `Content.Match.Modes` ([MATCH.md](MATCH.md)) |
| Throw a drone for a player / remove drones | `DroneService.Deploy(player, look)` / `DroneService.Clear(player?, refund?)` ([DRONES.md](DRONES.md)) |
| Every living drone | `DroneService.All()` (models in `workspace.Drones`) |
| Give grenades back / set the count | `ConsumableService.Refill(player)` / `ConsumableService.SetCount(player, 2)` |
| Set off a grenade or smoke anywhere | `ConsumableService.Detonate("Grenade", position, player)` |
| Is a line blocked by smoke? | `Smoke.Blocks(from, to)` (both sides) |

---

## Siege, matchmaking, classes, cameras (2026-11-12)

Everything added with Siege, in one place. The details are in [SIEGE.md](SIEGE.md), [MATCHMAKING.md](MATCHMAKING.md), [CLASSES.md](CLASSES.md) and [DRONES.md](DRONES.md). Where a row further down this page disagrees with this section, this section is right: the admin match controls, `Packets.Match.Admin`, the `match` / `matchmode` / `matchset` commands, the Match key, `Packets.Drone.Spot` / `Spotted` and the Team Deathmatch, Free-for-All and Elimination modes are archived.

### Recipes

| I want to… | Do this (server unless noted) |
| --- | --- |
| Know what kind of server this is | `ServerRole.Kind()`: `"Lobby"`, `"Match"` or `"Studio"` |
| Queue a player's party | `QueueService.Join(player, modeId?)` (the leader only; no mode: `Content.Matchmaking.DEFAULT_MODE`) |
| Add a queue mode (2v2, 3v3…) | Add a row to `Content.Matchmaking.MODES` ([MATCHMAKING.md](MATCHMAKING.md#queue-modes)) |
| Start a Siege match alone in Studio | Set the workspace attribute `SiegeTestTeam` to `Attackers` or `Defenders`, then press PLAY (K) |
| Know the Siege phase / a player's side | `SiegeService.Phase()` / `SiegeService.TeamOf(player)` |
| End the round now | `SiegeService.ForceEnd("Attackers", "BombsPlanted")` |
| Check the map | `SiegeMap.Load()` returns the map's info, or nil and warns every problem |
| Give a class / arm a player | `ClassService.Assign(player, "Breacher", guns?)` / `ClassService.Arm(player)` |
| Give guns that are not the saved loadout | `LoadoutService.Arm(player, { "Rifle", "Pistol" })` |
| Give a drone without a throw | `DroneService.Place(player, cframe)` |
| Show players a static mark | `DroneService.Mark(players, key, position, seconds)` |
| Add a security camera | `CameraService.Add(model, name, team, bulletproof)` |
| Change the plant time | `Extensions.Add("Siege.PlantTimeMultiplier", function(player, bombName) return 0.5 end)` |

### Server functions

| Function | What it does |
| --- | --- |
| `ServerRole.Kind()` / `IsLobby()` / `IsMatch()` / `IsLocal()` / `JobId()` | The server's role (`Systems.Matchmaking.ServerRole`) |
| `Store.Sorted(name)` / `Store.Hash(name)` / `Store.Publish(topic, message)` / `Store.Subscribe(topic, handler)` / `Store.Now()` | MemoryStore and MessagingService with retries; local stand-ins in Studio (`Systems.Matchmaking.Store`) |
| `Retry.Call(label, fn, attempts?)` | pcall, retries, exponential backoff (`Helpers.Retry`) |
| `TeamPacker.Pack(tickets, now, limits)` | The next match's two sides, or nil |
| `PartyService.Of(player)` / `Get(partyId)` / `Ensure(player)` / `IsLeader(player)` / `Owns(party)` / `UserIds(party)` | Parties |
| `PartyService.Park(party)` / `Restore(player, partyId)` / `SetTravelling(userId, on)` | Keeping a party through a match |
| `QueueService.Join(player, modeId?)` / `JoinPrivate(player)` / `Leave(player)` / `IsQueued(player)` | The queue. `modeId` is a `Content.Matchmaking.MODES` Id. `JoinPrivate` forms a match of the leader's party only, at once |
| `Content.Matchmaking.GetMode(id)` / `ModesIn(categoryId)` | A queue mode by Id (or nil) / the modes of one category |
| `MatchHost.Record()` / `TeamOf(userId)` / `ReturnAll()` / `Clear()` | The match server's record and the return to the lobby |
| `SiegeMap.Find()` / `Check(map)` / `Load()` | The Workspace map and its problems |
| `SiegeService.Phase()` / `IsPlaying(player)` / `TeamOf(player)` / `IsAlive(player)` / `Players(team?, aliveOnly?)` / `Site()` | The running match |
| `SiegeService.Reveal(defender)` / `ForceEnd(winner?, reasonKey)` | Show a defender's class to attackers / end the round |
| `SpectateService.Begin(player, delay, choices)` / `Stop(player)` / `StopAll()` / `Watching(player)` | Spectating after the death camera |
| `ClassService.Assign(player, classId, guns?)` / `ClassOf(player)` / `Arm(player)` / `Charges(player)` / `Clear(player)` / `Reset()` | Classes |
| `ClassService.Use(player, timestamp, origin, look)` | Every check, then the ability: ok, message |
| `Gadgets.Aim(context, range)` / `Place(kind, context, hit, health?)` / `OnDestroyed(model, fn)` / `Remove(model)` / `IsLive(model)` / `Blast(position, radius, damage, attacker, item)` / `Enemies(team)` / `Allies(team)` / `Clear()` | What abilities share (`Systems.Classes.Gadgets`) |
| `CameraService.Setup(sources, team)` / `Add(model, name, team, bulletproof)` / `List()` / `Stop(player)` / `Clear()` | Security cameras |
| `DroneService.Place(player, cframe)` / `Mark(players, key, position, seconds)` / `SetEnabled(player, on)` / `SetLockedIn(player, on)` / `Lock(player)` / `CanView(player)` | Drone controls for a game mode |
| `MatchService.BeginExternal(id, endsAt?)` / `SetClock(endsAt)` / `Finish(winner?)` / `Reset()` / `Kills(player)` / `Refresh()` | For the service that runs an `External` mode |
| `LoadoutService.Arm(player, guns)` | Gives exactly these guns and the knife |
| `LobbyService.Release(player)` | Out of the lobby without moving them |
| `DeathCamService.Release(player)` | Stop choosing who a dead player watches |

### Client

| Function | What it does |
| --- | --- |
| `Client.Core.UIFeel.Play(kind)` / `Pop(object)` / `Pulse(object)` | A UI sound (`Hover`, `Press`, `Open`, `Close`, `Confirm`, `Error`, `Tick`, `Notify`) / pop something in / a quick grow and settle. Needs a `UIScale` named `Feel` in the object ([UI.md](UI.md#feel)) |
| `Client.Hud.Nameplates.Refresh()` | Sets every other player's name and health display again: shown for teammates, hidden for enemies ([UI.md](UI.md)) |
| `Client.Core.Matchmaking.PlayWithParty()` | The lobby's PLAY WITH PARTY button |
| `Client.Core.Music.Play(kind)` / `.CurrentSong` / `.Playlist` | Crossfades to a random song of a kind (`Background`, `Start`, `Panic`, `End`) / the Sound playing now / the background folder ([MUSIC.md](MUSIC.md)) |
| `Client.Core.ModeMenu.Selected()` / `Pick(modeId)` / `Open()` / `.Changed` | The picked queue mode's Id / picks one / opens the Game Modes panel (`Menus` name `Modes`) / fires with the new Id |
| `Client.Core.Matchmaking.Play()` / `OpenModes()` / `OpenParty()` | The lobby's PLAY button (queue or cancel, for the picked mode) / opens the Game Modes panel (leader only, not while searching) / opens the Party menu (`Menus` name `Party`). The old Play menu is archived |
| `Client.Core.SiegeSelect` | No API: the selection and reveal screens |
| `Client.Hud.SiegeHud.UseAbility()` | Uses the class ability |
| `Client.Hud.Scoreboard` | No API: the scoreboard (hold Tab) |
| `Client.Gadgets.CameraController.Use()` / `View(model)` / `Cycle(direction)` / `Exit(tellServer?)` | Security cameras |
| `Client.Core.Spectate.Cycle(direction)` | Next or previous player to watch |
| `DroneController.Exit(force?)` | Leaving is refused while `DroneLockedIn`, unless forced |

### Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Party.Request` | Client → server, answered (ok, message) | action (`Invite`, `Accept`, `Decline`, `Leave`, `Kick`, `Promote`), argument |
| `Party.State` | Server → one client | `{ Id, Leader, Max, Members = { { UserId, Name, Here } } }` or nil |
| `Party.Invite` / `Party.InviteClosed` | Server → one client | PartyId, leader name, leader UserId, seconds / PartyId |
| `Queue.Request` | Client → server, answered (ok, message) | `Join`, `Private` (a match of the party only) or `Leave`, and the queue mode's Id (`""` for the default) |
| `Queue.State` | Server → one client | `{ Queued, Since, Status, Size, Mode }` |
| `Siege.State` | Server → one client | The match as their team may see it. During Selection also `Others` and `OtherTeam`: the other team's players as UserId, Name and Ready, nothing else |
| `Siege.Pick` | Client → server | kind (`Site`, `Spawn`, `Class`, `Gun`, `Ready`), value (`Ready`: `"1"` done picking, `"0"` changing picks) |
| `Siege.Plant` | Server → one attacker | bomb (`""` for none), server time it started, seconds |
| `Siege.Board` | Server → one client | Scoreboard rows, filtered for their team |
| `Siege.RequestState` | Client → server | — |
| `Class.Use` | Client → server, answered (ok, message) | server time, camera position, unit look |
| `Class.State` | Server → the owner only | `{ ClassId, Charges, ReadyAt, Guns }` or nil |
| `Class.Flash` | Server → one client | seconds blinded |
| `Camera.View` | Client → server, answered (ok) | CameraId, or `""` to stop |
| `Spectate.Next` / `Spectate.Mode` | Client → server / server → one client | 1 or -1 / `Team`, `Enemy` or `""` |
| `Drone.Scan` | Client → server, answered (scanned) | drone, unit look |
| `Drone.Marked` | Server → the scanner's team | key, position, seconds |

### Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Siege.PhaseChanged` | Fire | phase |
| `Siege.PreventPlant` / `Siege.PlantTimeMultiplier` | Any / Product | player, bombName |
| `Siege.Planted` / `Siege.SiteLocated` / `Siege.Ended` | Fire | player, bombName / player / winner?, reasonKey |
| `Party.PreventInvite` | Any | player, targetUserId |
| `Party.Changed` / `Party.Disbanded` | Fire | partyId |
| `Queue.PreventJoin` | Any | player |
| `Queue.Joined` / `Queue.Left` | Fire | partyId, ticket / partyId, reason |
| `Matchmaking.MatchFormed` / `Assigned` / `MatchReady` / `Arrived` | Fire | record / record / record / player, record |
| `Classes.PreventAbility` / `Classes.AllowBodiless` | Any | player, classId, ability / player, classId |
| `Classes.CooldownMultiplier` | Product | player, classId, abilityId |
| `Classes.AbilityUsed` / `Classes.Assigned` | Fire | player, classId, abilityId / player, classId |
| `Classes.GadgetPlaced` / `Classes.GadgetDestroyed` | Fire | player, kind, model / owner?, kind, model, killer? |
| Ability points | | `Classes.BreachDetonated`, `PreventFlash`, `FlashTimeMultiplier`, `Flashed`, `PreventPulseMark`, `Pulsed`, `PreventMineTrigger`, `MineDetonated`, `HealMultiplier`, `Healed` ([CLASSES.md](CLASSES.md#extension-points)) |
| `Camera.PreventView` / `Camera.PreventDamage` | Any | player, model / attacker, model |
| `Camera.Viewed` / `Camera.Destroyed` | Fire | player, model? / model, killer? |
| `Spectate.Changed` | Fire | viewer, model?, mode |
| `Drone.PreventRespawn` / `Drone.PreventView` | Any | player |
| `Drone.Spotted` | Fire | player, target, **position** (added) |
| `Lobby.PreventFirstSpawn` | Any | player |
| `Loadout.PreventApply` | Any | player |
| `Death.PreventSpectate` | Any | viewer |

### Content

| Module | What it holds |
| --- | --- |
| `Content.Matchmaking` | Party size, team sizes and minimums, waits, lifetimes, retry numbers, MemoryStore and topic names, the Studio settings |
| `Content.Siege` | Phase times, plant time, map folder names, bomb labels and colors, texts, win reasons |
| `Content.Classes` | Every class and ability; `Get`, `ForTeam`, `CategoryOf`, `Allows`, `Choices`, `GunCategories`, `HIDDEN` |
| `Content.Cameras` | Camera health, hit box, view limits, attribute names |
| `Content.Match.Modes.Siege` | The mode entry (`External = true`) |
| `Content.Match.Teams` | Also `Attackers` and `Defenders` |
| `Content.Drones` | Also `NO_SIGNAL_TIME` and the `DronesEnabled`, `DroneLockedIn`, `DroneLost`, `DroneLocked` attribute names; `SPOT_TIME` is 30, `SPOT_COOLDOWN` is 5 |

### Attributes, tags, folders, keys

| Name | On | Meaning |
| --- | --- | --- |
| `DronesEnabled`, `DroneLockedIn`, `DroneLost` | Player | No drone at all (false) / held in the drone's view / the drone is gone for good |
| `DroneLocked`, `ShieldedUntil` | Drone model | Nobody may view or drive it / the Drone Shield's end (server time) |
| `CameraViewing` | Player | The CameraId they look through |
| `CameraId`, `CameraName`, `Destroyed`, `Bulletproof` (and `Team`) | Camera model in `workspace.SiegeCameras` | Camera state |
| `Gadget`, `GadgetOwner`, `Armed` (and `Team`) | Gadget model in `workspace.SiegeGadgets` | Kind, owner UserId, a live mine |
| `Reinforced` | Board model | Reinforced by the Reinforcement Expert |
| `Planted` | A bomb in the map | A defuser is on it |
| `SiegeTestTeam` | Workspace (you set, Studio only) | Puts everyone queued on that side |
| Tag `Camera` | A part or model in the map | A security camera |
| `workspace.SiegeCameras`, `workspace.SiegeGadgets` | | Made at runtime |
| Keys | | `Play` (K), `Party` (L), `ClassAbility` (T) in `Shared.PlayerSettings.Actions`; the `Match`, `Loadout` and `GameMode` actions are gone. A player's class is **never** an attribute |

---

## Server: guns

### `Systems.Guns.GunService`

The server side of every gun: gives guns, checks and simulates every shot, reloads. Clients only send intent.

| Function | What it does |
| --- | --- |
| `GunService.Give(player: Player, gunId: string)` | Gives a gun Tool from `Content.Guns` with a full magazine and reserve |
| `GunService.GiveNPC(model: Model, gunId: string)` | Arms an NPC model; it shoots through the same path as players |
| `GunService.RemoveShooter(model: Model)` | Forgets an NPC shooter (on removal) |
| `GunService.ShooterOf(who: Player \| Model)` | The shooter record for a player or NPC, for `FireAs` / `ReloadAs` |
| `GunService.GetHeld(who: Player \| Model)` | The gun currently held (definition and tool), or nil |
| `GunService.Fire(player, timestamp: number, origin: Vector3, direction: Vector3, seed: number, spread: number)` | A player's trigger pull (what `Packets.Gun.Fire` calls) |
| `GunService.FireAs(shooter, origin, direction, seed, spread)` | Fires for any shooter, skipping the client checks (NPCs) |
| `GunService.Reload(player: Player)` / `GunService.ReloadAs(shooter)` | Starts a reload |
| `GunService.CancelReload(who: Player \| Model): boolean` | Cancels a reload in progress; true if one was cancelled |

### `Systems.Guns.LoadoutService`

| Function | What it does |
| --- | --- |
| `LoadoutService.Apply(player: Player)` | Gives the player's saved loadout (from `Content.Guns.Loadouts`), or takes guns away in the lobby |

### `Systems.Guns.AbilityRunner`

Runs gun abilities (`Content.Guns.Abilities`) on the server. Abilities normally call these through the context they're given.

| Function | What it does |
| --- | --- |
| `AbilityRunner.PlayEffect(name: string, options?)` | Plays an effect for everyone |
| `AbilityRunner.ApplyHit(ctx, humanoid, damage: number, headshot: boolean?)` | Ability damage with credit, hitmarker and `Gun.Killed` |
| `AbilityRunner.Hit(ctx, hit, bullet, deal?)` | The normal bullet-hit path (falloff, headshots, soft-wall multiplier, boards) |
| `AbilityRunner.Equip(ctx)` / `Unequip(ctx)` / `Reload(ctx)` | Runs abilities' `OnEquip` / `OnUnequip` / `OnReload` |
| `AbilityRunner.AltFire(ctx, active: boolean, source: "Aim" \| "Ability")` | Runs abilities' `OnAltFire` |

### `Systems.Combat.GunMelee` (gun bash)

| Function | What it does |
| --- | --- |
| `GunMelee.Swing(player, timestamp: number, direction: Vector3)` | A player's bash, with every check (what `Packets.Melee.Swing` calls) |
| `GunMelee.SwingAs(who: Player \| Model, direction: Vector3)` | A bash for anyone, skipping the client checks |
| `GunMelee.Query(character, origin, direction, settings)` | Finds what a bash would hit, without hitting it |

---

## Server: combat

### `Systems.Combat.Combat`

| Function | What it does |
| --- | --- |
| `Combat.ApplyHit(victimHumanoid, damage: number, options?: HitOptions)` | **The normal way to deal damage.** Shields, knockback, kill credit and the hit packet |
| `Combat.DealDamage(humanoid, damage: number, bypassShield: boolean?)` | Raw damage, shields first unless bypassed, no credit |
| `Combat.TryGiveShield(humanoid, chance: number, amount: number)` | Gives a shield with a chance (the `Shield` attribute) |
| `Combat.Knockback(character, direction: Vector3, speed: number)` | Pushes a character |
| `Combat.PlayHitEffects(character)` | The hit flash and sound |
| `Combat.CreateHitbox(character, options?)` | A cube hitbox in front of a character, owned by its player so the owner is never hit. Not started |

`HitOptions`: `KnockbackDirection: Vector3?`, `KnockbackSpeed: number?`, `BypassShield: boolean?`, `Attacker: (Player | Model)?` (kill credit), `Item: string?` (the kill feed's weapon name).

### `Systems.Combat.DamageLog`, `KillFeed`, `SwordCombat`

| Function | What it does |
| --- | --- |
| `DamageLog.Record(humanoid, attacker?, itemName: string?)` | Records who last hurt someone (`ApplyHit` does this) |
| `DamageLog.Last(victim, window: number)` | The last attacker and item within `window` seconds |
| `DamageLog.Clear(victim)` | Forgets a victim's record |
| `KillFeed.ReportDeath(humanoid)` | Sends a kill feed line for a death with a credited attacker |
| `SwordCombat:Attack(player, aimOrigin?, aimDirection?)` | A knife or sword swing (sword combat; don't change its behavior) |

---

## Server: world

### `Systems.Breakables.BreakableService` (boards)

`target` can be the board model or any part in it.

| Function | What it does |
| --- | --- |
| `BreakableService.IsBreakable(target): boolean` | Is this part of a breakable |
| `BreakableService.Get(target)` | The breakable's record (model, type, pieces) |
| `BreakableService.Damage(target, amount: number, attacker?, source: string?)` | Damages the top piece; leftover damage can spill to the next |
| `BreakableService.DamageRadius(position, radius, amount, attacker?, source?, ignore?): number` | Damages every breakable in a radius; returns how many were hit |
| `BreakableService.RemoveCoating(target)` | Strips the spray paint only |
| `BreakableService.Repair(target, player?, expectedPiece?)` | Puts back the next piece (in order) |
| `BreakableService.Reset(target)` | Makes the board whole |
| `BeginRepairHold` / `CompleteRepairHold` / `EndRepairHold` / `CancelRepairHold(target, player)` | The hold-E repair prompt's steps |

### `Systems.Destruction.SoftWalls`

| Function | What it does |
| --- | --- |
| `SoftWalls.Punch(target, position, direction?, radius?, attacker?, source?): boolean` | Queues a hole (radius: the caller's, else `Sources[source]`, else the wall's, else the default) |
| `SoftWalls.IsSoftWall(part): boolean` | Is this a soft wall or a piece of one |
| `SoftWalls.SourceOf(part)` | The original tagged wall a piece came from |
| `SoftWalls.Reset(target)` / `SoftWalls.ResetAll()` | Puts one wall / every punched wall back |
| `SoftWalls.Stats()` | Counters (rebuilds, debris) for debugging |

### `Systems.Consumables.ConsumableService` (grenade, smoke)

See [CONSUMABLES.md](CONSUMABLES.md).

| Function | What it does |
| --- | --- |
| `ConsumableService.Get(player): (Consumable?, number)` | The carried consumable and how many are left |
| `ConsumableService.Refill(player)` | Saved kind, count back to `PER_LIFE` (2); runs on every spawn |
| `ConsumableService.SetCount(player, count)` | Clamped to 0..`PER_LIFE` |
| `ConsumableService.Throw(player, direction): BasePart?` | Every check, then a throw |
| `ConsumableService.Detonate(id, position, attacker?): boolean` | A grenade blast or a smoke cloud there, no throw. `attacker` is a Player or an NPC model |
| `ConsumableService.ThrowAs(model, id, start, velocity): BasePart?` | A throw for a server-side thrower (NPCs), with an exact launch velocity and no player checks |

### `Systems.Match.MatchService` and `Systems.Match.TeamService`

See [MATCH.md](MATCH.md): modes, settings, teams, the match API for mode hooks.

| Function | What it does |
| --- | --- |
| `MatchService.SetMode(id): boolean` | The next match's mode (its default settings) |
| `MatchService.SetSetting(name, value): any` | One of the next match's settings, cleaned; nil if refused |
| `MatchService.StartNow()` / `EndNow()` / `Restart()` | Start now / end now (leader wins) / new match with the next setup |
| `MatchService.AddScore(teamIdOrPlayer, amount)` | Points from anything (objectives); reaching `ScoreLimit` wins |
| `MatchService.OnPlayerDeath(victim, killer?)` | KillFeed reports player deaths here |
| `MatchService.Phase()` / `Mode()` / `Setting(name)` / `ModeIds()` | The running match |
| `TeamService.Setup(ids)` / `Active()` / `Assign(player, id?)` / `Remove(player)` | Teams of a match; a player's team (nil = smallest) |
| `TeamService.TeamOf(who)` / `Members(id, arenaOnly?)` / `Smallest()` / `Balance()` | Team lookups (players, characters, NPC models) |
| `TeamService.AreAllies(a, b)` / `SpawnFor(player)` | Same team? / where to spawn |

### `Systems.Combat.DeathCamService`

See [DEATH_SCREEN.md](DEATH_SCREEN.md).

| Function | What it does |
| --- | --- |
| `DeathCamService.KillerOf(victim)` | The last recorded killer of a player or NPC model, or nil |
| `DeathCamService.Watching(player)` | Who a dead player is spectating (Player or NPC model), or nil |

### `Systems.Drones.DroneService`

See [DRONES.md](DRONES.md).

| Function | What it does |
| --- | --- |
| `DroneService.Deploy(player, look): Model?` | Every check, then throws a drone along the unit look |
| `DroneService.Spot(player, drone, look): boolean` | Spots the enemy the drone looks at for the player's team |
| `DroneService.Clear(player?, refund?)` | Removes a player's drones (nil: everyone's); refund gives the charges back now |
| `DroneService.Of(player)` / `DroneService.All()` | A player's living drones (by slot) / every living drone |

### `Systems.Lobby.LobbyService`

| Function | What it does |
| --- | --- |
| `LobbyService.IsInLobby(player): boolean` | Same as the `InLobby` attribute |
| `LobbyService.SendToArena(player)` | Moves to a random arena spawn, `InLobby` false, gives the loadout |
| `LobbyService.SendToLobby(player)` | Moves to `LobbySpawnPoint`, `InLobby` true, takes the guns |
| `LobbyService.SelectMap(player, mapId: string)` | The lobby hub's map choice (`SelectedMap` attribute) |

### `Systems.NPC.NPCService` and `Systems.NPC.Brain`

| Function | What it does |
| --- | --- |
| `NPCService.Spawn(profileId: string, where: CFrame, spawnPart: BasePart?)` | Spawns an NPC from `Content.NPC.Profiles` into `workspace.Enemies`. Refused past `MAX_NPCS` (10) |
| `NPCService.Clear()` | Removes every NPC |
| `NPCService.Count()` / `NPCService.ProfileNames()` | How many are alive / the profile names |
| `NPCService.Agents()` | The live agents (`Brain.Agent`), read only, for tests and debug tools |
| `NPCService.SetMode(model, mode: string, room: BasePart?): boolean` | `"Guard"`: the NPC stays in the `NPCRoom` part (nil: the one it stands in), patrols it, repairs its doors and windows and fights first; `"Roam"`: normal ([ADDING_NPCS.md](ADDING_NPCS.md), Guard mode) |
| `Tactics.Danger` / `Vault` / `Fortify` / `Pursue` / `Suspicion` / `Breach` / `TryGrenade(agent, now)`, `Tactics.OnHurt(agent, attacker)` | The reflexes around the tree (dodge grenades, climb windows, board up doors and windows, chase a target behind glass, shoot to test, break in or out, throw, turn toward a hit); see [ADDING_NPCS.md](ADDING_NPCS.md) |
| `Brain.*` | Helpers behavior-tree tasks use: `CanSee` (sees through windows), `SeeThrough`, `Penetrable`, `ShootThrough`, `BreachPoint`, `FindEntry`, `Connected`, `Ground`, `FindExit`, `FindFortify`, `BlockedAhead`, `Blocked` (soft walls and boards aren't cover), `AimPoint`, `Eye`, `MoveTo`, `MoveDirect`, `Stop`, `IsMoving`, `Ammo`, `IsReloading`, `SetLastKnown`, `FlatDistance`, `NewPath`, `AdvancePath` |
| Tasks (`Systems.NPC.Tasks.*`) | `FindTarget`, `HasLineOfSight`, `InRange`, `LowHealth`, `NeedsReload`, `MoveToCover`, `Reload`, `AimAndShoot`, `Strafe`, `Chase`, `Patrol`: each has `run(agent)`, some `start` / `finish`. See [ADDING_NPCS.md](ADDING_NPCS.md) |

### `Systems.Movement.MovementService`

| Function | What it does |
| --- | --- |
| `MovementService.GetState(player)` | The checked movement state (`Walk`, `Sprint`, `Crouch`, `Slide`, `Prone`, …) |
| `MovementService.IsCrouched(player): boolean` | Crouched, sliding or prone |
| `MovementService.BlocksFire(player, gun): boolean` | True while sprinting blocks this gun (`SprintOutTime`) |

### Other server services

| Function | What it does |
| --- | --- |
| `EffectService.Play(name, options?, except: Player?)` | Plays a `Content.Effects.Registry` effect on every client (optionally not one) |
| `EffectService.Stop(name, target?, data?)` | Stops a held effect |
| `SkinShopService.StyleTool(player, tool)` | Applies the player's equipped skin to a gun Tool |
| `SettingsService.GetOption(player, optionName)` | A player's saved option (`Shared.PlayerSettings.Options`) |
| `Helpers.TokenBucket.new(capacity, windowSeconds)` | A rate limiter; `:allow(userId): boolean`, `:remove(userId)` |
| `Helpers.SetCollisionGroup(model, group)` | Puts every part of a model in a collision group |
| `Helpers.WebHook:SendJoinMessage(player)` | The (off) join webhook |
| `Services.PlayerJoin` | No API: puts characters in the `Player` collision group |

---

## Shared

### `Shared.Extensions`: extension points

Content changes core behavior by adding handlers. With no handlers, `Any` is false, `Product` is 1 and `Fire` does nothing.

| Function | What it does |
| --- | --- |
| `Extensions.Add(point: string, handler): () -> ()` | Adds a handler; returns a function that removes it |
| `Extensions.Fire(point, ...)` | Calls every handler (a notification) |
| `Extensions.Any(point, ...): boolean` | True if any handler returns true (a veto) |
| `Extensions.Product(point, ...): number` | Multiplies every handler's number (a multiplier) |

Handlers are global: check that the player has the thing before acting. Errors are caught and warned. A new point needs no registration; just call it by a new name.

**Every point in the game:**

| Point | Kind | Arguments | Use |
| --- | --- | --- | --- |
| `Gun.PreventFire` | Any | who, gunId, tool | Stop a shot |
| `Gun.DamageMultiplier` | Product | who, gunId, humanoid, hit (nil for ability or bash damage) | Scale damage; NPCs use it to turn off friendly fire |
| `Gun.Hit` | Fire | who, humanoid, hit, gunId | A bullet hit a humanoid |
| `Gun.Killed` | Fire | who, victimHumanoid, gunId, headshot | A gun or bash kill, once per death |
| `Gun.Reloaded` | Fire | who, tool, gunId | A reload finished |
| `Gun.Fired` | Fire | who, gunId, origin | Every shot that goes off, players' and NPCs' (NPCs hear shots through it) |
| `Combat.PreventFriendlyFire` | Any | attacker, victimCharacter, humanoid | Cancel a hit in `Combat.ApplyHit` (MatchService blocks teammates unless `FriendlyFire` is on) |
| `Match.Started` / `Match.RoundStarted` | Fire | modeId / modeId, round | A match / a round started |
| `Match.Scored` | Fire | target, amount | A team (Id) or player scored |
| `Match.Ended` | Fire | modeId, winner? | A match ended (team Id, Player, or nil for a draw) |
| `Team.Changed` | Fire | player, oldTeam?, newTeam? | A player's team changed |
| `Combat.Death` | Fire | victim (Player or NPC model), attacker?, item? | Every death `KillFeed.ReportDeath` handles, credited or not, before the damage log is cleared |
| `Drone.PreventDeploy` | Any | player | Stop a drone throw |
| `Drone.Deployed` / `Drone.Destroyed` | Fire | player, drone / player, drone, killer? | A drone was thrown / destroyed |
| `Drone.Noise` | Fire | drone, position, share | A drone driving (NPCs hear it within share of their hearing range) |
| `Drone.Spotted` | Fire | player, target | A player spotted an enemy with a drone |
| `Gun.PreventMelee` | Any | who, gunId, tool | Stop a gun bash |
| `Gun.MeleeHit` | Fire | who, kind, instance, humanoid?, gunId | A bash landed; kind is `Humanoid`, `Breakable`, `SoftWall` or `Surface` |
| `Combat.BlockHit` | Any | humanoid, damage | Cancel a hit |
| `Combat.Damage` / `Combat.Hit` | Product / Fire | attacker / attacker, humanoid | Generic combat damage scale / after a hit |
| `Combat.PreventSwing` | Any | player | Stop a sword swing |
| `Combat.SwordHit` | Fire | player, victimHumanoid | A sword hit landed |
| `Combat.WeaponScale` | Product | tool | Grow the sword hitbox |
| `Breakable.PreventDamage` | Any | who, model, amount, source | Protect a board |
| `Breakable.DamageMultiplier` | Product | who, model, source | Scale board damage |
| `Breakable.PieceBroken` / `Breakable.Broken` | Fire | who, model, piece?, source | A piece came off / the board is fully broken |
| `Breakable.PreventRepair` | Any | player, model, piece | Stop a repair |
| `Breakable.Repaired` | Fire | player, model, piece | A piece went back |
| `SoftWall.PreventPunch` | Any | who, wall, source | Stop a hole |
| `SoftWall.PieceFell` | Fire | who, wall, piece | A chunk fell out |
| `Movement.PreventSprint` | Any | player, state | Refuse sprint / tactical sprint |
| `Movement.PreventSlide` / `Movement.PreventProne` | Any | player | Refuse slide / prone |
| `Movement.SpeedMultiplier` | Product | player, gunId? | Scale every move speed (sent to the client as `MoveSpeedMultiplier`) |
| `Consumable.PreventThrow` | Any | player, id | Stop a grenade or smoke throw |
| `Consumable.DamageMultiplier` | Product | attacker?, id, humanoid | Scale grenade damage |
| `Consumable.Thrown` | Fire | player, id, projectile | After a throw |
| `Consumable.Detonated` | Fire | attacker?, id, position | After a blast or smoke pop |

### `Shared.Data`: player data (Scribe)

```lua
local Data = require(game.ReplicatedStorage.Modules.Shared.Data)
local data = Data.Server.WaitForData(player)   -- server; nil if the player left
data.Coins.Increment(100)
data.WeaponSkins.Has("Rifle_Gold")
-- client: Data.Client.WaitForData(); Data.Client.Kills.Observe(function(value) ... end)
```

| Field | Type | Meaning |
| --- | --- | --- |
| `Coins` | Int, min 0 | Currency; the crate refund adds 500 |
| `Kills`, `Deaths` | Int, min 0 | Career stats (lobby hub) |
| `WeaponSkins` | Set of skin Ids | Owned skins; only the crate grants them |
| `<Gun>Skin` (`RifleSkin`, …) | Enum | Equipped skin per gun, or `"None"` |
| `Settings.Keybinds.<Action>` | String | Saved key names (`Shared.PlayerSettings`) |
| `Settings.Volumes.<Group>` | Number 0–1 | Sound volumes |
| `Settings.Options.<Option>` | Number | Options (toggles are 0 / 1) |
| Saved loadout | String | The picked loadout Id |
| `Consumable` | String | The picked consumable Id (`Grenade` or `Smoke`), from `Content.Consumables` |

Add fields from a new module without editing `Shared.Data`: tag a ModuleScript `ScribeFragment` that returns `{ Template = { ... }, ServerStore = { ... } }`. Each root name may only be used once.

**Products:** `SkinCrate` (id in `Shared.ProductIds`) grants one unowned skin, or 500 coins if every skin is owned.

### `Shared.ProductIds`

| Member | What it is |
| --- | --- |
| `ProductIds.Products.SkinCrate` | `3730208338`: "Skin Crate", 499 Robux |
| `ProductIds.GamePasses` | Empty; add passes here |
| `ProductIds.IsSet(id): boolean` | False for the `0` "not created" placeholder |

### `Shared.PlayerSettings`

| Member | What it is |
| --- | --- |
| `Actions` | Every rebindable action and default key (Fire, Aim, Reload, Ability, Inspect V, Melee Q, Consumable G, Sprint, Crouch LeftControl, Prone C, Slot1–4, Interact E, Loadout B, Settings P, Scoreboard Tab, Match M, Drone 5 (in / out / throw), DroneView X (leave drone)) |
| `Options` | Every option: `Fov` (60–110), `CameraBob`, `HoldSprint`, `HoldCrouch`, `MobileAutoSprint`, `SprintWhileReloading`, `AimAssist`. Add one here and the Settings menu shows it |
| `VolumeGroups` | The sound groups with sliders |
| `ToInput(name)` / `DefaultKey(action)` / `GetOption(name)` / `CleanOption(name, value)` / `IsVolumeGroup(name)` | Helpers |
| `InteractGamepadKey`, `MeleeMouseButton`, `MeleeGamepadKey`, `ConsumableGamepadKey` (DPad Right) | The fixed extra inputs |

### `Shared.Packets` and `Shared.UnreliablePackets`

Server: `packet.OnServerEvent:Connect(function(player, ...) end)`, `packet:FireClient(player, ...)`, `packet:Fire(...)` (all). Client: `packet:Fire(...)`, `packet.OnClientEvent:Connect(...)`. Answered packets use `:Response(...)`.

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Effects.Play` / `Effects.Stop` | Server → clients | effect name, options |
| `Combat.Hit` | Server → all | character, damage |
| `Combat.KillFeed` | Server → all | killer, victim, item |
| `Combat.Swing` | Client → server | sword aim origin, direction |
| `Gun.Fire` | Client → server | server time, origin, direction, seed, spread |
| `Gun.Reload` / `Gun.Aim` / `Gun.AltFire` | Client → server | — / aiming / pressed |
| `Gun.HitConfirm` | Server → shooter | headshot, killed |
| `Gun.Loadout` | Client → server | loadout Id |
| `Melee.Swing` | Client → server | server time, look direction |
| `Consumable.Throw` / `Consumable.Pick` | Client → server | server time, look direction / consumable Id |
| `Match.State` | Server → clients | the match snapshot (phase, mode, timer, teams, players, next setup) |
| `Death.Killed` | Server → the player who died | killer name ("" for none), killer UserId (0 for an NPC or none), weapon, seconds to respawn (-1: out until the next round) |
| `Death.Spectate` | Server → a dead player | who to watch now (a model, or nil for nobody), name |
| `Match.RequestState` | Client → server | — |
| `Match.Admin` | Client → server, answered (ok, message) | action (`Mode`, `Setting`, `Start`, `End`, `Restart`), argument; admins only |
| `Drone.Deploy` | Client → server | unit look direction |
| `Drone.View` | Client → server | looking through a drone (true / false) |
| `Drone.Spot` | Client → server, answered (spotted) | drone, unit look direction |
| `Drone.Spotted` | Server → the spotter's team | target model, seconds |
| `Skins.Equip` / `Skins.BuyCrate` | Client → server, answered (ok, message) | skin Id / — |
| `Lobby.SelectMap` | Client → server, answered | map Id |
| `Settings.Keybind` / `Volume` / `Option` | Client → server | name, value |
| `Movement.SetState` / `Movement.Correct` | Client → server / server → client | state |
| `Example.Ping` / `Example.Pong` | Example only | text |
| `UnreliablePackets.GunFired` | Server → nearby | UserId, gunId, origin, direction, seed, spread (cosmetic tracers) |
| `UnreliablePackets.GunAim` / `GunAimRelay` | Client → server / server → others | aim pitch (third-person arms) |

### Gun math (`Shared.Guns.*`)

| Function | What it does |
| --- | --- |
| `Ballistics.NewShot(gun, player?, tool?, origin, direction, seed, spread, isServer, isLocal, playEffect)` | Builds a shot context |
| `Ballistics.Prepare(ctx, out)` / `Fire(ctx, origin, direction, index, onHit)` / `Trace(...)` | Pellet directions, simulated bullets, hitscan |
| `Ballistics.Falloff(gun, distance)` | Damage multiplier at a distance |
| `Ballistics.IsHeadshot(part)` / `HumanoidOf(part)` / `IsSoftWall(part)` / `PlayerFromId(userId)` | Hit helpers |
| `Ballistics.Caster(gun)` / `Filter(ctx)` / `Hit(result, origin)` | Internals for simulated bullets |
| `Spread.Angle(gun, aiming, moveAlpha, bloom, stance?)` / `MinAngle` / `Direction` / `Fill` / `Recover` | Spread cone and bloom |
| `Abilities.Call(gun, hook, isServer, ...)` / `Any` / `Runs` / `SideOf` / `CanPierce` | Runs a gun's ability hooks |
| `Spring.new(speed, damper)` → `:Update(dt)`, `:Impulse(v)`, `:Reset(pos?)` | The spring used by recoil and camera |

### Other shared modules

| Function | What it does |
| --- | --- |
| `Shared.Movement.States.Can(from, to)` / `IsState(name)` | Allowed movement state changes |
| `Shared.Smoke.Blocks(from, to): boolean` | True if the line crosses a smoke cloud's core (NPC sight, aim assist) |
| `Shared.CursorAim.Ray(): (origin, direction)` | The local aim ray (screen center when locked) |
| `Shared.ReadOnly.Wrap(node, label)` | A read-only view of a table |
| `Handlers.StateHandler` | `SetState(plr, key, value, duration)`, `GetState`, `ReturnStates`, `RemoveStates`, `SetStun(plr, value, duration, stunSpeed)`, `ClearAllState`. Sets player attributes like `Reloading`, `Stunned` |
| `Handlers.AnimationHandler` | `LoadAnim(char, type, animId, keyframeCallback?, keyframes?, looped?, delay?)`, `StopAnim`, `RemoveAnim`, `IsAnim`, `GetAnims`, `PreloadAnimations`, `PlayAnimationEveryone`, `StopAnimationEveyone` (sic) |
| `Handlers.HitPopup.Show(model, amount)` | A floating damage number |
| `Classes.HealthUI` | `ConstructHealthBar`, `HealthChanged`, `ShieldChanged`: health bar helpers |
| `Helpers.TableHelpers` | `TableLength(t, useCache?)`, `CreateWatchedTable(t, onChanged)` |
| `Helpers.UIHelpers` | `:GetPlayerThumbnailIcon(player)`, `:ConvertToMMSS(seconds)` |

---

## Client

### Effects and audio

| Function | What it does |
| --- | --- |
| `Client.Effects.Play(name, options?)` / `Effects.Stop(name, target?, data?)` | Plays a `Content.Effects.Registry` effect locally (options: `Target`, `CFrame`, `Variant`, `Data`, …) |
| `Client.Guns.GunEffects.Play(name, options?)` / `LocalShot(ctx, directions, muzzle?)` | Gun effects; your own shot's tracers and flash |
| `Client.Guns.Quality.Scale()` / `Count(n)` | The effect quality factor and a particle count scaled by it |
| `Client.Audio.AudioSettings.Get(group)` / `GetAll()` / `Set(group, volume)` | Volumes |
| `Client.Audio.SoundGroups.Get(name?)` / `Assign(sound, name?)` / `Master()` | Sound groups |

Effect parts (`Content.Effects.Parts.*`), each `Play(spec, context)`: `Animation`, `Banner`, `ColorFade`, `Debris`, `Dust`, `Highlight`, `Impact`, `JointSwing`, `MuzzleFlash`, `Particles`, `PooledSound`, `Shards`, `Shell`, `Sound`, `Template`. Inside a part, `context` has `Add(instance, lifetime?)`, `Delay(seconds, fn)`, `Hold()`, `Keep(seconds)`, `OnStop(fn)`, `Anchor()`, `Group()`, `Stop(data?)` and `context.Data`.

### Guns (client)

| Function | What it does |
| --- | --- |
| `Viewmodel.Equip(gun, tool, modelName?, melee?)` / `Unequip()` | First-person gun |
| `Viewmodel.SetAiming(bool)` / `AimAlpha()` / `SetFov(fov?)` / `SetHidden(bool)` / `IsFirstPerson()` / `Ready()` | Aim and view state |
| `Viewmodel.Kick(recoil, rng?, stance?)` / `Muzzle()` | A shot's kick / the muzzle attachment |
| `Viewmodel.Inspect()` / `Bash()` / `Swing()` / `Reloading()` / `FinishReloading()` and `IsInspecting()` / `IsBashing()` | Actions |
| `Viewmodel.SetSkin()` | Re-applies the equipped skin |
| `Viewmodel.GunModel.*` | `Get`, `ApplySkin`, `SkinOf`, `Bounds`, `Scaled`, `MakeLocal`, `NearPush` |
| `GunHud.Show(gun)` / `ShowMelee()` / `Hide()` / `SetAmmo(ammo, reserve)` / `SetReloading(bool)` / `Crosshair(spread, aimAlpha)` / `Hitmarker(headshot, killed)` / `SetAimToggle(bool)` / `MobileButtons()` | The gun HUD. `MobileButtons()` returns Fire, Aim, Reload and Bash |
| `WeaponSlots.Equip(index)` / `Cycle(step)` | Switch weapons |
| `LoadoutMenu.Pick(id)` | Picks a loadout |
| `Client.Guns.Consumables.Throw()` / `Pick(id)` | Throws one (G) / picks grenade or smoke |
| `AimAssist.SetGun(gun?)` / `Update(dt, camera, turnPitch, turnYaw, aimAlpha)` | See [AIM_ASSIST.md](AIM_ASSIST.md) |
| `Recoil.ShotKick` / `Scale`, and `Recoil.Pattern` / `Camera` / `View` classes | Recoil math (see [ADDING_GUNS.md](ADDING_GUNS.md#recoil-fields)) |

### Movement and camera (client)

| Function | What it does |
| --- | --- |
| `MovementController.State()` / `Stance()` / `IsSprinting()` / `IsForcedCrouch()` | The local movement state |
| `MovementController.CancelSprint()` / `SprintEndedAt()` / `SprintOutScale()` | Sprint control |
| `MovementController.SetGunBlock(bool)` / `SetReloading(bool)` | Tell movement a gun is busy |
| `MovementCamera.Shake(magnitude, roughness, fadeIn, fadeOut)` | Camera shake |
| `MovementCamera.SetAim(alpha, gunAdsFov?)` / `SetFovOverride(fov?)` / `ScaledFov(fov)` | FOV control |
| `MovementCamera.ConfigureRecoil(gun)` / `AddRecoil(pitch, yaw)` / `Recoil(impulse)` / `SetRecoilSpeed(s)` / `RecoilSpeed()` / `ShotKick(roll, rng)` / `Offset()` | Recoil and camera offsets |
| `MovementDebug.Toggle()` | The movement readout (`movedebug`) |

### Menus, settings, input (client)

| Function | What it does |
| --- | --- |
| `Menus.Register(name, frame)` / `Open(name)` / `Close(name?)` / `Toggle(name)` / `IsOpen()` / `SetMouseIconAfterClose(bool)` | One menu at a time, frees the mouse. Names: `Loadout`, `Settings`, `Match`, `SkinShop`, `Career`, `Backpack`, `MapSelection` |
| `Client.Hud.MatchHud` | No API: the match HUD, scoreboard (Tab), result banner, teammate outlines |
| `Client.Hud.DeathScreen` | No API: the death screen and spectate camera ([DEATH_SCREEN.md](DEATH_SCREEN.md)) |
| `Client.Guns.ThirdPersonGuns` | Third-person gun poses for every character holding a gun ([THIRD_PERSON_GUNS.md](THIRD_PERSON_GUNS.md)). `Report()`: each posed character's gun kind and fit, for checking |
| `Client.Core.MatchMenu` | No API: the admin Match menu (M) |
| `Keybinds.Get(action)` / `KeyName(action)` / `Label(action)` / `Set(action, keyName)` / `Reset()` | Key bindings |
| `Options.Get(name)` / `IsOn(name)` / `Set(name, value, previewOnly?)` / `Save(name)` | Options |
| `Slider.Bind(bar, onChange)` / `Slider.Show(row, alpha, text)` | Settings sliders |
| `PromptKeys.Key()` | The current Interact key (ProximityPrompts follow it) |
| `HealthBillboards.SetupBillboard(humanoid)` | Shows a health billboard |
| `Client.Core.UI` | No API: fits the HUD to the screen and the touch layout |
| `Client.Core.CmdrClient` | No API: F2 opens Cmdr; on touch, admins (`Classes.Admins`) get a CMD button (`Main.Mobile.CmdrButton`) |

---

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
| `Content.Guns.Skins` | `List`, `CRATE_PRICE` (499), `CRATE_REFUND_COINS` (500); `Get(id)`, `ForWeapon`, `Weapons`, `Choices`, `EquipField`, `Apply(model, skinId?, weaponId?)` |
| `Content.Guns.Melee` | Bash numbers; `Melee.For(gunId)` |
| `Content.Consumables` | Grenade and smoke numbers; `List`, `Get(id)`, `PER_LIFE` (2), `DEFAULT`, `THROW_COOLDOWN` |
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
| `ModelScale` | Gun Tool | The third-person gun's scale (`GunService`); `Content.Guns.Skins` scales skins by it |
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
