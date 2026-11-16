# Battle Pass and Quests

Added 2026-11-16, changed the same day to a level track (no Battle Stars). A seasonal battle pass: XP fills levels, and every level has a **Free** reward (everyone) and a **Premium** reward (pass owners), claimed once the level is reached. Quests (daily, weekly, milestones) are the main source of XP.

## Where things are

| What | Where |
| --- | --- |
| The season, the level track, XP numbers, saved pass fields | `ReplicatedStorage.Content.BattlePass` (ScribeFragment) |
| Quest lists and saved quest fields | `ReplicatedStorage.Content.Quests` (ScribeFragment) |
| The season's exclusive skins (Breach Point) | `ReplicatedStorage.Content.Guns.SeasonSkins`, added by `Content.Guns.Skins`; finish profile `BreachPoint` in `SkinFinish`; charm model `Assets.Models.Charms.BreachPointCharm` (a copy of RocketCharm) |
| XP, levels, claims, match XP | `ServerScriptService.Modules.Systems.BattlePass.BattlePassService` |
| Quest sets, counting, quest XP | `ServerScriptService.Modules.Systems.BattlePass.QuestService` |
| The screen | `Main.BattlePass` (built in Studio from a copy of the Inventory panel), `Client.Core.BattlePass`; templates `BPLevel` (a level column), `BPQuestRow`, `NavButton`, `SectionHeader`; the XP line `Main.PassToast`; the lobby button `Main.Wallet.PassButton` |
| The premium pass | Store item `BattlePassS1` (`Content.Store.Store`, Section Passes, 399 Robux, giftable), grant `BattlePass = "S1"` (`StoreGrants.GivePremium`) |
| Packets | `Packets.BattlePass.Claim(rewardId or "ALL")` -> (ok, message); `Packets.BattlePass.Progress(amount, reason, level)` server -> client |

## How it works

**Research behind it** (2026-11-16): battle passes have a free track and a premium track; a casual player should be able to finish most of it; daily quests (reset each day), weekly quests (bigger, reset weekly) and milestones (staged, all season) are the main XP source. The screen follows the tiered Roblox battle pass the owner showed: a season card with the level bar, a summary and gift button, one column per level with a Free and a Premium row, and the picked reward big on the right.

### Levels

- 50 levels of 1,500 XP (75,000 XP). XP stops at the season's end (`SEASON.Ends`, 2027-02-01 00:00 UTC) and at level 50.
- Each level has one Free and one Premium reward (`TRACK`, made from `ROWS`). A reward's Id is `S1_L<level>_F` or `S1_L<level>_P`.
- A reward can be claimed once its level is reached; a Premium one also needs the pass. Buying the pass later unlocks every Premium reward already reached. **CLAIM ALL** claims everything claimable at once.
- A skin or class already owned pays 500 Coins instead.
- The whole track: 32,850 Coins, 10 Breach Point skins (only from the pass; the knife at level 50), 6 classes (Cyrus 8, Elliot 12, Carter 18, Matteo 24, phily 32, Caleb 40), 36 crates.

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

It uses the Store's and Inventory's own parts: the same panel, title and red X, the left rail of nav buttons (**PASS**, **QUESTS**), dark section panels with the slate outline, gold highlights. Opened from **BATTLE PASS** under STORE and INVENTORY in the lobby (it shows the level and how many rewards wait to be claimed).

- **PASS:** top left, the season card (name, time left, Lv. now -> Lv. next, the XP bar). Next to it, what the pass holds (colored), **GET BATTLE PASS** (Robux prompt; PASS OWNED once bought), **GIFT** (gift picker) and **CLAIM ALL (n)**. Below, the level track: one column per level (the number, gold once reached, blue for the next), a FREE cell and a PREMIUM cell (✓ when claimed, a gold outline when it can be claimed now, a lock when its level isn't reached or it needs the pass). It scrolls to your level when opened. Right: the picked reward big (a model turns), its kind, name, level, description and CLAIM. Clicking a claimable cell twice claims it.
- **QUESTS:** DAILY QUESTS (time to new ones, and the all-done bonus as a row), WEEKLY QUESTS, MILESTONES, each a row with a progress bar, count and XP.
- Earning XP anywhere shows "+400 XP · Daily: Play 3 matches" at the top, and LEVEL n! when a level is reached.

### Saved data

- `BattlePass`: `Season`, `XP`, `Premium` (0/1), `Claimed` (reward Ids); `Spent` is unused since the stars were removed.
- `Quests`: `Season`, `Day`, `Week`, `Daily`, `Weekly` (quest Ids), `DailyProgress`, `WeeklyProgress`, `Milestones` (`{ Value, Done }` each), `Bonus` (the day the daily bonus was paid).
- A player whose pass is from another season starts fresh at join.

## A new season

1. `Content.BattlePass`: a new `SEASON` (new Id, name, end time), new `ROWS`, and `PREMIUM_ITEM` set to a new store item.
2. `Content.Store.Store`: a new item like `BattlePassS1` with `Grants = { BattlePass = "<new Id>" }`, and its Robux product at `Store_<Id>` in `Shared.ProductIds`.
3. `Content.Guns.SeasonSkins`: a new set (Prefix, Source collection, palette) and a matching profile in `SkinFinish`.

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
