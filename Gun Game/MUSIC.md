# Music

One song plays at a time, and every change is a crossfade: the old song's volume slides to 0 while the new one rises from 0 to its own volume. The client does it all (`Client.Core.Music`); the numbers are in `Content.Music`.

> **Not run yet.** Written on 2026-11-12 with no playtest (by request). Both scripts compile and every folder was found with songs in it; nobody has heard a transition.

## When the music changes

| Moment | Folder in `ReplicatedStorage.Assets.Music` | When | Fade |
| --- | --- | --- | --- |
| Background | `Primary` | Whenever nothing else is playing, one song after another (the lobby, and most of a match) | 1.5 s |
| Start | `Start` | Once, when a Siege match begins (the first phase after the lobby, so the selection screen). When the song ends the background songs carry on | 2 s |
| Panic | `Panic` | Once, when the Action phase has 30 seconds left (`PANIC_TIME`) | 4 s |
| End | `End` | Once, when the match ends (the End phase). It plays to its end, also back in the lobby; then the background songs carry on | 2 s |

- **Map music (2026-11-13):** while a Siege match is on (`ActiveSiegeMap` on Workspace, phase not Idle), a folder named like that map in `Assets.Music`, or in `Assets.Music.Primary`, replaces the background songs, if it holds any Sounds.
- **The panic song** can play again in each round of a multi-round match.
- **A song is picked at random** from its folder, never the same one twice running.
- **Volume:** a song fades up to the `Volume` set on its Sound in the folder (0.5 on the panic songs), so a loud song is turned down there.
- **A round that ends early** (both defusers planted, a team gone) skips the panic song and goes straight to the end song.
- **After the panic song** (they are 29 to 30 s long) nothing else starts while the round is still on.
- **An empty or missing folder** means that moment keeps the music it had.
- **The Music volume slider** applies: every song is in the `Music` sound group.

## Adding or changing songs

Put a Sound in the folder for its moment and set its `Volume`. Nothing else. For a map's own background songs, make a folder named exactly like the map (as in `ReplicatedStorage.Maps`) in `Assets.Music` and put its Sounds there. To change the 30 seconds, the fades or the folder names, edit `Content.Music`.

The folders `Alpha` and `Folder` in `Assets.Music` are not used by anything.

## How it knows the match

`Packets.Siege.State` carries `Phase` and `EndsAt` (server time). The module only listens, and looks at the clock four times a second. The server sends nothing for music.

## API

```lua
local Music = require(ReplicatedStorage.Modules.Client.Core.Music)
Music.Play("Panic")   -- crossfade to a random song of a kind: "Background", "Start", "Panic", "End"; false if it has none
Music.CurrentSong     -- the Sound playing now (a clone in SoundService), or nil between songs
Music.Playlist        -- the folder background songs come from
```

## Changed from the old module

The old `Client.Core.Music` played only `Primary` songs through the `Music` effect, which gave no way to change a playing song's volume. It is kept in `ServerStorage.Archive.OldMusic`. The `Music` entry in `Content.Effects.Registry` is no longer used.
