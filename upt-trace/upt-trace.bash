#! /bin/bash

if (( $# < 2 ))
then
  echo "usage: $0 <trace.upt> <command> [<arg> [...]]" >&2
  exit 2
fi
TRACE_FILE="$1"
shift

UPT_HOME="$(readlink -f "$(dirname "$(dirname "$0")")")"

touch "$TRACE_FILE"
export UPTPL_OUTPUT="$(readlink -f "$TRACE_FILE")"
export LD_PRELOAD="$UPT_HOME/lib/uproctrace/libuptpl.so"

exec "$@"
