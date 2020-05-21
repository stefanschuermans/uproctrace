add_test(
  NAME
  first
  COMMAND
  bash -c
  "
    set -eux -o pipefail
    > out.proto
    (
      export UPTPL_OUTPUT=out.proto
      export LD_PRELOAD=${CMAKE_BINARY_DIR}/libuptpl/libuptpl.so
      /bin/true a b 'c d'
      /usr/bin/printf '' e f 'g h'
    )
    ls -l out.proto
    ${CMAKE_BINARY_DIR}/dump/dump.py out.proto | tee out.dump
    grep '^ *event *{ *$' out.dump | wc -l | grep '^4$'
  "
)
