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

rm -rf forkapp.upt

upt-trace forkapp.upt "$UPT_HOME/tests/fork/forkapp"

upt-tool forkapp.upt pstree | tee forkapp.pstree

sed -e "s%__UPT_HOME__%$UPT_HOME%" "$SCRIPT_DIR/forkapp.pstree_ref" \
  >forkapp.pstree_ref
diff -u forkapp.pstree forkapp.pstree_ref
