#!/usr/bin/env sh
exec "${PYTHON:-python3}"  "$(dirname "$(realpath "$0")")/main.py" "$@"