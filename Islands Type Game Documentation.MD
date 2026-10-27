# Kits, Abilities, Items, Effects, Blocks & Matches

A data-driven framework for kits, abilities, items, effects, block building and Bedwars-style matches in a Roblox game.

- **Definitions:** kits, items and blocks are plain definition modules. Abilities are small server modules with optional client specs. Effects are entries in one registry.
- **Kit state:** all player kit state lives in a shared [Scribe](https://scribe.ericplane.dev/) store. The server writes it and the client reads it.
- **Inventory:** every player has 36 slots, the first 9 are the hotbar. One server API (`ItemService`) gives, takes and moves items; the client only asks.
- **HUD:** the HUD builds itself from the definitions, so adding content never requires editing HUD code.
- **Effects:** the server never creates sounds or visuals. It sends an effect name, and every client plays it.
- **Blocks:** Bedwars-style building on a 3-stud grid. The server owns every block; clients only ask, then predict so building feels instant.
- **Matches:** a drop-in match system (`ReplicatedStorage.Match`): lobby, sky platform, teams, beds, generators, an item shop, team upgrades, kill feed, tab list and timed or random events.
- **Admin commands:** Cmdr commands to give items, kits and abilities and move teams, plus a `/shop` chat command.

---

## Table of Contents

- [Overview](#overview)
- [Project Layout](#project-layout)
- [Core Concepts](#core-concepts)
  - [Kits](#kits)
  - [Items](#items)
  - [Abilities](#abilities)
  - [Kit State](#kit-state)
  - [Effects](#effects)
  - [Blocks](#blocks)
  - [Matches](#matches)
- [Guides](#guides)
  - [Adding a Kit](#adding-a-kit)
  - [Adding an Item](#adding-an-item)
  - [Adding an Ability](#adding-an-ability)
  - [Adding an Effect](#adding-an-effect)
  - [Adding a Block](#adding-a-block)
  - [Adding a Special Block](#adding-a-special-block)
  - [Adding a Shop Entry](#adding-a-shop-entry)
  - [Adding a Team Upgrade](#adding-a-team-upgrade)
  - [Adding a Mode, Team, Event or Currency](#adding-a-mode-team-event-or-currency)
  - [Custom UI](#custom-ui)
  - [Setting a Player's Kits](#setting-a-players-kits)
- [Inventory & Hotbar](#inventory--hotbar)
- [Effects & Sound](#effects--sound)
  - [Effect Registry](#effect-registry)
  - [Playing Effects](#playing-effects)
  - [Replication](#replication)
  - [Sound Groups](#sound-groups)
  - [Volume Settings](#volume-settings)
  - [Writing a New Visual Kind](#writing-a-new-visual-kind)
- [Blocks & Building](#blocks--building)
  - [The Grid](#the-grid)
  - [Block Definitions](#block-definitions)
  - [Tool Types & Breaking](#tool-types--breaking)
  - [Placing](#placing)
  - [Map Blocks](#map-blocks)
  - [Block Hooks](#block-hooks)
  - [Generators, Beds & Shop Keepers](#generators-beds--shop-keepers)
  - [How a Request Flows](#how-a-request-flows)
  - [Grid Settings](#grid-settings)
- [Matches](#matches-1)
  - [Dropping It Into a Place](#dropping-it-into-a-place)
  - [Lifecycle](#lifecycle)
  - [Bedwars Rules](#bedwars-rules)
  - [Deaths & Kill Credit](#deaths--kill-credit)
  - [The Item Shop](#the-item-shop)
  - [Team Upgrades](#team-upgrades)
  - [Events](#events)
