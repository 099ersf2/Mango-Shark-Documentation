[Documentation home](../README.md) / Gun Game

# Siege bots

Added 2026-11-16. Bots play Siege beside and against players: they pick classes their teammates aren't using, pick spawns or vote a site, defend the two bombs, and break in to plant defusers. For now only **admins** (`Modules.Classes.Admins`) can add them.

## How to play with bots

1. Open **PARTY** (L). An admin sees a third tab, **BOTS**, beside THIS SERVER and FRIENDS.
2. Press **ADD** next to a bot (Nova, Echo, Rook...). It joins the party at once and its slot says **BOT**.
3. Play as usual:
   - **PLAY WITH PARTY** deals the party into two teams. A party of 1 player and 3 bots plays 2 v 2.
   - **PLAY** queues the party with its bots for a public match. Bots count toward team sizes like players.
4. **KICK** removes a bot. A bot can't be made leader. When the last player leaves, the party ends.

After a match the party comes back with its bots.

## Where things are

| What | Where |
| --- | --- |
| Numbers and names (names list, timings, id range) | `ReplicatedStorage.Content.Games.SiegeBots` |
| How a bot fights (health, speed, sight, aim) | `Content.NPC.Profiles.SiegeBot` |
| What a bot decides (picks, body, the plan) | `ServerScriptService.Modules.Systems.Games.Siege.SiegeBots` |
| The match with bots in it | `Systems.Games.Siege.SiegeService` (roster entries with `Bot = true`) |
| Bots in the party | `Systems.Matchmaking.PartyService` (the `AddBot` request) |
| Bots in tickets and match records | `Systems.Matchmaking.QueueService` |
| The BOTS tab | `Client.Core.Matchmaking`, `Main.Party.Invite.Tabs.BotsTab` (built in Studio) |
| Bot radio (bots talking to each other) | `radio` in `SiegeBots`, numbers in `Content.Games.SiegeBots` (2026-11-17) |
| Outfits | `Content.Games.SiegeBots.LOOKS` (2026-11-17) |

## How a bot is carried

| Stage | How |
| --- | --- |
| Party | A member with a **negative UserId**, `-ID_MIN` to `-ID_MAX`, so it never matches a real player or another party's bot. Its name is `PREFIX` + a name from `NAMES` ("BOT Nova"). It lives on the leader's server. The client view marks it `Bot = true` |
| Ticket | In `M` like any member, and in `B` (`{ U, N }`) with its name |
| Match record | In `Teams`. Listed in `Bots` (`{ U, N }`). **Never in `Expected`**: nobody waits for it or teleports it |
| Match server | `SiegeService.onMatchReady` puts each record bot in the roster: no `Player`, `Bot = true` |
| Back in the lobby | The parked party keeps its bots (`B`). The first player to claim the party gets them back |

## What a bot does

### Selection

- **When:** `PICK_DELAY` (2 to 6 s) into Selection, so players choose first. Then it is ready. If everyone is ready before that, it picks when Selection ends.
- **Class:** a random class of its team that **no teammate has**, players or bots. Locked classes are allowed: bots own every class.
- **Attacker spawn:** a free spawn, the one nearest its teammates' spawns, so the attack goes in together.
- **Defender site vote:** the site its **player teammates** voted for. Else the site another bot voted for. Else any site.
- **A player always wins a clash:** a player who picks a bot's class or spawn takes it, and the bot picks again.

### Body

- **Defenders** get a body in Prep, at the defense spawn. **Attackers** get one in Action, at their spawn.
- The body is an NPC on the bot's side (`NPCService.Spawn` with `Team`, `Name`, `Gun`, `AlwaysAwake`).
- **Gun:** its class's first loadout gun that exists. The Shield class's primary is "None", so that bot carries the pistol.
- **One life**, like players.
- **No friendly fire:** a bot and its teammates can't hurt each other (`Combat.PreventFriendlyFire` in SiegeBots).
- **Never sleeps:** NPCs normally sleep more than 350 studs from every player, but bots fight each other far from players.
- **Drones, no other gadgets:** attacker bots drive a scout drone in Prep (see Drones below). Bots don't use class gadgets or cameras.

