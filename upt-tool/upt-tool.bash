#! /bin/bash

UPT_HOME="$(readlink -f "$(dirname "$0")/..")"

export PYTHONPATH="$UPT_HOME/lib/python3/dist-packages${PYTHONPATH:+:${PYTHONPATH}}"

exec "$UPT_HOME/lib/uproctrace/upt-tool.py" "$@"
