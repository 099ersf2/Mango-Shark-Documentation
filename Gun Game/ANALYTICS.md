# Analytics

*Added 2026-11-14.*

Everything is reported to Roblox analytics (Creator Hub → your experience → Analytics) by `Systems.Analytics.AnalyticsService`, from the server only.

- **Names:** every event, funnel step and journey node is listed in `ReplicatedStorage.Content.Analytics`.
- **Studio:** nothing is sent from Studio (Roblox ignores it). With `PRINT_IN_STUDIO`, each event is printed in the Output as `[Analytics] ...` instead.

## Roblox's rules

- Events are only sent from the server, and only in a published game.
- **Custom events:** at most 100 names. Use custom fields instead of new names.
- **Custom fields:** up to 3 per event (`CustomField01..03`), with up to 8,000 unique combinations of values.
- **Rate:** a game-wide limit of 120 + 20 × CCU requests a minute. Each server keeps to its share (`BUDGET_BASE` + `BUDGET_PER_PLAYER` × players). Past `LOW_SHARE` of it, Kill, AbilityUsed and MenuOpened are skipped first.
- **Funnels:** a recurring funnel keeps the 10 most recent session ids per player. Only the first time a step is reached counts.
- **Journeys:** must be **created on the Creator Hub first** (see below). Events for nodes that aren't in the published journey don't count.
- **Delay:** dashboards fill in up to a day later.

## What it answers

| Question | Where to look |
| --- | --- |
| Where players drop out of the queue | Funnel **Queue** (Queued → MatchFound); custom **QueueEnded** by Outcome (Matched, Cancelled, Disbanded…); value = seconds waited |
| Where players drop out of a match | Funnel **Match** (Arrived → Selection → PickedClass → Prep → Action → RoundFinished → MatchFinished); **MatchLeftEarly** by Phase and Side |
| New players' first match | Onboarding funnel (Joined → Queued → MatchFound → ArrivedInMatch → FirstRoundFinished → FinishedMatch), only for players with no finished match |
| Top modes | **QueueJoined** by Mode, Category and PartySize; **MatchStarted** by Mode, Category and Map |
| Top classes | **ClassPicked** by Class, Side and Mode. **ClassRandom** counts classes given because the player picked none |
| Top sites and spawns | **SiteChosen** by Map, Site and Mode; **SpawnPicked** by Map, Spawn and Mode |
| Attackers or Defenders winning more | **RoundWon** by Side, Reason and Map (once per round); value = seconds of Action, so its average is the round length |
| Average kills per game | **PlayerKills**, by Mode, Category and Result (Won, Lost or Draw). Use the *Average value* metric. **PlayerDeaths**, **PlayerDamage** and **PlayerBuilt** work the same way. **MatchKills** totals the whole match by Mode, Category and Map |
| Match length in rounds | **MatchFinished** (value = rounds played) by Mode, Category and Map |
| Weapons and abilities | **Kill** by Weapon, Side and Mode; **AbilityUsed** by Class, Ability and Mode |
| Objective play | **DefuserPlanted** by Map, Site and Bomb; **SiteLocated** by Map and Mode (value = seconds into the phase) |
| Menus | **MenuOpened** by Menu and Place (Lobby or Match) |
| Store | **StoreBought** by Key, Currency and Kind; **RobuxPurchase** by Product and Category (value = listed Robux price); **CrateOpened** by Crate and Skin |
| Coins and Tokens economy | Economy events (below) |

## Economy events

| Flow | When | Transaction type | SKU |
| --- | --- | --- | --- |
| Source | Match rewards (`StoreService.Give`) | Gameplay (Playtime: TimedReward) | the reason (Victory, Match played, Draw, Playtime…) |
| Sink | Coins or Tokens spent in the Store | Shop | the store key (`Crate:Field`, `Item:Coins5000`…) |
| Source | Coins or Tokens granted by a pack bought with Coins or Tokens | Shop | the store key |
| Source | Coins or Tokens granted by a Robux pack | IAP | the product name (`Store_Tokens150`…) |

