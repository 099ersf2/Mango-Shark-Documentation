# Handlers and helpers

Small shared modules that many systems lean on: player states, animations, rate limits, retries, loot rolls and UI formatting.

!!! abstract "Source"

    Both sides: `ReplicatedStorage.Modules.Handlers.*`, `Modules.Helpers.*`, `Modules.Shared.*`, `Modules.Classes.*`. Server only: `ServerScriptService.Modules.Helpers.*`.

---

## `Handlers.StateHandler`

Short-lived **player states** (`Reloading`, `Stunned`, `CantDoAnything`, `Sprinting`, …). Each state is also mirrored to a **Player attribute** of the same name, so clients and other systems can read it. Many systems refuse actions while `Stunned` or `CantDoAnything` is set.

```lua
local StateHandler = require(game.ReplicatedStorage.Modules.Handlers.StateHandler)
```

### `StateHandler.SetState(player, key, value, duration?)`

Sets a state and the matching attribute. With `duration` (seconds) it clears itself afterwards.

```lua
StateHandler.SetState(player, "CantDoAnything", true, 1.5) -- no abilities, throws or drones for 1.5 s
```

### `StateHandler.GetState(player, key) → any`

The state's value, or `nil`. This is how `ClassService.Use` checks if a player may act:

```lua title="Systems.Classes.ClassService.Use"
if StateHandler.GetState(player, "Stunned") or StateHandler.GetState(player, "CantDoAnything") then
	return false, ""
end
```

### `StateHandler.ReturnStates(player) → { [string]: any }?`

Every state the player has, or `nil` with none.

```lua
for key, value in StateHandler.ReturnStates(player) or {} do
	print(key, value)
end
```

### `StateHandler.RemoveStates(player, key?)`

Clears one state (and its attribute), or every state with no `key`. `GunService` uses it to end a reload:

```lua title="Systems.Guns.GunService (cancelReload)"
if StateHandler.GetState(state.Subject, "Reloading") then
	StateHandler.RemoveStates(state.Subject, "Reloading")
end
```

### `StateHandler.SetStun(playerOrModel, on, duration, stunSpeed?)`

Stuns a player or an NPC model: sets `Stunned`, drops `WalkSpeed` to `stunSpeed` (default 0) and restores it after `duration`. Overlapping stuns extend to the latest end time. `on = false` ends it now.

```lua
StateHandler.SetStun(player, true, 2, 4)  -- 2 seconds at walk speed 4
StateHandler.SetStun(npcModel, false)     -- end early
```

!!! note "`SetStun` doesn't set the attribute"

    Unlike `SetState`, `SetStun` only stores `Stunned` internally; it doesn't set the Player attribute. Server checks via `GetState(player, "Stunned")` still work.

### `StateHandler.ClearAllState()`

Removes every state from everyone. For tests and full resets.

```lua
StateHandler.ClearAllState()
```

---

## `Handlers.AnimationHandler`

Loads and plays animations on a character and tracks them by **type** (a group name you choose, like `"Gun"` or `"Emote"`) and **id**.

```lua
local AnimationHandler = require(game.ReplicatedStorage.Modules.Handlers.AnimationHandler)
```

!!! bug "Pass animation ids as strings"

    In `LoadAnim`, a **number** id is turned into a string but never assigned to the Animation, so the track plays nothing. Use `"rbxassetid://123"` or `"123"`. `RemoveAnim` has the same problem with number ids. Worth fixing in the module.

### `AnimationHandler.LoadAnim(character, type, animId, keyframeCallback?, keyframes?, looped?, fadeTime?)`

Loads and plays the animation. `keyframeCallback(name, track)` fires on each marker named in `keyframes`. A non-looped track is cleaned up after it ends.

```lua
AnimationHandler.LoadAnim(character, "Emote", "rbxassetid://1234567890", function(marker, track)
	if marker == "Hit" then print("hit frame") end
end, { "Hit" })
```

### `AnimationHandler.GetAnims(character, type?) → table`

The tracked animations of one type (`{ [animId] = { Track, Connections } }`), or every type.

```lua
for animId, entry in AnimationHandler.GetAnims(character, "Emote") do
	print(animId, entry.Track.IsPlaying)
end
```

### `AnimationHandler.IsAnim(character, type, animId) → boolean`

`true` while that animation is playing.

```lua
if not AnimationHandler.IsAnim(character, "Emote", WAVE_ID) then
	AnimationHandler.LoadAnim(character, "Emote", WAVE_ID)
end
```

### `AnimationHandler.StopAnim(character, type, animId)` / `RemoveAnim(character, type, animId)`

Stop a track / forget it. `StopAnim(character, "ALL")` stops everything (NPCs do this when they die).

```lua
AnimationHandler.StopAnim(character, "Emote", WAVE_ID)
```