### The plan (every `THINK` = 0.5 s in Prep and Action)

Fighting always comes first: the NPC tree only follows the plan when there is nothing to shoot or hunt.

**Defenders**
- They guard a bomb room in NPC Guard mode: stay inside, patrol, rebuild its doors and windows, fight first.
- Each has a **home bomb** (2026-11-17): the team split evenly between the bombs still without a defuser. A bomb whose guards died takes one from a bomb with two or more.
- A threat (an attacker planting, or an enemy seen or heard in a bomb room) pulls in the defenders of other bombs, **but never a bomb's last guard**, not even for a plant on the other bomb. When it is over each goes home. Until 2026-11-17 every defender went to the threatened room and stayed there, leaving the other bomb open.
- Once a bomb has its defuser, they all hold the other one.
- A defender outside its room (it spawned elsewhere, or fell through a floor) walks back first, then guards it.

**Attackers**
- **Finding the site:** their drones (below), a player's drone, or a bot walking into the real site finds it for every bot. Failing that, they learn it after `SITE_INTEL_TIME` (45 s) of Action. Until then they check the sites nearest them that no teammate has checked.
- **Choosing a bomb (squad, 2026-11-17):** once the site is known the attackers share one target bomb: the room a teammate is already in, else the bomb with the fewest defender sightings in the last `THREAT_WINDOW` (20 s), plus a random 0 to 0.4 and a 0.5 penalty for last round's bomb. A new plan is made when that bomb gets its defuser or the map changes. Until 2026-11-17 each bot took its own bomb, so they arrived one at a time.
- **Rally and push:** the squad picks a random entrance of the target room (a door or window board within `RALLY_REACH`, 32 studs, not the one used last round) and a rally point `RALLY_BACK` (9 studs) outside it on the floor. Each bot walks there and waits facing the room. A bot within `RALLY_ARRIVED` (9 studs) has arrived; one already closer to the room than to the rally point counts as arrived and goes in. The push starts when all have arrived, `GATHER_WAIT` (6 s) after the first arrival, or `GATHER_MAX` (20 s) after the plan; then each goes in `PUSH_STAGGER` (0.7 s) after the one before. Debug: `workspace.BotSquad` (attribute) names the target, entrance and state.
- **Scouts spread out:** before the site is known, each checks a different site from the others.
- **Planting:** inside the bomb room (`ROOM_HOLD` studs in from its edges) the bot switches to Guard mode on that room. It stays in and keeps fighting while the defuser plants (8 s); leaving would reset it.
- **Hatches:** for a room on a floor below with no way down (the Mansion basement), the bot walks onto the hatch over that room, shoots it open (`HATCH_SHOOT`, 5 studs) and drops through. Only hatches on the floor right above count (`HATCH_ABOVE`), and since 2026-11-17 only one that really drops into the room: a raycast from 1 stud under the hatch must hit the room's space (`dropsInto`, cached). Bank's upstairs hatch is over basement A but opens into the vault, which kept bots circling the vault.
- **Shut out:** with no path to its room (or the hatch) for `DOOR_AFTER` (6 s), the bot picks the boarded door or window on its floor that best leads toward the room, stands in front of it and shoots the boards off. Doors come first: a window counts `WINDOW_COST` studs farther because it has to be climbed. A door or window it has tried is not picked again.
- **Unstick:** a bot that hasn't moved for `STUCK_TIME` (5 s) on its way somewhere walks 14 to 24 studs off for 4 s, then tries again. The spot is on its own floor (within 3 studs), never in water or a pit. Pathfinding sometimes "finds" a way straight up to the floor above.
- **Paths through doors** (2026-11-16): an attacker's paths may go through intact boards (`BreakThrough`), so it heads for a boarded door like an open one and breaks it when it gets there. Defenders' paths don't, so they never break their own boards.
- **Climbing and water:** bots climb trusses (the Mansion pool has an invisible one on its ladder) and walk round water.
- **Unreachable rooms:** a room with no path for `NO_WAY_TIME` (20 s), and no breach under way, is skipped for 40 s. The bot takes the other bomb, or hunts defenders if neither is reachable.
- **Focus:** a bot heading somewhere ignores gunshots and hunt spots on another floor, so it doesn't stand under an enemy it heard instead of going on.

