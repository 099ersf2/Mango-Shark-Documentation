# Matchmaking and parties

Players queue for Siege from a lobby server, alone or as a party of up to five. When a match forms, everyone in it is teleported to one reserved server that hosts that match and nothing else. When the match ends they go back to lobby servers, each party together.

**All matchmaking matches are played on reserved servers. A lobby server never hosts a Siege match.** Built 2026-11-11. The live cross-server flow has **not** been tested yet: see [Tested](#tested-2026-11-11-studio-one-player).

## Server roles

The place is one place with two kinds of server (`Systems.Matchmaking.ServerRole`):

| Role | What it is | What it does |
| --- | --- | --- |
| **Lobby** | A normal server (public, or a private server someone owns) | Parties, invites, the queue, the matchmaker. Never a match |
| **Match** | A reserved server (`TeleportService:ReserveServer`): it has a `PrivateServerId` and no owner | Exactly one Siege match: rounds, teams, classes, drones, cameras, objectives, scoreboard, win rules |
| **Studio** | Roblox Studio | Both at once, since Studio has no reserved servers |

## Where things are

| What | Where |
| --- | --- |
| Every number and name | `ReplicatedStorage.Content.Matchmaking` |
| Server role | `ServerScriptService.Modules.Systems.Matchmaking.ServerRole` |
| MemoryStore and MessagingService (the only module that touches them) | `Systems.Matchmaking.Store` |
| Retry with backoff | `ServerScriptService.Modules.Helpers.Retry` |
| Parties | `Systems.Matchmaking.PartyService` |
| Queue, matchmaker, match hand-off, teleports | `Systems.Matchmaking.QueueService` |
| Team packing (pure logic) | `Systems.Matchmaking.TeamPacker` |
| The match server's side | `Systems.Matchmaking.MatchHost` |
| Client | `ReplicatedStorage.Modules.Client.Core.Matchmaking` |
| UI | `StarterGui.Main.Lobby` (the PLAY bar), `Main.Party` (the Party menu), `Main.PartyInvite`; templates `PartySlot`, `InviteRow` |
| Packets | `Packets.Party` (`Request`, `State`, `Invite`, `InviteClosed`), `Packets.Queue` (`Request`, `State`) |

## How it plays

The UI was rebuilt on 2026-11-12 ([UI.md](UI.md#the-lobby)): the queue and the party are no longer one menu.

- **PLAY** is a big green button in the bottom center of the lobby (`Main.Lobby.Play`, key K). Pressing it queues the party at once. While searching it is red and cancels, with the status and timer above it. Only the party leader can use it; for a member it is grey. The bar hides during a match.
- **PARTY** (beside PLAY, key L) opens the Party menu (`Main.Party`): five member rows; the leader can make a member the leader (LEAD) or KICK them; anyone can LEAVE PARTY.
- **Invite list** (in the Party menu): two tabs. *This server* lists players here. *Friends* lists friends who are online in this game. Only the leader invites.
- **Invite popup:** "NAME invited you to their party", Accept or Decline, for 30 s.
- A change to a queued party (someone joins, leaves, is kicked or disconnects) takes it out of the queue.

## Parties

- Up to `MAX_PARTY_SIZE` (5) players. A player with no party is treated as a party of one when they invite or queue.
- **The party lives on its leader's lobby server.** That server owns it and decides every change. Other servers that have a member hold a copy they only show.
- Changes travel on the MessagingService topic `PARTY_TOPIC`:

| Message | From → to | Meaning |
| --- | --- | --- |
| `Invite` | owner → the invited player's server | Show the popup. Across servers the target must be a friend of the leader (the owner checks `IsFriendsWith`) |
| `Accept`, `Decline`, `Leave`, `Rejoin` | a member's server → owner | Requests. The owner checks the invite, the size and the member list |
| `State` | owner → every server with a member | The whole party with a version number. Also sent every 30 s as a heartbeat |
| `Disband` | owner → every server with a member | The party is gone |
| `Queue` | owner → every server with a member | Queued or not, and since when, for the members' timers |

- **Promote** moves ownership to the new leader's server (the `State` carries the new owner).
- **The leader leaves:** the member who joined first becomes leader, and their server the owner.
- **The owner server dies:** copies with no heartbeat for 100 s are dropped.
- **Party state through a match:** when a party's match is found, its owner saves it in MemoryStore (`PARTY_MAP`, 30 minutes). Returning players carry only `{ PartyId }` in their teleport data. The lobby server reads the saved party, checks the player is in it, and rebuilds it: the first server to see a returning member claims ownership, later ones rejoin through it.

## Queue modes

A party queues for one **mode**, and only tickets of the same mode are matched together. Modes are rows in `Content.Matchmaking.MODES`:

| Id | Name | Team size (each side) | Smallest match | Wait before a smaller match |
| --- | --- | --- | --- | --- |
| `1v1` | 1 V 1 | 1 | 1 v 1 | 60 s (never smaller than 1 v 1) |
| `5v5` | 5 V 5 | 5 | 1 v 1 | 60 s |

- `DEFAULT_MODE` is the mode the lobby bar starts on (`5v5` today; with `1v1` two players are enough for a match).
- The leader picks the mode in the **Game Modes panel** (the MODE button right of PLAY; [UI.md](UI.md#the-game-modes-panel)). It has no key. The pick travels with the queue request; the server checks the mode exists and that the party fits on one side of it. A party of two can't queue for 1 V 1.
- The mode's Id is in the ticket (`G`) and in the match record (`Mode`).
- **Categories.** Each mode names a category (`CATEGORIES`). The panel shows one card per category that has a mode. Since the owner's edit on 2026-11-12 there is one category, **SIEGE**, holding both modes, and `DEFAULT_MODE` is `5v5` (the table above still lists the modes correctly).
- **Card look.** A category row and a mode row both carry `Tag`, `TagColor`, `Color`, `Image` and `Icon` ([UI.md](UI.md#what-a-card-shows)).
- **To add a mode**, add a row to `MODES` (Id, Name, Category, Tag, Color, TagColor, Image, Icon, Description, TeamSize, MinTeamSize, MaxWait). Nothing else changes: the panel and the matchmaker read the table. Never reuse an old Id. To add a category, add a row to `CATEGORIES`.
- All modes share one queue map, so the matchmaker still makes one queue read per pass. It reads the 100 oldest tickets of all modes together; if one mode ever fills that window, give each mode its own map.

## Play with party (2026-11-12)

> **Not run.** Written on 2026-11-12 with no playtest (by request). The scripts compile and the UI parts the code waits for exist; none of it has been seen working.

The lobby bar's **PLAY WITH PARTY** button (`Main.Lobby.PartyPlay`, above PLAY) starts a match with only the party's own members in it.

- Request: `Queue.Request` with the action `Private`. Server: `QueueService.JoinPrivate(player)`.
- Only the leader may, on the server that owns the party, and not while the party is searching.
- It needs `PRIVATE_MIN_PLAYERS` (2) members; in Studio one is enough. The button shows from that size up.
- **Teams:** the members are shuffled and dealt into two teams as even as their number allows (2 → 1 v 1, 3 → 2 v 1, 4 → 2 v 2, 5 → 3 v 2). Which half attacks is random.
- There is no ticket and no wait: the match is formed at once through the same steps as a queued one (reserve a server, save the record, publish, teleport). The record's `Mode` is `Private`. Nobody outside the party is ever added.

## Party sync (2026-11-12, not run)

**The bug:** back in the lobby after a match, a player's screen showed no party, while inviting the same people was refused because they were already in it. The server was right and the screen was behind.

**Why:** the server sends `Party.State` only when a party changes. A returning player is put back in their party the moment they join the lobby server, and that message could go out before their client was listening for it. Nothing sent it again.

**Now:** the client asks. `Party.Request` has a `Sync` action that makes the server send that player's `Party.State` once more. `Client.Core.Matchmaking` sends it when it starts, again 3, 8 and 20 seconds later (restoring a party reads MemoryStore, which takes a moment), when a match ends, and whenever the Party menu opens.

## Leaving a queued party (2026-11-12)

A member who leaves a queued party (leaves, is kicked, disconnects) takes the whole party out of the queue; that was already so. What was missing: **the member who left was never told**, so their bar kept showing the search. `dequeue` now tells every player who was on the ticket, on this server and (through the `Queue` party message's new `U` list) on others. Once the match is found the ticket is gone, and a leave changes nothing: the match goes ahead.

## The queue

A MemoryStore **SortedMap** (`QUEUE_MAP`).

| Part | Value |
| --- | --- |
| Key | The PartyId, so a party can never have two tickets |
| Sort key | The time it queued (Unix seconds): the oldest ticket is first |
| Value | `{ P = PartyId, M = member UserIds, N = party size, T = queue time, J = owner server JobId, L = leader UserId, G = mode Id }` |
| Lifetime | 150 s (`TICKET_TTL`). The owner server refreshes it every 50 s, so a dead server's tickets expire by themselves |

The matchmaker also drops malformed tickets (an unknown mode, or a party too large for its mode, included), and any ticket naming a player that an older ticket already names (the older one wins), so a player is never in two matches.

## The matchmaker

Only one lobby server forms matches at a time.

- Every `TICK` (3 s) each lobby server tries to take or renew a **lease** in a MemoryStore HashMap (`LOCK_MAP`, key `Lease`, value `{ J = JobId, E = expiry }`), with a 15 s lifetime.
- A server takes the lease only if it is free, expired, or already its own. The update is atomic (`UpdateAsync`).
- If the holder dies it stops renewing; the lease runs out and the next server to try takes it.

Each pass the holder reads the 100 oldest tickets, sorts them by mode, and asks `TeamPacker` for matches one mode at a time, each with that mode's sizes (up to 4 matches per pass in all).

### Team filling

Sizes come from the ticket's mode (`TeamSize`, `MinTeamSize`, `MaxWait`). `TEAM_SIZE` and `MIN_TEAM_SIZE` are the largest and smallest any mode uses; the map check and the mid-match check read them.

1. The oldest ticket is always in the match that forms, so nobody is starved.
2. A party is one item. It is never split between matches or between the two sides.
3. A full match (both sides at the mode's team size) is taken whenever one exists among the 14 oldest tickets; among full matches, the one using the oldest tickets.
4. Once the mode's oldest ticket has waited its `MaxWait` (60 s), a smaller match may form: the most players that fit, then the most even sides, then the oldest tickets. Each side at least its minimum.
5. Which side a group gets is random when both arrangements are legal.

## Forming a match

1. `TeleportService:ReserveServer` gives the access code and the reserved server's `PrivateServerId`.
2. The **match record** is saved in a MemoryStore HashMap (`MATCH_MAP`, 30 minutes): `{ Id, Mode, Teams = { Attackers, Defenders }, Map, Code, ServerId, Expected, Parties, Created }`.
3. The tickets are removed from the queue.
4. `{ K = "Match", I = MatchId, U = UserIds }` is published on `MATCH_TOPIC`.
5. Each lobby server reads the record for the players it has, saves their parties, and teleports them with the access code. **The teleport data is only `{ MatchId }`.**

If the reserve or the save fails, the tickets stay queued and the next pass tries again.

## On the match server

`Systems.Matchmaking.MatchHost`:

1. The first player's `MatchId` is only a key. The server reads the record from MemoryStore and checks the record's `ServerId` is its own `PrivateServerId`, so a made-up id can't start another match there.
2. **Teams come from the record, never from teleport data or the client.**
3. `Matchmaking.MatchReady` fires; Siege waits for the expected players ([SIEGE.md](SIEGE.md)).
4. A player who is not in the record is sent back to a lobby.
5. At the end `MatchHost.ReturnAll` teleports each party together to a lobby server with `{ PartyId }`.

Characters don't load by themselves on a match server (`Players.CharacterAutoLoads` is off).

## Reliability

- **Every MemoryStore and MessagingService call** goes through `Systems.Matchmaking.Store` and `Helpers.Retry`: a `pcall`, up to 4 attempts, waits of 0.5 s doubling to at most 8 s with some randomness, and twice as long when the error looks like throttling.
- **Duplicate messages:** each message has an id; one seen in the last 90 s is ignored.
- **Message size:** a message over 950 bytes is refused with a warning (the limit is 1 kB). A party of five and a ten-player match fit.
- **Stale tickets** expire; **stale party copies** are dropped.
- **Teleport failure:** retried 3 times. Players who still can't go are told. If their whole party is still on that lobby server, it goes back in the queue at its old place; otherwise the leader queues again. The match server drops players who never arrive when its waiting time ends.
- **Matchmaker failover:** the lease expiring.
- **Limits:** MemoryStore allows 1000 + 100 × players requests a minute for the game. Each lobby server spends about 20 a minute on the lease; the holder adds about 20 for the queue read, plus a few per match.

## Studio

`ServerRole.IsLocal()` (Studio with `STUDIO_LOCAL` on):

- The store is tables in the server's memory; messages are delivered straight back to the same server. The queue, lease and packing code are the same code that runs live.
- There is no reserve and no teleport. A formed match is handed to the same server (`Matchmaking.Assigned`), and every expected player "arrives" at once.
- A match may start with one side empty (`STUDIO_MIN_PLAYERS = 1`) after 4 s (`STUDIO_MAX_WAIT`).
- Set the workspace attribute `SiegeTestTeam` to `Attackers` or `Defenders` to put everyone queued on that side.
- After the match everyone gets a body again and is sent to the lobby spawn.

## API

```lua
local Matchmaking = ServerScriptService.Modules.Systems.Matchmaking
local QueueService = require(Matchmaking.QueueService)
QueueService.Join(player, modeId) -- ok, message (leader only). No mode: DEFAULT_MODE
QueueService.JoinPrivate(player)  -- ok, message: a match of the leader's party only, formed at once
QueueService.Leave(player)
QueueService.IsQueued(player)

local PartyService = require(Matchmaking.PartyService)
PartyService.Of(player)          -- the party, or nil
PartyService.Ensure(player)      -- the party, making a party of one
PartyService.IsLeader(player)
PartyService.UserIds(party)

local MatchHost = require(Matchmaking.MatchHost)
MatchHost.Record()               -- the match this server hosts, or nil
MatchHost.TeamOf(userId)
MatchHost.ReturnAll()

local ServerRole = require(Matchmaking.ServerRole)
ServerRole.Kind()                -- "Lobby", "Match" or "Studio"
```

| Extension point | Kind | Arguments |
| --- | --- | --- |
| `Party.PreventInvite` | Any | player, targetUserId |
| `Party.Changed` / `Party.Disbanded` | Fire | partyId |
| `Queue.PreventJoin` | Any | player |
| `Queue.Joined` / `Queue.Left` | Fire | partyId, ticket / partyId, reason |
| `Matchmaking.MatchFormed` | Fire | record (on the matchmaker) |
| `Matchmaking.Assigned` | Fire | record (Studio: a match to host here) |
| `Matchmaking.MatchReady` / `Matchmaking.Arrived` | Fire | record / player, record (on the match server) |

## Tested (2026-11-11, Studio, one player)

| Check | Result |
| --- | --- |
| Join the queue | Accepted; `Queue.Joined` fired with a party of 1 |
| Join again while queued | Refused: "Already in the queue." |
| Cancel | Left the queue |
| Join, then wait | A match formed 5.3 s later (the 4 s Studio wait plus the 3 s tick), on the forced side; the host fired `MatchReady` and `Arrived` |
| Team packing, made-up tickets | 10 solos → 5 v 5. Parties of 5 and 5 → one each side. Parties of 4, 3, 2, 1 → 3+2 against 4+1, nobody split. Three parties of 3 → no match before 60 s, then 3 v 3 with the third party left queued. A solo alone → no match. Parties of 5, 4, 4, 1, 1 → 5 against 4+1 |
| Play menu | The Play button hides during a match and comes back after |

## Tested (2026-11-12, queue modes, Studio, one player)

| Check | Result |
| --- | --- |
| Queue for a mode that doesn't exist | Refused: "That game mode does not exist." |
| The mode key, M (removed since: the mode is now picked in the Game Modes panel) | 1 V 1 → 5 V 5 → 1 V 1; PLAY's small line followed |
| Queue 1 V 1 with made-up tickets in the queue (a 1v1 solo, a 5v5 solo, an unknown mode, a party of two marked 1v1) | The 1v1 match formed with the player and the 1v1 solo, one each side, record `Mode = "1v1"`. The 5v5 solo formed its own match (Studio lets one side be empty). The unknown-mode ticket and the oversized party were in no match |
| Team packing with the live 1v1 limits | One solo: no match, however long it waited. Three solos: 1 v 1 with the two oldest |

Not verified: the Game Modes panel (built after this test, compile-checked only), two real players queueing 1 V 1 against each other, a party refused for 1 V 1 from the UI, and everything on live servers (below).

**Not verified. None of this has run on live servers:**
- MemoryStore and MessagingService themselves (Studio used the local stand-ins).
- `ReserveServer`, the teleport to the match server, and the teleport back.
- The matchmaker lease with more than one lobby server, and failover.
- Parties across servers: invites, ownership moving on Promote, heartbeats, restoring a party after a match.
- Teleport failures and requeueing.
- Parties and invites with two or more players, even on one server.
- The Play menu with real clicks, a gamepad and touch.

## Limits

- The lobby is still off in the place (its portals are missing), so on a lobby server players currently spawn on the map with guns while they queue. See [NEXT_STEPS.md](NEXT_STEPS.md).
- No skill or region matching: oldest first.
- A restored party's leader is whoever arrives first on the owner server, unless the old leader lands on that same server.
- If a parked party's first server dies before the others arrive, the rest are not rejoined.
