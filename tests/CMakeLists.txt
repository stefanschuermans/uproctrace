add_test(
  NAME
  first
  COMMAND
  bash -c
  "
    > out.proto
    LWPTPL_OUTPUT=out.proto \
    LD_PRELOAD=${CMAKE_BINARY_DIR}/liblwptpl/liblwptpl.so \
    /bin/true
    ls -l out.proto
    protoc --proto_path ${CMAKE_SOURCE_DIR}/liblwpttr lwproctrace.proto \
           --decode lwproctrace.event < out.proto
  "
)
