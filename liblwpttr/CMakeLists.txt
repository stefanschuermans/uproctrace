add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/src/lwproctrace.pb-c.c
  ${CMAKE_CURRENT_BINARY_DIR}/src/lwproctrace.pb-c.h
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/lwproctrace.proto
  COMMAND
  protoc-c --proto_path ${CMAKE_CURRENT_SOURCE_DIR}
           --c_out ${CMAKE_CURRENT_BINARY_DIR}/src
           lwproctrace.proto
)

add_library(
  lwpttr
  STATIC
  include/liblwpttr/event.h
  src/cleaner.c
  src/cleaner.h
  src/event.c
  src/macros.h
  src/symlink.c
  src/symlink.h
  src/timestamp.c
  src/timestamp.h
  ${CMAKE_CURRENT_BINARY_DIR}/src/lwproctrace.pb-c.c
  ${CMAKE_CURRENT_BINARY_DIR}/src/lwproctrace.pb-c.h
)

target_include_directories(
  lwpttr
  PUBLIC
  include
  PRIVATE
  ${CMAKE_CURRENT_BINARY_DIR}/src
)

target_link_libraries(
  lwpttr
  PUBLIC
  -lprotobuf-c
)
