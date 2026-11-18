# Changelog

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

Tested in a Studio playtest with saving off (the new `ScribeNoSave` switch). See [TUTORIAL.md](TUTORIAL.md).

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
- Both now replace Roblox's walk animation instead of adding to it, which had lifted the crawling legs off the floor. See [MOVEMENT.md](MOVEMENT.md).

## 2026-11-17: Prone and slide animations

- **Prone:** a lying animation (breathing; forearms propped up when no gun is out) and a crawl animation that runs with the crawl speed (legs sweep out in turn, the body rolls, the arms pull when no gun is out). **Slide:** leans back further as it settles, with a wobble, and the trailing hand reaches for the floor when no gun is out. All made in code in `Client.Movement.MovementPoses`, seen by everyone. See [MOVEMENT.md](MOVEMENT.md).

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

Our own take on what Rainbow Six Siege's screens do well, in SiegeBlox's look: dark navy panels, gold for "you" and "next", the team's color for your side and red for the enemy, rounded blocky shapes with a little "stud" on class emblems, and Fredoka One everywhere. Tested in Studio playtests with bots on Mansion and Bank, at 1920 wide and at a narrow 919 wide (see [UI.md](UI.md#siege-ui-pass-2026-11-17)). The only player data written was the gadget pick (Frag grenade to Smoke bomb and back again).

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

