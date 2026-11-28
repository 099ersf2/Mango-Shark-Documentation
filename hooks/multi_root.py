"""MkDocs hook: builds one site from several top-level folders of this repository.

`docs_dir` (home/) holds only the site's home page. Every folder in ROOTS is added as if it sat inside docs_dir, at
the same path, so `Gun Game/SIEGE.md` is served at `/Gun Game/SIEGE/` and its relative links keep working. Edit links
point at each file's real path in the repository.

To add a game or a section: make its folder at the top of the repository, add it to ROOTS, and add it to `nav` in
mkdocs.yml.
"""

import os

from mkdocs.structure.files import File

ROOTS = ["Gun Game", "game-templates", "systems"]


def on_config(config):
    repo = os.path.dirname(config["config_file_path"])
    for root in ROOTS:
        path = os.path.join(repo, root)
        if path not in config["watch"]:
            config["watch"].append(path)
    return config


def on_files(files, config):
    repo = os.path.dirname(config["config_file_path"])
    docs_dir_name = os.path.relpath(config["docs_dir"], repo).replace(os.sep, "/")
    # The home page lives in docs_dir: point its edit link at its real place in the repository
    for file in files:
        if file.src_uri.endswith(".md"):
            file.edit_uri = f"{docs_dir_name}/{file.src_uri}"
    for root in ROOTS:
        base = os.path.join(repo, root)
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
            for name in sorted(filenames):
                if name.startswith("."):
                    continue
                path = os.path.relpath(os.path.join(dirpath, name), repo).replace(os.sep, "/")
                files.append(File(path, repo, config["site_dir"], config["use_directory_urls"]))
    return files
