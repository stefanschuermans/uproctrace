#! /bin/bash

UPT_HOME="$(readlink -f "$(dirname "$0")/..")"

export PYTHONPATH="$UPT_HOME/python3${PYTHONPATH:+:${PYTHONPATH}}"

exec "$UPT_HOME/lib/uproctrace/upt-tool.py" "$@"
