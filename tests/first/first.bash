#! /bin/bash

set -eux -o pipefail

if (( $# < 1 ))
then
  echo "usage: $0 <UPT_HOME>" >&2
  exit 2
fi
UPT_HOME="$1"

SCRIPT_DIR="$(dirname "$0")"

source "$UPT_HOME/exports"

rm -rf out.proto

upt-trace out.proto "$SCRIPT_DIR/traceme.bash"

ls -l out.proto

upt-tool out.proto dump | tee out.dump
grep '^ *event *{ *$' out.dump | wc -l | tee out.event_cnt
grep '^6$' out.event_cnt

upt-tool out.proto parse
