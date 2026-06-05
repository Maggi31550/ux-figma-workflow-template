#!/usr/bin/env bash
# nlm.sh — NotebookLM helper wrapper
# Usage: ./scripts/nlm.sh <command> [args...]
# Always uses the notebooklm-py venv from ~/Desktop/notebooklm-py

NLM="/Users/socket9/Desktop/notebooklm-py/.venv/bin/notebooklm"

if [ ! -f "$NLM" ]; then
  echo "ERROR: notebooklm-py not found at $NLM"
  exit 1
fi

exec "$NLM" "$@"
