#!/bin/bash
# Symlink system Chromium/Chrome and ChromeDriver into project paths.
# No download, no third-party; uses only system binaries.
# Run from lesson_17_frames: ./link_browser_and_driver.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

BIN_DIR="$SCRIPT_DIR/bin"
DRIVER_DIR="$SCRIPT_DIR/driver"
mkdir -p "$BIN_DIR" "$DRIVER_DIR"

# Find browser (chromium or google-chrome)
BROWSER=""
for candidate in /usr/bin/chromium-browser /usr/bin/chromium /usr/bin/google-chrome /usr/bin/google-chrome-stable /snap/bin/chromium; do
  if [ -x "$candidate" ]; then
    BROWSER="$candidate"
    break
  fi
done
if [ -z "$BROWSER" ]; then
  BROWSER="$(command -v chromium-browser 2>/dev/null)" || true
  [ -z "$BROWSER" ] && BROWSER="$(command -v chromium 2>/dev/null)" || true
  [ -z "$BROWSER" ] && BROWSER="$(command -v google-chrome 2>/dev/null)" || true
fi

# Find chromedriver (system driver only)
DRIVER=""
for candidate in /usr/bin/chromedriver /usr/lib/chromium/chromedriver; do
  if [ -x "$candidate" ]; then
    DRIVER="$candidate"
    break
  fi
done
if [ -z "$DRIVER" ]; then
  DRIVER="$(command -v chromedriver 2>/dev/null)" || true
fi

LINKED=0

if [ -n "$BROWSER" ]; then
  # Link as 'chromium' so conftest finds bin/chromium
  ln -sf "$BROWSER" "$BIN_DIR/chromium"
  echo "Linked browser: $BROWSER -> $BIN_DIR/chromium"
  LINKED=1
else
  echo "No system Chromium/Chrome found. Install chromium-browser or google-chrome."
fi

if [ -n "$DRIVER" ]; then
  ln -sf "$DRIVER" "$DRIVER_DIR/chromedriver"
  echo "Linked driver: $DRIVER -> $DRIVER_DIR/chromedriver"
  LINKED=1
else
  echo "No system chromedriver found. Tests will use Selenium Manager if no project driver."
fi

if [ "$LINKED" -eq 1 ]; then
  echo "Done. Project will use these paths when running tests."
else
  echo "Nothing linked. Install Chromium and/or ChromeDriver, or run again after installing."
  exit 1
fi
