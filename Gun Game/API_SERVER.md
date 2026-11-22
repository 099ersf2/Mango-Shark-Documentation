[Documentation home](index.md) / [API reference](API.md)

# Server-side API reference

> **Scope:** Server services across current and historical systems. For current Siege and matchmaking contracts, start with [API_SIEGE.md](API_SIEGE.md); the legacy match APIs are described in [MATCH.md](MATCH.md).

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
| `LobbyService.Readmit(player)` | The next character spawns in the lobby like the first one; call before `LoadCharacter` |
| `LobbyService.SelectMap(player, mapId: string)` | The lobby hub's map choice (`SelectedMap` attribute) |

### `Systems.NPC.NPCService` and `Systems.NPC.Brain`

| Function | What it does |
| --- | --- |
| `NPCService.Spawn(profileId: string, where: CFrame, spawnPart: BasePart?, ignoreCap: boolean?)` | Spawns an NPC from `Content.NPC.Profiles` into `workspace.Enemies`. Refused past `MAX_NPCS` (0 today) unless `ignoreCap` (Clear House's guards) |
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
