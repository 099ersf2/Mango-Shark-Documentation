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
