# UI

How the game's UI is laid out, how it should look, and how it feels. Revamped 2026-11-12 as the MVP pass: the lobby, the party, the Siege screens, one look for the menus, sound and motion on every button, and touch sizes. **Nobody has looked at it yet**: Studio was not rendering frames during the work, so everything was laid out and checked by measurement. See [Tested](#tested-2026-11-12).

## The rules

| Rule | Why |
| --- | --- |
| **One primary action per screen, and it is the biggest thing on it** | The lobby's is PLAY: big, green, bottom center. Fortnite, BedWars and Call of Duty all do this |
| **Secondary actions sit beside the primary, smaller and neutral** | PARTY left of PLAY, LOADOUT right of it |
| **Keep the middle of the screen clear in a round** | Anything that pulls the eye from aiming is a flaw. The menu buttons hide in Prep and Action |
| **Every button answers at once** | Squash on the way down (not on release), a click, a spring back. All of them, the same way |
| **Different actions sound different** | Hover, press, open, close, confirm, refused, tick, notify |
| **Touch targets are at least 40 px, 44 where there is room** | Apple's and Google's guidance is 44 to 48 |
| **Build it in Studio** | Scripts only show, hide, fill in text and color, and lay out. See the AI coding guide |

## Where the UI lives now

The ScreenGuis (`Main`, `SiegeSelect`, `DroneFeed`, `CameraFeed`, `ScanAlert`) are no longer in `StarterGui`. Another developer moved them under the LocalScript `ReplicatedFirst.UILoader`, which parents them into `PlayerGui` when the client starts. **Edit the UI there.** Where this doc says `StarterGui.Main…`, read `ReplicatedFirst.UILoader.Main…`. Templates are still in `Assets.UI.Templates`.

## UI standard and the Field look (2026-11-17, fourth look)

The owner asked for every screen to be redone again, from researched conventions and many references. This look is not modeled on one game: it follows published guidelines and the layouts most shooters share. The previous UI is archived in ServerStorage.Archive.UIBeforeField_2026_11_17.

### What the standard is based on

- Xbox Accessibility Guidelines 101 (text) and 102 (contrast), learn.microsoft.com/gaming/accessibility: body text at least 18 px at 1080p on PC, 4.5:1 contrast for text, 3:1 for large text and inactive items, contrast measured against the lightest part of a busy background, sentence case for lines of text, left-aligned text, at most about 80 characters a line.
- Game Accessibility Guidelines (gameaccessibilityguidelines.com): readable default text size, high contrast, never color alone, large well-spaced touch controls, simple clear text.
- Touch targets: Apple HIG 44 x 44 pt, Material Design 48 x 48 dp, about 8 pt between targets.
- Roblox Creator docs (UI/UX design, cross-platform design, on-screen containers): most important information first, bright color only for what matters, consistent close and lock conventions, CoreUISafeInsets for interactive UI, the bottom-left and bottom-right corners belong to the thumbstick and jump button, custom touch buttons placed relative to the jump button, only vital information on screen on mobile.
- Screenshots on the Game UI Database (gameuidatabase.com): Rainbow Six Siege (home, operator select, HUD, death screen), Call of Duty: Mobile (lobby, HUD, layouts, results), Battlefield 2042 (mode select, HUD, results, settings). Common to all: nav across the top, currency and settings top right, the start button bottom right, health bottom left, ammo bottom right, score and timer top center, kill feed top right, settings as tabs with rows of name left and value right.

### The rules (checked by an audit script over every label and button)

