# Next steps

This list tracks verification not available in the solo Studio session.

- [ ] Run a two-player test and verify balanced team assignment and team spawn sides.
- [ ] Credit an enemy-player kill and verify the player's kill count, team total, and winner.
- [ ] Verify a victim spectates the credited killer until respawn, including when that killer leaves or respawns first.
- [ ] Verify no-killer deaths show the death screen and do not award a kill.
- [ ] Verify teammate damage is blocked and enemy damage still works during an active round.
- [ ] Check the match HUD, avatar thumbnails, and death screen on a phone-sized viewport.

## Scout drones (2026-11-11)
- [ ] Drive a drone with real keys: does it feel fast and smooth? Tune `SPEED`, `ACCELERATION`, `BRAKING`, `HOP_SPEED` in `Content.Drones`.
- [ ] Spot a real enemy and check your teammate sees the mark; check teammates can't shoot your drone.
- [ ] Try gamepad (DPad Left / Down, sticks) and touch (DRONE, CAMS and the in-drone buttons) on a phone.
- [ ] Replace the placeholder motor sound (`Assets.Models.Gadgets.Drone.HumanoidRootPart.Motor`).
- [ ] Watch NPCs react to a drone driving past (hearing) and shoot it.


## Pistol shoot animation (2026-11-11)
- [ ] Publish `RBX_ANIMSAVES.Rig2."Pistol Shoot"` from the Animation Editor to get an animation ID, then hook it to the NPC or gun that should use it.


## Third-person gun animation (2026-11-11)
- [ ] Watch another player in a two-player test: aim pitch, aiming, sprinting, shooting and reloading in third person.
- [ ] Look at each gun from the side and front; tune `POSES` in `Client.Guns.ThirdPersonGuns` if a hold looks off.


## NPC guard mode (2026-11-11)
- [ ] Put an `NPCRoom` part over a room, make an NPC a guard (`Mode = "Guard"` on its `NPCSpawn`, or `NPCService.SetMode`), break one of the room's boards out of the guard's view, and check it rebuilds it.
- [ ] Shoot the guard while it repairs: it should fight from inside the room, then finish the repair.
- [ ] Note: the NPC cap (`MAX_NPCS`) was 0 and the lobby was off in the last playtest (not from this change).

