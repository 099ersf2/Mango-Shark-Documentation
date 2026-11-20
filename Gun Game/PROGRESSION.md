# Progression and retention

*Added 2026-11-18.* What brings players back: daily and weekly goals, the Flame streak, the Weekly Goal, account level, Ranked, career stats, leaderboards, badges, reminders, and bot-filled matches so nobody waits alone. Tuning is in `ReplicatedStorage.Content.Progress` (a ScribeFragment: it also declares the saved fields under `Progress`).

## Where things are

| Piece | Where |
| --- | --- |
| Tuning and saved fields | `Content.Progress` |
| Flame, Weekly Goal, level, career, ranked rating, badges | `Systems.Progress.ProgressService` |
| Leaderboards (OrderedDataStores) | `Systems.Progress.LeaderboardService` |
| Flame reminders (experience notifications) | `Systems.Progress.NotifyService` |
| GOALS menu and the flame chip in the nav | `Client.Core.Goals`, UI `Main.Goals`, `Main.Wallet.Buttons.GoalsButton` / `FlameChip` |
| The flame drawing | `Client.Core.FlameFx` (UI shapes only, no images) |
| Celebrations and prompts | `Client.Core.Celebrate`, UI `Main.FlameBurst`, `Main.EarnedToast` |
| Packets | `Packets.Progress` (Board, Seen, Asked, Earned) |
| Bot fill and Ranked queue rules | `Systems.Matchmaking.QueueService`, `Content.Matchmaking` (`BotFill`, `MinLevel`) |
| Quests without the pass | `Systems.BattlePass.QuestService`, `Content.Quests.COIN_SHARE` |

## What counts

A **public** match: queued from PLAY, bots included. PLAY WITH PARTY (private) and Recruit Training count for nothing, like quests. Results come from `Siege.Ended` (Clear House ends through it too).

## Flame streak

- One public match on a UTC day grows the flame by one (once a day). Miss a whole day and it goes out (back to 1 on the next match), unless a **Shield** covers it. A Shield is earned at every 7th day, at most 2.
- Each day pays `STREAK_DAY_COINS` (50 rising to 200 from day 7). Days 3, 7, 14, 30, 60, 100 pay `MILESTONES` extra (300 to 20,000 coins).
- **Flame bonus:** +5% of the match's coin reward per day of flame, at most +50% (day 10), paid as "Flame bonus" after each match.
- **Tiers** (name and colors of the fire): SPARK 1, BLAZE 3, WILDFIRE 7, FIRESTORM 14, SOULFIRE 30 (blue), SUPERNOVA 60 (violet-white). OUT is grey.
- States: **Lit** (played today), **Risk** (played yesterday, or missed days that shields cover: play today or it goes out), **Out**.
- Saved: `Progress.Streak.Days`, `Day` (UTC day number it last grew), `Best`, `Shields`. The field is `Days`, not `Count`: `Count` is a Scribe accessor method and a field of that name is unreachable (Scribe logs `API_NAME_COLLISION`).

### The look

- The nav row shows a flame chip next to GOALS with the day count; its ring glows in the tier color and turns solid while the flame is at risk.
- Back in the lobby with a bigger flame than last celebrated (`Progress.Seen.Streak`), a full-screen burst plays: the old count, a flare (the flame grows, a shockwave ring, a shower of embers), the new count, its tier ("NEW TIER: WILDFIRE" when it changed), the coins and the bonus, and how many days to the next tier. Side by side (760 x 330 design pixels), shrunk to fit a phone. Roblox's touch controls hide while it shows.
- The fire is drawn with UI frames: teardrop tongues (a circle and a 45 degree square) in three layers that flicker on `math.noise`, two glow circles, rising embers. One RenderStepped connection drives every flame on screen; hidden flames cost nothing; the nav chip updates 30 times a second.

### Daily Flame popup (2026-11-19)

`Client.Core.DailyFlame`, UI `Main.DailyFlame` (built in Studio). The first time a player is in the lobby on a new UTC day and their flame isn't lit today, a popup shows what one match today gets them:

