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

```lua
local Matchmaking = game.ServerScriptService.Modules.Systems.Matchmaking
local PartyService = require(Matchmaking.PartyService)
local QueueService = require(Matchmaking.QueueService)
```

A party table has `Id`, `L` (leader UserId) and `M` (member UserIds).

### `PartyService.Of(player) → Party?`

Their party (owned or mirrored), or `nil`.

```lua
local party = PartyService.Of(player)
print(party and #party.M or 1, "in party")
```

### `PartyService.Ensure(player) → Party`

Their party, making a party of one if they have none. `QueueService.Join` starts with this.

```lua
local party = PartyService.Ensure(player)
```

### `PartyService.Get(partyId) → Party?`

```lua
local party = PartyService.Get(ticket.P)
```

### `PartyService.IsLeader(player) → boolean`

```lua
if not PartyService.IsLeader(player) then
	return false, "Only the party leader can do that."
end
```

### `PartyService.Owns(party) → boolean`

`true` if this server owns it (the leader's server decides every change).

```lua
if not PartyService.Owns(party) then return end -- a mirror: show only
```

### `PartyService.UserIds(party) → { number }`

Its members' UserIds (bots are negative).

```lua
for _, userId in PartyService.UserIds(party) do print(userId) end
```

### `PartyService.Park(party)` / `PartyService.Restore(player, partyId)`

Keep a party in MemoryStore while its members play / put it back together when one returns (the first server to see a returning member owns it).

```lua
PartyService.Park(party) -- before teleporting its members
```

### `PartyService.SetTravelling(userId, on)`

A player leaving for a match is not leaving their party.

```lua
PartyService.SetTravelling(player.UserId, true)
```

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

### `QueueService.Join(player, modeId?) → (ok, message)`

Queues the leader's party for one mode (`nil`/`""` → `DEFAULT_MODE`, `"5v5"`). Lobby servers only.

```lua
local ok, message = QueueService.Join(player, "1v1")
if not ok then warn(message) end -- e.g. "Your party is too big for 1V1. Pick a different mode."
```

### `QueueService.JoinPrivate(player, modeId?) → (ok, message)`

"Play with party": a match of only the party's members, formed **at once** (no ticket, no wait). Members are dealt into two even teams. Needs `PRIVATE_MIN_PLAYERS` (2; `STUDIO_MIN_PLAYERS` = 1 in Studio) and at most `PrivateLimit(mode)`. Results count under `PRIVATE_MODE`, not the mode.

```lua
QueueService.JoinPrivate(player, "5v5")
```

### `QueueService.JoinTutorial(player) → (ok, message)`

Recruit Training, alone, against the training bot.

```lua
QueueService.JoinTutorial(player)
```

### `QueueService.Leave(player) → (ok, message)`

Leader only.

```lua
QueueService.Leave(player) -- "Left the queue."
```

### `QueueService.IsQueued(player) → boolean`

As far as this server knows.

```lua
if QueueService.IsQueued(player) then return false, "Leave the queue first." end
```

A party change (join, leave, kick, disconnect) takes the party out of the queue. Once the match is found, a leave changes nothing.

## Queue modes: `Content.Matchmaking`

Add a mode (2v2, 3v3…) by adding a row to `Content.Matchmaking.MODES`. A real row:

```lua title="Content.Matchmaking.MODES (Clear House)"
{ Id = "ClearHouse", Name = "CLEAR HOUSE", Category = "Arcade", Kind = "ClearHouse", Maps = { "Mansion", "Bank" },
  Tag = "NEW", Color = Color3.fromRGB(56, 40, 88), TagColor = Color3.fromRGB(52, 224, 176), Image = "", Icon = "PvE",
  Description = "Up to five players against NPC guards. Every door and window is boarded: breach in and clear every room. No bombs.",
  TeamSize = { Attackers = 5, Defenders = 0 }, MinTeamSize = { Attackers = 1, Defenders = 0 }, MaxWait = 20 },
```

| Field | Meaning |
| --- | --- |
| `Id`, `Name`, `Category` | Its Id (in tickets and records), display name, a `CATEGORIES` Id for the Game Modes panel |
| `TeamSize` / `MinTeamSize` | Full and smallest team sizes |
| `MaxWait` | Seconds the oldest ticket waits for a full match before a smaller one may start |
| `Kind` | `nil` for Siege, `"ClearHouse"`, `"Tutorial"` |
| `Maps` | Maps it may be played on (`nil`: `Content.Games.Siege.MAP_POOL`) |
| `BotFill` | Seconds of waiting after which bots fill the empty spots (`nil`: never) |
| `MinLevel` | Account level needed to queue |
| `Tag`, `Color`, `TagColor`, `Image`, `Icon`, `Description` | How its card looks |

### `Matchmaking.GetMode(id) → Mode?`

```lua
local MatchmakingContent = require(game.ReplicatedStorage.Content.Matchmaking)
local mode = MatchmakingContent.GetMode("5v5")
print(mode.Name, mode.TeamSize.Attackers)
```

### `Matchmaking.ModesIn(categoryId) → { Mode }`

```lua
for _, mode in MatchmakingContent.ModesIn("Arcade") do print(mode.Id) end
```

### `Matchmaking.PartyLimit(mode) → number`

The biggest party a mode allows: the smaller side, or the only side when the other is 0.

```lua
print(MatchmakingContent.PartyLimit(MatchmakingContent.GetMode("5v5"))) -- 5
```

### `Matchmaking.PrivateLimit(mode) → number` / `Matchmaking.FitMode(modeId, size, private) → Mode?`

Biggest party for a private match / the mode a party of that size plays (the picked one, or the next of its category that fits).

```lua
local mode = MatchmakingContent.FitMode("1v1", 3, false) -- a mode a party of 3 fits
```

## Helpers you can reuse

### `Store.Sorted(name)` / `Store.Hash(name)`

A MemoryStore SortedMap / HashMap wrapper whose calls retry with backoff (`Helpers.Retry`). In Studio (`ServerRole.IsLocal()`) they're local stand-ins, so the queue works offline. Methods used in the code: `Set(key, value, ttl, sortKey?)`, `Remove(key)`, and reads.

```lua
local Store = require(Matchmaking.Store)
local queue = Store.Sorted(MatchmakingContent.QUEUE_MAP)
queue.Set(party.Id, ticket, MatchmakingContent.TICKET_TTL, ticket.T)
```

### `Store.Publish(topic, message)` / `Store.Subscribe(topic, handler)` / `Store.Now()`

MessagingService with retries; `Now()` is the shared clock tickets are sorted by.

```lua
Store.Subscribe(MatchmakingContent.MATCH_TOPIC, function(message) print(message.K, message.I) end)
Store.Publish(MatchmakingContent.MATCH_TOPIC, { K = "Match", I = matchId, U = userIds })
```

### `TeamPacker.Pack(tickets, now, limits) → sides?`

The next match's two sides from the oldest tickets, or `nil`.

### `Helpers.Retry.Call(label, fn, attempts?)`

See [Handlers and helpers](../foundations/helpers.md#helpersretry-server).

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

```lua
local Core = game.ReplicatedStorage.Modules.Client.Core
local Matchmaking = require(Core.Matchmaking)
local ModeMenu = require(Core.ModeMenu)
```

| Function | Does | Example |
| --- | --- | --- |
| `Matchmaking.Play()` | The PLAY button (K): queue for the picked mode, or cancel | `Matchmaking.Play()` |
| `Matchmaking.PlayWithParty()` | PLAY WITH PARTY | `Matchmaking.PlayWithParty()` |
| `Matchmaking.Queued()` | Searching right now | `if Matchmaking.Queued() then button.Text = "CANCEL" end` |
| `Matchmaking.OpenModes()` | The Game Modes panel (leader only, not while searching) | `Matchmaking.OpenModes()` |
| `Matchmaking.OpenParty()` | The Party menu (L) | `Matchmaking.OpenParty()` |
| `ModeMenu.Selected()` | The picked mode's Id (this client only; the server re-checks) | `print(ModeMenu.Selected())` |
| `ModeMenu.Pick(modeId)` | Pick one | `ModeMenu.Pick("ClearHouse")` |
| `ModeMenu.Open()` | Open the panel | `ModeMenu.Open()` |
| `ModeMenu.SetPartySize(size)` | Grey out modes the party is too big for | `ModeMenu.SetPartySize(#party.Members)` |
| `ModeMenu.Changed` | Signal: the new Id | `ModeMenu.Changed:Connect(print)` |