### Drones (2026-11-16)

Every attacker bot gets a scout drone at its spawn in Prep (`Systems.Games.Siege.BotDrones`; the server drives it).

- **Scouting:** it drives to the nearest site no teammate has checked (bomb room A of that site). Inside a site (a stud inside its box, height too) the site is checked; inside the real one, the site is found. A site it can't get into is left for the next one.
- **Spotting:** every 0.5 s it looks for enemies within `DRONE_SPOT_RANGE` (45 studs) in clear view. Each goes into the team's memory and is marked on its player teammates' screens for `DRONE_SPOT_TIME` (15 s, `DroneService.Mark`). A defender standing in the real site gives the site away.
- **Found:** "Site located" for the players too (`SiegeService.checkDiscovery` reads `SiegeBots.SiteFound`). The drone then drives into its bot's bomb room and parks there, still spotting, until the round ends.
- **Like a player's drone:** `DRONE_SPEED` 14 studs/s (players' do 20), one hit kills it, defenders hear its motor (`Drone.Noise`) and see and shoot it (`DroneService.AddExternal`), teammates can't hurt it.
- **Under door boards:** it slips under a boarded door like a Siege drone through a barricade gap (a path through a `Breakable` label, cost 5). A boarded window needs a climb, which it can't do.
- **Through wall vents:** every model named `Vent` gets a `PathfindingLink` through its hole when the drones deploy (`BotDrones.Prepare`), and drones drive through. People's paths never take them. Mansion's vent behind the upstairs bunk bed isn't used (a drone can't get down from the bed).

### Memory (2026-11-16)

- **Sightings:** what each bot sees (and in Action hears; in Prep the only noises are drones) and what drones spot is kept for its team for `MEMORY_TIME` (30 s).
- **Sharing:** a bot with nothing to fight or hunt goes after a teammate's sighting from the last `SHARE_TIME` (6 s) within `SHARE_RANGE` (50 studs) on its floor.
- **Threat:** an enemy seen in a bomb room (or heard there in Action) in the last `THREAT_TIME` (10 s) counts like a planting attacker: the defenders that can leave their own bomb go to that room (see above).
- **Breaking their own boards:** only then may a defender outside the room break its own team's boards to get in (`Brain.SetBreakThrough`, `Tactics.Breach`). Otherwise defender bots never break boards (`agent.NoBreach`), and each keeps the room it holds when a teammate dies.
- **Checked sites** are shared by the team.
- **Entrances, for the whole match:** the boards attackers broke through on each map (`Breakable.Broken`). A defender guarding a room watches the one used most 60% of the time (`agent.WatchHint`). `SiegeBots.NewMatch` forgets them.

### Breaking boards from range (2026-11-16)

With the profile's `BreachRange` (30 studs), a bot shoots a board open from where it stands when it has a clear shot at an intact piece: a board on its path within range (`Brain.BoardOnPath`, the path's `Breakable` waypoints), or the entrance it chose. It never bashes (a door is 10 bullets, about a second). Without a clear shot it walks up as before.

### Radio: bots talk to each other (2026-11-17)

A team's bots tell each other what they know (`radio` in `SiegeBots`); players don't see it. Each message goes into the team's log (`radioLog`) and the teammates act on it at once:

