# Combat and damage

All damage in the game goes through one function, **`Combat.ApplyHit`**, so friendly fire, shields, kill credit, the kill feed and hit feedback behave the same for guns, grenades, gadgets and abilities.

!!! abstract "Source"

    `Systems.Combat.Combat`, `DamageLog`, `KillFeed`, `DeathCamService`, `SwordCombat`. Client: `Client.Combat.DamageFeedback`, `Client.Combat.KillFeed`, `Client.Hud.DeathScreen`. Guides: [Death screen and spectating](../../DEATH_SCREEN.md), [Kill feed](../../KILL_FEED.md).

```lua
local CombatFolder = game.ServerScriptService.Modules.Systems.Combat
local Combat = require(CombatFolder.Combat)
local DamageLog = require(CombatFolder.DamageLog)
```

## Which function do I use?

| You want… | Use |
| --- | --- |
| Damage **with** credit (kill feed, quests, stats, hit feedback) | [`Combat.ApplyHit`](#combatapplyhitvictimhumanoid-damage-options) |
| Damage from the world (fall damage, hazards), no credit | [`Combat.DealDamage`](#combatdealdamagehumanoid-damage-bypassshield-boolean) |
| A push | [`Combat.Knockback`](#combatknockbackcharacter-direction-speed) |
| Blast damage around a point | `Gadgets.Blast(...)` or `ConsumableService.Detonate("Grenade", ...)` |

---

## `Combat`

A plain library: no `Init` or `Start`, nothing happens when you require it.

### `Combat.ApplyHit(victimHumanoid, damage, options?)`

**The normal way to deal damage.** Line by line:

```lua title="Systems.Combat.Combat.ApplyHit"
function Combat.ApplyHit(victimHumanoid: Humanoid, damage: number, options: HitOptions?)
	local settings = options or {}
	local victimCharacter = victimHumanoid.Parent :: Model

	-- 1. Friendly fire: any handler may cancel the hit
	if settings.Attacker and Extensions.Any("Combat.PreventFriendlyFire", settings.Attacker, victimCharacter, victimHumanoid) then
		return
	end
	-- 2. Targets that count hits (training dummies) take 1 per hit
	if damage > 0 and victimHumanoid:GetAttribute("CountHits") == true then
		damage = 1
	end
	-- 3. Remember who hit them, for kill credit
	DamageLog.Record(victimHumanoid, settings.Attacker, settings.Item)
	-- 4. Shields first, then health (Combat.BlockHit can cancel it)
	local blocked = Combat.DealDamage(victimHumanoid, damage, settings.BypassShield)

	if settings.KnockbackDirection then
		Combat.Knockback(victimCharacter, settings.KnockbackDirection, settings.KnockbackSpeed or DEFAULT_KNOCKBACK_SPEED)
	end
	-- 5. Feedback for everyone, and the victim's red flash + arrow
	Combat.PlayHitEffects(victimCharacter)
	Packets.Combat.Hit:Fire(victimCharacter, if blocked then 0 else damage)
	-- (Packets.Combat.Hurt to the victim, with where the hit came from)
	-- 6. Stats (Siege's damage MVP, quests)
	Extensions.Fire("Combat.Hit", settings.Attacker, victimHumanoid, if blocked then 0 else damage, settings.Item)
end
```

| `HitOptions` field | Type | Meaning |
| --- | --- | --- |
| `Attacker` | `Player \| Model?` | Who dealt it. **Needed for kill credit and friendly-fire rules** |
| `Item` | `string?` | The weapon or ability name in the kill feed |
| `KnockbackDirection` | `Vector3?` | Horizontal push. Omit for none |
| `KnockbackSpeed` | `number?` | Default 10 (plus 10 up) |
| `BypassShield` | `boolean?` | Skip shields (poison) |

```lua
-- A trap that credits its owner and pushes the victim away
Combat.ApplyHit(humanoid, 30, {
	Attacker = owner,
	Item = "Spike Trap",
	KnockbackDirection = (victimRoot.Position - trap.Position).Unit,
	KnockbackSpeed = 40,
})
```

### `Combat.DealDamage(humanoid, damage, bypassShield?) → boolean?`

Raw damage with no credit: the `Shield` attribute absorbs it first unless bypassed. Returns `true` when a `Combat.BlockHit` handler cancelled it.

```lua title="Systems.Combat.Combat.DealDamage"
function Combat.DealDamage(humanoid: Humanoid, damage: number, bypassShield: boolean?)
	if damage <= 0 or humanoid.Health <= 0 then return false end
	if Extensions.Any("Combat.BlockHit", humanoid, damage) then return true end  -- blocked
	local shield = if bypassShield then nil else humanoid:GetAttribute("Shield")
	if shield and shield > 0 then
		local remaining = shield - damage
		humanoid:SetAttribute("Shield", math.max(remaining, 0))
		if remaining <= 0 then
			humanoid:TakeDamage(math.abs(remaining))
		end
	else
		humanoid:TakeDamage(damage)
	end
end
```

```lua
Combat.DealDamage(humanoid, 10)        -- fall damage
Combat.DealDamage(humanoid, 5, true)   -- poison tick, ignores shields
```

### `Combat.TryGiveShield(humanoid, chance, amount)`

Adds `amount` shield points with probability `chance` (0–1). Stacks.

```lua
Combat.TryGiveShield(humanoid, 0.25, 20) -- 25% chance of +20 shield
```

### `Combat.Knockback(character, direction, speed)`

Pushes a character's root with a short LinearVelocity (0.2 s, plus a lift of 10). The movement anti-cheat recognises it.

```lua
Combat.Knockback(victimCharacter, look, 60)
```

### `Combat.PlayHitEffects(character)`

The `Hit` effect (sound, red flash, particles) on every client. `ApplyHit` calls it.

```lua
Combat.PlayHitEffects(victimCharacter)
```

### `Combat.CreateHitbox(character, options?) → hitbox`

A cube hitbox in front of a character (`Size` default 7, `Lifetime` 0.1 s, optional `Offset`), owned by its player so the owner is never hit. **Not started**: call `:Start()`.

```lua title="From the Combat header"
local hitbox = Combat.CreateHitbox(character, { Size = 7 })
hitbox.Touched:Connect(function(_hit, victimHumanoid)
	Combat.ApplyHit(victimHumanoid, damage, { KnockbackDirection = direction, KnockbackSpeed = 10 })
end)
hitbox:Start()
```

---

## Kill credit: `DamageLog`

Who last damaged each player or NPC, and with what. "Victim" and "attacker" are a **Player** or an **NPC's character Model** (not a Humanoid).

### `DamageLog.Record(humanoid, attacker?, item?)`

Records a hit. `ApplyHit` does this for you; hits with no attacker, or on yourself, are ignored.

```lua
DamageLog.Record(humanoid, player, "Stone Sword")
```

### `DamageLog.Last(victim, window) → (attacker?, item?)`

Who hit them within `window` seconds (and is still in the game).

```lua
local attacker, item = DamageLog.Last(player, 10)
if attacker then print(player.Name, "was last hit by", attacker.Name, "with", item) end
```

### `DamageLog.Clear(victim)`

```lua
DamageLog.Clear(player) -- e.g. after a respawn
```

## Deaths: `KillFeed` and `DeathCamService`

### `KillFeed.ReportDeath(humanoid)`

Sends the kill feed line (when there's a credited attacker within the credit window) and fires **`Combat.Death`** for every death, credited or not, before the damage log is cleared.

```lua
humanoid.Died:Connect(function()
	KillFeed.ReportDeath(humanoid)
end)
```

`Combat.Death` is the one hook for "someone died". The tutorial uses it to tick off its kill goal:

```lua title="Systems.Games.Siege.TutorialService"
Extensions.Add("Combat.Death", function(victim, attacker, _item)
	local model = if typeof(victim) == "Instance" and victim:IsA("Humanoid") then victim.Parent else victim
	if SiegeBots.IsBotModel(model) then
		reach(asPlayer(attacker), "Kill")
	end
end)
```

### `DeathCamService.KillerOf(victim) → (Player | Model)?`

The last recorded killer of a player or NPC.

```lua
local killer = DeathCamService.KillerOf(player)
```

### `DeathCamService.Watching(player) → (Player | Model)?`

Who a dead player is spectating right now.

```lua
print(player.Name, "is watching", DeathCamService.Watching(player))
```

### `DeathCamService.Release(player)`

Stop choosing who a dead player watches (a game mode takes over, like Siege's `SpectateService`).

```lua
DeathCamService.Release(player)
SpectateService.Begin(player, 3, choicesFor)
```

`SwordCombat:Attack(player, aimOrigin?, aimDirection?)` is the knife/sword swing. Sword combat is off limits: don't change its behavior.

---

## Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Combat.PreventFriendlyFire` | Any | attacker, victimCharacter, humanoid |
| `Combat.BlockHit` | Any | humanoid, damage |
| `Combat.Hit` | Fire | attacker?, humanoid, damage (0 when blocked), item? |
| `Combat.Death` | Fire | victim (Player or NPC model), attacker?, item? |
| `Combat.PreventSwing` / `Combat.SwordHit` / `Combat.WeaponScale` | Any / Fire / Product | sword combat |

```lua
-- God mode for one player while testing
Extensions.Add("Combat.BlockHit", function(humanoid, damage)
	return humanoid.Parent == testPlayer.Character
end)

-- Track total damage dealt
Extensions.Add("Combat.Hit", function(attacker, humanoid, damage, item)
	if typeof(attacker) == "Instance" and attacker:IsA("Player") then
		totals[attacker] = (totals[attacker] or 0) + damage
	end
end)
```

!!! warning "There is no `Combat.Damage` point"

    Older docs listed a `Combat.Damage` multiplier. It only appears as an example in the `Shared.Extensions` comment; no code calls it. Scale gun damage with `Gun.DamageMultiplier` and grenades with `Consumable.DamageMultiplier`.

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Combat.Hit` | Server → all | character, damage |
| `Combat.Hurt` | Server → the player hit | damage, where it came from |
| `Combat.KillFeed` | Server → all | killer name, victim name, item |
| `Death.Killed` | Server → the player who died | killer name, killer UserId (0: NPC/none), weapon, seconds to respawn (-1: out until next round) |
| `Death.Spectate` | Server → a dead player | who to watch (model or `nil`), name |

More: [Damage and combat](../../EXAMPLES.md#damage-and-combat), including a full trap module.