- the flame (FlameFx) with its days and tier, or NOT LIT
- a title and line by state: KEEP YOUR FLAME BURNING ("Play 1 match today to reach day 5 and earn 150 coins"), LIGHT A NEW FLAME (went out; shows the best), LIGHT YOUR FLAME (never lit)
- a week of day tiles (days 1-7, 8-14, ...): done days checked on mint, TODAY in the flame's color with a breathing ring, coming days by weekday with their coins; milestone days show a gift with a gold ring
- the next tier (days to go, a bar in its color) and the match coin bonus on the day reached
- shields: how many, the day the next one comes, or that one saved the flame
- PLAY NOW (queues the picked mode, like PLAY) and LATER / X

It waits for the training offer, a menu or Celebrate's flame burst to close, then shows once a day: the client sends `Packets.Progress.Seen "Daily"` and the server saves its own day in `Progress.Seen.Daily`. It shrinks to fit a phone (design 680 x 392). Wording is kind on purpose: research on streak screens (Mobbin's study of 859 streak designs, Duolingo's streak posts, reward calendar conventions) found loss threats and countdowns push players away, while a visible next step, a week view and a featured milestone pull them back.

### The flame window: 8 PM to 12 AM, the player's own clock (2026-11-20)

The owner's rule: the flame runs on each player's time. Every evening a window opens at **8 PM** their time and closes at **12 AM**. One public match inside it grows the flame. A window that closes without one puts the flame out, unless a Shield covers it. Matches outside the window don't count for the flame (they still pay everything else).

- `Content.Progress.Window(now, tz)`: the window's number (the one that opened most recently; `Streak.Day` saves it), whether it's open, and seconds until it closes or the next one opens. `WINDOW_OPEN` 20:00, `WINDOW_LENGTH` 4 h.
- `FlameState(count, day, shields, now, tz)` / `FlameOf(streak, now)`: Lit (played this window), Risk (window open, not played), Wait (alive, between windows), Out.
- The player's clock: the client sends its UTC offset (`Progress.DeviceOffset`, rounded to 15 min) with `Packets.Progress.Zone`; the server checks it (-12 h to +14 h, multiple of 15) and saves `Streak.Tz`; it can change at most once in `TZ_CHANGE_DAYS` (7) days (`Streak.TzSet`), so a player can't hop zones to reopen a window.
- The Daily Flame popup shows once per window, only while it's open ("Play before 12 AM (3h 0m left)"); STREAK REWARDS still opens it any time. The GOALS flame card says "Done. Next at 8 PM", "Play before 12 AM: 2h 5m left", "Window opens in 6h 3m". The flame reminder notification is booked for the player's next 8 PM.
- Saves from before (UTC day numbers in `Streak.Day`) carry over: the numbers line up closely enough that a flame lit yesterday stays lit until tonight's window.

### Flame rewards: crates and skins (2026-11-19)

Every flame day pays its day coins (`STREAK_DAY_COINS`) plus, on milestone days, crates or a skin (`Content.Progress.MILESTONES`, read through `Progress.DayReward(day)`):

| Day | Extra |
|---|---|
| 3 | Cosmetic crate |
| 5 | 500 coins |
| 7 | a Glacier skin the player doesn't own |
| 10 | Afterburn crate |
| 14 | an Afterburn skin (luck 2) |
| 21 | 2 Glacier crates |
| 30 | a Glacier skin (luck 3) + 2000 coins |
| 60 | an Afterburn skin (luck 3) + 5000 coins |
| 100 | 3 Glacier crates + 10000 coins |

From day 30, every 7th day with no milestone gives a Cosmetic crate. Crates go to the crate inventory; a skin is given at once through `StoreGrants.OpenCrate` (if every skin of that crate is owned, its refund coins instead), in one `Data.Transaction` (`ProgressService` grantItems). The Daily Flame tiles show each day's biggest reward with the game's own icons (`Progress.RewardBadge`: coin, crate, skins); crate and skin days are ringed in gold, and the popup names the next one ("Day 3: CRATE"). The popup text was cut down: KEEP YOUR STREAK / START A NEW STREAK / START YOUR STREAK, "Play a match today: +75 coins".