| Message | Sent when | What teammates do |
| --- | --- | --- |
| Contact | It sees an enemy (every 8 s per bot at most) | The spot goes into the team's memory; idle bots nearby go after it (Sharing) |
| Down | It dies | Where it was shooting (within 6 s), else where it fell, goes into memory; the nearest free attacker within `TRADE_RANGE` (70 studs) on that floor goes there to trade |
| Help | An attacker in a fight drops under `HELP_HEALTH` (60%), every `HELP_GAP` (6 s) at most | The nearest free attacker within `HELP_RANGE` (60 studs) on that floor comes to the enemy |
| Plant | An attacker gets into the bomb room | The squad stops gathering at the rally and pushes in now |
| Plan / Push / Site | The squad picks a bomb, pushes, or learns the site | Shared plan (the squad already holds it) |
| Rotate | Defenders see a new threat | Shared (the defender split already acts on it) |

"Free" means alive, not fighting, not fleeing and not holding a bomb room. Defenders answer threats through their home-bomb split instead, so a bomb's last guard never leaves. For tests the last messages are in `workspace.BotRadio` (attribute): `[Team] Name Kind: text`, with "(BOT X coming)" when a teammate answered.

Until later on 2026-11-17 these were callouts shown in the players' chat (packet `Siege.BotCall`, `Client.Hud.BotCallouts`, archived in `ServerStorage.Archive.BotCallouts_2026_11_17`).

### Looks (2026-11-17)

`dress(model, userId)` runs after spawn: from the bot's id (so the same bot looks the same every round) it picks a shirt, pants, hair, face and skin tone from `LOOKS` and applies them with `Humanoid:ApplyDescription` (body parts unchanged). The NPC's mesh head shows no face after that, so a `face` decal is added from the face asset's texture (`InsertService:LoadAsset`, cached). Hair parts don't collide, can't be hit and are massless, so they change nothing in a fight. The items are free official Roblox ones (found with `AvatarEditorService:SearchCatalog`). To add one, put its asset id in the list.

### What the match does with bots

