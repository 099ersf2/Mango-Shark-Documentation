[Documentation home](index.md) / Gun Game

# Recruit Training (the tutorial)

Added 2026-11-17. A two-round 1v1 against a very easy bot that teaches both sides of Siege: **round 1 the player attacks** (drone, breaking in, planting defusers), **round 2 they defend** (building boards, cameras, holding). Nothing is picked: the class, the site and the spawn are given. The first time a player finishes, they get the **Recruit Crate** (always Rare or better). A player can skip it on first join and start it any time later from the lobby's TRAINING button; the crate waits until they finish once.

## What we learned from other games first

| Game | What its tutorial does | What we took |
| --- | --- | --- |
| **Rainbow Six Siege**: Situations | Optional, short missions that switch roles: one as attacker, one as defender, explaining reinforcements and gadgets as you play | Two rounds, attack then defend, with boards as the defense lesson |
| **Valorant**: Basic Training | A separate track after the tutorial, with an attacker section (plant the Spike) and a defender section, and a reward per section (a free agent, a card, a title) | A real reward for finishing (the crate), and plant/defend as the core goals |
| **CS2**: Training Day | Movement, weapons, objectives and utility on a practice map; skippable | Skippable, with the core loop (find, breach, plant) taught by doing |
| **Roblox BedWars** | Barely any built-in teaching: new players learn from guides, and guides say they struggle | Don't drop new players into real matches unguided: invite them on first join |
| **Portal / Half-Life 2** (Valve) | Teaches through level design with almost no text; shows why something matters before teaching it; "if a player doesn't know what to do, it's our fault" | Each goal says *what* to do, not *how*. The how (keys) only appears as a hint after the player has been stuck for a while, so they discover things themselves |

## How it plays

