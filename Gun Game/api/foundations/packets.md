# Networking with Packets

All client–server traffic goes through **`Shared.Packets`** (reliable) and **`Shared.UnreliablePackets`** (cosmetic, may drop). There are no RemoteEvents or RemoteFunctions in game code.

!!! abstract "Source"

    `ReplicatedStorage.Modules.Shared.Packets`, `ReplicatedStorage.Modules.Shared.UnreliablePackets`, built on `Modules.Utilities.Packet`. Every packet is listed in [All packets](../reference/packets.md).

## Why one module

Both sides `require` the same `Packets` table, so both build the same packets with the same types. The module's own warning:

> Never build a packet with the same name somewhere else: a second copy of the packet library cannot read the first one's traffic.

## Declaring a packet

Packets are grouped by feature. Each is a name and the **types** of its arguments, which the library uses to pack them into a small buffer:

```lua title="Shared.Packets (excerpt)"
Gun = {
	-- Client -> server. A trigger pull: server time, origin, unit aim direction, random seed and the spread cone in
	-- degrees. Pellet directions are rebuilt from the seed on every side.
	Fire = Packet("GunFire", Packet.NumberF64, Packet.Vector3F32, Packet.Vector3F32, Packet.NumberU32, Packet.NumberF32),

	-- Server -> one client. One of their bullets hit a humanoid: was it a headshot, and did it kill.
	HitConfirm = Packet("GunHitConfirm", Packet.Boolean8, Packet.Boolean8),
},

Queue = {
	-- Client -> server, answered (ok, message).
	Request = Packet("QueueRequest", Packet.String, Packet.String):Response(Packet.Boolean8, Packet.String),
},
```

| Type | Use for |
| --- | --- |
| `Packet.String` | Ids, names, actions |
| `Packet.Boolean8` | Flags |
| `Packet.NumberF64` | Server timestamps (`workspace:GetServerTimeNow()`), UserIds |
| `Packet.NumberF32` | Seconds, amounts, angles |
| `Packet.NumberU32` | Seeds and counts |
| `Packet.Vector3F32` | Positions and directions |
| `Packet.Instance` | A model or part both sides can see |
| `Packet.Any` | Tables (snapshots, state). Flexible but biggest: use typed fields for anything sent often |

Every packet's comment says its **direction** and what each argument means. Keep that up when you add one.

## Two kinds of packet

### One-way events

Fire and forget. Use them for intent the server doesn't need to answer, and for state the server pushes.

```lua
-- Client: send intent
Packets.Gun.Reload:Fire()

-- Server: listen
Packets.Gun.Reload.OnServerEvent:Connect(function(player)
	GunService.Reload(player)
end)

-- Server: tell one client, or everyone
Packets.Gun.HitConfirm:FireClient(player, headshot, killed)
Packets.Combat.Hit:Fire(victimCharacter, damage)      -- every client

-- Client: listen
Packets.Class.Flash.OnClientEvent:Connect(function(seconds)
	-- show the white screen
end)
```

### Answered requests (`:Response`)

A packet declared with `:Response(...)` works like a function call: the client's `:Fire` **yields** and returns what the server's handler returns. Use these when the player needs to know if it worked ("Only the party leader can queue.").

The real queue button, both halves:

```lua title="Client.Core.Matchmaking (the PLAY button)"
busy = true
local ok, text = Packets.Queue.Request:Fire(action, modeId)
busy = false
if ok == true then
	UIFeel.Play("Confirm")
else
	UIFeel.Play("Error")
	say(if ok == nil then "The server did not answer. Try again." else text)
end
```

```lua title="Systems.Matchmaking.QueueService"
local function onRequest(player: Player, action: any, modeId: any)
	-- (rate limit first)
	if action == "Join" then
		if type(modeId) ~= "string" or #modeId > MAX_ID_LENGTH then
			return false, "That game mode does not exist."
		end
		return QueueService.Join(player, modeId)
	elseif action == "Leave" then
		return QueueService.Leave(player)
	end
	return false, "Unknown action."
end

function QueueService:Start()
	Packets.Queue.Request.OnServerInvoke = onRequest
end
```

Notice three things the client handles: `ok == true`, `ok == false` with a message, and `ok == nil` when the server never answered.

## Rules for every server handler

The server must assume every argument is wrong, and every request is spam. From the real handlers:

| Check | Example from the code |
| --- | --- |
| **Types** | `if type(modeId) ~= "string" or #modeId > MAX_ID_LENGTH then return false, ... end` |
| **Finite vectors** | `ClassService`'s `finite(v)`: `v.X == v.X` (not NaN) and `v.Magnitude < 1e6` |
| **Unit directions** | `local length = look.Magnitude; if length < 0.5 or length > 1.5 then return false, "" end` |
| **Fresh timestamps** | `if math.abs(now() - timestamp) > MAX_CLOCK_DRIFT then return false, "" end` |
| **Rate limits** | `Helpers.TokenBucket.new(USES_PER_WINDOW, USE_WINDOW)` and `bucket:allow(player.UserId)` |
| **Use the server's position** | `ClassService.Use` uses the character's own head as the origin, not the client's camera position |

Never trust a client for anything that decides the game: team, class, damage, who was hit, whether they're alive.

## Unreliable packets

`Shared.UnreliablePackets` are for things that may be dropped without harm, sent often:

| Packet | Direction | Arguments |
| --- | --- | --- |
| `GunFired` | Server → nearby clients | UserId, gunId, origin, direction, seed, spread (other players' cosmetic tracers) |
| `GunAim` / `GunAimRelay` | Client → server / server → others | aim pitch (third-person arms) |

## Adding a packet: checklist

1. Add it to the right group in `Shared.Packets`, with a comment: direction, each argument, and who sends and receives it.
2. Use the narrowest types. A table (`Packet.Any`) only for snapshots.
3. On the server: validate everything, rate-limit, and for answered packets always return the declared values.
4. Add it to [All packets](../reference/packets.md).

A full worked example (packet, server handler, client call) is in [Networking: a new client request](../../EXAMPLES.md#networking-a-new-client-request).
