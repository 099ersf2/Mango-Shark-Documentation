# Design decisions

The answers to open design questions, so the code and the docs follow the same rules. Newest first. Each entry says what was decided and where it lives in the place.

## 2026-11-11

### Matches and teams

| Question | Decision |
| --- | --- |
| How are rounds built? | **A modular match system** (`Systems.Match.MatchService`): each mode is one module in `Content.Match.Modes`. It replaced the fixed Red vs Blue rounds below. Team Deathmatch, Free-for-All and Elimination ship |
| Who adjusts a match? | **Admins** (`Classes.Admins`), from the Match menu (M) or Cmdr. Changes apply to the next match, or at once with Restart |
| Roblox Teams or our own? | **Our own** (`Systems.Match.TeamService`, `Content.Match.Teams`): the player attribute `Team`. Up to 4 teams |
| Friendly fire | **Off by default**, a per-match setting (`FriendlyFire`) |
| Scoreboard key | **Tab**, replacing Roblox's player list |

## 2026-11-10

### Team deathmatch rounds

| Question | Decision |
| --- | --- |
| Round mode and length | **Red vs. Blue team deathmatch, three minutes per round.** The team with the most credited player kills wins; a tie is a draw. |
| Who is assigned to teams? | Arena players are split as evenly as possible. Players in the lobby are not assigned. |
| What does the match leaderboard show? | The ten players with the highest round kill counts, including profile thumbnails. |
| What happens after a player is killed? | Show a death screen and spectate the credited killer until the victim respawns. |
| Does friendly fire count? | No. The server blocks teammate damage during active rounds; self-damage is unchanged. |
| Do damaged boards and walls reset between rounds? | Not currently. Round start does not reset breakables or soft walls. |

## 2026-11-09

### Lobby and skins

| Question | Decision |
| --- | --- |
| Do respawns go back to the lobby? | **No.** Only a player's first spawn of a session is in the lobby; later respawns are in the arena (`Systems.Lobby.LobbyService`). |
| Is the lobby a safe zone? | **No.** `nuke` and other damage can hit players in the lobby. |
| Does the skin shop have a key? | **No key.** The shop has a **physical location in the lobby**: walk up to the shop stand and use its prompt (the Interact key) to open it. The old I key is removed. |
| Crate price | **499 Robux** per crate, sold as a developer product. Its id is in `Shared.ProductIds` (`Products.SkinCrate`). Product id `3730208338`. |
| Buying a crate when you already own every skin | **Coins back** instead of a skin: 500 coins (`Skins.CRATE_REFUND_COINS`). Claude picked the amount; change it there. |
| Where product ids live | **`Shared.ProductIds`**: one module holds every developer product and game pass id. |
| Is Inspect rebindable? | **Yes**, in Settings > Controls (default V). |

### Movement

| Question | Decision |
| --- | --- |
| Default crouch and prone keys | **Crouch = Left Ctrl, prone = C** (swapped from C / Left Ctrl). Saved keys still on the old defaults move to the new ones on join. |

### Guns

| Question | Decision |
| --- | --- |
| Shotgun kick | **Too much.** Lowered. |
| SMG bloom never recovers, and its damage falls to 0 at 80 studs | **Intended.** Kept. |
| Revolver | **Make it a gun**: a Handle, attachments, a definition and effects. |
| Knife `CanQuery` | **Stays on.** |
| Recoil recovery (the aim easing back down after a spray) | **Off for now.** The recovery code stays and is switched on with one config value; the player controls the aim after a spray. |

### Gun bash (melee)

| Question | Decision |
| --- | --- |
| Does a bash cancel a reload? | **Yes.** Bashing mid-reload cancels the reload and bashes. |
| Damage and cooldown | **45 damage, 0.9 s cooldown** are right. |
| Does a bash wait for SprintOutTime after a sprint? | **No.** It bashes at once. |
| Animation | The old jab looked bad. **Replaced** with a new bash animation. On 2026-11-10 the wide sideways swing that replaced it also looked bad (it swung the gun across the middle of the screen), so it became a **long straight jab** with about 1.6 studs of forward travel. **No camera shake.** |

### Soft walls and boards

| Question | Decision |
| --- | --- |
| Per-gun hole sizes | **Yes.** Each gun's `HoleRadius` in `SoftWallConfig.Guns` applies. |
| Explosive BurstRifle rounds and soft walls | **They stop at soft walls** (`Penetrates = false`), so one round can't explode twice. |
| Hole shape | **Square** (fast), turned at a random angle. |
| Debris | **Visible.** Pieces knocked out of a soft wall and planks broken off a board fall as debris you can see, then clean up after a few seconds. |
| Door board prompt text | **"Door board".** |
| Walls reset at round start? | Not decided yet (no round system exists). |

### Studio

| Question | Decision |
| --- | --- |
| Other people in live editing (robloxoppen, Matteo_the7best) | **Expected.** They're developers on the place. |
