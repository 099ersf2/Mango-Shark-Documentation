# CLAUDE.md: Gun Game (Roblox place "FPS")

Context for Claude working on this project. Read it before doing anything. For the full coding rules read
`docs/AI_CODING_GUIDE.md`, and for the system you touch, its doc in `docs/` (index: `GUN_GAME.md`).

## The project

- **What it is:** a Roblox FPS game. The place is "FPS": placeId `80699390327837`, universe `10775243847`.
- **How you work on it:** in Roblox Studio, through the Studio tools (execute Luau, multi-edit, playtests, screenshots). There is no local source tree; the code lives in the place.
- **Docs:** pushed to the GitHub repo `099ersf2/Mango-Shark-Documentation`: the `Gun Game/` folder, plus `Gun Game Documentation.MD` as its home page.
- **Other contributors:** other developers and other AI agents work on the place and on the docs repo at the same time. Keep what they built, and merge with their doc changes rather than overwriting them.

## Hard rules

1. **Loading:** everything loads through `ReplicatedStorage.ModuleLoader` (Init, then Start). Never add a Script or LocalScript; new code is a ModuleScript in a loaded container. Client modules get the `ClientOnly` attribute.
2. **Code style:** `--!strict`, a `--[[ ]]` header (path, purpose, usage, extension points), typed functions, `UPPER_CASE` constants at the top, and doc blocks on public functions. Match the existing code.
3. **UI:** never build UI in scripts. Build it in Studio (Edit mode, by hand or with execute Luau) under `StarterGui.Main`, or as templates in `Assets.UI.Templates`. `Main` uses Global ZIndex, and anything drawn on a menu needs a ZIndex of 12 or higher.
4. **Trust:** the server decides. Clients send intent only, and the server validates every request.
5. **Networking:** only through `Shared.Packets` / `Shared.UnreliablePackets`. No RemoteEvents.
6. **Tuning numbers** live in `ReplicatedStorage.Content`.
7. **Inputs:** every feature works on keyboard and mouse, gamepad and touch.
8. **Off limits:**
   - sword combat;
   - `ModuleLoader`, the `Start` scripts, `Packages/` and `Utilities/`;
   - systems archived in `ServerStorage.Archive`.
9. **Publishing:** never publish without the user asking. To publish, run `publish-studio.ps1` (it sends Alt+P to Studio).
10. **Docs, every change:**
    - write the system doc, plus `API.md`, `CHANGELOG.md` and `NEXT_STEPS.md`;
    - push them to the docs repo: `git pull`, diff against the repo copy, merge, then copy and commit;
    - check `git show --stat HEAD` for deletions you didn't mean.
11. **Privacy:** treat the user's personal details as private.

## How the user wants you to work

- **Do the work inline.** Don't spawn sub-agents; the user said they use too much of their plan.
- **Verify with numbers in a playtest** and report plainly what you checked and what you didn't. Don't claim something works without having checked it.
- **The user often plays in the running playtest.** Ask before stopping it. Never take desktop screenshots, since they capture the user's whole screen; use Studio's `screen_capture`.
- **When the user says "no playtest, just doc",** do exactly that.
- **Reply format:** short sections, tables for comparisons, and a clear list of anything left to do or decide.

## Map of the code

| Area | Where |
| --- | --- |
| Server systems | `ServerScriptService.Modules.Systems.*`: Guns, Combat (KillFeed, DeathCamService, DamageLog), NPC (NPCService, Brain, Tactics, Tasks), Match (MatchService, TeamService), Drones, Showcase, Breakables, Destruction, Lobby, Consumables, Movement, Effects |
| Client | `ReplicatedStorage.Modules.Client.*`: Guns (GunController, Viewmodel, ThirdPersonGuns, GunEffects, AimAssist), Gadgets (DroneController), Hud (MatchHud, DeathScreen), Core (Menus, MatchMenu), Movement, Settings |
| Shared | `ReplicatedStorage.Modules.Shared.*`: Packets, Extensions (Any, Product, Fire, Add), PlayerSettings (keybind actions), Data (Scribe) |
| Content | `ReplicatedStorage.Content.*`: Guns (Definitions, Registry, Skins), NPC (Profiles), Match (Modes, Settings, Teams), Drones, Effects.Registry, Movement.Config |
| Admin commands | Cmdr: `ServerScriptService.Modules.Services.CmdrSetup.Commands` (a `Name` + `NameServer` pair). Admins are listed in `Classes.Admins` |

## Key facts you'll need

- **Damage:** goes through `Combat.ApplyHit(humanoid, dmg, { Attacker, Item })`, which checks `Combat.PreventFriendlyFire` first. Every death fires `Combat.Death`.
- **Teams:** our own system: the player's `Team` attribute (`TeamService`), not Roblox Teams.
- **NPCs:**
  - They live in `workspace.Enemies` and are tagged `NPC`. `NPCService.MAX_NPCS` should be 10; it was found at 0 on 2026-11-11.
  - Room guards: `NPCService.SetMode(npc, "Guard", room)` with a part tagged `NPCRoom`.
  - Joints are AnimationConstraint (kinematic). Write `.Transform` in PreSimulation, and handle Motor6D too.
- **Guns in third person** are posed in code (`ThirdPersonGuns`). A gun model's Handle needs `Muzzle`, `Aim`, `RightGrip` and `LeftGrip` attachments. The third-person tool is scaled to fit (`ModelScale`). Check guns on the gun range with the `range` command.
- **Camera render priority:** MovementCamera Camera+1, Viewmodel +2, drone camera +3, death camera +4.
- **Lobby:** the first spawn is in the lobby (`InLobby`), where most actions are refused. In tests, use `LobbyService.SendToArena`.

## Testing in Studio

- **Live modules:** command-bar and execute-Luau code gets its own copy of every module. To reach the live ones, use a temporary Script in ServerScriptService, or a LocalScript in PlayerGui, and delete it after.
- **Long tests:** have the temporary script log to a `workspace` attribute, return at once, and read the attribute in short calls. Long tool calls time out and can drop the Studio connection.
- **Before testing:**
  - close the Loadout menu (`Menus.Close`);
  - leave the lobby;
  - give the test player high health (NPCs shoot it).
- **Screenshots:** they use the play client's camera. Pin it from a temporary LocalScript at `RenderPriority.Last + 50`, then always restore it.
- **Studio's key-press tool** doesn't reach the game. Call the module's functions instead.
