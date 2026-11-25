# Progress, leaderboards and analytics

The reasons to come back (flame streak, weekly goal, account level, ranked, badges), the game-wide leaderboards, flame reminders, and everything the game reports to Roblox analytics.

!!! abstract "Source"

    `Systems.Progress.ProgressService`, `LeaderboardService`, `NotifyService`; `Systems.Analytics.AnalyticsService`. Data: `Content.Progress`, `Content.Analytics`. Client: `Client.Core.Goals`, `Client.Core.Celebrate`, `Client.Core.AnalyticsClient`. Guides: [Progression and retention](../../PROGRESSION.md), [Analytics](../../ANALYTICS.md).

## What `ProgressService` tracks

| | How it grows |
| --- | --- |
| **Flame streak** | One public match in the player's 8 PM–12 AM window (their own clock, sent with `Packets.Progress.Zone`) grows it. A missed window puts it out unless a Shield covers it |
| **Weekly Goal** | Points from matches, wins, quests and flame days; each tier pays at once; resets with the weeklies |
| **Level** | Account XP from matches, wins, kills, quests and flame days; each level pays coins |
| **Ranked** | An Elo rating from the `Ranked` queue mode; a new season pulls it halfway back to the start |
| **Badges** | `Content.Progress.BADGES`, awarded when reached (ids still `0` are skipped) |

Only **public** matches count (PLAY WITH PARTY and training count for nothing). Match results come from `Siege.Ended`; quests from `Quests.Completed`. The lobby celebrates new progress by comparing saved values with what the client last saw (`Packets.Progress.Seen`).

```lua
local ProgressService = require(game.ServerScriptService.Modules.Systems.Progress.ProgressService)
```

### `ProgressService.AddXP(player, amount, reason)`

Adds account XP (whole, above 0). Every level reached pays `LEVEL_COINS` (plus `LEVEL_BONUS` every `LEVEL_BONUS_EVERY` levels), tells the player with `Progress.Earned`, and awards the Level10/25/50 badges.

```lua
ProgressService.AddXP(player, 150, "Event")
```

```lua title="ProgressService.AddXP (the level-up loop)"
local before = Progress.LevelOf(data.Progress.XP.Get() or 0)
data.Progress.XP.Increment(xp)
local after = Progress.LevelOf(data.Progress.XP.Get() or 0)
for level = before + 1, after do
	local coins = Progress.LEVEL_COINS + (if level % Progress.LEVEL_BONUS_EVERY == 0 then Progress.LEVEL_BONUS else 0)
	give(player, coins, `Level {level}`)
	earned(player, "Level", `LEVEL {level}`, `+{coins} coins`)
end
Extensions.Fire("Progress.Changed", player)
```

### `ProgressService.AddPoints(player, amount, reason)`

Weekly Goal points. Each tier of `Content.Progress.WEEKLY_TIERS` reached pays its reward once; finishing them all awards `WeeklyDone`.

```lua
ProgressService.AddPoints(player, 20, "Event")
```

### `ProgressService.Award(player, badgeKey)`

Awards a `Content.Progress.BADGES` badge once per session (checks `UserHasBadgeAsync` first). Ids still `0` are skipped.

```lua
ProgressService.Award(player, "Level10")
```

### `ProgressService.FlameBonus(player) → number`

The match coin bonus share the player's flame gives right now (`0` when out).

```lua
local coins = math.floor(baseCoins * (1 + ProgressService.FlameBonus(player)))
```

| Point | Kind | Arguments |
| --- | --- | --- |
| `Progress.FlameGrew` | Fire | player, count, tz (NotifyService books a reminder) |
| `Progress.Changed` | Fire | player (a score the leaderboards show changed) |

## Leaderboards: `LeaderboardService`

Four boards (`Content.Progress.BOARDS`) in OrderedDataStores: **Weekly** (one store per week), **Flame**, **Level** (total XP) and **Ranked** (per season, once placed). Scores are written on join, on `Progress.Changed` (at most once per `BOARD_WRITE` s) and on leave. Reads are cached `BOARD_REFRESH` s per server. Every DataStore call is in a `pcall`; a failure keeps the old board.

No public functions. Clients ask with an answered packet:

```lua
-- Client
local rows, mine = Packets.Progress.Board:Fire("Weekly")
for _, row in rows do
	print(row.Rank, row.Name, row.Value)
end
print("You:", mine.Rank or "unranked", mine.Value)
```

