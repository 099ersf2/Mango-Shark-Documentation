# Battle Pass and Quests

Added 2026-11-16. A seasonal battle pass in the style of Fortnite's: XP fills levels, every level gives Battle Stars, and stars buy rewards on pages, in the order the player chooses. Quests (daily, weekly, milestones) are the main source of XP.

## Where things are

| What | Where |
| --- | --- |
| The season, pages, rewards, XP numbers, saved pass fields | `ReplicatedStorage.Content.BattlePass` (ScribeFragment) |
| Quest lists and saved quest fields | `ReplicatedStorage.Content.Quests` (ScribeFragment) |
| The season's exclusive skins (Breach Point) | `ReplicatedStorage.Content.Guns.SeasonSkins`, added by `Content.Guns.Skins`; finish profile `BreachPoint` in `SkinFinish` |
| XP, levels, stars, claims, match XP | `ServerScriptService.Modules.Systems.BattlePass.BattlePassService` |
| Quest sets, counting, quest XP | `ServerScriptService.Modules.Systems.BattlePass.QuestService` |
| The screen | `Main.BattlePass` (built in Studio), `Client.Core.BattlePass`; templates `BPPage`, `BPReward`, `BPQuestRow`; the XP line `Main.PassToast`; the lobby button `Main.Wallet.PassButton` |
| The premium pass | Store item `BattlePassS1` (`Content.Store`, Section Passes, 399 Robux, giftable), grant `BattlePass = "S1"` (`StoreGrants.GivePremium`) |
| Packets | `Packets.BattlePass.Claim(rewardId)` -> (ok, message); `Packets.BattlePass.Progress(amount, reason, level)` server -> client |

## How it works

**Research behind it** (2026-11-16): Fortnite's current pass is levelled with XP; each level gives Battle Stars that are spent on rewards page by page, in any order, and pages open at set levels; the last page is bonus rewards. Common practice across battle passes: a free track and a premium track; a pass a casual player can mostly finish; daily quests (reset each day), weekly quests (bigger, reset weekly) and milestones (staged, all season) as the main XP source.

### Levels and stars

- 50 levels of 1,500 XP (75,000 XP). Each level gives 5 Battle Stars: 250 stars over 50 levels, which is exactly what the six main pages cost.
- Bonus levels 51 to 100 keep giving stars, for the BONUS page (250 more stars).
- Stars on hand = level x 5 - stars spent. Nothing is spent automatically.
- XP stops at the season's end (`SEASON.Ends`, 2027-02-01 00:00 UTC).

### Pages and rewards

| Page | Opens at | Rewards | Stars | Free |
| --- | --- | --- | --- | --- |
| BOOT CAMP | level 1 | 8 | 30 | 3 (300 Coins, Breach Point Charm, Shield Crate) |
| FIRST CONTACT | level 8 | 8 | 40 | 3 (incl. the Elliot class) |
| BREACH | level 16 | 8 | 45 | 2 |
| HOLD THE LINE | level 24 | 8 | 45 | 2 |
| OVERRUN | level 32 | 8 | 45 | 2 |
| BREACH POINT | level 40 | 8 | 45 | 2 (last premium reward: Breach Point Knife, Mythic) |
| BONUS REWARDS | level 50, pass only | 7 | 250 | 0 |

- A page also opens as soon as every reward of the page before it is claimed (Fortnite does the same).
- Rewards: Coins, Breach Point skins (all 10), classes (Cyrus, Elliot, Carter, Matteo, phily, Caleb), crates (into the Inventory).
- A skin or class already owned pays 500 Coins instead.
- Free rewards can be claimed by everyone; the rest need the pass. Buying the pass later unlocks them, nothing is lost.

### Quests

| Kind | How many | Reset | XP |
| --- | --- | --- | --- |
| Daily | 3, drawn from 9 | 00:00 UTC | 350 to 450 each; all 3 done: +500 |
| Weekly | 5, drawn from 10 | Tuesday 00:00 UTC | 1,000 to 1,800 each |
| Milestones | 5, always on | the season | 500 or 600 per stage, 5 stages each |

Counted (public matches only; private matches count for nothing, so they can't be farmed): enemies taken down, Clear House guards taken down, matches played and won (Siege and Clear House apart too), damage, doors and windows rebuilt to whole, defusers planted, drone scans, abilities used, crates opened (anywhere).

### Match XP

Every public match finished: 120 XP, +120 for a win, +15 per kill (10 at most).

### The screen

Opened from **BATTLE PASS** under STORE and INVENTORY in the lobby (it shows the level and stars).

- Header: BATTLE PASS, SEASON 1 · BREACH POINT, REWARDS / QUESTS tabs.
- Bar: level badge, XP to the next level, Battle Stars, time left, **GIFT THE PASS** (gift picker) and **GET BATTLE PASS** (Robux prompt; PASS OWNED once bought).
- REWARDS: the pages (claimed count, lock with its level) and the open page's rewards (picture, name, kind, star cost, FREE or PASS ribbon, CLAIMED or a lock). What can be claimed now is outlined. A reward opens the detail page with **CLAIM (★ n)**, or why it can't be claimed.
- QUESTS: daily (with the time to new ones), weekly, milestones, each with a progress bar, count and XP.
- Earning XP anywhere shows "+400 XP · Daily: Play 3 matches" at the top, and LEVEL n! with the stars gained.

### Saved data

- `BattlePass`: `Season`, `XP`, `Premium` (0/1), `Spent`, `Claimed` (reward Ids).
- `Quests`: `Season`, `Day`, `Week`, `Daily`, `Weekly` (quest Ids), `DailyProgress`, `WeeklyProgress`, `Milestones` (`{ Value, Done }` each), `Bonus` (the day the daily bonus was paid).
- A player whose pass is from another season starts fresh at join.

## A new season

1. `Content.BattlePass`: a new `SEASON` (new Id, name, title, end time, featured skin), new pages and reward Ids (never reuse an Id), and `PREMIUM_ITEM` set to a new store item.
2. `Content.Store`: a new item like `BattlePassS1` with `Grants = { BattlePass = "<new Id>" }`, and its Robux product at `Store_<Id>` in `Shared.ProductIds`.
3. `Content.Guns.SeasonSkins`: a new set (Prefix, Source collection, palette) and a matching profile in `SkinFinish`.

## Tested (2026-11-16, Studio playtest, one player)

- At join: the pass and quests were set to season S1; 3 dailies and 5 weeklies were drawn.
- 8,000 XP gave level 5; finishing a daily paid its XP; 5 wins reached the first Wins milestone stage and finished the weekly "Win 5 matches" (level 7).
- Claims: a free coin reward (+300 Coins) and the free Breach Point Charm went through; a premium reward without the pass, a reward on a locked page, a second claim and an unknown Id were refused with their messages.
- The screen showed level 7, XP, 29 stars, the season countdown, the pages (BOOT CAMP open, the rest locked at their levels), the page's 8 rewards with CLAIMED and claimable states, and the quests with progress. The lobby button read LEVEL 7 · ★ 29.
- All test data was removed afterwards (coins, the charm, XP, claims, quest progress).

## Not done yet

- **The pass can't be bought yet:** the store item has no Robux product (`Store_BattlePassS1` in `Shared.ProductIds`), so GET BATTLE PASS shows the store's "isn't for sale yet". Create a developer product and put its id there.
- Not tested: a real match paying XP and quest progress, a level up toast in a match, buying and gifting the pass.
- No big featured render of the season's top reward like Fortnite's (`SEASON.Featured` is there for it).
