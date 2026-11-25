# Progression and economy

What players earn and spend: **Coins** and **Siege Tokens**, crates and skins, store items and classes, stats, the battle pass, quests, and the daily flame streak and levels.

!!! abstract "Source"

    `Systems.Store.StoreService`, `StatsService`, `BotCoinService`, `PassCosmetics`; `Systems.SkinShopService`; `Systems.BattlePass.BattlePassService`, `QuestService`; `Systems.Progress.ProgressService`, `LeaderboardService`, `NotifyService`; `Systems.Analytics.AnalyticsService`. Data: `Content.Store.*`, `Content.Crates.*`, `Content.Guns.Skins.*`, `Content.BattlePass`, `Content.Quests`, `Content.Progress`. Guides: [Store](../../STORE.md), [Battle pass and quests](../../BATTLE_PASS.md), [Skins](../../SKINS.md), [Progression](../../PROGRESSION.md), [Analytics](../../ANALYTICS.md).

## Store: `StoreService`

The client only **asks** (`Packets.Store.Buy`, `Packets.Store.Open`); every check is on the server.

```lua title="From the StoreService header"
StoreService.Buy(player, "Crate:Glacier", "Coins")    -- (ok, message): a crate goes into the crate inventory
StoreService.OpenCrate(player, "Glacier")             -- (ok, message, skinId): opens one crate from the inventory
StoreService.Give(player, "Coins", 500, "Quest")      -- pay out currency (battle pass, quests, rewards)
StoreService.Perk(player, "CoinMultiplier")           -- the product of that perk over owned passes (1 if none)
StoreService.OwnsClass(player, classId)               -- free classes, and locked ones they bought or were given
StoreService.OwnsPass(player, itemId)
StoreService.Gift(player, key, recipientUserId)       -- (ok, message): Scribe's gift prompt for a Robux product
```

**Keys:** `"Crate:<crateId>"`, `"Item:<itemId>"`, `"Class:<classId>"`.

**How paying works:**

| Currency | How it's charged |
| --- | --- |
| Robux | Opens the product or game pass prompt. What it gives arrives with the **receipt** (`Shared.Data`, `Shared.StoreGrants`) |
| Coins, Tokens | `Data.Purchase`: the price comes off and the item is given **in one transaction, or neither happens**. Price: `Content.Store.PriceOf` (listed, less the daily deal) |

**Crates are never opened on purchase.** They wait in `CrateInventory`; `OpenCrate` takes one out and gives a random **unowned** skin (by weight) in one transaction, returning the skin so the client's reel can land on it. A crate whose skins are all owned can't be bought or opened. `OpenWithBonus(player, crateId, count)` opens several with the bonus roll.

```lua
local Store = game.ServerScriptService.Modules.Systems.Store
local StoreService = require(Store.StoreService)
```

### `StoreService.Buy(player, key, currency) → (ok, message, skinId?)`

Buys a crate, item or class with `"Robux"`, `"Coins"` or `"Tokens"`. Coins/Tokens: one Scribe transaction (price off and item in, or neither). Robux: opens the prompt; the grant arrives with the receipt. What `Packets.Store.Buy` calls.

```lua
local ok, message = StoreService.Buy(player, "Crate:Glacier", "Coins")
local ok2 = StoreService.Buy(player, "Class:" .. classId, "Coins") -- a locked class (Content.Store.CLASS_PRICES)
```

### `StoreService.OpenCrate(player, crateId) → (ok, message, skinId)`

Opens one crate from the player's `CrateInventory`: a random **unowned** skin by weight, in one transaction. The skin Id lets the client's reel land on it.

```lua
local ok, message, skinId = StoreService.OpenCrate(player, "Glacier")
```

### `StoreService.OpenWithBonus(player, crateId, count)` / `StoreService.OpenThree(player, crateId)`

