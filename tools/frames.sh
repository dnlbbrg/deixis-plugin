#!/bin/bash
# Usage: frames.sh <svg> <outdir> <width> <height> <ms...>
# Inlines the SVG into an HTML page, freezes all CSS animations at each time and screenshots it with headless Chrome.
set -e
svg="$1"; out="$2"; w="$3"; h="$4"; shift 4
chrome="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
name="$(basename "$svg" .svg)"
mkdir -p "$out"
for ms in "$@"; do
  html="$out/$name-$ms.html"
  {
    printf '<!doctype html><html><head><style>html,body{margin:0;background:#888}</style></head><body>'
    sed '1{/^<?xml/d;}' "$svg"
    printf '<script>document.getAnimations().forEach(a=>{a.pause();a.currentTime=%s;});</script></body></html>' "$ms"
  } > "$html"
  "$chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --user-data-dir="$out/.chrome-profile" --window-size="$w,$h" --screenshot="$out/$name-$ms.png" "file://$html" >/dev/null 2>&1
  rm "$html"
done
