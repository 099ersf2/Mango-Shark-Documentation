# Changelog archive: 2026-11-12 to 14

Historical implementation notes, retained as written for search and context. Verify behavior against current system guides before using these details.

## 2026-11-14: Clear House map vote, no prep, guards by room count

Tested in Studio with one player: map vote, Reveal straight to Action, 15 guards on Bank. The test loss was removed from the saved data afterwards.

### Changed

- **Map vote:** Clear House's Selection starts with a vote between the mode's maps, now Mansion and Bank.
    - The map with the most votes is played; a tie is drawn among the tied maps.
    - The map loads when Selection ends. Each player is then given a random free attacker spawn, since spawns belong to a map.
- **Classes:** the attackers' classes, as before.
- **No prep phase:** Reveal goes straight to Action. The doors and windows are boarded, the rooms found and the guards placed while Reveal runs.
- **Guards:** half the map's rooms, rounded up (`ROOM_SHARE` 0.5), plus 2 for each player after the first. No upper limit besides 3 a room. Mansion (26 rooms): 13 to 21. Bank (29 rooms): 15 to 23.
- `Content.ClearHouse`: `PREP_TIME`, `BASE_GUARDS`, `MAX_GUARDS` and `TEXT.Prep` removed; `ROOM_SHARE` added.
- New Siege pick `"Map"` (Clear House only); the snapshot's `Maps` (`{ Name, Votes }`) during Clear House Selection.


## 2026-11-14: Arcade category, Clear House mode

Tested in Studio with one player: a win (guards killed from a test script) and a loss. See [Clear House](CLEAR_HOUSE.md). Both test results were removed from the saved data afterwards.

### Added

- **ARCADE category** in the Game Modes panel, with one mode, **CLEAR HOUSE**:
    - up to 5 players against NPC guards in the Mansion;
    - every door and window boarded up;
    - no bombs, one round.
- **The match:** Selection (spawn and class), Reveal, a 30 s drone Prep while the guards take their rooms, then Action.
    - The players win when every guard is dead.
    - They lose when every player is dead or has left, or after 8 minutes.
- **Room finder** (`Systems.Siege.ClearHouse`): a grid flood fill over the map's floors, with walls, doors and windows as dividers, builds an `NPCRoom` box per room. A map may give hand-drawn rooms in a `Rooms` folder instead.
- **Guards:**
    - 6 for one player, plus 2 for each other player, up to 16, spread over random rooms (big rooms more often, at most 3 a room);
    - Soldier, Breacher or Grenadier;
    - in Guard mode, so each one stays in, patrols and re-boards its room;
    - no respawns.
- **Wins** are saved under `Mode:ClearHouse` and `Category:Arcade`, apart from Siege's stats. The overall Wins/Losses totals still count them.
- `Content.ClearHouse`; `Content.Matchmaking.PartyLimit(mode)`; the mode fields `Kind` and `Maps`; `Content.Siege.ROUNDS.ClearHouse = 1` and the reasons `HouseCleared` / `HouseHeld`.

### Changed

- **Queue:** a party may be as large as the only side of a mode whose other side is empty (5 for Clear House). It was the smaller side, which would have been 0.
- **Maps:** a mode with `Maps` only uses those maps.
- `NPCService.Spawn(profileId, where, spawnPart?, ignoreCap?)`: the new `ignoreCap` passes the `MAX_NPCS` cap, which is 0 today.
- **Siege screens in Clear House:**
    - the roster's enemy section reads HOUSE GUARDS;
    - the HUD objective counts the guards left, and the bomb chips are hidden;
    - the result screen shows "x / y guards down" and a HOUSE GUARDS column.


## 2026-11-14: Shotgun loadouts use PumpShotgun

Studio playtest: `GunService.Give(player, "PumpShotgun")` gave the gun with no warning, and every gun id in the class, lobby and NPC loadouts now has a definition.

### Fixed

- **The shotgun was never given.** The pump shotgun's definition id is `PumpShotgun`, but loadouts still asked for the old id `Shotgun`, so `GunService.Give` warned "no gun named Shotgun" and the player got nothing. Now `PumpShotgun` in:
    - `Content.Classes` loadouts: Breacher (Mason), Hacker (Caleb), and the two other classes that carried it;
    - `Content.Guns.Loadouts`: Breacher, Arsenal, Sprayer;
    - `Content.NPC.Profiles.Breacher`;
    - the per-gun settings in `Content.Guns.Melee` and `Content.Destruction.SoftWallConfig`, so its melee and wall holes apply again.
- The `"Shotgun"` entries in class `Categories` are the category name and stay as they are.


## 2026-11-14: Analytics, crate opening on phones

Studio playtest of a 1v1 up to the end of round 1. Every event logged up to there was printed with the right fields (see [Analytics](ANALYTICS.md)). The crate opening screen was not seen on a phone.

### Added

- **Analytics** (`Systems.Analytics.AnalyticsService`, `Content.Analytics`, `Client.Core.AnalyticsClient`, `Packets.Analytics.MenuOpened`):
    - economy events for Coins and Tokens;
    - Queue and Match funnels, and an onboarding funnel;
    - LobbyVisit and SiegeMatch journeys, which must be created on the Creator Hub;
    - 23 custom events, covering:
        - queue drop-offs and waits;
        - top modes, classes, sites and spawns;
        - which side wins rounds and how long rounds last;
        - kills, deaths, damage and builds per player per match, by mode, category and result;
        - leaving early, weapons, abilities, menus and purchases.
- **New extension points for analytics:**
    - `Siege.SelectionEnded(summary)`: every player's final picks each round, with `Random` set when the class was filled in;
    - `Siege.RoundEnded` gets a 4th argument: mode, map, site and `Final`. At the end of a match it now also fires for the last round;
    - `Siege.Ended` gets a 3rd argument: the match summary, with every player's kills, deaths, damage, builds, side and result;
    - `Store.Bought` gets a 5th argument: the price paid.

### Fixed

- **Crate opening on phones:** the OPEN MORE and DONE buttons were below the bottom of the screen. `Main.Opening` now has a FitScale (design height 460, full width), so the reel and its buttons shrink to fit. The reel's width is read in design pixels, so the won skin still lands under the marker.
- `Content.Store` had been rolled back to an earlier version, losing the `OwnedItems` saved field (bundle purchases would have errored on the server) and the ⚔ Classes icon. Both are back.


## 2026-11-13: Mobile pass for the Store, Inventory, Details and match result

