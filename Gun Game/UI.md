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

The ScreenGuis (`Main`, `SiegeSelect`, `DroneFeed`, `CameraFeed`) are no longer in `StarterGui`. Another developer moved them under the LocalScript `ReplicatedFirst.UILoader`, which parents them into `PlayerGui` when the client starts. **Edit the UI there.** Where this doc says `StarterGui.Main…`, read `ReplicatedFirst.UILoader.Main…`. Templates are still in `Assets.UI.Templates`.

## Touch buttons (2026-11-12, not run)

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

## The look

| Thing | Value |
| --- | --- |
| Panel | `#14171c`, 3% transparent, corners 14, a 1 px white outline at 80% transparency |
| Card / row | `#20242c`, corners 10 to 12 |
| Button | `#2b303a`, bold text, corners 10 |
| Primary | green `#3ecf5e` with a `#1f8f3b` edge |
| Danger | red `#e5484d`; quiet danger (Leave, Kick, Decline) `#5a2a2d` |
| Accent text | gold `#ffd678`; muted `#9aa3b2` |
| Font | **Fredoka One** (`rbxasset://fonts/families/FredokaOne.json`) on every piece of text in the game. It has one weight, so size and color carry the hierarchy. New UI must use it. Cmdr's admin console keeps its own fonts |
| Menus | Scale-sized with a maximum size; `Main` uses Global ZIndex (menus 11, things on a menu 12 and up) |

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
| `PartyPlay` | **PLAY WITH PARTY**, above PLAY (in the status's place while not searching). Starts a match of the party's own members, dealt into two even teams ([MATCHMAKING.md](MATCHMAKING.md#play-with-party-2026-11-12)). Shown from 2 members (always in Studio); refuses for a member who is not the leader |
| `Message` | A line under the bar when the server refuses something |

The bar sits just above the health bar. On a touch screen while the fire button is showing it goes compact: PLAY is narrower and the two side buttons move above it, clear of the right thumb.

**Party is its own menu** (`Main.Party`, key L), no longer inside a Play menu: five member rows with avatars (LEAD and KICK for the leader), LEAVE PARTY, and the invite list with its two tabs. The invite popup is `Main.PartyInvite`.

Keys: **Play (K)** queues or cancels; **Party (L)** opens the Party menu.

## Siege screens

- **Team cards** (`Assets.UI.Templates.SiegeTeamCard`): tall cards in a row, like the operator line-up in Rainbow Six Siege. The class's picture (its first letter until icons exist) on the team's color, then the class, the player, and their vote or spawn.
- **Reveal:** "OBJECTIVE LOCATION" (defenders) or "INSERTION POINT" (attackers) with the place in large type, and the cards dealt in one after another.
- **HUD chips:** NO DEFUSER / DEFUSER PLANTED.
- **SCORE** on touch is a pill at the top of the Siege HUD, out of the combat buttons.

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
| Weapon slots | 67 × 21 before the phone boost of 1.6 (were 15 tall) | 190 × 60 |
| Buttons under 40 px | only the weapon slots | none |

## Where things are

| What | Where |
| --- | --- |
| Feel | `ReplicatedStorage.Modules.Client.Core.UIFeel` |
| Lobby bar, Party menu, invite popup | `Client.Core.Matchmaking` → `Main.Lobby`, `Main.Party`, `Main.PartyInvite`; templates `PartySlot`, `InviteRow` |
| Siege screens | `Client.Core.SiegeSelect` → `StarterGui.SiegeSelect`; `Client.Hud.SiegeHud` → `Main.SiegeHUD` |
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
- **The gun HUD** (ammo, crosshair, hitmarker), the kill feed, the death screen, the drone and camera feeds: fonts and corners only.
- **Icons.** There are none: classes show a letter, buttons are text.
- Hover and press scaling nudges neighbors by a pixel or two inside list layouts.