The balance after is read from the player's data.

## Journeys: create these on the Creator Hub

Go to Analytics → Journeys → **Create**. Enter the stages and nodes **exactly** as below; the nodes of a stage are alternatives. Then select Next and Acknowledge to publish. The game already logs them. Each lobby visit and each match is its own session.

**LobbyVisit**

| Stage | Nodes |
| --- | --- |
| 1 Arrive | NewPlayer, ReturningPlayer |
| 2 Browse | Store, Inventory, SkinShop, Loadout, Modes |
| 3 Spend | BoughtWithCoins, BoughtWithTokens, BoughtWithRobux |
| 4 Queue | QueuedSolo, QueuedParty |
| 5 Outcome | MatchFound, LeftQueue |

**SiegeMatch**

| Stage | Nodes |
| --- | --- |
| 1 Side | Attacker, Defender |
| 2 Class | PickedClass, RandomClass |
| 3 FirstRound | WonRound, LostRound, DrawRound |
| 4 Match | WonMatch, LostMatch, DrawMatch, LeftEarly |

A player who skips a stage (for example, queues without opening a menu) is shown as having skipped it.

## Where things are

| What | Where |
| --- | --- |
| Names, funnels, journeys, budget, menus | `ReplicatedStorage.Content.Analytics` |
| All logging | `ServerScriptService.Modules.Systems.Analytics.AnalyticsService` |
| Menu opens (the only client report) | `Client.Core.AnalyticsClient` → `Packets.Analytics.MenuOpened` (checked against `MENUS`, at most one per menu every `MENU_COOLDOWN` s) |
| Siege data it uses | `Siege.SelectionEnded` (final picks), `Siege.RoundEnded` (4th argument: mode, map, site), `Siege.Ended` (3rd argument: the match summary with every player's stats) |
| Robux purchases | `MarketplaceService.PromptProductPurchaseFinished`. `ProcessReceipt` can't be read; Scribe owns it |

## API

```lua
AnalyticsService.Custom(player, "EventName", value?, field1?, field2?, field3?) -- name must be in Content.Analytics.EVENTS
AnalyticsService.Economy(player, "Source"/"Sink", "Coins"/"Tokens", amount, transactionType, sku?)
AnalyticsService.Funnel(player, funnelName, sessionId, stepName)  -- steps from Content.Analytics.FUNNELS
AnalyticsService.Onboarding(player, stepName)                     -- only for players with no finished match
AnalyticsService.Journey(player, journeyName, nodeName, sessionId?)
```

To track something new, add the name to `Content.Analytics.EVENTS` (there are 23 of the 100 allowed) and call `Custom` from a listener in `AnalyticsService:Start`.

## Tested (2026-11-14, Studio playtest, one player, 1v1 as attacker)

The Output showed, in order:
- LobbyVisit ReturningPlayer;
- MenuOpened Store, then LobbyVisit Store;
- Queue funnel step 1 and QueueJoined `1v1, Siege, Solo`;
- QueueEnded `6 s, Matched`, then Queue step 2 and LobbyVisit MatchFound;
- Match funnel steps 1, 2, 4 and 5;
- MatchStarted `1v1, Siege, Bank`;
- ClassRandom `Hacker, Attackers`, SpawnPicked `Bank, Backdoor` and SiteChosen `Bank, Upstairs`;
- the SiegeMatch nodes Attacker and RandomClass;
- RoundWon `Defenders, AttackersDead, Bank` (3 s), then Match step 6 and SiegeMatch LostRound.

**Not checked:**
- The end of a whole match: PlayerKills, MatchFinished, the Match step MatchFinished, and the won/lost match nodes.
- Economy events from a real purchase.
- Robux purchase events.
- What a live server actually sends to the dashboard.

## Limits

- **SpawnPicked:** counts spawns filled in at random too, not only chosen ones.
- **Match-wide events:** MatchStarted, SiteChosen, RoundWon, MatchFinished and MatchKills are attached to one player in the server, because Roblox needs a player for every event. Count them, not their unique users.