Compile-checked. Desktop checked in a playtest: the Store is unchanged (1180×700, scale 1), and the health bar is hidden in the lobby. **Not yet checked at phone size.**

### Changed

- **The Store, Inventory and Details panels are fitted menus.**
    - Each has a `Fit` UIScale tagged `FitScale`, with `DesignHeight` 640 and `WidthShare` 0.95. On a phone they shrink as a whole instead of cutting cards off.
    - The `Feel` UIScale on these panels was removed (only one UIScale works per frame), so they no longer pop when opened.
- **FitScale changes** (`Client.Core.UI`):
    - a `MinScale` attribute;
    - `FitMode = "Dialog"`: a box built in pixels keeps its size and place and is scaled down to fit the screen both ways.
    - The gift picker and the match result's `Body` (now a 1150×680 pixel box) use it.
- **Cards per row** in the Store (2 to 5) and Inventory (2 to 6) come from the page's width, so cards keep their shape on any screen.
- **Inventory filter chips:** the row scrolls sideways when they don't fit, and gun names are spaced (PUMP SHOTGUN).
- **Lobby wallet panel:** on screens 600 px tall or less it is scaled to 0.72 and sits in the top-left corner, clear of PARTY, PLAY and MODE.
- **Health bar:** hidden while in the lobby (`InLobby`).

### Fixed

- Close buttons were blank squares on phones: the ✕ glyph doesn't draw there and is now X.
- The Classes tab icon (🪖) doesn't draw on phones and is now ⚔.


## 2026-11-13: Prep drone frozen by streaming (found in a playtest)

Playtested in Studio, one player, a 1v1 as the attacker:

- **Before the fix:** in Prep the drone view showed, but the drone didn't move. Its velocity read -37 down while its position never changed, only 1 map part had loaded near it on the client, and the server had the player's `ReplicationFocus` at nil.
- **After the fix:** 36 parts had loaded around the drone at once, holding W drove it 30 studs during Prep (clock at 00:23), no viewmodel was drawn, and there were no new errors.

### Fixed

- **The prep drone was frozen.** The place uses `StreamingIntegrityMode.PauseOutsideLoadedArea`, so a client-owned part outside the loaded area has its physics paused. In Prep the body waits in the lobby, so the area around the drone is only loaded if the player's `ReplicationFocus` is on the drone. It was set when the drone was placed but found cleared later (respawning the body was tested and is not what clears it). This is why drones worked in Action, with the body nearby, and not in Prep.
    - `DroneService` now sets the focus again every check (0.25 s) for every held player, and after their body spawns.
    - `focusOn` only writes the focus when it changes.


## 2026-11-13: Owned Store cards show an OWNED button

Compile-checked only.

### Changed

- **Store cards:** anything the player owns (a game pass, a bundle or other product, a skin, a class, a crate whose skins are all owned) shows a green ✓ OWNED button where the prices were. The Coins, Tokens and Robux buttons are not shown to an owner. A giftable item keeps its gift button at the right of the row. This replaces the greyed prices on owned cards from earlier today.
- **Detail page (unchanged from earlier today):** an owned item shows ✓ OWNED, and its Coins, Tokens and Robux buttons greyed and unclickable.


## 2026-11-13: Prep drone drives, no gun over the drone view

Compile-checked only (not playtested).

### Fixed

- **The gun viewmodel showed over the drone view in Prep.** The server arms the attacker's lobby body when it spawns, after the drone view has opened, and equipping a gun resets the viewmodel's hidden flag. While in a drone, `DroneController` now hides it again on every frame.
- **The prep drone didn't move.**
    - The drive input came only from the default controls, which give no movement while the body is parked (and its controls are off) in the lobby. When they report nothing, the keyboard (WASD) and the gamepad's left stick are now read directly.
    - When a player starts looking through a drone (`Packets.Drone.View`), the server gives them network ownership of their landed drones again, so a body spawning or a short take-back can't leave the drone stuck under server physics.


## 2026-11-13: OWNED for passes and bundles, greyed prices on the detail page

Compile-checked only.

### Added

- **`OwnedItems`** (saved, in `Content.Store`): once-only store items bought, by item Id.
    - `StoreGrants.ApplyItem(data, item)` gives an item's grants and records it. Robux receipts (`Shared.Data`) and Coins/Tokens purchases (`StoreService`) both use it.
    - Bundles bought before this are found in the purchase log when the player joins (`backfillOwned` in `StoreService`), or on their next purchase try, and recorded.
- `StoreViews.Owns(data, "Item", id)` tells whether a store item is owned:
    - a game pass, from Scribe's client pass mirror (`Data.Owns`);
    - a once-only item, from `OwnedItems`, or when everything it grants is owned.

### Changed

- **Store cards:** owned game passes and bundles now show ✓ OWNED with greyed prices, like skins and classes. Before, they showed OWNED only after the server refused a second purchase.
- **Detail page:** an owned item or class shows a green ✓ OWNED button, with its price buttons still there but greyed and unclickable. Gifting stays available.
- The open detail page redraws when the player's data changes, and about 1 s and 3 s after a game pass purchase, so it turns to OWNED right away.


## 2026-11-13: Developer skin pack

Compile-checked only. In Edit mode `Skins.Apply` was run on the Rifle, Pistol and SMG models: 35, 6 and 3+ rainbow parts were tagged, and putting the normal look back cleared every one.

### Added

- **Developer pack:** `DevRifle`, `DevPistol` and `DevSMG` in `Content.Guns.Skins`:
    - black guns;
    - neon rainbow parts (magazine, sights, rifle handguard);
    - rainbow lines down both sides, cut into 0.2-stud pieces;
    - the colors run along the gun as a moving gradient.
    - **Not for sale:** never in a crate or the Store, and hidden in the Inventory from players who don't own them.
- **Rainbow skins** (any skin can use them):
    - a skin's `Rainbow` list of part-name patterns, and `Rainbow = true` on a Detail, make those parts Neon and tag them `SkinRainbow`, with a `RainbowOffset`;
    - `Client.Guns.SkinRainbow` turns their colors every frame;
    - the settings are in `Skins.RAINBOW`: Speed, Length, Saturation, Value, Piece.
- **Skin cards:** a skin's `Card` sets its Inventory card: background colors and a `BORDERS` preset. The Developer skins have black cards with the moving Rainbow border.
- **Commands (admins only, Cmdr):**
    - `givedevskins <players>` (alias `devskins`) gives the pack for good (saved in `WeaponSkins`);
    - `takedevskins <players>` takes it back and unequips it.
    - Both go through `StoreService.GiveSkins(player, skinIds, take?)` and `StoreService.DeveloperSkins()`.
