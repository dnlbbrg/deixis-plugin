#!/bin/bash
# Usage: tools/social.sh   (regenerates assets/social-preview.svg and renders assets/social-preview.png, 1280 x 640)
set -e
root="$(cd "$(dirname "$0")/.." && pwd)"
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
python3 "$root/tools/social.py"
work="$(mktemp -d)"
html="$work/social-preview.html"
{
  printf '<!doctype html><html><head><meta charset="utf-8"><style>html,body{margin:0;overflow:hidden}svg{display:block}</style></head><body>'
  sed '1{/^<?xml/d;}' "$root/assets/social-preview.svg"
  printf '</body></html>'
} > "$html"
"$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
  --user-data-dir="$work/chrome-profile" --window-size=1280,640 \
  --screenshot="$root/assets/social-preview.png" "file://$html" >/dev/null 2>&1
rm -r "$work"
echo "$root/assets/social-preview.png"