- **Win rules:** bots count like players. A team whose players and bots are all dead loses. A side group with bots left has not "left".
- **Scoreboard and result screen:** bots are listed by name. Their kills and deaths are counted by SiegeService.
- **Kill feed:** shows "BOT Nova".
- **Class hiding:** drone and camera scans reveal a bot's class like a player's.
- **Not given to bots:** no coins, wins, quests, Battle Pass XP or analytics (they are left out of `Siege.Ended`'s players), no player drone (they drive their own, above), no camera, no snapshot.

## Tested (2026-11-16, Studio playtests, one admin player)

| Check | Result |
| --- | --- |
| BOTS tab | Shown for an admin. ADD Nova, Echo, Rook: added. Nova again: "BOT Nova is already in your party." |
| PLAY WITH PARTY, 1 player + 3 bots | Private 5 V 5, 2 v 2. `Expected` held only the player; the bots were in `Teams` and `Bots` |
| Selection | Each bot took a class no teammate had (BulletproofCamera, Trapper, Smoker, Breacher...), spawns and votes, then was ready |
| Defenders in Prep | Spawned and guarded one bomb room each (Guard mode) |
| Attackers in Action | Spawned, scouted, went upstairs and **planted a defuser on Bomb B**. In another round a defender bot killed an attacker bot |
| Defender out of its room | It hunted an attacker downstairs, killed it, then walked back up to its room |
| Mansion basement hatch (bot alone, map loaded) | Walked onto the hatch, shot it open in about 9 s, dropped into the Bomb A room and held it |
| Round change | Bot bodies cleared, sides swapped, bots picked again for their new side |
| Match end | Result screen listed the bots with kills and deaths. Then Idle, no bot bodies left, the player back in the lobby, the party still holding its bots |
| Party | Promote a bot: "A bot can't lead the party." Kick: removed. Leaving with only bots left ended the party |
| Output | No errors or warnings |

**Not tested:**
- Bots in a public queue against other players.
- Bots on a live reserved server (teleport, `Bots` read back from MemoryStore).
- A remote member's view of a party's bots.
- Clear House with bots (they join the attackers and fight the guards with the normal NPC behavior).
- A full 5 v 5 of bots.
- A full basement plant in a real match: the hatch was tested with the bot alone. (Done 2026-11-17 on Bank, see below.)

### Squad and basement (2026-11-17, Studio, Bank and Mansion)

- Bank, basement site forced, 3 attacker bots: the plan came first. Echo and Rook were in the basement in 12 to 16 s; the attackers planted both bombs and won in 43 s. Vex stayed upstairs by the vault.
- Mansion basement: the squad gathered, pushed and planted B in about 25 s, then went for A. A bot that passed the rally point on the way used to walk back to it; now it goes in.
- Outfits and faces were seen in a playtest.
- Radio, Bank Upstairs, two rounds (2 bots a side and the player): the plan, push, plants, contacts, rotations and downs were sent; help calls were answered by the nearest free attacker. Trade answers weren't seen (no attacker bot died near a free teammate).
- **Not tested:** a full multi-round match on every map, phones.

## Limits

- **Breaking in takes time:** several attackers going for the same boarded front door stand there while it breaks (Mansion: 10 to 15 s). Rooms behind soft walls only (the small side room of Bedrooms A) take up to 15 s of shooting before the bot gives up and goes round.

### Getting to the bomb rooms (2026-11-16, Studio, boards up, no defenders)

| Map, room | From | In the room after |
| --- | --- | --- |
| Mansion Main Floor B | Back Porch | 8 s |
| Mansion Main Floor A | Pool Side | 17 to 38 s |
| Mansion Upstairs A | Back Porch | 13 s |
| Mansion Upstairs B | Street Left | 11 to 52 s |
| Mansion Upstairs Bedrooms A | Street Right; in the pool | 45 to 46 s |
| Mansion Upstairs Bedrooms B | Roof Side | 44 to 53 s |
| Bank Upstairs A | Right Side | 13 to 15 s |
| Bank Upstairs B | Field; Backdoor | 38 s; 58 s |
| Bank Vault B | Front Street | 14 s |
| Bank Basement A | Front Street | 19 s |
| Bank Basement B | Backside | 25 to 31 s |

A bot dropped in the Mansion pool climbed out by the ladder and was in the house within 5 s.
- **Health bars:** bots stand in `workspace.Enemies`, so `HealthBillboards` gives every bot a health bar, teammates and enemies alike.
- **Fair-play shortcut:** attacker bots learn the site after 45 s of Action if nothing found it.

### Drones, memory and breaking in (2026-11-16)

| Check | Result |
| --- | --- |
| Drones, Bank | Before the board gap: no path into the bank at all, the drone never moved. After: both drones drove in; one went down to the basement and found the site 18 s after the drones came out |
| Drones, Mansion | Three drones drove into the house; the site (Basement) was found 40 s into Prep. One drone parked in Basement bomb room B. In another run the defenders shot both drones on their way to the vault |
| Shooting from range | DoorBoard1 from 21 and 13 studs, Board11 (a window) from 29, DoorBoardBuild from 14 and 28 |
| Defender threat | An attacker bot put in Mansion's Main Floor bomb room B next to its guard: the guard saw it, the defender upstairs was allowed to break boards within a second, came down, broke its own board into the room 5 s later and guarded it. When the threat was 10 s old it stopped breaking boards again |
| Output | No errors or warnings from the bot, NPC or drone modules |

Not tested: the remembered entrances over several rounds (rounds ended early: the test player was kicked when Studio lost its connection), a player seeing a bot drone's marks, and bots in a live server.

- **Bot ids are random:** two bots in the queue could share one in theory (1 in about 2 billion). The matchmaker would then drop the newer ticket.