- **SMG skin family:** `SMG` and `SiegeSMG` share one (`SMGSkin` saved field), so the Inventory gets an SMG tab.


## 2026-11-13: Prep drone streaming restored, reinforce counts as building, Store card fixes

Compile-checked only (a playtest was not allowed this time).

### Fixed

- **The prep drone still wasn't viewable.** The earlier streaming fix had been lost from `DroneService`, and the drone template was back to `ModelStreamingMode.Default`, so the drone at the attacker spawn never reached a client whose body waits in the lobby. Restored and made sturdier:
    - every placed drone is `Persistent`, and so is the template;
    - while a player is held in their drone, `focusOn` points their `ReplicationFocus` at it, and clears it when the hold ends or the drone is cleared;
    - the client goes into the drone as soon as one of its drones is there, without needing a body.
- **End screen outlines were cut off.**
    - A player's row outline was clipped by the rows list; it now has 3 px padding.
    - The team columns and MVP cards have room for their edges.
    - The totals now read KILLS, DAMAGE, BUILT in that order.
- **Reinforce was silent for others.** Its sound part now sits in a `Persistent` model, so with streaming on it reaches everyone before the short sound ends. The player who reinforces also hears a local lock-in sound (`BoardPlace` and `FootstepMetal`, in `SiegeHud`).
- **Daily deal text was covered.** The struck-through old price and the detail line now sit just above the price buttons (anchored to the bottom), with a slightly smaller picture.

### Changed

- **A reinforced wall counts as building** (`Classes.Reinforced`, fired by `Abilities.Reinforce`), so it adds to Built and to MASTER BUILDER.
- **Owned Store items** keep their price buttons, greyed and unclickable, under a green ✓ OWNED line. Gifting still works.
- **The % EXTRA tag** is brighter red, not tilted, and sits on the top-left edge of the card, level with the deal tag on the right.


## 2026-11-13: Store coin buttons, OWNED cards, skin tabs per gun

Compile-checked only.

### Fixed

- **The coin icon covered the amount** on Store price buttons, the item page's coin button and the lobby wallet chip. Each now has a `Content` row (`CoinIcon`, then an `Amount` label) laid out side by side, and the code writes the amount there (`setMoneyText` in `Client.Core.Store` and `ItemDetails`).
- **OWNED covered the struck-through old price** on discounted cards the player owns. The old price is hidden once the item is owned.
- **Inventory skin tabs** only offered Rifle and Pistol. There is now a chip for every gun with skins (`Skins.Weapons()`), so LMG shows up, and any gun given skins later gets its own tab.


## 2026-11-13: Siege rounds, match result screen, lobby leaderboard, map music

Compile-checked only (not playtested, as asked).

### Added

- **Siege matches have several rounds**, and the sides swap every round:
    - `1v1` and private matches: best of 3.
    - `5v5`: best of 5.
    - Set in `Content.Siege.ROUNDS` (`DEFAULT_ROUNDS` 3).
- **Between rounds** (new phase `RoundEnd`, `ROUND_END_TIME` 8 s), the next round starts like this:
    - The map is rebuilt from a fresh copy, so boards, walls and broken pieces are whole again.
    - Bombs, defusers, drones and cameras are cleared.
    - Every player is put on their new side and goes through Selection again: class, spawn or site vote, and loadout.
- **The match winner** is the side that won the most rounds, not the side that won the last one:
    - The match stops early once one side has a majority.
    - It also stops early when a side has left (`MATCH_ENDING_REASONS`).
    - Rewards and stats are recorded once, at the end of the match.
- **Round result banner** (`Main.RoundResult`): ROUND WON / LOST / DRAW, the reason, the score (you vs them), a pip per round, and the next round.
- **Match result screen** (`Main.MatchResult`), revealed in stages with count-ups:
    - VICTORY / DEFEAT / DRAW over a green or red tint, with the round score.
    - MVP cards with avatars: TOP FRAGGER (kills), MOST DAMAGE, MASTER BUILDER (pieces repaired).
    - Both teams side by side, each with its totals and every player's K, D, damage and builds. Your row is outlined, and the winning column gets a gold edge and a WINNER tag.
    - Templates: `RoundPip`, `MvpCard`, `TeamColumn`, `ResultRow`.
