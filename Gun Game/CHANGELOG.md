# Changelog

Recent implementation notes are kept here. Older dated entries are grouped into [searchable archives](#archives) so the current page stays quick to scan.

!!! note "Note"

    Entries record what was changed and checked at the time. They are not a guarantee of current behavior; use the relevant system guide and its verification notes.

## Archives

| Dates | Archive |
| --- | --- |
| 2026-11-15 to 2026-11-17 | [Nov 15–17](CHANGELOG_2026-11-15_to_17.md) |
| 2026-11-12 to 2026-11-14 | [Nov 12–14](CHANGELOG_2026-11-12_to_14.md) |
| 2026-11-09 to 2026-11-11 | [Nov 9–11](CHANGELOG_2026-11-09_to_11.md) |
| 2026-11-07 to 2026-11-08 | [Nov 7–8](CHANGELOG_2026-11-07_to_08.md) |

## Recent changes

## 2026-11-25: Shorter Siege rounds

- The owner wants matches to feel faster for casual players. Siege phase times in `Content.Games.Siege`: Selection 30 to **40 s**, Prep 40 to **30 s**, Reveal 15 to **10 s** (the docs already said 10 s; the code had 15), Action 5:00 to **3:00** (`ACTION_TIME` 180), so a player who dies early waits less.
- Applies to every Siege match (1v1, 5v5, Ranked, Private). Recruit Training keeps its own times (`Content.Games.Tutorial`).
- Clear House used Siege's Selection time; it now has its own `Content.Games.ClearHouse.SELECTION_TIME` (30 s, unchanged), read by both `setPhase("Selection", …)` calls in `SiegeService`.
- Checked in Edit mode: the three modules compile, and the values read back as 40 / 10 / 30 / 180 (Clear House 30 / 480). **Not playtested** (by request).

## 2026-11-25: Code map page

- New [Code map](CODE_MAP.md): every server, shared, client and content module by area, the lobby/match server split, and how a shot, an ability, a round, a death and a purchase cross the modules.
- Built from these docs, not a live Studio session; check it against the place next time Studio is connected.

## 2026-11-24: Bigger gun animations, the hand pumps the shotgun, the Sawed-Off breaks open

- The owner: the pistol slide was hard to see; "the pump shotgun had no animation. The lever in the back also has no animation. Also move the hand on top to prepare for the next shot and do an animation showing you're pumping it", plus the Sawed-Off break-open.
- **Pistol.** The slide travels further (0.42 studs) and slower (back in 0.05 s, a beat, home in 0.2 s); the hammer swings 40 degrees. SiegePistol too.
- **Pump shotgun.** The pump did move, but the first-person left hand sat on it and covered it. Now the left hand rides the pump (first and third person): 0.2 s after each shot it pulls the pump back 0.5 studs, holds, and pushes it forward, with the gun canting 8 degrees toward the pull. The exposed hammer behind the receiver (the "lever in the back", named `RearSight` on this model) falls on the shot and is cocked again by the pump. SiegeShotgun's pump the same.
- **Sawed-Off.** On reload the top lever swings and the barrels tip open on their hinge, then close.
- `Content.Guns.Mechanics` now describes each mechanism by Motion (Slide, Tilt, Turn, Spin) and Profile (Kick, Rack, Cock, Open); `GunMechanics.Reload` added; the Viewmodel and ThirdPersonGuns move the left hand by the mechanics' `Hand`. Details in ADDING_GUNS.md.

Checked in a playtest (no saving): first person, one pump-shotgun shot moved the pump its full travel and back, the left hand with it, and the hammer 32 degrees. A recording of two shots and a reload shows the pistol slide back, the pump racking and the Sawed-Off opening and closing. No errors. Not checked: the left hand on video (the lobby draws the first-person view wrong), third person on video, a real match, other players.

## 2026-11-24: Skin trim stays on the gun; the Revolver's turn shows

- The owner: "Some skins still go off the edge or have floating parts like on the pistol and smg. The revolver does not have the spinning cylinder or it was not clear."
- **Skins.** Every piece of skin trim on a firearm now sits flat on a real part of that gun and inside its edges (details in SKINS.md). The SMG's own trim had never been moved onto its split model; now it is. Trim no longer goes on parts that move or hide (magazine, cylinder, trigger, hammer, pump), and the Revolver's side plaque, which covered the cylinder, is gone.
- **Revolver.** The cylinder did turn, but it is nearly round (its surface is 0.147 to 0.153 studs from the middle all the way around), so a turn looked like nothing. Six dark flutes now run along it (made on the client, welded to it) and the turn is slower with a small overshoot (0.3 s, 15% of a chamber), so each shot clearly clicks to the next chamber.

Checked: lineups in Studio (side and angled) of every Pistol and SMG skin and one skin on each other gun; a recording in a playtest of five revolver shots shows the flutes moving one chamber each time with the hammer cocking. No errors. Not checked: the first-person view in a real match (in the lobby the first-person gun draws small and far, and the training popup covers it). Not saved or published.

## 2026-11-24: Guns move their parts when they fire

- The owner: "Can you give the guns animations make the pistol have the slide back when shot on the top part. Give the revolver a barrel spin to the next slot to make it cool."
- **Pistol slide.** On each shot the Pistol's slide (with its sights, ribs and any skin trim on it) snaps back 0.32 studs and returns in about 0.12 s, so the barrel shows; the hammer flicks. At 0 rounds the slide stays locked back until the gun is loaded. The SiegePistol does the same.
- **Revolver cylinder.** Each shot turns the cylinder one chamber (60 degrees, its six facets line up again) over 0.14 s, and the hammer falls.
- **Also:** the PumpShotgun and SiegeShotgun rack their pump after each shot, and every gun's trigger pulls.
- New: `Content.Guns.Mechanics` (what moves, by model) and `Client.Guns.GunMechanics` (plays it), used by `Client.Guns.Viewmodel` and `Client.Guns.ThirdPersonGuns`. Details in ADDING_GUNS.md.

Checked in a playtest with no saving: three pistol shots in first person moved the slide its full travel and back to rest each time, with the 18 trim parts of the Obsidian skin riding on it; at 0 Ammo the slide sat locked back. Three revolver shots turned the cylinder 60, 120 and 180 degrees with no drift. In third person (your own body from the side) one shot turned the Revolver's cylinder 60 degrees. No errors. Not checked: how it looks to the eye in motion (the lobby's training popup covered the view; the poses were checked in Edit instead), the pump in play, and other players on a live server. Not saved or published.

