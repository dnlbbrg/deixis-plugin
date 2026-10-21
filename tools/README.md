# tools

Scripts that generate the images in `assets/`. The SVGs are generated files: edit the scripts, not the SVGs. Run everything from the repository root on a Mac with Python 3 and Google Chrome (set `CHROME` to use another Chromium binary).

| Script | What it does |
|---|---|
| `banner.py` | Writes `assets/banner-light.svg` and `assets/banner-dark.svg`, the animated README banner (880 x 520, one 8 s CSS loop). |
| `flow.py` | Writes `assets/flow-1-light.svg` to `assets/flow-3-dark.svg`, one 560 x 288 image per step of the README. |
| `social.py` | Writes `assets/social-preview.svg`, the 1280 x 640 GitHub social preview, the still frame of the banner scaled to full height. |
| `social.sh` | Runs `social.py` and renders `assets/social-preview.png` with headless Chrome. |
| `frames.sh` | Screenshots an animated SVG at given times, for checking single frames. |
| `preview.sh` | Renders `README.md` through the GitHub markdown API (needs `gh`) and screenshots it in light and dark. |

```sh
python3 tools/banner.py
python3 tools/flow.py
tools/social.sh
tools/frames.sh assets/banner-light.svg /tmp/frames 880 520 1000 3800 7400
tools/preview.sh /tmp/readme-preview
```

After running the generators, `git status` should show no change to `assets/` unless a script was edited.

All images are laid out on an 8 px grid. Text is at least 14 px in the banner and 20 px in the step images, so it stays legible in GitHub's 830 px column.

Text inside the SVGs uses no symbol that a platform could swap for a colour emoji: check marks and the asterisk are drawn as paths.
