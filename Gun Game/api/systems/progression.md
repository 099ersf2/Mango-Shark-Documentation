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

Other functions: `GiveSkins(player, skinIds, take?)` and `DeveloperSkins()` (the `givedevskins` / `takedevskins` commands), `StatsService.Record(player, modeId, categoryId, won)`.

| Point | Kind | Arguments |
| --- | --- | --- |
| `Store.PreventBuy` | Any | player, key, currency |
| `Store.Bought` | Fire | player, key, currency (Coins/Tokens purchases) |
| `Store.CrateOpened` | Fire | player, crateId, skinId |
| `Store.Given` | Fire | player, currency, amount, reason |
| `Stats.Recorded` | Fire | see [Store](../../STORE.md) |

## Skins

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

| Function | What it does |
| --- | --- |
| `QuestService.Add(player, stat, amount?)` | Counts toward every quest with that `Stat`. Other systems may call it |
| `BattlePassService.AddXP(player, amount, reason)` | Battle pass XP |
| `BattlePassService.Claim(player, rewardId or "ALL")` | Claim a reached reward |
| `BattlePassService.Level(player)` | The pass level |

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