### Flame easter egg (2026-11-19)

Every full-size flame (`Client.Core.FlameFx`: the Daily Flame popup, the flame burst, the GOALS card; not the small nav chip) can be played with:

- **Tap:** a puff (it jumps and bounces, a ring and embers), a fire whoosh (`FlameTap`) and a haptic click. Quick taps (within 0.55 s) build a run: each whoosh higher, the fifth a big flare (`FlameRelease`).
- **Drag** (finger or mouse): the tongues split apart and stretch toward the pointer, leaning into it, embers stream from the pointer, and it grows up to 1.6x over 1.6 s of holding, with crackles (`FlameCrackle`) and light haptic ticks while moving.
- **Let go:** it springs back with a small wobble and flares as big as it grew (`FlameRelease`, a stronger haptic).
- A controller can select the flame and press A for a tap. A flame that is out only sputters.

Haptics use `HapticEffect` (UIClick, UIHover, GameplayCollision) and play only when the last input was touch or a gamepad. Sounds are ProSoundEffects fire whooshes in `Content.Effects.Registry` (UI group, so the Interface volume controls them). `FlameFx.new(frame, { Playable = false })` turns it off for a flame.

## Weekly Goal

The card shows the points and each tier's coin reward on the track (2026-11-18: trimmed; the point values per action are listed here, not on the card).


Points: match +20, win +15, daily quest +25, all dailies +40, weekly quest +60, flame day +15. Tiers at 100 / 250 / 450 / 700 / 1000 points pay 300 / 600 / 1,000 / 1,600 / 3,000 coins at once. Resets with the weekly quests (Tuesday 00:00 UTC). Saved: `Progress.Weekly.Week`, `Points`, `Paid`.

## Quests without the battle pass

Quests used to run only while the battle pass was on, and the pass is still off, so no daily or weekly goals were live. They now always run; while the pass is off a quest pays `XP * Quests.COIN_SHARE` (0.25) coins instead of pass XP. Either way a quest also gives account XP (`QuestShare` 0.25 of its XP) and Weekly Goal points. They show on the GOALS tab.

## Level

Account XP: match 100, win +100, kill +10, flame day +50, quests 25% of their XP. Level n to n+1 costs 500 + 100 x (n - 1) XP (at most 3,000). Every level pays 150 coins; every 5th level 500 more. The `Level` player attribute holds it (the Ranked gate reads it). Saved: `Progress.XP` (total).

## Ranked

- A new queue mode `Ranked` (5 v 5, smallest 1 v 1, 90 s wait, players only, no bot fill) in the SIEGE category. Opens at level 5 (`MinLevel`): every party member on the lobby server needs it, and a party with bots can't queue.
- Elo: each player against the other side's average rating, K 48 for the first 5 (placement) matches, then 24. Starts at 1000. Ranks: IRON, BRONZE 900, SILVER 1100, GOLD 1300, PLATINUM 1500, DIAMOND 1700, ELITE 1900. A new battle pass season pulls ratings halfway back to 1000.
- Saved: `Progress.Ranked.Season`, `Rating`, `Peak`, `Played`, `Wins`, `Last` (last change).
- There is no skill bracket in matchmaking yet (the queue is too small); the rating only moves.

## Career and the PROFILE tab

