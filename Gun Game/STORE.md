[Documentation home](index.md) / Gun Game

# Store, currencies, crates and stats

*Added 2026-11-13.*

## What it is and how it plays

> **2026-11-17:** the Gilded, Eclipse, Verdant, Field and Shield crates and their 65 skins were removed (archived in `ServerStorage.Archive.RemovedCrates_2026_11_17`). Crates left: Cosmetic, Afterburn, Glacier. Players lose any of those skins and unopened crates they owned (data migration 2 in `Shared.Data`). The Starter Bundle now gives 2,000 Coins only, the 5,000 Coins pack says only that, the Battle Pass lost its 19 crate rewards from those crates, and the daily deal is only the 15,000 Coins pack. Mentions of those crates further down are history.

There are two currencies:

- **Coins** come from playing:
  - **Win:** 100.
  - **Finish a match on the losing side:** 30.
  - **Draw:** 50, only if the match ran at least 60 s.
  - **Play time:** 15 every 5 minutes in any server.
  - The VIP pass doubles all of these.
- **Siege Tokens were removed (2026-11-15).** Coins are the only currency. Nothing is priced in Tokens or pays them out, `StoreService` refuses them, and the wallet doesn't show them. The saved `Tokens` field stays unused so old saves load.

What can be bought:

- **Crates** with Coins or Robux. Opening one plays the reel (see [SKINS.md](SKINS.md)).
- **Everything in the Store** (lobby: STORE button on the wallet bar at the top):
  - crates;
  - coin packs (for Robux);
  - game passes;
  - bundles;
  - special skins (Store only, never in a crate);
  - classes.

Every match result counts:

- A win or a loss, in the totals and per **mode** (the matchmaking mode, like `5v5`) and **category** (like `Siege`).
- A **win streak** per mode. From 2 wins in a row, a 🔥 tag with the streak shows above the player's head for everyone: in a match, their streak in that mode; in the lobby, in their last mode.
- The lobby's **PLAY** button starts on the last mode played.

## The Store and Inventory screens (2026-11-13)

### Store

`Main.Store`, `Client.Core.Store`:

- An icon rail of sections.
- Cards with ribbons (`Tag`), % OFF (`Discount`), % EXTRA (`Bonus`), double width (`Big`) and a glowing sheen (`Glow`).
- Featured first, then the Daily Deal (`DAILY_DEALS`, `DAILY_DISCOUNT`), then Crates. A deal only lowers a Coins price, so it lists crates and coin-priced items, never bundles or passes.

### Bundles and passes (2026-11-15)

- **Robux only.** `StoreService` refuses Coins for an item in the `Bundles` section or marked `Pass`.
- **New contents reach owners.** Add a skin or class to a bundle's or pass's `Grants` and every owner gets it on their next join:
  - bundles: owned = in `OwnedItems`, or in the purchase log (then recorded);
  - passes: `PassCosmetics` checks every `Pass` item with Roblox (retries once after 5 s), and right after a purchase.
- Coins and crates in `Grants` are given once, at purchase, never again.
- Price buttons are on the card. Clicking the card opens the detail page.

Why it is laid out this way, from how other game stores sell:

- **Anchoring:** the old price, struck through.
- **Bigger packs read as the better deal:** "% EXTRA", BEST VALUE.
- **Scarcity:** the daily deal's countdown.
- **Social proof:** POPULAR.
- **Visual weight:** big, glowing cards for what you most want sold.

### Inventory

`Main.Inventory`, `Client.Core.Inventory`:

- **Classes** (team filter): yours, then locked with their price.
- **Skins** (gun filter): owned, then locked.
- **Crates:** waiting to be opened.

### Detail page

`Main.Details`, `Client.Core.ItemDetails`, built by `Client.Core.StoreViews`. Since 2026-11-15 the big preview turns while the page is open, and a row with a preview (a bundle's items, a crate's skins) can be clicked to show that item there, with its name and description, under the bundle's title; clicking it again goes back. Cards turn their gun while hovered.

