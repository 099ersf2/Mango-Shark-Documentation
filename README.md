# Mango Shark Documentation

Internal developer documentation for Mango Shark Studio's Roblox games, game templates and drop-in systems.

- **Published site:** [099ersf2.github.io/Mango-Shark-Documentation](https://099ersf2.github.io/Mango-Shark-Documentation/)
- **Home page:** [home/index.md](home/index.md)
- **Games:** [Gun Game](Gun%20Game/index.md) ([API](Gun%20Game/api/index.md))
- **Game templates:** [game-templates/](game-templates/index.md) — the Game Template asset (`GameTemplate.rbxm`)
- **Separate systems:** [systems/](systems/index.md) — the Gun System asset (`GunSystem.rbxm`)

The site is built from the folders `home/`, `Gun Game/`, `game-templates/` and `systems/` by the MkDocs hook
`hooks/multi_root.py`. A new game gets its own top-level folder: see `game-templates/new-game-docs.md`.

## For maintainers

### Preview locally

Install the docs dependencies, then run the local preview server:

```sh
python -m pip install -r requirements-docs.txt
mkdocs serve
```

### Publish the site

GitHub Pages is configured to use **GitHub Actions**. Merging documentation changes into `main` builds and publishes the site at `https://099ersf2.github.io/Mango-Shark-Documentation/`.
