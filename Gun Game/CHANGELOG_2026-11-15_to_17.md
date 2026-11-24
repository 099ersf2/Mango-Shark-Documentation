# Changelog archive: 2026-11-15 to 17

Historical implementation notes, retained as written for search and context. Verify behavior against current system guides before using these details.

## 2026-11-17: Cleaner spectate screen

- One spectate plate at the bottom with PREV and NEXT on its ends, a hint above and the status under it; the killed-by card at the top left.
- Gameplay controls and Roblox's thumbstick hide while dead.

See UI.md. Not published.


## 2026-11-17: No building or billboards from cameras, drones or death

- Server: no repairing or reinforcing while looking through a camera or driving a drone.
- Client: `Client.Core.ViewHide` hides every billboard (except scan marks) and turns prompts off while dead, on a camera or in a drone.
- The round result keeps the death screen hidden when a death ends the round.

See UI.md. Not published.


## 2026-11-17: Feeds checked in play on a phone

Drone and camera feeds checked in Recruit Training (attack and defend rounds) on the phone emulator. Feed text over the 3D view has an outline, camera PREV and NEXT have chevron icons, and the training panel keeps its size inside a feed. Not published.


## 2026-11-17: Exit buttons no longer overlap on phones

Drone and camera feeds: EXIT top right, other touch buttons placed so none overlap on a phone; no overlaps found in menus or the HUD either. See UI.md. Not published.


## 2026-11-17: Drone and camera feeds on a phone

- Phone layouts also switch on for phone-sized screens with keyboard input.
- Feeds on a phone: header below Roblox's buttons, a compact objective tag, a narrower compass and boost row, and Roblox's thumbstick and jump button hidden while the feed is up.
- The training panel takes the objective tag's place in a feed on a phone, clear of the compass and touch buttons.
- `Client.Gadgets.DroneBoost` reads the clock itself and keeps `Bars`, so the drone feed works with the controller as it is (an edit to the controller had been overwritten).

Checked on the phone emulator. Not published.


## 2026-11-17: Drones can be driven again

- `Content.Drones.HITBOX_PADDING` (0.3) added: `DroneService` used it for the drone's hit box and every drone placement errored, so no drone spawned.
- `Client.Gadgets.DroneController` matches the rewritten `DroneBoost` (three charges): the feed no longer errors every frame, the boost label shows BOOST n/3, and boost bursts end and come back.

See DRONES.md. Checked in Recruit Training. Not published.


## 2026-11-17: Pop-ups out of the way on phones

- The phase banner no longer stays at the bottom over the health bar and weapons after the selection screen closes.
- On touch, notices sit under the bomb sites and the planting bar above the weapon row.
- On touch the training panel is just the goal and one line, clear of the left buttons.

Checked on the phone emulator. Not published.


## 2026-11-17: No mint in the in-match HUD

- The HUD in play is white, gray and team colors only; mint stays in menus (`Content.Theme` convention 3).
- Training help panel uses the HUD's glass plate; ammo panel without the stripe and with a gray AUTO; your top bar slot outlined white.
- Won rounds ally blue, a won match gold; gadget meters white; Leo's warning gold.

Checked on the phone emulator. Not published.


## 2026-11-17: Gray held weapon slot, roomier training stepper

- The held weapon slot is gray with a white outline (was a light fill with a mint outline).
- The training stepper names only the current step on touch and narrow panels; on touch the hint replaces the description instead of growing the panel.

Checked on the phone emulator. Not published.


## 2026-11-17: Kill feed with gun pictures, phone HUD without overlaps

See UI.md "Guns as pictures and no overlaps on a phone". Not published.

### Changed

- Kill feed rows show the gun's picture (a white silhouette of its model) or an icon between the names, colored by side; two compact rows on touch.
- On touch the weapon slots show the gun's model instead of its name.
- On touch the weapon row, objective line and bomb sites are placed from the real edges of the pieces next to them; health and ammo no longer touch the bottom edge; the training goal panel shrinks to stay above the left buttons; banners settle under the crosshair on phones.


## 2026-11-17: Field UI bug fixes and phone pass

From the owner's screenshots and a test on Studio's device emulator (750 x 382 touch). See UI.md "Bug fixes and the phone pass". Not published.

### Fixed

