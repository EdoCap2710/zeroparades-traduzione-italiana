#!/usr/bin/env bash
# Traduzione italiana amatoriale di ZERO PARADES - avvio su Linux / Steam Deck.
# Uso: ./installa.sh [cartella del gioco] [--ripristina | --verifica]
# Questo script non scarica nulla: avvia soltanto installa.py.
cd "$(dirname "$(readlink -f "$0")")" || exit 1
if [ -x .venv/bin/python ]; then
  PY=.venv/bin/python
elif command -v python3 >/dev/null 2>&1; then
  PY=python3
else
  echo "Serve Python 3 (pacchetto python3 della tua distribuzione)."
  exit 1
fi
if ! "$PY" -c "import UnityPy, lz4.block" >/dev/null 2>&1; then
  echo "Manca la libreria UnityPy, che serve a leggere e riscrivere il file dei testi."
  echo "Installala una volta sola con questi due comandi, da questa cartella:"
  echo
  echo "  python3 -m venv .venv"
  echo "  .venv/bin/python -m pip install -r requisiti.txt"
  echo
  echo "Poi rilancia ./installa.sh"
  exit 1
fi
exec "$PY" installa.py "$@"
