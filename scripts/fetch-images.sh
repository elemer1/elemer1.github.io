#!/usr/bin/env bash
# Download externally-sourced images referenced by posts into assets/images/.
# Idempotent: skips files that already exist.

set -euo pipefail

cd "$(dirname "$0")/.."

mkdir -p assets/images

UA="ElemerBlog/1.0 (https://elemer.net)"

fetch() {
  local url="$1" out="$2"
  if [[ -s "$out" ]]; then
    echo "✓ $out"
    return 0
  fi
  echo "↓ $out"
  curl -sSL --fail --retry 3 --max-time 60 -A "$UA" "$url" -o "$out.tmp"
  mv "$out.tmp" "$out"
}

fetch "https://commons.wikimedia.org/wiki/Special:FilePath/NCSA_Mosaic_Browser_Screenshot.png?width=1000" \
      "assets/images/mosaic-1993.png"

fetch "https://commons.wikimedia.org/wiki/Special:FilePath/Looshaus_Michaelerplatz.JPG?width=1000" \
      "assets/images/looshaus.jpg"

fetch "https://commons.wikimedia.org/wiki/Special:FilePath/First_Web_Server.jpg?width=1000" \
      "assets/images/first-web-server.jpg"

fetch "https://commons.wikimedia.org/wiki/Special:FilePath/The_Memex_(3002477109).jpg?width=1000" \
      "assets/images/memex-1945.jpg"