1. **Lobby.** On first join (no Done, Rewarded or Skipped flag), a popup invites them after 4 s: WELCOME, RECRUIT, the free crate, START TRAINING or NOT NOW. NOT NOW saves `Skipped`; the TRAINING button (left of the lobby bar, above PARTY) stays and reads FREE CRATE with a red dot until the crate is earned, OPEN CRATE while it is unopened (opens the Inventory's crates), then PRACTICE.
2. **Start.** Alone only (no party members or bots). `Packets.Tutorial.Request("Start")` → `QueueService.JoinTutorial`: a private match of mode `Tutorial` on Mansion, the player attacking, the training bot (`BOT Rookie`) defending.
3. **Each round:** Selection is skipped (everyone is given their side's class, the attackers the spawn Back Porch, the defenders the site Main Floor, and marked ready). Reveal (8 s) shows the round's briefing: ROUND 1 · ATTACK / ROUND 2 · DEFEND, the story line and YOUR CLASS.
4. **Goals** (the card on the left, above the drone and camera feeds):

| Round | Phase | Goal | Reached when | Hint after |
| --- | --- | --- | --- | --- |
| 1 | Prep | FIND THE BOMBS | Their drone finds the site | 15 s |
| 1 | Prep | ★ MARK THE ENEMY (bonus) | Their drone scans the bot | 25 s |
| 1 | Action | BREAK IN | They break a board | 20 s |
| 1 | Action | PLANT A DEFUSER | The first defuser | 30 s |
| 1 | Action | FINISH THE JOB | The second defuser (round won) | 30 s |
| 1 | Action | ★ TAKE THEM DOWN (bonus) | They kill the bot | 40 s |
| 2 | Prep | FORTIFY (0/2) | Two doors or windows built whole | 12 s |
| 2 | Prep | ★ EYES EVERYWHERE (bonus) | They open a camera | 20 s |
| 2 | Action | HOLD THE LINE | The defenders win the round | 45 s |

   Each goal reached pops a SKILL LEARNED toast with a sound and the SKILLS n/9 counter goes up. A Prep goal not reached by Action is missed (it stops showing). If the drone didn't find the site, the site is shown at the start of Action anyway, so nobody is left wandering.
5. **End.** TRAINING COMPLETE, with the skills learned. The first finish saves `Done` and `Rewarded` and puts one Recruit Crate in the crate inventory, in one transaction; finishing again only says "Ready for a real match?". Winning or losing a round doesn't matter: finishing both rounds does.

**Easier on purpose:** the player has 300 health (`PLAYER_HEALTH`), prep is 45 s (drone) and 60 s (building), and the bot (`Content.NPC.Profiles.TutorialBot`) sees 90 studs with a 90° view, reacts in 1.4 s, misses a lot (aim error 26° settling to 14°, ×2.5), walks at 12, throws no grenades, never retreats, and walks up to boards to break them instead of shooting them from range.

## The screens (2026-11-17, second pass: fewer words)

- **Goal card:** the round's main goals as circles joined by a line (round 1: FIND, BREAK IN, PLANT, PLANT; round 2: FORTIFY, HOLD); reached ones fill aqua with a check, the current one is outlined aqua. Under it the goal's title and one short line (FORTIFY adds 0/2 and a bar). The bonus is a small pink chip (★ Scan the defender). The hint is one line of keys (WASD drive · Space hop), shown only after HintAfter seconds.
- **Toast:** a check and the goal's name (a pink star for a bonus).
- **Briefing (Reveal):** ROUND n OF 2, ATTACK (aqua) or DEFEND (pink), one line, the class chip. Low on the screen, under the spawn card.
- **Invite:** RECRUIT TRAINING, "Attack once. Defend once. About 5 minutes.", the FREE CRATE · RARE+ chip, START (pink) and Not now. 70% backdrop.
- **End:** TRAINING COMPLETE, the RECRUIT CRATE · RARE+ chip, one line, AWESOME!.

## Where things are

| What | Where |
| --- | --- |
| Numbers, texts, goals, saved flags | `ReplicatedStorage.Content.Games.Tutorial` (a ScribeFragment: `Tutorial = Scribe.Flags({ "Done", "Rewarded", "Skipped" })`) |
| The bot | `Content.NPC.Profiles.TutorialBot`; a bot entry's `Profile` (`SiegeBots.Spawn`) |
| The crate | `Content.Crates.Definitions.Recruit` (`Hidden = true`: not in the Store or the Inventory's skin groups; 19 Rare-or-better skins from Afterburn, Glacier and the Cosmetic charms, no Commons, so Common's chance falls to Rare) |
| The mode | `Content.Matchmaking` MODES `Tutorial` (`Kind = "Tutorial"`, Category `Training`, which no category row has, so the Game Modes panel doesn't list it); `Content.Games.Siege.ROUNDS.Tutorial = 2` |
| Starting it | `Systems.Matchmaking.QueueService.JoinTutorial` (also the `Queue.Request` action `"Tutorial"`) |
| The match | `Systems.Games.Siege.SiegeService` with its `tutorial` flag: `tutorialPicks`, training times, health, picks refused, `state.Tutorial`, site shown at Action; `SiegeService.IsTutorial()`, `SiegeService.Round()` |
| Goals and reward | `Systems.Games.Siege.TutorialService` |
| Client | `Client.Hud.Tutorial` (ClientOnly) |
| UI (built in Studio) | `ReplicatedFirst.UILoader.Training` (ScreenGui, DisplayOrder 6: `Goal`, `Learned`, `Briefing`, `Prompt`, `Reward`) and `Main.Lobby.Training` |
| Packets | `Packets.Tutorial`: `Request` (Start / Skip), `Progress`, `Learned`, `Finished` |

## Tested (2026-11-17, Studio playtest, saving off)

The test ran with the new `ScribeNoSave` workspace attribute (see below), so no real data was written.

- First join: the popup showed after the lobby loaded, and the lobby button read FREE CRATE.
- START TRAINING (a real click) started the match on Mansion: class Flash given, spawn Back Porch, site Main Floor, Selection skipped; the briefing read ROUND 1 · ATTACK; in Prep the goal card showed over the drone feed (FIND THE BOMBS, the bonus line, SKILLS 0/9).
- Round 1 (done from a test script as the player): the player had 300 health; breaking a board gave BreakIn, killing the bot Kill, standing in room A PlantA, room B PlantB, and the round ended.
- Round 2: the player was a defender; the FORTIFY card showed 0/2 with its hint after 12 s; two boards built gave Boards 1/2 then done, a camera view Cams, and killing the attacker ended the round as a defender win (Hold).
- End: TRAINING COMPLETE showed SKILLS LEARNED 7/9 (the drone goals were skipped in the test); the data had Done, Rewarded and one Recruit Crate; back in the lobby the crate opened (a Mythic Glacier LMG) and the button then read PRACTICE.
- 4,000 test rolls of the Recruit Crate: Rare 78%, Epic 15%, Legendary 5%, Mythic 1.5%, Secret 0.05%, Common 0.

**Not tested:** driving the drone into the site and scanning by hand; a real fight with the bot (how easy it feels); a live server (the teleport to a reserved server and back); phones.

## Studio: testing without saving

`Shared.Data` (2026-11-17): in Studio only, the workspace attribute `ScribeNoSave = true` (set in Edit before Play) loads profiles in Scribe's `NoSave` mode: real data is read, nothing is written. Live servers ignore it. Remove the attribute when done.

## The coach (2026-11-18)

The owner sent a video of a fighting game's tutorial: one short instruction at a time, the exact key under it, a counter, a praise word when it is done, then the next step. Recruit Training now coaches the same way (our own look):

- **`Client.Hud.TutorialCoach`** (UI `Training.Coach`, `Training.Skip`): one short line in the middle of the screen (above the bottom HUD on foot, near the top in a drone or camera feed), with the keys as key chips under it, using the player's own bindings (`Client.Settings.Keybinds`; a gold HOLD before keys that must be held, W A S D for driving). On a touch screen the real buttons glow instead: a pulsing mint ring and a bobbing arrow (under the target, pointing up, when it is near the top of the screen). HUD parts the step is about glow on every device (the bomb chips).
- **Beats** come from `Content.Games.Tutorial` STEPS[].Coach (Text, Keys, Move, Hold, Touch, TouchText, Highlight, Until). Main goals of the phase first, then bonus goals. A beat with `Until = "Feed"` (open your drone) moves on once a feed is open; the last beat lasts until the server reaches the step. A counted step shows `1/2`.
- **Praise:** reaching a step flashes NICE!, GOOD!, GREAT! or WELL DONE! for 1.4 s, then the next beat pops in (the side popup no longer shows). The old "stuck" hint no longer appears.
- **Size and place:** 1x on a 720 px tall screen, down to 0.65x on a phone, lower on a phone so it never reaches the crosshair; wider on a narrow screen, and it wraps to two lines. It steps aside while the HUD's toast or plant bar shows.
- **On a phone** the old goal card hides (the coach says the same); SKIP TRAINING takes the top-left corner (in a feed, under its header and site box).
- **SKIP TRAINING:** one tap arms it (TAP AGAIN TO LEAVE, 3 s), the second asks `Packets.Tutorial.Request "Leave"`: `TutorialService` sets Skipped (if not Done) and sends the recruit back to the lobby (`MatchHost.ReturnAll`); no crate, since only a finished run gives one. In Studio, where there is no lobby to go to, the match ends instead.
- The coach listens to `Packets.Siege.State` and `Packets.Tutorial.Progress` itself; the goal card's update is wrapped in a pcall that warns.

Checked in Studio playtests (desktop window): Prep shows "Drive into the house to find the bombs" with W A S D, a reached goal shows NICE! then "Tip: scan the defender" with HOLD X, Action shows "Shoot the boards on a door to break in" with LMB, then the bomb chips glow for "Follow a bomb marker and stand in its room"; SKIP arms then leaves. Not checked: the glowing touch buttons on a real phone, round 2 (boards, cameras, hold) by hand.

## Quicker, less told, arrows (2026-11-19)

The owner: the tutorial was confusing; shorter timers, don't give them all the info, lead them with arrows, 2-minute attack and defend, and tell defenders that killing the attacker wins faster.

- **Timers** (`Content.Games.Tutorial`): briefing 5 s (was 8), prep 30 s attack / 40 s defend (was 45 / 60), action 120 s (was 240), round result 5 s and match result 10 s (new `ROUND_END_TIME`, `END_TIME`, used by `SiegeService` in training; Siege's are 8 and 18).
- **Figure it out first:** each coach line now names only the goal ("Find the bombs", "Break in", "Defuse a bomb", "Board up the doorways"). Its keys and the glowing buttons appear only after the step's `HintAfter` seconds (6 to 15) if it isn't done by then, with a soft sound.
- **Guide arrows** (`Client.Hud.TutorialCoach`, beat field `Guide`): a mint arrow bobbing over the target with its distance (a BillboardGui `CoachGuide`, seen through walls) and, when the target is off screen or behind, an arrow at the screen's edge pointing the way (`Training.CoachEdge`). Targets: Site (the middle of the site's bombs), Bomb (the nearest bomb without a defuser), Boarded (the nearest doorway with boards), Open (the nearest unfinished doorway within 50 studs of the site), Bot (the bot in `workspace.Enemies`). The map is `workspace[TutorialContent.MAP]` (other maps can sit in workspace too). Doorways are found once per map (it is rebuilt every round).
- **Defend tip:** round 2 Action says "Guard the bombs. Take down the attacker to win the round faster".

Checked in a Studio training run: Prep shows "Find the bombs" with no keys and an edge arrow toward the site (68 m); Action shows "Break in", an arrow to the nearest boarded doorway (40 m), LMB after 8 s, and the 2:00 timer. Not checked: round 2 by hand, a real phone.

- 2026-11-19: the guide billboard keeps across respawns (ResetOnSpawn off) and only missing guide parts are remade; an arrow had stayed stuck on screen after a respawn.
- 2026-11-19 (later): guide arrows are 3D parts in the world (a marker over the target, a pointer above the crosshair when it is off screen); rings glow 5 s then fade.

### Tips and timed beats (2026-11-19)

Optional lines start with "Tip:" (they were "Bonus"). A beat can have `After` (seconds into the phase before it shows) and its own `HintAfter` (when the keys and glowing buttons come in). Defending, after 30 s of Action the coach suggests the cameras (key 5, the phone's camera button after 2 s) until the player opens them. On phones the coach is a left column under the top bar so it never covers the hotbar.