- **Classes:** starter items and the ability.
- **Crates:** contents and odds, and OPEN.
- **Skins:** a big preview, and EQUIP.
- **Items:** what they include.

### Gifting

A gift button on Robux crate and item cards, and GIFT on their page, open `Main.GiftPicker`: the other players in the server. The server checks the item can be gifted and that the recipient doesn't own it (a once-only item, or every skin of a crate), then opens Scribe's gift prompt. Not for game passes, Coins or Tokens prices.

### Borders

An item with `Hidden = true` is left out of `ITEMS`: not shown, not sold (the Battle Pass uses it while it's off).

An item's `Border` names a `Content.Store.Store.BORDERS` preset (Gold, Rainbow, Obsidian). Its colors turn around the card. Add presets as ColorSequences.

### Lobby panel

`Main.Wallet`, on the left: the Coins chip, and STORE and INVENTORY. (The Tokens chip is hidden since 2026-11-15.)

### Classes for sale

Blake (`Hologram`): Coins only (see `CLASS_PRICES`), featured.

### Inventory borders (2026-11-13)

A skin granted by a store item with a `Border` or `Glow` (like the Obsidian Pack) gets that item's border, turning, and its sheen in the Inventory too.

### Locked classes in Siege (2026-11-13)

On the Siege class page, a locked class the player doesn't own is greyed out, says LOCKED, and is sorted to the bottom. The server still refuses it.

### Owned cards (2026-11-13)

On a Store card, an owned item shows a ✓ OWNED button (or ✓ ALL SKINS OWNED) instead of its prices, with the gift button beside it when the item can be gifted. On the detail page, it shows ✓ OWNED with its price buttons greyed and inactive. % EXTRA is a bright ribbon on the top-left edge.

### Coin buttons (2026-11-13)

Coin prices are a centered row: the coin image, then the amount (`Content.CoinIcon`, `Content.Amount`) on `StoreCard.Card.Prices.Coins`, `Main.Details.Actions.Coins` and `Main.Wallet.Coins`. Write the amount to `Amount`, not to the button's own Text.

### Inventory search (2026-11-15)

The box at the right of the Inventory's filter chips narrows the open tab to cards whose name, subtitle or lock hint holds every word typed (any case), on top of the chip. Headings become one RESULTS heading while searching; X clears it.

### Battle Pass (2026-11-16)

The store item `BattlePassS1` (Passes, 399 Robux, once, giftable) is Season 1's premium battle pass: `Grants = { BattlePass = "S1" }` (`StoreGrants.GivePremium`). Its Robux product (`Store_BattlePassS1`) isn't set up yet. See [BATTLE_PASS.md](BATTLE_PASS.md).

### Crate inventory

Bought crates wait in `CrateInventory` until opened (`Packets.Store.Open` → `StoreService.OpenCrate`). Then the reel plays (`Main.Opening`).

## Controls

| Input | How |
| --- | --- |
| Mouse / touch | STORE button on the lobby wallet bar; Store tabs and price buttons. Crates also from the Armory (shop stand prompt) |
| Gamepad | The same buttons, with the selection cursor |

## Where things are

| What | Where |
| --- | --- |
| Crates (data) | `ReplicatedStorage.Content.Crates.Crates` |
| Store items, currencies, rewards, saved fields | `ReplicatedStorage.Content.Store.Store` (tagged `ScribeFragment`) |
| Product and pass ids | `Shared.ProductIds`: `Crate_<crateId>`, `Store_<itemId>`, `GamePasses.<itemId>` |
| Robux products and passes declared | `Shared.Data` (built from the two Content modules) |
| What a purchase gives | `Shared.StoreGrants` |
| Selling, currency, perks, class ownership | `ServerScriptService.Modules.Systems.Store.StoreService` |
| Results, rewards, streaks, play coins | `Systems.Store.StatsService` |
| Store screen, wallet bar, reward toast | `Client.Core.Store` → `Main.Store`, `Main.Wallet`, `Main.RewardToast` |
| Armory crates and the reel | `Client.Core.SkinShop` → `Main.SkinShop` |
| PLAY starts on the last mode | `Client.Core.ModeMenu` |
| Templates | `StoreItem`, `StoreTab`, `CrateTab`, `StreakTag` in `Assets.UI.Templates` |

## How it works

- **Robux:** `StoreService.Buy` opens the product's prompt (Scribe's `PromptPurchase`) or the game pass prompt. The receipt runs the product's Grant in `Shared.Data`:
  - a crate gives a random skin the player doesn't own and equips it;
  - an item applies its `Grants`.
  A Robux crate's skin shows up in the player's data, and the Armory plays the reel for it.
