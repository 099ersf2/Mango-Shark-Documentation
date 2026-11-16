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
- **No gadgets:** bots don't use class gadgets, drones or cameras.

### The plan (every `THINK` = 0.5 s in Prep and Action)

Fighting always comes first: the NPC tree only follows the plan when there is nothing to shoot or hunt.

**Defenders**
- They guard a bomb room in NPC Guard mode: stay inside, patrol, rebuild its doors and windows, fight first.
- They split between the two rooms.
- When an attacker is planting a defuser on a bomb, every defender bot goes to that room.
- Once a bomb has its defuser, they all hold the other one.
- A defender outside its room (it spawned elsewhere, or fell through a floor) walks back first, then guards it.

**Attackers**
- **Finding the site:** they have no drones, so they learn the site when a player's drone finds it, or after `SITE_INTEL_TIME` (25 s) of Action. Until then they check the sites nearest them. A bot that walks into the real site tells the other bots.
- **Choosing a bomb:** each takes one of the bombs still without a defuser, split between them.
- **Planting:** inside the bomb room (`ROOM_HOLD` studs in from its edges) the bot switches to Guard mode on that room. It stays in and keeps fighting while the defuser plants (8 s); leaving would reset it.
- **Hatches:** for a room on a floor below with no way down (the Mansion basement), the bot walks onto the hatch over that room, shoots it open (`HATCH_SHOOT`, 5 studs) and drops through. Only hatches on the floor right above count (`HATCH_ABOVE`).
- **Shut out:** with no path to its room (or the hatch) for `DOOR_AFTER` (6 s), the bot picks the boarded door or window on its floor that best leads toward the room, stands in front of it and shoots the boards off. Doors come first: a window counts `WINDOW_COST` studs farther because it has to be climbed. A door or window it has tried is not picked again.
- **Unstick:** a bot that hasn't moved for `STUCK_TIME` (5 s) on its way somewhere walks 14 to 24 studs off for 4 s, then tries again. The spot is on its own floor (within 3 studs), never in water or a pit. Pathfinding sometimes "finds" a way straight up to the floor above.
- **Paths through doors** (2026-11-16): an attacker's paths may go through intact boards (`BreakThrough`), so it heads for a boarded door like an open one and breaks it when it gets there. Defenders' paths don't, so they never break their own boards.
- **Climbing and water:** bots climb trusses (the Mansion pool has an invisible one on its ladder) and walk round water.
- **Unreachable rooms:** a room with no path for `NO_WAY_TIME` (20 s), and no breach under way, is skipped for 40 s. The bot takes the other bomb, or hunts defenders if neither is reachable.
- **Focus:** a bot heading somewhere ignores gunshots and hunt spots on another floor, so it doesn't stand under an enemy it heard instead of going on.

### What the match does with bots

- **Win rules:** bots count like players. A team whose players and bots are all dead loses. A side group with bots left has not "left".
- **Scoreboard and result screen:** bots are listed by name. Their kills and deaths are counted by SiegeService.
- **Kill feed:** shows "BOT Nova".
- **Class hiding:** drone and camera scans reveal a bot's class like a player's.
- **Not given to bots:** no coins, wins, quests, Battle Pass XP or analytics (they are left out of `Siege.Ended`'s players), no drone, no camera, no snapshot.

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
- A full basement plant in a real match: the hatch was tested with the bot alone.

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
- **Fair-play shortcut:** attacker bots learn the site after 25 s without drones.
- **Bot ids are random:** two bots in the queue could share one in theory (1 in about 2 billion). The matchmaker would then drop the newer ticket.