- **Per-match stats** on the server: kills, deaths, damage dealt to the other side (Prep and Action) and pieces built (`Breakable.Repaired`).
- **Lobby leaderboard:** in the lobby, Tab (the Scoreboard key) shows everyone on the server ranked by total wins, highest first, with rank (#1 gold, #2 silver, #3 bronze) and win streak. The wins come from the new `TotalWins` player attribute, set by `StatsService`.
- **Per-map background music:** a folder in `Assets.Music` (or `Assets.Music.Primary`) named like the active Siege map is played instead of the normal background songs during that match.

### Changed

- **Siege class picking:** classes for sale that the player doesn't own are greyed out, marked LOCKED, and listed after the ones they can pick.
- **Inventory:** a skin sold by a store item with a `Border` or `Glow` (the Obsidian Pack) shows that item's moving border and sheen on its card, as in the Store.
- `Combat.Hit` now also passes the damage dealt (0 when blocked) and the item.

### Fixed

- **The prep drone view was lost when the body spawned.**
    - In Prep the attacker's body loads in the lobby a moment after the drone view opens, and the client left the drone whenever a new body arrived.
    - A player held in their drone now stays in it: the new body is anchored where it is, and drone control is asked for again (the server drops it when a body spawns).
- `SiegeService` called `ownsClass` before it was defined (nil at runtime) at the end of Selection.


## 2026-11-13: Gifting, border styles, coin icon, class initials

Compile-checked only.

### Added

- **Gifting Robux crates and items** to another player in the server: a gift button on the card and GIFT on the detail page open the picker (`Main.GiftPicker`, `Client.Core.GiftPicker`). It lists every other player with their avatar.
    - `Packets.Store.Gift` → `StoreService.Gift` checks the recipient can get it, then opens Scribe's gift prompt (`Data.PromptGift`).
    - Scribe records the gift before money moves and delivers it to the recipient's data, even if they leave.
    - Game passes, and Coins or Tokens prices, can't be gifted.
- **Border styles** (`Content.Store.BORDERS`, an item's `Border`): the glowing outline's colors turn around the card. Gold is the default; there are also Rainbow and Obsidian.
    - The Obsidian skin has the Obsidian border (black and violet, turning) with the glow.
- **The coin icon:** "Glossy Gold Coin Icon" from the Creator Store (`Content.Store.COIN_ICON`). It is on every coin price and both wallets.
- **Class pictures:** a class's `Icon`, or its first initial when it has none, on its card and big page.
- **A dimmed blocker** under the detail page (`Main.DetailsBlocker`): nothing behind it can be pressed while it is open.

### Fixed

- **Ribbons (NEW...) overlapped the title:** they sit above the card's top edge now.
- **Hovered cards' borders overlapped their neighbors:** wider margins in the card holder.


## 2026-11-13: Store fixes, Blake for sale, lobby panel, PLAY shine

Compile-checked only.

### Fixed

- **Inventory error** (`Inventory:104: attempt to index function with 'Get'`): the crate inventory's field was named `Count`, which Scribe containers already use for their `Count()` method. It is `Amount` now (`CrateInventory[crateId].Amount`). The server wrote the same field, so no crate was ever saved under the old name.
- **Hovering a card made the grid re-wrap:** every card, rail button and filter chip now sits in an invisible holder frame at its layout size (`StoreCard.Card`, `NavButton.Button`, `FilterChip.Button`). The hover grow happens inside it.
- **Outlines and ribbons were cut off at the page edges:** the holders leave a margin and the pages have padding.

### Added

- **Blake** (the `Hologram` class) is sold: 6,000 Coins or 60 Siege Tokens, featured with a NEW ribbon. Players who don't own it can't pick it in Siege.
- **PLAY shine:** a shine sweeps across the PLAY button every 2.4 s (`Client.Core.Shine` animates any UIGradient tagged `ShineSweep`).

### Changed

- **The lobby panel:** Coins, Siege Tokens, STORE and INVENTORY are one panel on the left (`Main.Wallet`), in the lobby buttons' slate-and-white style.
- **Removed:** the extra Inventory (old Backpack) button in the top-right menu.


## 2026-11-13: Store and Inventory redesign, crates go to the inventory

Compile-checked only (no playtest, as asked).

### Added

- **The Store** (`Main.Store`, `Client.Core.Store`), redesigned:
    - **Layout:** an icon rail (Featured, Crates, Currency, Passes, Bundles, Skins, Classes), balances with "+" buttons, and section headers.
    - **Big cards:** double-width cards for featured and big items.
    - **Labels and badges:** ribbons (POPULAR, BEST VALUE, 🔥 HOT DEAL, NEW), "% OFF" with the old price struck through, and "% EXTRA" on bigger packs.
    - **Glow:** glowing outlines with a sweeping sheen.
    - **Daily deal:** one item a day at 30% off its Coins and Tokens price, with a countdown. The server charges the same price (`Content.Store.PriceOf`).
- **The Inventory** (`Main.Inventory`, `Client.Core.Inventory`; INVENTORY on the lobby bar, and the old Backpack button):
    - **Classes:** yours, then "CLASSES TO BE UNLOCKED", filtered by team.
    - **Skins:** owned, then locked; equip from the skin's page.
    - **Crates:** the crates you own, with a count.
- **A big detail page** (`Main.Details`, `Client.Core.ItemDetails`), like a character select screen:
    - the name, team or rarity, description and a large 3D preview;
    - starter items with gun previews;
    - the ability in depth (cooldown, charges, description);
    - a crate's contents with each chance and what you own;
    - prices or OPEN / EQUIP, and BACK / EXIT.
- **Shared view builders:** `Client.Core.StoreViews`, so a crate or class looks the same in both screens.
- **Classes for sale:** `Content.Store.CLASS_PRICES` (Coins and/or Tokens). A class listed there is locked until bought (`Class:<id>`). None is listed yet.
- **Crate rarity and ribbon:** each crate has a `Rarity` (card colors) and a `Tag`.
- **Packet `Store.Open`:** opens a crate from the inventory.

### Changed

- **Crates no longer open when bought** (Coins, Tokens or Robux). They go into the new saved `CrateInventory` and are opened from the Inventory. OPEN plays the reel (`Main.Opening`), which offers OPEN ANOTHER while you have more.
- **Bundles can include crates** (`Grants.Crates`). The Starter Bundle now has a Field Crate, and is shown as a 50% OFF hot deal.
- **The Armory screen is gone:** the shop stand opens the Store on CRATES.
- `StoreService.Buy` answers (ok, message). The new `StoreService.OpenCrate` gives the skin.


## 2026-11-13: Store products created

- The 8 new developer products and the VIP game pass are created on Roblox (through Open Cloud), at the prices the Store shows, and their ids are in `Shared.ProductIds`. Every Robux price in the Store is now live instead of SOON. The icons are placeholders. See [Store, currencies, crates, and stats](STORE.md#limits).


## 2026-11-13: Store, Siege Tokens, your own crates, wins and streaks

Server side checked in a Studio playtest. The screens weren't seen (no playtest asked). See [Store, currencies, crates, and stats](STORE.md#testing).

### Added

- **Crates as data** (`Content.Crates`): add a crate with its skins and weights, and its Coins, Tokens and Robux prices. The Armory has a crate picker and Coins / Tokens / Robux buttons.
- **Siege Tokens:** a premium currency, 5 to start. Bought with Robux, or given by `StoreService.Give` (battle pass, quests).
- **Coins for playing:** 100 for a win, 30 for a loss, 50 for a draw (at least 60 s), and 15 every 5 minutes of play. The VIP pass doubles them.
- **The Store** (`Main.Store`, STORE on the lobby wallet bar):
    - tabs for crates, currency packs, game passes, bundles, special skins and classes, all from `Content.Store`;
    - Robux items show SOON until their id is set.
    - New: the special skin Obsidian, the Starter Bundle and the VIP pass.
- **Wins and losses:** totals, and per mode and category. A win streak per mode, with a 🔥 tag above the head from 2.
- **The last mode played** is saved, and PLAY starts on it.
- `Systems.Store.StoreService`, `Systems.Store.StatsService`, `Shared.StoreGrants`, `Client.Core.Store`; packets `Store.Buy` and `Store.Reward`.

### Changed

- Robux products are declared from the data in `Shared.Data`: `Crate_<Id>` and `Store_<Id>`, plus game passes. The old `SkinCrate` product is the same id as `Crate_Field`.
- `Packets.Skins.BuyCrate` now buys the Field Crate through `StoreService`.
- Siege refuses a locked class the player doesn't own (none is locked).


## 2026-11-13: Armory shop, crate reel, skins on every gun

Compile-checked; the shop opened in a playtest and its cards, tabs and crate list filled in. Studio was not rendering frames, so the 3D previews and the reel were not seen moving. A real crate purchase was not made.

### Added

- **The shop is now the ARMORY** (`Main.SkinShop`, built in Studio):
    - Tabs (All / Pistol / Rifle).
    - A grid of skin cards, each with a 3D preview of the gun wearing the skin, its color stripe, and Equip / Equipped / In crate.
    - A crate panel with the price, OPEN CRATE, every skin still in the crate with its chance, and a status line.
    - New templates: `SkinCard`, `SkinTab`, `CrateItem`, `ReelCard`.
- **Crate opening reel:**
    - After a crate is bought, the won skin arrives in the player's data and the reel spins: a strip of skin cards slows down over 6 s onto the skin won, ticking as each card passes the gold marker.
    - YOU GOT then shows the skin, with EQUIP / DONE.
    - It is a show only: the server picks and grants the skin before the reel starts.
    - `SkinShop.Preview(skinId)` plays it without buying, for testing.

### Fixed

- **Skins did nothing in matches.** A skin was for one gun Id (`Rifle`, `Pistol`), but Siege hands out other guns. Skins now belong to a family:
    - Rifle skins show on the Rifle, BurstRifle, SiegeCarbine and Tactical bullpup.
    - Pistol skins show on the Pistol, SiegePistol and Revolver.
    - (`Content.Guns.Skins` `FAMILIES`, `Skins.FamilyOf`; `EquipField` uses the family.)
- A gun that is one textured mesh shows the skin's color: its texture comes off while the skin is on, and comes back with "None". Checked on copies: the SiegePistol, BurstRifle, SiegeCarbine and Revolver recolor, and go back exactly on "None".


## 2026-11-13: Cameras show your own body

Compile-checked only (not playtested).

### Changed

- Looking through a security camera now shows your own body and held gun, like the drone view. First person hides them on your screen every frame, and `Client.Gadgets.CameraController` shows them again after that.


## 2026-11-13: Siege prep drone always shows

Compile-checked only (not playtested, as asked).

### Fixed

- **The prep drone didn't show.** With streaming on, an attacker's drone stood at the attacker spawn while their body waited in the lobby, so the drone and the area around it never loaded on their client and there was nothing to look through. Drones are now `ModelStreamingMode.Persistent`, and while a player is held in their drone the server sets their `ReplicationFocus` to it, so the world around the drone streams in.
- The attacker is held in the drone (`SetLockedIn`) before the drone is placed, so the body arriving in the lobby can never clear it.
- A missing spawn no longer means no drone: the attacker's picked spawn, else any attacker spawn, is used. With none at all, the player gets NO SIGNAL (and a warning in the output).
- While held (Prep), the client always shows the drone view, or NO SIGNAL when there is no drone, until the server lets go at Action. No body is needed for it.


## 2026-11-13: Siege attackers keep the prep drone and get a second one

Playtested in Studio with one player, driving DroneService and DroneController directly (no full two-team match):

- The prep drone stayed in the world, and the player stayed held in it, with the body flagged InLobby.
- At "Action" the player had DronesReady 1 and DronesMax 2. The Drone key threw the second drone and looked through it, and the touch NEXT button showed.
- Switching went DRONE 2 → DRONE 1 → DRONE 2.
- A scan from each drone at a target in front of it returned true.
- Console clean.

### Added

- `DroneService.AddCharge(player)`: one more drone (a slot and a ready charge) until the next refund. A player's limit is the `DronesMax` attribute (`Content.Drones.MAX_ATTRIBUTE`).
- **Switching drones** while in one, like the cameras: Aim (right mouse), LB / RB on gamepad, or the NEXT button on touch (`DroneFeed.Feed.Touch.Next`, shown only with a second drone). Scanning works from whichever drone you look through.

### Changed

- **Siege prep:** the attacker stays on the drone screen until Action, NO SIGNAL included. Their body waits in the lobby (InLobby), which used to clear the drone and refuse the view; a drone the player is held in now survives it.
- **Siege Action:** the prep drone stays where it is and each attacker gets a second drone to throw (Drone key). A destroyed drone still never comes back. NO SIGNAL shows only when no drone is out and none is ready.
- The Drone key on foot throws a ready drone first; after that it goes into one you already have out.


## 2026-11-13: Custom prompts, build or reinforce, startup fix

Playtested in Studio with one player: startup clean, a drone thrown outside the lobby showed its feed and stayed in it for over 8 s. The new prompt cards were not seen in a playtest (it was stopped before a board was placed), and nothing was run on a phone or gamepad.

### Added

- **Custom proximity prompts** (`Client.Interact.CustomPrompts`): every prompt is drawn as the game's own card (key, action, object, hold bar), from `Assets.UI.Templates.PromptCard`. Prompts on the same object share one `PromptStack`, 2 cards per row, wrapping onto a new row. On touch, hold the card itself.
- Prompt keys never clash: if two shown prompts use the same key or gamepad button, the one without `FixedKey` moves to a free one (E, F, T, G, Z, V / DPad Up, DPad Down, DPad Right, Y).

### Changed

- **A defender frame offers both choices:** build normal boards (Interact, E) or place a reinforced wall (the Reinforcement Expert's ability key, T), side by side. No board needs to be there first. Until now the build prompt was hidden from the Reinforcement Expert while they had charges.
- Attackers never see or trigger the build prompt (its reach is 0 on their client; before, it was only hidden).

### Fixed

- `ClassService.BeginPlacement` errored (`attempt to call a nil value`, line 344): it called `BreakableService.PositionBuilder`, which doesn't exist. Reinforce placement never started.
- **Drones (and every other client system) could fail to start.** `Client.Settings.Options` and `Keybinds` waited for saved data inside `Init`, so a slow or stuck data load held up every client module after them: no drone keys, no HUD. They now load in the background, use the defaults until the data arrives, then apply the saved values.


## 2026-11-13: Mobile UI pass (icons, smaller buttons, no overlaps)

Checked in Studio by laying the screens out in an 844 × 390 frame (a phone in landscape) and with one playtest on the desktop-sized Studio window: console clean. Not run on a real phone, a tablet or a gamepad, and not in a real two-player Siege match.

### Added

- **Icons on the touch buttons**, from the Creator Store: fire (bullet), aim (crosshair), reload, crouch, melee (knife), sprint, grenade or smoke, camera, drone, ability (lightning), admin console. Each is an ImageLabel `Glyph` inside the button's `Icon`. Only the grenade, drone and ability buttons keep a small label (the count or the cooldown).
- `Content.Consumables` entries have an `Icon` (the grenade and smoke pictures on the button).
- **Full-screen menus fit any screen** (`FitScale` tag on a UIScale, run by `Client.Core.UI`). The Siege selection screen starts under Roblox's top bar and shrinks to fit a phone, so nothing hides behind the Roblox buttons.
- `Main.MenuButtons.TouchScale` shrinks the top-right buttons to 0.8 on small touch screens.

### Changed

- Touch buttons are about 30% smaller and re-spaced like other Roblox shooters: FIRE 1.15 of the jump button, the others 0.55 to 0.72, with a gap between every pair.
- The phone boost for the health bar, ammo box, weapon slots and kill feed is 1.15 (was 1.6).
- Siege HUD: a compact timer pill at the top with SCORE beside it (it sat on top of the timer), the objective line and the A and B chips under it, each on one line ("PLANTED" instead of "DEFUSER PLANTED").
- The announcement banner ("Preparation phase", "Defuser planted…") is slimmer and sits above the crosshair, below the timer, instead of over it.
- Selection screen: small text is 1 to 2 px bigger, the Loadout column is more compact, so nothing spills under the Ready button on a phone.
- Death screen: a compact card, the SPECTATING line and the countdown stack at the bottom centre, above Siege's spectate bar, instead of on top of each other.

### Fixed

- The round-end panel no longer draws over the still-visible death and spectate texts: it hides them and draws above them, and its kill rows draw above the panel.
- The empty grey bar at the top right after dying: Roblox's own health bar, now turned off (the HUD has its own).


## 2026-11-12: Camera and drone scans reveal players and cameras

Single-client Studio startup check passed and all nine changed Luau sources parsed. Multiplayer scanning and class reveal were not exercised.

### Added

- **Defender cameras scan attackers.** Interact (DPad Up; touch `SCAN`) asks the server to scan an enemy player in a live camera's view (150 studs, 6°, clear line of sight, five-second cooldown). A successful scan reveals the attacker's class to defenders for the match and alerts the target.
- **Drone scans can reveal enemy cameras.** When no player or NPC is selected, a scan can mark a live enemy camera for the drone user's team with key `Camera:<CameraId>` for `SPOT_TIME`.
- A red `SCANNED` notice appears for `SCANNED_ALERT_TIME` after a player is scanned by either system.
- API additions: `Packets.Camera.Scan`, `Packets.Scan.Alert`, and the `Camera.Scanned(spotter, targetModel)` extension.

### Changed

- Enemy classes are hidden from both teams until revealed by their side's scan: drones reveal defenders to attackers; cameras reveal attackers to defenders.
- Camera and drone feeds show the match timer over both live and NO SIGNAL screens.
- Cycling away from a destroyed camera is no longer blocked by the normal view-switch cooldown.


## 2026-11-12: Drone scan reveals nearby enemies with a popup

Not playtested (compile-checked only).

### Changed

- **A scan no longer needs the enemy in the crosshair:** with nobody there, it takes the nearest enemy within 40 studs in clear view (`NEARBY_RANGE` in `DroneService`).
- **Every attacker gets a popup** on a scan of a defender: "ENEMY SCANNED" with the defender's name and class (`SiegeService.onSpotted`). The class shows on the attackers' scoreboard (Tab) from then on, and the mark where the defender stood goes to the whole team, as before.


## 2026-11-12: Party shows again after a match

Not playtested (it needs live servers and two players).

### Fixed

- **Back from a match, the screen showed no party** although the server still had it (inviting the same players was refused as "already in your party"). The party message could be sent before the returning client was listening. The client now asks for its party when it starts, a few times in the first seconds, when a match ends, and when the Party menu opens (`Party.Request` action `Sync`, [Matchmaking and parties](MATCHMAKING.md#party-sync-2026-11-12-not-run)).


## 2026-11-12: The other team in the ready list; Reinforce works again

Not playtested. The Reinforce swap was checked in Edit mode on copies of a board and a door.

### Added

- **The ready list shows the other team too,** in its own section under a red ENEMY TEAM heading with the side's name, red names and dark red rows. Only who they are and whether they are ready is sent; never their picks ([Siege](SIEGE.md)).

### Fixed

- **Reinforce refused every board and door** ("That can't be reinforced"). The reinforced models had been moved from `Assets.Models.Siege` to `Assets.Models` and renamed (`ReinforcedDoor`), and the ability only looked in the old place. It now looks in `Assets.Models` first and says "The reinforced model is missing" if a model is ever gone.
- **Reinforce could not target an empty door frame** (a door whose boards are not built yet has nothing to aim at). It now takes the board nearest the line of sight.


## 2026-11-12: Drone, camera and slide fixes; ready list; play with party; touch layout

Not playtested (by request): compile-checked, and the touch layout worked out by arithmetic for three screen sizes.

### Added

- **PLAY WITH PARTY** in the lobby: a match of the party's own members only, dealt into two even teams (`QueueService.JoinPrivate`, [Matchmaking and parties](MATCHMAKING.md#play-with-party-2026-11-12)).
- **Selection:** a team list down the right side with each teammate's picture, name and READY or PICKING; when everyone in the match is ready the clock is skipped. A Consumable row on the Class page.
- **`Client.Hud.Nameplates`:** enemies show no name and no health bar; teammates show both.
- The drone feed's own touch stick, and control hints and touch buttons on the NO SIGNAL screens.

### Fixed

- **Drone scans found nobody:** the line of sight stopped at invisible room volumes and other triggers, and the aim had to be near the torso's center. Now only visible, solid parts block, and any body part near the crosshair counts.
- **Touch could not drive the drone.**
- **The drone camera looked through walls.**
- **NO SIGNAL could not be closed** with the drone keys.
- **A destroyed camera was 4% see-through;** it is opaque now.
- **A player who left a queued party kept seeing the search.**
- **Sliding was inconsistent:** a crouch press is judged by sprint intent and waits up to 0.3 s for a slide to be possible ([Movement and camera](MOVEMENT.md)).
- **Touch buttons:** the left ones were placed from the right corner and slid off narrow phones; the right ones ran up the whole edge. All are now laid out from one table ([UI](UI.md)).

### Changed

- **Reinforce** replaces the board with its reinforced model (`Assets.Models.Siege.ReinforcedBoard` / `ReinforcedDoorBoard`) instead of cutting the damage the original takes. The original is kept and put back when the match ends.
- The UI's ScreenGuis live under `ReplicatedFirst.UILoader` (another developer's move); the docs say so now.


## 2026-11-12: Match music (start, panic, end)

See [Music](MUSIC.md). Not playtested (by request): compile-checked only.

### Added

- **A panic song in the last 30 seconds** of the Action phase: the playing song fades to 0 over 4 s while a random song from `Assets.Music.Panic` rises from 0 to its volume (0.5).
- **An end song** from `Assets.Music.End` when the match ends, and **a start song** from `Assets.Music.Start` when a match begins.
- `Content.Music` (folder names, the 30 seconds, the fade times) and `Client.Core.Music.Play(kind)`.

### Changed

- `Client.Core.Music` was rewritten: it plays its own Sounds (in the Music sound group) so it can crossfade, and never picks the same song twice running. The old module is in `ServerStorage.Archive.OldMusic`; the `Music` effect in `Content.Effects.Registry` is no longer used.


## 2026-11-12: Images, tags and colors on mode cards

Not playtested (by request): compile-checked only.

### Added

- **`Image` on categories and modes** (`Content.Matchmaking`): a picture that fills the card, under a dark fade so the name stays readable. `Assets.UI.Templates.ModeCard` has new `Art` and `Shade` parts.
- **`Tag`, `TagColor` and `Color` on modes.** A mode's card used its category's; now each mode has its own (1 V 1: red, DUEL; 5 V 5: blue, TEAM).
- **`Icon` on categories and modes:** the big faded text on the card. `""` keeps the automatic text (none over an image); anything else is shown as written ([UI](UI.md#what-a-card-shows)).


## 2026-11-12: Game Modes panel; no loadout picking in the lobby

Not playtested (by request): compile-checked, and the panel measured at phone and desktop sizes.

### Added

- **The Game Modes panel** (`Main.Modes`, `Client.Core.ModeMenu`): a full-screen game-select screen with one card per mode category (DUELS, SQUADS), a description box, and EXIT ([UI](UI.md#the-game-modes-panel)). Pressing a category shows its modes; a category with one mode picks it at once.
- `Content.Matchmaking.CATEGORIES`; each mode has a `Category` and a `Description`; `Content.Matchmaking.ModesIn(categoryId)`.
- `ModeMenu.Selected()` / `Pick(id)` / `Open()` / `Changed`; `Client.Core.Matchmaking.OpenModes()`.

### Changed

- **The lobby bar's MODE button** sits right of PLAY (where LOADOUT was) and opens the panel instead of stepping to the next mode.
- `LoadoutService` refuses a loadout pick while the player's `InLobby` attribute is true, and always on a lobby server.

### Removed

- **The Loadout key (B) and the game-mode key (M).** Both actions are gone from `Shared.PlayerSettings` and the Settings menu.
- **The lobby bar's LOADOUT button** (archived as `ServerStorage.Archive.OldUI.LobbyLoadoutButton`). Nothing opens the Loadout menu now, which also holds the grenade / smoke picker.
- `Content.Matchmaking.NextMode`, `Client.Core.Matchmaking.NextMode`.


## 2026-11-12: Queue modes (1 V 1), Fredoka One, lobby clean-up

### Added

- **Queue modes.** A party queues for one mode and is only matched with tickets of that mode ([Matchmaking and parties](MATCHMAKING.md#queue-modes)). Modes are rows in `Content.Matchmaking.MODES`: **1 V 1** (the default, so two players are enough) and **5 V 5**. The ticket carries the mode (`G`), the match record too (`Mode`).
- **A mode button above PLAY** (`Main.Lobby.ModeButton`) and a key, **GameMode (M)**: each press moves to the next mode. The search status shows the mode.
- `QueueService.Join(player, modeId)`, `Content.Matchmaking.GetMode` / `NextMode`, `Client.Core.Matchmaking.NextMode()`.

### Changed

- **Every piece of text is Fredoka One** (221 labels, buttons and text boxes in `StarterGui`, the UI templates and the world, plus the text `LobbyHubUI` and the banner effect build in code). Cmdr's console keeps its own fonts.
- `Queue.Request` takes the mode's Id as a second value; `Queue.State` has `Mode`.
- `Content.Matchmaking.MAX_WAIT` is gone: each mode has its own `MaxWait`.

### Removed

- **The Loadout menu no longer opens by itself on join.** It still opens from the lobby bar's LOADOUT button and with B.
- **The Career and Maps buttons** are no longer shown in the lobby (`Client.Core.LobbyHubUI`). Their panels and code are still there; Backpack still shows.


## 2026-11-12: No strafe tilt in the lobby

### Changed

- The camera no longer tilts when strafing (A/D) in the lobby, where there's no gun in hand (`Client.Movement.MovementCamera`, the `InLobby` attribute). It still tilts in the arena.


## 2026-11-12: UI revamp (MVP pass)

See [UI](UI.md). Laid out and checked by measurement only: nobody has seen it rendered yet.

### Added

- **A big green PLAY button, bottom center** (`Main.Lobby`). Pressing it queues the party at once; while searching it is red and cancels. PARTY sits to its left and LOADOUT to its right, with the queue status above.
- **Party is its own menu** (`Main.Party`, key L): member rows with avatars, LEAD and KICK, LEAVE PARTY, and the invite list. It is no longer inside a Play menu.
- **`Client.Core.UIFeel`:** every button in the game squashes when pressed, grows on hover, and has a sound; refused buttons buzz; menus pop in. Six new UI sounds (`UIOpen`, `UIClose`, `UIConfirm`, `UIError`, `UITick`, `UINotify`), placeholders made from the two the game had.
- **Siege team cards** in the style of an operator line-up, dealt in on the reveal; the reveal reads OBJECTIVE LOCATION or INSERTION POINT.
- Sounds and effects on the moments that matter: search started, match found, invite received, pick accepted, the last 5 seconds of selection, a new phase, an ability used or refused, the round's end.
- Keys: **Party (L)**. Play (K) now queues or cancels.

### Changed

- **One look** for the Loadout, Settings, Skin shop and Scoreboard menus and their rows: the same panel, heavy titles, bold buttons, round corners.
- **Touch sizes:** close buttons 44 × 40 (were 36), the top-right menu buttons 120 × 44 and wrapping onto rows (were 132 × 36 in one line), invite buttons 42 tall (were 30), party rows 44 tall, the health bar 40% thicker, weapon slots 30% taller. The SCORE touch button moved out of the combat buttons to the top of the Siege HUD.
- The top-right menu buttons hide during Prep and Action.

### Removed (archived in `ServerStorage.Archive.OldUI`)

- The Play menu that held the queue and the party together (`Main.Matchmaking`) and its button (`MenuButtons.PlayButton`).


## 2026-11-12: Siege bombs are in place from the prep phase

See [Siege](SIEGE.md#the-bombs).

### Added

- **The bombs are placed for the defenders.** When Prep starts, a copy of the bomb model (`Content.Siege.BOMB_MODEL`, today `Workspace.Bomb`) is stood on `BombA` and `BombB` of the chosen site, in `workspace.SiegeBombs`, and removed after the match. Checked in Studio: 2 bombs one second into Prep, every part anchored and visible, centered on the map's bomb part; 0 after the match.
- **A bomb's room can be a folder of parts**, not only one part (`Sites/<site>/BombA`), for rooms one box doesn't fit.

### Changed

- **Wording:** nobody plants a bomb. Only attackers plant anything, a defuser; defenders keep them away from the bombs. The HUD chips read NO DEFUSER / DEFUSER PLANTED, and the defenders' objective reads "Keep the attackers off both bombs". The docs and code comments say the same.

### Fixed

- The end-of-match cleanup called a helper before it was defined, which left a match stuck in its End phase with a repeating error (introduced and fixed the same day, before any push).


## 2026-11-12: Siege, global matchmaking, parties and classes

See [Siege](SIEGE.md), [Matchmaking and parties](MATCHMAKING.md) and [Siege classes](CLASSES.md). Tested in Studio with one player only; nothing cross-server has run live.

### Added

- **Siege**, the only mode: attackers plant a defuser on both bombs of the site the defenders voted for; one round, one life. `Systems.Siege.SiegeService`, `SiegeMap`, `SpectateService`; `Content.Siege`; `Content.Match.Modes.Siege`.
- **Global matchmaking:** a MemoryStore queue, one matchmaker at a time (a lease), party-aware team packing, a reserved server per match, and the return to the lobby. `Systems.Matchmaking.*`, `Helpers.Retry`, `Content.Matchmaking`. Studio forms matches on the Studio server.
- **Parties** of up to five across lobby servers: invite, accept, leave, kick, promote.
- **Classes:** five a side, one player per class per team, each with an ability. `Content.Classes`, `Systems.Classes.ClassService`, `Gadgets`, ten modules in `Systems.Classes.Abilities`; gadget models in `Assets.Models.Siege`.
- **Defender cameras:** `Systems.Cameras.CameraService`, `Client.Gadgets.CameraController`, `Content.Cameras`, `StarterGui.CameraFeed`.
- **Spectating** teammates, then enemies, after the death camera (same camera, Camera + 4).
- **UI, built in Studio:** `Main.Matchmaking`, `Main.PartyInvite`, `Main.MenuButtons.PlayButton`, `StarterGui.SiegeSelect`, `Main.SiegeHUD`, `Main.SiegeScoreboard`, `StarterGui.CameraFeed`, `DroneFeed.NoSignal`, `Main.Mobile.AbilityButton` / `CameraButton` / `ScoreButton`, and templates `PartySlot`, `InviteRow`, `SiegeOption`, `SiegeClassCard`, `SiegeTeamCard`, `SiegeBoardRow`, `SiegeBoardTeam`, `SiegeKillRow`, `BombMarker`.
- **Client modules:** `Client.Core.Matchmaking`, `Client.Core.SiegeSelect`, `Client.Core.Spectate`, `Client.Hud.SiegeHud`, `Client.Hud.Scoreboard`, `Client.Gadgets.CameraController`.
- **Packets:** groups `Party`, `Queue`, `Siege`, `Class`, `Camera`, `Spectate`; `Drone.Scan`, `Drone.Marked`.
- **Keys:** Play (K), Class ability (T). Teams `Attackers` and `Defenders`. Effects `GadgetPlace`, `GadgetDestroyed`, `Flashbang`, `AbilityPulse`.
- **Extension points:** `Siege.*`, `Party.*`, `Queue.*`, `Matchmaking.*`, `Classes.*`, `Camera.*`, `Spectate.Changed`, `Drone.PreventRespawn`, `Drone.PreventView`, `Lobby.PreventFirstSpawn`, `Loadout.PreventApply`, `Death.PreventSpectate` (all in [All extension points](api/reference/extension-points.md)).

### Changed

- **Drones:** a scan leaves a static mark where the enemy stood (30 s, replaced by the next scan) instead of a highlight and marker that followed them; the scan cooldown is 5 s and fully enforced by the server. New: `DroneService.Place`, `Mark`, `SetEnabled`, `SetLockedIn`, `Lock`, `CanView`; the NO SIGNAL screen.
- **MatchService** keeps `External` modes: for those it never starts, shuffles, respawns or ends anything itself. New: `BeginExternal`, `SetClock`, `Finish`, `Reset`, `Kills`, `Refresh`.
- **MatchHud** no longer owns the scoreboard (`Client.Hud.Scoreboard` does).
- **LoadoutService:** `LoadoutService.Arm(player, guns)`; `Loadout.PreventApply`.
- **LobbyService:** `LobbyService.Release(player)`; `Lobby.PreventFirstSpawn`.
- **DeathCamService:** `DeathCamService.Release(player)`; `Death.PreventSpectate`.

### Removed (archived, nothing deleted)

In `ServerStorage.Archive.OldMatchModes`: the Team Deathmatch, Free-for-All and Elimination modes; the admin Match menu (`Client.Core.MatchMenu`, `Main.MatchMenu`, `MenuButtons.MatchButton`); the `match`, `matchmode` and `matchset` commands; the old scoreboard frame and its `ScoreboardRow` / `ScoreboardTeam` templates; and copies of `MatchService`, `Packets`, `PlayerSettings` and `Content.Match.Settings` as they were. `Packets.Match.Admin` and the Match key (M) are gone. In `ServerStorage.Archive.OldDroneSpot`: the `SpotHighlight` template.
