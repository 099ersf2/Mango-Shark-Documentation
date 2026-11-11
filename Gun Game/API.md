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
| Give grenades back / set the count | `ConsumableService.Refill(player)` / `ConsumableService.SetCount(player, 2)` |
| Set off a grenade or smoke anywhere | `ConsumableService.Detonate("Grenade", position, player)` |
| Is a line blocked by smoke? | `Smoke.Blocks(from, to)` (both sides) |

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
| `Tactics.Danger` / `Suspicion` / `Breach` / `TryGrenade(agent, now)` | The reflexes around the tree (dodge grenades, shoot to test, breach, throw); see [ADDING_NPCS.md](ADDING_NPCS.md) |
| `Brain.*` | Helpers behavior-tree tasks use: `CanSee` (sees through windows), `SeeThrough`, `Penetrable`, `ShootThrough`, `BreachPoint`, `Blocked` (soft walls and boards aren't cover), `AimPoint`, `Eye`, `MoveTo`, `MoveDirect`, `Stop`, `IsMoving`, `Ammo`, `IsReloading`, `SetLastKnown`, `FlatDistance`, `NewPath`, `AdvancePath` |
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
| `Actions` | Every rebindable action and default key (Fire, Aim, Reload, Ability, Inspect V, Melee Q, Consumable G, Sprint, Crouch LeftControl, Prone C, Slot1–4, Interact E, …) |
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
| `Menus.Register(name, frame)` / `Open(name)` / `Close(name?)` / `Toggle(name)` / `IsOpen()` / `SetMouseIconAfterClose(bool)` | One menu at a time, frees the mouse. Names: `Loadout`, `Settings`, `SkinShop`, `Career`, `Backpack`, `MapSelection` |
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
| `movedebug` | — | Toggles the movement readout |
| `aimassistpc` (`aapc`) | player, on? | Turns controller aim assist on or off for that player on mouse and keyboard, for testing; leave out `on` to toggle |

Add a command: a `<Name>` definition and a `<Name>Server` module in `Services.CmdrSetup.Commands`.

---

## Attributes

Read them anywhere with `:GetAttribute`; the **server** sets them unless noted.

| Attribute | On | Meaning |
| --- | --- | --- |
| `InLobby` | Player | In the lobby (no guns) |
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
| `NPCSpawn` | A part | An NPC spawn point |
| `ScribeFragment` | A ModuleScript | Adds player data fields |
| `SmokeCloud` | (set by the game) | A live smoke cloud part, with a `Radius` attribute |

## Collision groups

| Group | Who |
| --- | --- |
| `Player` | Every character part; doesn't collide with itself |
| `ProneBody` | The prone collision box |
| `SoftWallDebris` | Falling soft-wall pieces and debris chips; no player collision |
| `Thrown` | Thrown grenades and smoke bombs; no collision with `Player` or each other |
