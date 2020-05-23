#! /bin/bash

set -eux -o pipefail

if (( $# < 2 ))
then
  echo "usage: $0 <SOURCE_DIR> <UPT_HOME>" >&2
  exit 2
fi
SOURCE_DIR="$(readlink -f "$1")"
UPT_HOME="$(readlink -f "$2")"

SCRIPT_DIR="$(dirname "$0")"

source "$UPT_HOME/exports"

rm -rf out.proto build

upt-trace out.proto "$SCRIPT_DIR/run_build.bash" "$SOURCE_DIR"

ls -l out.proto

upt-tool out.proto dump | tee out.dump
grep -A 1 '^ *cmdline {$' out.dump | grep '^ *s: "mkdir"$'
grep '^ *s: "proc_begin.c"$' out.dump
grep '^ *s: "libuptpl.so"$' out.dump

upt-tool out.proto parse
