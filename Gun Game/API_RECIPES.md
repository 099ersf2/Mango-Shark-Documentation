[Documentation home](index.md) / [API reference](API.md)

# Common API recipes

> **Scope:** General task recipes. Some match-mode examples describe historical APIs; use [current Siege APIs](API_SIEGE.md) for active game flow.

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
