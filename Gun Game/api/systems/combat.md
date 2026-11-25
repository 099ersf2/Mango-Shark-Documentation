# Combat and damage

All damage in the game goes through one function, **`Combat.ApplyHit`**, so friendly fire, shields, kill credit, the kill feed and hit feedback behave the same for guns, grenades, gadgets and abilities.

!!! abstract "Source"

    `Systems.Combat.Combat`, `DamageLog`, `KillFeed`, `DeathCamService`, `SwordCombat`. Client: `Client.Combat.DamageFeedback`, `Client.Combat.KillFeed`, `Client.Hud.DeathScreen`. Guide: [Death screen and spectating](../../DEATH_SCREEN.md), [Kill feed](../../KILL_FEED.md).

## Which function do I use?

| You want… | Use |
| --- | --- |
| Damage **with** credit (kill feed, quests, stats, hit feedback) | `Combat.ApplyHit(humanoid, damage, { Attacker = player, Item = "Trap" })` |
| Damage from the world (fall damage, hazards): no credit | `Combat.DealDamage(humanoid, damage)` |
| A push | `Combat.Knockback(character, direction, speed)` or `KnockbackDirection` in `ApplyHit` |
| Blast damage around a point | `Gadgets.Blast(...)` or `ConsumableService.Detonate("Grenade", ...)` |

## `Combat.ApplyHit`, line by line

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
	local victimPlayer = Players:GetPlayerFromCharacter(victimCharacter)
	if victimPlayer and not blocked then
		-- `from` is the attacker's position, or the victim's own with no attacker
		Packets.Combat.Hurt:FireClient(victimPlayer, damage, from)
	end
	-- 6. Stats (Siege's damage MVP, quests)
	Extensions.Fire("Combat.Hit", settings.Attacker, victimHumanoid, if blocked then 0 else damage, settings.Item)
end
```

### `HitOptions`

| Field | Type | Meaning |
| --- | --- | --- |
| `Attacker` | `Player \| Model?` | Who dealt it (a player or an NPC model). **Needed for kill credit and friendly-fire rules** |
| `Item` | `string?` | The weapon or ability name shown in the kill feed |
| `KnockbackDirection` | `Vector3?` | Horizontal push direction. Omit for none |
| `KnockbackSpeed` | `number?` | Default 10 (plus a lift of 10 up) |
| `BypassShield` | `boolean?` | Skip shields (poison) |

### Shields

`Combat.DealDamage` drains the Humanoid's `Shield` attribute before health. `Combat.TryGiveShield(humanoid, chance, amount)` adds shield points with a chance.

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

## Kill credit and deaths

| Function | What it does |
| --- | --- |
| `DamageLog.Record(humanoid, attacker?, item?)` | Who last hurt someone (`ApplyHit` does this for you) |
| `DamageLog.Last(victim, window)` | The last attacker and item within `window` seconds |
| `DamageLog.Clear(victim)` | Forget a victim's record |
| `KillFeed.ReportDeath(humanoid)` | Sends the kill feed line and fires `Combat.Death` |
| `DeathCamService.KillerOf(victim)` | The last recorded killer of a player or NPC, or `nil` |
| `DeathCamService.Watching(player)` / `Release(player)` | Who a dead player watches / stop choosing for them |

**`Combat.Death`** fires for every death `KillFeed` handles, credited or not, *before* the damage log is cleared. It's the one hook for "someone died":

```lua title="Systems.Games.Siege.TutorialService"
Extensions.Add("Combat.Death", function(victim, attacker, _item)
	local model = if typeof(victim) == "Instance" and victim:IsA("Humanoid") then victim.Parent else victim
	if SiegeBots.IsBotModel(model) then
		reach(asPlayer(attacker), "Kill")
	end
end)
```

## Hitboxes

`Combat.CreateHitbox(character, { Size?, Offset?, Lifetime? })` makes a cube hitbox in front of a character (default 7 studs, 0.1 s), owned by its player so the owner is never hit. **It isn't started**; call `:Start()`:

```lua title="From the Combat header"
local hitbox = Combat.CreateHitbox(character, { Size = 7 })
hitbox.Touched:Connect(function(_hit, victimHumanoid)
	Combat.ApplyHit(victimHumanoid, damage, { KnockbackDirection = direction, KnockbackSpeed = 10 })
end)
hitbox:Start()
```

## Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Combat.PreventFriendlyFire` | Any | attacker, victimCharacter, humanoid |
| `Combat.BlockHit` | Any | humanoid, damage |
| `Combat.Hit` | Fire | attacker?, humanoid, damage (0 when blocked), item? |
| `Combat.Death` | Fire | victim (Player or NPC model), attacker?, item? |
| `Combat.PreventSwing` / `Combat.SwordHit` / `Combat.WeaponScale` | Any / Fire / Product | sword combat (don't change its behavior) |

!!! warning "There is no `Combat.Damage` point"

    Older docs listed a `Combat.Damage` multiplier. It only appears as an example in the `Shared.Extensions` comment; no code calls it. To scale gun damage use `Gun.DamageMultiplier`; for grenades, `Consumable.DamageMultiplier`.

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Combat.Hit` | Server → all | character, damage |
| `Combat.Hurt` | Server → the player hit | damage, where it came from |
| `Combat.KillFeed` | Server → all | killer name, victim name, item |
| `Death.Killed` | Server → the player who died | killer name, killer UserId (0: NPC/none), weapon, seconds to respawn (-1: out until next round) |
| `Death.Spectate` | Server → a dead player | who to watch (model or `nil`), name |

More: [Damage and combat](../../EXAMPLES.md#damage-and-combat), including a full trap module.
