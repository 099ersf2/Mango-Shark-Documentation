# Cookbook

One line for each common task. All server-side unless marked **(client)**. Follow the link for the explanation; for full, commented code see [Task-based code examples](../EXAMPLES.md).

## Server and match

| I want to… | Do this |
| --- | --- |
| Know what kind of server this is | `ServerRole.Kind()` → `"Lobby"`, `"Match"`, `"Studio"` ([Siege](systems/siege.md#which-server-am-i-on-serverrole)) |
| Know the phase / a player's side | `SiegeService.Phase()` / `SiegeService.TeamOf(player)` |
| List living defenders | `SiegeService.Players("Defenders", true)` |
| End the round now | `SiegeService.ForceEnd("Attackers", "BombsPlanted")` |
| Run code when a phase starts | `Extensions.Add("Siege.PhaseChanged", function(phase) ... end)` |
| Change plant time | `Extensions.Add("Siege.PlantTimeMultiplier", function(player, bomb) return 0.5 end)` |
| React when the match ends | `Extensions.Add("Siege.Ended", function(winner, reason, info) ... end)` (`info.Players`) |
| Test a match alone in Studio | Workspace attribute `SiegeTestTeam = "Attackers"`, then PLAY (K) |
| Check the map | `SiegeMap.Load()` (`nil` and warns every problem) |

## Matchmaking

| I want to… | Do this |
| --- | --- |
| Queue a player's party | `QueueService.Join(player, modeId?)` → `(ok, message)` (leader only) |
| Start a private match | `QueueService.JoinPrivate(player, modeId?)` |
| Add a queue mode | A row in `Content.Matchmaking.MODES` ([Matchmaking](systems/matchmaking.md#queue-modes-contentmatchmaking)) |
| Block queueing | `Extensions.Add("Queue.PreventJoin", function(player) return ... end)` |

## Classes, drones, cameras

| I want to… | Do this |
| --- | --- |
| Give a class / arm a player | `ClassService.Assign(player, "Breacher", guns?)` / `ClassService.Arm(player)` |
| Read a player's class | `ClassService.ClassOf(player)` (never an attribute) |
| Add a class | A file in `Content.Classes.Definitions` ([Classes](systems/classes.md#adding-a-class-checklist)) |
| Add an ability | `Systems.Classes.Abilities.<Ability.Id>` with `Use(context)` → `(ok, message?)` |
| Shorten cooldowns | `Extensions.Add("Classes.CooldownMultiplier", function(p, classId, abilityId) return 0.8 end)` |
| Give a drone without a throw | `DroneService.Place(player, cframe)` |
| Show players a mark | `DroneService.Mark(players, key, position, seconds)` |
| Add a camera mid-match | `CameraService.Add(model, name, team, bulletproof)` |

## Guns and combat

| I want to… | Do this |
| --- | --- |
| Give one gun | `GunService.Give(player, "AssaultRifle")`, or `givegun <player> <gunId>` |
| Set exactly these guns | `LoadoutService.Arm(player, { "AssaultRifle", "Pistol" })` (plus the knife) |
| Give an NPC a gun | `GunService.GiveNPC(model, "AssaultRifle")` |
| Cancel a reload | `GunService.CancelReload(player)` → `true` if one was running |
| Scale gun damage | `Extensions.Add("Gun.DamageMultiplier", function(who, gunId, humanoid, hit) return 1 end)` |
| Block shooting | `Extensions.Add("Gun.PreventFire", function(who, gunId, tool) return ... end)` |
| React to a kill | `Extensions.Add("Gun.Killed", ...)` (guns), or `Combat.Death` (any death) |
| Damage with credit | `Combat.ApplyHit(humanoid, 30, { Attacker = player, Item = "Trap" })` |
| Damage without credit | `Combat.DealDamage(humanoid, 10)` |
| Knock someone back | `Combat.Knockback(character, direction, 60)` |

## World and NPCs

| I want to… | Do this |
| --- | --- |
| Break a board | `BreakableService.Damage(boardPartOrModel, 50, player, "Trap")` |
| Explosion damage to boards | `BreakableService.DamageRadius(position, 12, 100, player, "Explosion")` |
| Fix a board fully | `BreakableService.Reset(board)` |
| Hole a soft wall | `SoftWalls.Punch(wall, hitPosition, direction, 0.3, player, "Trap")` |
| Put walls back | `SoftWalls.ResetAll()`, or `softwallreset all` |
| A grenade blast anywhere | `ConsumableService.Detonate("Grenade", position, player)` |
| Refill grenades | `ConsumableService.Refill(player)` |
| Is a line blocked by smoke? | `Smoke.Blocks(from, to)` (both sides) |
| Spawn an NPC | `NPCService.Spawn("Soldier", cframe)` → model, or `spawnnpc Soldier 3` |
| Make an NPC guard a room | `NPCService.SetMode(npc, "Guard", roomPart)` (a part tagged `NPCRoom`) |
| Remove every NPC | `NPCService.Clear()`, or `clearnpcs` |

## Lobby, movement, state

| I want to… | Do this |
| --- | --- |
| Take a test player out of the lobby | `LobbyService.SendToArena(player)` ([Lobby](systems/lobby.md)) |
| Spawn a player outside the lobby next time | `LobbyService.Release(player)` |
| Stop a player acting for a while | `StateHandler.SetState(player, "CantDoAnything", true, 2)` ([Helpers](foundations/helpers.md)) |
| Stun a player or NPC | `StateHandler.SetStun(playerOrModel, true, 2)` |
| Read the server's movement state | `MovementService.GetState(player)` ([Movement](systems/movement.md)) |
| Block sprinting | `Extensions.Add("Movement.PreventSprint", function(player, state) return ... end)` |
| Rate-limit a packet | `local bucket = TokenBucket.new(5, 2)`; `if not bucket:allow(player.UserId) then return end` |
| Retry a MemoryStore/DataStore call | `Retry.Call("Label", function() return store:GetAsync(key) end)` |
| A teleport pad | Tag a part `Teleporter`, set its `TeleportTo` attribute to the destination part's name |

## Data, economy, progression

| I want to… | Do this |
| --- | --- |
| Give coins | `StoreService.Give(player, "Coins", 100, "Reason")` |
| Read or write player data | `local data = Data.Server.WaitForData(player)`; `data.Coins.Increment(100)` |
| Add saved fields | A ModuleScript tagged `ScribeFragment` returning `{ Template = { ... } }` |
| Test without saving | Workspace attribute `ScribeNoSave = true` in Edit mode |
| Count toward quests | `QuestService.Add(player, "Kills", 1)` |
| Battle pass XP | `BattlePassService.AddXP(player, 50, "Event")` |
| Account XP / weekly points | `ProgressService.AddXP(player, 100, "Event")` / `ProgressService.AddPoints(player, 20, "Event")` ([Progress](systems/progress-analytics.md)) |
| Log an analytics event | `AnalyticsService.Custom(player, "ClassPicked", 1, classId, side, mode)` (name must be in `Content.Analytics.EVENTS`) |
| Use a product id | `ProductIds.Products.<Name>`; never type an id anywhere else |

## Effects and client

| I want to… | Do this |
| --- | --- |
| Effect for everyone | `EffectService.Play("BulletImpact", { CFrame = cf })` |
| Effect for everyone but me | `EffectService.Play(name, options, player)` |
| Effect only for me **(client)** | `Effects.Play("Hitmarker", { Target = part })` |
| Shake the camera **(client)** | `MovementCamera.Shake(3, 10, 0.1, 0.6)` |
| Open a menu **(client)** | `Menus.Open("Settings")` |
| Show a popup **(client)** | `Notice.Show("TITLE", "Text")` |
| Change and save a setting **(client)** | `Options.Set("Fov", 90)` (saves too; pass `true` as a third argument to preview only) |
| Rebind a key **(client)** | `Keybinds.Set("Prone", "C")` |
| Read a setting on the server | `SettingsService.GetOption(player, "AimAssist")` ([Settings](systems/settings.md)) |
| Change move speed | `Extensions.Add("Movement.SpeedMultiplier", function(player, gunId) return 0.8 end)` |
