# Effects and sound

The server never creates visuals or sounds itself. It sends an effect **name** and options, and each client builds the effect from `Content.Effects.Registry`. This keeps the server cheap and every effect in one place.

!!! abstract "Source"

    Server: `Systems.Effects.EffectService`. Client: `Client.Effects` (and `Client.Effects.Context`). Data: `Content.Effects.Registry`, `Content.Effects.Parts.*`.

## Playing an effect

```lua title="From the EffectService header"
EffectService.Play("Hit", { Target = character })
EffectService.Play("Hit", { Position = position })
EffectService.Play("Hit", { Target = character, Tool = sword, Variant = combo, Speed = 1.5 })
EffectService.Stop("Hit", character)
EffectService.Play("GunFire_Rifle", { Parent = muzzle }, shooter) -- everyone but the shooter, who played it already
```

| Function | What it does |
| --- | --- |
| `EffectService.Play(name, options?, except?)` | Sends the effect to the clients its `Replicate` setting names, skipping `except` |
| `EffectService.Stop(name, target?, data?)` | Stops a held effect on every client (`data` like `{ Instant = true }` is passed to its parts) |
| `Client.Effects.Play(name, options?)` / `Stop(...)` | Plays an effect **only on this client** |

## Who receives it

Each registry entry's `Replicate` decides:

| `Replicate` | Sent to |
| --- | --- |
| `All` (default) | Every loaded client |
| `Nearby` | Clients whose character is within the entry's `Range` (default 200 studs) of the effect's position |
| `Local` | Never sent. Only a client may play it; the server warns if it tries |

From the code, the position for `Nearby` comes from `Position`, then `CFrame`, then `Parent`/`Target` (a model's pivot, a part's position or an attachment's world position). Effects are only sent to clients whose modules have loaded (the `_ModulesLoaded` attribute), since an early packet can't be read.

Options must be plain values (instances, numbers, strings, vectors, CFrames, colors, tables of them). Callbacks are not sent.

## Pattern: predict locally, skip yourself on the server

For your own shot, the client plays the muzzle flash at once, then the server sends it to **everyone else** by passing the shooter as `except`. You see no delay and nobody sees it twice.

```lua
-- Client (the shooter): instant feedback
Effects.Play("GunFire_Rifle", { Parent = muzzle })
-- Server: everyone but the shooter
EffectService.Play("GunFire_Rifle", { Parent = muzzle }, shooter)
```

Real abilities use the same rule. `Flashbang` plays the throw sound for others and the pop for everyone:

```lua title="Systems.Classes.Abilities.Flashbang"
EffectService.Play("ConsumableThrow", { Target = context.Character }, context.Player)
-- ...after the fuse:
EffectService.Play("Flashbang", { Position = position })
```

## Effect parts

A registry entry is built from parts in `Content.Effects.Parts`, each with `Play(spec, context)`: `Animation`, `Banner`, `ColorFade`, `Debris`, `Dust`, `Highlight`, `Impact`, `JointSwing`, `MuzzleFlash`, `Particles`, `PooledSound`, `Shards`, `Shell`, `Sound`, `Template`.

Inside a part, `context` offers `Add(instance, lifetime?)`, `Delay(seconds, fn)`, `Hold()`, `Keep(seconds)`, `OnStop(fn)`, `Anchor()`, `Group()`, `Stop(data?)` and `context.Data`.

## Other client feedback

| Function | What it does |
| --- | --- |
| `Client.Movement.MovementCamera.Shake(magnitude, roughness, fadeIn, fadeOut)` | Camera shake |
| `Client.Guns.GunEffects.Play(name, options?)` / `LocalShot(ctx, directions, muzzle?)` | Gun effects; your own shot's tracers and flash |
| `Client.Guns.Quality.Scale()` / `Count(n)` | The effect quality factor; a particle count scaled by it |
| `Client.Audio.AudioSettings.Get(group)` / `GetAll()` / `Set(group, volume)` | Volumes |
| `Client.Audio.SoundGroups.Get(name?)` / `Assign(sound, name?)` / `Master()` | Sound groups |
| `Client.Core.UIFeel.Play(kind)` | UI sounds: `Hover`, `Press`, `Open`, `Close`, `Confirm`, `Error`, `Tick`, `Notify` |

More: [Effects and camera shake](../../EXAMPLES.md#client-settings-menus-and-feedback).