Open several at once with the bonus roll (the Inventory's reel; what `Store.OpenMany` calls).

```lua
StoreService.OpenWithBonus(player, "Glacier", 3)
```

### `StoreService.Give(player, currency, amount, reason)`

Pays out currency (battle pass, quests, level-ups, rewards). Fires `Store.Given`; the client gets `Store.Reward`.

```lua
StoreService.Give(player, "Coins", 250, "Event")
```

### `StoreService.Perk(player, perk) → number`

The product of that perk over every pass the player owns (`1` with none). VIP's double coins is a perk.

```lua
local coins = math.floor(100 * StoreService.Perk(player, "CoinMultiplier"))
```

### `StoreService.OwnsClass(player, classId) → boolean` / `StoreService.OwnsPass(player, itemId) → boolean`

Free classes count as owned; locked ones once bought or given.

```lua
if not StoreService.OwnsClass(player, classId) then return false, "Unlock this class in the store." end
```

### `StoreService.Gift(player, key, recipientUserId) → (ok, message)`

Scribe's gift prompt for a Robux product (crates and store items only, to a player in this server who could receive it). The gift is delivered to the recipient's data even if they leave.

```lua
StoreService.Gift(player, "Crate:Glacier", friend.UserId)
```

### `StoreService.GiveSkins(player, skinIds, take?)` / `StoreService.DeveloperSkins() → { string }`

Give or take skins directly (the `givedevskins` / `takedevskins` commands use the Developer pack).

```lua
StoreService.GiveSkins(player, StoreService.DeveloperSkins())
StoreService.GiveSkins(player, { "GlacierRifle" }, true) -- take it back
```

### `StatsService.Record(player, modeId, categoryId, won)`

Saves a match result into `Wins`, `Losses` and `Stats` (and `TotalWins`). Fires `Stats.Recorded`.

```lua
local StatsService = require(Store.StatsService)
local mode = MatchmakingContent.GetMode(record.Mode)
StatsService.Record(player, mode.Id, mode.Category, won)
```

`BotCoinService` pays `REWARDS.BotKill` Coins for an NPC kill (no API).

| Point | Kind | Arguments |
| --- | --- | --- |
| `Store.PreventBuy` | Any | player, key, currency |
| `Store.Bought` | Fire | player, key, currency (Coins/Tokens purchases) |
| `Store.CrateOpened` | Fire | player, crateId, skinId |
| `Store.Given` | Fire | player, currency, amount, reason |
| `Stats.Recorded` | Fire | see [Store](../../STORE.md) |

## Skins

```lua
local Skins = require(game.ReplicatedStorage.Content.Guns.Skins.Skins)
local skin = Skins.Get("GlacierRifle")                  -- { Id, Name, WeaponId = "AssaultRifle", ... }
Skins.Apply(gunModel, "GlacierRifle", "AssaultRifle")   -- paint a model
print(Skins.FamilyOf("AssaultRifle"), Skins.EquipField("AssaultRifle")) -- "AssaultRifle", "AssaultRifleSkin"
```

`Content.Guns.Skins.Skins`: `List`, `Get(id)`, `ForWeapon`, `Weapons`, `Choices`, `EquipField`, `Apply(model, skinId?, weaponId?)`. `Skins.FamilyOf(gunId)` gives the family a gun wears (`"AssaultRifle"`, `"Pistol"`, else its own Id). `SkinShopService.StyleTool(player, tool)` applies the equipped skin to a gun Tool (`LoadoutService.Arm` calls it). Parts tagged `SkinRainbow` are animated by `Client.Guns.SkinRainbow`.

## Battle pass and quests

```lua title="Systems.BattlePass.QuestService:Start (what counts toward quests)"
Extensions.Add("Combat.Death", onDeath)                        -- Kills, GuardKills
Extensions.Add("Siege.Ended", onSiegeEnded)                    -- MatchesPlayed, MatchesWon, SiegeWins, Damage...
Extensions.Add("Siege.Planted", inMatch("BombsPlanted"))
Extensions.Add("Drone.Spotted", inMatch("DroneScans"))
Extensions.Add("Breakable.Repaired", inMatch("BoardsBuilt"))
Extensions.Add("Classes.AbilityUsed", inMatch("AbilitiesUsed"))
Extensions.Add("Store.CrateOpened", function(player) QuestService.Add(asPlayer(player), "CratesOpened") end)
```

Only **public** matches count (a private PLAY WITH PARTY match counts for nothing). Everyone gets the same dailies and weeklies: they're drawn with the UTC day/week number as the seed, so every server picks the same ones.

```lua
local BattlePass = game.ServerScriptService.Modules.Systems.BattlePass
local QuestService = require(BattlePass.QuestService)
local BattlePassService = require(BattlePass.BattlePassService)
```

### `QuestService.Add(player, stat, amount?)`

Counts toward every quest in the player's sets with that `Stat` (capped at its Goal). Reaching it pays its XP once. Any system may call it.

```lua
QuestService.Add(player, "Kills")         -- +1
QuestService.Add(player, "Damage", 120)   -- +120
```

### `BattlePassService.AddXP(player, amount, reason)`

Battle pass XP, scaled by the `BattlePass.XPMultiplier` extension point (Product). The client gets `BattlePass.Progress`.

```lua
BattlePassService.AddXP(player, 50, "Event")
```

### `BattlePassService.Claim(player, rewardId) → (ok, message)`

Claim a reached reward, or `"ALL"` for everything claimable.

```lua
local ok, message = BattlePassService.Claim(player, "ALL")
```

### `BattlePassService.Level(player) → number`

```lua
if BattlePassService.Level(player) >= 10 then unlockTitle(player) end
```

With `Content.BattlePass.ENABLED` false, quests still run and pay Coins (`XP * Quests.COIN_SHARE`). A completed quest also gives account XP and Weekly Goal points (`ProgressService`).

| Point | Kind | Arguments |
| --- | --- | --- |
| `BattlePass.LevelUp` / `BattlePass.Claimed` | Fire | player, level / player, rewardId |
| `BattlePass.XPMultiplier` | Product | player, reason |
| `Quests.Completed` | Fire | player, questId, xp |

## Packets

| Packet | Direction | Arguments / answer |
| --- | --- | --- |
| `Store.Buy` | Client → server, answered | key, currency → ok, message, skinId (`""` unless a Coins/Tokens crate gave one) |
| `Store.Open` / `Store.OpenMany` | Client → server, answered | crateId (, count) → ok, message, skinId(s) (, outcomes) |
| `Store.Gift` | Client → server, answered | key, recipient UserId → ok, message |
| `Store.Reward` | Server → one client | amount, currency, reason |
| `Skins.Equip` / `Skins.BuyCrate` | Client → server, answered | skinId / — → ok, message |
| `BattlePass.Claim` | Client → server, answered | rewardId or `"ALL"` → claimed, message |
| `BattlePass.Progress` | Server → one client | amount, reason, level |
| `Progress.Board` | Client → server, answered | board Id → rows, own `{ Rank?, Value }` |
| `Progress.Seen` / `Asked` / `Zone` | Client → server | what was celebrated / prompt shown / UTC offset minutes |
| `Progress.Earned` | Server → one client | kind, line, reward line |
| `Analytics.MenuOpened` | Client → server | a name in `Content.Analytics.MENUS` |

## Example: pay a reward

```lua
local Systems = game.ServerScriptService.Modules.Systems
local StoreService = require(Systems.Store.StoreService)
local QuestService = require(Systems.BattlePass.QuestService)

StoreService.Give(player, "Coins", 250, "Event")  -- fires Store.Given; client gets Store.Reward
QuestService.Add(player, "Kills", 1)
```

!!! warning "Grants must not yield"

    A product's `Grant` runs inside a Scribe transaction. No `WaitForChild`, no `task.wait`, no web calls inside it.

More: [Player data, coins and progression](../../EXAMPLES.md#player-data-coins-and-progression).
