[Documentation home](index.md) / [API reference](API.md)

# Current Siege APIs

> **Status:** Current-game reference for Siege, matchmaking, classes, cameras and drones. Check the linked system guides and their verification notes before relying on an entry.

## Siege, matchmaking, classes, cameras (2026-11-12)

Current Siege, matchmaking, class, camera and drone APIs are summarized here. For implementation details, see [SIEGE.md](SIEGE.md), [MATCHMAKING.md](MATCHMAKING.md), [CLASSES.md](CLASSES.md) and [DRONES.md](DRONES.md). Legacy admin match controls, `Packets.Match.Admin`, the `match` / `matchmode` / `matchset` commands, the Match key, `Packets.Drone.Spot` / `Spotted` and the Team Deathmatch, Free-for-All and Elimination modes are not current; see the historical references linked from [API.md](API.md).

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
| `QueueService.Join(player, modeId?)` / `JoinPrivate(player, modeId?)` / `Leave(player)` / `IsQueued(player)` | The queue. `modeId` is a `Content.Matchmaking.MODES` Id. `JoinPrivate` forms a private match of that mode with the leader's party only, at once |
| `Content.Matchmaking.GetMode(id)` / `ModesIn(categoryId)` | A queue mode by Id (or nil) / the modes of one category |
| `Content.Matchmaking.PartyLimit(mode)` | The largest party a mode allows: the smaller side, or the only side when the other is 0 |
| `Content.Matchmaking.PrivateLimit(mode)` / `FitMode(modeId, size, private)` | The largest party for a private match of a mode; the mode a party of that size plays (the picked one, or the next of its category that fits) |
| `Client.Core.ModeMenu.SetPartySize(size)` | Marks the modes the party is too big for (PARTY TOO BIG, PRIVATE ONLY) |
| `Client.Core.Notice.Show(title, text, sound?)` / `Hide()` | The `Main.Notice` popup (sound defaults to `Error`) |
| `Client.Core.Tooltip.Set(object, text?)` / attribute `Tooltip` | A hover tooltip on a UI element (nil or "" removes it) |
| `Client.Core.ItemDetails.Spin(viewport, on)` / `Hover(viewport, on)` | Turns a `GunPreview` around (the page); a card's while hovered, one at a time |
| `ItemDetails` `Row.Description` | A row's own description, shown when the row is clicked |
| `ClearHouse.Prepare(map)` / `Populate(players)` / `Left()` / `Total()` / `GuardOf(model)` / `Rows()` / `Rooms()` / `Clear()` | `Systems.Games.ClearHouse.ClearHouse`: boards the map and finds rooms / places guards / guard counts and records ([CLEAR_HOUSE.md](CLEAR_HOUSE.md)) |
| `Content.Games.ClearHouse` | Clear House numbers: Action time, guard counts (`ROOM_SHARE`, `GUARDS_PER_PLAYER`, `MAX_PER_ROOM`) and profiles, room finder settings |
| `Packets.Siege.Pick("Map", name)` / snapshot `Maps` | Clear House's map vote during Selection: `{ Name, Votes }` per map of the mode |
| `Content.BattlePass` | The season, `TRACK` (a Free and a Premium reward per level), `LevelOf`, `Progress`, `Unlocked`, `Reward`, `Totals`, `SecondsLeft`, `MATCH_XP`, `PREMIUM_ITEM` ([BATTLE_PASS.md](BATTLE_PASS.md)) |
| `Content.Quests` | `DAILY`, `WEEKLY`, `MILESTONES`, `Get`, `Day`, `Week` |
| `BattlePassService.AddXP(player, amount, reason)` / `Claim(player, rewardId or "ALL")` / `Level(player)` | Server: battle pass XP, claims, level |
| `QuestService.Add(player, stat, amount?)` | Server: counts toward quests ("Kills", "MatchesWon"...) |
| `Packets.BattlePass.Claim(rewardId)` / `Progress(amount, reason, level)` | Claim a reward (answered); XP earned (server -> client) |
| Extension points `BattlePass.LevelUp(player, level)`, `BattlePass.Claimed(player, rewardId)`, `BattlePass.XPMultiplier(player, reason)` (Product), `Quests.Completed(player, questId, xp)` | Battle pass and quest hooks |
| `Client.Core.BattlePass.Open(tab?)` | Opens the Battle Pass ("Pass" or "Quests") |
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
| `Client.Core.ClassPanel` | `Fill(panel, class, { Color?, UserId? })`, `FillGun(panel, { Kind, Title, Description?, GunId?, Color?, Preview? })`, `Letter(class)`, `GunName(class, slot, gunId)`, `KitNames(class, slot)`, `Speed(class)`, `GunLine(gunId)`: the class and gun panels |
| `ItemDetails` View `Class` / `GunId`, Row `GunId` | 2026-11-17: show the class panel or the gun panel on the detail page |
| `Client.Hud.SiegeTopBar` | No API: the Siege top bar (HUD and feeds) and the "3 VS 4" flash |
| `Client.Combat.DamageFeedback` | No API: red edges, hit arrows and the low-health look |
| `Client.Gadgets.FeedInfo` | No API: the drone and camera feeds' objective, location and compass |
| `Client.Hud.SiegeHud.UseAbility()` | Uses the class ability |
| `Client.Hud.Scoreboard` | No API: the scoreboard (hold Tab) |
| `Client.Gadgets.CameraController.Use()` / `View(model)` / `Cycle(direction)` / `Scan()` / `Exit(tellServer?)` | Security cameras |
| `Client.Core.Spectate.Cycle(direction)` | Next or previous player to watch |
| `DroneController.Exit(force?)` | Leaving is refused while `DroneLockedIn`, unless forced |

### Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Party.Request` | Client → server, answered (ok, message) | action (`Invite`, `Accept`, `Decline`, `Leave`, `Kick`, `Promote`, or `Sync` to be sent `Party.State` again), argument |
| `Party.State` | Server → one client | `{ Id, Leader, Max, Members = { { UserId, Name, Here } } }` or nil |
| `Party.Invite` / `Party.InviteClosed` | Server → one client | PartyId, leader name, leader UserId, seconds / PartyId |
| `Queue.Request` | Client → server, answered (ok, message) | `Join`, `Private` (a private match of the party only) or `Leave`, and the mode's Id for `Join` and `Private` (`""` for the default) |
| `Queue.State` | Server → one client | `{ Queued, Since, Status, Size, Mode }` |
| `Siege.State` | Server → one client | The match as their team may see it. During Selection also `Others` and `OtherTeam`: the other team's players as UserId, Name and Ready, nothing else. `Map` (2026-11-17): the map's name in `ReplicatedStorage.Maps` |
| `Siege.Pick` | Client → server | kind (`Site`, `Spawn`, `Class`, `Gun`, `Ready`), value (`Ready`: `"1"` done picking, `"0"` changing picks) |
| `Siege.Plant` | Server → one attacker | bomb (`""` for none), server time it started, seconds |
| `Siege.Board` | Server → one client | Scoreboard rows, filtered for their team |
| `Tutorial.Request` | Client → server, answered (ok, message) | `"Start"` (training, alone) or `"Skip"` (2026-11-17, [TUTORIAL.md](TUTORIAL.md)) |
| `Tutorial.Progress` / `Tutorial.Learned` / `Tutorial.Finished` | Server → the recruit | `{ Round, Phase, Done, Missed, Counts }` / a goal Id reached / true if this finish gave the Recruit Crate |
| `Siege.RequestState` | Client → server | — |
| `Class.Use` | Client → server, answered (ok, message) | server time, camera position, unit look |
| `Class.State` | Server → the owner only | `{ ClassId, Charges, ReadyAt, Guns }` or nil |
| `Class.Flash` | Server → one client | seconds blinded |
| `Camera.View` | Client → server, answered (ok) | CameraId, or `""` to stop |
| `Camera.Scan` | Client → server, answered (scanned) | CameraId; server checks live view, team, cooldown, range, angle and line of sight |
| `Scan.Alert` | Server → the player scanned by a camera or drone | — |
| `Spectate.Next` / `Spectate.Mode` | Client → server / server → one client | 1 or -1 / `Team`, `Enemy` or `""` |
| `Drone.Scan` | Client → server, answered (scanned) | drone, unit look |
| `Drone.Marked` | Server → the scanner's team | key, position, seconds |

### Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Siege.PhaseChanged` | Fire | phase |
| `Siege.PreventPlant` / `Siege.PlantTimeMultiplier` | Any / Product | player, bombName |
| `Siege.Planted` / `Siege.SiteLocated` / `Siege.Ended` | Fire | player, bombName / player / winner?, reasonKey | `Siege.Ended` is the match end (the side with the most rounds) |
| `Siege.RoundEnded` | Fire | winner?, reasonKey, round | A round of a multi-round match ended; the next one follows |
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
| `Camera.Scanned` | Fire | spotter, targetModel (a live defender camera scanned a player; Siege uses it to reveal attacker classes; `Camera.PreventView` also gates scans) |
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
| `Content.Games.Siege` | Phase times, plant time, map folder names, bomb labels and colors, texts, win reasons |
| `Content.Crates.Crates` / `Content.Store.Store` | Loaded from one file per crate / store item in `Content.Crates.Definitions` / `Content.Store.Definitions` (sorted by `Order`); the shared colors are in `Content.Store.Style` |
| `Systems.Store.BotCoinService` | Pays `REWARDS.BotKill` Coins for an NPC kill |
| `Systems.Games.Siege.SiegeBots` | Siege bots: `Pick(entry, team, info, teamEntries)`, `Spawn(entry, cframe)`, `Despawn(entry)`, `Update(context)`, `Reset()`, `NewMatch()`, `Scout(entry, cframe)`, `SiteFound()`, `IsBot(userId)`, `IsBotModel(model)`. See [SIEGE_BOTS.md](SIEGE_BOTS.md) |
| `Systems.Games.Siege.BotDrones` | Bot scout drones: `Deploy(userId, team, cframe)`, `Of(userId)`, `Drive(model, goal?)`, `State(model)`, `Clear()`, `Prepare(map)` (links through wall vents) |
| `Content.Theme` | The UI style (tactical since 2026-11-17): Void, Base, Panel, Raised, Card, Line, Accent (+Dim, Well), Highlight, Text, Muted, Faint, Ink, Danger, Success, `FONT`, `FONT_BOLD`, `BLUR`, `Map(color)`, `IsBright(color)`; the old names (Aqua, Pink, Midnight...) now give the new colors |
| `Client.Core.MenuAmbience` | No API: blurs and greys the world while a menu is open |
| `Client.Core.Peek` | `Cut(scroller, share?)`: a horizontal list shows part of its next card |
| `Client.Core.Notice` | `Show(title, text, sound?)`: since 2026-11-17 with a 70% backdrop and a red "!" (error) or aqua "i" icon |
| `Content.Games.Tutorial` | Recruit Training: map, site, spawn, classes, bot, times, health, crate, texts, goals (`STEPS`), saved `Tutorial` flags |
| `Systems.Games.Siege.TutorialService` | `Progress(player)`; the goals and the reward. Fires `Tutorial.Finished(player, rewarded)` |
| `SiegeService.IsTutorial()` / `SiegeService.Round()` | 2026-11-17 |
| `QueueService.JoinTutorial(player)` | ok, message: Recruit Training against the bot |
| `Content.Games.SiegeBots` | Bot names, prefix, id range, pick delay, plan timings, drone speed and spotting, memory times; since 2026-11-17 the squad (`GATHER_WAIT`, `GATHER_MAX`, `PUSH_STAGGER`, `RALLY_*`, `THREAT_WINDOW`), the bot radio (`TRADE_RANGE`, `HELP_RANGE`, `HELP_HEALTH`, `HELP_GAP`) and outfits (`LOOKS`) |
| `Systems.Lobby.Teleporters` | Parts tagged `Teleporter` send players to the part named by their `TeleportTo` attribute |
| `Content.Classes.Classes` | Every class and ability, loaded from one file per class in `Content.Classes.Definitions` (sorted by `Order`); `Get`, `ForTeam`, `CategoryOf`, `Allows`, `Choices`, `GunCategories`, `HIDDEN` |
| `Content.Cameras` | Camera health, hit box, view limits, scan range/angle/cooldown/ray steps, attribute names |
| `Content.Match.Modes.Siege` | The mode entry (`External = true`) |
| `Content.Match.Teams` | Also `Attackers` and `Defenders` |
| `Content.Drones` | Also `NO_SIGNAL_TIME`, `SCANNED_ALERT_TIME`, `CAMERA_MARK_COLOR`, scan range/angle and the `DronesEnabled`, `DroneLockedIn`, `DroneLost`, `DroneLocked` attribute names; `SPOT_TIME` is 30, `SPOT_COOLDOWN` is 5 |

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
| Tag `FitScale` (and `DesignHeight`, `WidthShare`, `BelowTopbar`) | A UIScale in a full-screen menu frame | `Client.Core.UI` scales the menu to fit the screen, under the top bar ([UI.md](UI.md#full-screen-menus-that-fit-fitscale)). On `SiegeSelect.Screen.Content.Fit` |
| `Main.MenuButtons.TouchScale` | UIScale | 0.8 on small touch screens |
| `Main.RoundResult` / `Main.MatchResult` | Frame | The Siege round banner and the final match screen (`Client.Hud.SiegeHud`); templates `RoundPip`, `MvpCard`, `TeamColumn`, `ResultRow` |
| `Classes.Reinforced` (extension, Fire) | player, model | A reinforced wall was placed; Siege counts it as Built |
| `givedevskins` / `takedevskins` | Cmdr command (admins) | players: give or take the Developer skin pack (`StoreService.GiveSkins`) |
| `SkinRainbow` / `RainbowOffset` | Tag / attribute on gun parts | Rainbow skin parts, animated by `Client.Guns.SkinRainbow` |
| `Packets.Analytics.MenuOpened` | Client → server | A menu name from `Content.Analytics.MENUS`, for analytics |
| `Siege.SelectionEnded` (extension, Fire) | summary | Each round's final picks (`Picks`: Player, Team, Class, Spawn, Random), Mode, Map, Site |
| `TotalWins` | Player | Saved total wins, set by `StatsService`; the lobby leaderboard sorts by it |
| `Content.Games.Siege.ROUNDS` / `DEFAULT_ROUNDS` / `ROUND_END_TIME` / `MATCH_ENDING_REASONS` | Content | Rounds per mode, the pause between rounds, reasons that end the whole match |
| `DronesMax` | Player | How many drones they may have out at once (`Content.Drones.MAX_ATTRIBUTE`). `DroneService.AddCharge(player)` raises it by one until the next refund |
| `StoreService.Buy` / `Give` / `Perk` / `OwnsClass` / `OwnsPass`, `StatsService.Record` | Server | See [STORE.md](STORE.md#api-and-extension-points) |
| `Store.Buy` / `Store.Open` / `Store.Reward` | Packets | Buy a crate (into the inventory), item or class; open a crate from the inventory; a reward was earned |
| `Client.Core.Store.Open(section?)`, `Client.Core.Inventory.Open(tab?)`, `Client.Core.ItemDetails.Show(view)`, `Client.Core.StoreViews` | Client | Store, Inventory, detail page, shared views |
| `CrateInventory` | Saved data | `[crateId].Count`: crates bought and not opened |
| `Store.PreventBuy`, `Store.Bought`, `Store.Given`, `Stats.Recorded` | Extension points | See [STORE.md](STORE.md) |
| `Tokens`, `OwnedClasses`, `Wins`, `Losses`, `Stats`, `LastMode` | Saved data | From `Content.Store.Store` (ScribeFragment). `Tokens` is unused since 2026-11-15 |
| `WinStreak` | Player attribute | The win streak shown above the head |
| `Skins.FamilyOf(gunId)` | Shared | The skin family a gun wears ("Rifle", "Pistol", else its own Id). `Skins.EquipField(gunId)` returns the family's field |
| `Client.Core.SkinShop.Preview(skinId)` | Client | Plays the crate reel landing on a skin, granting nothing (testing) |
| `Assets.UI.Templates.SkinCard` / `SkinTab` / `CrateItem` / `ReelCard` | Templates | The ARMORY shop's cards, tabs, crate rows and reel cards |
| `Client.Gadgets.DroneController.Cycle(direction)` | Client | Switch to the next (1) or previous (-1) living drone while in one |
| `Assets.UI.Templates.PromptStack` / `PromptCard` | BillboardGui / TextButton | The custom proximity prompt: one stack per object, cards 2 per row (`Client.Interact.CustomPrompts`). Every prompt is Custom style on the client |
| `FixedKey` | ProximityPrompt attribute | Its key is kept: `PromptKeys` doesn't move it to Interact, and `CustomPrompts` moves the other prompt on a clash |
| `Main.Mobile.<Button>.Icon.Glyph` | ImageLabel | The touch button's icon. `Content.Consumables.Consumables` entries have an `Icon` for the grenade button |
| `workspace.SiegeCameras`, `workspace.SiegeGadgets` | | Made at runtime |
| Keys | | `Play` (K), `Party` (L), `ClassAbility` (T) in `Shared.PlayerSettings.Actions`; the `Match`, `Loadout` and `GameMode` actions are gone. A player's class is **never** an attribute |

---