Tested in Studio playtests: private matches of one admin player and four bots on Bank and Mansion (see [SIEGE_BOTS.md](SIEGE_BOTS.md#drones-memory-and-breaking-in-2026-11-16)). No player data was written. One run was cut short when Studio lost its connection to Roblox (DataStore and asset requests timed out and the server kicked the player: "We couldn't load your data").

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

Tested in Studio playtests with attacker bots sent from the attacker spawns to the bomb rooms of both maps, boards up (results in [SIEGE_BOTS.md](SIEGE_BOTS.md#getting-to-the-bomb-rooms-2026-11-16-studio-boards-up-no-defenders)). No player data was written.

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

Tested in Studio playtests with one admin player and three bots (see [SIEGE_BOTS.md](SIEGE_BOTS.md#tested-2026-11-16-studio-playtests-one-admin-player)). No player data was written.

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

Tested in a Studio playtest (server and client). The test claim was undone (Coins back to 308, XP 0, no claims, the crate taken back). See [BATTLE_PASS.md](BATTLE_PASS.md).

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

Tested in a Studio playtest; the test data was removed afterwards. See [BATTLE_PASS.md](BATTLE_PASS.md).

### Changed

- **No more Battle Stars or pages.** Every one of the 50 levels has a Free and a Premium reward, claimed once the level is reached (Premium needs the pass). **CLAIM ALL** takes everything claimable. Same rewards overall: 32,850 Coins, the 10 Breach Point skins, 6 classes, 36 crates; the Breach Point Knife is level 50's Premium reward.
- **The Battle Pass screen was rebuilt** to match the Store and Inventory (the same panel, title, X, left nav rail with PASS and QUESTS, section panels and gold highlights), laid out like a tiered Roblox battle pass: a season card with the level bar, the pass summary with GET BATTLE PASS, GIFT and CLAIM ALL, the level track (one column per level, FREE and PREMIUM rows), and the picked reward big on the right with CLAIM.
- The lobby button shows how many rewards wait to be claimed; the XP line at the top uses the game's dark panel and gold.
- `Content.BattlePass`: `TRACK` (from `ROWS`), `Unlocked`, `Totals`; `PAGES`, `StarsAt`, `PageOpen`, `MAX_LEVEL` and `STARS_PER_LEVEL` are gone. `BattlePassService.Claim(player, "ALL")`.

### Added

- `Assets.Models.Charms.BreachPointCharm` (a copy of RocketCharm), so the Breach Point Charm has a model.

## 2026-11-16: Battle Pass and quests

Tested in a Studio playtest with one player; the test data was removed afterwards. See [BATTLE_PASS.md](BATTLE_PASS.md).

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

## 2026-11-14: Clear House map vote, no prep, guards by room count

Tested in Studio with one player: map vote, Reveal straight to Action, 15 guards on Bank. The test loss was removed from the saved data afterwards.

### Changed

- **Map vote:** Clear House's Selection starts with a vote between the mode's maps, now Mansion and Bank.
  - The map with the most votes is played; a tie is drawn among the tied maps.
  - The map loads when Selection ends. Each player is then given a random free attacker spawn, since spawns belong to a map.
- **Classes:** the attackers' classes, as before.
- **No prep phase:** Reveal goes straight to Action. The doors and windows are boarded, the rooms found and the guards placed while Reveal runs.
- **Guards:** half the map's rooms, rounded up (`ROOM_SHARE` 0.5), plus 2 for each player after the first. No upper limit besides 3 a room. Mansion (26 rooms): 13 to 21. Bank (29 rooms): 15 to 23.
- `Content.ClearHouse`: `PREP_TIME`, `BASE_GUARDS`, `MAX_GUARDS` and `TEXT.Prep` removed; `ROOM_SHARE` added.
- New Siege pick `"Map"` (Clear House only); the snapshot's `Maps` (`{ Name, Votes }`) during Clear House Selection.

## 2026-11-14: Arcade category, Clear House mode

Tested in Studio with one player: a win (guards killed from a test script) and a loss. See [CLEAR_HOUSE.md](CLEAR_HOUSE.md). Both test results were removed from the saved data afterwards.

### Added

- **ARCADE category** in the Game Modes panel, with one mode, **CLEAR HOUSE**:
  - up to 5 players against NPC guards in the Mansion;
  - every door and window boarded up;
  - no bombs, one round.
- **The match:** Selection (spawn and class), Reveal, a 30 s drone Prep while the guards take their rooms, then Action.
  - The players win when every guard is dead.
  - They lose when every player is dead or has left, or after 8 minutes.
- **Room finder** (`Systems.Siege.ClearHouse`): a grid flood fill over the map's floors, with walls, doors and windows as dividers, builds an `NPCRoom` box per room. A map may give hand-drawn rooms in a `Rooms` folder instead.
- **Guards:**
  - 6 for one player, plus 2 for each other player, up to 16, spread over random rooms (big rooms more often, at most 3 a room);
  - Soldier, Breacher or Grenadier;
  - in Guard mode, so each one stays in, patrols and re-boards its room;
  - no respawns.
- **Wins** are saved under `Mode:ClearHouse` and `Category:Arcade`, apart from Siege's stats. The overall Wins/Losses totals still count them.
- `Content.ClearHouse`; `Content.Matchmaking.PartyLimit(mode)`; the mode fields `Kind` and `Maps`; `Content.Siege.ROUNDS.ClearHouse = 1` and the reasons `HouseCleared` / `HouseHeld`.

### Changed

- **Queue:** a party may be as large as the only side of a mode whose other side is empty (5 for Clear House). It was the smaller side, which would have been 0.
- **Maps:** a mode with `Maps` only uses those maps.
- `NPCService.Spawn(profileId, where, spawnPart?, ignoreCap?)`: the new `ignoreCap` passes the `MAX_NPCS` cap, which is 0 today.
- **Siege screens in Clear House:**
  - the roster's enemy section reads HOUSE GUARDS;
  - the HUD objective counts the guards left, and the bomb chips are hidden;
  - the result screen shows "x / y guards down" and a HOUSE GUARDS column.

## 2026-11-14: Shotgun loadouts use PumpShotgun

Studio playtest: `GunService.Give(player, "PumpShotgun")` gave the gun with no warning, and every gun id in the class, lobby and NPC loadouts now has a definition.

### Fixed

- **The shotgun was never given.** The pump shotgun's definition id is `PumpShotgun`, but loadouts still asked for the old id `Shotgun`, so `GunService.Give` warned "no gun named Shotgun" and the player got nothing. Now `PumpShotgun` in:
  - `Content.Classes` loadouts: Breacher (Mason), Hacker (Caleb), and the two other classes that carried it;
  - `Content.Guns.Loadouts`: Breacher, Arsenal, Sprayer;
  - `Content.NPC.Profiles.Breacher`;
  - the per-gun settings in `Content.Guns.Melee` and `Content.Destruction.SoftWallConfig`, so its melee and wall holes apply again.
- The `"Shotgun"` entries in class `Categories` are the category name and stay as they are.

## 2026-11-14: Analytics, crate opening on phones

Studio playtest of a 1v1 up to the end of round 1. Every event logged up to there was printed with the right fields (see [ANALYTICS.md](ANALYTICS.md)). The crate opening screen was not seen on a phone.

### Added

- **Analytics** (`Systems.Analytics.AnalyticsService`, `Content.Analytics`, `Client.Core.AnalyticsClient`, `Packets.Analytics.MenuOpened`):
  - economy events for Coins and Tokens;
  - Queue and Match funnels, and an onboarding funnel;
  - LobbyVisit and SiegeMatch journeys, which must be created on the Creator Hub;
  - 23 custom events, covering:
    - queue drop-offs and waits;
    - top modes, classes, sites and spawns;
    - which side wins rounds and how long rounds last;
    - kills, deaths, damage and builds per player per match, by mode, category and result;
    - leaving early, weapons, abilities, menus and purchases.
- **New extension points for analytics:**
  - `Siege.SelectionEnded(summary)`: every player's final picks each round, with `Random` set when the class was filled in;
  - `Siege.RoundEnded` gets a 4th argument: mode, map, site and `Final`. At the end of a match it now also fires for the last round;
  - `Siege.Ended` gets a 3rd argument: the match summary, with every player's kills, deaths, damage, builds, side and result;
  - `Store.Bought` gets a 5th argument: the price paid.

### Fixed

- **Crate opening on phones:** the OPEN MORE and DONE buttons were below the bottom of the screen. `Main.Opening` now has a FitScale (design height 460, full width), so the reel and its buttons shrink to fit. The reel's width is read in design pixels, so the won skin still lands under the marker.
- `Content.Store` had been rolled back to an earlier version, losing the `OwnedItems` saved field (bundle purchases would have errored on the server) and the ⚔ Classes icon. Both are back.

## 2026-11-13: Mobile pass for the Store, Inventory, Details and match result

Compile-checked. Desktop checked in a playtest: the Store is unchanged (1180×700, scale 1), and the health bar is hidden in the lobby. **Not yet checked at phone size.**

### Changed

- **The Store, Inventory and Details panels are fitted menus.**
  - Each has a `Fit` UIScale tagged `FitScale`, with `DesignHeight` 640 and `WidthShare` 0.95. On a phone they shrink as a whole instead of cutting cards off.
  - The `Feel` UIScale on these panels was removed (only one UIScale works per frame), so they no longer pop when opened.
- **FitScale changes** (`Client.Core.UI`):
  - a `MinScale` attribute;
  - `FitMode = "Dialog"`: a box built in pixels keeps its size and place and is scaled down to fit the screen both ways.
  - The gift picker and the match result's `Body` (now a 1150×680 pixel box) use it.
- **Cards per row** in the Store (2 to 5) and Inventory (2 to 6) come from the page's width, so cards keep their shape on any screen.
- **Inventory filter chips:** the row scrolls sideways when they don't fit, and gun names are spaced (PUMP SHOTGUN).
- **Lobby wallet panel:** on screens 600 px tall or less it is scaled to 0.72 and sits in the top-left corner, clear of PARTY, PLAY and MODE.
- **Health bar:** hidden while in the lobby (`InLobby`).

### Fixed

- Close buttons were blank squares on phones: the ✕ glyph doesn't draw there and is now X.
- The Classes tab icon (🪖) doesn't draw on phones and is now ⚔.

## 2026-11-13: Prep drone frozen by streaming (found in a playtest)

Playtested in Studio, one player, a 1v1 as the attacker:
- **Before the fix:** in Prep the drone view showed, but the drone didn't move. Its velocity read -37 down while its position never changed, only 1 map part had loaded near it on the client, and the server had the player's `ReplicationFocus` at nil.
- **After the fix:** 36 parts had loaded around the drone at once, holding W drove it 30 studs during Prep (clock at 00:23), no viewmodel was drawn, and there were no new errors.

### Fixed

- **The prep drone was frozen.** The place uses `StreamingIntegrityMode.PauseOutsideLoadedArea`, so a client-owned part outside the loaded area has its physics paused. In Prep the body waits in the lobby, so the area around the drone is only loaded if the player's `ReplicationFocus` is on the drone. It was set when the drone was placed but found cleared later (respawning the body was tested and is not what clears it). This is why drones worked in Action, with the body nearby, and not in Prep.
  - `DroneService` now sets the focus again every check (0.25 s) for every held player, and after their body spawns.
  - `focusOn` only writes the focus when it changes.

## 2026-11-13: Owned Store cards show an OWNED button

Compile-checked only.

### Changed

- **Store cards:** anything the player owns (a game pass, a bundle or other product, a skin, a class, a crate whose skins are all owned) shows a green ✓ OWNED button where the prices were. The Coins, Tokens and Robux buttons are not shown to an owner. A giftable item keeps its gift button at the right of the row. This replaces the greyed prices on owned cards from earlier today.
- **Detail page (unchanged from earlier today):** an owned item shows ✓ OWNED, and its Coins, Tokens and Robux buttons greyed and unclickable.

## 2026-11-13: Prep drone drives, no gun over the drone view

Compile-checked only (not playtested).

### Fixed

- **The gun viewmodel showed over the drone view in Prep.** The server arms the attacker's lobby body when it spawns, after the drone view has opened, and equipping a gun resets the viewmodel's hidden flag. While in a drone, `DroneController` now hides it again on every frame.
- **The prep drone didn't move.**
  - The drive input came only from the default controls, which give no movement while the body is parked (and its controls are off) in the lobby. When they report nothing, the keyboard (WASD) and the gamepad's left stick are now read directly.
  - When a player starts looking through a drone (`Packets.Drone.View`), the server gives them network ownership of their landed drones again, so a body spawning or a short take-back can't leave the drone stuck under server physics.

## 2026-11-13: OWNED for passes and bundles, greyed prices on the detail page

Compile-checked only.

### Added

- **`OwnedItems`** (saved, in `Content.Store`): once-only store items bought, by item Id.
  - `StoreGrants.ApplyItem(data, item)` gives an item's grants and records it. Robux receipts (`Shared.Data`) and Coins/Tokens purchases (`StoreService`) both use it.
  - Bundles bought before this are found in the purchase log when the player joins (`backfillOwned` in `StoreService`), or on their next purchase try, and recorded.
- `StoreViews.Owns(data, "Item", id)` tells whether a store item is owned:
  - a game pass, from Scribe's client pass mirror (`Data.Owns`);
  - a once-only item, from `OwnedItems`, or when everything it grants is owned.

### Changed

- **Store cards:** owned game passes and bundles now show ✓ OWNED with greyed prices, like skins and classes. Before, they showed OWNED only after the server refused a second purchase.
- **Detail page:** an owned item or class shows a green ✓ OWNED button, with its price buttons still there but greyed and unclickable. Gifting stays available.
- The open detail page redraws when the player's data changes, and about 1 s and 3 s after a game pass purchase, so it turns to OWNED right away.

## 2026-11-13: Developer skin pack

Compile-checked only. In Edit mode `Skins.Apply` was run on the Rifle, Pistol and SMG models: 35, 6 and 3+ rainbow parts were tagged, and putting the normal look back cleared every one.

### Added

- **Developer pack:** `DevRifle`, `DevPistol` and `DevSMG` in `Content.Guns.Skins`:
  - black guns;
  - neon rainbow parts (magazine, sights, rifle handguard);
  - rainbow lines down both sides, cut into 0.2-stud pieces;
  - the colors run along the gun as a moving gradient.
  - **Not for sale:** never in a crate or the Store, and hidden in the Inventory from players who don't own them.
- **Rainbow skins** (any skin can use them):
  - a skin's `Rainbow` list of part-name patterns, and `Rainbow = true` on a Detail, make those parts Neon and tag them `SkinRainbow`, with a `RainbowOffset`;
  - `Client.Guns.SkinRainbow` turns their colors every frame;
  - the settings are in `Skins.RAINBOW`: Speed, Length, Saturation, Value, Piece.
- **Skin cards:** a skin's `Card` sets its Inventory card: background colors and a `BORDERS` preset. The Developer skins have black cards with the moving Rainbow border.
- **Commands (admins only, Cmdr):**
  - `givedevskins <players>` (alias `devskins`) gives the pack for good (saved in `WeaponSkins`);
  - `takedevskins <players>` takes it back and unequips it.
  - Both go through `StoreService.GiveSkins(player, skinIds, take?)` and `StoreService.DeveloperSkins()`.
- **SMG skin family:** `SMG` and `SiegeSMG` share one (`SMGSkin` saved field), so the Inventory gets an SMG tab.

## 2026-11-13: Prep drone streaming restored, reinforce counts as building, Store card fixes

Compile-checked only (a playtest was not allowed this time).

### Fixed

- **The prep drone still wasn't viewable.** The earlier streaming fix had been lost from `DroneService`, and the drone template was back to `ModelStreamingMode.Default`, so the drone at the attacker spawn never reached a client whose body waits in the lobby. Restored and made sturdier:
  - every placed drone is `Persistent`, and so is the template;
  - while a player is held in their drone, `focusOn` points their `ReplicationFocus` at it, and clears it when the hold ends or the drone is cleared;
  - the client goes into the drone as soon as one of its drones is there, without needing a body.
- **End screen outlines were cut off.**
  - A player's row outline was clipped by the rows list; it now has 3 px padding.
  - The team columns and MVP cards have room for their edges.
  - The totals now read KILLS, DAMAGE, BUILT in that order.
- **Reinforce was silent for others.** Its sound part now sits in a `Persistent` model, so with streaming on it reaches everyone before the short sound ends. The player who reinforces also hears a local lock-in sound (`BoardPlace` and `FootstepMetal`, in `SiegeHud`).
- **Daily deal text was covered.** The struck-through old price and the detail line now sit just above the price buttons (anchored to the bottom), with a slightly smaller picture.

### Changed

- **A reinforced wall counts as building** (`Classes.Reinforced`, fired by `Abilities.Reinforce`), so it adds to Built and to MASTER BUILDER.
- **Owned Store items** keep their price buttons, greyed and unclickable, under a green ✓ OWNED line. Gifting still works.
- **The % EXTRA tag** is brighter red, not tilted, and sits on the top-left edge of the card, level with the deal tag on the right.

## 2026-11-13: Store coin buttons, OWNED cards, skin tabs per gun

Compile-checked only.

### Fixed

- **The coin icon covered the amount** on Store price buttons, the item page's coin button and the lobby wallet chip. Each now has a `Content` row (`CoinIcon`, then an `Amount` label) laid out side by side, and the code writes the amount there (`setMoneyText` in `Client.Core.Store` and `ItemDetails`).
- **OWNED covered the struck-through old price** on discounted cards the player owns. The old price is hidden once the item is owned.
- **Inventory skin tabs** only offered Rifle and Pistol. There is now a chip for every gun with skins (`Skins.Weapons()`), so LMG shows up, and any gun given skins later gets its own tab.

## 2026-11-13: Siege rounds, match result screen, lobby leaderboard, map music

Compile-checked only (not playtested, as asked).

### Added

- **Siege matches have several rounds**, and the sides swap every round:
  - `1v1` and private matches: best of 3.
  - `5v5`: best of 5.
  - Set in `Content.Siege.ROUNDS` (`DEFAULT_ROUNDS` 3).
- **Between rounds** (new phase `RoundEnd`, `ROUND_END_TIME` 8 s), the next round starts like this:
  - The map is rebuilt from a fresh copy, so boards, walls and broken pieces are whole again.
  - Bombs, defusers, drones and cameras are cleared.
  - Every player is put on their new side and goes through Selection again: class, spawn or site vote, and loadout.
- **The match winner** is the side that won the most rounds, not the side that won the last one:
  - The match stops early once one side has a majority.
  - It also stops early when a side has left (`MATCH_ENDING_REASONS`).
  - Rewards and stats are recorded once, at the end of the match.
- **Round result banner** (`Main.RoundResult`): ROUND WON / LOST / DRAW, the reason, the score (you vs them), a pip per round, and the next round.
- **Match result screen** (`Main.MatchResult`), revealed in stages with count-ups:
  - VICTORY / DEFEAT / DRAW over a green or red tint, with the round score.
  - MVP cards with avatars: TOP FRAGGER (kills), MOST DAMAGE, MASTER BUILDER (pieces repaired).
  - Both teams side by side, each with its totals and every player's K, D, damage and builds. Your row is outlined, and the winning column gets a gold edge and a WINNER tag.
  - Templates: `RoundPip`, `MvpCard`, `TeamColumn`, `ResultRow`.
- **Per-match stats** on the server: kills, deaths, damage dealt to the other side (Prep and Action) and pieces built (`Breakable.Repaired`).
- **Lobby leaderboard:** in the lobby, Tab (the Scoreboard key) shows everyone on the server ranked by total wins, highest first, with rank (#1 gold, #2 silver, #3 bronze) and win streak. The wins come from the new `TotalWins` player attribute, set by `StatsService`.
- **Per-map background music:** a folder in `Assets.Music` (or `Assets.Music.Primary`) named like the active Siege map is played instead of the normal background songs during that match.

### Changed

- **Siege class picking:** classes for sale that the player doesn't own are greyed out, marked LOCKED, and listed after the ones they can pick.
- **Inventory:** a skin sold by a store item with a `Border` or `Glow` (the Obsidian Pack) shows that item's moving border and sheen on its card, as in the Store.
- `Combat.Hit` now also passes the damage dealt (0 when blocked) and the item.

### Fixed

- **The prep drone view was lost when the body spawned.**
  - In Prep the attacker's body loads in the lobby a moment after the drone view opens, and the client left the drone whenever a new body arrived.
  - A player held in their drone now stays in it: the new body is anchored where it is, and drone control is asked for again (the server drops it when a body spawns).
- `SiegeService` called `ownsClass` before it was defined (nil at runtime) at the end of Selection.

## 2026-11-13: Gifting, border styles, coin icon, class initials

Compile-checked only.

### Added

- **Gifting Robux crates and items** to another player in the server: a gift button on the card and GIFT on the detail page open the picker (`Main.GiftPicker`, `Client.Core.GiftPicker`). It lists every other player with their avatar.
  - `Packets.Store.Gift` → `StoreService.Gift` checks the recipient can get it, then opens Scribe's gift prompt (`Data.PromptGift`).
  - Scribe records the gift before money moves and delivers it to the recipient's data, even if they leave.
  - Game passes, and Coins or Tokens prices, can't be gifted.
- **Border styles** (`Content.Store.BORDERS`, an item's `Border`): the glowing outline's colors turn around the card. Gold is the default; there are also Rainbow and Obsidian.
  - The Obsidian skin has the Obsidian border (black and violet, turning) with the glow.
- **The coin icon:** "Glossy Gold Coin Icon" from the Creator Store (`Content.Store.COIN_ICON`). It is on every coin price and both wallets.
- **Class pictures:** a class's `Icon`, or its first initial when it has none, on its card and big page.
- **A dimmed blocker** under the detail page (`Main.DetailsBlocker`): nothing behind it can be pressed while it is open.

### Fixed

- **Ribbons (NEW...) overlapped the title:** they sit above the card's top edge now.
- **Hovered cards' borders overlapped their neighbors:** wider margins in the card holder.

## 2026-11-13: Store fixes, Blake for sale, lobby panel, PLAY shine

Compile-checked only.

### Fixed

- **Inventory error** (`Inventory:104: attempt to index function with 'Get'`): the crate inventory's field was named `Count`, which Scribe containers already use for their `Count()` method. It is `Amount` now (`CrateInventory[crateId].Amount`). The server wrote the same field, so no crate was ever saved under the old name.
- **Hovering a card made the grid re-wrap:** every card, rail button and filter chip now sits in an invisible holder frame at its layout size (`StoreCard.Card`, `NavButton.Button`, `FilterChip.Button`). The hover grow happens inside it.
- **Outlines and ribbons were cut off at the page edges:** the holders leave a margin and the pages have padding.

### Added

- **Blake** (the `Hologram` class) is sold: 6,000 Coins or 60 Siege Tokens, featured with a NEW ribbon. Players who don't own it can't pick it in Siege.
- **PLAY shine:** a shine sweeps across the PLAY button every 2.4 s (`Client.Core.Shine` animates any UIGradient tagged `ShineSweep`).

### Changed

- **The lobby panel:** Coins, Siege Tokens, STORE and INVENTORY are one panel on the left (`Main.Wallet`), in the lobby buttons' slate-and-white style.
- **Removed:** the extra Inventory (old Backpack) button in the top-right menu.

## 2026-11-13: Store and Inventory redesign, crates go to the inventory

Compile-checked only (no playtest, as asked).

### Added

- **The Store** (`Main.Store`, `Client.Core.Store`), redesigned:
  - **Layout:** an icon rail (Featured, Crates, Currency, Passes, Bundles, Skins, Classes), balances with "+" buttons, and section headers.
  - **Big cards:** double-width cards for featured and big items.
  - **Labels and badges:** ribbons (POPULAR, BEST VALUE, 🔥 HOT DEAL, NEW), "% OFF" with the old price struck through, and "% EXTRA" on bigger packs.
  - **Glow:** glowing outlines with a sweeping sheen.
  - **Daily deal:** one item a day at 30% off its Coins and Tokens price, with a countdown. The server charges the same price (`Content.Store.PriceOf`).
- **The Inventory** (`Main.Inventory`, `Client.Core.Inventory`; INVENTORY on the lobby bar, and the old Backpack button):
  - **Classes:** yours, then "CLASSES TO BE UNLOCKED", filtered by team.
  - **Skins:** owned, then locked; equip from the skin's page.
  - **Crates:** the crates you own, with a count.
- **A big detail page** (`Main.Details`, `Client.Core.ItemDetails`), like a character select screen:
  - the name, team or rarity, description and a large 3D preview;
  - starter items with gun previews;
  - the ability in depth (cooldown, charges, description);
  - a crate's contents with each chance and what you own;
  - prices or OPEN / EQUIP, and BACK / EXIT.
- **Shared view builders:** `Client.Core.StoreViews`, so a crate or class looks the same in both screens.
- **Classes for sale:** `Content.Store.CLASS_PRICES` (Coins and/or Tokens). A class listed there is locked until bought (`Class:<id>`). None is listed yet.
- **Crate rarity and ribbon:** each crate has a `Rarity` (card colors) and a `Tag`.
- **Packet `Store.Open`:** opens a crate from the inventory.

### Changed

- **Crates no longer open when bought** (Coins, Tokens or Robux). They go into the new saved `CrateInventory` and are opened from the Inventory. OPEN plays the reel (`Main.Opening`), which offers OPEN ANOTHER while you have more.
- **Bundles can include crates** (`Grants.Crates`). The Starter Bundle now has a Field Crate, and is shown as a 50% OFF hot deal.
- **The Armory screen is gone:** the shop stand opens the Store on CRATES.
- `StoreService.Buy` answers (ok, message). The new `StoreService.OpenCrate` gives the skin.

## 2026-11-13: Store products created

- The 8 new developer products and the VIP game pass are created on Roblox (through Open Cloud), at the prices the Store shows, and their ids are in `Shared.ProductIds`. Every Robux price in the Store is now live instead of SOON. The icons are placeholders. See [STORE.md](STORE.md#limits).

## 2026-11-13: Store, Siege Tokens, your own crates, wins and streaks

Server side checked in a Studio playtest. The screens weren't seen (no playtest asked). See [STORE.md](STORE.md#testing).

### Added

- **Crates as data** (`Content.Crates`): add a crate with its skins and weights, and its Coins, Tokens and Robux prices. The Armory has a crate picker and Coins / Tokens / Robux buttons.
- **Siege Tokens:** a premium currency, 5 to start. Bought with Robux, or given by `StoreService.Give` (battle pass, quests).
- **Coins for playing:** 100 for a win, 30 for a loss, 50 for a draw (at least 60 s), and 15 every 5 minutes of play. The VIP pass doubles them.
- **The Store** (`Main.Store`, STORE on the lobby wallet bar):
  - tabs for crates, currency packs, game passes, bundles, special skins and classes, all from `Content.Store`;
  - Robux items show SOON until their id is set.
  - New: the special skin Obsidian, the Starter Bundle and the VIP pass.
- **Wins and losses:** totals, and per mode and category. A win streak per mode, with a 🔥 tag above the head from 2.
- **The last mode played** is saved, and PLAY starts on it.
- `Systems.Store.StoreService`, `Systems.Store.StatsService`, `Shared.StoreGrants`, `Client.Core.Store`; packets `Store.Buy` and `Store.Reward`.

### Changed

- Robux products are declared from the data in `Shared.Data`: `Crate_<Id>` and `Store_<Id>`, plus game passes. The old `SkinCrate` product is the same id as `Crate_Field`.
- `Packets.Skins.BuyCrate` now buys the Field Crate through `StoreService`.
- Siege refuses a locked class the player doesn't own (none is locked).

## 2026-11-13: Armory shop, crate reel, skins on every gun

Compile-checked; the shop opened in a playtest and its cards, tabs and crate list filled in. Studio was not rendering frames, so the 3D previews and the reel were not seen moving. A real crate purchase was not made.

### Added

- **The shop is now the ARMORY** (`Main.SkinShop`, built in Studio):
  - Tabs (All / Pistol / Rifle).
  - A grid of skin cards, each with a 3D preview of the gun wearing the skin, its color stripe, and Equip / Equipped / In crate.
  - A crate panel with the price, OPEN CRATE, every skin still in the crate with its chance, and a status line.
  - New templates: `SkinCard`, `SkinTab`, `CrateItem`, `ReelCard`.
- **Crate opening reel:**
  - After a crate is bought, the won skin arrives in the player's data and the reel spins: a strip of skin cards slows down over 6 s onto the skin won, ticking as each card passes the gold marker.
  - YOU GOT then shows the skin, with EQUIP / DONE.
  - It is a show only: the server picks and grants the skin before the reel starts.
  - `SkinShop.Preview(skinId)` plays it without buying, for testing.

### Fixed

- **Skins did nothing in matches.** A skin was for one gun Id (`Rifle`, `Pistol`), but Siege hands out other guns. Skins now belong to a family:
  - Rifle skins show on the Rifle, BurstRifle, SiegeCarbine and Tactical bullpup.
  - Pistol skins show on the Pistol, SiegePistol and Revolver.
  - (`Content.Guns.Skins` `FAMILIES`, `Skins.FamilyOf`; `EquipField` uses the family.)
- A gun that is one textured mesh shows the skin's color: its texture comes off while the skin is on, and comes back with "None". Checked on copies: the SiegePistol, BurstRifle, SiegeCarbine and Revolver recolor, and go back exactly on "None".

## 2026-11-13: Cameras show your own body

Compile-checked only (not playtested).

### Changed

- Looking through a security camera now shows your own body and held gun, like the drone view. First person hides them on your screen every frame, and `Client.Gadgets.CameraController` shows them again after that.

## 2026-11-13: Siege prep drone always shows

Compile-checked only (not playtested, as asked).

### Fixed

- **The prep drone didn't show.** With streaming on, an attacker's drone stood at the attacker spawn while their body waited in the lobby, so the drone and the area around it never loaded on their client and there was nothing to look through. Drones are now `ModelStreamingMode.Persistent`, and while a player is held in their drone the server sets their `ReplicationFocus` to it, so the world around the drone streams in.
- The attacker is held in the drone (`SetLockedIn`) before the drone is placed, so the body arriving in the lobby can never clear it.
- A missing spawn no longer means no drone: the attacker's picked spawn, else any attacker spawn, is used. With none at all, the player gets NO SIGNAL (and a warning in the output).
- While held (Prep), the client always shows the drone view, or NO SIGNAL when there is no drone, until the server lets go at Action. No body is needed for it.

## 2026-11-13: Siege attackers keep the prep drone and get a second one

Playtested in Studio with one player, driving DroneService and DroneController directly (no full two-team match):

- The prep drone stayed in the world, and the player stayed held in it, with the body flagged InLobby.
- At "Action" the player had DronesReady 1 and DronesMax 2. The Drone key threw the second drone and looked through it, and the touch NEXT button showed.
- Switching went DRONE 2 → DRONE 1 → DRONE 2.
- A scan from each drone at a target in front of it returned true.
- Console clean.

### Added

- `DroneService.AddCharge(player)`: one more drone (a slot and a ready charge) until the next refund. A player's limit is the `DronesMax` attribute (`Content.Drones.MAX_ATTRIBUTE`).
- **Switching drones** while in one, like the cameras: Aim (right mouse), LB / RB on gamepad, or the NEXT button on touch (`DroneFeed.Feed.Touch.Next`, shown only with a second drone). Scanning works from whichever drone you look through.

### Changed

- **Siege prep:** the attacker stays on the drone screen until Action, NO SIGNAL included. Their body waits in the lobby (InLobby), which used to clear the drone and refuse the view; a drone the player is held in now survives it.
- **Siege Action:** the prep drone stays where it is and each attacker gets a second drone to throw (Drone key). A destroyed drone still never comes back. NO SIGNAL shows only when no drone is out and none is ready.
- The Drone key on foot throws a ready drone first; after that it goes into one you already have out.

## 2026-11-13: Custom prompts, build or reinforce, startup fix

Playtested in Studio with one player: startup clean, a drone thrown outside the lobby showed its feed and stayed in it for over 8 s. The new prompt cards were not seen in a playtest (it was stopped before a board was placed), and nothing was run on a phone or gamepad.

### Added

- **Custom proximity prompts** (`Client.Interact.CustomPrompts`): every prompt is drawn as the game's own card (key, action, object, hold bar), from `Assets.UI.Templates.PromptCard`. Prompts on the same object share one `PromptStack`, 2 cards per row, wrapping onto a new row. On touch, hold the card itself.
- Prompt keys never clash: if two shown prompts use the same key or gamepad button, the one without `FixedKey` moves to a free one (E, F, T, G, Z, V / DPad Up, DPad Down, DPad Right, Y).

### Changed

- **A defender frame offers both choices:** build normal boards (Interact, E) or place a reinforced wall (the Reinforcement Expert's ability key, T), side by side. No board needs to be there first. Until now the build prompt was hidden from the Reinforcement Expert while they had charges.
- Attackers never see or trigger the build prompt (its reach is 0 on their client; before, it was only hidden).

### Fixed

- `ClassService.BeginPlacement` errored (`attempt to call a nil value`, line 344): it called `BreakableService.PositionBuilder`, which doesn't exist. Reinforce placement never started.
- **Drones (and every other client system) could fail to start.** `Client.Settings.Options` and `Keybinds` waited for saved data inside `Init`, so a slow or stuck data load held up every client module after them: no drone keys, no HUD. They now load in the background, use the defaults until the data arrives, then apply the saved values.

## 2026-11-13: Mobile UI pass (icons, smaller buttons, no overlaps)

Checked in Studio by laying the screens out in an 844 × 390 frame (a phone in landscape) and with one playtest on the desktop-sized Studio window: console clean. Not run on a real phone, a tablet or a gamepad, and not in a real two-player Siege match.

### Added

- **Icons on the touch buttons**, from the Creator Store: fire (bullet), aim (crosshair), reload, crouch, melee (knife), sprint, grenade or smoke, camera, drone, ability (lightning), admin console. Each is an ImageLabel `Glyph` inside the button's `Icon`. Only the grenade, drone and ability buttons keep a small label (the count or the cooldown).
- `Content.Consumables` entries have an `Icon` (the grenade and smoke pictures on the button).
- **Full-screen menus fit any screen** (`FitScale` tag on a UIScale, run by `Client.Core.UI`). The Siege selection screen starts under Roblox's top bar and shrinks to fit a phone, so nothing hides behind the Roblox buttons.
- `Main.MenuButtons.TouchScale` shrinks the top-right buttons to 0.8 on small touch screens.

### Changed

- Touch buttons are about 30% smaller and re-spaced like other Roblox shooters: FIRE 1.15 of the jump button, the others 0.55 to 0.72, with a gap between every pair.
- The phone boost for the health bar, ammo box, weapon slots and kill feed is 1.15 (was 1.6).
- Siege HUD: a compact timer pill at the top with SCORE beside it (it sat on top of the timer), the objective line and the A and B chips under it, each on one line ("PLANTED" instead of "DEFUSER PLANTED").
- The announcement banner ("Preparation phase", "Defuser planted…") is slimmer and sits above the crosshair, below the timer, instead of over it.
- Selection screen: small text is 1 to 2 px bigger, the Loadout column is more compact, so nothing spills under the Ready button on a phone.
- Death screen: a compact card, the SPECTATING line and the countdown stack at the bottom centre, above Siege's spectate bar, instead of on top of each other.

### Fixed

- The round-end panel no longer draws over the still-visible death and spectate texts: it hides them and draws above them, and its kill rows draw above the panel.
- The empty grey bar at the top right after dying: Roblox's own health bar, now turned off (the HUD has its own).

## 2026-11-12: Camera and drone scans reveal players and cameras

Single-client Studio startup check passed and all nine changed Luau sources parsed. Multiplayer scanning and class reveal were not exercised.

### Added

- **Defender cameras scan attackers.** Interact (DPad Up; touch `SCAN`) asks the server to scan an enemy player in a live camera's view (150 studs, 6°, clear line of sight, five-second cooldown). A successful scan reveals the attacker's class to defenders for the match and alerts the target.
- **Drone scans can reveal enemy cameras.** When no player or NPC is selected, a scan can mark a live enemy camera for the drone user's team with key `Camera:<CameraId>` for `SPOT_TIME`.
- A red `SCANNED` notice appears for `SCANNED_ALERT_TIME` after a player is scanned by either system.
- API additions: `Packets.Camera.Scan`, `Packets.Scan.Alert`, and the `Camera.Scanned(spotter, targetModel)` extension.

### Changed

- Enemy classes are hidden from both teams until revealed by their side's scan: drones reveal defenders to attackers; cameras reveal attackers to defenders.
- Camera and drone feeds show the match timer over both live and NO SIGNAL screens.
- Cycling away from a destroyed camera is no longer blocked by the normal view-switch cooldown.

## 2026-11-12: Drone scan reveals nearby enemies with a popup

Not playtested (compile-checked only).

### Changed

- **A scan no longer needs the enemy in the crosshair:** with nobody there, it takes the nearest enemy within 40 studs in clear view (`NEARBY_RANGE` in `DroneService`).
- **Every attacker gets a popup** on a scan of a defender: "ENEMY SCANNED" with the defender's name and class (`SiegeService.onSpotted`). The class shows on the attackers' scoreboard (Tab) from then on, and the mark where the defender stood goes to the whole team, as before.

## 2026-11-12: Party shows again after a match

Not playtested (it needs live servers and two players).

### Fixed

- **Back from a match, the screen showed no party** although the server still had it (inviting the same players was refused as "already in your party"). The party message could be sent before the returning client was listening. The client now asks for its party when it starts, a few times in the first seconds, when a match ends, and when the Party menu opens (`Party.Request` action `Sync`, [MATCHMAKING.md](MATCHMAKING.md#party-sync-2026-11-12-not-run)).

## 2026-11-12: The other team in the ready list; Reinforce works again

Not playtested. The Reinforce swap was checked in Edit mode on copies of a board and a door.

### Added

- **The ready list shows the other team too,** in its own section under a red ENEMY TEAM heading with the side's name, red names and dark red rows. Only who they are and whether they are ready is sent; never their picks ([SIEGE.md](SIEGE.md)).

### Fixed

- **Reinforce refused every board and door** ("That can't be reinforced"). The reinforced models had been moved from `Assets.Models.Siege` to `Assets.Models` and renamed (`ReinforcedDoor`), and the ability only looked in the old place. It now looks in `Assets.Models` first and says "The reinforced model is missing" if a model is ever gone.
- **Reinforce could not target an empty door frame** (a door whose boards are not built yet has nothing to aim at). It now takes the board nearest the line of sight.

## 2026-11-12: Drone, camera and slide fixes; ready list; play with party; touch layout

Not playtested (by request): compile-checked, and the touch layout worked out by arithmetic for three screen sizes.

### Added

- **PLAY WITH PARTY** in the lobby: a match of the party's own members only, dealt into two even teams (`QueueService.JoinPrivate`, [MATCHMAKING.md](MATCHMAKING.md#play-with-party-2026-11-12)).
- **Selection:** a team list down the right side with each teammate's picture, name and READY or PICKING; when everyone in the match is ready the clock is skipped. A Consumable row on the Class page.
- **`Client.Hud.Nameplates`:** enemies show no name and no health bar; teammates show both.
- The drone feed's own touch stick, and control hints and touch buttons on the NO SIGNAL screens.

### Fixed

- **Drone scans found nobody:** the line of sight stopped at invisible room volumes and other triggers, and the aim had to be near the torso's center. Now only visible, solid parts block, and any body part near the crosshair counts.
- **Touch could not drive the drone.**
- **The drone camera looked through walls.**
- **NO SIGNAL could not be closed** with the drone keys.
- **A destroyed camera was 4% see-through;** it is opaque now.
- **A player who left a queued party kept seeing the search.**
- **Sliding was inconsistent:** a crouch press is judged by sprint intent and waits up to 0.3 s for a slide to be possible ([MOVEMENT.md](MOVEMENT.md)).
- **Touch buttons:** the left ones were placed from the right corner and slid off narrow phones; the right ones ran up the whole edge. All are now laid out from one table ([UI.md](UI.md)).

### Changed

- **Reinforce** replaces the board with its reinforced model (`Assets.Models.Siege.ReinforcedBoard` / `ReinforcedDoorBoard`) instead of cutting the damage the original takes. The original is kept and put back when the match ends.
- The UI's ScreenGuis live under `ReplicatedFirst.UILoader` (another developer's move); the docs say so now.

## 2026-11-12: Match music (start, panic, end)

See [MUSIC.md](MUSIC.md). Not playtested (by request): compile-checked only.

### Added

- **A panic song in the last 30 seconds** of the Action phase: the playing song fades to 0 over 4 s while a random song from `Assets.Music.Panic` rises from 0 to its volume (0.5).
- **An end song** from `Assets.Music.End` when the match ends, and **a start song** from `Assets.Music.Start` when a match begins.
- `Content.Music` (folder names, the 30 seconds, the fade times) and `Client.Core.Music.Play(kind)`.

### Changed

- `Client.Core.Music` was rewritten: it plays its own Sounds (in the Music sound group) so it can crossfade, and never picks the same song twice running. The old module is in `ServerStorage.Archive.OldMusic`; the `Music` effect in `Content.Effects.Registry` is no longer used.

## 2026-11-12: Images, tags and colors on mode cards

Not playtested (by request): compile-checked only.

### Added

- **`Image` on categories and modes** (`Content.Matchmaking`): a picture that fills the card, under a dark fade so the name stays readable. `Assets.UI.Templates.ModeCard` has new `Art` and `Shade` parts.
- **`Tag`, `TagColor` and `Color` on modes.** A mode's card used its category's; now each mode has its own (1 V 1: red, DUEL; 5 V 5: blue, TEAM).
- **`Icon` on categories and modes:** the big faded text on the card. `""` keeps the automatic text (none over an image); anything else is shown as written ([UI.md](UI.md#what-a-card-shows)).

## 2026-11-12: Game Modes panel; no loadout picking in the lobby

Not playtested (by request): compile-checked, and the panel measured at phone and desktop sizes.

### Added

- **The Game Modes panel** (`Main.Modes`, `Client.Core.ModeMenu`): a full-screen game-select screen with one card per mode category (DUELS, SQUADS), a description box, and EXIT ([UI.md](UI.md#the-game-modes-panel)). Pressing a category shows its modes; a category with one mode picks it at once.
- `Content.Matchmaking.CATEGORIES`; each mode has a `Category` and a `Description`; `Content.Matchmaking.ModesIn(categoryId)`.
- `ModeMenu.Selected()` / `Pick(id)` / `Open()` / `Changed`; `Client.Core.Matchmaking.OpenModes()`.

### Changed

- **The lobby bar's MODE button** sits right of PLAY (where LOADOUT was) and opens the panel instead of stepping to the next mode.
- `LoadoutService` refuses a loadout pick while the player's `InLobby` attribute is true, and always on a lobby server.

### Removed

- **The Loadout key (B) and the game-mode key (M).** Both actions are gone from `Shared.PlayerSettings` and the Settings menu.
- **The lobby bar's LOADOUT button** (archived as `ServerStorage.Archive.OldUI.LobbyLoadoutButton`). Nothing opens the Loadout menu now, which also holds the grenade / smoke picker.
- `Content.Matchmaking.NextMode`, `Client.Core.Matchmaking.NextMode`.

## 2026-11-12: Queue modes (1 V 1), Fredoka One, lobby clean-up

### Added

- **Queue modes.** A party queues for one mode and is only matched with tickets of that mode ([MATCHMAKING.md](MATCHMAKING.md#queue-modes)). Modes are rows in `Content.Matchmaking.MODES`: **1 V 1** (the default, so two players are enough) and **5 V 5**. The ticket carries the mode (`G`), the match record too (`Mode`).
- **A mode button above PLAY** (`Main.Lobby.ModeButton`) and a key, **GameMode (M)**: each press moves to the next mode. The search status shows the mode.
- `QueueService.Join(player, modeId)`, `Content.Matchmaking.GetMode` / `NextMode`, `Client.Core.Matchmaking.NextMode()`.

### Changed

- **Every piece of text is Fredoka One** (221 labels, buttons and text boxes in `StarterGui`, the UI templates and the world, plus the text `LobbyHubUI` and the banner effect build in code). Cmdr's console keeps its own fonts.
- `Queue.Request` takes the mode's Id as a second value; `Queue.State` has `Mode`.
- `Content.Matchmaking.MAX_WAIT` is gone: each mode has its own `MaxWait`.

### Removed

- **The Loadout menu no longer opens by itself on join.** It still opens from the lobby bar's LOADOUT button and with B.
- **The Career and Maps buttons** are no longer shown in the lobby (`Client.Core.LobbyHubUI`). Their panels and code are still there; Backpack still shows.

## 2026-11-12: No strafe tilt in the lobby

### Changed

- The camera no longer tilts when strafing (A/D) in the lobby, where there's no gun in hand (`Client.Movement.MovementCamera`, the `InLobby` attribute). It still tilts in the arena.

## 2026-11-12: UI revamp (MVP pass)

See [docs/UI.md](UI.md). Laid out and checked by measurement only: nobody has seen it rendered yet.

### Added

- **A big green PLAY button, bottom center** (`Main.Lobby`). Pressing it queues the party at once; while searching it is red and cancels. PARTY sits to its left and LOADOUT to its right, with the queue status above.
- **Party is its own menu** (`Main.Party`, key L): member rows with avatars, LEAD and KICK, LEAVE PARTY, and the invite list. It is no longer inside a Play menu.
- **`Client.Core.UIFeel`:** every button in the game squashes when pressed, grows on hover, and has a sound; refused buttons buzz; menus pop in. Six new UI sounds (`UIOpen`, `UIClose`, `UIConfirm`, `UIError`, `UITick`, `UINotify`), placeholders made from the two the game had.
- **Siege team cards** in the style of an operator line-up, dealt in on the reveal; the reveal reads OBJECTIVE LOCATION or INSERTION POINT.
- Sounds and effects on the moments that matter: search started, match found, invite received, pick accepted, the last 5 seconds of selection, a new phase, an ability used or refused, the round's end.
- Keys: **Party (L)**. Play (K) now queues or cancels.

### Changed

- **One look** for the Loadout, Settings, Skin shop and Scoreboard menus and their rows: the same panel, heavy titles, bold buttons, round corners.
- **Touch sizes:** close buttons 44 × 40 (were 36), the top-right menu buttons 120 × 44 and wrapping onto rows (were 132 × 36 in one line), invite buttons 42 tall (were 30), party rows 44 tall, the health bar 40% thicker, weapon slots 30% taller. The SCORE touch button moved out of the combat buttons to the top of the Siege HUD.
- The top-right menu buttons hide during Prep and Action.

### Removed (archived in `ServerStorage.Archive.OldUI`)

- The Play menu that held the queue and the party together (`Main.Matchmaking`) and its button (`MenuButtons.PlayButton`).

## 2026-11-12: Siege bombs are in place from the prep phase

See [docs/SIEGE.md](SIEGE.md#the-bombs).

### Added

- **The bombs are placed for the defenders.** When Prep starts, a copy of the bomb model (`Content.Siege.BOMB_MODEL`, today `Workspace.Bomb`) is stood on `BombA` and `BombB` of the chosen site, in `workspace.SiegeBombs`, and removed after the match. Checked in Studio: 2 bombs one second into Prep, every part anchored and visible, centered on the map's bomb part; 0 after the match.
- **A bomb's room can be a folder of parts**, not only one part (`Sites/<site>/BombA`), for rooms one box doesn't fit.

### Changed

- **Wording:** nobody plants a bomb. Only attackers plant anything, a defuser; defenders keep them away from the bombs. The HUD chips read NO DEFUSER / DEFUSER PLANTED, and the defenders' objective reads "Keep the attackers off both bombs". The docs and code comments say the same.

### Fixed

- The end-of-match cleanup called a helper before it was defined, which left a match stuck in its End phase with a repeating error (introduced and fixed the same day, before any push).

## 2026-11-12: Siege, global matchmaking, parties and classes

See [docs/SIEGE.md](SIEGE.md), [docs/MATCHMAKING.md](MATCHMAKING.md) and [docs/CLASSES.md](CLASSES.md). Tested in Studio with one player only; nothing cross-server has run live.

### Added

- **Siege**, the only mode: attackers plant a defuser on both bombs of the site the defenders voted for; one round, one life. `Systems.Siege.SiegeService`, `SiegeMap`, `SpectateService`; `Content.Siege`; `Content.Match.Modes.Siege`.
- **Global matchmaking:** a MemoryStore queue, one matchmaker at a time (a lease), party-aware team packing, a reserved server per match, and the return to the lobby. `Systems.Matchmaking.*`, `Helpers.Retry`, `Content.Matchmaking`. Studio forms matches on the Studio server.
- **Parties** of up to five across lobby servers: invite, accept, leave, kick, promote.
- **Classes:** five a side, one player per class per team, each with an ability. `Content.Classes`, `Systems.Classes.ClassService`, `Gadgets`, ten modules in `Systems.Classes.Abilities`; gadget models in `Assets.Models.Siege`.
- **Defender cameras:** `Systems.Cameras.CameraService`, `Client.Gadgets.CameraController`, `Content.Cameras`, `StarterGui.CameraFeed`.
- **Spectating** teammates, then enemies, after the death camera (same camera, Camera + 4).
- **UI, built in Studio:** `Main.Matchmaking`, `Main.PartyInvite`, `Main.MenuButtons.PlayButton`, `StarterGui.SiegeSelect`, `Main.SiegeHUD`, `Main.SiegeScoreboard`, `StarterGui.CameraFeed`, `DroneFeed.NoSignal`, `Main.Mobile.AbilityButton` / `CameraButton` / `ScoreButton`, and templates `PartySlot`, `InviteRow`, `SiegeOption`, `SiegeClassCard`, `SiegeTeamCard`, `SiegeBoardRow`, `SiegeBoardTeam`, `SiegeKillRow`, `BombMarker`.
- **Client modules:** `Client.Core.Matchmaking`, `Client.Core.SiegeSelect`, `Client.Core.Spectate`, `Client.Hud.SiegeHud`, `Client.Hud.Scoreboard`, `Client.Gadgets.CameraController`.
- **Packets:** groups `Party`, `Queue`, `Siege`, `Class`, `Camera`, `Spectate`; `Drone.Scan`, `Drone.Marked`.
- **Keys:** Play (K), Class ability (T). Teams `Attackers` and `Defenders`. Effects `GadgetPlace`, `GadgetDestroyed`, `Flashbang`, `AbilityPulse`.
- **Extension points:** `Siege.*`, `Party.*`, `Queue.*`, `Matchmaking.*`, `Classes.*`, `Camera.*`, `Spectate.Changed`, `Drone.PreventRespawn`, `Drone.PreventView`, `Lobby.PreventFirstSpawn`, `Loadout.PreventApply`, `Death.PreventSpectate` (all in [API.md](API.md)).

### Changed

- **Drones:** a scan leaves a static mark where the enemy stood (30 s, replaced by the next scan) instead of a highlight and marker that followed them; the scan cooldown is 5 s and fully enforced by the server. New: `DroneService.Place`, `Mark`, `SetEnabled`, `SetLockedIn`, `Lock`, `CanView`; the NO SIGNAL screen.
- **MatchService** keeps `External` modes: for those it never starts, shuffles, respawns or ends anything itself. New: `BeginExternal`, `SetClock`, `Finish`, `Reset`, `Kills`, `Refresh`.
- **MatchHud** no longer owns the scoreboard (`Client.Hud.Scoreboard` does).
- **LoadoutService:** `LoadoutService.Arm(player, guns)`; `Loadout.PreventApply`.
- **LobbyService:** `LobbyService.Release(player)`; `Lobby.PreventFirstSpawn`.
- **DeathCamService:** `DeathCamService.Release(player)`; `Death.PreventSpectate`.

### Removed (archived, nothing deleted)

In `ServerStorage.Archive.OldMatchModes`: the Team Deathmatch, Free-for-All and Elimination modes; the admin Match menu (`Client.Core.MatchMenu`, `Main.MatchMenu`, `MenuButtons.MatchButton`); the `match`, `matchmode` and `matchset` commands; the old scoreboard frame and its `ScoreboardRow` / `ScoreboardTeam` templates; and copies of `MatchService`, `Packets`, `PlayerSettings` and `Content.Match.Settings` as they were. `Packets.Match.Admin` and the Match key (M) are gone. In `ServerStorage.Archive.OldDroneSpot`: the `SpotHighlight` template.

## 2026-11-11: NPC guard mode

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Guard mode).

### Added

- **Guard mode for every NPC** (for a future game mode). A guard:
  - stays in its room (a part tagged `NPCRoom`);
  - patrols it and watches its doors and windows;
  - rebuilds any damaged door or window board of the room, at any health, the most broken first, so the room can't be sieged;
  - always fights first: an enemy it can shoot, or a hit it just took, stops a repair, and it fights from inside the room;
  - never chases, pursues through glass or breaks out.
- **Turning it on:** `NPCService.SetMode(npc, "Guard", room)` / `"Roam"`, or `Mode = "Guard"` (and optional `Room`) on an `NPCSpawn` part. NPC models show `NPCMode` and `GuardRoom`.

Partly tested in a playtest on a temporary room in the NPC test area:
- **Patrol:** a guard patrolled and never left the room (0 of 16 samples outside).
- **Repair:** with an enemy visible through the broken window, it fought instead of repairing, as designed.
- **Not tested:** a full repair with no enemy in view, and a repair interrupted by a hit. Those weren't checked; see [NEXT_STEPS.md](NEXT_STEPS.md).

## 2026-11-11: Shotgun idles fixed

### Fixed

- **Both shotgun idles** (Shotgun, SiegeShotgun) held the gun too far back, with the stock up over the shoulder.
  - **Cause:** the gun slides back when the left hand can't reach the front grip. Held out to the side, a shotgun met no body to stop it.
  - **Slide limit:** the slide is now capped at 0.45 studs.
- **One idle for every long gun:** the long-gun idle, sprint and reload are now placed by the grip, not the rear sight, which sits in a different spot on every gun (on a shotgun it's on the grip). Every long gun now idles in the same low ready: the hand at the right of the chest, the stock at the right shoulder, the muzzle 25 degrees down and a little across the body.

Checked on the gun range:
- **Shotguns:** both are in the low ready, seen from the side.
- **Fit, all 72 rigs:** clipping 0.01 studs at most, and the right hand always on the grip.

## 2026-11-11: Guns held higher

### Fixed

- **Long guns were still held too low** (around the waist when aiming). The step that brings the left hand to the front grip was pulling the gun down toward the left shoulder. It now only slides the gun straight back, level, and the left hand holds as far along the gun as it reaches.
- **The poses are higher:** long guns aim with the sights at eye level beside the right cheek, idle and reload sit at chest height, and the pistol idle is higher.

Measured on the gun range, all 72 rigs:
- **Long guns aiming:** the sight sits at eye level (+0.10 from the head center); before, it was at -0.25 and 0.38 studs to the wrong side.
- **Long guns at idle:** chin/shoulder height.
- **Fit:** clipping 0.02 studs at most, and the right hand always on the grip.

## 2026-11-11: Guns no longer sit low in the hand

### Fixed

- **Long guns** (Rifle, BurstRifle, LMG, Shotgun, SiegeShotgun, Tactical_Bullpup_1, SiegeCarbine) **sat too low in the hand.** The hand gripped the middle of the gun's short pistol grip, so the gun sank into the fist. `GunService` now sets each gun's grip on equip from the holder's own hand size, so the top of the fist sits just under the gun body (`fitGrip`). This applies to every gun and every avatar's hands.

Measured on the gun range: every gun's body sits on top of the fist (0.03 studs above it) in all 72 rigs. The guns moved up 0.24 to 0.41 studs relative to the hand. The other fit checks held: clipping at most 0.15 studs, and the left hand 0.16 studs from the front grip on average.

## 2026-11-11: Third-person guns fixed: no more guns through heads, revolvers fixed

See [docs/THIRD_PERSON_GUNS.md](docs/THIRD_PERSON_GUNS.md).

### Fixed

- **Guns stuck out of characters' heads and bodies.** The gun models are far bigger than an R15 character can hold (a full rifle is 4.4 studs; an arm reaches 1.7). Third-person guns are now scaled to fit: long guns about 2.2 studs, pistols and revolvers about 1.15. The first-person view and gameplay are unchanged. The poses also keep every part of the gun out of the head and torso; a stock may rest slightly into the shoulder.
- **Revolver animations were wrong.** Their long barrel made them count as rifles (sight half a stud from the face, rifle sprint carry). Guns are now sorted by whether they have a stock, so revolvers use the pistol poses.
- **The left hand on long guns** now goes as far toward the front grip as it can reach instead of dragging the gun into the body.

### Changed

- `Content.Guns.Skins` scales skins by a gun's `ModelScale`, so skins fit the smaller third-person guns.
- `ThirdPersonGuns.Report()` gives each character's gun fit, for checking.

Measured on the gun range, all 72 rigs:
- **Clipping:** at most 0.10 studs into the body.
- **Right hand:** always on the grip.
- **Left hand:** 0.19 studs from the front grip on average.

## 2026-11-11: Gun animation range

See [docs/GUN_SHOWCASE.md](docs/GUN_SHOWCASE.md).

### Added

- **A gun range with 72 rigs** (`workspace.GunShowcase`, east of the map): one per gun (12) and animation (idle, walk, sprint, aim, shoot, reload), each doing only that one, for real.
  - **Shoot:** fire real bullets at their lane's target in the gun's own rhythm and reload when empty.
  - **Reload:** reload on a loop.
  - **Walk and Sprint:** pace their lanes.
  - **Aim:** aim at their target.
- **Driver:** `Systems.Showcase.GunShowcase` runs them; the rigs can't be hurt.
- **The `range` command** (alias `showcase`) takes you there.

### Changed

- `Client.Guns.ThirdPersonGuns` treats only an Ammo drop of at most 3 rounds as a shot. It also poses `GunShowcase`-tagged rigs; `Client.Guns.GunEffects` draws their tracers.

Tested in a playtest:
- **Guns:** all 72 rigs were armed.
- **Shooters:** every one fired and reloaded.
- **Lanes:** the walk and sprint rigs moved.
- **Visible:** muzzle flashes and tracers showed.
- **Errors:** none.

## 2026-11-11: Third-person gun animation for every gun

See [docs/THIRD_PERSON_GUNS.md](docs/THIRD_PERSON_GUNS.md).

### Added

- **Other players and NPCs now hold, aim, shoot and reload guns properly** in third person, for all guns (`Client.Guns.ThirdPersonGuns`). Before, every gun's animation slots were empty and characters used Roblox's one-arm hold.
  - **Idle:** a two-handed low ready, with a walk bob.
  - **Sprint:** long guns are carried across the chest, pistols held low.
  - **Aim:** the sights come up to the eyes and follow where they look, with the waist and head following too.
  - **Shoot:** a recoil kick on every shot (pistols 13 degrees, shotguns 10, rifles 5).
  - **Reload:** the left hand goes to the magazine, down to the belt and back, with the magazine hidden while it's out.
  - **Lower body:** the legs keep the normal walk and run.
- It is code, not animation files: each gun is posed from its own sight and grip attachments with IK, so new guns work with nothing to upload. Long guns slide back toward the body until both hands reach their grips.
- New shared state: `GunAiming` (characters), `Reloading` (gun tools), `AimPitch` (NPCs).

### Changed

- The old third-person aim tilt in `Client.Guns.GunEffects` is replaced by the new system.

Tested in a playtest on the test-area NPCs:
- **Pistol aim:** the sight sat 1.17 studs in front of the eyes, on the aim line.
- **Idle:** the left hand sat on the front grip (0.00 studs) for the pistol, burst rifle and shotgun.
- **Reload:** the full magazine path.
- **Shotgun shots:** they kicked the barrel to about 11 degrees.

## 2026-11-11: Pistol shoot animation (Rig2)

### Added

- **A "Pistol Shoot" animation** for the R15 rig `Workspace.Enemies.Rig2` and the Pistol it holds, saved as `ServerStorage.RBX_ANIMSAVES.Rig2."Pistol Shoot"` (open it in the Animation Editor). It is 0.3 s, plays once, priority Action, and moves only the upper body (waist, neck, both arms), so it layers over walking:
  - 0 s: an aimed two-handed stance: barrel level and straight ahead, the rear sight on the eye line 1.16 studs in front of the eyes, the support hand on the pistol's `LeftGrip` point.
  - 0.04 s: the kick: muzzle up 13.5 degrees and pulled 0.2 studs toward the face, hands still on the gun.
  - 0.12 s: settling (muzzle 2.7 degrees up), easing back.
  - 0.3 s: back on target.
- The poses were solved from the rig's real joints (its `AnimationConstraint`s and attachments) and the pistol's attachments, not hand-placed. The solved joint angles are kept on Rig2 as the `SolvedAimPose` and `SolvedKickPose` attributes (JSON) to build more pistol animations from.

Checked in a playtest: played on Rig2, the barrel pointed within 0.7 degrees of straight ahead at the aim frame and 13.5 degrees up at the kick frame (screenshots).

## 2026-11-11: Death screen and spectating the killer chain

See [docs/DEATH_SCREEN.md](docs/DEATH_SCREEN.md).

### Added

- **A new death screen** (`Main.DeathScreen`, `Client.Hud.DeathScreen`): who killed you (a player's avatar, or an NPC's name), the weapon, and the respawn countdown.
- **Spectating your killer** in a third-person camera that follows behind them smoothly and never goes through walls. **If your killer dies, you watch their killer**, and so on; **with nobody to watch, the camera stays on your body**. When you respawn, the camera goes back to you. Works for NPC killers and outside matches too (`Systems.Combat.DeathCamService`).
- The `Combat.Death` extension point: every death, credited or not, with its attacker and weapon.

### Changed

- The old death screen in the match HUD (`Main.MatchHUD.DeathScreen`, `Packets.Match.Death`), which only followed player killers in first person, is removed; `Packets.Death` replaces it.

Tested in a playtest: killed by the Soldier NPC, the camera followed it; when the Breacher killed the Soldier, it moved to the Breacher; when the Breacher died with no killer, it went back to the body; on respawn it went back to the new character.

## 2026-11-11: Quicker, smoother movement and faster slides

See [docs/MOVEMENT.md](docs/MOVEMENT.md) (Tuning).

### Changed

- **Faster movement**: walk 17, sprint 26, tactical sprint 31, crouch 9 studs/s (was 16 / 23 / 27 / 8). Speed changes ramp almost twice as fast (acceleration 80, deceleration 100), and air control is stronger, so starting, stopping and turning feel snappier.
- **Faster, longer slides**: a slide starts at 38 studs/s or 1.35 times your speed (up to 52), loses speed more slowly, and ends at 15 instead of 11. A full slide now lasts about 1.1 s and covers about 29 studs (was about 0.8 s and 20). It steers better and can be used again after 0.45 s (was 0.75). A slide-jump keeps 90% of its speed.
- **A slide that ends in a sprint keeps its speed**, instead of the sprint ramping up again from crouch speed (the slow part after a slide).
- The camera drops into a slide or crouch and its field of view changes a little quicker.
- The server's speed check allows slide speed for 2 s after a slide (was 0.6 s), to cover the longer slides.

Measured in a playtest: a full slide lasted 1.1 s, peaked at 37 studs/s and covered 29 studs, then went straight back into a sprint.

## 2026-11-11: Siege-style scout drones

See [docs/DRONES.md](docs/DRONES.md).

### Changed

- **The drone system is rebuilt from scratch**, modeled on Rainbow Six Siege's drones, in the framework's structure: `Content.Drones` (settings), `Systems.Drones.DroneService` (server), `Client.Gadgets.DroneController` (client), with a new UI built in Studio (`StarterGui.DroneFeed`, `Main.DroneSlot`, mobile buttons). The old system (`DroneService` Script, `DroneController` LocalScript, `DroneRemote`, its model) is archived, disabled, in `ServerStorage.Archive.OldDroneSystem`.

### Added

- **Throw a drone with 5 and look through it at once**; 5 or X leaves it.
- **Fast, smooth driving**: 24 studs/s, quick to start and stop, the drone turns with your look. **Hop** (Space), **boost** (Shift, 36 studs/s, an empty bar locks for 6 s), a camera that eases landings and leans into turns.
- **Spotting**: the Fire button marks the enemy in the crosshair for your team for 8 s (red outline and marker).
- **Drones have health (30)** and can be shot or blown up by anyone but the owner's team. A destroyed drone shows "SIGNAL LOST" and **comes back after 30 s**.
- **NPCs deal with drones**: they see them up close (55 studs, players first), hear them driving, are woken by them, and shoot them down.
- Your body stays where you left it; taking damage drops you out of the drone. Gamepad (DPad Left / Down) and touch controls.

### Changed the same day, after your playtest

- **One drone out at a time; 5 goes in and out, X goes out**: 5 takes you into your drone where you left it while it lives, and throws a new one only when it is gone and the cooldown is done. In the drone, 5 or X takes you back to your body. X never puts you in. The touch CAMS button is gone (DRONE goes in, the feed's EXIT leaves).
- **The respawn cooldown is 30 s** (was 18).
- **Fixed: X put you straight back into the drone** (and 5 threw a new one) when you used it to leave: the same key press reached the on-foot key too.
- **Your body stays visible** while you look through the drone (first person was hiding it).
- Q / E (switch drones) and the touch NEXT button are gone, since there is only one drone.

Tested in a Studio playtest: a throw lands and is handed to the client, the feed opens with the HUD and gun viewmodel hidden, the HUD count and cooldown work, and NPCs shot drones down. Fixed during the test: destroyed drones were never removed (a Humanoid without a state machine never fires `Died`), a thrown drone slid 100 studs while its physics changed hands, and the gun viewmodel drew over the drone camera.

## 2026-11-11: Modular matches and our own teams

See [docs/MATCH.md](docs/MATCH.md).

### Changed

- **The round system is rebuilt as a modular match system** (`Systems.Match.MatchService`), replacing the fixed Red vs Blue `Systems.Round.RoundService`, `Content.Round` and `Client.Hud.RoundHud`. A mode is one ModuleScript in `Content.Match.Modes` (data plus optional hooks); three ship: **Team Deathmatch**, **Free-for-All** and **Elimination** (rounds, no respawns).
- **Our own team system** (`Systems.Match.TeamService`, `Content.Match.Teams`) replaces Roblox `Teams`: a player's team is the `Team` attribute. Red, Blue, Green and Yellow; up to 4 teams a match; team spawns from a SpawnLocation `Team` attribute or an automatic split of the arena. NPCs, aim assist, NPC hearing and friendly fire read it.
- **The match UI is redone in the style of the other menus:** a top bar with a score chip per team, a status line and result banner, a Tab scoreboard (replacing Roblox's player list), the death screen, and teammate outlines.

### Added

- **Match settings an admin can adjust** (`Content.Match.Settings`): time limit, score limit, rounds to win, number of teams, respawn delay, friendly fire, auto-balance, players to start, intermission. Each mode picks which it uses and its defaults; the server cleans every value.
- **The Match menu** (M, `Main.MatchMenu`, admins only): pick the next mode, adjust its settings, start, end or restart a match. Also Cmdr: `match start|end|restart`, `matchmode`, `matchset`.
- `MatchService.AddScore` for objectives, and extension points `Match.Started`, `Match.RoundStarted`, `Match.Scored`, `Match.Ended`, `Team.Changed`.
- Keys: **Scoreboard** (Tab) and **Match setup** (M) in Settings > Controls.

Tested in a Studio playtest with one player: waiting, admin start, team assignment and team spawns, the score limit ending Team Deathmatch and Free-for-All, an Elimination round ending and the next starting, setting cleaning, the admin packet, the HUD and the menu.

## 2026-11-10: Team deathmatch rounds

See [Team deathmatch rounds](ROUND_SYSTEM.md). *Replaced on 2026-11-11 by the modular match system ([docs/MATCH.md](docs/MATCH.md)); Team Deathmatch is now one of its modes.*

### Added

- **Three-minute Red vs. Blue rounds.** The server balances arena players, tracks credited enemy-player kills, and awards the round to the team with the higher kill total (ties are draws). Rounds require two arena players and have a ten-second intermission.
- **Match HUD and death spectating.** The HUD displays team totals and the ten highest-kill players with profile thumbnails. On death, the victim sees a death screen and follows the credited killer until respawn.
- **Friendly-fire protection during active rounds.** Teammate damage is blocked by the server; self-damage remains unchanged.

### Changed

- The kill-feed death hook now reports a credited player death to the round service before clearing its damage record.

### Fixed

- None.

## 2026-11-10: NPCs board up doors and windows

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics, Board up).

### Added

- **NPCs rebuild broken door and window boards when they need to hide or hold.** When their health is low and they know where you are, or you hit them from out of sight, they board up a broken door or window between you and them (on their floor, within 25 studs). When they hold a room they secured, they seal its broken doors and windows. They walk to the inside, face the board and put a piece back every 0.6 s (`BreakableService.Repair`), stopping at once to fight if they can see and shoot you. Tested: a wounded Soldier boarded a fully broken door back up in 4-5 s; a healthy one with no threat left it alone; one holding a room sealed both of its doors.

### Fixed

- NPCs marked a door or board as unreachable when an older, unrelated path failed just after they picked it; now only a failed path to that door counts.

## 2026-11-10: NPCs stop shooting glass and come for you

### Fixed

- **NPCs shot at you through unbreakable see-through walls.** Their "can a bullet reach" check counted a hit within 2 studs of you, and glass right in front of you is that close. At a person they now only fire when the bullet reaches that person; behind glass they go after you instead.
- **NPCs couldn't walk while they saw a target.** Turning set the root's CFrame every frame, which stopped them walking. They now turn with an `AlignOrientation`, so they face you and move at the same time.
- **Paths to a person failed.** Path goals were the person's root, inside their body, which pathfinding refuses. Paths now go to the floor under the goal (`Brain.Ground`).
- **NPCs didn't find the door into your room** when it was round a corner. They now check the nearest doors, boards, soft walls and windows by pathfinding from just inside each to you (`Brain.Connected`) and break the first that leads in.
- Trapped NPCs look for a way into the target's room before breaking out of their own; a failed search retries after 4 s (was 10).

Tested: a Soldier facing the test Rig behind the glass held fire, went round, cut through a soft wall and was in the room shooting the Rig 4.5 s later.

## 2026-11-10: NPCs move, hunt and get around

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics).

### Fixed

- **NPCs stood still.** They wandered only near their spawn, and froze or walked into walls when a path failed, and some were shut in rooms with no path anywhere. Now: wander points 20-90 studs away on their own floor, paths through corridors about 3 studs wide, the closest reachable path when there's no full one, faster re-pathing when stuck, and **breaking out** of rooms they're shut in (through a board, soft wall or window). Live: NPCs moved in 30-37 of 40 samples (was 21 for the Grenadier), and a Grenadier trapped upstairs broke a window board, climbed out and dropped down.
- **NPCs stared through glass.** Seeing a target they can't shoot, they now go after it and break in if they must.
- **NPCs walked into boards.** A board or soft wall right ahead on their path is broken on the spot.
- **Shooting at hidden players** is shorter: 1.2 s after the last reason (was 2.5), 1.5 s after losing sight (was 3). NPC bullets only pass soft walls and boards, like players' (0 of 14 logged hits went through anything solid).

### Added

- **NPCs turn toward where a hit came from** when they can't see the shooter, and hunt there.
- **NPCs hear boards being rebuilt** (`Breakable.Repaired`) within 60% of their hearing range.
- **NPCs climb through windows**, including after breaking a window's board, and drop from upper floors.

## 2026-11-10: NPCs decide to break in

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics).

### Added

- **NPCs decide when boards and soft walls must be broken to get in.** Going after a hidden enemy, or a room they're securing, they breach when there's no path, they're stuck, or the way round is much longer than going through (over 1.8x + 20 studs). They pick the door-height board or soft wall that opens onto the room on the shortest trip, walk to it (lobbing a grenade when the arc is clear), and **bash** or **shoot** it until a person fits, then walk in. Tested: the Breacher broke in through a door board with one shotgun blast and secured the room in 2 s; the Grenadier bashed it open and was in within 8 s.
- **Secure rooms.** Tag a part `NPCSecure` inside a room and idle NPCs go clear it (breaking in if they must), hold it a few seconds, and move on. A fight interrupts them; they go back after.

### Fixed

- **NPCs stood still when told to face a spot while walking a path.** Facing set the root's CFrame every frame, which stopped the walk; they now face where they walk until they stop.
- NPCs no longer pick a window as a way in; entrances must reach from near the floor to above head height.

## 2026-11-10: Smarter NPCs

See [docs/ADDING_NPCS.md](docs/ADDING_NPCS.md) (Tactics).

### Added

- **Every NPC hears gunshots** (new `Hearing`, 150 studs, through the new `Gun.Fired` extension point). If it can't see the shooter it turns to the sound and hunts there.
- **Shoot to test.** An NPC that just lost sight of you, or heard you, fires at that spot through soft walls, soft floors, boards or smoke (never into open air or solid walls), and keeps firing while it keeps hearing you.
- **Breaching.** When an NPC has no path to where you are (a sealed room) and a board or soft wall is in the way, it shoots it open, then walks in once pathfinding finds the opening.
- **NPCs see through windows** (glass, or parts at least 0.3 transparent). They only fire when a bullet can actually reach you; otherwise they look for a way in.
- **NPC grenades.** Every NPC carries a frag grenade (`Grenades` 1, the Grenadier 3). It throws when you hide (1–8 s) or peek with only your head over cover (2.5 s), solving an arc that clears walls, never inside its own blast or near a teammate. Tested: a Soldier behind a 9-stud wall threw over it (peak 15.5 studs) and the grenade went off 0.6 studs from the hidden spot; it held its grenade for a spot 10 studs away, a spot by a teammate, and one 80 studs away.
- **NPCs dodge grenades.** Any NPC within a live grenade's blast (+4 studs) with no solid cover runs straight away, still shooting what it can see. Tested: two NPCs 4.5 studs from a grenade got 21–23 studs away before it went off and took no damage.
- `ConsumableService.ThrowAs(model, id, start, velocity)`, `NPCService.Agents()`, `Brain.SeeThrough` / `Penetrable` / `ShootThrough` / `BreachPoint`, and a `DetonateAt` attribute on thrown parts.

### Changed

- **Soft walls, soft floors and boards are no longer cover** for NPCs: bullets get through them.
- `ConsumableService.Detonate` takes an NPC model as the attacker (kill feed credit). NPC grenades don't hurt the thrower's teammates.

## 2026-11-10: Grenade lands heavy and breaks more

### Changed

- **Grenades and smoke bombs stay near where they land.** They're heavy and barely bounce, keep half their speed on landing, then roll about 2–4 studs to a stop (`Bounce`, `LandingKeep`, `RollDrag` in `Content.Consumables`). They used to roll away like a light ball.
- **Grenades remove more of boards and soft walls.** Board damage 80 → 350: a blast 4 studs from a board strips all 6 pieces (it took 2). Soft walls: hole 1.6 → 3.5 studs, reach 6 → 10 studs, up to 6 walls (was 3); a blast 2 studs from a wall removed 9.0 cubic studs of it (2.0 before). Player damage is unchanged. See [docs/CONSUMABLES.md](docs/CONSUMABLES.md).

## 2026-11-10: SMG sound and a new gun bash

### Fixed

- **The SMG's gunfire sound was silent.** The `RifleFire` sound file starts with about 0.3 s of silence. The SMG fires every 0.07 s with 4 pooled copies, so each copy restarted before it reached the bang. Gunfire now skips that silence (`Start = 0.3` on `GunFire_Rifle`; `PooledSound` takes a new `Start` field) and keeps 6 copies per muzzle. Checked: at SMG speed there was sound in 89 of 91 frames (0 of 61 before). This also removes a 0.3 s delay between the shot and the sound for every gun using `GunFire_Rifle` (Rifle, SMG, LMG and others).

### Changed

- **The gun bash is a long straight jab.** The gun pulls back toward the shoulder, then thrusts about 1.6 studs straight forward (full scale) with a slight cant, holds a beat, and snaps back. It stays on its own side of the screen instead of swinging across the middle. No camera shake. Tune the `BASH_*` constants in `Client.Guns.Viewmodel.Actions`. See [docs/ADDING_GUNS.md](docs/ADDING_GUNS.md).

## 2026-11-10: Tracers no longer come out of your face

### Fixed

- **Your own tracers start out at the barrel.** The viewmodel's muzzle sits about 1.2 studs from the eye (on the crosshair when aimed), so full-size tracers started there looked like they came out of your head. They now start on the same screen line but 4 studs out (`TRACER_START_DISTANCE` in `Client.Guns.GunEffects`), or just in front of a closer wall or target. Checked in a playtest: hip and aimed tracers first appear 4.0 studs out, at the barrel's spot on screen. Hits are unchanged (still from the camera). See [docs/ADDING_GUNS.md](docs/ADDING_GUNS.md).

## 2026-11-10: Stronger head aim assist

### Changed

- **Aim assist favors the head.** The head now wins about two thirds of the space between head and chest, gets 1.4× friction and 1.6× pull, and the assist sticks to the point it locked last frame so a small wobble doesn't drop it to the chest. Tuning: `HEAD_PREFERENCE`, `STICKY`, `HEAD_FRICTION_BOOST`, `HEAD_PULL_BOOST`, `MAX_FRICTION` in `Client.Guns.AimAssist`. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

## 2026-11-10: Aim assist holds headshots

### Changed

- **Aim assist sticks to the head or the chest, whichever is nearer the crosshair.** It used to know only the chest, so aiming at a head got pulled down to the body. Now aiming near the head holds the head. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

## 2026-11-10: Aim assist on PC for testing

### Added

- **`aimassistpc <player> [true/false]`** (alias `aapc`), an admin Cmdr command that gives a player controller aim assist on mouse and keyboard, so it can be tried on PC. With no true/false it toggles. It sets the server-side player attribute `AimAssistPC`, which `Client.Guns.AimAssist` reads; the Aim assist setting must also be on. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

## 2026-11-10: AI coding guide

### Added

- **[docs/AI_CODING_GUIDE.md](docs/AI_CODING_GUIDE.md):** one file to give any AI agent before it codes in the FPS place: the hard rules, where code lives, how ModuleLoader loads it, the module template and code style, the shared building blocks (packets, extension points, Scribe data, effects, states, input, Cmdr, products), world conventions, a feature walkthrough, testing and docs standards, and a done checklist.

### Fixed

- `API.md` said `Content` isn't loaded by ModuleLoader. It is, on both sides; most Content modules just return a table.

## 2026-11-10: Stronger aim assist

See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).

### Changed

- **Aim assist is stronger** (controller and touch). Cone 12° at the hip and 9° aimed (was 7° / 5°), covering 4 studs of body up close (was 2.2). Friction 50% / 70% (was 35% / 50%). Pull 7 / 11 per second (was 3 / 5), up to 120° per second (was 40°). The fade toward the cone's edge is now squared, so it stays strong over most of the cone. It still never moves the aim while the player is still.
- **Test rigs count as enemies.** `Rig`, `Rig1` and `Rig2` moved into `workspace.Enemies`, so they get health bars and aim assist.

## 2026-11-10: Grenade and smoke bomb

See [docs/CONSUMABLES.md](docs/CONSUMABLES.md).

### Added

- **Consumables.** Each player carries a frag grenade or a smoke bomb, picked in the Loadout menu (saved). They get 2 per life; the count refills on respawn, so it resets on death.
- **Throw with G** (rebindable, "Throw grenade / smoke"), gamepad DPad Right, or the NADE / SMOKE touch button (`Main.Mobile.ConsumableButton`, left of BASH, showing the count). A HUD line above the ammo box shows the name and count on keyboard and gamepad.
- **Frag grenade:** bounces, explodes after 3 s. 120 damage at the center falling to 15% at 16 studs, only through clear view, half damage to the thrower, kill feed credit and hitmarkers. It damages boards and holes nearby soft walls.
- **Smoke bomb:** pops after 1.5 s into a 13-stud cloud for 15 s. NPCs can't see through it and aim assist ignores targets behind it (`Shared.Smoke`).
- New: `Content.Consumables`, `Systems.Consumables.ConsumableService`, `Client.Guns.Consumables`, `Shared.Smoke`, the `Consumable` packets, the `Thrown` collision group, the `ConsumableThrow` and `SmokePop` effects, models in `Assets.Models.Consumables` and the `Assets.Vfx.SmokeCloud` particles.

## 2026-11-10: Touch buttons for bash and Cmdr

### Added

- **BASH touch button** (`Main.Mobile.BashButton`), above FIRE, shown with the other gun buttons; it does the same gun bash as Q.
- **CMD touch button** (`Main.Mobile.CmdrButton`) that opens the Cmdr bar, shown only to admins in `Classes.Admins`. The server still checks every command.

## 2026-11-10: API reference

### Added

- **[docs/API.md](docs/API.md)**: one page covering every public function, extension point, packet, Cmdr command, attribute, tag, data field and collision group, with recipes for common jobs.

## 2026-11-09: Decisions round (shop stand, keys, recoil, bash, debris, Revolver)

Follows the answers in [docs/DECISIONS.md](docs/DECISIONS.md).

### Changed

- **Crouch is Left Ctrl, prone is C** (swapped). Saved keys still on an old default move on join, and swaps work both ways (`Client.Settings.Keybinds` `MOVED_DEFAULTS`).
- **The skin shop is a stand in the lobby** (`Workspace.Lobby.SkinShopStand`), opened with its prompt (Interact, E). The I key and the Skin shop button are gone.
- **Lobby camera fixed.** The shop no longer forces a free mouse every frame in the lobby, so the camera turns again.
- **Recoil doesn't drag the aim back down.** After a spray, the aim stays where recoil left it and the player pulls it back. The old ease-back is kept behind `Recoil.RecoverAim = true` (default `false`, in `Content.Guns.Registry`).
- **Shotgun kick lowered** (Shotgun and SiegeShotgun: Vertical 4.5 / 6, ViewFlip 9, Kick 0.2).
- **New gun bash animation.** A timed windup, a cross-body strike and a smooth return (0.5 s, `Viewmodel.Actions`), replacing the spring jab.
- **A bash cancels a reload** (client and server: `GunService.CancelReload`).
- **Per-gun soft-wall holes.** Each gun's `SoftWallConfig.Guns[Id].HoleRadius` applies (Pistol 0.15, LMG 0.25, SMG 0.18, Shotgun pellets 0.15, and so on). BurstRifle explosive rounds stop at soft walls (`Penetrates = false`).
- **Door board prompt** reads "Door board".
- **Old helpers tidied** to house style (headers, `--!strict`), with these fixes:
  - `Services.PlayerJoin` sets the Player collision group when parts are added instead of scanning every character each frame; only the UpperTorso rule still runs per frame.
  - `Client.Hud.HealthBillboards` no longer errors without `workspace.Enemies`, and its waits time out.
  - `Handlers.AnimationHandler.RemoveAnim` works with numeric ids; `Handlers.StateHandler.SetStun` finds the Humanoid on the character.
  - `Client.Combat.CharacterHurt` drops an unused camera shaker. `Main`, `UI`, `CharacterAdded`, `CmdrClient`, `CursorAim`, `TableHelpers`, `UIHelpers`, `SetCollisionGroup`, `CmdrSetup`, `TokenBucket`, `UnreliablePackets`, `PersonalHealth`, `HealthUI` and `config` got headers.

### Added

- **Visible debris.** A broken plank falls as a copy of itself; soft-wall holes and chunks throw small chips. These are client-only effect parts (`Content.Effects.Parts.Debris`), faded and removed after a few seconds.
- **Revolver** is a gun (`Content.Guns.Definitions.Revolver`: semi, 48 damage, 6 rounds), with a Handle and attachments on its model, and a **Gunslinger** loadout (Revolver, Pistol, Knife).
- **`Shared.ProductIds`**: one module for every developer product and game pass id. The skin crate reads `Products.SkinCrate` from it instead of the old `SkinCrateProductId` attribute.
- **Crate refund.** Buying a crate with every skin owned gives 500 coins (`Skins.CRATE_REFUND_COINS`).

- **Aim assist for controller and touch** (`Client.Guns.AimAssist`): friction and a gentle pull toward enemies, stronger when aimed, never on mouse. Settings > Toggles turns it off. See [docs/AIM_ASSIST.md](docs/AIM_ASSIST.md).
- **The HUD scales with the screen.** Health, ammo, weapon slots and kill feed are sized in scale with aspect locks. On touch, the ammo box moves above the health bar, the weapon slots go top left, and small screens get a bigger HUD. The touch buttons keep their original pixel layout.

- **Skin crate product is live.** "Skin Crate", 499 Robux, product id `3730208338`, in `Shared.ProductIds`.

## 2026-11-09: Gun bash (melee)

### Added

- **Gun bash.** Press Q (rebindable "Melee" in Settings > Controls), click the mouse wheel, or press R3 on a gamepad to hit with any gun.
  - It deals 45 damage within 6 studs (35° cone) on a 0.9 s cooldown.
  - The Pistol is lighter and quicker; the Shotgun and LMG hit harder.
  - Scrolling the wheel still switches weapons.
- **Server-decided hits** (`Systems.Combat.GunMelee`).
  - Hits are credited like bullets: the kill feed shows "<Gun> bash", plus the hitmarker and DamageLog.
  - Each bash knocks one piece (the spray paint or a plank) off a board, and cuts a melee-sized hole in soft walls.
- **Animation.** A spring-based gun-jab in the viewmodel. It ends aiming, sprinting and inspecting, and isn't possible while reloading.
- **Config and hooks.**
  - Numbers and per-gun overrides live in `Content.Guns.Melee`.
  - New extension points `Gun.PreventMelee` and `Gun.MeleeHit`, and a new packet `Packets.Melee.Swing`.
- **Effects.**
  - New: `MeleeSwing`, `MeleeImpact`, and the soft-wall `SoftWallHole` and `SoftWallChunk` (stone knock, rubble and dust).
  - New sounds: `MeleeImpact`, `RockImpact`, `RubbleFall` (ProSoundEffects).

## 2026-11-09: Soft walls rebuilt

### Changed

- **Soft walls rebuilt (`Systems.Destruction.SoftWalls`).**
  - Every hit that lands on a wall while it waits or rebuilds is cut in one CSG pass, so a shotgun blast is one rebuild.
  - Caps limit rebuilds per frame, rebuilds in flight and cuts per rebuild. Nothing runs while idle.
- **Loose pieces fall as debris** instead of vanishing.
  - Debris doesn't collide with players, and bullets pass through it. It's removed after 8 s, with at most 20 pieces at once.
  - New support rule: `Auto`, `Bottom`, `Touching` or `All`, set per wall with the `SoftWallSupport` attribute.
- **Bullets lose damage through soft walls.** `PenetrationMultiplier` applies per wall and can be set per gun, up to 4 walls, without using up the gun's Pierce. Before this, the multiplier was never applied.
- **Square holes,** turned by a random angle (`HoleShape`, `HoleSpin`). Round holes cost about 10× more with the precise collision that holes need.
- **Melee and explosions.** Melee cuts 0.45-stud holes (source `"Melee"`). Explosions now damage boards whose planks have holes.
- **Config.** `Content.Destruction.SoftWallConfig` holds every soft wall number, with per-gun and per-source settings.

### Added

- **Cmdr commands** `softwallpunch [radius] [ring]` and `softwallreset [all]`.
- **Docs.** New `docs/SOFTWALLS.md`, plus updates to the shot flow in `GUN_SYSTEM.md`, a board note in `BREAKABLES.md` and a link in `GUN_GAME.md`.

## 2026-11-09: Gun recoil patterns, gun client refactor and Shotgun model fix

### Added

- **Recoil patterns.** Each gun has a learnable spray: the first shots climb straight, then the aim weaves side to side the same way every spray, with a small random part. The weave comes from a seeded curve or an authored `Recoil.Pattern`, and the spray starts over after `ResetTime`.
- **Camera and gun recoil are separate.** The camera (where you aim) and the gun in your hands (push-back, muzzle flip, twist, roll) each have their own spring. While you aim, the gun turns about its sights, so they stay centered.
- **Recovery respects your pull-down.** After firing, the aim returns only by the recoil you didn't already pull against, and never drags the view below where you put it.
- **Stance and fire rate.**
  - Multipliers for ADS, crouch (also used while sliding) and prone, plus a first-shot multiplier.
  - The springs stay fast enough that every shot of a fast gun still reads.
- **Per-gun feel.**
  - Rifle (steady), Pistol (snap), Shotgun (one big kick), Burst Rifle (tight burst), SMG (fast, jittery) and LMG (heavy, slow).
  - Every number is in the gun's `Recoil` table, with defaults in `Content.Guns.Registry`. See "Tuning recoil" in `docs/ADDING_GUNS.md`.
- **`Client.Guns.Recoil`.** Pure recoil math that can be tested from Studio's command bar.

### Changed

- **Viewmodel split.** `Client.Guns.Viewmodel` is now three documented parts:
  - the frame and API;
  - `Viewmodel.GunModel`: gun copies, skins, near guard;
  - `Viewmodel.Actions`: reload, inspect, knife swing.

  Behavior is unchanged.
- **House style.** SMG, LMG and Loadouts follow it now. The docs list the SMG and LMG, and the six loadouts with the knife slot.

### Fixed

- **Shotgun model.** The imported mesh had no Handle, so the Shotgun's viewmodel and muzzle were broken (boot warning "model Shotgun has no Handle part"). It now has an invisible Handle carrying Muzzle, Aim (on the sight line), RightGrip, LeftGrip (on the pump) and EjectionPort. The new look is unchanged.
- **Skins in first person** were drawn about three times too big. They're now applied at full size and scaled with the viewmodel.
- **Knife skin.** The knife no longer wears the Pistol's skin.
- **Skin changes** now update the viewmodel for every gun that has skins, not only the Rifle and Pistol.

## 2026-11-09: Skins, lobby and kill feed cleanup

### Changed

- **Lobby moved into the loader.** The loose `ServerScriptService.LobbySpawn` script is now `Systems.Lobby.LobbyService`, with the same behavior:
  - first spawn in the lobby;
  - the arena and return portals;
  - the `InLobby` attribute;
  - a 2-second portal cooldown.

  Portals now also check that the player is really next to them, and dying in the lobby gives your guns once on the next spawn instead of twice.
- **Skin shop uses Studio-built UI and packets.** The shop is `StarterGui.Main.SkinShop`, with `Main.SkinShopButton` and the `Assets.UI.Templates.SkinRow` template, instead of UI built by script. Requests go through `Packets.Skins.Equip` and `Packets.Skins.BuyCrate` instead of the runtime `SkinShopRemote`.
- **Skins are data.** `Content.Guns.Skins` describes each skin's colors, resized parts and detail parts. The saved `<Gun>Skin` fields and the shop are built from that list, so adding a skin is one entry.
- **Kill feed, Nuke and DoorBoard documented and tidied.** No behavior change. DoorBoard no longer shares tables with Board.

### Fixed

- **Skin shop on the server.** It no longer loads on the server (it had no `ClientOnly`).
- **Skin requests.** They're rate limited (4 per 2 s) and Ids are validated. Setting the crate product id mid-session no longer errors.
- **Cursor in the arena.** It no longer stays visible after you leave the lobby holding a gun.
- **Stale shop state.** The shop briefly showed the old "Equipped" state after equipping.
- **Music.** It stored the playlist folder as the "current song".

### Added

- **Docs.** `docs/SKINS.md`, `docs/LOBBY.md` and `docs/KILL_FEED.md`, plus a DoorBoard section in `docs/BREAKABLES.md`.

## 2026-11-08: Breakable boards and the Interact key

### Added

- **Breakable boards.**
  - At server start, every part tagged `Board` is replaced with `Assets.Models.Board`, positioned by its BasePart.
  - Damage removes the spray paint first, then planks from the highest number down (planks 60 HP, spray paint 25 HP).
  - Broken pieces hide and stop blocking players and bullets.
- **Board repair.**
  - Hold the Interact key on the board's prompt to place the next missing piece: planks 1 to N, then the spray paint last.
  - The server checks distance, cooldown and order.
  - Numbers are in `Content.Breakables.Definitions.Board`.
- **Guns damage boards.** Every bullet, including shotgun pellets and ricochets, damages the board piece it hits, and explosive rounds damage boards in their blast radius. Intact planks stop bullets like walls.
- **`Systems.Breakables.BreakableService`.** A weapon-agnostic API (`Damage`, `DamageRadius`, `Repair`, `Reset`, `IsBreakable`, `Get`) with `Breakable.*` extension points. New breakable types come from the data-driven `Content.Breakables` registry.
- **Interact keybind.** A rebindable Interact action (default E, gamepad DPad Up) in Settings > Controls. Every ProximityPrompt uses the player's Interact key and updates live when it is rebound (`Client.Interact.PromptKeys`).
- **Effects.** `BoardBreak` and `BoardPlace`, with ProSoundEffects wood-crack, hammer and spray-can sounds and a pooled `BoardDust` burst.
- **Docs.** New `docs/BREAKABLES.md`.

## 2026-11-08: Crouch on C, prone on Left Ctrl

### Changed

- **Controls.** C crouches (or slides while sprinting) and Left Ctrl goes prone; press Left Ctrl again to get up. Z no longer does anything by default.
- **Second crouch key removed.** `CrouchAlt` (Left Ctrl) is gone from `Shared.PlayerSettings`. The Settings menu now shows one "Crouch / slide" row (C) and "Prone" (LCtrl).
- **Saved keybinds move over.**
  - When keybinds load, `Client.Settings.Keybinds` moves a saved Prone still on the old default Z to Left Ctrl, and saves it through `Packets.Settings.Keybind`. It doesn't move it if the player already put another action on Left Ctrl.
  - Old profiles keep an unused `CrouchAlt` field, which Scribe loads without errors.
  - To move another default later, add its old key to `MOVED_DEFAULTS`.
- **Unchanged:** gamepad (B: tap crouch, hold prone) and touch (Crouch button: tap or hold).

### Fixed

- **Gun clipping into the camera.** Parts of the gun could come closer to the camera than its near clip plane, at high FOV and in the crouch and prone poses, which cut them off. When any part gets within `Config.ViewmodelNearClearance` (0.15), the viewmodel now eases forward along the view axis, never closer than `Config.ViewmodelNearMin` (0.11). Moving along the view axis keeps aimed sights centered. Built by an agent that was stopped before writing its report, so this hasn't had its full playtest yet.

## 2026-11-08: Prone, and viewmodel and tracer fixes

### Added

- **Prone.**
  - Lie down with Z (rebindable), hold gamepad B or hold the touch Crouch button. Press again, crouch, jump or sprint to get up; you stay down under anything too low to rise into.
  - Crawls at `ProneSpeed` (3.5). The eye is about 1.3 studs above the floor, and spread is best here (`Spread.Prone`, default 0.5).
  - No jumping and no footsteps. `ProneCooldown` applies between going down and getting up, on both client and server.
  - Sets the `Prone` attribute and StateHandler state, and adds the `Movement.PreventProne` extension point.
  - Third person: the body tips flat onto its front through `MovementPoses`, or plays `Config.Animations.Prone` if set. The viewmodel gets a braced prone pose.
  - The server registers the `ProneBody` collision group; the prone player's own body parts use it so the lowered torso can't lift the character.

### Fixed

- **Viewmodel disappearing or flickering while sliding and crouch-walking.** The viewmodel judged first person by the camera's distance to the head. The crouch and slide camera offsets and body poses pushed that past 1.5 studs. It now uses the camera mode and the camera's distance to its focus.
- **Shots starting at the camera.** Tracers and the muzzle flash now always start at the gun: the viewmodel muzzle while it's drawn, else the held Tool's muzzle. Before, they started at the camera whenever the viewmodel was hidden.
- **Stance changes read as falling.** Lowering the body (crouch, slide, prone) drops it onto the floor; that short fall no longer counts as the Air state.
- **Standing-up headroom check.** It now measures from the root part instead of the posed head.

## 2026-11-08: Movement, camera feel and FOV

### Added

- **Movement states.** Walk, Sprint, TacticalSprint (double-tap sprint), Crouch, Slide and Air.
  - Flags and the one transition table live in `Shared.Movement.States`.
  - Every tunable number lives in `Content.Movement.Config`.
- **`Client.Movement.MovementController`.** Runs the state machine on the client for instant response.
  - WalkSpeed ramps; HipHeight crouch with a headroom shapecast before standing.
  - A reused `LinearVelocity` drives slides (slope gain and loss, steering, cooldown) and carries slide-jump momentum with limited air control.
  - Footsteps run on a stride timer for this player and nearby others.
  - Keys come from Keybinds; the gamepad uses L3 and B; touch uses Sprint and Crouch buttons plus thumbstick auto-sprint.
- **`Client.Movement.MovementCamera`.** One RenderStep at Camera + 1, layered on the default camera.
  - Crouch and slide eye height on a spring, FOV kicks, strafe and slide tilt, a landing dip, and head bob tied to footsteps.
  - Gun recoil is in the same spring stack. CameraShaker is kept for impacts and explosions only.
- **`Systems.Movement.MovementService`.**
  - It checks each `Packets.Movement.SetState` against the transition table, cooldowns, grounded state and `Stunned` / `CantDoAnything`, and corrects with `Packets.Movement.Correct`.
  - It sets the `Sprinting`, `Crouching` and `Sliding` StateHandler states and attributes, plus `MoveState`, WalkSpeed and HipHeight.
  - It runs a 4 Hz speed check that logs and counts violations (`MoveViolations`) without kicking.
- **`Client.Movement.MovementPoses`.** Third-person crouch and slide leg poses for every character, from the replicated attributes. It uses `Config.Animations` ids through AnimationHandler when they're set, and works with Motor6D and AnimationConstraint joints.
- **Extension points.** `Movement.PreventSprint`, `Movement.PreventSlide` and `Movement.SpeedMultiplier`.
- **Settings.**
  - Actions `Sprint` (Left Shift), `Crouch` (C) and `CrouchAlt` (Left Ctrl).
  - `PlayerSettings.Options`, saved under `Settings.Options` through the new `Packets.Settings.Option`:
    - `Fov` (60–110, default 80) and `CameraBob` (0–100%);
    - `HoldSprint`, `HoldCrouch`, `MobileAutoSprint` and `SprintWhileReloading`.
  - `Client.Settings.Options` loads and applies them, previewing live while a slider is dragged.
  - Settings menu sections **Movement** and **Display**, with rows from the new `ToggleRow` and `SliderRow` templates.
- **`Client.Settings.Slider`.** The drag and snap logic shared by every settings slider; the volume sliders use it too.
- **Gun fields.** `SprintOutTime` (default 0.15) and `MoveSpeedMultiplier` (default 1), plus `Spread.Crouch` (0.7) and `Spread.Slide` (2).
  - Pistol: 0.1s and 1.05.
  - Shotgun: 0.2s and 0.95.
  - BurstRifle: 0.18s and 0.95.
- **Effects.**
  - Registry entries: `SlideStart`, `SlideLoop` (Persistent), `Land` and `Footstep` (variants Concrete, Grass, Soft, Wood and Metal).
  - A pooled `Dust` effect part.
  - Sounds in `Assets.Sounds` and the dust emitters `SlideDust`, `LandDust` and `StepDust` in `Assets.Vfx`.
- **UI.** `Main.Mobile.CrouchButton`, and the `SprintButton` wired with a label. The `MovementDebug` template.
- **Cmdr.** `movedebug` toggles an on-screen movement readout.
- **Docs.** `docs/MOVEMENT.md`.

### Changed

- **Viewmodel.**
  - It runs at Camera + 2, after MovementCamera, and no longer writes the camera's CFrame or FOV. Recoil, ADS zoom and scopes go through MovementCamera.
  - ADS FOV is `base × ADSFov / 70`, so zoom is the same at any FOV.
  - New crouch and slide poses.
  - At the hip, the gun's offset partly makes up for high FOV (`Config.ViewmodelFovCompensation`).
- **GunController.**
  - Sprinting blocks firing and aiming. The trigger or aim ends a sprint and waits `SprintOutTime` (×2 after a tactical sprint).
  - Spread uses the movement stance.
- **GunService.**
  - `tryShot` refuses a player's shot while sprinting or inside `SprintOutTime` (`MovementService.BlocksFire`).
  - The minimum spread accepts the crouch cone while the player is crouched.
- **`PooledSound`.** Supports `Looped` (until the effect stops) and a per-play `Data.Volume`.
- **`StarterPlayer.EnableMouseLockOption`.** Now off, since Left Shift is sprint.
- **Default Running sound.** Muted on every character, since footsteps replace it.

### Fixed

- **Aim tilt on newer R15 rigs.** Other players' upper bodies follow their aim again on characters whose joints are `AnimationConstraint`s, the newer Roblox avatar joints this place uses. `GunEffects` turns the constraint's `Attachment0` there, and still turns `C0` on `Motor6D` joints. Before, it only handled `Motor6D` and did nothing on these rigs.

## 2026-11-08: Kill sounds and NPCs with guns

### Added

- **Kill sounds.** `Assets.Sounds.KillConfirm` (the headshot sound at 0.75 speed, lower with a longer tail) and `KillThump` (the body hit at 0.55, a heavy low thump). The `Hitmarker` effect gets `Kill` and `HeadshotKill` variants; `GunHud.Hitmarker` picks HeadshotKill, Kill, Headshot or body, one per hit.
- **`Gun.Killed` extension point.** Fires `(who, victimHumanoid, gunId, headshot)` once per kill, for players and NPCs.
- **NPCs.**
  - Profiles: `Content.NPC.Profiles` (Soldier, Breacher, Grenadier), typed by `Content.NPC.Types`.
  - Rig, tree and spawning: the rig is `ServerStorage.NPC.Templates.Soldier`. The behavior tree `ServerStorage.NPC.Trees.Soldier` is in the BTrees Editor format.
  - Code: `Systems.NPC.NPCService` (spawning, respawns, round-robin scheduler, sleeping, aiming and shooting) and `Systems.NPC.Brain` (shared helpers and the `NPCWorld` blackboard).
  - Tasks in `Systems.NPC.Tasks`: FindTarget, HasLineOfSight, InRange, LowHealth, NeedsReload, MoveToCover, Strafe, Chase, AimAndShoot, Reload and Patrol.
  - NPCs on the same team don't hurt each other.
- **Cmdr.** `spawnnpc <profile> [count]` and `clearnpcs`, with an `npcProfile` argument type.
- **Test area.** `Workspace.NPCTestArea` (three NPCSpawn parts and cover crates) and `Workspace.Enemies`. The Enemies folder also fixes the existing `HealthBillboards` startup error.
- **Docs.** `docs/ADDING_NPCS.md`.

### Changed

- **`GunService` serves players and NPCs.**
  - Held guns are keyed by character, and a `Shooter` type is `{ Character, Player?, Id }`.
  - New functions: `ShooterOf`, `GiveNPC`, `FireAs`, `ReloadAs` and `RemoveShooter`.
  - Players' `Fire` packet handler is unchanged; both paths share the same shot checks.
  - Extension points get the Player or the NPC model.
  - Ability damage through `ctx.ApplyHit` now applies `Gun.DamageMultiplier`.
- **Shot context.** `ShotContext` and `GunContext` have a `Character`, and `Player` can be nil for an NPC. `Ballistics.Filter` and `ExplosiveRounds` use the shooter's character.
- **`Combat.ApplyHit` and `DamageLog`.** They accept a `Player` or an NPC `Model` as `Attacker`, and `DamageLog` records NPC victims too.
- **`UnreliablePackets.GunFired`.** It carries a UserId or an NPC Id. `GunEffects` finds NPC shooters by their `NPC` tag and `NPCId` attribute.
- **Client tracer pool.** It starts larger (40 per gun), so crowds of NPCs don't make it grow.

### Fixed

- **Kill detection.** A kill is reported only on the hit that takes health from above 0 to 0 or below, so a corpse or a second pellet never plays a kill sound again.

## 2026-11-07: Loadouts, weapon switching and settings

### Added

- **Loadouts.** `Content.Guns.Loadouts` lists Assault, Breacher, Grenadier and Arsenal (up to three guns each). `Systems.Guns.LoadoutService` gives the picked loadout on every spawn with `Slot` attributes and equips slot 1. The Loadout menu (`Main.Loadout`, `Client.Guns.LoadoutMenu`) opens on join and with `B`; the pick is saved in player data.
- **Weapon switching.** `Client.Guns.WeaponSlots` replaces the Roblox hotbar: keys 1/2/3, the mouse wheel, gamepad L1/R1, and the slot strip on the right side (`Main.Weapons`).
- **Settings menu.** `Main.Settings` (`Client.Settings.SettingsMenu`, key `P`) rebinds every action and sets Master, Effects, Music and Interface volume. Keybinds (`Client.Settings.Keybinds`) and volumes are saved in player data through `Packets.Settings` and `Services.SettingsService`.
- **Menus.** `Client.Core.Menus` tracks the open menu, frees the mouse in first person and stops gun input while one is open.
- **UI.** `Main.MenuButtons` (Loadout, Settings) and templates `LoadoutCard`, `KeybindRow` and `VolumeRow` in `Assets.UI.Templates`.

### Changed

- `GunController` reads its keys from `Keybinds` and rebinds when they change.
- `GunService.Give` sets a `Slot` attribute on each Tool.
- `AudioSettings.Store` now loads and saves volumes from player data instead of keeping them for the session only.

## 2026-11-07: Iron sights

### Changed

- **Iron sights.** Rifle, Pistol and Shotgun have a rear notch and a front sight (`RearSightL`, `RearSightR`, `FrontSight`), and each `Aim` attachment sits on the line through them, so aiming looks down the sights.
- **No scope on the Rifle.** The Rifle no longer has the `Scope` ability; it stays in `Content.Guns.Abilities` for a sniper.
- **Crosshair while aiming.** It shrinks as you aim in and hides halfway (`GunHud.AIM_HIDE`), so you aim with the iron sights alone.
- **Hit sounds.** The `Hitmarker` effect now plays the hitmarker click plus a body hit (`BodyHit`), and its `Headshot` variant plays `HeadshotHit` instead. Both are non-positional and louder than before, so they cut through gunfire.

### Fixed

- **Gun parts hanging off the handle in first person.** The viewmodel now swaps a gun's `WeldConstraint`s for fixed `Weld`s before showing it, so the order joints turn on can't leave parts behind.
- **Crosshair not visible.** `Main.Crosshair` was 0×0, so converting it to scale gave its lines infinite sizes. It is now 48×48 with its lines placed from its center.

## 2026-11-07: Gun system

### Added

- **Data-driven guns.** `Content.Guns` holds `Registry` (definitions with defaults and load-time checks), `Types`, `Definitions` (Rifle, Pistol, Shotgun, BurstRifle) and `Abilities` (ShotgunSpread, Burst, ExplosiveRounds, Scope, Ricochet).
- **Server.** `Systems.Guns.GunService` handles giving guns, equips, server-owned ammo and reloads, fire-rate checks (a minimum interval plus a `TokenBucket` per gun), origin clamping with a line-of-sight check, spread clamping and server casts. `Systems.Guns.AbilityRunner` handles per-bullet damage and server ability hooks. All damage goes through `Combat.ApplyHit`.
- **Shared.** `Shared.Guns.Ballistics` (seeded shots, one FastCast2 Serial caster per gun per side, hitscan traces, the pierce/bounce rule), `Shared.Guns.Abilities` (hook runner), `Shared.Guns.Spread` and `Shared.Guns.Spring` (both `--!native`).
- **Client.** `Client.Guns.GunController` (KB/M, gamepad and touch input; fire loop; reload; ADS), `Viewmodel` (first-person arms and gun with sway, bob, recoil, ADS, sprint and equip poses), `GunEffects` (local and replicated cosmetic shots, aim pitch), `GunHud` and `Quality`.
- **Networking.** A `Packets.Gun` group (`Fire`, `Reload`, `Aim`, `AltFire`, `HitConfirm`), plus `UnreliablePackets.GunFired`, `GunAim` and `GunAimRelay`.
- **Extension points.** `Gun.PreventFire`, `Gun.DamageMultiplier`, `Gun.Hit` and `Gun.Reloaded`.
- **States.** `Reloading` and `Firing` through `StateHandler`.
- **Effects.**
  - Registry entries: `GunFire_Rifle`, `GunFire_Pistol`, `GunFire_Shotgun`, `BulletImpact`, `Reload`, `DryFire`, `Hitmarker` and `Explosion`.
  - Pooled effect kinds: `MuzzleFlash`, `PooledSound`, `Shell` and `Impact`.
- **Assets.**
  - Gun models (`Assets.Models.Guns`): Rifle, Pistol and Shotgun, each with `Handle`, `Muzzle`, `EjectionPort`, `Aim`, `RightGrip` and `LeftGrip`.
  - Viewmodel rig: `Assets.Models.Viewmodel`.
  - VFX: `MuzzleFlash`, `BulletImpact`, `BulletHole`, `ShellEject`, `Tracer`, `TracerRed` and `Explosion`.
  - Sounds: `RifleFire`, `PistolFire`, `ShotgunFire`, `Reload`, `DryFire`, `Explosion` and `Hitmarker`.
  - UI template: `ScopeOverlay`.
- **UI.**
  - `StarterGui.Main.Gun`: ammo, reserve, fire mode and reload bar.
  - `Main.Crosshair`: the gap follows the spread.
  - `Main.Hitmarker`.
  - `Main.Mobile` buttons: `FireButton`, `AimButton` and `ReloadButton`.
- **Cmdr.** `givegun <player> <gunId>`, with a `gun` argument type.
- **Docs.** `docs/ADDING_GUNS.md` and `docs/GUN_SYSTEM.md`.

### Changed

- **`EffectService.Play`.** Takes an optional third argument, `except`: a player not to send the effect to. Existing calls are unchanged.
- **`Shared.Extensions`.** The header now lists the gun extension points.
