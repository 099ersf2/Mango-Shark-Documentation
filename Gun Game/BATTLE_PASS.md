[Documentation home](index.md) / Gun Game

# Battle Pass and Quests

Added 2026-11-16, changed the same day to a level track (no Battle Stars). A seasonal battle pass: XP fills levels, and every level has **Free** rewards (everyone) and **Premium** rewards (pass owners), claimed once the level is reached. A side can hold one reward, several, or none. Quests (daily, weekly, milestones) are the main source of XP.

**Off for now (2026-11-16):** `Content.BattlePass.ENABLED = false` keeps the pass for its own update. No XP, quests or claims, and nothing of it is shown (button, screen, store item, unowned season skins, the Season 1 tag). To launch: set `ENABLED = true`, check `SEASON.Ends`, and put the Robux product's id at `Store_BattlePassS1` in `Shared.ProductIds`.

> **2026-11-18:** quests now run while the pass is off and pay `XP * Content.Quests.COIN_SHARE` coins instead of pass XP; they show on the GOALS menu (`Client.Core.Goals`). A completed quest also gives account XP and Weekly Goal points ([PROGRESSION.md](PROGRESSION.md)).

## Where things are

| What | Where |
| --- | --- |
| The season, the level track, XP numbers, saved pass fields | `ReplicatedStorage.Content.BattlePass` (ScribeFragment) |
| Quest lists and saved quest fields | `ReplicatedStorage.Content.Quests` (ScribeFragment) |
| The season's exclusive skins (Breach Point) | `ReplicatedStorage.Content.Guns.Skins.SeasonSkins`, added by `Content.Guns.Skins.Skins`; finish profile `BreachPoint` in `SkinFinish`; charm model `Assets.Models.Charms.BreachPointCharm` (a copy of RocketCharm) |
| XP, levels, claims, match XP | `ServerScriptService.Modules.Systems.BattlePass.BattlePassService` |
| Quest sets, counting, quest XP | `ServerScriptService.Modules.Systems.BattlePass.QuestService` |
| The screen | `Main.BattlePass` (built in Studio from a copy of the Inventory panel), `Client.Core.BattlePass`; templates `BPLevel` (a level column), `BPQuestRow`, `NavButton`, `SectionHeader`; the XP line `Main.PassToast`; the lobby button `Main.Wallet.PassButton` |
| The premium pass | Store item `BattlePassS1` (`Content.Store.Store`, Section Passes, 399 Robux, giftable), grant `BattlePass = "S1"` (`StoreGrants.GivePremium`) |
| Packets | `Packets.BattlePass.Claim(rewardId or "ALL")` -> (ok, message); `Packets.BattlePass.Progress(amount, reason, level)` server -> client |

## How it works

**Research behind it** (2026-11-16): battle passes have a free track and a premium track; a casual player should be able to finish most of it; daily quests (reset each day), weekly quests (bigger, reset weekly) and milestones (staged, all season) are the main XP source. The screen follows the tiered Roblox battle pass the owner showed: a season card with the level bar, a summary and gift button, one column per level with a Free and a Premium row, and the picked reward big on the right.

### Levels

- 50 levels of 1,500 XP (75,000 XP). XP stops at the season's end (`SEASON.Ends`, 2027-02-01 00:00 UTC) and at level 50.
- Each level has a list of Free and a list of Premium rewards (`TRACK[level] = { Free = { ... }, Premium = { ... } }`, made from `ROWS`; `LIST` holds every reward). A reward's Id is `S1_L<level>_F` or `S1_L<level>_P`, and `_F2` / `_P2` for a level's second reward on that side.
- Season 1 (2026-11-16):
  - **Coins** are always 250 (`COINS`), and every 5th level pays **1,000** (`COINS_BIG`) on the Free side.
  - **Empty Free levels:** 2, 7, 12, 16, 19, 23, 27, 31, 34, 38, 42, 44, 47.
  - **Two rewards:** levels 1, 8, 15, 25, 32, 40, 45 and 50.
  - **Classes:** only at level 50: Matteo (Medic) free, Caleb (Hacker) premium, beside the Breach Point Knife.
  - A Breach Point skin on every 5th Premium level; the Breach Point Charm free at 8 and the Season 1 Dog Tag charm free at 45.
- A reward can be claimed once its level is reached; a Premium one also needs the pass. Buying the pass later unlocks every Premium reward already reached. **CLAIM ALL** claims everything claimable at once.
- A skin or class already owned pays 500 Coins instead.
- The whole track: 21,750 Coins, 11 season skins (only from the pass; the knife at level 50), 2 classes, 31 crates, in 97 rewards.
- **Season tag:** skins and classes the pass gives show the season (`SEASON.Tag`, "Season 1") before their rarity or team wherever they're listed (`BattlePass.SeasonOf(kind, ref)`). On an Inventory card a season skin's line is "Season 1 · Epic" (no gun, so it fits a phone).

