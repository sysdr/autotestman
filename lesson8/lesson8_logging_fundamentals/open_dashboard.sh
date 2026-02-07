#!/bin/bash
# Alternative: Open dashboard directly in browser (no server needed)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HTML_FILE="$SCRIPT_DIR/logging_comparison.html"

if [ -f "$HTML_FILE" ]; then
    echo "Opening dashboard: $HTML_FILE"
    
    # Try different methods to open the file
    if command -v xdg-open &> /dev/null; then
        xdg-open "$HTML_FILE"
    elif command -v wslview &> /dev/null; then
        wslview "$HTML_FILE"
    elif command -v explorer.exe &> /dev/null; then
        explorer.exe "$HTML_FILE"
    else
        echo "Could not find a way to open the file automatically."
        echo "Please open this file manually:"
        echo "$HTML_FILE"
    fi
else
    echo "Error: Dashboard file not found at $HTML_FILE"
    exit 1
fi
