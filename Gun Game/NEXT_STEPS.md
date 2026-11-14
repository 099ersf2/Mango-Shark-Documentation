# Next steps

## Mobile pass (2026-11-13, not seen on a phone)

- [ ] **Store and Inventory on a phone:** whole cards visible, readable text, X close button, ⚔ Classes icon, filter chips scroll sideways.
- [ ] **Match result on a phone:** fits the screen, MVP cards and both team columns visible.
- [ ] **Lobby on a phone:** the wallet sits top-left without covering PARTY, and there is no health bar.
- [ ] **Crate opening reel (`Main.Opening`):** not fitted yet; check it on a phone.

## Developer skin pack (2026-11-13, not run)

- [ ] `givedevskins me`, then the Inventory shows three black cards with the rainbow border under ALL, and under the RIFLE, PISTOL and SMG tabs.
- [ ] Equipped, each gun is black, and its rainbow lines flow along it in first person, in third person and in the preview.
- [ ] The side lines sit flush on the Rifle body, Pistol slide and SMG (their offsets were placed from the models' sizes, not seen). Adjust `Details` in `Content.Guns.Skins` if they float or sink.
- [ ] A player without the pack doesn't see the skins anywhere.
- [ ] `takedevskins me` removes and unequips them.

## Siege rounds and result screens (2026-11-13, not run)

- [ ] **A 1v1 match:** three rounds at most, sides swap, the banner shows between rounds, and the match stops at 2 wins.
- [ ] **A 5v5:** five rounds at most, stopping at 3.
- [ ] **Between rounds:** the map is whole again (broken boards and walls back) and the bombs are gone. Everyone picks a class, spawn or vote and loadout again.
- [ ] **The match result screen:**
  - the reveal plays in order;
  - the MVP avatars load;
  - the totals add up;
  - WINNER is on the right column.
- [ ] **Phone size:** the MatchResult columns and MVP cards fit at 844×390.
- [ ] **Rewards:** paid once per match, to the side with more rounds.
- [ ] **Prep drone:** the view stays when the lobby body spawns, and driving and scanning work.
- [ ] **Locked classes** grey out and sort last in Selection, and unlock after buying.
- [ ] **Lobby Tab** ranks players by wins.
- [ ] **A map music folder** plays during that map's match.

## Store and Inventory redesign (2026-11-13, not run)

- [ ] **Open the Store and the Inventory in a client that renders:**
  - cards, ribbons, the glow sheen, the daily deal countdown;
  - the detail page for a class, a crate and a skin;
  - buy a crate with coins, see it in Inventory > Crates, OPEN, and watch the reel.
- [ ] **Decide which classes to sell** (`Content.Store.CLASS_PRICES`; none locked now).
- [ ] **Phone:** the Store cards are 4 per row; they may need 2 on a phone.

## Store and stats (2026-11-13)

- [ ] **Replace the placeholder icons** of the 8 new products and the VIP pass on the Creator Dashboard (created 2026-11-13; ids in `Shared.ProductIds` and [STORE.md](STORE.md#limits)).
- [ ] **Buy one Robux item in a live server** to see the receipt give it.
- [ ] **See the Store, the wallet bar, the reward toast and a coin-bought crate's reel** on screen.
- [ ] **A real match:** the winners and losers get coins, a win or a loss, and the streak tag; back in the lobby, PLAY shows the last mode.
- [ ] **Decide** whether any class should be locked and sold.

## Armory and skins (2026-11-13)

- [ ] **See the 3D previews and the reel spin** in a client that is rendering (Studio wasn't).
- [ ] **Buy a real crate:** the reel lands on the skin the server gave, and EQUIP / DONE work.
- [ ] **In a Siege match,** an equipped rifle or pistol skin shows on the class guns.
- [ ] **The shop on a phone** (the grid is 3 columns; it may want 2).

## Siege drones (2026-11-13)

- [ ] **Prep, in a real match:**
  - Each attacker sees their drone's view at once, with the map around it loaded.
  - With the drone destroyed, NO SIGNAL stays until Action, then the body spawns.

- [ ] **A real match, as an attacker:**
  - In prep, held in the drone; if it is destroyed, NO SIGNAL stays until Action.
  - At Action, the body spawns, the Drone key throws the second drone, and switching between the two works.
  - Scans from either drone mark defenders and cameras.
- [ ] **Gamepad LB / RB and touch NEXT** switching.

## Prompts and reinforce (2026-11-13)

- [ ] **See the prompt cards in a match:** a defender at an empty frame sees two cards (build boards E, Reinforce T) side by side; holding either fills its bar and builds it.
- [ ] **Touch:** holding a card builds or reinforces; **gamepad:** the two cards show different buttons.
- [ ] **Attackers** see no build card at a frame.
- [ ] **Three or more prompts** on one object wrap onto a second row.

## Mobile UI pass (2026-11-13)

Laid out at 844 × 390 in Studio, not run on a device.

- [ ] **A real phone:** the icon buttons are easy to hit, nothing overlaps, the selection screen's text is readable at scale 0.645.
- [ ] **A tablet** (about 1180 × 820): the larger 120 px buttons and the selection screen at scale 1.
- [ ] **A real Siege match on a phone:** the timer pill and SCORE, the slim announcement banner, the death card above the spectate bar, and the round-end panel hiding them.
- [ ] **The drone button's labels** (`OUT`, `LOST`, `x1`, `12s`) and the ability's (`x1`, `12s`) fit under the icon.
- [ ] **Smoke picked:** the grenade button shows the smoke icon.

## Fixes and features of 2026-11-12 (none of it has been run)

No playtest was asked for. Everything below compiles and its UI parts exist; nothing has been seen working.

- [ ] **Scan popup:** every attacker sees ENEMY SCANNED with the name and class, also when the defender is only nearby and not in the crosshair.
- [ ] **Drone scan** on a defender standing in the site: the mark appears where they stood, and their class shows on the attackers' scoreboard.
- [ ] **Drone on a phone:** the DRIVE stick drives, another finger looks, HOP / SPOT / BOOST still work.
- [ ] **Drone against a wall:** the camera stays on the drone's side.
- [ ] **Destroyed drone and camera:** NO SIGNAL shows nothing of the world, shows how to leave, and 5 / X / B / EXIT leave it. A destroyed camera still lets you go to the next one.
- [ ] **Names and health:** teammates show both, enemies neither. Check a player who changes team mid-game.
- [ ] **The ready list with two teams:** the enemy section is clearly the enemy (red heading and names), and its READY changes live.
- [ ] **Reinforce on an empty door frame** (most of the map's doors): a whole reinforced door appears in the frame you are looking at, not a neighbouring one.
- [ ] **Reinforce** on a board and on a door board: the reinforced model stands exactly in the old one's place and size, breaks piece by piece, and the original is back after the match.
- [ ] **Selection:** the team list on the right, READY turning green for teammates, the clock skipping when everyone is ready, the consumable row. On a phone the loadout panel is short: check the consumable row can be reached.
- [ ] **Play with party** with 2, 3, 4 and 5 members: even teams, nobody else in the match, the party intact afterwards. Live servers only.
- [ ] **Party after a match** (live servers): play a match as a party of two or more, come back, and check the party shows on every member's screen within a few seconds, without opening the Party menu.
- [ ] **Leave a queued party:** the party leaves the queue and the member who left sees no search. With the member on another lobby server too.
- [ ] **Sliding:** crouch while sprinting right after firing, right after a slide, and in the air before landing. Tune `Config.SlideBuffer` (0.3 s) if it feels late or too eager.
- [ ] **Touch layout** on a real phone and a tablet: reach, and whether FIRE and AIM sit right for the thumb. Positions are one table, `TOUCH_BUTTONS` in `Client.Core.UI`.
- [ ] Fix `Definitions.ReinforcedDoor`'s model name (`ReinforcedDoor`, the asset is `ReinforcedDoorBoard`) if maps will tag parts with it.

## Music (2026-11-12)

- [ ] **Listen to a whole match.** None of it has run: the start song on the selection screen, the 4 s crossfade into a panic song at 0:30, the end song, and the background songs coming back after.
- [ ] End a round early and check the end song comes in without the panic song.
- [ ] Check the levels against gunfire; a song's loudness is the `Volume` on its Sound.
- [ ] `Assets.Music.Panic` holds "Global Strike 30 sec edit" twice, so it plays twice as often as "Urgent Action". Remove one if that is not meant.
- [ ] Decide what the unused `Alpha` and `Folder` folders in `Assets.Music` are for.

This list tracks verification not available in the solo Studio session.

## Queue modes, font, lobby clean-up (2026-11-12)

- [ ] Two real players queue 1 V 1 and get matched against each other; a party of two is refused for 1 V 1 with a clear message.
- [ ] Two players in different modes at once are never matched together (checked with made-up tickets only).
- [ ] **Look at the font.** Every label is now Fredoka One, which is wider than Builder Sans: check for clipped or shrunken text, mostly in the Settings rows, the scoreboard and the kill feed.
- [ ] **The Game Modes panel has not been run at all** (no playtest was asked for; it compiles and its parts exist). Open it from MODE, pick each category, check the outline, the description box and SELECTED, then EXIT. On a phone and with a gamepad too.
- [ ] A category with two or more modes (none exists yet): its second page and BACK have never been shown.
- [ ] Upload pictures for the cards and set `Image` on the rows in `Content.Matchmaking`. A card with an image has never been shown: check the crop, the dark fade, and that the name is readable.
- [ ] Decide what happens to the Loadout menu and the grenade / smoke picker inside it: nothing opens them now.
- [ ] Decide whether two friends in one party should be able to 1 V 1 each other (today a party is never split, so they queue separately).
- [ ] Decide the default mode once the game has players (`DEFAULT_MODE` is `1v1`).

## UI revamp (2026-11-12)

- [ ] **Look at it.** Nothing was seen rendered. Check colors, spacing and text fit in the lobby, the Party menu, the selection and reveal screens, and the restyled Loadout and Settings menus, on a desktop and at phone size.
- [ ] Press things: PLAY (green, then red CANCEL with the timer counting), the Party menu, an invite between two players, the selection pages.
- [ ] Watch and listen: buttons squash on press and grow on hover, menus pop in, and each sound is distinct and not too loud.
- [ ] A real phone: the compact lobby bar while the fire button shows, the SCORE pill, 44 px rows.
- [ ] Replace the six placeholder UI sounds, and add class icons.
- [ ] Decide whether `LobbyHubUI`'s Career, Backpack and Map panels get rebuilt in Studio in the new look (they are another developer's, built in code).
- [ ] Decide whether the combat touch buttons get a new layout.

## Siege, matchmaking, classes (2026-11-12)

**Before Siege can be played at all**
- [ ] Fix the map (`Workspace.CurrentMap`) so it passes the check in [SIEGE.md](SIEGE.md#the-map): add `AttackerSpawnLocations` (5 parts), add `Cameras`, rename the second `Bombs.MainFloor`, name each site's volumes `BombA` / `BombB`, give every site a folder in `Sites` and a spawn in `DefenseSpawnLocations` named after it. The four spawns in `DefenseSpawnLocations` today (BackPorch, PoolSide, RoofSide, Street) look like attacker spawns.
- [ ] Decide the lobby: it is off (its portals are gone), so on a lobby server players spawn on the map with guns while they queue. `LobbyService` has a marked line to require only `Lobby` and `LobbySpawnPoint` once that is wanted.

**Live servers (nothing here has run)**
- [ ] Publish to a test place and queue from two lobby servers: one matchmaker at a time; shut that server down and check another takes the lease within about 15 s.
- [ ] A full reserved-server match: teleport in, teams from the match record, the round, the teleport back with parties intact.
- [ ] A party with members on two lobby servers: invite, accept, kick, promote (ownership moves), leader leaves.
- [ ] Force a teleport failure and check the requeue.
- [ ] Watch MemoryStore and MessagingService usage with many lobby servers.

**Two or more players**
- [ ] Two attackers pick the same spawn, and two teammates the same class, at the same moment: one gets it, the other sees it greyed out at once.
- [ ] A tied site vote: only tied sites are ever chosen.
- [ ] A second client is never sent the other team's picks, or a defender's class before a scan (read the packets on an attacker client).
- [ ] Drone scan: the mark stays where the defender stood, the next scan replaces it, the first scan shows the class on the attackers' scoreboard.
- [ ] Site located once; red A and blue B marks for attackers.
- [ ] Spectate teammates, then enemies when none is left; a dead attacker can't get into their drone.
- [ ] Mid-match leaves: the last defender leaving gives the attackers the round; the last attacker leaving gives it to the defenders.
- [ ] Every class ability in play ([CLASSES.md](CLASSES.md)).

**With Studio's window visible (render steps did not run in the tests)**
- [ ] The drone, security-camera and spectate views; the mouse free on the selection screens.
- [ ] Real clicks through the Play menu and the selection pages.
- [ ] Gamepad and touch for every new control.

**Assets**
- [ ] Class icons (`Content.Classes`, `Icon` is empty) and real sounds for `GadgetPlace`, `GadgetDestroyed`, `Flashbang`, `AbilityPulse`.

- [ ] Run a two-player test and verify balanced team assignment and team spawn sides.
- [ ] Credit an enemy-player kill and verify the player's kill count, team total, and winner.
- [ ] Verify a victim spectates the credited killer until respawn, including when that killer leaves or respawns first.
- [ ] Verify no-killer deaths show the death screen and do not award a kill.
- [ ] Verify teammate damage is blocked and enemy damage still works during an active round.
- [ ] Check the match HUD, avatar thumbnails, and death screen on a phone-sized viewport.

## Scout drones (2026-11-11)
- [ ] Drive a drone with real keys: does it feel fast and smooth? Tune `SPEED`, `ACCELERATION`, `BRAKING`, `HOP_SPEED` in `Content.Drones`.
- [ ] Spot a real enemy and check your teammate sees the mark; check teammates can't shoot your drone.
- [ ] Try gamepad (DPad Left / Down, sticks) and touch (DRONE, CAMS and the in-drone buttons) on a phone.
- [ ] Replace the placeholder motor sound (`Assets.Models.Gadgets.Drone.HumanoidRootPart.Motor`).
- [ ] Watch NPCs react to a drone driving past (hearing) and shoot it.


## Pistol shoot animation (2026-11-11)
- [ ] Publish `RBX_ANIMSAVES.Rig2."Pistol Shoot"` from the Animation Editor to get an animation ID, then hook it to the NPC or gun that should use it.


## Third-person gun animation (2026-11-11)
- [ ] Watch another player in a two-player test: aim pitch, aiming, sprinting, shooting and reloading in third person.
- [ ] Look at each gun from the side and front; tune `POSES` in `Client.Guns.ThirdPersonGuns` if a hold looks off.


## NPC guard mode (2026-11-11)
- [ ] Put an `NPCRoom` part over a room, make an NPC a guard (`Mode = "Guard"` on its `NPCSpawn`, or `NPCService.SetMode`), break one of the room's boards out of the guard's view, and check it rebuilds it.
- [ ] Shoot the guard while it repairs: it should fight from inside the room, then finish the repair.
- [ ] Note: the NPC cap (`MAX_NPCS`) was 0 and the lobby was off in the last playtest (not from this change).

