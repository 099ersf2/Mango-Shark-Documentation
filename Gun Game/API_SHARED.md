# Shared API reference

!!! abstract "Scope"

    Shared modules, data, extension points and packets. Some packet entries support historical match modes; current Siege packet contracts are in [Current Siege APIs](API_SIEGE.md).

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

!!! example "The three kinds of extension point"

    ```lua
    local Extensions = require(game.ReplicatedStorage.Modules.Shared.Extensions)

    -- Any (veto): return true to stop it.
    Extensions.Add("Gun.PreventFire", function(who, gunId, tool)
    	return who:GetAttribute("Frozen") == true
    end)

    -- Product (multiplier): always return 1 when your rule doesn't apply.
    Extensions.Add("Movement.SpeedMultiplier", function(player, gunId)
    	return if gunId == "SniperRifle" then 0.85 else 1
    end)

    -- Fire (notification): react, return nothing.
    local remove = Extensions.Add("Gun.Reloaded", function(who, tool, gunId)
    	print(who.Name, "reloaded", gunId)
    end)
    remove() -- Add returns a function that removes the handler
    ```

    More: [Block shooting under a rule](EXAMPLES.md#block-shooting-under-a-rule), [Spawn protection](EXAMPLES.md#spawn-protection-full-module), [React to kills and deaths](EXAMPLES.md#react-to-kills-and-deaths).

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
| `Combat.Damage` / `Combat.Hit` | Product / Fire | attacker / attacker, humanoid, damage, item | Generic combat damage scale / after a hit (damage 0 when blocked) |
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
| `Consumable` | String | The picked consumable Id (`Grenade` or `Smoke`), from `Content.Consumables.Consumables` |

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
| `Combat.Hurt` | Server → the player hit | damage, where it came from (the attacker's position, or the victim's own) |
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

!!! example "Send and receive"

    ```lua
    local Packets = require(game.ReplicatedStorage.Modules.Shared.Packets)

    -- Server: listen, then answer one player or everyone.
    Packets.Gun.Loadout.OnServerEvent:Connect(function(player, loadoutId)
    	if type(loadoutId) ~= "string" then return end -- always check types
    	-- ...
    end)
    Packets.Gun.HitConfirm:FireClient(player, false, false) -- one client: headshot, killed

    -- Client: send intent only.
    Packets.Gun.Reload:Fire()
    ```

    A full request/answer round trip, from declaring the packet to the client call: [Networking: a new client request](EXAMPLES.md#networking-a-new-client-request).

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
