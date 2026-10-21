#!/bin/bash
# Usage: tools/preview.sh <outdir> [height]   (renders README.md through the GitHub markdown API, screenshots light and dark)
set -e
root="$(cd "$(dirname "$0")/.." && pwd)"
P="${1:?outdir required}"
H="${2:-2600}"
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
mkdir -p "$P/assets"
cp "$root"/assets/*.svg "$P/assets/"
gh api markdown -f mode=gfm -f context=dnlbbrg/deixis-plugin -f text="$(cat "$root/README.md")" > "$P/body.html"
{
  printf '<!doctype html><html><head><meta charset="utf-8"><meta name="color-scheme" content="light dark">'
  printf '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown.min.css">'
  printf '<style>body{margin:0;background:#fff}@media (prefers-color-scheme:dark){body{background:#0d1117}}'
  printf '.markdown-body{box-sizing:border-box;max-width:1012px;margin:0 auto;padding:32px 45px}</style></head>'
  printf '<body><article class="markdown-body">'
  cat "$P/body.html"
  printf '</article></body></html>'
} > "$P/index.html"
"$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --user-data-dir="$P/.chrome-light" \
  --virtual-time-budget=6000 --window-size=1280,"$H" --screenshot="$P/readme-light.png" "file://$P/index.html" >/dev/null 2>&1
"$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --user-data-dir="$P/.chrome-dark" \
  --force-dark-mode --blink-settings=preferredColorScheme=0 \
  --virtual-time-budget=6000 --window-size=1280,"$H" --screenshot="$P/readme-dark.png" "file://$P/index.html" >/dev/null 2>&1
echo "$P/readme-light.png $P/readme-dark.png"