### `AnimationHandler.PreloadAnimations(character, animList)`

Loads a list of animations ahead of time so the first play doesn't stall.

```lua
AnimationHandler.PreloadAnimations(character, { WAVE_ID, CHEER_ID })
```

### `AnimationHandler.PlayAnimationEveryone(character, type, animId, looped?, fadeTime?)` / `StopAnimationEveyone(...)`

Server → every client plays (or stops) it. Note the spelling of `StopAnimationEveyone`.

```lua
AnimationHandler.PlayAnimationEveryone(character, "Emote", "rbxassetid://1234567890")
```

---

## `Handlers.HitPopup` (client)

### `HitPopup.Show(targetModel, amount)`

A floating damage number over a character, from the `HitPopup` template in `StarterGui.Main`.

```lua
HitPopup.Show(victimCharacter, 38)
```

## `Classes.HealthUI` (client)

| Function | Does |
| --- | --- |
| `HealthUI.ConstructHealthBar(humanoid, bar, label)` | Wires a bar and label to a humanoid's health |
| `HealthUI.HealthChanged(humanoid, frame, lastDamaged, current, new)` | Animates one change |
| `HealthUI.ShieldChanged(humanoid, frame, label?)` | Shows the `Shield` attribute |

```lua
HealthUI.ConstructHealthBar(humanoid, frame.Bar, frame.Label)
```

`Client.Hud.HealthBillboards.SetupBillboard(humanoid)` puts a health billboard over any humanoid (NPCs get one automatically).

---

## `Helpers.TokenBucket` (server)

The game's rate limiter. Each user has a bucket of `capacity` tokens that refills smoothly over `windowSeconds`; each action takes one.

### `TokenBucket.new(capacity, windowSeconds) → bucket`

```lua title="Systems.Classes.ClassService"
local USES_PER_WINDOW = 4 -- Ability requests a player may send...
local USE_WINDOW = 2      -- ...in this many seconds
local bucket = TokenBucket.new(USES_PER_WINDOW, USE_WINDOW)
```

### `bucket:allow(userId) → boolean`

`false` when the user is over the limit.

```lua
if not bucket:allow(player.UserId) then
	return false, ""   -- spam: drop it silently
end
```

### `bucket:remove(userId)` / `TokenBucket.RemoveUserFromAllBuckets(userId)`

Forget a user (on leave) in one bucket / in every bucket.

```lua
Players.PlayerRemoving:Connect(function(player)
	bucket:remove(player.UserId)
end)
```

## `Helpers.Retry` (server)

### `Retry.Call(label, fn, attempts?) → (ok, ...)`

Calls `fn` in a `pcall` and retries with exponential backoff (doubling from `Content.Matchmaking.RETRY_BASE_DELAY`, capped at `RETRY_MAX_DELAY`, ×2 when throttled, with jitter). Default attempts: `RETRY_ATTEMPTS` (4). **Yields.** Warns once with `label` if every attempt fails.

```lua title="From the Retry header"
local ok, value = Retry.Call("Queue.Get", function() return map:GetAsync(key) end)
local ok = Retry.Call("Publish", publish, 2)   -- at most 2 attempts
```

Use it around every MemoryStore, MessagingService, DataStore and TeleportService call.

## `Helpers.SetCollisionGroup` (server)

### `SetCollisionGroup(model, groupName)`

Puts every BasePart in a model into a collision group. It's the module itself, a function.

```lua
local SetCollisionGroup = require(game.ServerScriptService.Modules.Helpers.SetCollisionGroup)
SetCollisionGroup(npcModel, "Player")
```

## `Helpers.Rarity` (server)

Weighted random picks over a loot table `{ [name] = weight }`.

| Function | Returns |
| --- | --- |
| `Rarity.CreateLootTable(list)` | A loot table from `{ { Name, Weight } }` (or keyed entries) |
| `Rarity.Roll(lootTable, luck?)` | One name. Higher `luck` (in hundreds) favours rarer entries |
| `Rarity.MultiRoll(lootTable, count, luck?)` | A list of names |
| `Rarity.PercentChance(lootTable, name)` / `FractionChance` | Display text like `" 25 % "` / `" 1 / 4 "` |

```lua
local loot = Rarity.CreateLootTable({ { Name = "Common", Weight = 75 }, { Name = "Rare", Weight = 25 } })
print(Rarity.Roll(loot), Rarity.PercentChance(loot, "Rare"))
```

`Roll` yields a frame per retry (it uses `task.wait()`), so don't call it inside a Scribe transaction.

## `Helpers.TableHelpers` / `Helpers.UIHelpers` (both sides)

### `TableHelpers.TableLength(t, useCache?) → number`

Counts every key, not just the array part.

```lua
print(TableHelpers.TableLength({ a = 1, b = 2, [3] = true })) -- 3
```

