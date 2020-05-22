#! /bin/bash

set -eux -o pipefail

if (( $# < 1 ))
then
  echo "usage: $0 <SOURCE_DIR>" >&2
  exit 2
fi
SOURCE_DIR="$(readlink -f "$1")"


mkdir build
cd build
cmake -G Ninja -D CMAKE_BUILD_TYPE=Release "$SOURCE_DIR"
ninja
