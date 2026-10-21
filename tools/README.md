# tools

Scripts that generate the images in `assets/`. The SVGs are generated files: edit the scripts, not the SVGs. Run everything from the repository root on a Mac with Python 3 and Google Chrome (set `CHROME` to use another Chromium binary).

| Script | What it does |
|---|---|
| `banner.py` | Writes `assets/banner-light.svg` and `assets/banner-dark.svg`, the animated README banner (880 x 568, one 8 s CSS loop). |
| `flow.py` | Writes `assets/flow-1-light.svg` to `assets/flow-3-dark.svg`, one 880 x 384 image per step of the README. |
| `social.py` | Writes `assets/social-preview.svg`, the 1280 x 640 GitHub social preview, the still frame of the banner scaled to full height. |
| `social.sh` | Runs `social.py` and renders `assets/social-preview.png` with headless Chrome. |
| `frames.sh` | Screenshots an animated SVG at given times, for checking single frames. |
| `preview.sh` | Renders `README.md` through the GitHub markdown API (needs `gh`) and screenshots it in light and dark. |

```sh
python3 tools/banner.py
python3 tools/flow.py
tools/social.sh
tools/frames.sh assets/banner-light.svg /tmp/frames 880 568 0 1000 3800 7400
tools/preview.sh /tmp/readme-preview
tools/preview.sh /tmp/readme-phone 4200 390
```

After running the generators, `git status` should show no change to `assets/` unless a script was edited.

All images are laid out on an 8 px grid and shown across GitHub's full 830 px column. Text is at least 20 px in the banner and 28 px in the step images, so it stays legible on a desktop and as far as possible on a 360 px wide phone. The banner's first frame is already a complete scene: the animation only adds pins, words and results, and pins never fade.

Text inside the SVGs uses no symbol that a platform could swap for a colour emoji: check marks and the asterisk are drawn as paths.
