# All extension points

Every [extension point](../foundations/extensions.md) in the game, grouped by the system that asks it. **Any** = veto (return `true` to stop), **Product** = multiplier (return a number, `1` for no change), **Fire** = notification.

"who" means a Player **or** an NPC model; check `who:IsA("Player")` before using player-only things.

## Siege

Asked by `Systems.Games.Siege.SiegeService`. [Siege match](../systems/siege.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Siege.PhaseChanged` | Fire | phase |
| `Siege.PreventPlant` | Any | player, bombName |
| `Siege.PlantTimeMultiplier` | Product | player, bombName |
| `Siege.Planted` | Fire | player, bombName |
| `Siege.SiteLocated` | Fire | player? |
| `Siege.SelectionEnded` | Fire | `{ Round, Mode, Map, Site, Picks }` |
| `Siege.RoundEnded` | Fire | winner?, reasonKey, round, `{ Mode, Map, Site, Final }` |
| `Siege.Ended` | Fire | winner?, reasonKey, `{ Mode, Map, Rounds, ScoreA, ScoreB, Draw, Players }` |
| `Tutorial.Finished` | Fire | player, rewarded |

## Matchmaking

Asked by `PartyService`, `QueueService`, `MatchHost`. [Matchmaking](../systems/matchmaking.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Party.PreventInvite` | Any | player, targetUserId |
| `Party.Changed` / `Party.Disbanded` | Fire | partyId |
| `Queue.PreventJoin` | Any | player |
| `Queue.Joined` | Fire | partyId, ticket |
| `Queue.Left` | Fire | partyId, reason |
| `Matchmaking.MatchFormed` / `Assigned` / `MatchReady` | Fire | record |
| `Matchmaking.Arrived` | Fire | player, record |
| `Lobby.PreventFirstSpawn` | Any | player |

## Classes and gadgets

Asked by `ClassService`, `Gadgets` and ability modules. [Classes](../systems/classes.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Classes.PreventAbility` | Any | player, classId, ability |
| `Classes.AllowBodiless` | Any | player, classId |
| `Classes.CooldownMultiplier` | Product | player, classId, abilityId |
| `Classes.AbilityUsed` | Fire | player, classId, abilityId |
| `Classes.Assigned` | Fire | player, classId |
| `Classes.GadgetPlaced` | Fire | player, kind, model |
| `Classes.GadgetDestroyed` | Fire | owner?, kind, model, killer? |
| `Classes.PreventFlash` | Any | thrower, victim |
| `Classes.FlashTimeMultiplier` | Product | thrower, victim |
| `Classes.Flashed` | Fire | thrower, victim, seconds |
| `Classes.Reinforced` | Fire | player, model |
| `Classes.BreachDetonated`, `PreventPulseMark`, `Pulsed`, `PreventMineTrigger`, `MineDetonated`, `HealMultiplier`, `Healed` | | see each module in `Systems.Classes.Abilities` and [Siege classes](../../CLASSES.md#extension-points) |

## Drones and cameras

[Drones and cameras](../systems/drones-cameras.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Drone.PreventDeploy` | Any | player |
| `Drone.PreventRespawn` / `Drone.PreventView` | Any | player |
| `Drone.Deployed` | Fire | player, drone |
| `Drone.Destroyed` | Fire | player, drone, killer? |
| `Drone.Noise` | Fire | drone, position, share |
| `Drone.Spotted` | Fire | player, target, position |
| `Camera.PreventView` | Any | player, model |
| `Camera.PreventDamage` | Any | attacker, model |
| `Camera.Viewed` | Fire | player, model? |
| `Camera.Scanned` | Fire | spotter, target |
| `Camera.Destroyed` | Fire | model, killer? |
| `Spectate.Changed` | Fire | viewer, model?, mode |
| `Death.PreventSpectate` | Any | viewer |

## Guns

Asked by `GunService`, `AbilityRunner`, `GunMelee`, `LoadoutService`. [Guns](../systems/guns.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Gun.PreventFire` | Any | who, gunId, tool |
| `Gun.DamageMultiplier` | Product | who, gunId, humanoid, hit (`nil` for ability damage) |
| `Gun.Hit` | Fire | who, humanoid, hit, gunId |
| `Gun.Killed` | Fire | who, victimHumanoid, gunId, headshot |
| `Gun.Reloaded` | Fire | who, tool, gunId |
| `Gun.Fired` | Fire | who, gunId, origin |
| `Gun.PreventMelee` | Any | who, gunId, tool |
| `Gun.MeleeHit` | Fire | who, kind, instance, humanoid?, gunId |
| `Loadout.PreventApply` | Any | player |

## Combat

Asked by `Combat`, `KillFeed`, `SwordCombat`. [Combat](../systems/combat.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Combat.PreventFriendlyFire` | Any | attacker, victimCharacter, humanoid |
| `Combat.BlockHit` | Any | humanoid, damage |
| `Combat.Hit` | Fire | attacker?, humanoid, damage, item? |
| `Combat.Death` | Fire | victim, attacker?, item? |
| `Combat.PreventSwing` | Any | player |
| `Combat.SwordHit` | Fire | player, victimHumanoid |
| `Combat.WeaponScale` | Product | tool |

## World

[World](../systems/world.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Breakable.PreventDamage` | Any | who, model, amount, source |
| `Breakable.DamageMultiplier` | Product | who, model, source |
| `Breakable.PieceBroken` | Fire | who, model, piece, source |
| `Breakable.Broken` | Fire | who, model, source |
| `Breakable.PreventRepair` | Any | player, model, piece |
| `Breakable.Repaired` | Fire | player, model, piece |
| `SoftWall.PreventPunch` | Any | who, wall, source |
| `SoftWall.PieceFell` | Fire | who, wall, piece |
| `Consumable.PreventThrow` | Any | player, id |
| `Consumable.DamageMultiplier` | Product | attacker?, id, humanoid |
| `Consumable.Thrown` | Fire | player, id, projectile |
| `Consumable.Detonated` | Fire | attacker?, id, position |

## Movement

| Point | Kind | Arguments |
| --- | --- | --- |
| `Movement.PreventSprint` | Any | player, state |
| `Movement.PreventSlide` / `Movement.PreventProne` | Any | player |
| `Movement.SpeedMultiplier` | Product | player, gunId? |

## Progression and economy

[Progression](../systems/progression.md)

| Point | Kind | Arguments |
| --- | --- | --- |
| `Store.PreventBuy` | Any | player, key, currency |
| `Store.Bought` | Fire | player, key, currency |
| `Store.CrateOpened` | Fire | player, crateId, skinId |
| `Store.Given` | Fire | player, currency, amount, reason |
| `Stats.Recorded` | Fire | see [Store](../../STORE.md) |
| `BattlePass.LevelUp` | Fire | player, level |
| `BattlePass.Claimed` | Fire | player, rewardId |
| `BattlePass.XPMultiplier` | Product | player, reason |
| `Quests.Completed` | Fire | player, questId, xp |

## Legacy (old match modes)

Still called by `MatchService` / `TeamService`, which don't run Siege. See [Legacy APIs](legacy.md).

| Point | Kind | Arguments |
| --- | --- | --- |
| `Match.Started` / `Match.RoundStarted` | Fire | modeId / modeId, round |
| `Match.Scored` | Fire | target, amount |
| `Match.Ended` | Fire | modeId, winner? |
| `Team.Changed` | Fire | player, oldTeam?, newTeam? |

!!! note "Removed or never real"

    `Combat.Damage` (only an example in a comment). `Drone.Spotted` now has a third argument, `position`.