## 2026-11-24: Assault Rifle replaces the Rifle, new Pistol model, skins fit every model

- The owner: "Make the AssaultRifle split", "make the skins actually work on all the models and attach properly", "give the pistol a new model", "replace the old Rifle with the Assault Rifle model and rename all references to rifle to Assault Rifle". The owner chose a full Id rename, the Assault Rifle model for the Burst Rifle too, and a pistol from the gun pack.
- **Assault Rifle.** The one-piece mesh is split into 18 named pieces with a real `Magazine` (asset 72081744528566). The gun Id `Rifle` ("Ak-47") is gone; `AssaultRifle` ("Assault Rifle") takes its place everywhere a gun Id is named, with the Assault Rifle definition's stats (15 damage, 550 rounds a minute, was 12 and 600). The Burst Rifle uses the new model. Data migration 3 moves the equipped `RifleSkin` to `AssaultRifleSkin`. Skin and store Ids are unchanged; rifle skin names now say "Assault Rifle". Details in ADDING_GUNS.md.
- **Pistol.** New model from the gun pack (`Pistol_3`), split into 19 pieces (asset 124198947340469), placed on the SiegePistol's Handle and scale.
- **Skins.** `Skins.Apply` fits a family's trim to each model's own parts (grip to grip, body side to body side, never longer than the part), colors split pieces by their nearest named part (Upper and Lower like Body, Grip like Handle, then the old one-piece `default`), and applies skin sizes only to the model they were drawn for. The SiegeSMG's receiver pieces were renamed (`Body` upper, `Lower` lower). The `Tactical_Bullpup_1` model had been renamed `Tactical_Bullpup_` (its definition could not find it); the name is back. Store cards now show a gun as words ("Epic · Assault Rifle"). Details in SKINS.md.