- Shop class cards showed the template's crate icon beside the class letter (`Content.Icons` now marks labels code has set; `Client.Core.IconBinder` skips them).
- Class prices were invisible (dark text on the dark can't-afford button); `Client.Core.AutoContrast` now reaches nested text.
- "NEW" and "INVENTORY" were cut off; auto-sized text is measured again once the fonts have loaded.
- Menus started 58 pixels too low (the top bar was counted twice).
- `Content.Store.Style` borders and ribbons have their own colors again.

### Changed (touch)

- Compact menu headers on short screens; the lobby nav and gear hide while a menu is open; Settings hides keyboard binds on touch.
- HUD: health and ammo bottom center, weapon slots as a tappable row, SCORE beside the gear, bigger score bar and bomb sites.
- Recruit Training: goal panel in the top-left corner, touch hints.
- Game Modes and the death screen no longer overlap on a short screen.


## 2026-11-17: Field UI, built from researched conventions

Every screen was redone again, this time from published guidelines (Xbox Accessibility Guidelines 101 and 102, Game Accessibility Guidelines, Apple and Material touch targets, Roblox's UI and cross-platform docs) and screenshots of Rainbow Six Siege, Call of Duty: Mobile and Battlefield 2042 on the Game UI Database. See UI.md "UI standard and the Field look". Checked in Studio playtests at desktop and phone size; not checked on a real phone. Not published.

### Changed

- **Look:** graphite glass panels, one signal-mint accent with dark text on it, Titillium Web and Builder Sans, 6 px corners and hairlines, applied to every GUI object and to the colors in 28 UI scripts (`Content.Theme`).
- **Standard:** no text under 12 px (14 in menus), 4.5:1 contrast, 44 px touch targets; menus shrink to no less than 72% on a phone.
- **Lobby:** a bottom-right column with PLAY at the bottom; settings is a gear icon.
- **HUD:** health, ammo, slots and gadgets on glass plates; dark numbers on team score boxes.
- **Menus:** one frame for all of them (title, tabs with a mint bar, X close, mint top line); Game Modes aligned with a BACK button; store ribbons and item borders recolored; locked classes show a lock and price; compact class panels on phones.
- **End screens:** round result, match result and death screen restyled; the spectating name no longer overlaps.

### Added

- `Client.Core.AutoContrast`: keeps text readable when code recolors a button.
- 34 icons in `Content.Icons` (settings, users, heart, skull, eye, info and more).


## 2026-11-17: Icons instead of emoji

Every emoji and symbol glyph in the UI is now an icon from one set of white line icons (Lucide, from the Creator Store), drawn by the new `Content.Icons` and `Client.Core.IconBinder` (see UI.md "Icons, not emoji"). Checked in a Studio playtest with saving off: lobby, Shop (Featured, Currency), Inventory, Settings and the selection screen, with no errors in the Output. Not checked: a phone, the Battle Pass screen (the pass is switched off), Recruit Training, the death and match-end screens. Not published.

### Changed

- **Studio UI:** 51 labels in UILoader and Assets.UI.Templates now carry `Icon` attributes instead of emoji text (wallet and nav icons, store cards, gift, lock and check marks, Battle Pass cells, option arrows, BACK and CONTINUE buttons, the HOME chip, the PLAY arrow, training crates and marks).
- **Code:** Store, StoreViews, ItemDetails, Inventory, BattlePass, SiegeSelect, ModeMenu, Tutorial, Scoreboard, CustomPrompts, the phase Banner and `Content.Theme.Crumb` draw icons through `Content.Icons`. Store section icons, glyphs and HOT DEAL tags in `Content.Store`, `Content.Crates` and `Content.Matchmaking` are icon names.
- **Server:** StatsService writes only the streak number; the StreakTag template has a flame image.
- **VIP charm:** the crown glyph on the dog tag is a crown image.


## 2026-11-17: Siege UI (third look)

Rebuilt in the style of Rainbow Six Siege's menus, from the owner's reference (Game UI Database, game id 264). Checked in a Studio playtest with saving off (`ScribeNoSave`): lobby, Settings (Controls, Audio), Shop, Inventory, the selection screen and the in-round HUD at desktop size, with no errors in the Output. Not checked: a real phone, the death screen, the match result, Party and the Game Modes panel (these got the new colors and fonts but no new layout). The UI before this is in `ServerStorage.Archive.UIBeforeSiege_2026_11_17`. Not published.

### Changed

- **Colors and type (`Content.Theme`):** slate navy panels, Siege blue for the main action, gold only for currency and NEW, Oswald Bold titles and Roboto Condensed text, square corners. Applied to every screen and template (1,120 backgrounds, 762 fonts, 316 corners, 104 outlines) and to the colors set in code in 24 client modules, `Content.Store.Style` (tags and coin gold) and `Content.Matchmaking` (mode colors).
- **Lobby:** a Siege PLAY page: "◀ HOME" chip, a huge PLAY title and picture-style tiles (blue PLAY, GAME MODE, PLAY WITH PARTY, then TRAINING and SQUAD as light slate tiles), with dark shades behind it and the nav bar. The DEPLOY card is gone.
- **Nav bar:** the wallet strip is now Siege's top nav: HOME, SHOP, INVENTORY, BATTLE PASS as big words; the open menu's word is white and underlined. Coins in gold on the right.
- **Store, Inventory, Battle Pass:** tabs across the top under the title (the left icon column is gone); featured Store cards fill the row two by two.
- **Settings:** option rows with a black value box on the right; sliders are a thin white line.
- **HUD:** health and ammo float without panels; the phase banner is big centered capitals with a gold objective line; the round result is a fading dark band with a colored title.


## 2026-11-17: Lobby, wallet and store cards rebuilt; touch buttons fixed

Checked in a Studio playtest with saving off, at a narrow (phone-like) and a desktop width. Touch itself could not be run in Studio from the tools.

### Fixed

- **Huge dark disks around every touch button (and a broken crosshair):** the last restyle set every UIStroke to Thickness 1, but the touch buttons' and crosshair's strokes use `StrokeSizingMode.ScaledSize`, where 1 means the element's whole size. The 35 scaled strokes got their old thickness back from the archive (0.03 / 0.04 buttons, 0.5 crosshair). Rule for later passes: never set a ScaledSize stroke's thickness in pixels.
- **Combat touch buttons in the lobby:** they covered the lobby and did nothing there; `Client.Core.UI` now hides `Main.Mobile` while `InLobby` (Roblox's thumbstick and jump stay).
- **Menus under Roblox's buttons on phones:** Store, Inventory, the detail page and Battle Pass now start below Roblox's top bar (`BelowTopbar`).

### Changed

- **Lobby: a DEPLOY card** in the bottom right (was a bar along the bottom): MODE row, a big PLAY (left-aligned, with an arrow), PLAY WITH PARTY and PARTY side by side (PARTY takes the row when PLAY WITH PARTY is hidden), and a slim TRAINING row. On touch it is lifted above the jump button and 78% size on short screens. Layout in `Client.Core.Matchmaking.layoutBar` (`CARD_*`).
- **Wallet:** a strip across the top left (coins, INVENTORY, STORE, BATTLE PASS as tabs with an icon), instead of tiles. The settings button is one compact button at the top right.
- **Store and Inventory cards:** operator-card style: a thin bar in the item's color on top, the art in the middle, name and type bottom left, the old price bottom right, tags inside the card, a slimmer glow.
- **Menus are pages:** Store, Inventory, detail page and Battle Pass take 97% of the width (up to 1600 x 900); Settings and Party are larger and sit below the top bar.


## 2026-11-17: Tactical UI (Siege-style) for the whole game, Settings tabs, volume sliders fixed

Checked in Studio playtests with saving off: lobby, Settings (every tab), Store, Inventory, Party, the training reveal and the in-match HUD; a text-overflow scan of every menu found nothing cut off. The UI before this is in `ServerStorage.Archive.UIBeforeTactical_2026_11_17`.

### Changed

- **New look, same system:** the Midnight / Aqua / Pink colors were too bright for an FPS. `Content.Theme` keeps the system and conventions with tactical colors: near-black glass panels (Void, Base, Panel, Raised, Card, Line), one **Amber** accent (`#F0B43C`) for the main action and what is selected, white text, and red, green, team and rarity colors only where they mean something. Every screen and template was restyled by `Theme.Map` (1,817 objects, 279 outlines, 253 corners) and 285 colors set in code.
- **Font:** FredokaOne (round, cartoon) replaced by **Gotham** everywhere (756 labels and the fonts set in code): bold for titles and buttons, medium for the rest.
- **Shapes:** small corners (4 to 6) and 1 px hairlines instead of big rounded bubbles and thick outlines.
- **Every menu has the same frame:** an amber bar along the top, title left, close right, slightly see-through glass (Store, Inventory, Settings, Battle Pass, Party, invites, Loadout, Modes, detail page, gift picker).
- **Menus sit in the world:** while a menu is open the world behind it is blurred and a little darker and greyer (`Client.Core.MenuAmbience`).
- **Text never overflows:** every fixed-size label shrinks to fit (474 labels got a `UITextSizeConstraint` with their old size as the most, and `TextScaled`).
- **Settings in tabs:** CONTROLS, GAMEPLAY, DISPLAY, AUDIO along the top (white with an amber underline when chosen), one section at a time.
- Bomb letters stay red A and blue B; a lost match tints red.
- Training: the stepper's BREAK IN is now BREACH (it fits), the briefing no longer repeats the round (the banner says it), and the goal card sits lower so announcements don't run into it.

### Fixed

- **Volume sliders showed 100% after rejoining** although the saved volumes were applied to the sound: they load after the Settings rows are built, and nothing told the rows. `Client.Audio.AudioSettings` now fires `Changed` for each loaded volume, so the sliders show the saved values (checked: 58%, 69%, 30% shown and heard).

### Added

- `Client.Core.MenuAmbience` (menu blur and grade), `Main.Settings.Tabs`.


## 2026-11-17: One theme (Midnight, Aqua, Pink) and UI conventions everywhere; a quieter tutorial

Checked in a Studio playtest with saving off (lobby, Store, Inventory, the Notice popup, the training briefing, goal card and toast). The UI before this is kept in `ServerStorage.Archive.UIBeforeTheme_2026_11_17`.

### Changed

- **Colors:** the owner's palette everywhere: **Midnight Abyss** `#171F44` (every surface, in five steps), **Aqua Jade** `#74FFED` (accent: selected, values, progress) and **Baby Pink** `#FE81D1` (the main action: PLAY, START, BUY). Dark text goes on aqua and pink. Red stays for danger and the enemy; team, bomb and rarity colors are unchanged. Recolored by one rule (`Content.Theme.Map`): 1,813 UI objects in `UILoader` and `Assets.UI.Templates`, and 284 colors set in code in 27 UI modules (not skins, effects, teams or bombs).
- **Popups dim what's behind** (70%): the Notice popup (new `Main.NoticeBackdrop`), the detail page and gift picker blocker, and the training popups. A tap on the dimmed area closes them.
- **Notices look like content, not ads:** the Notice popup is a card with an icon (red "!" for an error, aqua "i" for a heads-up), a title, one short line and one GOT IT button. The announcement banner is a quiet card with a colored bar at the left instead of a colored outline and colored title. Reward and pass toasts are outlined cards; SCANNED is a small red-outlined chip.
- **Store and Inventory cards** show only a hint of the item's color over midnight (they were full-color gradients with dark titles that were hard to read).
- **Secondary buttons are outlined** (TRAINING, PLAY WITH PARTY), so PLAY is the only bright action in the lobby.
- **The Battle Pass track** starts with the next level cut at the right edge (`Client.Core.Peek`), so it reads as a row that goes on.
- **Recruit Training, far fewer words:** the goal card is the round's steps as circles joined by a line (FIND, BREAK IN, PLANT, PLANT / FORTIFY, HOLD), a title and one short line; the bonus is a small pink chip; the hint is one line of keys, only once stuck. The briefing is ROUND n OF 2, ATTACK or DEFEND, one line and the class chip. The invite is RECRUIT TRAINING, one line, a FREE CRATE · RARE+ chip, START and Not now. The toast is a check (or a star for a bonus) and the goal's name.

### Added

- `Content.Theme`: the palette, its steps, the conventions, and `Map` / `IsBright`.
- `Client.Core.Peek`: `Peek.Cut(scroller)` for horizontal lists.


## 2026-11-17: Recruit Training (the tutorial) and the Recruit Crate

Tested in a Studio playtest with saving off (the new `ScribeNoSave` switch). See [Recruit Training](TUTORIAL.md).

### Added

- **Recruit Training:** a 1v1 against a very easy bot, two rounds: attack (find the bombs with the drone, break in, plant both defusers), then defend (board up two doorways, check the cameras, hold). No class, site or spawn picks. Goals say what to do; the how appears as a hint only after the player is stuck. SKILL LEARNED toasts and a SKILLS n/9 counter. Built after looking at Rainbow Six Siege's Situations, Valorant's Basic Training, CS2's Training Day, Roblox BedWars and Valve's Portal/Half-Life 2.
- **First-join invite** (START TRAINING / NOT NOW) and a lobby **TRAINING** button (FREE CRATE until earned, then OPEN CRATE, then PRACTICE). Skipping is saved; the reward stays available until they finish once.
- **Recruit Crate:** given once, for the first finish. Rare or better (no Commons in it). Not sold.
- Files: `Content.Games.Tutorial`, `Content.NPC.Profiles.TutorialBot`, `Content.Crates.Definitions.Recruit`, `Systems.Games.Siege.TutorialService`, `Client.Hud.Tutorial`, UI `UILoader.Training` and `Main.Lobby.Training`, packets `Packets.Tutorial`.
- Saved data: `Tutorial` flags (`Done`, `Rewarded`, `Skipped`).
- **Studio only:** the workspace attribute `ScribeNoSave = true` makes playtests read real data and never save (`Shared.Data`).

### Changed

- `SiegeService` plays a `Tutorial` mode match (given picks, training times, 300 health, site shown at Action); new `SiegeService.IsTutorial()` and `SiegeService.Round()`.
- `QueueService.JoinTutorial` and the `Queue.Request` action `Tutorial`. Matchmaking mode `Tutorial` (hidden from the Game Modes panel); `Siege.ROUNDS.Tutorial = 2`.
- `SiegeBots.Spawn` uses a bot entry's `Profile` when it has one.
- Crates can be `Hidden` (left out of the Store and the Inventory's skin groups).


## 2026-11-17: Attacker bots push together, talk to each other and dress like players

Tested in Studio playtests on Bank (basement forced) and Mansion. No player data was written.

### Fixed

- **Attacker bots circled the vault and never reached Bank's basement.** The hatch upstairs sits right above basement bomb A (9.75 studs), so bots took it as the way down, but it opens into the vault. They dropped into the vault, found no path, and climbed back to the hatch. A hatch now only counts for a room when a raycast from under it lands in that room (`dropsInto`, cached per hatch and room). Checked: from every Bank attacker spawn the paths reach both basement rooms; with the basement forced, two bots were in the basement in 12 to 16 s and the attackers won by planting both bombs in 43 s.

### Changed

- **Attacker bots work as a squad.** Once they know the site they all go for one bomb: the room a teammate is already in, else the one with the fewest recent sightings of defenders (a little random, and less likely last round's bomb). They gather at a rally point outside a random entrance of that room (not last round's), then push in together, each `PUSH_STAGGER` (0.7 s) after the one before. The push starts when all have arrived, `GATHER_WAIT` (6 s) after the first arrived, or `GATHER_MAX` (20 s) after the plan was made. A bot already closer to the room than the rally point goes straight in. Before the site is known the scouts spread over different sites.
- **Bots talk to each other over a team radio** (players don't see it; their chat is unchanged). Teammates act on what they hear: an enemy seen goes into the team's memory and idle bots go after it; a bot killed tells where it was shot from and the nearest free attacker goes there to trade (`TRADE_RANGE`, 70 studs); a hurt attacker in a fight (under `HELP_HEALTH`, 60%) asks for help and the nearest free attacker comes (`HELP_RANGE`, 60 studs; at most every `HELP_GAP`, 6 s); an attacker planting makes the squad stop gathering and push in; the plan, the push, the site and a defender rotating are shared too. The last messages are in `workspace.BotRadio` (attribute) for tests. Checked on Bank over two rounds: plan, push, plant, contact, down and rotate messages, and help calls answered ("Rook coming", "Vex coming").
- **Bots look like players:** each gets a shirt, pants, hair, face and skin tone from `Content.Games.SiegeBots.LOOKS` (free official Roblox items), picked from its id, so a bot looks the same every round.

### Added

- Nothing for players: the first version of this change showed the bots' callouts in the players' chat (packet `Siege.BotCall`, `Client.Hud.BotCallouts`); both were removed the same day, the module is in `ServerStorage.Archive.BotCallouts_2026_11_17`.


## 2026-11-17: Five crates removed, new grenade and smoke bomb models

- **Removed** the Gilded, Eclipse, Verdant, Field and Shield crates and their 65 skins (archived in `ServerStorage.Archive.RemovedCrates_2026_11_17`). As decided: players lose those skins and unopened crates (data migration 2 in `Shared.Data`, run once per profile when it loads; an equipped one goes back to None), and the rewards that gave them are dropped, not replaced: the Starter Bundle gives 2,000 Coins only, 19 Battle Pass crate rewards are gone (some pass sides are empty now), the daily deal is only the 15,000 Coins pack, the old Field Crate request refuses, and the `Crate_Field` and `Crate_Gilded` Robux products are no longer offered in game. Breach Point's shield (pass level 30) is still made, from a source-only copy of the Afterburn shield (`SeasonSkins.Sources`).
- **New models** for the frag grenade (bands, fuse, lever, pull ring) and the smoke bomb (caps, white band, vents, lever, pull ring): welded details on the same physics part; the throw carries them along.
- Checked in Studio: my test profile loaded, lost the removed AK-47 and still owns 20 skins; Inventory and Store opened with no errors; the Breach Point shield exists and the Afterburn shield doesn't.
- **Publishing:** a server still on the old code kicks a player whose data was already cleaned up (Scribe fails closed on newer data), so after publishing, restart old servers (Migrate to Latest Update).


## 2026-11-17: Gadget model on the Loadout page

- Picking a gadget (grenade or smoke bomb) on the selection screen's Loadout page shows its model in the panel, like the guns (`ClassPanel.ConsumablePreview`). Fixed on the way: the gun preview's turning kept aiming the camera at the last gun, which threw a gadget's model off-screen; it now only turns for guns.


## 2026-11-17: Crawl and slide like the reference clips

- **Crawl:** a low crawl: one knee drawn up and out to the side like a frog while the other leg stretches back, swapping as it moves, flat on the floor.
- **Slide:** a seated slide: hips on the floor, legs straight out in front, leaning back, one hand forward.
- Both now replace Roblox's walk animation instead of adding to it, which had lifted the crawling legs off the floor. See [Movement and camera](MOVEMENT.md).


## 2026-11-17: Prone and slide animations

- **Prone:** a lying animation (breathing; forearms propped up when no gun is out) and a crawl animation that runs with the crawl speed (legs sweep out in turn, the body rolls, the arms pull when no gun is out). **Slide:** leans back further as it settles, with a wobble, and the trailing hand reaches for the floor when no gun is out. All made in code in `Client.Movement.MovementPoses`, seen by everyone. See [Movement and camera](MOVEMENT.md).


## 2026-11-17: Scan marks as pins with meters, picks on the selection map stay put

### Changed

- **Scan marks** (a drone or camera scan of an enemy, `Templates.SpotMarker`): a map pin (round head with "!" and a point on the spot) with the distance in meters over it, kept up to date. Red for drones, the camera color for cameras.
- **Selection map, Siege and Clear House:** the site, spawn or map you tap or click stays on the map until you pick another. Hover (mouse only) previews while the pointer is on a row; on a touch screen it is ignored, so a tap no longer jumps the view back. Clicking a pin on the map votes the site or takes the spawn on PC and on touch. Checked on PC in Studio; not tried on a phone. Studio screenshots don't show BillboardGuis, so the pin was checked by its parts and a copy drawn on screen.


## 2026-11-17: No view bob crouched or prone, defender bots hold both bombs, the bot icon

Tested in Studio playtests with bots on Bank. No player data was written.

### Fixed

- **Defender bots left a bomb unguarded.** A threat (an attacker seen, heard or planting in a bomb room) sent every defender bot to that room, and afterwards each kept the room it stood in, so all of them stayed there and the other bomb was free to plant. Now each defender has a home bomb (the team split evenly; a bomb whose guards died takes one from a bomb with two or more), a threat pulls in the others but never a bomb's last guard (not even for a plant on the other bomb), and when the threat is over each goes home. A defender walking home doesn't chase what it sees on the way. Checked: with A held by two and B by one, a threat in B brought one from A while the other stayed and B's guard held; back home 5 s after the threat. With one guard each, an attacker planting in B left A's guard where it was.

### Changed

- **No view bob crouched or prone:** the gun's walk bob (`Client.Guns.Viewmodel`) fades out with the stance change, the shield's (`ShieldView`) stops, and the camera's strafe tilt is off then too (the camera bob already was). The camera's head correction is smoothed in those stances too, so the crouch-walk and crawl animations' head bounce can't reach the camera. Measured crouch-walking and crawling: camera, gun and shield move 0.000 studs. A slide (crouch while sprinting) still tilts and dips the camera on purpose.
- **Bot icon** (`Content.Games.SiegeBots.ICON`, image 117259180607823) wherever a player's picture shows: party slots and the bot list, the selection screen's player cards, the death screen when a bot killed you (`DeathCamService` now sends the bot's own negative id), and the MVP cards.


## 2026-11-17: A lighter look, one class panel everywhere, a weapon HUD with gun models

Tested in Studio playtests (lobby menus and a Siege match on Mansion). No player data was written.

### Changed

- **Lighter UI across the game:** every near-black panel (221 of them in `ReplicatedFirst.UILoader` and `Assets.UI.Templates`) is now a slate blue, keeping its own hue when it had one; touch-button icons, NO SIGNAL screens and dimmers stay dark. Colors set in code got the same change (`LobbyHubUI`, `Matchmaking`, `SiegeSelect`, `Store`, `Inventory`, `BattlePass`, `SiegeHud`, `LoadoutMenu`, `DroneController`, `DeadCallController`, `DeadCallTargets`, the announcement `Banner`). Menus whose dark gradient multiplied their background (Store, Inventory, Battle Pass, crate opening, the selection screen) got light gradients. The UI before this is kept in `ServerStorage.Archive.UIBeforeLight_2026_11_17`.
- **Inventory, CLASSES tab:** like the Siege selection screen: a grid of class tiles (locked ones covered with their price) and the class panel beside it. UNLOCK opens the class's page to buy it.
- **Store and Inventory detail pages:** a class shows the selection screen's class panel (role, difficulty, speed, ability, weapons and gadgets, your avatar). A skin shows the gun panel: the gun's damage, fire rate, magazine and mobility bars beside its turning model, and a DETAILS list (rarity, weapon, copies owned, where it comes from). Clicking a class's starter gun shows that gun's stats.
- **Weapon HUD:** each weapon slot is a row with its key, the gun's model (in your skin) and its name; the held one turns light with dark text. The ammo box shows the held gun's model beside the big count.
- **Selection screen's loadout panel** shows the gun's model in your skin instead of your avatar.

### Added

- `Client.Core.ClassPanel`: fills the class panel and the gun panel (templates `ClassPanel`, `GunPanel`) for the selection screen, the Inventory and the detail page.


## 2026-11-17: Siege UI pass: pre-match screens, top bar, hit effects, HUD

Our own take on what Rainbow Six Siege's screens do well, in SiegeBlox's look: dark navy panels, gold for "you" and "next", the team's color for your side and red for the enemy, rounded blocky shapes with a little "stud" on class emblems, and Fredoka One everywhere. Tested in Studio playtests with bots on Mansion and Bank, at 1920 wide and at a narrow 919 wide (see [UI](UI.md#siege-ui-pass-2026-11-17)). The only player data written was the gadget pick (Frag grenade to Smoke bomb and back again).

### Added

- **Pre-match in four steps** (`Client.Core.SiegeSelect`, rewritten; the old one is in `ServerStorage.Archive.SiegeSelectOld`): LOCATION, CLASS, LOADOUT, READY across the top, the current one gold, done ones ticked (click one to go back), and a NEXT line saying what to do.
    - **Location** shows the map in a viewport. Attackers see it from above with a pin per spawn (click a pin to take it, a teammate's shows their name). Defenders see a pin per site; pointing at a site (or voting it) shows it **cut away**: everything above that floor hidden, the A and B rooms drawn in red and blue, the bombs pinned. Clear House previews the map you point at.
    - **Class** is a grid of class tiles and a big panel: role, difficulty, speed (from the primary gun), ability, weapons and gadgets, with your avatar on the team's color. Picking a free class takes you to the loadout once the server confirms it.
    - **Loadout**: primary, secondary, ability and gadget rows with arrows, and a panel with the focused gun's damage, fire rate, magazine and mobility as bars against the best gun in the game. CONFIRM LOADOUT readies you.
    - **Ready / Reveal**: a tall player card per teammate (avatar, class badge and name, spawn or vote, a tick when ready), dealt one by one at the reveal.
    - The footer counts who is ready on each team (a dot per player).
- **Top bar** (`Client.Hud.SiegeTopBar`, `Main.SiegeHUD.TopBar`): a tile per player on both teams (class letter, team stripe, you outlined in gold, dead players crossed out; an enemy shows "?" until seen), both scores, the clock and the round. The drone and camera feeds have the same bar.
- **"3 VS 4"** in the middle of the screen whenever someone dies in Action, your side first, with ENEMY ELIMINATED or TEAMMATE DOWN.
- **Hit effects** (`Client.Combat.DamageFeedback`, `Main.DamageFX`): red at the screen's edges on every loss of health (stronger for bigger hits), an arrow round the crosshair pointing at the attacker (new packet `Combat.Hurt`, sent to the victim by `Combat.ApplyHit`), and at 35% health or less a heartbeat pulse, a greyer world and a red health bar.
- **Drone and camera feeds** (`Client.Gadgets.FeedInfo`): the team bar, the objective (FIND THE SITE / SITE LOCATED / DEFEND ...), where the feed is (a bomb room by name, INSIDE or OUTSIDE), a compass and faint scanlines.
- **Classes** have a `Role` and a `Difficulty` (1 to 3), shown in the class panel.
- The Siege snapshot has the map's name (`Map`), so the selection screen can draw it from `ReplicatedStorage.Maps` (the live map streams in).

### Changed

- **HUD near the edges**: health is a panel in the bottom-left corner (bottom middle on touch); the ammo box, the weapon slots and the grenade, drone and ability chips are one stack in the bottom-right corner on dark panels. The held weapon shows a gold bar and pops when you switch.
- **Bomb marks** are a diamond with the letter and the distance in meters under it.
- The announcement banner sits at the bottom while the selection screen is up, so it doesn't cover the map.
- Old selection templates (`SiegeOption`, `SiegeClassCard`, `SiegeTeamCard`, `SiegeReadyRow`, `SiegeReadyHeader`) moved to `ServerStorage.Archive.SiegeSelectOld`.


## 2026-11-16: Bot drones go through wall vents

Tested in a Studio playtest (no player data written).

### Added

- **Vents for bot drones:** a wall vent's hole (about 2.8 by 0.85 studs) is too small for pathfinding, so `BotDrones.Prepare(map)` puts a `PathfindingLink` labelled `Vent` through every model named `Vent` when the bot drones deploy (once per map copy, so new maps get them too). Bot drones' paths take them; every NPC's path prices `Vent` at `math.huge` (`Brain.NewPath`), so bots on foot never try to crawl through.
- Checked: paths through all 5 vents of the bank building and 2 of Mansion's 4. A bot drone drove through the Mansion vent at x 17.5 in about a second. In a real match on Mansion the 4 links were made when the drones came out. Mansion's other two: one is in a garden wall (grass on both sides, nothing gained) and one opens onto a bunk bed, which a drone can't get down from.


## 2026-11-16: Siege bots: drones, shooting boards from range, team memory, defenders breaking in

Tested in Studio playtests: private matches of one admin player and four bots on Bank and Mansion (see [Siege bots](SIEGE_BOTS.md#drones-memory-and-breaking-in-2026-11-16)). No player data was written. One run was cut short when Studio lost its connection to Roblox (DataStore and asset requests timed out and the server kicked the player: "We couldn't load your data").

### Added

- **Bot drones** (`Systems.Games.Siege.BotDrones`, new): every attacker bot drives a scout drone in Prep. It checks the nearest sites no teammate has checked, finds the real one (inside it, or spotting a defender standing in it), then parks in its bot's bomb room. It spots enemies within 45 studs: into the team's memory, and marked on its player teammates' screens. It can be shot (one hit), defenders hear its motor, and teammates can't hurt it. It slips under door boards like a Siege drone through a barricade gap (player drones can't yet). When a bot's drone finds the site, the players get "Site located" too.
- **Shooting boards from range:** a profile's new `BreachRange` (SiegeBot: 30 studs) lets an NPC shoot a board on its path open from where it stands, with a clear shot, instead of walking up to it; it never bashes. In the tests bots shot boards open from 13 to 29 studs.
- **Team memory** (`SiegeBots`): bots share what they see and hear (30 s), and which sites they checked. A bot with nothing to fight goes after a teammate's sighting from the last 6 s within 50 studs on its floor.
- **Defenders break their own boards for a threat:** an enemy seen in a bomb room (or heard there in Action) in the last 10 s sends every defender bot there, and one outside may break its own team's boards to get in (`Brain.SetBreakThrough`). Without a threat a defender bot never breaks boards (`agent.NoBreach`).
- **Remembered entrances:** for the whole match, the boards attackers broke through on each map. A defender guarding a room watches the one attackers used most 60% of the time (`agent.WatchHint`, `Tasks.Patrol`).
- `DroneService.AddExternal(model)`: a server-driven drone NPCs see and shoot (listed in `DroneService.All`).
- `SiegeBots.Scout`, `SiegeBots.SiteFound`, `SiegeBots.NewMatch`; `Brain.BoardOnPath`, `Brain.SetBreakThrough`.

### Changed

- `SITE_INTEL_TIME` 25 → 45 s: attacker bots now find the site with their drones; the timer is only a fallback.
- **Defenders keep their room:** a defender bot that holds a bomb room keeps it when a teammate dies (until then the split dealt the rooms again, sending one across the map, where it broke its way into a room its teammates had boarded up).


## 2026-11-16: NPC pathfinding: stairs, climbing, the pool, breaking in through doors

Tested in Studio playtests with attacker bots sent from the attacker spawns to the bomb rooms of both maps, boards up (results in [Siege bots](SIEGE_BOTS.md#getting-to-the-bomb-rooms-2026-11-16-studio-boards-up-no-defenders)). No player data was written.

### Fixed

- **Stairs and floors:** a waypoint counted as reached by flat distance only, so on stairs, at a jump or below a floor the NPC skipped waypoints above or under it and walked at a wall. A waypoint now also has to be at the NPC's height (`WAYPOINT_HEIGHT`, 3.5 studs from its feet).
- **Paths that started on the roof:** a path started from the NPC's root, so under a porch roof (Mansion's back door) pathfinding started it up on the roof. Paths now start from the floor under the NPC.
- **Stuck in the Mansion pool:** the only way out was a 7-stud jump past the ladder's rails, which failed every time, so the NPC jumped at the wall forever. The pool ladder now has an invisible truss (`Maps.Mansion.PoolLadderTruss`, at x 28; the ladder's metal parts moved 1.8 studs to line up and no longer collide), and NPCs climb it.
- **Breaching loops:** a goal a floor up always has a long path (the stairs), which `Tactics.Breach` took for a detour worth breaking a wall for: the NPC walked to a ground-floor soft wall, found nothing to break, and picked it again. Long paths count as detours only for a goal on its own floor (`DETOUR_FLOOR`, 6 studs from its feet), and an entrance found already open isn't picked again for 20 s.

### Added

- **Climbing:** NPC paths climb trusses (`AgentCanClimb`), visible or not, so an invisible `TrussPart` on a ladder or wall gives NPCs a way up. While climbing, the NPC keeps walking into the truss and never hops off it.
- **Water:** the Mansion pool's `Water` parts have a `PathfindingModifier` labelled `Water`, which costs 8 per stud, so paths go round the pool.
- **Paths through boards** (Siege attacker bots): every intact piece of a door or window board carries a `PathfindingModifier` labelled `Breakable` (PassThrough), taken off when it breaks (`BreakableService`). A path made with `Brain.NewPath(true)` goes through a boarded door at a small cost, and `Tactics.Breach` breaks the board when the NPC gets there (`Brain.BlockedAhead`). Other NPCs price the label `math.huge`, so boards still block them. `NPCService.Spawn` has a `BreakThrough` option; Siege attacker bots use it, defenders don't.
- **Bot detours** (`SiegeBots`): the unstick detour spot is now on the bot's own floor and never in water or a pit.

### Changed

- **Bank's upstairs is reachable:** with paths through boards, attacker bots get up the stairs (13 to 58 s from a spawn). The stairs were never the problem: every path into the bank went through a boarded door.


## 2026-11-16: Siege bots (admins only for now)

Tested in Studio playtests with one admin player and three bots (see [Siege bots](SIEGE_BOTS.md#tested-2026-11-16-studio-playtests-one-admin-player)). No player data was written.

### Added

- **Siege bots** (`Systems.Games.Siege.SiegeBots`, `Content.Games.SiegeBots`, `Content.NPC.Profiles.SiegeBot`):
    - **Selection:** a bot picks a class no teammate has. An attacker bot picks a free spawn next to its team's; a defender bot votes for the site its player teammates voted for. A player who takes a bot's class or spawn gets it, and the bot picks again.
    - **Defending:** defender bots guard the two bomb rooms (Guard mode: stay in, rebuild boards, fight first). They all go to a bomb being planted, and hold the other bomb once one has its defuser.
    - **Attacking:** attacker bots find the site (a drone, a bot walking into it, or after 25 s of Action) and split between the bombs. To get in they break boarded doors and windows, or shoot open a hatch over a room below (the Mansion basement) and drop through. They hold the room while the defuser plants.
    - Bots count for the win rules and appear on the scoreboard, kill feed and result screen. They get no rewards, quests or analytics.
- **BOTS tab** in the Party menu, for admins (`Modules.Classes.Admins`): ADD puts a bot in the party (`Party.Request` "AddBot"). Bots queue and play like members, can be kicked, never lead, and come back with the party after a match.
- `NPCService.Spawn(id, cframe, part, ignoreCap, options)`:
    - `options` gives an NPC its own `Team`, `Name`, `Gun` and `AlwaysAwake` (never sleeps far from players).
    - `NPCService.AgentOf(model)` returns the live agent of an NPC model.
    - Profiles may set `AimErrorScale` and `AimErrorFloor`.
- NPC objectives (`agent.Objective`, `ObjectivePart`, `ObjectiveShoot`, `ObjectiveDirect`): with nothing to fight, `Tasks.Patrol` walks there (breaking in if it must), shoots a point open, or walks straight in.

### Changed

- Match records have `Bots` (`{ U, N }`), and tickets have `B`. Bots are in `Teams` but never in `Expected`.
- `Tactics` hearing: an NPC with an objective ignores noise on another floor.
- `SiegeService` planting progress is kept per UserId, so bots plant too.


## 2026-11-16: Battle Pass off until its own update

Tested in a Studio playtest (server and client). No data was written (Coins 1,058, XP 0, quests unchanged).

### Changed

- **The Battle Pass is off** (`Content.BattlePass.ENABLED = false`), so it can launch later as its own update. While it's off:
    - **No XP:** `BattlePassService.AddXP` pays nothing (matches and quests).
    - **No quests:** `QuestService` doesn't start, count or draw anything.
    - **No claims:** `Claim` answers "The Battle Pass isn't out yet."
    - **Nothing shown:** the BATTLE PASS button in the lobby is hidden (the wallet closes up), the screen won't open, the pass isn't in the Store (`Hidden`), season skins show only to owners in the Inventory, a season skin's page says COMING SOON, and no "Season 1" tag is shown (`SeasonOf` gives nil).
    - To launch it: set `ENABLED = true`, check `SEASON.Ends` (now 2027-02-01), and link the Robux product (`Store_BattlePassS1` in `Shared.ProductIds`).
- **Store items can be hidden:** an item with `Hidden = true` is left out of `Content.Store.Store.ITEMS`, so it isn't shown or sold. `BattlePassS1` sets `Hidden = not BattlePass.ENABLED`. Its description now names Caleb (Hacker) instead of "classes".

### Fixed

- `Content.BattlePass` and `Content.Crates.Crates` had been put back to old versions in Studio (a collaborator's save). The reworked track and the `Content.Guns.Skins.Skins` require were reapplied. With the old Crates require, nearly every module failed to load.


## 2026-11-16: Guns through walls can't shoot past them, Studio match clean-up, next steps

Tested in Studio playtests. Two Clear House test wins were undone afterwards (Coins back to 1,058, Wins 5, the Clear House and Arcade stats, LastMode `5v5`, two weekly quests, two milestones, Battle Pass XP 0).

### Fixed

- **A gun (or head) poking through a wall can't shoot past it**, for players and NPCs (`Systems.Guns.GunService`). A shot's start is moved back in front of any solid wall between the shooter's HumanoidRootPart and it (`clearOfWalls`). NPC shots (`FireAs`) skipped every origin check before; they now get this one too. Tested on the server: a player's and an NPC's shot started 1.5 studs past a wall did no damage to a target behind it; the same NPC shot with the wall moved away hit it (20 damage).
- **Studio: back to the lobby after a match.** The new body counted as an arena spawn, so `InLobby` went back to false and the match loadout was given in the lobby. `LobbyService.Readmit(player)` (new) makes the next character a lobby spawn; Siege's end calls it before `LoadCharacter`. Tested: after a Clear House win the player was in the lobby, `InLobby` true, no guns.
- **Studio: the match's map copy stays in Workspace** after a match, so a second match played over two maps. Siege's end now destroys the copy it made from `ReplicatedStorage.Maps` and clears `ActiveSiegeMap`. Tested: the Mansion copy was gone after the match.
- **Game Modes panel opened empty** (no cards, the template's DUELS text) the first time in a session. The cards are now also drawn whenever the panel becomes visible (`Client.Core.ModeMenu`).
- **Mode card ribbon:** RECOMMENDED was cut off by SELECTED at the card's top. The ribbon is wider (72%) and SELECTED sits above the name (`Templates.ModeCard`).
- **Motion Scanner ability loads again:** its `tick` function was declared twice on one line (`local function tick()local function tick()`).

### Checked

- A full Clear House match (Mansion, solo) after the Games folder move: Selection, map vote, guards in waves (6, 4, 6), HouseCleared, the win paid, back to the lobby.
- Inventory search: "glacier" narrowed 127 cards to 11.
- `Definitions.ReinforcedDoor`'s model name is right: the asset is now named `ReinforcedDoor`.


## 2026-11-16: Shield shots through walls, coin icon, less camera bob, touch controls hidden behind menus

Tested in a Studio playtest on the phone screen (device emulator). No player data was written.

### Fixed

- **The Shield class (Bruno) appeared to shoot through walls.** Lying prone or holding the shield against a wall puts his third-person pistol's muzzle on the far side (measured 1.3 studs past a 1-stud wall). Other players draw his shots from that muzzle, so tracers, flashes and impacts came out of the wall. The real bullet was already stopped (tested: a dummy behind the wall took no damage).
    - `Client.Guns.GunEffects`: a shot drawn from a muzzle now starts in front of any wall between the shooter's eye and the muzzle (`clearStart`), for other players' and NPCs' shots and the local player's own in third person. The first-person tracer start no longer falls back to a muzzle that is inside a wall.
    - `Systems.Guns.GunService` (server): the shot's origin is checked for line of sight from the HumanoidRootPart (the collision box) instead of the head, which poses can push through a wall. A blocked origin moves to just in front of the wall instead of to the head. Only solid (CanCollide) parts block it.
- **Battle Pass track restored:** a later save had put back the old `Content.BattlePass`. The new track (several or no rewards per level, `LIST`, `SeasonOf`) was applied again; the totals match (97 rewards, 21,750 Coins).
- Old require paths fixed in `Content.Crates.Crates` (skins) and in the new `DroneShield` and `BulletproofCamera` abilities (classes).

### Changed

- **One coin icon everywhere:** every coin picture is `Content.Store.Style.COIN_ICON`. The new `Client.Core.CoinIcon` sets every ImageLabel or ImageButton named `CoinIcon` in the UI to it (the wallet, the Store and Inventory headers, the detail page, the StoreCard prices), including ones cloned later; Coins cards and rewards already used it. The Studio pictures were set to it too, and the coin emoji was taken out of the wallet texts and the reward line ("+500 Coins").
- **Camera bob** (`Client.Movement.MovementCamera`, `Content.Movement.Config`):
    - none while crouched, prone or sliding;
    - about half while walking (`BobUp` 0.035, `BobSide` 0.022, `BobRoll` 0.15);
    - none in third person, and no strafe tilt there either.
    - Measured walking 2.5 s: first person standing 0.028 studs of sway; crouched, prone and third person 0.
- **Touch controls behind menus:** the move stick and jump button are hidden while a menu is open (`Client.Core.Menus`, `GuiService.TouchControlsEnabled`) and come back when it closes.
- **No UI sounds** on Roblox's own touch move stick and jump button (`Client.Core.UIFeel` skips the `TouchGui`).

### Known

- `Systems.Classes.Abilities["Motion Scanner"]` (another developer's, in progress) does not load: a missing `end` at line 131.


## 2026-11-16: Battle Pass track rework, shared quests, season tags, skins in files, menu buttons toggle, no reset in the lobby

Tested in a Studio playtest (server and client). The test claim was undone (Coins back to 308, XP 0, no claims, the crate taken back). See [Battle pass and quests](BATTLE_PASS.md).

### Changed

- **Everyone has the same quests.** Today's dailies are drawn with the UTC day number as the seed and this week's weeklies with the week number, so every player on every server gets the same ones. A saved set that isn't today's (including sets drawn per player before this change) is replaced, and its progress for that day or week is cleared.
- **Battle Pass track** (`Content.BattlePass`):
    - A level can hold **several rewards on a side, or none**. Season 1 has 8 levels with two rewards (1, 8, 15, 25, 32, 40, 45, 50) and 13 empty Free levels.
    - **Coins:** always 250 (`COINS`), and **1,000 on every 5th level** (`COINS_BIG`) on the Free side.
    - **Classes:** only two, both at level 50: Matteo (Medic) free and Caleb (Hacker) premium, with the Breach Point Knife.
    - The whole track: 21,750 Coins, 11 season skins, 2 classes, 31 crates in 97 rewards.
    - `TRACK[level]` is now `{ Free = { Reward }, Premium = { Reward } }`; new `LIST` (every reward). A level's second reward on a side has the Id `S1_L<n>_F2` / `_P2`.
    - The screen widens a level's column for two rewards side by side, and shows a dim empty slot for a side with none.
- **Season tag:** skins and classes the pass gives show "Season 1" before their rarity or team, like "Season 1 · Epic · Rifle" or "Season 1 · Defenders" (`Content.BattlePass.SeasonOf`, `SEASON.Tag`; `StoreViews.SkinRarity` and `ClassTeam` in the Inventory, Store and detail pages).
- **Skins in files, like guns and classes:** `Content.Guns.Skins` is now a folder: the `Skins` module, `Definitions` (one ModuleScript per skin, in a folder per WeaponId, 115 skins), `Styles` (shared part styles), and `SkinFinish` and `SeasonSkins` moved in. Requires are `Content.Guns.Skins.Skins`.
- **Menu buttons toggle:** pressing STORE, INVENTORY or BATTLE PASS while that menu is open closes it (the other lobby buttons already did).

### Added

- `Client.Core.LobbyReset`: the Roblox menu's Reset Character button is off while the player is in the lobby (`InLobby`), and on again in a match.

### Tested on a phone screen (Studio device emulator, 749×323)

- The Battle Pass fits: two-reward columns and empty slots read clearly.
- Inventory and Store show the season tag. A season skin's card line is now just "Season 1 · Epic" (`StoreViews.SkinLine`): with the gun added ("Season 1 · Epic · PumpShotgun") it wrapped and was cut off. The skin's name already says the gun; other skins keep "Epic · Rifle".


## 2026-11-16: Data in Definitions folders, Games folder, no RemoteEvents

Tested in a Studio playtest (server and client): every module loads with no errors, and the lists come out in the same order as before. No player data was written.

### Changed

- **One file per entry, like guns.** Each of these is now a Folder holding its module and a `Definitions` folder, one ModuleScript per entry with an `Order` field (lowest first). The module only loads and sorts them; it no longer holds a copy of the data. A file that fails to load, has no Id or repeats an Id is warned about and left out.

    | Before | Module | Definitions |
    | --- | --- | --- |
    | `Content.Classes` + `Content.ClassDefinitions` | `Content.Classes.Classes` | `Content.Classes.Definitions` (17 classes) |
    | `Content.Crates` | `Content.Crates.Crates` | `Content.Crates.Definitions` (8 crates) |
    | `Content.Store` | `Content.Store.Store` | `Content.Store.Definitions` (7 items) |
    | `Content.Consumables` | `Content.Consumables.Consumables` | `Content.Consumables.Definitions` (Grenade, Smoke) |

    - `Content.Store.Style` (new) holds the shared look: `TAG_COLORS`, `COIN_COLOR`, `COIN_ICON`, `BORDERS`. Store items use it; `Store.TAG_COLORS`, `BORDERS` and `COIN_ICON` still work.
    - `Content.Store.Store` and `Content.Consumables.Consumables` keep the `ScribeFragment` tag, so saved data is unchanged.
    - Every `require` was updated.
- **Games folder:** `Content.Siege` and `Content.ClearHouse` are now `Content.Games.Siege` and `Content.Games.ClearHouse`. On the server, `Systems.Siege` became `Systems.Games.Siege` (`SiegeService`, `SiegeMap`, `SpectateService`) and `Systems.Games.ClearHouse.ClearHouse`. `SiegeService`'s optional calls take a dotted folder (`call("Games.Siege", "SpectateService", ...)`).
- The Battle Pass store item's text no longer mentions Battle Stars.

### Removed

- **Every RemoteEvent and RemoteFunction in ReplicatedStorage** (`HologramPose`, `HologramGlitch`, `DeadCallState`, `DeadCallControl`, `DeadCallPhoneRequest`, and the Store's open-many and buy remotes). The scripts use Packets instead:
    - `Packets.Store.OpenMany(crateId, count)`, answered with ok, a message and the results; the Store's Buy now uses `Packets.Store.Buy`.
    - `Packets.Camera.Look`;
    - `Packets.Class.HologramPose`, `Packets.Class.HologramGlitch`;
    - `Packets.DeadCall.State`, `Control`, `Phone` (answered).
- The loose `ServerScriptService.BotCoins` and `ServerScriptService.SecretTeleport` scripts, replaced by modules:
    - `Systems.Store.BotCoinService`: pays `Content.Store.Store.REWARDS.BotKill` (10 Coins) for an NPC kill.
    - `Systems.Lobby.Teleporters`: any part tagged `Teleporter` with a `TeleportTo` attribute (the name of a part in Workspace) sends a player touching it there (1 s cooldown, 3 studs up). TeleportA → TeleportBox and TeleportB → TeleportReturn are set up.


## 2026-11-16: Battle Pass as a level track, and a screen that matches the game

Tested in a Studio playtest; the test data was removed afterwards. See [Battle pass and quests](BATTLE_PASS.md).

### Changed

- **No more Battle Stars or pages.** Every one of the 50 levels has a Free and a Premium reward, claimed once the level is reached (Premium needs the pass). **CLAIM ALL** takes everything claimable. Same rewards overall: 32,850 Coins, the 10 Breach Point skins, 6 classes, 36 crates; the Breach Point Knife is level 50's Premium reward.
- **The Battle Pass screen was rebuilt** to match the Store and Inventory (the same panel, title, X, left nav rail with PASS and QUESTS, section panels and gold highlights), laid out like a tiered Roblox battle pass: a season card with the level bar, the pass summary with GET BATTLE PASS, GIFT and CLAIM ALL, the level track (one column per level, FREE and PREMIUM rows), and the picked reward big on the right with CLAIM.
- The lobby button shows how many rewards wait to be claimed; the XP line at the top uses the game's dark panel and gold.
- `Content.BattlePass`: `TRACK` (from `ROWS`), `Unlocked`, `Totals`; `PAGES`, `StarsAt`, `PageOpen`, `MAX_LEVEL` and `STARS_PER_LEVEL` are gone. `BattlePassService.Claim(player, "ALL")`.

### Added

- `Assets.Models.Charms.BreachPointCharm` (a copy of RocketCharm), so the Breach Point Charm has a model.


## 2026-11-16: Battle Pass and quests

Tested in a Studio playtest with one player; the test data was removed afterwards. See [Battle pass and quests](BATTLE_PASS.md).

### Added

- **Battle Pass, Season 1: Breach Point** (Fortnite-style): XP fills 50 levels (1,500 XP each, bonus levels to 100); each level gives 5 Battle Stars; stars buy rewards on 6 pages (and a bonus page), in any order. Pages open at levels 1, 8, 16, 24, 32 and 40, or when the page before is fully claimed.
    - Rewards: Coins, the new **Breach Point** skins, classes, crates. Free rewards for everyone; the rest need the pass (store item `BattlePassS1`, 399 Robux, giftable: GIFT THE PASS).
    - `Content.BattlePass`, `Systems.BattlePass.BattlePassService`, `Packets.BattlePass`.
- **Quests:** 3 dailies (reset 00:00 UTC, +500 XP for all three), 5 weeklies (reset Tuesday 00:00 UTC), 5 milestones of 5 stages. Counted from matches (kills, guards, wins, damage, builds, plants, scans, abilities) and crates opened; private matches count for nothing. `Content.Quests`, `Systems.BattlePass.QuestService`.
- **Match XP:** 120 per public match, +120 for a win, +15 per kill (10 at most).
- **The screen** `Main.BattlePass` (`Client.Core.BattlePass`): REWARDS and QUESTS tabs, level, XP bar, stars, countdown, GET BATTLE PASS and GIFT THE PASS; the lobby's **BATTLE PASS** button under STORE and INVENTORY; "+XP" and LEVEL UP lines at the top (`Main.PassToast`).
- **Breach Point collection:** 10 skins only from the pass (rifle, pistol, LMG, both shotguns, revolver, knife, phone, shield, charm), recolored from the Afterburn set in an olive, gunmetal and neon-lime palette (`Content.Guns.SeasonSkins`, `SkinFinish` profile `BreachPoint`). The Inventory lists them under "Battle Pass: Season 1"; their page says "Only from the Battle Pass" and links to the pass.
- `StoreGrants.GivePremium(data, season)`; a store item's `Grants.BattlePass`.

### Not done

- The pass's Robux product isn't set up (`Store_BattlePassS1`), so it can't be bought yet.


## 2026-11-15: Guns held further right

Compile-checked only (not playtested).

### Changed

- **The first-person gun sits further right on screen.** Every gun's hip position is moved 0.4 studs to the right of its own `Viewmodel.Offset` by one setting, `Content.Movement.Config.ViewmodelHipShiftRight` (0.4), used by `Client.Guns.Viewmodel`. The rifle (0.42 before) now sits at 0.82, the others at 0.95 to 1.1. Melee tools move with it.
- Aiming down sights is not moved: the sights still line up in the middle. Raise or lower `ViewmodelHipShiftRight` to taste; 0 is the old look.


## 2026-11-15: Inventory search

Compile-checked only (not playtested, as asked).

### Added

- **A search box in the Inventory** (`Main.Inventory.Search`, built in Studio: a magnifier icon, the text box `Input`, and an X `Clear` button that shows while there is text), at the right end of the filter chips (the chip row is 236 px narrower for it).
    - Fixed the same day: the box was drawn under the Inventory panel (ZIndex 1 against the panel's 12), so it didn't show. It is now 13, its parts 14 and X 15.
    - The magnifier is an image from the Creator Store ("Search Icon Round", decal 85365761530931, image `rbxassetid://139935609048710`), tinted light grey, instead of an emoji.
    - Typing narrows the open tab (Classes, Skins or Crates) to the cards whose name, subtitle or lock hint holds every word typed, in any case: "gilded rifle", "mythic", "shield crate", "defenders".
    - It works on top of the chip filter, and stays when the tab changes.
    - While searching, the section headings give way to one `RESULTS FOR "..."` heading; with no card left the status line says "No matches. Try another word, or clear the search."
    - The outline lights up while the box is focused. Tooltips on the box and on X.


## 2026-11-15: Class files moved up, face-on shields and phones, still items on the detail page

Tested in a Studio playtest: on the Starter Bundle page the whole bundle turned, Crimson Tide turned when picked, 2,000 Coins showed the coin picture and its description (still), and picking it again went back to the bundle.

### Changed

- **Class files are in `Content.ClassDefinitions`** (a folder right under Content, like `Content.Guns.Definitions`), not inside the `Content.Classes` module.
    - `Content.Classes` had its whole class list back in it (most likely an open script editor saved an older copy over the change). The files were made again from that list, which is the newest: 16 matched, and Leo's Id is now `Motion_Scanner` (renamed in that list).
    - `Content.Classes` now only loads `Content.ClassDefinitions` and answers questions (`Get`, `ForTeam`, `Allows`...). Its header says to edit classes in the folder. Checked: 17 classes in the same order.
    - **Anyone with `Content.Classes` open in a script editor should close it without saving**, or the old list comes back again.
- **Shields and phones face the viewer** in every preview (cards, detail page, rows): a shield shows its plated front, a phone its screen (`FACE_ON` in `ItemDetails`). Spinning starts from the front.
- **Things that aren't models work like guns on the detail page:** Coins (the coin picture), crates (📦) and pass perks (like x2) in a bundle or pass can be clicked: the big picture, their name and their own description show, under the bundle's title, without turning. Rows show their picture in a new `Icon` / `IconGlyph` slot of `Templates.ContentRow`. `Row.Image` and `Row.Glyph`.

### Fixed

- **The Inventory timed out the client when data loaded while it was open.** It watched every skin's count and redrew all 100+ cards (with 3D previews) once per change, over 100 times in a row. Changes now cause one redraw at the end of the frame (`refresh` is deferred).


## 2026-11-15: Spinning previews, bundle item previews, tooltips

Tested in a Studio playtest: a hovered Inventory card turned and showed its tooltip; the Obsidian Pack page turned its gun, and clicking an item row showed that item (title kept). Going back to the whole bundle by clicking the row again was not checked (someone else was using the playtest).

### Added

- **Previews turn.**
    - Inventory and Store cards: the gun turns while the pointer is on the card, one card at a time (`ItemDetails.Hover`).
    - The detail page: the gun turns the whole time the page is open (`ItemDetails.Spin`).
- **Bundle items on the detail page.** A row with a preview (a bundle's or pass's items, a crate's skins, a class's guns) can be clicked:
    - the big preview shows that item, turning;
    - the subtitle shows its name and kind, and the description its own description (`Row.Description`, filled from skins and classes);
    - the title stays the bundle's, crate's or pass's;
    - the row is outlined; clicking it again shows the whole bundle again.
    - Template `ContentRow` got a transparent `Select` button and a `Selected` outline.
- **Tooltips.** `Main.Tooltip` (built in Studio) and `Client.Core.Tooltip` (ClientOnly): resting the mouse 0.35 s on an element with a `Tooltip` attribute (on it or an ancestor) shows a small box by the pointer. Mouse only.
    - Set in Studio: the lobby bar (PLAY, PARTY, MODE, PLAY WITH PARTY), STORE and INVENTORY, Settings, the Coins chip, the detail page's BACK, EXIT, GIFT, Coins and Robux, and the Store, Inventory, Modes and Party close buttons.
    - Set in code (`Tooltip.Set`): Inventory and Store cards (name, kind, where it comes from, "Click for details"), Game Modes cards, and detail page rows.


## 2026-11-15: One file per class

Checked in Studio without a playtest (as asked): every file compiles, and the new class list was compared field by field with the old one.

### Changed

- **Classes are separate files, like guns.** Each class is a ModuleScript in `Content.Classes.Definitions` (17 files, named by class Id: `Breacher`, `Hacker`, `Motion Scanner`, ...), returning that class's table with its comments.
    - New field `Order`: the class's place in the menu. `Content.Classes` loads every file once and sorts by `Order`, then `Name`, so the menu order is the same as before.
    - A file that fails to load, has no `Id`, or repeats an `Id` is warned about and skipped.
    - `Content.Classes` keeps its API (`List`, `Get`, `ForTeam`, `CategoryOf`, `Allows`, `Choices`, `GunCategories`, `HIDDEN`), so nothing that uses it changed.
    - The old list's shared `SIDEARM`, `ACTION` and `PREP_AND_ACTION` tables are now declared at the top of each file that uses them.
    - Checked: same 17 classes in the same order with the same fields. The one difference is Leo's (`Motion Scanner`) ability description, which someone edited in Studio during the move; its latest text is in `Definitions.Motion Scanner`.
- Space-indented classes (Caleb, Wren, Tiffany, Blake) were reindented with tabs.


## 2026-11-15: Prep drone, leavers, boards, guards, messages, health bars

### Fixed

- **The prep drone couldn't be driven.** Only what is within `StreamingTargetRadius` (1024 studs) of a player's body streams in to their client, and during Prep the attacker's body waited at the lobby, about 1300 studs from Mansion and Bank. The drone is driven by the client, so it wasn't there to drive, or fell through a floor that hadn't loaded yet.
    - In Prep the attacker's body now waits `PREP_HOLD_HEIGHT` (120) studs above their spawn: invisible, anchored, can't be touched, hit by rays or hurt (a hidden ForceField), no name, no weapons (`holdAt` in SiegeService). Action gives a new body at the spawn as before.
    - The drone is handed over only after `Player:RequestStreamAroundAsync` around the spawn (up to `PREP_STREAM_WAIT`, 6 s), so the floor is there first.
    - Tested: the hidden body sat 120 studs above the Bank spawn, invisible and anchored. Before the stream wait, the client's drone had fallen to Y -500. With the wait in place, a full Prep wasn't run again (the test player's data kept failing to load), so driving is **not yet confirmed**.
- **A match went on after a side left, and could say the remaining side lost.**
    - The round's winning group was read from the roster, which still held players who had left, with the team of the round they left in. After a side swap that is the other side's team, so the side that left could be credited.
    - Each round's "a side left" check used that round's starting count, so a side that left during RoundEnd started the next round with 0 players and the check never fired.
    - Now: the winning group is the group playing the winning team this round (`teamOfGroup`). Each side group's size at the start of the match (`groupStart`) is kept; a group with nobody left loses the match at once, in any phase from Selection to Action, and `nextRound` checks right away. A side that left forfeits the match whatever the score.
    - Not tested with real players (needs two).
- **Bullets stopped in some broken doorways and windows (Bank).** Bank's bomb-room volumes (`Sites`, up to 68 studs across) and both maps' spawn markers were invisible and walk-through but could still be hit by rays. Bullets stopped on them once the boards were down.
    - Those parts are now `CanQuery`/`CanTouch` off in both maps (30 parts), and `SiegeMap.Load` makes sure of it for every map.
    - Tested: Mansion 32 and Bank 47 boards broken, then shot through: Bank blocked 9 before, 0 after.

### Changed

- **Lobby messages are colored by kind:** red for refusals, green when it went through (a private match starting), yellow for news (PLAY switched mode, "your party leader picks the mode"). The Party menu's line too. The Store's and item page's line under the buttons: green when a purchase went through, red when refused. `ItemDetails.SetStatus(text, color?)`.
- **No health bars over other players.** Names stay; NPCs keep their bars (`Client.Hud.HealthBillboards`).
- **Siege "Built" counts whole doors and windows,** not planks: only the piece that completes a board counts (and reinforced walls, as before). The MASTER BUILDER card and BUILT column use it.
- **Clear House guards:**
    - **Roam their room:** a new patrol spot is at least 45% of the room's size away when possible (`GUARD_SPREAD`), and they stand 0.6 to 1.8 s between walks (was 1.5 to 4). Tested with a player nearby (guards sleep beyond 350 studs): 61 to 228 studs walked in 24 s, covering most of each room.
    - **No Grenadier:** `PROFILES = { Soldier = 3, Breacher = 1 }`.
    - **Count:** `ROOM_SHARE` 2/3, one guard per room first, so at least 2/3 of the rooms hold one (maps with no hand-made spawn rooms).
    - The indoor check no longer needs a bomb room (`Sites`); a map's `NPCIndoorVolumes`, when it has them, still bound the guards.
    - Mansion and Bank now have hand-made `ClearHouseSpawnRooms` and `NPCIndoorVolumes` (14 each) and floor **waves** (Main 6, Upstairs 4, Basement 6; 16 guards, the next floor after the last is cleared). Those were added by another developer and are not changed here; with waves only one floor holds guards at a time.


## 2026-11-15: Party-size popup

Tested in a Studio playtest: with a party of 3, pressing 1v1 opened the popup, nothing was picked, and the description line kept the mode's own text.

### Changed

- **"Party too big" is a popup now**, not text in the Game Modes panel's description line. The description always shows the mode's own description.
    - Pressing a greyed-out mode or category: PARTY TOO BIG popup, "Your party of N is too big for X. Pick a different mode." Nothing is picked.
    - Picking a PRIVATE ONLY mode: a PRIVATE ONLY popup says what PLAY and PLAY WITH PARTY will play (a notify sound, not an error).
    - PLAY or PLAY WITH PARTY with no mode that fits, the server's own size refusal, and a party growing too big for every mode of the category also open the popup.
    - The note under the bar when the party's size switches PLAY stays as it was.

### Added

- `Main.Notice` (built in Studio, in the PartyInvite style): Title, Text and an OK button, centered above menus.
- `Client.Core.Notice` (ClientOnly): `Notice.Show(title, text, sound?)` and `Notice.Hide()`.


## 2026-11-15: Private matches in the picked mode, modes by party size

Tested in a Studio playtest with one player and a party faked from the server (2, 3 and 1 members). No result was saved (the playtest was stopped during Selection).

### Changed

- **PLAY WITH PARTY plays the picked mode.** A private 1v1, 5v5 or Clear House instead of a fixed "Private" Siege match.
    - The record's `Mode` is the mode's Id, with `Private = true`. So a private Clear House is Clear House (map vote, guards), and rounds come from `Content.Siege.ROUNDS` for the mode.
    - Teams: dealt evenly as before; in a mode with no defenders (Clear House) everyone attacks.
    - Results still count under `Mode:Private` / `Category:Private` (`StatsService`), never the public mode's stats.
- **Party size picks the mode.** Each mode has two limits:
    - queue (PLAY): `PartyLimit` (1v1: 1, 5v5: 5, Clear House: 5);
    - private (PLAY WITH PARTY): `PrivateLimit`, both sides together, at most 5 (1v1: 2, 5v5: 5, Clear House: 5).

    PLAY and PLAY WITH PARTY each use the picked mode when the party fits, else the mode of the same category with the smallest limit that fits (`Content.Matchmaking.FitMode`). With 1v1 picked: 2 players queue 5v5 while the private match stays 1v1; a third makes the private match 5v5 too; back to 1, it is 1v1 again. Arcade works the same way.
- **The bar says so:** PLAY's line shows the mode it queues for, PLAY WITH PARTY shows "PRIVATE 1 V 1 · 2 PLAYERS", and a line under the bar says when the party's size switched either one ("Party of 2: PLAY now queues for 5 V 5.").
- **Game Modes panel:** a mode the party is too big for, even privately, is greyed out, says PARTY TOO BIG and can't be picked. A mode the party fits only privately says PRIVATE ONLY. (The explanations moved to a popup later the same day.) A category with no mode that fits is greyed out too.
- **Too big:** if no mode of the category fits, PLAY and PLAY WITH PARTY say "Your party is too big for X. Pick a different mode." The server checks the same limits.

### Added

- `Content.Matchmaking.PrivateLimit(mode)`, `FitMode(modeId, size, private)`, `MatchRecord.Private`.
- `QueueService.JoinPrivate(player, modeId)`; the `Private` request carries the mode's Id.
- `ModeMenu.SetPartySize(size)`.


## 2026-11-15: Bundles Robux only, new bundle and pass contents reach owners

Tested in a Studio playtest: Coins purchases of bundles and the VIP pass were refused with no Coins taken, and the new grant helpers were checked on fake data. No player data was changed.

### Changed

- **Bundles and game passes are Robux only.**
    - `StoreService` refuses Coins for any item in the `Bundles` section or marked `Pass`, whatever its data says.
    - The Obsidian Pack lost its 3,000 Coins price (149 Robux, as before).
    - The Neon Circuit Bundle is 149 Robux. It reuses the old "50 Siege Tokens" product (3731060058), renamed through Open Cloud to "Neon Circuit Bundle" at 149 Robux with a new icon, as `Store_NeonCircuitBundle` in `Shared.ProductIds`. Checked in a playtest: purchasable, and Roblox reports the new name and price.
    - `DAILY_DEALS`: the Obsidian Pack was replaced by `Crate:Eclipse`, since a deal only lowers Coins prices.

### Added

- **New contents reach owners.** When skins or classes are added to a bundle's or game pass's `Grants`, players who own it get them the next time they join.
    - Bundles (`backfillOwned` in `StoreService`): owned means recorded in `OwnedItems` or found in the purchase log (`Item:<Id>`, `<Id>` or `Store_<Id>`), not "has every skin", so a bundle with a new skin still counts as bought.
    - Game passes (`PassCosmetics`): every `Pass` item now, not only VIP. Also right after a pass is bought.
    - Only skins and classes are given again. Coins and crates in `Grants` are given once, at purchase.
    - New `StoreGrants.Missing(data, grants)` and `StoreGrants.ApplyLasting(data, grants)`.


## 2026-11-15: Siege Tokens removed, crate contents rows, Clear House end screen and guard count

Tested in a Studio playtest (server and client). No player data was written.

### Removed

- **Siege Tokens** are gone as a currency. Coins are the only one.
    - No crate or store item has a Tokens price; the three token packs (`Tokens50`, `Tokens150`, `Tokens400`) are no longer sold. Their product ids were taken out of `Shared.ProductIds`; turn the products off on the Creator Dashboard. (Later that day the Tokens50 product became the Neon Circuit Bundle.)
    - The Starter Bundle no longer grants 25 Tokens (its text was updated).
    - Bundles that had a Tokens price were first given Coins prices; later the same day bundles became Robux only (see above).
    - `StoreService` refuses Tokens: `CURRENCIES = { Coins = true }`, for buying and for `Give`.
    - The Tokens chips are hidden in `Main.Wallet`, the Store and Inventory headers, and the detail page's Tokens button.
    - The saved `Tokens` field stays (unused) so old saves still load.

### Fixed

- **Crate contents rows overlapped** (`Templates.ContentRow`): long names ran under the odds, and the detail ran under OWNED.
    - The name and detail now end 130 px before the right edge.
    - The odds and OWNED are 50 px wide.
    - The detail is 12 px and cut off with "…"; the name shrinks to fit (10 px at least) and is cut off below that.

### Changed

- **Clear House end screen:** the guards' stats are no longer shown. The server sends only the players' rows, and the client shows only YOUR TEAM (no HOUSE GUARDS column).
- **Clear House guard count:** every room the finder found counts, not only the rooms with indoor guard spots. Guards = half the rooms (rounded up) + 2 for each player after the first.
    - Guards still stand only on indoor spots (`NPCIndoorVolumes` or `Sites` volumes, with a ceiling and walls around). Mansion has 7 such rooms of 26, Bank 6 of 29.
    - Rooms fill up to `MAX_PER_ROOM` first; if guards are left over, any free indoor spot is used. A warning is printed if the spots run out.
    - Tested: Mansion 13 guards for 1 player and 21 for 5; Bank 15 and 23. All of them indoors.
