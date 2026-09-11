#!/bin/bash
# Tek bir kitapçık sayfasını (sayfalar/sayfa-XX-*.html) PNG'ye render eder.
# Kullanım: scripts/render-page.sh sayfa-01-kapak
set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
NAME="$1"
SRC="$PROJECT_ROOT/docs/kitapcik-hazirlik/sayfalar/$NAME.html"
OUT="$PROJECT_ROOT/docs/kitapcik-hazirlik/ornek-tasarimlar/$NAME.png"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

if [ ! -f "$SRC" ]; then
  echo "Bulunamadı: $SRC"
  exit 1
fi

"$CHROME" --headless --disable-gpu --hide-scrollbars \
  --window-size=1240,1754 \
  --screenshot="$OUT" \
  --default-background-color=FFFFFFFF \
  --virtual-time-budget=3000 \
  "file://$SRC" 2>/dev/null

echo "Yazıldı: $OUT"
