add_test(
  NAME
  first
  COMMAND
  bash -c
  "
    > out.proto
    (
      export LWPTPL_OUTPUT=out.proto
      export LD_PRELOAD=${CMAKE_BINARY_DIR}/liblwptpl/liblwptpl.so
      /bin/true a b 'c d'
      /bin/false e f 'g h'
    )
    ls -l out.proto
  "
)
