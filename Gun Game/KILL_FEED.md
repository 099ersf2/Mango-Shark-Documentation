# Kill feed

The top-right list of recent kills: `Killer  [Item]  Victim`, newest on top. It shows player and NPC kills by any weapon that passes an attacker to `Combat.ApplyHit`.

## Where things are

| What | Where |
| --- | --- |
| Server | `ServerScriptService.Modules.Systems.Combat.KillFeed` |
| Kill credit | `Systems.Combat.DamageLog` (filled by `Combat.ApplyHit`) |
| NPC deaths | `Systems.NPC.NPCService` calls `KillFeed.ReportDeath` when an NPC dies |
| Packet | `Shared.Packets.Combat.KillFeed` (`"CombatKillFeed"`: killer, victim, item; all strings) |
| Client | `ReplicatedStorage.Modules.Client.Combat.KillFeed` (`ClientOnly`) |
| UI | `StarterGui.Main.KillFeed` (a frame with a `UIListLayout` sorted by `LayoutOrder`) and its hidden `EntryTemplate` TextLabel |

## How it works

1. Every hit through `Combat.ApplyHit` with an `Attacker` records the attacker and `Item` in `DamageLog`.
2. When a player's humanoid dies (`KillFeed` hooks every character), or an NPC dies (`NPCService`), `KillFeed.ReportDeath` takes the last attacker from the past 10 seconds (`CREDIT_WINDOW`) and clears the log. Each humanoid is reported at most once.
3. If someone gets credit, the server sends the packet to everyone. Names are the player's `DisplayName` or the NPC model's name; the item is the `Item` given to `ApplyHit` (a gun's name, `"Nuke"`...), or `"Unknown"`.
4. The client clones `EntryTemplate` per kill. At most 5 rows show (`MAX_ENTRIES`), and each goes away after 6 seconds (`DISPLAY_SECONDS`). `Main` has `ResetOnSpawn` off, so the feed keeps going after your own death.

Deaths nobody gets credit for (a reset, falling off the map with no recent hit) aren't shown.

## Making a weapon show up

Pass `Attacker` and `Item` to `Combat.ApplyHit`:

```lua
Combat.ApplyHit(humanoid, damage, { Attacker = player, Item = "Rocket Launcher" })
```

Guns already do this through `AbilityRunner`. To restyle the rows, edit `Main.KillFeed.EntryTemplate` in Studio.

## Admin: nuke

`nuke <player>` (Cmdr, admins only) shows a "NUCLEAR STRIKE" banner, waits 5 seconds, then hits every humanoid within 180 studs of where the target stood: 500 damage at the center down to 125 at the edge, with knockback, credited to the caller as `"Nuke"`. It also damages breakables in the radius (`"Explosion"` source). The numbers are at the top of `CmdrSetup.Commands.NukeServer`.
