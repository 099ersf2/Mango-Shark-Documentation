# Performance pass (2026-11-18)

The owner asked for the code to be optimized across the game. Rather than rewrite by guesswork, every change below came from Roblox's script profiler (`ScriptProfilerService`), run in Studio playtests in the lobby and in a 5v5 Siege match with 9 bots, before and after.

## How to profile (for next time)

- **Client:** from the Client datamodel (the command bar or execute_luau), connect `ScriptProfilerService.OnNewData`, call `ClientStart(LocalPlayer, 1000)`, wait, `ClientRequestData(LocalPlayer)`, then `ClientStop(LocalPlayer)`. A LocalScript can't listen (it lacks the Plugin capability).
- **Server:** from the Server datamodel, connect `OnNewData`, then `ServerStart(1000)`, wait, `ServerRequestData(player)`, `ServerStop()`.
- **Reading it:** `DeserializeJSON` gives `Categories` (root `NodeId`s), `Nodes` (`Duration` is self time, `Children` maps function id to node id) and `Functions` (`Source`, `Line`, `Name`). Durations are in seconds (checked against a script that busy-waits 2 ms a frame). Engine calls show as `[C]`; add their time to the Lua function that called them to see who pays.

## What it found

The server is lean: with 9 bots fighting, the game's own server scripts take about 0.3 ms of a 16.7 ms frame (SiegeService's discovery check, the bots' brains, drones). Nothing there was worth changing. The cost was on the client and in what every client is sent.

| Where | Problem | Fix | Before | After |
| --- | --- | --- | --- | --- |
| `Teams.GunShowcase` | The gun range (72 rigs, 20,807 instances) had been parked in Teams, which replicates. Every player downloaded it on join, and its 72 rig scripts (RunContext Client) ran on every client. Nothing used it: the range system and the `range` command only look in Workspace | Moved, unchanged, to `ServerStorage.GunShowcase` (not replicated, scripts don't run). To use the range again, move it into Workspace (GUN_SHOWCASE.md) | 63% of all replicated instances | 0 |
| `Client.Guns.SkinRainbow` | Recoloured every rainbow-skin part every frame: 154 to 266 parts, most in backpacks and hidden menu previews, plus the held gun's hidden third-person copy | Only parts that can be seen: in the world within 250 studs and not hidden (`Transparency`, `LocalTransparencyModifier`), or in a ViewportFrame whose GUI shows; worked out every 0.25 s. Colours change 30 times a second (the hue turns a quarter a second) | 0.33 ms/frame | 0.10 ms in a match, about 0.02 in the lobby |
| `Client.Guns.ThirdPersonGuns` | One pose asks for the same arm joints' offsets about ten times; each read crossed into the engine (`IsA`, `Attachment0/1`, `CFrame`) | Offsets cached for the frame (cleared at the start of `onStep`). A joint that lost an attachment (a body being taken apart) no longer errors every frame | 0.39 ms/frame (17 rigs) | 0.27 |
| `Client.Interact.ReinforcePrompt` | The board search (a raycast and a pass over every board) ran every frame for a defender with the reinforce class | Search 10 times a second; giving up the prompt is still checked every frame | 0.16 ms/frame | under 0.01 |
| `Client.Gadgets.LeoMotionWarning` | Every frame it set the timer text, the panel and all 72 ring segments, shown or not, for everyone | Nothing runs unless the player is a defender in a match or the warning shows; segments only change when the number lit changes | 0.03 to 0.05 ms/frame | 0 when hidden |
| `Client.Hud.SiegeTopBar` | Formatted and wrote the clock every frame | Writes only when the second, the colour or the number of feed bars changes | 0.04 ms/frame | 0 between seconds |

Totals for the client's own scripts (Roblox's core scripts included, Studio plugins left out):

- **Lobby:** 0.78 ms per frame before, 0.35 after. The client holds about 25,000 fewer instances (98k to 73k in Studio, which counts Studio's own too).
- **Match:** 1.37 ms per frame before, 1.00 after. The rest is spread thin: arm posing, the viewmodel, aim assist, Roblox's camera and chat.

## Not changed

- **Sword combat** (a standing rule).
- **The bots' scripts:** each bot's `Animate`-style script shows up at about 0.05 ms; the NPC template is the other developer's.
- **Anything under about 0.02 ms a frame.**

## Checked

- Rainbow skins still turn on the first-person gun; the hidden third-person copy is skipped.
- The reinforce prompt appears at once when you look at a board, stays while you aim, and goes when the ability can't be used.
- No errors in a full Siege round, other than the arm-joint error, which is now handled.
- **Not checked by hand:** the Inventory and Store previews of rainbow skins (they should turn while their menu is open), and the Leo warning in a real scan. **Not published.**
