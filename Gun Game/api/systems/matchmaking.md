# Matchmaking and parties

Players gather in **parties** on lobby servers, the party leader **queues** for a mode, a single **matchmaker** packs tickets into matches, and everyone is teleported to a reserved match server.

!!! abstract "Source"

    `Systems.Matchmaking.PartyService`, `QueueService`, `TeamPacker`, `MatchHost`, `Store`, `ServerRole`; client `Client.Core.Matchmaking`, `Client.Core.ModeMenu`. Data: `Content.Matchmaking`. Design guide: [Matchmaking and parties](../../MATCHMAKING.md).

## The journey of a match

```text
Lobby server(s)                                                          Match server
───────────────                                                          ────────────
1 Leader presses PLAY ─▶ Queue.Request("Join", modeId)
2 QueueService.Join: checks ─▶ ticket in MemoryStore SortedMap (key = PartyId)
3 Matchmaker (whoever holds the lease) reads oldest tickets ─▶ TeamPacker.Pack
4 ReserveServer ─▶ match record in MATCH_MAP ─▶ tickets removed
5 Publish on MATCH_TOPIC ─▶ every lobby parks its parties, teleports { MatchId } ──▶ MatchHost reads record
                                                                                   SiegeService runs it
6                                                         ◀── ReturnAll (PartyId in teleport data)
7 PartyService.Restore puts each party back together
```

Key design choices, from the `QueueService` header:

- **One ticket per party.** The key is the PartyId, so a party can never queue twice. The sort key is when it queued (oldest first).
- **Tickets expire by themselves.** The owning lobby refreshes each ticket every `TICKET_REFRESH` s; one not refreshed for `TICKET_TTL` s vanishes, so a crashed server's tickets go away.
- **One matchmaker at a time.** Lobby servers compete for a lease in a MemoryStore HashMap; only the holder forms matches. If it dies, the lease runs out and another takes over.
- **The client never says which team.** Teleport data is only `{ MatchId }`; the match server reads teams from the record.
- **Modes never mix.** Tickets are sorted by mode and each mode is packed by itself.

## Parties: `PartyService`

A party is up to `Content.Matchmaking.MAX_PARTY_SIZE` players, possibly on **different lobby servers**. The server the leader is on **owns** the real party; others hold a mirror and only show it. Changes travel over MessagingService (`PARTY_TOPIC`).

| Function | Returns / does |
| --- | --- |
| `PartyService.Of(player)` | Their party (owned or mirrored), or `nil` |
| `PartyService.Ensure(player)` | Their party, making a party of one if they have none |
| `PartyService.Get(partyId)` | A party by Id |
| `PartyService.IsLeader(player)` | `true` if they lead it |
| `PartyService.Owns(party)` | `true` if this server owns it |
| `PartyService.UserIds(party)` | Its members' UserIds |
| `PartyService.Park(party)` / `Restore(player, partyId)` | Keep a party in MemoryStore during a match / rebuild it on return |
| `PartyService.SetTravelling(userId, on)` | A player leaving for a match is not leaving their party |

If the leader leaves, the oldest member leads. Admins may add **bots** (negative UserIds) from the BOTS tab; a bot never leads.

## The queue: `QueueService`

```lua title="Systems.Matchmaking.QueueService.Join (trimmed)"
function QueueService.Join(player: Player, modeId: string?): (boolean, string)
	if not ServerRole.IsLobby() then
		return false, "You can't queue from here."
	end
	local mode = Matchmaking.GetMode(if modeId == nil or modeId == "" then Matchmaking.DEFAULT_MODE else modeId)
	if not mode then
		return false, "That game mode does not exist."
	end
	local party = PartyService.Ensure(player)
	if party.L ~= player.UserId or not PartyService.Owns(party) then
		return false, "Only the party leader can queue."
	end
	local members = PartyService.UserIds(party)
	if #members > Matchmaking.MAX_PARTY_SIZE or #members > Matchmaking.PartyLimit(mode) then
		return false, `Your party is too big for {mode.Name}. Pick a different mode.`
	end
	if Extensions.Any("Queue.PreventJoin", player) then
		return false, "You can't queue right now."
	end
	-- (MinLevel checks), then the ticket:
	local ticket = { P = party.Id, M = members, N = #members, T = Store.Now(), J = jobId, L = party.L, G = mode.Id, B = botsOf(party) }
	if not queue.Set(party.Id, ticket, Matchmaking.TICKET_TTL, ticket.T) then
		return false, "The queue is busy. Try again."
	end
	-- ...
	Extensions.Fire("Queue.Joined", party.Id, ticket)
	return true, `Searching for a {mode.Name} match.`
end
```

