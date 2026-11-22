# Gun Game documentation

## Read the docs

Start with the [documentation index](Gun%20Game/index.md), or open the [API reference](Gun%20Game/API.md).

**Website status:** The docs site is not published yet. Until GitHub Pages is enabled, use the Markdown guides linked from the index above.

## For maintainers

### Preview locally

Install the docs dependencies, then run the local preview server:

```sh
python -m pip install -r requirements-docs.txt
mkdocs serve
```

### Publish the site

Before merging docs-site changes, enable **Settings → Pages → Build and deployment → Source: GitHub Actions**. The workflow then publishes the site on pushes to `main` at `https://099ersf2.github.io/Mango-Shark-Documentation/`.
