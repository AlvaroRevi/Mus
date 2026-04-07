#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PYTHON="$PROJECT_ROOT/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "No se encontro Python del entorno virtual en $VENV_PYTHON" >&2
  exit 1
fi

if [[ "${1:-}" == "--clean" ]]; then
  rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist"
fi

cd "$PROJECT_ROOT"

"$VENV_PYTHON" -m PyInstaller \
  --noconfirm \
  --windowed \
  --name MusSimulator \
  --paths "$PROJECT_ROOT" \
  --paths "$PROJECT_ROOT/src" \
  --add-data "$PROJECT_ROOT/card_images:card_images" \
  src/main.py

APP_CARD_DIR="$PROJECT_ROOT/dist/MusSimulator.app/Contents/MacOS/card_images"
EXTERNAL_CARD_DIR="$PROJECT_ROOT/dist/card_images"

if [[ -d "$PROJECT_ROOT/card_images" ]]; then
  rm -rf "$EXTERNAL_CARD_DIR"
  cp -R "$PROJECT_ROOT/card_images" "$EXTERNAL_CARD_DIR"
fi

echo
echo "Build completada."
echo "App:    $PROJECT_ROOT/dist/MusSimulator.app"
echo "Cartas: $EXTERNAL_CARD_DIR"
