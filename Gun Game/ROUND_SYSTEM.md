# Team deathmatch rounds (replaced)

The fixed Red vs Blue round system (`Systems.Round.RoundService`, `Content.Round`, `Client.Hud.RoundHud`) was replaced on 2026-11-11 by the modular match system: see [MATCH.md](MATCH.md).

What it did now lives there: Team Deathmatch is a mode (`Content.Match.Modes.TeamDeathmatch`), teams are our own (`Systems.Match.TeamService`, the `Team` player attribute instead of `RoundTeam`), friendly fire is a match setting, and the HUD, scoreboard and death screen are `Client.Hud.MatchHud`. `Packets.Round` became `Packets.Match`.