| Rule | Value |
|---|---|
| Smallest text | 12 px anywhere; 14 design px inside fitted menus (Store, Inventory, Details, Battle Pass). Labels that scale have a UITextSizeConstraint with that minimum |
| Contrast | 4.5:1 for text. Text on the mint accent, gold and team colors is dark (Theme.Ink, 11:1 on mint) |
| Touch targets | 44 px both ways (close buttons, settings gear, arrows) |
| Fonts | Titillium Web Bold for short capital labels, titles and numbers; Builder Sans (Roblox's UI font) for sentences |
| One accent | Signal mint (52, 224, 176) marks the main action, what is selected and progress, once per screen. Gold only for currency. Team colors always come with a letter, icon or word |
| Shape | Graphite glass panels, 6 px corners, 1 px hairline borders, a 2 px mint line along the top of every menu |
| Phones | A fitted menu never shrinks below 72% (it was 55%: 12 px text became 7 pt). Short class and weapon panels show a compact version |

The audit before the change found 716 of 767 labels that could shrink to any size, 101 labels under 4.5:1 (white on the old Siege blue was 3.5:1) and 37 buttons under 44 px.

### What changed

- **Content.Theme** is the Field palette and fonts. Theme.Map turns any older color into its Field role; it was run once over every GUI object (about 2,150 colors), and the hard-coded colors in 28 UI scripts were converted the same way. Fonts: 767 labels moved from Oswald and Roboto Condensed.
- **Client.Core.AutoContrast** (new): when code recolors a button at runtime (PLAY turning red to cancel, BUY turning OWNED), text on a bright fill turns dark and text on a dark fill turns light. A gradient that darkens a fill is taken into account (store cards).
- **Lobby**: one column in the bottom-right corner, where shooters put the start button: TRAINING and SQUAD side by side, the GAME MODE row with CHANGE, PLAY WITH PARTY, then PLAY, the one mint button, at the bottom. The Siege "< HOME" chip and the huge PLAY title are gone. On touch the column sits left of the jump button at the bottom edge. Settings is a 44 px gear icon (its key is in the tooltip). Client.Core.Matchmaking layoutBar places it.
- **HUD**: same conventional places, now on dark glass plates so they read over bright maps: the health plate with a heart icon and a white bar, the ammo plate with a mint stripe and fire mode, weapon slots with key chips, gadget rows. Score boxes have dark numbers on the team colors; control hints over the world have an outline.
- **Menus**: every menu has the same frame: title top left, tabs with a mint bar under the open one (Settings now matches the Store), a 44 px X icon top right, the mint line on top. The Game Modes screen is aligned to one left edge with a BACK button bottom left; mode cards have their own dark colors instead of all being the old blue, and ribbons are mint (RECOMMENDED, NEW) or orange (Fast).
- **Store**: ribbons mean one thing each (HOT red, POPULAR gold, VALUE green, NEW mint). The item borders (Neon Circuit, Rainbow, Obsidian, Secret) got their own colors back. Featured cards are two to a row from three columns up, so a phone shows two.
- **Inventory**: locked classes show a lock icon with the price under it instead of LOCKED text over the letter; the class text column no longer runs under the portrait.
- **End screens**: the round result band has mint rules and bigger scores; the death screen's spectating line is its own plate (the name no longer overlaps SPECTATING); big titles and numbers use the heading face.
- **New icons** in Content.Icons: settings, users, userPlus, user, heart, skull, eye, bomb, target, sword, shieldHalf, training, info, alert, plus, minus, search, up, down, refresh, map, mapPin, medal, award, clock, cctv, radar, scan, volume, gamepad, keyboard, monitor, leave.

### Checked

Studio playtests at 1920 x 783 and at a phone-sized 844 x 390 view (mouse input, so the touch layout itself was not shown): lobby, Shop, Inventory (both sizes), Settings, Party, Game Modes, the Recruit Training popup, the reveal screen, the drone feed and the soldier HUD in Recruit Training, and the round result, match result and death screens shown by hand. No errors in the Output.

Not checked: a real phone or tablet, the touch button layout, the Battle Pass screen (the pass is off), the camera feed, crate opening, the gift picker, a full 5v5 match. Not published.

### Bug fixes and the phone pass (2026-11-17, after the owner's test)

The owner found three bugs on screenshots and asked for a phone test; Studio's device emulator was set to a 750 x 382 touch screen, so this pass tested the real touch layout.

Bugs:

- **Crate icon beside class letters (Shop, CLASSES):** the StoreCard template's Glyph has `Icon = crate`. The Store wrote the class letter, then `Client.Core.IconBinder` saw the card arrive in PlayerGui and drew the crate again. Now any `Content.Icons` call from code marks the label `IconByCode`, and IconBinder leaves marked labels alone (`Icons.FromBinder` is set only while IconBinder itself applies a Studio label).
- **Prices missing on class cards:** the price sits in `Prices.Coins.Content.Amount`, two levels inside the button. It was dark text on the dark can't-afford button. `Client.Core.AutoContrast` now checks every text drawn on a fill, however deep, and the StoreCard template's text defaults to light.
- **"NE" and "INVENTOR" cut off:** boxes that size to their text measured it before Titillium Web had loaded. `Client.Core.UI` now waits for every font face the UI uses, then has every auto-sized box under PlayerGui measure again. Ribbons also have a 44 px minimum width.

Phone (touch) layout:

- **Menus start right under Roblox's top bar.** Main's coordinates already begin below the bar, but the menu fit added the bar's height a second time (58 of 382 pixels on a phone). The lobby nav room is now a `NavRoom` attribute (58) used only on screens taller than 600 pixels.
- **Compact menu headers:** on short screens Store, Inventory and Battle Pass (`CompactHeader` attribute) hide their title and put the tabs in the wallet and close row; Settings does the same in its own code.
- **The lobby nav row and the gear hide while a menu is open on a phone** (the menu has its own wallet and close); the coins sit beside the gear.
- **Settings on touch** hides the CONTROLS tab (keyboard binds) and opens GAMEPLAY.
- **HUD on touch:** health and ammo side by side in the bottom center, the weapon slots as one row of three tappable 45 px buttons above them (they were 13 px tall in the top-left corner, under the SCORE button), the SCORE button beside the gear, the score and timer bar and the bomb sites 30% bigger (`Client.Core.UI` TOUCH_LAYOUT and BOOSTS).
- **Recruit Training on touch:** the goal panel moves from the middle of the left edge (over the thumbstick and the drone and ability buttons) to the top-left corner at 72%, and steps show touch hints (`TouchHint` in `Content.Games.Tutorial`: "Stick drives · jump button hops" instead of "WASD drive · Space hop").
- **Game Modes:** the description moved up and BACK is pinned 12 px from the bottom, so they no longer overlap on a short screen.
- **Death screen:** the spectated name on the left and the respawn countdown on the right of one plate (both can show at once).

Checked on the emulated 750 x 382 touch screen: lobby, Shop (Featured and Classes), Inventory, Settings, Party, Game Modes, Recruit Training (prep and action, HUD and touch buttons), round result and death screen. No UI errors in the Output. Seen in passing, not UI: the server logged `DroneService:316` (`Content.Drones.HITBOX_PADDING` is missing) when it placed the training drone. Not checked: a real phone, the class pick page of the selection screen on a phone, a full 5v5 match. Not published.

### Guns as pictures and no overlaps on a phone (2026-11-17, second phone test)

From the owner's phone screenshot: pieces sat on top of each other, the weapon slots should show the gun rather than its name on mobile, and the kill feed should show the gun rather than text.

- **Kill feed (Client.Combat.KillFeed, rewritten):** each row is the killer, a picture of the gun, then the victim. The picture is the gun's own model (Content.Guns.Registry, found by Id, display name or model) drawn as a white silhouette in a small ViewportFrame through `Client.Core.ItemDetails.GunPreview`; a knife shows the knife; other kills get an icon (bomb for grenades and explosives, sword for melee, skull otherwise). Players in this server are colored by side (allies blue, enemies red), and a row with you in it has a mint outline. Rows have a fixed height (26 pixels, 22 on touch); on touch at most two show, so the feed stays between the settings gear and the right thumb's buttons. `Main.KillFeed` no longer clips its rows. The old text row (`EntryTemplate`) stays hidden.
- **Touch weapon row:** each slot shows the gun's model (the Preview viewport, wider view) with its key number small in the corner; the name is hidden.
- **Stacking on touch (Client.Core.UI `stackTouch`):** the weapon row is placed from the real top of the health and ammo plates, the objective line and the bomb sites from the real bottom of the (bigger) score bar, so they never overlap whatever their sizes. Health and ammo sit 8 pixels above the bottom edge (they were cut off). The objective line is 40% bigger on small touch screens.
- **Training goal panel on touch:** shrinks further (down to 50%) when a hint row makes it taller, so it always ends above the left touch buttons.
- **Banners on a phone (Content.Effects.Parts.Banner):** on screens up to 500 pixels tall they settle just under the crosshair (58% down) instead of 30% down, where the score bar, objective and bomb sites now are.

Checked on the emulated 750 x 382 touch screen in Recruit Training, with test kills sent from a temporary server script (a rifle kill, your own kill with the Ak-47, a grenade death): no overlaps, no UI errors. Not checked: a real phone, a real kill, the drone feed on a phone (the training drone is not placed: `DroneService:316`, `Content.Drones.HITBOX_PADDING` missing), desktop after these changes (the emulator stayed on). Not published.

### Held weapon slot and the training stepper (2026-11-17, third phone test)

- **Held weapon slot (Client.Guns.WeaponSlots):** a lighter gray than the other slots (Content.Theme Card) with a white outline and light text; the mint stripe is gone. It was a light fill with dark text and a mint outline, which the owner found odd.
- **Training stepper (Client.Hud.Tutorial):** on touch, or when the panel has less than 70 design pixels per step, only the current step is named under its circle; the others are numbers (the title says what to do). The labels used to run together ("BREACHPLANT"). Rows in the goal panel have 8 pixels between them (6 before) and the links between steps are a little longer.
- **Hint on touch:** once the hint appears, it takes the description line's place, so the panel does not grow over the left touch buttons; a new goal shows its description again.

Checked on the emulated 750 x 382 touch screen in Recruit Training (attack round). No UI errors in the Output. Not published.

### No mint in play (2026-11-17, fourth phone test)

The owner found the mint accent out of place on the in-match screen (the training help panel did not match the other plates, the mint stripe on the ammo panel, the mint AUTO, the mint outline on your own slot in the top bar). New rule, written into `Content.Theme`: the accent is for menus; in play the HUD is white, gray and team colors only.

- **Training help panel (StarterGui.Training.Goal):** the same glass plate as the health and ammo plates (Panel at 30%, 1 px Line outline, 6 px corners); the stepper, count bar and hint are white and gray; the bonus chip is a gray chip (its star is gold).
- **Ammo panel:** the mint stripe is gone; the fire mode (AUTO) is Muted gray; the reload bar is white.
- **Top bar:** your own slot has a white outline (Assets.UI.Templates.TopBarSlot `Me`); the line under the clock is gray.
- **Everything else in play** (Main's HUD frames, DroneFeed, CameraFeed, the training panels and the HUD templates): mint became white, the dim accent gray and the accent wells gray cards. In code: the planted defuser and gadget meters (drone boost and health, scan hold, Dead Call) are white, the Leo motion warning is gold, the scoreboard's first place is gold, the picked gadget row and your kill feed rows have a white outline.
- **Results:** a won round and your side are ally blue (Theme.Defend), lost rounds red, a won match gold; the round result's rules are white.

Checked on the emulated 750 x 382 touch screen in Recruit Training. No UI errors in the Output. Seen during the test: `Content.Store.Store` had a syntax error for a moment (line 188, a new BarrierSpecialist class being added by the other developer), which stopped the data and store modules from loading; it was fixed when tested again. Not published.

### Pop-ups in free lanes, compact training panel (2026-11-17, fifth phone test)

The owner: pop-ups kept covering things, and the training steps covered the touch buttons.

- **Phase banner at the bottom (Content.Effects.Parts.Banner):** a banner that starts while the selection screen is up settles at the bottom edge, between that screen's ready counts. The Prep banner starts just before the reveal screen closes, so it stayed at the bottom over the health bar and weapon row for its whole four seconds. It now moves to its normal place the moment the selection screen closes. On phones that place is 60% down: the free strip between the crosshair and the weapon row. Its second line is gray, not mint.
- **Pop-up lanes on touch (Client.Core.UI `stackTouch`):** short notices (SiegeHUD.Toast) sit just under the bomb sites, and the planting bar (SiegeHUD.Plant) just above the weapon row; at their desktop places (78% and 70% down) they covered the weapons on a phone.
- **Training panel on touch (Client.Hud.Tutorial):** only the goal's title and one line (the description, or the hint once stuck); the stepper and the bonus chip are hidden on touch, so the panel is short and never reaches the left touch buttons. It rests at 85% on phones (it still shrinks if it would reach them).

Checked on the emulated 750 x 382 touch screen in Recruit Training, including a banner started with the selection screen up and then closed. No UI errors in the Output. Not checked: a notice (Toast) and the planting bar on a phone in a real round. Not published.

### Drone and camera feeds on a phone (2026-11-17, sixth phone test)

The owner: the objective took too much of the screen on mobile, and the training panel covered important information in the drone feed.

- **Phone layout by size too (Client.Core.UI `isPhone`, Client.Hud.Tutorial `phoneLayout`):** the phone layouts switch on for touch or for a screen whose shorter side is up to 500 pixels, since an emulated (or real) phone can report keyboard input. The owner's screenshot showed the desktop places because of that.
- **Feeds (DroneFeed, CameraFeed; `layoutFeed`):** on a phone the header (DRONE 1, LIVE) moves below Roblox's top-bar buttons, which covered it, and the OBJECTIVE box becomes a compact two-line tag (the goal and the place, no caption). The compass (300 pixels) and the boost row (240) are narrower so they end before the feed's BOOST touch button. Desktop places are saved in attributes and come back on bigger screens.
- **Roblox's touch controls hide while a feed is up on touch:** the feed has its own DRIVE stick and HOP button; Roblox's thumbstick and jump button sat under them. They come back when the feed closes (Client.Core.Menus does the same for menus).
- **Training panel in a feed:** on a phone it takes the place of the feed's objective tag, under the header (the tag says the same goal and hides while the panel shows), so the compass, boost bar and the touch buttons (EXIT, SPOT, HOP, BOOST) stay clear.
- **Drone boost (Client.Gadgets.DroneBoost):** the drone controller is being edited by the other developer and an earlier fix to it was overwritten, so the boost module now meets the controller as it is: it reads the clock itself (the controller passes `dt`) and keeps `state.Bars` for the feed. The feed no longer errors every frame, and its label shows BOOST n/3 (it read "Label").

Checked on the emulated 750 x 382 touch screen in Recruit Training: the prep drone feed, then the action phase (feed closed, Roblox's controls and the objective tag back). No errors in the Output. Not published.

### Exit buttons on a phone (2026-11-17, seventh phone test)

EXIT sat over SPOT in the drone feed (and over SCAN in the camera feed) on a 334-pixel phone, because one was placed from the top and the other from the bottom. On phones `Client.Core.UI` (FEED_TOUCH) now places the feeds' touch buttons: EXIT in the top-right corner beside the score bar (NEXT drone left of it), the drone's integrity bar under them, SPOT under that, HOP and BOOST at the bottom right; the camera feed's SCAN, PREV and NEXT stack up from the bottom right; the NoSignal screens use the same places. The decorative corner brackets are hidden on phones (they ran through EXIT).

An overlap check (every visible button on screen, any pair overlapping) at 750 x 382 touch found none in the lobby, Shop, Inventory, Settings, Party, Game Modes, the drone feed, the camera feed's buttons and the match HUD. Then checked in play on the phone emulator: the drone feed in Recruit Training's attack round (corner brackets hidden, EXIT clear) and the camera feed in its defend round (reached with SiegeService.ForceEnd from a temporary server script). Fixed there: the feeds' text drawn straight over the 3D view (header, integrity, boost row, notices) has a dark outline (it was hard to read over light walls); the camera feed's PREV and NEXT use the chevron icons instead of typed < >; the training panel keeps its phone size inside a feed (it shrank against the match's left buttons, which are hidden while a feed is up). No errors on the client or the server. Not checked: a real phone. Not published.

### Nothing to see or build from a camera, a drone or death (2026-11-17)

The owner: no building while on cameras; no billboards while dead, on a camera or in a drone.

- **`Client.Core.ViewHide` (new, ClientOnly):** while the player is dead (no living Humanoid outside the lobby, or Main.DeathScreen showing), looks through a security camera (`CameraViewing` attribute or the CameraFeed up) or drives a drone (`DroneControlling` or the DroneFeed up), every BillboardGui in the workspace and PlayerGui is turned off (names, health bars, prompts, bomb marks, streak tags, hit numbers), and billboards made or re-enabled meanwhile are turned off too; they come back afterwards. The scan marks (`SpotMarker`) stay, since spotting is what drones and cameras are for. Interaction prompts are off for that client (`ProximityPromptService.Enabled`). State is checked five times a second.
- **Server:** `Systems.Breakables.BreakableService` `builderIsValid` refuses a player who is looking through a camera or driving a drone, so a doorway can't be started or kept building from there (a build in progress is cancelled at its next step). `Systems.Classes.Abilities.Reinforce.Use` refuses the same ("Leave the camera first.").
- **Round result over a death:** a death that ends the round brought the death screen up just after ROUND LOST, under it ("You died" under the band, seen on a phone). `Client.Hud.SiegeHud` now keeps the death screen and the spectate bar hidden while the round or match result shows.

Checked in Recruit Training on the phone emulator: in the drone prompts are off; in the body the bomb marks show and prompts are on; dead, prompts are off and the result shows alone; on a camera the bomb marks are hidden and prompts off, and a temporary server script's attempt to start each of the 42 unfinished doorways was refused (the same attempt started building once out of the camera). No errors on the client or the server. Not published.

### Spectate screen (2026-11-17)

The owner: the spectate screen looked cluttered and janky. It was three loose pieces stacked in the bottom centre (the "<" ">" spectate bar with two floating lines, the killed-by card, and a SPECTATING plate whose one-life line ran into the name), with the weapon row, the touch buttons and Roblox's thumbstick still on screen.

Now:

- **One plate at the bottom centre** (Main.DeathScreen.Bottom, 440 x 60): SPECTATING over the watched player's name, centred. Siege's spectate bar (Main.SiegeHUD.Spectate) lies exactly on it, so PREV and NEXT are chevron buttons at the plate's two ends; its hint (WATCHING TEAMMATES, and the keys on desktop) is a small line just above. The status (respawn countdown, or "One life. Spectating until the round ends.") is a small line just under the plate, or alone inside it while nobody is watched (`placeStatus` in Client.Hud.DeathScreen). The bar's separate "ELIMINATED · ONE LIFE" line is gone.
- **The killed-by card** sits at the top left, below the score bar's row (16, 60; 226 x 56), clear of the bomb sites on a phone. (Deleted on 2026-11-18: the killer is in the plate. See below.)
- **While dead, the gameplay controls hide** (Client.Core.ViewHide): Main.Mobile, Weapons, Gun, Consumable, DroneSlot, Crosshair and SiegeHUD.Ability, and Roblox's thumbstick and jump button. Each comes back as it was on respawn.

Checked in a private 5v5 with four bots on the phone emulator: died in prep and watched a teammate. No errors. Not checked on desktop size (the emulator was on). Not published.

### Death screen killer line, and less text everywhere (2026-11-18)

The owner: the killer on the death screen overlapped the UI; remove every unnecessary piece of text. Every label in every screen was listed (Main, the menus, the templates, the feeds, the selection screen, training) and each one that repeated something already on screen, or told the player what the screen already shows, was removed. What a label says that nothing else says stays (timers, scores, AUTO, the objective, the round result, key hints on desktop).

**Death screen (Client.Hud.DeathScreen, Client.Core.Spectate):**
- The killed-by card at the top left (`Main.DeathScreen.Card`: ELIMINATED, "Killed by", "with", avatar) is deleted. The killer is in the bottom plate instead, so nothing sits over the score bar, the bomb sites or the kill feed.
- The plate's caption says what the name under it is: **KILLED YOU · RIFLE** while the camera follows your killer, **KILLED BY · RIFLE** while nobody is watched, **SPECTATING** (or **SPECTATING ENEMY** once no teammate is left) for anyone else. The name is red (Theme.Danger) for your killer and for enemies, white for teammates.
- With one life (Siege) there is no status line under the plate while you watch someone; alone in the plate it reads "Out this round". The countdown ("Respawning in 3") stays in modes with respawns.
- The spectate hint no longer says WATCHING TEAMMATES / NO TEAMMATES LEFT; it is only the keys (Fire next · Aim previous, or R1 / L1), under the plate, and nothing on touch (the arrows say it). The bar keeps a `Mode` attribute ("Team", "Enemy" or "") that the caption reads. The unused `Spectate.Out` label is deleted.

**In play:**
- Ammo panel: no gun name (`Main.Gun.GunName` hidden); the picture beside the ammo shows the gun.
- Health: the current number only ("100", not "100/100"). Client.Hud.PersonalHealth writes it; the bar still animates through Classes.HealthUI.
- Bomb chips: only the letter until a defuser is planted (no "NO DEFUSER"), then the letter and PLANTED.
- Top bar: PREP instead of PREPARE (it was cut to "PREPA" in a feed on a phone). The objective line has no phase word in front ("Defend Upstairs", "Find the site"), since the top bar says the phase.
- Drone and camera feeds: no LIVE in the header (the camera keeps "1 of 3", and OFFLINE when destroyed), no OBJECTIVE caption over the objective tag (the tag is shorter, 340 x 52), no heading in degrees under the compass, no BOOST word before the boost bar (BOOST 3/3 is over it).
- The phase banner stays at the top centre while a feed is open on a phone (Content.Effects.Parts.Banner `topFor`): at 60% down it covered the feed's compass.

**Lobby and menus:**
- PLAY has no second line (the GAME MODE row names the mode; SEARCHING is the status line's). It keeps one for a party member ("YOUR LEADER QUEUES") and for PARTY TOO BIG. With no second line the label sits in the middle of the tile (Client.Core.Matchmaking `subLine`).
- PLAY WITH PARTY: no "PRIVATE 1 V 1 · 3 PLAYERS" line (the tiles above show the mode and the party size); a member still reads "YOUR LEADER STARTS IT".
- TRAINING: FREE CRATE or OPEN CRATE while there is something to get, otherwise no line (no PRACTICE).
- GAME MODE: a chevron instead of the word CHANGE.
- Mode cards: no SELECTED label (`Templates.ModeCard.Picked` deleted); the outline shows the pick.
- Store: no section header repeating the open tab (Crates over the crates); the Featured page keeps its Daily Deal (with the timer) and Crates headers.
- Selection screen (Client.Core.SiegeSelect): no "NEXT: PICK WHERE YOU SPAWN" line under the steps (`Header.Next` deleted), no rule lines on the location, class and ready pages (they were cut off on a phone, and the lists show free and taken), no "TOP VIEW" caption, no "pick in the list or on the map" legend (the legend's box hides while empty), the cutaway caption is only the site's name, and stacked site pins are named only when picked or pointed at. ROUND 1/5 instead of ROUND 1 OF 5, which was cut off on a phone.

Also fixed in passing: in Client.Core.Matchmaking, the lobby column's watchers for the screen size, the training tile and PLAY WITH PARTY were connected inside the input-change handler, so they only started after the input type changed.

Checked on the emulated 750 x 382 touch screen: the lobby, the Store, a private 5v5 with four bots (selection screen, drone feed, prep and action HUD), and two deaths (to an enemy bot: KILLED BY / KILLED YOU · RIFLE in red; then SPECTATING a teammate). No errors in the Output. Not checked: desktop size and the keyboard hint, a camera feed, and the objective line without the phase word (changed after the last run). Published on 2026-11-18 at 16:01 UTC (place version 992).

## Mobile pass (2026-11-13)

Sized and placed after other Roblox shooters on a phone (BedWars, Rivals and similar): a small timer pill at the top, nothing behind Roblox's top-left buttons, a column or row of small square buttons on the left, a big fire button with smaller ones in an arc for the right thumb, thin bars at the bottom, short messages instead of boxes over the view.

| What | Now |
| --- | --- |
| Touch buttons | Icons (`Mobile.<Button>.Icon.Glyph`), not words. FIRE 1.15 of the jump button; AIM 0.72; crouch and reload 0.62; melee and grenade 0.6; sprint 0.65; drone or camera and ability 0.66; admin 0.55. Left row (drone or camera, ability, admin) 2.55 buttons up from the bottom; right arc around the jump button with a gap between each |
| Button labels | Hidden, except the grenade (`2`), drone (`x1`, `OUT`, `LOST`, `12s`) and ability (`x1`, `12s`) counts, shown small under the icon |
| Phone boost | Health, ammo box, weapon slots and kill feed are 1.15 times their desktop size on a phone (was 1.6) |
| Siege top | Timer pill (`SiegeHUD.Timer`, 0.11 × 0.07 of the screen, 4 px from the top), SCORE beside it, then the objective line, then the A and B chips (one line each) |
| Announcement banner | `Content.Effects.Parts.Banner`: 36% of the screen width (240 to 460 px), at 30% of the screen height, smaller text below 500 px tall |
| Death screen | Card 320 × 56, SPECTATING line and countdown 320 × 46, both at the bottom centre above Siege's spectate bar (340 × 40, 6 px from the bottom) |
| Round end | `SiegeHUD.End` is ZIndex 12 (its contents 13+, and `SiegeKillRow`); when it opens it hides the death screen and the spectate bar |
| Menu buttons | `MenuButtons.TouchScale` = 0.8 on small touch screens |
| Roblox's health bar | Off (`Client.Core.UI`); the HUD has its own |

### Full-screen menus that fit (`FitScale`)

The Siege selection screen is laid out in pixels. A UIScale named `Fit` in `SiegeSelect.Screen.Content`, tagged `FitScale`, makes it fit any screen:

| Attribute | Meaning |
| --- | --- |
| `DesignHeight` | Pixels of height the layout needs (490). The scale is the free height over this, between 0.55 and 1 |
| `WidthShare` | Share of the screen width the frame covers (0.94), kept whatever the scale |
| `BelowTopbar` | The frame starts under Roblox's top bar (`GuiService.TopbarInset`, 58 px) |

`Client.Core.UI` sets the scale and the frame's size and place when the menu arrives in `PlayerGui` and whenever the screen or the top bar changes. On a 844 × 390 phone the scale is 0.645: three class cards show, the Loadout column fits above Ready, and all four site names show in full. On a desktop it is 1 (no change). `Client.Core.SiegeSelect` divides the roster's on-screen width by the scale when it sizes the pages. To fit another pixel-built menu, give it the same tagged UIScale.

## Touch buttons (2026-11-12, not run)

The sizes below were replaced on 2026-11-13 (see above); the way they are placed is the same.

`Client.Core.UI` places and sizes every button in `Main.Mobile` from one table, `TOUCH_BUTTONS`, in units of one touch button (70 px on a phone, 120 on a tablet; the `Mobile` frame sits exactly on Roblox's jump button).

| Group | Buttons | Placed from |
| --- | --- | --- |
| Right thumb | FIRE (1.3, the biggest, beside the jump button), AIM (0.9, above the jump button), crouch, reload (0.8), melee, grenade (0.7) | The jump button's center |
| Left | Sprint (0.8, beside the thumbstick); drone or camera, ability, admin console in a row above it | The screen's bottom-left corner |

- Worked out for 812 × 375, 667 × 375 and 1180 × 820: no button overlaps another or the jump button, none is off screen, the smallest is 46 px and the closest gap 4 px.
- The right cluster's top is at y = 152 on a 375-tall phone. Before, it ran up the whole edge: the grenade button's top was at y = 4.
- Before, the left buttons were placed from the right corner, so on a screen narrower than about 893 px the sprint button was partly or wholly off the left edge.
- To move a button, change its row in `TOUCH_BUTTONS`. The sword's Swing and Grab buttons are not in the table and keep their Studio place.

## Names and health bars (2026-11-12, not run)

`Client.Hud.Nameplates` sets, on each client, how other players' characters show their name and health: a teammate (same `Team` attribute) always shows both; an enemy shows neither; with no teams (the lobby) it is Roblox's default. Display only.

## Rebuilt layouts (2026-11-17, third pass)

| Screen | Layout |
| --- | --- |
| Lobby (`Main.Lobby`) | DEPLOY card, bottom right: Head, ModeButton row, Play (big, arrow), PartyPlay + PartyButton (halves), Training row; Status above the card. Sized and placed by `Matchmaking.layoutBar` (340 x 238; touch: 112 px up, 0.78 scale on screens 600 or less tall) |
| Wallet (`Main.Wallet`) | Horizontal strip top left: Coins, Buttons (Inventory, Store), PassButton |
| Store / Inventory cards (`StoreCard`) | `Stripe` (item color) on top, art centered, ItemName and Subtitle bottom left, Detail/OldPrice bottom right, Prices row, Tag top left, Bonus/Count top right |
| Pages | Store, Inventory, Details, Battle Pass: `WidthShare` 0.97, `BelowTopbar`, max 1600 x 900 |
| Touch | Combat buttons hidden in the lobby. Touch buttons and the crosshair use `ScaledSize` strokes: thickness is a share of their size (0.03 to 0.5), never pixels |


The first theme's colors (Midnight / Aqua / Pink, below) were replaced the same day with a tactical, Siege-like style. `Content.Theme` holds it:

| Token | Color | Use |
| --- | --- | --- |
| Void | `#07090C` | Dimmers and backdrops |
| Base | `#0E1116` | Menu frames (glass: 6% see-through over the blurred world) |
| Panel / Raised / Card | `#141821` / `#1B2029` / `#252B36` | Panels, rows and cards, chips and inputs |
| Line | `#343C4A` | 1 px hairlines and outlines |
| Accent (Amber) | `#F0B43C` | The one main action (filled, Ink text) and what is selected; the bar on top of every menu |
| Text / Muted / Faint | `#EDF0F4` / `#8C95A5` / `#5C6575` | Text |
| Danger / Success | `#E5484D` / `#4CC38A` | Only where they mean it |

Type: Gotham (`Theme.FONT`, `FONT_BOLD`). Corners 4 (6 on big panels). Team colors (orange attackers, blue defenders), bomb colors (red A, blue B) and rarity colors keep their meaning.

**One frame for every menu:** amber 2 px bar on top (`HeaderBar`), title left in capitals, close right, the same nav buttons, rows and cards. While a menu is open the world is blurred (`Client.Core.MenuAmbience`, `Theme.BLUR`). Fixed-size text always has a `UITextSizeConstraint` (its design size as the most) and `TextScaled`, so it shrinks instead of spilling out.

**Settings** are tabs (`Main.Settings.Tabs.Row`): CONTROLS, GAMEPLAY, DISPLAY, AUDIO.

The UI before this is in `ServerStorage.Archive.UIBeforeTactical_2026_11_17`.

## Icons, not emoji (2026-11-17)

No label shows an emoji or symbol glyph any more: emoji draw differently on every device and don't fit the Siege look. Every icon is a white line icon from the Lucide set (ISC licence), from two sprite sheets in the Creator Store (`rbxassetid://134788982523503` and `rbxassetid://122251837315841`, 24 px cells). `ReplicatedStorage.Content.Icons` lists them by name and draws them; it tints each icon with the label's text color.

| Name | Shows | Used for |
|---|---|---|
| crate | package | crates (cards, Battle Pass rewards, Recruit Training reward) |
| gift | gift box | GIFT buttons, Bundles section |
| lock | padlock | locked cards and pass rewards |
| timer, zap | stopwatch, lightning | daily deal countdown, ability cooldown and charges |
| star | star | Featured, Battle Pass, perks, tutorial bonus |
| flame | flame | HOT DEAL tags, the 1 V 1 "Fast" tag, win streaks (scoreboard, the StreakTag over heads) |
| crown | crown | game passes, the VIP dog tag charm |
| token | gem | Siege Tokens amounts and the Currency section |
| classes, skins, helmet | swords, palette, hard hat | Inventory and Store sections |
| check | tick | OWNED, CLAIMED, done steps and quests |
| cart, backpack, quests | cart, backpack, scroll | nav icons |
| play, left, right, back, arrowUp/Down/Right | arrows | PLAY tile, HOME chip, BACK and CONTINUE buttons, option arrows, D-pad key prompts |
| objective | crosshair | the line under the phase banner |

How to use it:

- **Studio-built labels:** give the TextLabel or TextButton an `Icon` attribute (a name above) and, unless the icon goes before the text, `IconMode` = `Trail` (after the text) or `Glyph` (icon only). `Client.Core.IconBinder` applies it to everything in PlayerGui, clones included.
- **Code:** `Icons.Glyph(label, name)`, `Icons.Lead(label, name, text)`, `Icons.Trail(label, text, name)`, or `Icons.Text(label, value)` for data strings: `":flame: HOT DEAL"` (icon first), `"CONTINUE :right:"` (icon last), `":crate:"` (icon only). A value that is not an icon name shows as text (a class's initial, "x2").
- **Data:** `Content.Store.Store` SECTIONS `Icon`, store entries' `Glyph` and `Tag` hold icon names or `:name:` strings.
- The icon sits over spaces in the text, so it follows any alignment, padding and UIScale. If other code writes a different Text to the label, the icon hides itself.
- Not in PlayerGui: the StreakTag BillboardGui has a fixed `Flame` image beside its number, and the VIP charm's SurfaceGuis have a `CrownIcon` image.

Kept as text: the separators `·` and `—` and the degree sign on drone and camera compasses. Coins keep their coin picture (`Content.Store.Style.COIN_ICON`).

## Siege style (2026-11-17, third look, replaced by Field)

Modeled on Rainbow Six Siege's menus (the owner's reference: Game UI Database, game id 264). The look before it is in `ServerStorage.Archive.UIBeforeSiege_2026_11_17`.

**Palette** (`Content.Theme`): slate navy. Void `#090C12` (dimmers, shades), Base `#161B25`, Panel `#212733` (menus), Raised `#2E3543` (rows, cards), Card `#3E4757`, Line `#5C687C`, **Tile** `#7A899A` (light slate tiles), **Well** `#0A0C10` (the black value box of an option row). **Accent** Siege blue `#248EE2` for the main action and what is selected, AccentDim `#1A64A2`, AccentWell `#14324E`, **Highlight** `#C4E2F6` (pale blue outline on the selected tile). **Gold** `#F6C61E` only for currency, NEW tags and the objective line. Text `#EEF1F5`, Muted `#9CA7B7`, Ink is white (text on blue). Attack `#E8701E`, Defend `#1E88E6`.

**Type:** Oswald Bold (`FONT_BOLD`) for titles, nav words, buttons and numbers; Roboto Condensed Medium (`FONT`) for body text. **Shapes:** square (`CORNER` 0); circles stay circles.

| Piece | How it looks |
| --- | --- |
| Nav bar (`Main.Wallet`) | Big condensed words across the top: HOME, SHOP, INVENTORY, BATTLE PASS. The open one is white and underlined (HOME when no menu is open; `Store.lua` `lightNav` on `Menus.Changed`). Coins in gold at the right; SETTINGS [P] is a dark outlined box at the top right. A dark band (`Main.NavShade`) sits behind it in the lobby |
| PLAY page (`Main.Lobby`) | A notched "◀ HOME" chip, a huge PLAY title, then tiles: the blue PLAY tile (outlined pale blue), GAME MODE (dark slate, "CHANGE ›"), PLAY WITH PARTY (dark blue, only when a party can play privately), and a column of two light slate tiles, TRAINING and SQUAD. Searching shows a blue strip beside the title. Bottom left on desktop over a dark corner shade (`Main.PlayShade`); bottom right on touch, lifted over the jump button. Grows with the screen (`CardScale` 1 at 720 px tall, up to 1.35; 0.7 on short screens). Layout: `Client.Core.Matchmaking.layoutBar` |
| Menus (Store, Inventory, Battle Pass) | Slate panel, big title top left, an X box top right, a row of tab words under the title with a hairline under the row (`Theme.Tab` lights one). The old left icon column is gone |
| Settings | Siege OPTIONS rows: name on the left, a black value box on the right half; toggles show ‹ ›, sliders are a thin white line with a small white knob and the value at the right |
| Phase banner (`Content.Effects.Parts.Banner`) | No box: ACTION PHASE in big capitals with a shadow, centered, and a gold "◇ LINE" under it |
| HUD | No panels behind health and ammo: white numbers with a soft shadow. The score bar keeps the team-colored score boxes around a dark timer box |
| Round result | A dark band fading out at both ends; ROUND WON / LOST carries the color |
| Store featured cards | Two to a row, so the row is always full |

Helpers: `Theme.Tab(button, on)` for nav tabs, `Theme.Crumb(parent, text, position)` for the notched chip.

## Theme and conventions (2026-11-17)

**Palette** (`Content.Theme`, the owner's three colors): Midnight Abyss `#171F44` for every surface (steps: Deep `#0C1026` dimmers, Surface `#171F44` panels, Raised `#212B5C` cards, Card `#2C3874` chips and inputs, Line `#3E4C94` outlines), Aqua Jade `#74FFED` for the accent (selected, values, progress, "you"), Baby Pink `#FE81D1` for the one main action on a screen (PLAY, START, BUY). Ink `#171F44` text on aqua and pink; Text `#F4F6FF` and Muted `#9AA3CD` elsewhere. Red `#FF5C7A` for danger and the enemy. Team, bomb and rarity colors keep their own meaning. New UI takes its colors from `Content.Theme`, never new hex values.

**Conventions** (from six UI laws, applied to every screen):

| Rule | What it means here |
| --- | --- |
| Dim the background (figure-ground) | Every popup sits on a backdrop at 70% (Theme.Deep, transparency 0.3); a tap on it closes the popup |
| Don't make important things look like ads (banner blindness) | Notices are cards: icon, title, one short line, one action. Color only as an icon or a bar, never a full-color banner |
| Connect the steps of a flow (connectedness) | Steps are circles joined by a line: the selection screen's LOCATION–CLASS–LOADOUT–READY, the training goal card |
| Half a card says swipe (closure) | A horizontal list shows part of its next card (`Client.Core.Peek.Cut`) |
| Few words | A title and one short line. Extras go in a small chip |
| One bright action | Only the main action is pink; secondary buttons are outlined (aqua outline on a dark aqua fill) |

The UI before the theme is in `ServerStorage.Archive.UIBeforeTheme_2026_11_17`. The values in "The look" below are from before it (they map to the steps above).

## The look

**Lighter since 2026-11-17 (slate blue, not black).** The old dark values below became slate: `#14171c` is now about `#374159`, `#20242c` about `#4a5677`, `#2b303a` about `#4e5a7e`. Use slate for new panels (`#2e3a56` base, `#3c4a6a` cards, `#54627f` off chips and tracks); keep near-black only for dimmers and NO SIGNAL screens. A UIGradient on a panel multiplies its color: give panels light gradients (white to light grey) or the panel turns black. The UI before the change is in `ServerStorage.Archive.UIBeforeLight_2026_11_17`.

| Thing | Value |
| --- | --- |
| Panel | `#14171c` (now slate, see above), 3% transparent, corners 14, a 1 px white outline at 80% transparency |
| Card / row | `#20242c` (now slate), corners 10 to 12 |
| Button | `#2b303a` (now slate), bold text, corners 10 |
| Primary | green `#3ecf5e` with a `#1f8f3b` edge |
| Danger | red `#e5484d`; quiet danger (Leave, Kick, Decline) `#5a2a2d` |
| Accent text | gold `#ffd678`; muted `#9aa3b2` |
| Font | **Fredoka One** (`rbxasset://fonts/families/FredokaOne.json`) on every piece of text in the game. It has one weight, so size and color carry the hierarchy. New UI must use it. Cmdr's admin console keeps its own fonts |
| Menus | Scale-sized with a maximum size; `Main` uses Global ZIndex (menus 11, things on a menu 12 and up). On a touch screen the move stick and jump button hide while a menu is open |
| Coin icon | Name a coin picture `CoinIcon`: `Client.Core.CoinIcon` gives it `Content.Store.Style.COIN_ICON` |

## The Game Modes panel

`StarterGui.Main.Modes` (`Menus` name `Modes`), client `Client.Core.ModeMenu`. A dimmed full screen in the style of a game-select screen: a big title, a row of tall cards, a description box under the row, and EXIT.

| Part | What it does |
| --- | --- |
| `Title` | SELECT A MODE, or the open category's name |
| `Cards` | A row of `Assets.UI.Templates.ModeCard`. First page: one card per category (`Content.Matchmaking.CATEGORIES`) with its tag ribbon, name and "N MODES". Pressing a category shows its modes as cards; a category with a single mode picks that mode at once |
| `Info` | The name and description of the card the mouse or gamepad points at; on touch, of the picked mode |
| `Back` | On a category's page: back to the categories |
| `Close` | EXIT |

### What a card shows

Categories and modes have the same card fields in `Content.Matchmaking`:

| Field | What it does |
| --- | --- |
| `Tag`, `TagColor` | The small ribbon in the corner and its color. `""` hides the ribbon |
| `Color` | The card's color (the whole card when there is no image) |
| `Image` | A picture that fills the card, cropped to fit, for example `"rbxassetid://123"`. `""` for none. A dark fade sits over its lower half so the name stays readable |
| `Icon` | The big faded text in the middle. `""` lets the panel choose: nothing over an image; otherwise a mode shows its team sizes ("1v1") and a category its first letter (or "1v1" when it holds one mode). Any other text is shown as written, over an image too. `" "` (a space) shows no text |
| `Description` | The text in the box under the row |

- The picked mode's card, and its category's, have a gold outline and say SELECTED. Hovering a card outlines it.
- Picking a mode closes the panel with the confirm sound; the MODE button on the lobby bar pulses and shows the new mode.
- Only the party's leader can open it, and not while searching. It closes when a match starts or the player stops being leader.
- Sizes: at 812 × 375 a card is 130 × 142 and EXIT is 200 × 44; at 1920 × 1080 a card is 240 × 410.
- No card has an image yet: set `Image` on a row to give it one.

## The lobby

`StarterGui.Main.Lobby`, shown whenever no match is running and no menu is open. Client: `Client.Core.Matchmaking`.

| Part | What it does |
| --- | --- |
| `Play` | **The big green button, bottom center.** Pressing it queues the party for the picked mode; its small line reads the mode (SIEGE · 1 V 1). While searching it is red and reads CANCEL. For a party member who is not the leader it is grey and refuses |
| `ModeButton` | Right of PLAY: shows the picked queue mode and opens the Game Modes panel. It refuses (buzz, and a line under the bar) for a party member who is not the leader, and while searching. No key |
| `Status` | Above PLAY while searching: the status, the mode and the queue timer. "MATCH FOUND" pops in |
| `PartyButton` | Opens the Party menu; shows the party's size |
| ~~`LoadoutButton`~~ | Removed on 2026-11-12 (archived as `ServerStorage.Archive.OldUI.LobbyLoadoutButton`): loadouts are not picked in the lobby |
| `PartyPlay` | **PLAY WITH PARTY**, above PLAY (in the status's place while not searching). Starts a private match of the picked mode (or the next one the party fits) with the party's own members ([MATCHMAKING.md](MATCHMAKING.md#play-with-party-2026-11-12)). Its line reads "PRIVATE 1 V 1 · 2 PLAYERS". Shown from 2 members (always in Studio); refuses for a member who is not the leader |
| `Message` | A line under the bar when the server refuses something |

`Main.Tooltip` (2026-11-15): the hover tooltip (`Client.Core.Tooltip`). Give any element a `Tooltip` string attribute (in Studio, or `Tooltip.Set(object, text)` in code) and resting the mouse on it for 0.35 s shows the text by the pointer. Mouse only.

`Main.Notice` (2026-11-15): a popup in the middle of the screen, above menus: `Title`, `Text`, `Ok`. Filled by `Client.Core.Notice.Show(title, text, sound?)`. Used for PARTY TOO BIG and PRIVATE ONLY.


The bar sits just above the health bar. On a touch screen while the fire button is showing it goes compact: PLAY is narrower and the two side buttons move above it, clear of the right thumb.

**Party is its own menu** (`Main.Party`, key L), no longer inside a Play menu: five member rows with avatars (LEAD and KICK for the leader), LEAVE PARTY, and the invite list with its two tabs. The invite popup is `Main.PartyInvite`.

Keys: **Play (K)** queues or cancels; **Party (L)** opens the Party menu.

## Siege UI pass (2026-11-17)

Inspired by what Rainbow Six Siege's screens do well (steps that say what's next, a real map to pick from, a class panel with stats, player cards, a top bar with every player, "3 VS 4", hit effects), drawn in our own look, not copied.

**Our look:** dark navy panels (`#0e121c`, raised `#1a202e`, `#262e40`), gold `#ffd678` for you, the current step and the main button, your team's color for your side (orange attackers, blue defenders), red `#ff6060` for the enemy, Fredoka One, rounded corners, and a small white "stud" on class emblems (the blocky touch). Siege is white and orange with a condensed font; keep ours different.

### Pre-match (`Client.Core.SiegeSelect` → `SiegeSelect`)

| Part | What it is |
| --- | --- |
| `Header.Steps` | LOCATION, CLASS, LOADOUT, READY: gold block = where you are, team-colored tick = done, grey = not yet. A step already reached can be clicked |
| `Header.Next` | One line: what to do next |
| `Header.Clock` | Team (in its color), "ROUND 1 OF 5", the clock (red in the last 5 seconds) |
| `Pages.Location` | `Left.Options` (template `SelOption`: radio, name, detail, vote badge), CONTINUE, and `MapPanel`: a ViewportFrame with the map, pins (`MapPin`: diamond, letter, label, ring), a caption and a legend |
| `Pages.Class` | `Left.Cards` (template `ClassTile`: emblem with letter and stud, name, a cover when taken or locked) and `Info` (emblem, name, role, `Stats` pips (`Pip`), ability, kit, status, SELECT CLASS, and the player's avatar on the team's color) |
| `Pages.Loadout` | CONFIRM LOADOUT, rows `Slot1`, `Slot2`, `Ability`, `Consumable` (arrows, "1 / 3"), and `Info` with `Bars` (damage, fire rate, magazine, mobility). The panel shows the focused gun's model turning, and since 2026-11-17 the gadget's model too (`ClassPanel.ConsumablePreview`, from `Assets.Models.Consumables`, still) |
| `Pages.Ready` / `Pages.Reveal` | A row of `PlayerCard`s (avatar, class badge and name, ready tick, player, spawn or vote) |
| `Footer` | `OwnReady` / `EnemyReady`: a dot per player (`ReadyDot`), "2/5 READY". Shown in Selection only |

**The map** is copied from `ReplicatedStorage.Maps.<snapshot Map>` into the viewport once (scripts, sounds, lights and effects left out), because the live map streams in. The top view frames the spawns and sites, straight down. The **cutaway** leans back 28 degrees over one site and hides: anything reaching more than 2.5 studs over the site's top, thin slabs at its top (its ceiling), and big pieces crossing its top over most of its floor (Mansion's ground and basement are unions). The bomb rooms are drawn as see-through red and blue boxes. Pins are placed by projecting their world point through the viewport's camera.

**Picking on the map (2026-11-17):** the map shows the site, spawn or map last tapped or clicked, in the list or on its pin (a pin's `Hit` button), and keeps showing it until another is picked; pointing with a mouse previews another while the pointer is on it. On a touch screen pointing does nothing (a tap fired the hover's enter and leave too, so the view jumped back to the vote). Clicking a site's or a free spawn's pin votes or takes it. Checked on PC: a spawn pin's click took the spawn; a site picked in the list stayed cut away with the mouse off it. Not tried on a phone.

**The viewport's Camera is made in code**: a Camera inside a ScreenGui is not copied into PlayerGui.

### In the round

| Part | What it is |
| --- | --- |
| `Main.SiegeHUD.TopBar` | `Own` / `Enemy` tiles (`TopBarSlot`: letter, stripe, `Dead` cover with an X, gold `Me` outline), `OwnScore`, `Center` (clock, round), `EnemyScore`. Copies in `DroneFeed.Feed.TopBar` and `CameraFeed.Feed.TopBar`. `Client.Hud.SiegeTopBar` fills all three. The old `SiegeHUD.Timer` is hidden but still updated: the feeds' NO SIGNAL timers copy it |
| `Main.SiegeHUD.Versus` | "3 VS 4" and a line under it, for 2.6 s when a player dies in Action |
| `Main.DamageFX` | `Edges` (four red gradient frames) and `Indicators.Arrow` (cloned per hit). `Client.Combat.DamageFeedback`. It sizes itself over Roblox's top bar too |
| `Main.Health` | Bottom-left panel: gold "+", "100/100", a thin bar (red at low health). On touch it goes bottom middle (`Client.Core.UI` TOUCH_LAYOUT) |
| `Main.Gun`, `Main.Weapons`, `Main.Consumable`, `Main.DroneSlot`, `SiegeHUD.Ability` | One stack in the bottom-right corner, each on a dark `Panel`; the held weapon slot shows its gold `Accent` and pops |
| `Templates.BombMarker` | `Diamond`, `Letter`, `Distance` ("21 m") |

### One class panel everywhere (2026-11-17)

`Client.Core.ClassPanel` fills two panels so a class or a gun reads the same wherever it shows:

| Panel | Where | Shows |
| --- | --- | --- |
| `ClassPanel` (template; originals in `SiegeSelect...Pages.Class.Info`) | Selection Class page, `Main.Inventory.ClassView.Panel`, `Main.Details.Left.ClassPanel` | Emblem, name, role and team, difficulty and speed pips, ability, weapons, gadgets, the avatar on the team's color |
| `GunPanel` (template; original `SiegeSelect...Pages.Loadout.Info`) | Selection Loadout page, `Main.Details.Left.GunPanel` | Kind, name, fire mode line, description, damage / fire rate / magazine / mobility bars against the best gun, and the gun's model (`Preview`) |

`Main` uses Global ZIndex: a panel copied into it needs its parts lifted above the menu (the Details and Inventory copies are at 22+ and 13+; `ClassPanel` gives its pips the pips row's ZIndex).

**Inventory CLASSES tab** (`Main.Inventory.ClassView`): `Cards` (ClassTile grid: owned first, locked covered with LOCKED and the coin price) and `Panel`. Pointing shows a class; clicking keeps it. The button is OWNED / FREE CLASS (green), or UNLOCK, which opens the class's detail page with its prices. The team chips and the search filter the tiles; the status line counts classes owned.

**Detail page** (`Client.Core.ItemDetails`): a View with `Class` shows the class panel on the left (the ABILITY section is left out: the panel has it); a View with `GunId` (skins) shows the gun panel; a Row with `GunId` (a class's starter guns) shows the gun panel when clicked, and again goes back.

### Weapon HUD (2026-11-17)

`Main.Weapons.SlotN`: key, `Preview` (the gun's model in the skin the player wears, rebuilt only when the gun or skin changes; camera field of view 21 so it fills the short row), name on the right. The held slot is light (`#ecf0f8`) with dark text and its gold accent. `Main.Gun`: `Preview` of the held gun on the left, ammo big on the right with the fire mode above and reserve beside it, the gun's name top left, the reload bar along the bottom. The grenade, drone and ability chips sit above the slots.

### Feeds

`Client.Gadgets.FeedInfo` fills `Intel` (OBJECTIVE, and where the feed is: a bomb room by name from the map's `Sites`, else INSIDE if something is overhead within 60 studs, else OUTSIDE), `Compass` (`Strip` of headings every 15 degrees, 3 px per degree, under a gold mark) and leaves `Scanlines` (static) alone. The feeds' own `Timer` labels are hidden: the top bar has the clock.

### Tested (2026-11-17, Studio, one player and bots)

| Check | Result |
| --- | --- |
| Location, attackers (Mansion) | Top view with five spawn pins; taking Pool Side turned its pin gold with "(YOU)" and the list row gold; bots' spawns grey with their names |
| Location, defenders | Bank and Mansion top views with site pins. Cutaways of Mansion's Basement and Upstairs Bedrooms show the rooms, stairs and walls with A red and B blue. (Bank's basement was checked before the union rule; not re-checked) |
| Class | Tiles taken by a bot show its name; locked ones say LOCKED; pointing previews; picking moved on to Loadout by itself |
| Loadout | Bars for the LMG and rifle; gadget arrows switch the gadget (saved data: switched back) |
| Reveal | Cards for the player and two bots, ticks, spawns |
| Top bar | Both teams' tiles, enemy "?", a killed enemy bot crossed out |
| 3 VS 1 | Shown when an enemy bot was killed, ENEMY ELIMINATED |
| Hit effects | Two hits from a dummy on the right: edges flashed, the arrow pointed right (89 degrees), and at 30 health the world went grey and the bar red |
| Camera feed | Top bar, objective DEFEND UPSTAIRS BEDROOMS, INSIDE, compass (feed shown by hand over the HUD) |
| Output | No errors from these modules |

**Not checked:** a phone or tablet (only the layout math: the selection screen fits by `FitScale` at DesignHeight 600), the real drone feed while driving (only the camera feed's frame by hand), the Ready page while a teammate is still picking (everyone was ready at once), Clear House's map vote preview, TEAMMATE DOWN, and a gamepad.

## Siege screens

- **Team cards** (`Assets.UI.Templates.PlayerCard` since 2026-11-17; `SiegeTeamCard` before): tall cards in a row with the player's avatar on the team's color, the class's badge and name, the player, and their vote or spawn.
- **Reveal:** "OBJECTIVE LOCATION" (defenders) or "INSERTION POINT" (attackers) with the place in large type, and the cards dealt in one after another.
- **HUD chips:** NO DEFUSER / DEFUSER PLANTED.
- **SCORE** on touch is a pill at the top of the Siege HUD, out of the combat buttons.

## Camera and drone feeds (2026-11-12)

The feed and alert ScreenGuis are built in `ReplicatedFirst.UILoader` and moved into `PlayerGui` by `UILoader`.

| UI | Behavior |
| --- | --- |
| `CameraFeed.Feed.Timer`, `CameraFeed.NoSignal.Timer` | Mirror `Main.SiegeHUD.Timer`, including its text color; the match timer remains visible over NO SIGNAL. Since 2026-11-17 `Feed.Timer` is hidden: `Feed.TopBar` shows the clock |
| `CameraFeed.Feed.Touch.Scan` | Touch scan button while viewing a live camera |
| `DroneFeed.Feed.Timer`, `DroneFeed.NoSignal.Timer` | Mirror the same match timer on live and NO SIGNAL feeds (`Feed.Timer` hidden since 2026-11-17, as above) |
| `Feed.TopBar`, `Feed.Intel`, `Feed.Compass`, `Feed.Scanlines` (both feeds) | 2026-11-17: the team bar, objective and location, compass, scanlines. See [Siege UI pass](#siege-ui-pass-2026-11-17) |
| `ScanAlert.Label` | Independent red `SCANNED` notice shown for `SCANNED_ALERT_TIME` after a camera or drone scan finds a player |

Camera scan controls are Interact on keyboard, DPad Up on gamepad, and `SCAN` on touch. See [SIEGE.md](SIEGE.md#defender-cameras) for server validation and class reveal behavior.

## Feel

`Client.Core.UIFeel` gives every `GuiButton` under PlayerGui the same behavior, including buttons other modules clone or build.

| Moment | What happens |
| --- | --- |
| Hover (mouse) | Grows to 104% in 0.08 s, a soft tick |
| Press | Squashes to 94% in 0.07 s **on the way down**, a click |
| Release | Springs back in 0.16 s |
| Refused (not `Active`, or the `Disabled` attribute) | A low buzz, no squash |
| A menu opens / closes | It pops in from 92%; its own sound each way |

Other moments, added by the modules that own them:

| Moment | Sound and effect |
| --- | --- |
| The search starts, a match is found, a pick is accepted, an ability works, the round ends | Confirm (two rising notes); the status, slot or panel pops or pulses |
| The server refuses a request, no charges left | Error; the message pops |
| A party invite, a new phase | Notify (two notes); the popup pops |
| The last 5 seconds of the selection | A tick each second; the timer pulses |
| The party grows or shrinks | Confirm or the close sound; the PARTY button pulses |
| The reveal | Each card pops in 0.07 s after the last, with a tick |

How it is wired:
- The scale effects drive a `UIScale` named **`Feel`** inside the button or frame. It is built in Studio on every button and template (59 added). A button without one still gets its sounds.
- Attributes: `FeelSilent = true` on a button or a frame around it means squash but no sound (the combat touch buttons, the weapon slots: a fire button must not click on every shot). `NoFeel = true` means nothing. `Menu = true` on a menu frame makes it pop when opened.
- `UIFeel.Play(kind)`, `UIFeel.Pop(object)`, `UIFeel.Pulse(object)`.
- The sounds are `UIOpen`, `UIClose`, `UIConfirm`, `UIError`, `UITick`, `UINotify` (and the older `ButtonHover`, `ButtonClick`) in `Content.Effects.Registry`, in the UI sound group. **They are placeholders**: the two UI sounds the game already had, at different pitches.

## Sizes on a phone and a desktop

Measured by laying the UI out in a frame of that size (no rendering needed).

| Element | 812 × 375 (phone) | 1920 × 1080 |
| --- | --- | --- |
| PLAY | 200 × 60, centered, bottom at y 327 | 334 × 92, bottom at y 941 |
| PARTY, LOADOUT | 114 × 46 each | 197 × 71 |
| Health bar | y 328, 10 px tall (was 7) | y 945, 30 px |
| Menu buttons | 120 × 44, wrapping onto rows (were 132 × 36 in one line) | the same |
| Party menu | 763 × 330, two columns of 359 | 780 × 430 |
| Invite popup buttons | 192 × 42 (were 30 tall) | the same |
| Weapon slots | 67 × 21 before the phone boost (1.6, now 1.15) (were 15 tall) | 190 × 60 |
| Buttons under 40 px | only the weapon slots | none |

## Where things are

| What | Where |
| --- | --- |
| Feel | `ReplicatedStorage.Modules.Client.Core.UIFeel` |
| Lobby bar, Party menu, invite popup | `Client.Core.Matchmaking` → `Main.Lobby`, `Main.Party`, `Main.PartyInvite`; templates `PartySlot`, `InviteRow` |
| Siege screens | `Client.Core.SiegeSelect` → `StarterGui.SiegeSelect`; `Client.Hud.SiegeHud` → `Main.SiegeHUD`; `Client.Hud.SiegeTopBar` → `SiegeHUD.TopBar`, `SiegeHUD.Versus` and the feeds' `TopBar` |
| Hit effects | `Client.Combat.DamageFeedback` → `Main.DamageFX` |
| Feed extras | `Client.Gadgets.FeedInfo` → `DroneFeed.Feed` / `CameraFeed.Feed` `Intel`, `Compass` |
| Scoreboard | `Client.Hud.Scoreboard` → `Main.SiegeScoreboard`, `Main.SiegeHUD.ScoreButton` |
| HUD layout for touch | `Client.Core.UI` (unchanged) |
| Replaced UI | `ServerStorage.Archive.OldUI`: the Play menu that held the queue and the party together, and its button |

## Tested (2026-11-12)

Studio, one player, one full match as a defender.

| Check | Result |
| --- | --- |
| Client and server output | No errors or warnings from this code |
| Lobby bar | Hidden during the match, back after it, PLAY green, party "1 / 5" (the loadout button it also checked is gone since) |
| Menu buttons | Hidden in Prep, back in the lobby |
| Reveal | "OBJECTIVE LOCATION", the site in capitals, a card 151 × 434 with the class, its letter, and the team's color |
| HUD | Objective line and "NO DEFUSER" chips shown in Prep |
| Feel scales | 117 of 129 buttons in PlayerGui have one (the other 12 are built in code by another module) |
| Sizes | The table above |

Two things found and fixed in that run: the bar still said MATCH FOUND after the match, and the old top-right Loadout button was shown again by another module.

**Not verified:**
- **How any of it looks.** No screenshot could be taken. Colors, spacing and text fit need a person's eye.
- **The motion.** Tweens did not advance in the test (a popped card stayed at 92%), which fits Studio not rendering; it is not confirmed in a normal window.
- **The sounds**, by ear.
- **Real presses**: the PLAY button, the Party menu, invites between two players, the queue timer counting, the red CANCEL state.
- A real phone, and a gamepad.

## Not redone yet

- **`Client.Core.LobbyHubUI`** (another developer's Career, Backpack and Map panels) builds its UI in code with its own colors. Its Career and Maps buttons are hidden since 2026-11-12 (the panels and their code remain); Backpack still shows in the lobby. Its buttons get the click and hover sounds, and its menu buttons inherit the new button style, but the panels are untouched.
- **The combat touch buttons** (`Main.Mobile`) keep their layout. Only the SCORE button moved out; ABILITY and CAMS were added on free cells.
- **The crosshair and hitmarker**, the kill feed and the death screen: fonts and corners only. (The ammo box, weapon slots, health and the feeds were redone on 2026-11-17.)
- **Icons.** There are none: classes show a letter (on an emblem since 2026-11-17), buttons are text. Class art would make the class grid and the player cards much better.
- Hover and press scaling nudges neighbors by a pixel or two inside list layouts.

## Card entrance (2026-11-20)

`Client.Core.CardIntro.Arm(container)` right before a menu draws its page: the cards added in the next 0.8 s come in staggered (pop from 72% with a slight tilt, Store and Inventory cards rise, one light sweep). Arm it only on opening a menu or changing its tab, never on a data redraw. Reduced Motion turns it off.