### `TableHelpers.CreateWatchedTable(initial?, onChanged) → proxy`

A proxy that calls `onChanged(key, old, new)` whenever a key changes.

```lua
local state = TableHelpers.CreateWatchedTable({ Ammo = 30 }, function(key, old, new)
	print(key, old, "->", new)
end)
state.Ammo = 29 -- prints: Ammo 30 -> 29
```

### `UIHelpers:ConvertToMMSS(seconds) → string` / `UIHelpers:GetPlayerThumbnailIcon(player) → string`

Timer text (`"05.3"` under a minute, else `"02:07"`) / a 420×420 headshot (yields). Note the colon call.

```lua
label.Text = UIHelpers:ConvertToMMSS(endsAt - workspace:GetServerTimeNow())
image.Image = UIHelpers:GetPlayerThumbnailIcon(player)
```

---

## `Shared.ReadOnly`

### `ReadOnly.Wrap(accessor, label) → view`

Scribe lets the client write its own mirror of the data. Wrap client views so a write **errors** instead of silently diverging from the server.

```lua title="From the ReadOnly header"
local view = ReadOnly.Wrap(Data.Client.Coins, "Coins")
view.Get()      -- fine
view.Set(5)     -- error: Coins is read-only on the client: Set was rejected
```

## `Shared.Smoke`

### `Smoke.Blocks(from, to) → boolean`

`true` if the line passes through the **core** (inner 75%) of any smoke cloud. Smoke only hides: bullets still pass.

```lua
if Smoke.Blocks(npcEye, targetHead) then
	return false -- can't see through smoke
end
```

`Smoke.TAG` (`"SmokeCloud"`) and `Smoke.RADIUS_ATTRIBUTE` (`"Radius"`) are exported.

## `Shared.CursorAim` (client)

### `CursorAim.Ray() → (origin, direction)`

The local aim ray: the screen centre when the mouse is locked or on touch/gamepad, else the cursor.

```lua
local origin, direction = CursorAim.Ray()
local hit = workspace:Raycast(origin, direction * 500, params)
```

## `Shared.ProductIds`

Every developer product and game pass id, by name. **Never type an id anywhere else.** `0` means "not created yet" and anything that sells it treats it as off.

```lua
local ProductIds = require(game.ReplicatedStorage.Modules.Shared.ProductIds)
local vip = ProductIds.GamePasses.VIP
local coins = ProductIds.Products.Store_Coins5000
```

Names: crates are `Crate_<crateId>`, store items `Store_<itemId>`, game passes keyed by the store item's Id.

## `Shared.StoreGrants`

Applies what a purchase gives to a player's data. Runs **inside Scribe transactions**, so nothing in it yields.

| Function | Does |
| --- | --- |
| `StoreGrants.Apply(data, grants)` | Coins, Tokens, Skins, Classes, Crates, BattlePass |
| `StoreGrants.ApplyItem(data, item)` | An item's grants; a once-only item is recorded in `OwnedItems` |
| `StoreGrants.ApplyLasting(data, grants)` | Only skins and classes (for owners when a bundle gets new ones) |
| `StoreGrants.Missing(data, grants)` | Whether the player lacks any of its skins or classes |
| `StoreGrants.AddCrate(data, crateId, n)` | Crates into the inventory |
| `StoreGrants.OpenCrate(data, crate)` | A random unowned skin, added and equipped (refund Coins if all owned); the skin Id or `nil` |
| `StoreGrants.GivePremium(data, season)` | The season's premium pass |

```lua
-- inside a transaction (no yields)
StoreGrants.AddCrate(data, "Glacier", 1)
```

## `Classes.Admins`

The one list of admin UserIds (`Admins.UserIds`). Cmdr's `BeforeRun` hook checks it for every command.

```lua
local Admins = require(game.ReplicatedStorage.Modules.Classes.Admins)
local isAdmin = table.find(Admins.UserIds, player.UserId) ~= nil
```

## Gadget math (`Shared.CameraRig`, `DroneStep`, `BallisticShield`)

| Function | Does |
| --- | --- |
| `CameraRig.Frame(model, yaw, pitch) → (viewCFrame, orbit)` / `Apply(model, yaw, pitch)` | Where a security camera looks, and turning its lens |
| `DroneStep.Lift(root, direction, travel, params, maxHeight, clearance) → number?` | How far to lift a drone over a small step, or `nil` |
| `BallisticShield.Pose(prone, crouched, aiming) → (pose, offset)` / `CanFire(prone, aiming)` / `ViewOffset(pose)` / `ClearGround(frame, groundY, clearance?)` | The Shield class's carry rules, shared by server and client |

```lua
local pose, offset = BallisticShield.Pose(false, true, false) -- "Crouch", CFrame
```