## Flame reminders: `NotifyService`

When a flame grows, a reminder is booked in a MemoryStore SortedMap for when the player's next window opens. Growing it again re-books it, so only players who haven't played that day get one. Any lobby server sends due reminders once a minute through Open Cloud (claiming each first so two servers never both send).

**Off until set up:** it needs `NOTIFICATIONS.FlameReminder` (a message id), the experience secret `NOTIFY_SECRET`, and HTTP requests on. Booking runs anyway. Roblox only delivers to opted-in players aged 13+, at most once a day.

## Analytics: `AnalyticsService`

Everything is sent from the **server** (Roblox requires it) and mostly by **listening** to other systems' extension points. In Studio nothing is sent; with `Content.Analytics.PRINT_IN_STUDIO` each event is printed instead. A per-minute budget (`BUDGET_BASE + BUDGET_PER_PLAYER × players`) drops low-priority events first. Every call is wrapped, so a failed log never breaks the game.

```lua
local AnalyticsService = require(game.ServerScriptService.Modules.Systems.Analytics.AnalyticsService)
```

### `AnalyticsService.Custom(player, name, value?, field1?, field2?, field3?)`

A custom event. `name` **must be listed** in `Content.Analytics.EVENTS` or nothing is sent. Fields are cut to 50 characters.

```lua
-- EVENTS.ClassPicked = "Class, Side, Mode. A class the player chose"
AnalyticsService.Custom(player, "ClassPicked", 1, "Flash", "Attackers", "5v5")
```

Existing events: `QueueJoined`, `QueueEnded`, `MatchStarted`, `ClassPicked`, `ClassRandom`, `SiteChosen`, `SpawnPicked`, `RoundWon`, `MatchFinished`, `MatchKills`, `PlayerKills`, `PlayerDeaths`, `PlayerDamage`, `PlayerBuilt`, `MatchLeftEarly`, `Kill`, `AbilityUsed`, `DefuserPlanted`, `SiteLocated`, `MenuOpened`, `StoreBought`, `RobuxPurchase`, `CrateOpened`. To add one, add its name and field description to `EVENTS` (Roblox allows 100 names at most).

### `AnalyticsService.Economy(player, "Source" | "Sink", currency, amount, transactionType, sku?, field1?)`

Currency in or out (`Coins` or `Tokens`). `amount` is positive; the balance after is read from the data.

```lua
AnalyticsService.Economy(player, "Source", "Coins", 250, "Gameplay", "MatchWin")
AnalyticsService.Economy(player, "Sink", "Coins", 1200, "Shop", "Crate:Glacier")
```

### `AnalyticsService.Funnel(player, funnel, sessionId, stepName)`

A step of a recurring funnel (`Content.Analytics.FUNNELS`, by name; the step number comes from the list).

```lua
-- FUNNELS.Queue = { "Queued", "MatchFound" }
AnalyticsService.Funnel(player, "Queue", ticketId, "Queued")
AnalyticsService.Funnel(player, "Queue", ticketId, "MatchFound")
```

`Match` funnel steps: `Arrived`, `Selection`, `PickedClass`, `Prep`, `Action`, `RoundFinished`, `MatchFinished`.

### `AnalyticsService.Onboarding(player, stepName)`

A step of the onboarding funnel, logged only for players with no finished match yet.

```lua
-- ONBOARDING = { "Joined", "Queued", "MatchFound", "ArrivedInMatch", "FirstRoundFinished", "FinishedMatch" }
AnalyticsService.Onboarding(player, "Queued")
```

### `AnalyticsService.Journey(player, journey, node, sessionId?)`

A node of a journey (`Content.Analytics.JOURNEYS`: `LobbyVisit`, `SiegeMatch`). Unknown nodes aren't sent. Journeys must be created on the Creator Hub with the same names.

```lua
-- LobbyVisit stages: Arrive → Browse → Spend → Queue → Outcome; Browse nodes: Store, Inventory, SkinShop, Loadout, Modes
AnalyticsService.Journey(player, "LobbyVisit", "Store")
```

The client only reports menus: `Packets.Analytics.MenuOpened(name)` (a name in `Content.Analytics.MENUS`, sent by `Client.Core.AnalyticsClient` when `Menus` opens one).
