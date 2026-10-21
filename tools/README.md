# tools

Scripts that generate the images in `assets/`. The SVGs are generated files: edit the scripts, not the SVGs. Run everything from the repository root on a Mac with Python 3 and Google Chrome (set `CHROME` to use another Chromium binary).

| Script | What it does |
|---|---|
| `banner.py` | Writes `assets/banner-light.svg` and `assets/banner-dark.svg`, the animated README banner (one 8 s CSS loop). |
| `flow.py` | Writes `assets/flow-light.svg` and `assets/flow-dark.svg`, the three-step diagram. |
| `social.py` | Writes `assets/social-preview.svg`, the 1280 x 640 GitHub social preview, from the still frame of the banner. |
| `social.sh` | Runs `social.py` and renders `assets/social-preview.png` with headless Chrome. |
| `frames.sh` | Screenshots an animated SVG at given times, for checking single frames. |
| `preview.sh` | Renders `README.md` through the GitHub markdown API (needs `gh`) and screenshots it in light and dark. |

```sh
python3 tools/banner.py
python3 tools/flow.py
tools/social.sh
tools/frames.sh assets/banner-light.svg /tmp/frames 1280 400 0 2000 7000
tools/preview.sh /tmp/readme-preview
```

After running the generators, `git status` should show no change to `assets/` unless a script was edited.

Text inside the SVGs uses no symbol that a platform could swap for a colour emoji: check marks and the asterisk are drawn as paths.