Checked in Studio: the split Assault Rifle matches the one-piece mesh exactly, and the new Pistol's muzzle and sights line up. Twelve guns compared with five skin sets before and after the fix. In a playtest with no saving: no warnings or errors, the migration moved the owner's Glacier skin to `AssaultRifleSkin`, both guns were given and equipped, first person wore their skins (Glacier on the Assault Rifle, Obsidian on the Pistol), and reloading the Assault Rifle took its magazine out in the hand and refilled 3 to 30. Not checked: shooting, third person, the Burst Rifle, aiming with the new Pistol's sights, and a live server. The Robux product is still named "Obsidian Rifle Skin" on the website. Not saved or published.

## 2026-11-22: One-piece gun meshes split into parts

- The owner: PumpShotgun, Revolver, SMG, SawedOffShotgun, SiegeCarbine, SiegePistol, SiegeSMG, SiegeShotgun and Tactical_Bullpup_1 were one full mesh each, hard to animate. Each is now made of the separate pieces its mesh was built from (177 parts in all), placed exactly where they were and welded to the Handle, with named key parts (Magazine, Barrel, Body, Grip, Trigger, Pump, Slide, Cylinder...). Nine Model assets uploaded to the group. Originals backed up in `ServerStorage.GunModelsBackup_20261122`. Details in ADDING_GUNS.md.

Checked in Studio: all nine side by side with their originals (identical shapes; the Magazine is the real magazine on the four guns that have one); skins apply on the new models with their details (PumpShotgun, Revolver, SawedOff, SiegeCarbine, SMG). Reload checked in a playtest on the SiegeCarbine (first person): its Magazine hides and the left hand carries a copy out and back, and ammo refills. The SMG, SiegeSMG and Bullpup have a visible Magazine the same way; the shotguns, Revolver and SiegePistol have none and keep the hand-only reload. Not checked: inspect, and the other guns in play. Not saved or published.


## 2026-11-20: Card entrance on the Inventory's Classes tab

- The Inventory opens on CLASSES, whose class tiles live in their own panel (`Inventory.ClassView.Cards`), so v1051's entrance (armed on the Skins and Crates page) missed them. The tiles are armed too now: on opening, on tab changes and on filters, the 19 class tiles come in one after another.

Checked in Studio: opening the Inventory staggers the class tiles (small with their sweep, in order). Not seen moving (Studio draws no frames). Not published.


## 2026-11-20: Card entrance in the Party menu

- The Party menu's five member slots come in one after another each time it opens (`CardIntro.Replay`, for rows made once and reused), and the invite list's rows come in too (`CardIntro.Arm`). The Shop already had it (v1051: opening and each section).

Checked in Studio: opening Party staggers the five slots (each starts small and tilted with its sweep); the Shop's crate cards do the same. Not seen moving: Studio's view still draws no frames (tweens paused). Not published.


## 2026-11-20: Card entrance animation

- New `Client.Core.CardIntro`: when a menu opens or its tab changes, its cards come in one after another (45 ms apart, at most 0.55 s): each pops up from 72% with a 5 degree tilt (Back easing, 0.42 s), Store and Inventory cards also rise 34 px into place, and a light sweep crosses each card once. Used by the Game Modes panel (both pages), the Store (open and each section), the Inventory (open, tabs, filters) and GOALS (quests and leaderboard rows). Not on data redraws (a purchase doesn't replay it). Roblox's Reduced Motion setting turns it off.

Checked in Studio: every menu arms it, the cards start small and tilted and come in staggered with their sweep, no errors. Not seen moving: Studio's view stopped drawing frames during the test (RenderStepped 0, tweens paused), so the motion itself is unverified. Not published.


## 2026-11-20: Flame reminder switched on

- The owner made the notification string on the Creator Hub; its id is in `Content.Progress.NOTIFICATIONS.FlameReminder`. With the `NotifyKey` secret in place, live servers send the 8 PM reminder. Not checked: a reminder actually arriving (needs the live game, an opted-in account, and the secret). Not published.


## 2026-11-20: Flame on the player's clock, 8 PM to 12 AM

- The daily flame runs on each player's own time: a window opens at 8 PM and closes at 12 AM; one match in it keeps the streak, a missed window resets it (shields still cover one). The device sends its time zone; the server checks it and lets it change at most once a week. Popup, GOALS card and reminders follow the window. Details in PROGRESSION.md.

Checked in Studio: the rule at 8:00 PM, 11:59 PM, 12:00 AM, a day later, with and without a shield (all as specified); the owner's save got Tz -480 and shows "Done. Next at 8 PM" with no popup in the morning; with the save moved to 9 PM the popup showed "Play before 12 AM (3h 0m left)" and today's tile on Friday. The save was put back (Tz -480, Day 20776, Seen.Daily 0). Not checked: a real match growing the flame inside a window. Not published.


## 2026-11-19: Gold win-streak flame, Training in Game Modes, streak rewards view

- **Win streak = gold flame:** the tag above a player's head (StatsService's StreakTag, from 2 wins in a row) now shows a small live gold flame (`Client.Hud.StreakTags`, FlameFx with `Content.Progress.WIN_FLAME`) instead of the flat image, for every player's tag; the lobby leaderboard's STREAK column shows the same gold flame with the count.
- **TRAINING is a card in the Game Modes panel** (last on the first page: 1V1 VS BOT, FREE CRATE / OPEN CRATE ribbon until earned and opened). The lobby bar's TRAINING tile is gone (SQUAD takes the row).
- **The training invite** shows only to a player who never finished or skipped it and has played no match of any mode (Career.Matches + Wins + Losses = 0).
- **STREAK REWARDS** button on the GOALS flame card opens the Daily Flame panel any time to see the week's rewards (`DailyFlame.View`: does not use up the once-a-day popup; on a day already played it says STREAK REWARDS, "Done today. Tomorrow: +...", and the next tile says NEXT).