- **Coins and Tokens:** Scribe's `Data.Purchase` takes the price and gives the item in one transaction. For a crate, the skin is picked inside it and sent back, and the reel lands on that skin.
- **Refusals:**
  - an unknown item, or no price in that currency;
  - a product or pass id still 0 (shows SOON);
  - not enough currency, or the rate limit;
  - a once-only item already owned (skins, classes, passes, items marked `Once`);
  - a crate the player owns every skin of.
- **Results:** `StatsService` listens to `Match.Ended` (Siege ends through `MatchService.Finish`). Each player with a `Team` attribute:
  - gets a win or a loss;
  - their mode's streak goes up or back to 0;
  - `LastMode` is saved, and coins are paid.
  A match with no winner pays the draw coins and records nothing.
- **Classes:** a class Id in `Content.Store.Store.LOCKED_CLASSES` must be owned (`OwnedClasses`) to be picked in Siege. `SiegeService` asks `StoreService.OwnsClass`, both for a pick and for the random class given at the end of Selection. None is locked now.

## API and extension points

| Call | What |
| --- | --- |
| `StoreService.Buy(player, "Crate:<id>" or "Item:<id>", "Robux"/"Coins")` | (ok, message, skinId) |
| `StoreService.Give(player, "Coins", amount, reason)` | Pays out Coins and shows it to the player |
| `StoreService.Perk(player, "CoinMultiplier")` | Product of that perk over owned passes (1 if none) |
| `StoreService.OwnsClass(player, classId)` / `OwnsPass(player, itemId)` | |
| `StatsService.Record(player, modeId, categoryId, won)` | Records one result; returns the mode streak |
| `Crates.Pick(crate, owns, roll?)` / `Crates.Chances(crate, owns)` | Weighted pick / chances among unowned skins |
| `Client.Core.Store.Open(sectionId?)` | Opens the Store |
| `Client.Core.SkinShop.ShowOpening(skinId, crateId?)` / `ExpectCrate(crateId)` | Plays the reel / waits for a Robux crate's skin |

| Packet | Direction | Arguments |
| --- | --- | --- |
| `Store.Buy` | Client → server, answered (ok, message, skinId) | key, currency |
| `Store.Reward` | Server → one client | amount, currency, reason |

| Extension point | Kind | Arguments |
| --- | --- | --- |
| `Store.PreventBuy` | Any | player, key, currency |
| `Store.Bought` | Fire | player, key, currency, skinId? |
| `Store.Given` | Fire | player, currency, amount, reason |
| `Stats.Recorded` | Fire | player, modeId, categoryId, won, streak |

Saved fields (from `Content.Store.Store`):

- `Tokens`, `OwnedClasses`, `OwnedItems` (once-only items bought, 2026-11-13), `Wins`, `Losses`, `LastMode`.
- `Stats["Mode:<id>"]` and `Stats["Category:<id>"]`: `Wins`, `Losses`, `Streak`, `BestStreak`.

Player attributes: `WinStreak`, and `TotalWins` (saved `Wins`, for the lobby leaderboard; 2026-11-13).

## How to add more

