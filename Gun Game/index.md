# Gun Game documentation

Documentation for the Roblox FPS place **Gun Game**. Use the sidebar to browse by topic, or search across every guide.

## Start here

- **New to the project or changing code?** Read the [AI coding guide](AI_CODING_GUIDE.md) first.
- **Looking for a function, packet, command, or data field?** Start with the [API reference](API.md).
- **Learning the current game flow?** Read [Siege](SIEGE.md), then [matchmaking and parties](MATCHMAKING.md).
- **Checking what remains to be done?** See [next steps](NEXT_STEPS.md).

## Game flow and player experience

| Guide | Covers |
| --- | --- |
| [Siege](SIEGE.md) | The current game mode, objectives, rounds, and player roles |
| [Matchmaking and parties](MATCHMAKING.md) | Queues, parties, reserved servers, and match formation |
| [Recruit Training](TUTORIAL.md) | The guided attack-and-defend tutorial |
| [Lobby](LOBBY.md) | Lobby flow and player entry points |
| [UI](UI.md) | Interface structure, layout, and interaction patterns |
| [Movement and camera](MOVEMENT.md) | Player movement, camera behavior, and tuning |
| [Music](MUSIC.md) | Music playback and transitions |
| [Death screen and spectating](DEATH_SCREEN.md) | Death camera and spectating behavior |
| [Kill feed](KILL_FEED.md) | Kill feed entries and weapon names |

## Combat and gameplay systems

| Guide | Covers |
| --- | --- |
| [Gun system](GUN_SYSTEM.md) | Gun-system architecture and shot flow |
| [Adding guns](ADDING_GUNS.md) | Gun definitions, abilities, recoil, and checks |
| [Third-person gun animation](THIRD_PERSON_GUNS.md) | Weapon poses, attachments, and animation |
| [Gun animation range](GUN_SHOWCASE.md) | The in-game weapon preview range |
| [Aim assist](AIM_ASSIST.md) | Controller and touch aim assist |
| [Classes](CLASSES.md) | Siege classes, loadouts, and abilities |
| [Scout drones](DRONES.md) | Drone controls and game-mode integration |
| [Breakables](BREAKABLES.md) | Boards and other destructible objects |
| [Soft walls](SOFTWALLS.md) | Penetrable walls and weapon damage |
| [Consumables](CONSUMABLES.md) | Grenades and smoke bombs |
| [Adding NPCs](ADDING_NPCS.md) | NPC setup, behavior, and extension points |
| [Siege bots](SIEGE_BOTS.md) | Bot roles and behavior in Siege |
| [Clear House](CLEAR_HOUSE.md) | The arcade house-clearing mode |

## Progression and economy

| Guide | Covers |
| --- | --- |
| [Progression and retention](PROGRESSION.md) | Levels, goals, streaks, and career stats |
| [Battle pass and quests](BATTLE_PASS.md) | Seasonal progression and rewards |
| [Store, currencies, crates, and stats](STORE.md) | Purchases, currencies, crates, and player stats |
| [Weapon skins](SKINS.md) | Skin assets, ownership, and presentation |
| [Analytics](ANALYTICS.md) | Gameplay analytics and recorded events |

## Engineering and project reference

| Guide | Covers |
| --- | --- |
| [API reference](API.md) | Public functions, packets, commands, tags, and data |
| [AI coding guide](AI_CODING_GUIDE.md) | Project architecture, implementation rules, and testing |
| [Claude project context](CLAUDE.md) | Condensed project-specific instructions for Claude |
| [Performance](PERFORMANCE.md) | Performance measurements and optimizations |
| [Security](SECURITY.md) | Server validation and security review notes |
| [Design decisions](DECISIONS.md) | Recorded decisions that guide implementation |
| [Changelog](CHANGELOG.md) | Chronological feature and change history |
| [Next steps](NEXT_STEPS.md) | Follow-up work and items awaiting verification |

## Historical references

These pages describe systems that have been replaced or are no longer the current game flow. Use them for context, not as implementation guidance.

- [Matches, modes, and teams](MATCH.md) — older modular match-system documentation; Siege is now the active mode.
- [Team deathmatch rounds](ROUND_SYSTEM.md) — replaced by the current Siege flow.

Treat the system guide and [API reference](API.md) as the primary technical references. The [changelog](CHANGELOG.md) records history and may describe behavior that has since changed. Check each guide's testing notes before relying on an unverified feature.
