# Next steps

This list tracks verification not available in the solo Studio session.

## Queue modes, font, lobby clean-up (2026-11-12)

- [ ] Two real players queue 1 V 1 and get matched against each other; a party of two is refused for 1 V 1 with a clear message.
- [ ] Two players in different modes at once are never matched together (checked with made-up tickets only).
- [ ] **Look at the font.** Every label is now Fredoka One, which is wider than Builder Sans: check for clipped or shrunken text, mostly in the Settings rows, the scoreboard and the kill feed.
- [ ] **The Game Modes panel has not been run at all** (no playtest was asked for; it compiles and its parts exist). Open it from MODE, pick each category, check the outline, the description box and SELECTED, then EXIT. On a phone and with a gamepad too.
- [ ] A category with two or more modes (none exists yet): its second page and BACK have never been shown.
- [ ] Art for the mode cards (they are flat color with a faded "1v1").
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