Saved per player: `Progress.Career.Matches`, `Kills`, `Deaths`, `Damage`, `Built` (public matches). PROFILE shows level, XP to the next level, the rank card, eight stat tiles (matches, wins, win rate, kills, K/D, damage, boards built, best flame), INVITE FRIENDS and FAVORITE THE GAME. (The other developer's Career panel in `Client.Core.LobbyHubUI` stays hidden.)

## Leaderboards

THIS WEEK (weekly points, a store per week), FLAME (days now), LEVEL (total XP), RANKED (rating this season, once placed). Written when a player joins, after a score changes (at most every 120 s) and when they leave; read through `Packets.Progress.Board`, top 50, cached 90 s per server, names from `UserService`. Zero scores are hidden. Studio tests with `ScribeNoSave` write nothing.

## Bot fill

`5v5` (`BotFill = 30`) and `1v1` (`BotFill = 20`): once the mode's oldest ticket has waited that many seconds with no match, a match forms with whoever is queued (one player is enough) and Siege bots (`Content.Games.SiegeBots`, "BOT Atlas"...) fill every empty spot on both sides. Every public match of those modes is topped up the same way. Private matches never get bots. In Studio the workspace attribute `NoBotFill = true` turns it off. Bots earn nothing; the players' rewards, quests and flame count as usual.

## Badges, invites, favorites, reminders

- **Badges:** `Content.Progress.BADGES` (Welcome, FirstMatch, FirstWin, Flame3/7/30, Level10/25/50, RankedPlaced, WeeklyDone). Ids are 0 until made on the Creator Hub; 0 is skipped.
- **Invite:** INVITE FRIENDS on PROFILE and in the Party menu's INVITE side opens Roblox's invite (`SocialService:PromptGameInvite`).
- **Favorite:** shown once after 2 finished matches (`AvatarEditorService:PromptSetFavorite`), and as a button on PROFILE until used.
- **Notifications opt-in:** after a flame burst from day 2, Roblox's opt-in (`ExperienceNotificationService:PromptOptIn`), at most once a week from the game (Roblox itself limits it to once per 30 days and 13+).
- **Flame reminders:** when the flame grows, a reminder is booked for 16:00 UTC the next day (MemoryStore SortedMap `FlameReminders_v1`). Growing it again re-books it, so it only reaches players who haven't played that day. Lobby servers send the due ones once a minute (claimed so only one server sends each).

### To switch reminders on (Creator Hub, by the owner)

1. Creator Hub > the experience > Engagement > Notifications: create a notification string, for example `Your {count}-day flame goes out at midnight UTC. Keep it burning!` Put its id in `Content.Progress.NOTIFICATIONS.FlameReminder`.
2. Create an Open Cloud API key with the `user.user-notification:write` permission for this experience, and add it as an experience secret named `NotifyKey` (Creator Hub > the experience > Secrets).
3. HTTP requests are already on (`HttpService.HttpEnabled`).

Until then booking runs and nothing is sent.

### To switch badges on

Create the badges on the Creator Hub (the first ones each day are free) and put their ids in `Content.Progress.BADGES`.

## Tested (2026-11-18, Studio playtests, one player, `ScribeNoSave`)

| Test | Result |
| --- | --- |
| Lobby | GOALS word and the grey flame chip in the nav; no errors |
| Seeded 13-day flame, Seen 12 | The burst played (WILDFIRE red, embers); GOALS tab shows the flame card, weekly track at 320 pts with tiers 1-2 lit, today's quests paying coins (+100, +87, +125) |
| PROFILE | Level 8, XP bar, UNRANKED with placements 0/5, career tiles (K/D 1.40 from 42/30) |
| LEADERBOARDS | Reads and writes the stores; zeros hidden ("Nobody on this board yet") |
| Queue 1v1 alone | Matched against BOT Atlas / BOT Rook (bot fill) |
| Won it with the flame last grown yesterday (6 days) | Flame 7 (WILDFIRE, a shield), +250 XP, +50 weekly points paying tier 2, coins +2,740 = win + day-7 coins + milestone + 35% flame bonus + tier 2 |
| Back in the lobby | The burst (6 to 7, NEW TIER: WILDFIRE, Shield earned!), then Roblox's notification opt-in |
| Ranked at level 3 / 8 | Refused ("opens at level 5") / queued; leaving works |

Not tested: a Ranked match between two real players (the rating change), reminders being sent (needs the Creator Hub setup), badges (no ids yet), the favorite prompt on a live server, a real phone.
