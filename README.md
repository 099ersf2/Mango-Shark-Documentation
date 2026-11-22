# Gun Game documentation

Documentation for the Roblox FPS place **Gun Game**. Use this page as the index; each link opens a focused guide.

## Start here

- **New to the project or changing code?** Read the [AI coding guide](Gun%20Game/AI_CODING_GUIDE.md) first.
- **Looking for a public function, packet, command, or data field?** Start with the [API reference](Gun%20Game/API.md).
- **Learning the current game flow?** Read [Siege](Gun%20Game/SIEGE.md), then [matchmaking and parties](Gun%20Game/MATCHMAKING.md).
- **Checking what remains to be done?** See [next steps](Gun%20Game/NEXT_STEPS.md).

## Browse by topic

### Game flow and player experience

| Guide | Covers |
| --- | --- |
| [Siege](Gun%20Game/SIEGE.md) | The current game mode, objectives, rounds, and player roles |
| [Matchmaking and parties](Gun%20Game/MATCHMAKING.md) | Queues, parties, reserved servers, and match formation |
| [Recruit Training](Gun%20Game/TUTORIAL.md) | The guided attack-and-defend tutorial |
| [Lobby](Gun%20Game/LOBBY.md) | Lobby flow and player entry points |
| [UI](Gun%20Game/UI.md) | Interface structure, layout, and interaction patterns |
| [Movement and camera](Gun%20Game/MOVEMENT.md) | Player movement, camera behavior, and tuning |
| [Music](Gun%20Game/MUSIC.md) | Music playback and transitions |
| [Death screen and spectating](Gun%20Game/DEATH_SCREEN.md) | Death camera and spectating behavior |
| [Kill feed](Gun%20Game/KILL_FEED.md) | Kill feed entries and weapon names |

### Combat and gameplay systems

| Guide | Covers |
| --- | --- |
| [Gun system](Gun%20Game/GUN_SYSTEM.md) | Gun-system architecture and shot flow |
| [Adding guns](Gun%20Game/ADDING_GUNS.md) | Gun definitions, abilities, recoil, and checks |
| [Third-person gun animation](Gun%20Game/THIRD_PERSON_GUNS.md) | Weapon poses, attachments, and animation |
| [Gun animation range](Gun%20Game/GUN_SHOWCASE.md) | The in-game weapon preview range |
| [Aim assist](Gun%20Game/AIM_ASSIST.md) | Controller and touch aim assist |
| [Classes](Gun%20Game/CLASSES.md) | Siege classes, loadouts, and abilities |
| [Scout drones](Gun%20Game/DRONES.md) | Drone controls and game-mode integration |
| [Breakables](Gun%20Game/BREAKABLES.md) | Boards and other destructible objects |
| [Soft walls](Gun%20Game/SOFTWALLS.md) | Penetrable walls and weapon damage |
| [Consumables](Gun%20Game/CONSUMABLES.md) | Grenades and smoke bombs |
| [Adding NPCs](Gun%20Game/ADDING_NPCS.md) | NPC setup, behavior, and extension points |
| [Siege bots](Gun%20Game/SIEGE_BOTS.md) | Bot roles and behavior in Siege |
| [Clear House](Gun%20Game/CLEAR_HOUSE.md) | The arcade house-clearing mode |

### Progression and economy

| Guide | Covers |
| --- | --- |
| [Progression and retention](Gun%20Game/PROGRESSION.md) | Levels, goals, streaks, and career stats |
| [Battle pass and quests](Gun%20Game/BATTLE_PASS.md) | Seasonal progression and rewards |
| [Store, currencies, crates, and stats](Gun%20Game/STORE.md) | Purchases, currencies, crates, and player stats |
| [Weapon skins](Gun%20Game/SKINS.md) | Skin assets, ownership, and presentation |
| [Analytics](Gun%20Game/ANALYTICS.md) | Gameplay analytics and recorded events |

### Engineering and project reference

| Guide | Covers |
| --- | --- |
| [API reference](Gun%20Game/API.md) | Public functions, packets, commands, tags, and data |
| [AI coding guide](Gun%20Game/AI_CODING_GUIDE.md) | Project architecture, implementation rules, and testing |
| [Claude project context](Gun%20Game/CLAUDE.md) | Condensed project-specific instructions for Claude |
| [Performance](Gun%20Game/PERFORMANCE.md) | Performance measurements and optimizations |
| [Security](Gun%20Game/SECURITY.md) | Server validation and security review notes |
| [Design decisions](Gun%20Game/DECISIONS.md) | Recorded decisions that guide implementation |
| [Changelog](Gun%20Game/CHANGELOG.md) | Chronological feature and change history |
| [Next steps](Gun%20Game/NEXT_STEPS.md) | Follow-up work and items awaiting verification |

### Historical references

These pages describe systems that have been replaced or are no longer the current game flow. Use them for context, not as implementation guidance.

- [Matches, modes, and teams](Gun%20Game/MATCH.md) — older modular match-system documentation; Siege is now the active mode.
- [Team deathmatch rounds](Gun%20Game/ROUND_SYSTEM.md) — replaced by the current Siege flow.

## Keeping the docs useful

Treat the system guide and [API reference](Gun%20Game/API.md) as the primary technical references. The [changelog](Gun%20Game/CHANGELOG.md) records history; it may describe behavior that has since changed. Check each guide's testing notes before relying on an unverified feature.
