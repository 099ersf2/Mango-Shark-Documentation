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

## The look

| Thing | Value |
| --- | --- |
| Panel | `#14171c`, 3% transparent, corners 14, a 1 px white outline at 80% transparency |
| Card / row | `#20242c`, corners 10 to 12 |
| Button | `#2b303a`, bold text, corners 10 |
| Primary | green `#3ecf5e` with a `#1f8f3b` edge |
| Danger | red `#e5484d`; quiet danger (Leave, Kick, Decline) `#5a2a2d` |
| Accent text | gold `#ffd678`; muted `#9aa3b2` |
| Font | Builder Sans: ExtraBold for titles and the big numbers, Bold for buttons and labels |
| Menus | Scale-sized with a maximum size; `Main` uses Global ZIndex (menus 11, things on a menu 12 and up) |

## The lobby

`StarterGui.Main.Lobby`, shown whenever no match is running and no menu is open. Client: `Client.Core.Matchmaking`.

| Part | What it does |
| --- | --- |
| `Play` | **The big green button, bottom center.** Pressing it queues the party at once (there is one mode). While searching it is red and reads CANCEL. For a party member who is not the leader it is grey and refuses |
| `Status` | Above PLAY while searching: the status and the queue timer. "MATCH FOUND" pops in |
| `PartyButton` | Opens the Party menu; shows the party's size |
| `LoadoutButton` | Opens the Loadout menu. It replaces the Loadout button that was among the top-right menu buttons |
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
| Lobby bar | Hidden during the match, back after it, PLAY green, party "1 / 5", loadout key "[B]" |
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

- **`Client.Core.LobbyHubUI`** (another developer's Career, Backpack and Map panels) builds its UI in code with its own colors. Its buttons get the click and hover sounds, and its menu buttons inherit the new button style, but the panels are untouched.
- **The combat touch buttons** (`Main.Mobile`) keep their layout. Only the SCORE button moved out; ABILITY and CAMS were added on free cells.
- **The gun HUD** (ammo, crosshair, hitmarker), the kill feed, the death screen, the drone and camera feeds: fonts and corners only.
- **Icons.** There are none: classes show a letter, buttons are text.
- Hover and press scaling nudges neighbors by a pixel or two inside list layouts.