Checked in Studio with screenshots: the Game Modes page with TRAINING; a gold flame on a real streak tag (copied to the screen, captures don't show billboards); STREAK REWARDS from GOALS opens the panel and leaves Seen.Daily at 0. The owner's Seen.Daily was found marked by a test again and reset to 0. Not checked: the leaderboard column on screen, the invite with a brand-new account. Not published.


## 2026-11-19: Daily Flame tiles drawn like the game's items

- The owner: the daily rewards should use the icons already in the game and show what the player can get. Each day tile now draws its reward the way the Store and Inventory do: coins as the wallet's gold coin picture, a crate as the Inventory's crate card (its rarity's colors, the crate icon), a skin as the 3D gun of that crate's rarest gun skin (ItemDetails.GunPreview; knives skipped, they read as a line at that size), e.g. the Glacier LMG on day 7.
- Studio tests opening the popup marked the owner's real save as seen for today (ScribeNoSave didn't stop that); reset to 0 again.

Checked in Studio with a screenshot: coin tiles, the day 3 crate card, the day 7 Glacier LMG. Not published.


## 2026-11-19: Streak crates and skins, PLAY green and stop icon, HOME button

- Flame milestones now give crates and skins (day 3 crate, day 7 skin, day 10 crate, day 14 skin, ...; table in PROGRESSION.md). The Daily Flame tiles use the game's coin, crate and skin icons, gold rings on crate and skin days, and much shorter text.
- PLAY, PLAY NOW and the PLAY WITH PARTY edge use a new green (#3AD660) instead of the mint accent. While searching, PLAY's round icon is a stop square.
- HOME in the lobby nav is a button now (it was only a label): it closes any open menu.
- The earlier Studio test had marked the owner's Daily Flame as seen for today in the real save; reset to 0 so it shows live.

Checked in Studio: the popup with the real save (KEEP YOUR STREAK, "+75 coins", crate on day 3, skin on day 7, "Day 3: CRATE"), all text fits; PLAY green; searching shows CANCEL with the stop square, cancelling brings the play arrow back; HOME clicked with the Store open closed it. Not checked: a crate or skin actually granted on a milestone day (needs a public match on that day). Not published.


## 2026-11-19: Flame easter egg

- The streak flame can be played with: tap for a puff with a fire whoosh and a haptic click (five quick taps flare); drag a finger or the mouse to split the flame apart and stretch it toward you as it grows bigger, with crackles and haptic ticks; let go and it springs back and flares. Haptics on phones and controllers only. Details in PROGRESSION.md.

Checked in Studio (driving the flame's update by hand, because Studio's viewport wasn't drawing frames): five taps built a run and flared; a 1.6 s drag up-right grew the flame from 65 to 248 px wide and 1.6x tall; let go, it overshot a little and settled in about 1.5 s; the three sounds load. Not checked: a real press with the mouse or a finger, haptics on a device, how it looks (no screenshot). Not published.


## 2026-11-19: Daily Flame popup

- New popup the first time a player is in the lobby on a new day and their flame isn't lit yet: the flame and its days, what one match today gets ("Play 1 match today to reach day 5 and earn 150 coins"), a week of day tiles with TODAY lit and milestone gifts, the days to the next tier with a bar, the match coin bonus, shields, and PLAY NOW / LATER. Once a day (new saved field `Progress.Seen.Daily`, set by the server). Details in PROGRESSION.md.
- `Client.Core.Matchmaking.Queued()` added (PLAY NOW never cancels a search).

Checked in Studio: a 4-day flame from yesterday showed KEEP YOUR FLAME BURNING, tiles DAY 1-4 done, TODAY on day 5 (+150), gifts on day 3 and 7, "3 DAYS TO WILDFIRE"; PLAY NOW closed it and started a search; it didn't come back that day; a flame out showed LIGHT A NEW FLAME with the best. All text fits (measured). Not checked: a picture (Studio's screen capture timed out), a real phone. Not published.


## 2026-11-19: Training: coach off the hotbar, Tip, cameras tip

- **Phones:** the coach line sat on the hotbar (the owner's screenshot). On a small screen outside a feed it is now a left column under the top bar (12, 56), 45% wide, left aligned; the goal card stays hidden on phones.
- **"Bonus" is now "Tip"** in every coach line and the tag (`TEXT.Bonus = "TIP"`).
- **Cameras tip:** 30 s into the defend Action phase, if the player hasn't opened the cameras, the coach says "Tip: check the cameras to find the attacker"; 2 s later the 5 key shows and the phone camera button glows. Opening the feed ends the tip. Beats can now have `After` (seconds into the phase) and their own `HintAfter`; the coach rechecks once a second.
- **Banner:** a long title ("DEFUSER PLANTED ON BOMB B") was cut off on a phone; the title now grows to more lines.

Checked in Studio: defend Action showed "Guard the bombs..." at 3 s and the cameras tip with the 5 key at 32 s; pressing 5 opened the feed and the line went back. The banner wrapped to three lines on a narrow window. Not checked on a real phone. Not published.


## 2026-11-19: Training: 3D guide arrows, shorter rings

- **Physical arrows** (the owner: use physical arrows instead of on-screen ones when pointing to physical objects): the guide is now two 3D arrows made of neon mint parts on the client only (in the camera; no collisions, queries or touches): one over the target pointing down, bobbing and turning, seen through walls (a Highlight, AlwaysOnTop); and, when the target is off screen, a smaller one floating just above the crosshair, turned flat to the view so it points left, right, up or down (a target behind turns it to the nearer side). The on-screen edge arrow and the billboard are gone.
- **Rings** around HUD parts and touch buttons glow for 5 s once they come in (`RING_TIME`), then fade (the owner: the bomb rings stayed too long).

Checked in Studio: a full training run (both rounds) with a watcher: rings shown 4.9 s, no arrow outside Prep/Action, one marker and one pointer at the end; screenshots of the pointer in the drone feed (right, toward the site) and on foot (left, toward a boarded door); the arrow shape checked from two angles in Edit. Not published.


## 2026-11-19: Training: stuck guide arrow

- The owner: an arrow got stuck on screen (v1030). The guide's floating marker (a BillboardGui straight in PlayerGui) was removed on a respawn (ResetOnSpawn), and `guideParts` then made all three parts again, leaving the old screen-edge arrow visible and no longer updated (and an attachment more each round). Now the billboard has ResetOnSpawn off, only a missing part is made again, the arrows hide whenever the coach's loop stops or a guide search errors (pcall), and ring arrows show only during a live beat.

Checked in Studio: a full training run (both rounds, forced round ends) with a watcher on the client: no arrow outside Prep/Action or without the coach line, one edge arrow and one anchor at the end (the same run before the fix showed the arrow stuck through RoundEnd, round 2's Reveal and End). Not published.


## 2026-11-19: Training: quicker, less told, guide arrows

- Shorter training timers: briefing 5 s, prep 30 / 40 s, attack and defend 2 minutes, results 5 and 10 s.
- The coach names only the goal; keys and glowing buttons come only if the player is stuck (6 to 15 s).
- Arrows lead the way: over the target with its distance, or at the screen's edge when it is off screen (the site, the nearest boarded door, the bombs, open doorways, the bot).
- Defending: "Take down the attacker to win the round faster".

Details in TUTORIAL.md. Not published.


## 2026-11-18: Training coach

- Recruit Training walks the player through each step: one short line in the middle, the exact keys as chips (gold HOLD for held keys), the real buttons glowing on a phone, the bomb chips glowing when the step is about them, a counter, a praise word when done, then the next line. New `Client.Hud.TutorialCoach`, beats in `Content.Games.Tutorial` STEPS[].Coach.
- SKIP TRAINING (tap twice) leaves training for the lobby (no crate).
- Fixed on the way: a feed closing just before Action's state put the Prep beat back.

Details in TUTORIAL.md. Not published.


## 2026-11-18: Phone screenshots pass: overlaps, cut-off text, contrast, bomb B, camera scan

From the owner's phone screenshots after v1018:

- **Icons on text** (`Content.Icons`): a Lead/Trail icon was sized to the font's line height (~1.5 em for Titillium) but the spaces kept for it are sized in ems, so the star, timer and check icons covered the first letter ("SCAN THE DEFENDER", "NEW IN", "OWNED"). The icon is now never wider than its spaces (`reservedWidth`).
- **Training popups** (`Client.Hud.Tutorial`): the "goal done" popup (DEFUSE A BOMB, FORTIFY, HOLD THE LINE) sits at the left under the goal panel instead of the middle, where it covered the bomb bar, the drone's ENEMY SCANNED and the match result's cards. In training's Reveal the player card hides under the briefing (the briefing names the side and class; it covered half the card on a phone).
- **Reveal cards** (`Client.Core.SiegeSelect`): the line under a player shows only the pick ("MAIN FLOOR"), not "SITE VOTE  ·  MAIN FLOOR", which was cut off.
- **Drone feed on a phone** (`Client.Core.UI` `layoutFeed`): the keyboard's "HOP" ready label by the boost bar hides (the HOP button says it).
- **Match result** (`Client.Hud.SiegeHud`): one color per stat everywhere (KILLS red, DEATHS violet, DAMAGE gold, BUILT mint) in the headers (now full words, wider columns: player 34%, 15/17/17/17), every row, the team totals and the MVP cards. The count-up always ends on the real number (a redraw could leave team totals at 0).
- **PROFILE**: the level card is tighter so "Next level" stays inside it on a phone; MATCHES is never below wins + losses (matches before the career counter); "1 day".
- **Item page** (`Client.Core.ItemDetails`): fully opaque (the page behind showed through and looked like part of it). Facts without a picture (a skin's Rarity, Weapon, Owned, From) show a caption and the value under it, full width, two lines if needed, instead of the bundle row layout with an empty picture slot and a 50 px value ("From  Afterb").
- **Class panel on a phone** (`Client.Core.ClassPanel`): compact mode keeps the ability (name and description, moved up under the class name) and hides only stats, rule, kit and status. It showed nothing but the name.
- **Bomb B blue** on the bomb bar (`SiegeHud`, `Main.SiegeHUD.Bombs.BombB.Letter`), like its markers: red A, blue B.
- **Camera scan** (`Systems.Cameras.CameraService`): scanned only enemy players, so a camera could never scan a bot (training, bot-filled matches). It now also scans NPC characters with a Team (workspace and one folder down, `workspace.Enemies`), never cameras or drones.
- **Readable over the world** (new `Client.Core.Readability`, ClientOnly): light text with no panel behind it gets a thin dark outline; Roblox's Background Transparency accessibility setting (`GuiService.PreferredTransparency`) is applied to see-through panels.

Checked in Studio playtests (a 919 x 889 window, the short-screen layout forced on for the menus): PROFILE, the Inventory class panel, the skin page, a 1v1 against a bot (BOT Mako is in workspace.Enemies with a Team and a Head), the colored match result. Not checked: a real phone, the compact class panel at phone height, the training popups and briefing in a training run, a camera scan by hand. Not published.


## 2026-11-18: Game modes: BACK and EXIT together

- `Main.Modes.Buttons` (bottom left, a horizontal list): **BACK** (to the categories, only inside a category) and **EXIT** (closes the screen; was labelled BACK, which was confusing) side by side. On the category list only EXIT shows, in the same place. `Client.Core.ModeMenu` finds them under `Buttons`.
- The title-row "ALL MODES" button from earlier today is now this BACK.

Checked in a Studio playtest: SIEGE shows BACK and EXIT together; BACK returns to SELECT A MODE with EXIT in the same spot. Not published.


## 2026-11-18: Phone menus: nav stays, no overlaps

From the owner's phone screenshots after v1016:

- **HOME, SHOP, INVENTORY, GOALS stay visible over menus on a phone,** to switch menus quickly. `Client.Core.Store` no longer hides the nav row (and the settings gear) while a menu is open on a short screen; `Client.Core.UI` keeps `SHORT_NAV_ROOM` (40 px) free above fitted menus there, so they start below it.
- **Coins box and X:** on a short screen the folded header also hides the menu's own coin box (the nav row shows the coins). In the tab row it sat on the Inventory's search box and crowded the close button.
- **Game modes screen:** the category BACK button (now "ALL MODES") hung left of the panel and was cut off on a phone; it now sits at the right end of the title row. The screen starts 56 px down (`Main.Modes`), below the nav row. The description box is as wide as the cards; Ranked's text is shorter ("Win to climb from Iron to Elite. Players only, level 5+.").

Checked in Studio with the short-screen layout forced on (the phone emulator could not be driven from here): the nav row sits above the Inventory and the mode screen, no coin box in the menu, X and search apart, ALL MODES visible. Not checked on a real phone.


## 2026-11-18: Smaller PLAY card, no grey tint, renamed tiers

- **PLAY card (`Client.Core.Matchmaking` `layoutBar`):** about 120 design pixels tall instead of 300. GAME MODE and PLAY now share the bottom row (GAME MODE 42% of the width), TRAINING and SQUAD are 48 high, PLAY WITH PARTY 44. It grows at most 1.15x on big screens (was 1.25x). On the 1852 x 840 Studio window: 391 x 198 pixels with PLAY WITH PARTY (was about 420 x 350). The GAME MODE tile's labels were resized for the narrower tile (`Main.Lobby.ModeButton` Label and Value: width minus 52).
- **No grey tint:** the dark bands behind the nav bar and the PLAY card (`Main.NavShade`, `Main.PlayShade`) stay hidden, and a menu no longer darkens and greys the world (`Client.Core.MenuAmbience` grade set to zero; the blur stays).
- **Renamed:** flame tiers INFERNO is now WILDFIRE and HELLFIRE is now FIRESTORM (`Content.Progress`); the knife skin shown as "Hellfire" is now "Emberfang" (its Id stays `HellfireKnife`, since owned skins and crate odds use the Id).

Checked in a Studio playtest (desktop window). Not checked on a phone. Not published.


## 2026-11-18: Menu title, Store text and Goals text fixes

- **Title over the tabs (every menu):** on a short screen a menu folds its title row into its tab row (`Client.Core.UI` `compactHeader`). Unfolding moved back only the parts still at 60 px or lower, so after a screen grew (a window short while loading, then resized) the tabs stayed on the title row and the title showed over them ("SHOP" over FEATURED, "GOALS" over GOALS). It now saves each part's place when folding and puts it back exactly.
- **Unreadable Store text:** dark text stayed on dark fills: the OWNED bar on the detail page and the Store cards, and greyed prices (the Robux price beside OWNED). `ItemDetails` (`textOn`) and `Store.priceButton` now set the text color with the fill: Ink on bright fills, light (muted when it can't be bought) on dark ones, mint OWNED on its dark green.
- **Less text on GOALS:** the flame card shows the days, the tier, one short line ("Done for today", "Play within 5h 12m!", "Play a match to light it"), the bonus with shields, and the days to the next tier (hidden while the flame is out). The Weekly Goal card shows the points and the coin reward of each tier (the points line under each tier and the long points hint are gone).

Checked in a Studio playtest (desktop window): GOALS and SHOP titles sit above their tabs, the owned Obsidian Pack shows a mint OWNED and a readable R$ 149. Not published.


## 2026-11-18: Retention pass

- **Quests are live** without the battle pass: they pay coins while the pass is off, on a new GOALS menu.
- **Flame streak:** play a match a day to grow it; tiers SPARK to SUPERNOVA, shields, daily coins, milestones and up to +50% match coins. A flame chip in the nav and a full-screen flame burst on return.
- **Weekly Goal:** points from matches, wins, quests and flame days; five tiers paying coins; resets Tuesdays.
- **Account level**, **Ranked** mode (from level 5, Elo, Iron to Elite), **career stats**, **leaderboards** (week, flame, level, ranked).
- **Bot fill:** 5v5 and 1v1 fill empty spots with bots after 30 / 20 s, so one player always gets a match.
- **Invite friends** (Party menu, PROFILE), a one-time **favorite** prompt, Roblox's **notification opt-in**, and flame **reminders** (need Creator Hub setup), **badges** (need ids).

Details in PROGRESSION.md. Not published.


## 2026-11-18: UI performance pass

- Inventory Skins tab opens in 23 ms instead of about 145 ms: gun previews fill only near the screen (new `Client.Core.LazyPreviews`) and cards past the first 12 build over the next frames.
- Inventory and Store keep their drawn page: reopening with nothing changed costs 0.2 ms instead of a full redraw. The Inventory no longer draws twice per open.
- Store: one redraw per burst of data changes, glow parts cached, deal timer text set once a second.
- Fixed: the Inventory's Classes tab errored on every draw (its owned count).

Details in PERFORMANCE.md. Not published.


## 2026-11-18: Performance pass

- Profiled the client and server with Roblox's script profiler in the lobby and a 5v5 bot match. The server was already lean (about 0.3 ms of game scripts a frame); the client and its downloads were not.
- The gun range moved from `Teams` (replicated: 20,807 instances and 72 client scripts for every player) to `ServerStorage.GunShowcase`.
- Rainbow skins recolour only visible parts, 30 times a second. Third-person arm posing caches joint offsets per frame and no longer errors on a joint without attachments. The reinforce prompt searches 10 times a second. The Leo warning and the Siege top-bar clock stop writing when nothing changes.
- Client scripts per frame: lobby 0.78 to 0.35 ms, match 1.37 to 1.00 ms.

See PERFORMANCE.md. Not published.


## 2026-11-18: Exploit and lag pass

- The network library caps packets a player a server frame (96; a request with a reply counts 8). A crafted flood had frozen the server for 553 ms; now the worst frame is 23 ms.
- Unreliable packets: 30 a second per player, malformed ones dropped.
- Movement: teleports, CFrame speed hacks, flying and hovering are put back (position and hover checks, `MoveCorrections`). Drones get the same position check (`DroneCorrections`).
- Gun fire, gun bash and throws refuse infinite vectors; opening a crate re-checks the count inside the transaction; the reinforce hold is limited to 5 starts a second; a per-player table in Dead Call is cleared on leave; a debug print of the bot behaviour tree is gone.
- Checked in Studio by attacking from a client script before and after, and in a 5v5 bot match (60 fps on the server and client).

See SECURITY.md. Not published.


## 2026-11-18: Killer in the death plate, less text everywhere

- Death screen: the top-left killer card is gone; the bottom plate says KILLED YOU · WEAPON (or KILLED BY) over the killer's name in red, then SPECTATING over a teammate. No one-life line while spectating, and the spectate hint is only the keys.
- Removed repeated text: the gun name on the ammo panel, "/100" on health, NO DEFUSER on the bomb chips, LIVE / OBJECTIVE / degrees / BOOST in the feeds, the phase word before the objective, the second line of PLAY and PLAY WITH PARTY, PRACTICE, CHANGE (now a chevron), SELECTED on mode cards, Store headers that repeat the tab, and the selection screen's NEXT line, rule lines, TOP VIEW and map hints.
- PREP instead of PREPARE and ROUND 1/5 instead of ROUND 1 OF 5 (both were cut off on a phone). The phase banner stays clear of a feed's compass on a phone.
- Lobby column watchers in Client.Core.Matchmaking now connect at start.

See UI.md and DEATH_SCREEN.md. Checked on the phone emulator. Published 2026-11-18 16:01 UTC (place version 992).