Every function returns **`(ok, message)`**: the message is ready to show the player.

| Function | What it does |
| --- | --- |
| `QueueService.Join(player, modeId?)` | Leader only. `nil`/`""` → `DEFAULT_MODE` |
| `QueueService.JoinPrivate(player, modeId?)` | "Play with party": a match of only the party's members, formed **at once** (no ticket). Needs `PRIVATE_MIN_PLAYERS` (1 in Studio) and at most `PrivateLimit(mode)` |
| `QueueService.JoinTutorial(player)` | Recruit Training, alone, against the training bot |
| `QueueService.Leave(player)` | Leader only |
| `QueueService.IsQueued(player)` | As far as this server knows |

A party change (join, leave, kick, disconnect) takes the party out of the queue. Once the match is found, a leave changes nothing.

## Queue modes: `Content.Matchmaking`

Add a mode (2v2, 3v3…) by adding a row to `Content.Matchmaking.MODES`. Helpers:

| Function | Returns |
| --- | --- |
| `GetMode(id)` / `ModesIn(categoryId)` | A mode by Id (or `nil`) / the modes of one category |
| `PartyLimit(mode)` | The biggest party a mode allows (the smaller side, or the only side) |
| `PrivateLimit(mode)` / `FitMode(modeId, size, private)` | Biggest private party / the mode a party of that size plays |

A mode with `Kind = "ClearHouse"` or `"Tutorial"` starts those match kinds; `MinLevel` gates by account level.

## Helpers you can reuse

| Function | What it does |
| --- | --- |
| `Store.Sorted(name)` / `Hash(name)` / `Publish(topic, msg)` / `Subscribe(topic, fn)` / `Now()` | MemoryStore and MessagingService **with retries**, and local stand-ins in Studio |
| `Helpers.Retry.Call(label, fn, attempts?)` | `pcall` with retries and exponential backoff |
| `TeamPacker.Pack(tickets, now, limits)` | The next match's two sides, or `nil` |

## Extension points

| Point | Kind | Arguments |
| --- | --- | --- |
| `Party.PreventInvite` | Any | player, targetUserId |
| `Party.Changed` / `Party.Disbanded` | Fire | partyId |
| `Queue.PreventJoin` | Any | player |
| `Queue.Joined` / `Queue.Left` | Fire | partyId, ticket / partyId, reason |
| `Matchmaking.MatchFormed` / `Assigned` / `MatchReady` | Fire | record |
| `Matchmaking.Arrived` | Fire | player, record |

## Packets

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Party.Request` | Client → server, answered `(ok, message)` | action (`Invite`, `Accept`, `Decline`, `Leave`, `Kick`, `Promote`, `Sync`, `AddBot`), argument |
| `Party.State` | Server → one client | `{ Id, Leader, Max, Members = { { UserId, Name, Here } } }` or `nil` |
| `Party.Invite` / `Party.InviteClosed` | Server → one client | PartyId, leader name, leader UserId, seconds / PartyId |
| `Queue.Request` | Client → server, answered `(ok, message)` | `Join`, `Private`, `Tutorial` or `Leave`; the mode Id (`""` for default) |
| `Queue.State` | Server → one client | `{ Queued, Since, Status, Size, Mode }` |

## Client

| Function | What it does |
| --- | --- |
| `Client.Core.Matchmaking.Play()` / `PlayWithParty()` / `OpenModes()` / `OpenParty()` | The lobby's PLAY / PLAY WITH PARTY buttons; the Game Modes and Party panels |
| `Client.Core.ModeMenu.Selected()` / `Pick(modeId)` / `Open()` / `.Changed` / `SetPartySize(size)` | The picked mode (client-only; the server re-checks it) |
