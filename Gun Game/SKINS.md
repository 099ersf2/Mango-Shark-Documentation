# Weapon skins and the skin shop

A skin restyles one gun's model: new colors and materials, a few resized parts, and a few small detail parts welded on. Stats never change. Players get skins from a Robux **skin crate** in the lobby shop and equip them there.

The server owns every skin. The shop only asks; `SkinShopService` checks and writes the player's data.

## Where things are

| What | Where |
| --- | --- |
| Skins (data, shared) | `ReplicatedStorage.Content.Guns.Skins` |
| Server | `ServerScriptService.Modules.Systems.SkinShopService` |
| Shop (client) | `ReplicatedStorage.Modules.Client.Core.SkinShop` (`ClientOnly`) |
| Packets | `Shared.Packets.Skins.Equip`, `Shared.Packets.Skins.BuyCrate` |
| Saved data | `Shared.Data`: `WeaponSkins`, `RifleSkin`, `PistolSkin`, and the `SkinCrate` product |
| UI | `StarterGui.Main.SkinShop` (the panel), `Main.SkinShopButton`, `Assets.UI.Templates.SkinRow` (one row per skin) |
| Spawn styling | `Systems.Guns.LoadoutService` calls `SkinShopService.StyleTool` for each gun it gives |
| First-person styling | `Client.Guns.Viewmodel` (reads the `RifleSkin` / `PistolSkin` Player attributes) |

## How it works

1. **Owning.** `WeaponSkins` (a saved set of skin Ids) is what the player owns. Only the `SkinCrate` product's `Grant` adds to it.
2. **Equipping.** Each gun with a skin has a saved field `<Gun>Skin` (`RifleSkin`, `PistolSkin`): `"None"` or a skin Id. `Shared.Data` builds these fields from `Content.Guns.Skins`, so the allowed values always match the list.
3. **Showing it.** `SkinShopService` copies each `<Gun>Skin` field to the Player attribute of the same name, and restyles the player's gun Tools whenever a field changes. Other players see the styled Tool. The player's own first-person viewmodel is styled by `Viewmodel` from the attribute.
4. **The shop.** Walk up to the shop stand in the lobby (`Workspace.Lobby.SkinShopStand`) and use its prompt (Interact, E). Any `ProximityPrompt` tagged `SkinShopPrompt` opens the shop, only while in the lobby; leaving the lobby closes it. There is no key. Each row shows **Equip** / **Equipped** for an owned skin, or **In crate**. Clicking **Equip** on the equipped skin takes it off.
5. **The crate.** One random skin the player doesn't own yet, equipped at once. The odds line shows the chance for each skin left (equal odds; owned skins are never rolled). Once every skin is owned, the Buy button is off and the server refuses the prompt. If every skin is already owned when a purchase is granted anyway, the player gets `Skins.CRATE_REFUND_COINS` (500) coins instead.

### Server checks

Every `Packets.Skins` request is refused unless:

- the player is in the lobby (`InLobby`, see [LOBBY.md](LOBBY.md));
- their data has loaded;
- they are under the rate limit (4 requests per 2 seconds, `TokenBucket`).

`Equip` also needs a skin Id the player owns (unknown or over-long Ids are refused). `BuyCrate` also needs the product to be declared, at least one skin left, and Scribe's product state to be `purchasable` (it is not for accounts where paid random items are restricted). Both packets answer `(ok, message)`, and the shop shows the message.

## Setting up the crate product

The crate is off until it has a developer product:

1. Create a developer product named "Skin Crate", priced like `Skins.CRATE_PRICE` (**499 Robux**), on the Creator Dashboard (the experience > Monetization > Developer Products). Claude can create it through Open Cloud once the Studio connection has the `developer-product:write` permission.
2. In Studio, set the number attribute `SkinCrateProductId` on `ReplicatedStorage` to the product's id.

`Shared.Data` reads the attribute **once, when the server starts**, and only then declares the `SkinCrate` product, so set it in Studio before publishing. Changing it while a server runs does nothing until a new server starts. The product is marked `PaidRandom`, so Scribe refuses it for players whose policy restricts paid random items.

## Adding a skin

Add an entry to `Skins.List` in `Content.Guns.Skins`:

```lua
{
	Id = "GoldPistol",            -- saved in player data; never rename one that has shipped
	Name = "Gold Pistol",         -- shown in the shop
	WeaponId = "Pistol",          -- a gun Id in Content.Guns.Registry
	Description = "Solid gold.",  -- one line for the shop
	Swatch = Color3.fromRGB(212, 175, 55),
	Base = { Color = Color3.fromRGB(212, 175, 55), Material = Enum.Material.Metal },  -- every part
	Parts = {                     -- optional; first matching name pattern wins, on top of Base
		{ Match = "^Slide$", Style = { Color = Color3.fromRGB(240, 220, 120) } },
	},
	Details = {                   -- optional; welded to the Handle
		{ Class = "Part", Size = Vector3.new(0.1, 0.1, 0.4), Offset = CFrame.new(0, 0.4, -0.3), Color = Color3.new(1, 1, 1), Material = Enum.Material.Neon },
	},
},
```

- A skin for a gun that already has skins needs nothing else: its saved field takes the new Id, the shop shows a row, and the crate can roll it.
- A skin for a **new** gun also gets a new saved field (`<Gun>Skin`) automatically. `Viewmodel` already reads `<GunId>Skin` for any gun.
- The crate's odds are equal across unowned skins. `WeaponSkins` holds at most as many Ids as `Skins.List` has.

## API

```lua
local Skins = require(ReplicatedStorage.Content.Guns.Skins)
Skins.Get(id)              -- the skin, or nil
Skins.ForWeapon("Rifle")   -- skins for one gun
Skins.Weapons()            -- gun Ids that have skins
Skins.Choices("Rifle")     -- { "None", "AK47" }
Skins.EquipField("Rifle")  -- "RifleSkin"
Skins.Apply(model, id, gunId)  -- style a model; "None" puts it back

-- Server
SkinShopService.StyleTool(player, tool)  -- style a gun Tool with the player's equipped skin
```

`Skins.Apply` remembers each part's original look the first time it sees it, so it can be called again or with `"None"` safely.

## Limits

- A gun given outside `LoadoutService` (for example `givegun`) isn't styled for other players until the player's equipped skin changes. The first-person view is always right.
- The crate is the only way to get a skin. There's no gifting or coin price.