- **A crate:** add a ModuleScript to `Content.Crates.Definitions` (copy one, change its `Id` and `Order`):
  - `Skins` maps skin Ids to weights;
  - set `Coins`, and `Robux` for the price shown;
  - for Robux, create a developer product and put its id at `Crate_<Id>` in `Shared.ProductIds`.
- **A store item:** add a ModuleScript to `Content.Store.Definitions` (copy one, change its `Id` and `Order`), with a `Section` and prices. Ribbon and coin colors come from `Content.Store.Style`. `Grants` takes Coins, Skins and Classes. For Robux, put the product id at `Store_<Id>`.
- **A game pass:** an item with `Pass = true` and `Perks`. Put the pass id at `GamePasses.<Id>`.
- **A special skin:** add the skin to `Content.Guns.Skins.Skins` (in no crate), and an item in the `Skins` section that grants it.
- **A class for sale:**
  - add `[classId] = true` to `LOCKED_CLASSES`;
  - add an item in the `Classes` section with `Grants = { Classes = { classId } }`.
  - Locking a class takes it away from everyone who doesn't own it.
- **Battle pass or quests:** call `StoreService.Give(player, "Coins", n, "Battle pass")`.

## Testing

Checked on 2026-11-13 in a Studio playtest, on the server (no screens, as asked):

- A new player's `Tokens` was 5.
- `Give` added coins.
- Buying:
  - The Field Crate with coins was refused for a player who owns all its skins ("You already own every skin in that crate").
  - Obsidian with 5 tokens was refused (needs 30).
  - The Tokens50 pack for Robux was refused while its id is 0 ("isn't for sale yet").
  - The coins pack with coins was refused (no coin price).
- Stats:
  - Two wins put the `5v5` and `Siege` wins at 2, the streak at 2, the 🔥 2 tag on the head and `LastMode` at `5v5`.
  - A loss reset the streak to 0, kept the best at 2 and removed the tag.
- Console clean.
- The test's coins and stats were taken back off the profile afterwards (Studio saves to the real DataStore).

`Crates.Pick` was checked in Edit mode:

- Weights 3 / 2 / 1 gave 2,938 / 2,002 / 1,060 of 6,000 picks.
- An owned skin never comes up.
- A crate fully owned gives nil.

**Not checked:**

- The Store screen, the wallet bar, the reward toast and the reel on screen.
- A real Robux purchase or game pass.
- A coin crate purchase that gives a skin.
- The PLAY button picking the last mode.
- Rewards at the end of a real match.
- Phone and gamepad.

## Limits

- Robux items show SOON until their product or pass id is put in `Shared.ProductIds`.
- Every product and the VIP pass exist (created 2026-11-13 through Open Cloud, each with a placeholder colored icon; replace the icons on the Creator Dashboard).

| Name in `Shared.ProductIds` | Id | Price |
| --- | --- | --- |
| `Crate_Field` (also `SkinCrate`) | 3730208338 | 499 (crate removed 2026-11-17: commented out, not sold in game) |
| `Crate_Gilded` | 3731059935 | 299 (crate removed 2026-11-17: commented out, not sold in game) |
| `Store_NeonCircuitBundle` (was `Store_Tokens50`; reused 2026-11-15) | 3731060058 | 149 |
| `Store_Tokens150` (removed 2026-11-15) | 3731060067 | 249 |
| `Store_Tokens400` (removed 2026-11-15) | 3731060078 | 499 |
| `Store_Coins5000` | 3731060085 | 99 |
| `Store_Coins15000` | 3731060095 | 249 |
| `Store_StarterBundle` | 3731060107 | 199 |
| `Store_ObsidianRifle` | 3731060114 | 149 |
| `GamePasses.VIP` | 2089466749 | 399 |
- Owned passes and bundles show OWNED from the start (2026-11-13): passes from Scribe's pass mirror, bundles from `OwnedItems`.
- Leaving a match before it ends records nothing.
