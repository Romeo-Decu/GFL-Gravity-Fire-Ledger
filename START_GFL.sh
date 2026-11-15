#!/bin/sh
# Gravity Fire Ledger: starts the dashboard on this computer (macOS, Linux). Needs Python 3.10 or later. Nothing is installed.
cd "$(dirname "$0")" || exit 1
URL=http://localhost:8137/visualization/gfl.html
echo "Gravity Fire Ledger is starting at $URL (Ctrl+C stops it)"
(sleep 1; (command -v xdg-open >/dev/null && xdg-open "$URL") || (command -v open >/dev/null && open "$URL")) >/dev/null 2>&1 &
exec python3 -m http.server 8137 --bind 127.0.0.1
