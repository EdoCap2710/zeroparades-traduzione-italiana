#!/usr/bin/env bash
# Rimette i file originali del gioco dal backup creato dall'installer.
cd "$(dirname "$(readlink -f "$0")")"
exec ./installa.sh --ripristina "$@"