### Quests

| Kind | How many | Reset | XP |
| --- | --- | --- | --- |
| Daily | 3, drawn from 9 (the same for everyone) | 00:00 UTC | 350 to 450 each; all 3 done: +500 |
| Weekly | 5, drawn from 10 (the same for everyone) | Tuesday 00:00 UTC | 1,000 to 1,800 each |
| Milestones | 5, always on | the season | 500 or 600 per stage, 5 stages each |

Everyone has the same quests (2026-11-16): the draw is seeded with the UTC day number (dailies) or the week number (weeklies), so every server picks the same ones.

Counted (public matches only; private matches count for nothing, so they can't be farmed): enemies taken down, Clear House guards taken down, matches played and won (Siege and Clear House apart too), damage, doors and windows rebuilt to whole, defusers planted, drone scans, abilities used, crates opened (anywhere).

### Match XP

Every public match finished: 120 XP, +120 for a win, +15 per kill (10 at most).

### The screen

It uses the Store's and Inventory's own parts: the same panel, title and red X, the left rail of nav buttons (**PASS**, **QUESTS**), dark section panels with the slate outline, gold highlights. Opened from **BATTLE PASS** under STORE and INVENTORY in the lobby (it shows the level and how many rewards wait to be claimed); pressing it again closes the screen.

- **PASS:** top left, the season card (name, time left, Lv. now -> Lv. next, the XP bar). Next to it, what the pass holds (colored), **GET BATTLE PASS** (Robux prompt; PASS OWNED once bought), **GIFT** (gift picker) and **CLAIM ALL (n)**. Below, the level track: one column per level (the number, gold once reached, blue for the next), the FREE and PREMIUM rewards (two side by side in a wider column, a dim empty slot when a side has none; ✓ when claimed, a gold outline when it can be claimed now, a lock when its level isn't reached or it needs the pass). It scrolls to your level when opened. Right: the picked reward big (a model turns), its kind, name, level, description and CLAIM. Clicking a claimable cell twice claims it.
- **QUESTS:** DAILY QUESTS (time to new ones, and the all-done bonus as a row), WEEKLY QUESTS, MILESTONES, each a row with a progress bar, count and XP.
- Earning XP anywhere shows "+400 XP · Daily: Play 3 matches" at the top, and LEVEL n! when a level is reached.

### Saved data

- `BattlePass`: `Season`, `XP`, `Premium` (0/1), `Claimed` (reward Ids); `Spent` is unused since the stars were removed.
- `Quests`: `Season`, `Day`, `Week`, `Daily`, `Weekly` (quest Ids), `DailyProgress`, `WeeklyProgress`, `Milestones` (`{ Value, Done }` each), `Bonus` (the day the daily bonus was paid).
- A player whose pass is from another season starts fresh at join.

## A new season

0. `ENABLED` must be `true` for the pass to run at all.
1. `Content.BattlePass`: a new `SEASON` (new Id, name, end time), new `ROWS`, and `PREMIUM_ITEM` set to a new store item.
2. `Content.Store.Store`: a new item like `BattlePassS1` with `Grants = { BattlePass = "<new Id>" }`, and its Robux product at `Store_<Id>` in `Shared.ProductIds`.
3. `Content.Guns.Skins.SeasonSkins`: a new set (Prefix, Source collection, palette) and a matching profile in `SkinFinish`.

## Tested (2026-11-16, Studio playtest, one player)

First version (stars and pages), then the level track the same day:

- At join the pass and quests were set to season S1, with 3 dailies and 5 weeklies drawn.
- Quests: finishing a daily paid its XP; 5 wins reached the first Wins milestone stage and finished the weekly "Win 5 matches".
- Level track: 10,500 XP gave level 7. Level 8's reward was refused ("Reach level 8"), a Premium one without the pass was refused, level 1's free 200 Coins was claimed, then CLAIM ALL took the 6 other free rewards up to level 7 (coins 308 -> 1,458, a Shield and an Afterburn crate); a second CLAIM ALL had nothing left.
- The screen: Lv. 7 -> Lv. 8, the XP bar, the time left, GET BATTLE PASS, CLAIM ALL (7), 50 level columns scrolled to level 7, the Breach Point Knife in the preview; the lobby button read LEVEL 7 · 7 TO CLAIM.
- All test data was removed afterwards (coins, crates, the charm, XP, claims, quest progress).
- **Not seen:** the 3D models in the cells and the preview (Studio wasn't drawing 3D while the screenshots were taken; the models are there).

## Not done yet

- **The pass can't be bought yet:** the store item has no Robux product (`Store_BattlePassS1` in `Shared.ProductIds`), so GET BATTLE PASS shows the store's "isn't for sale yet". Create a developer product and put its id there.
- Not tested: a real match paying XP and quest progress, the LEVEL UP line in a match, buying and gifting the pass, the screen on a phone.
