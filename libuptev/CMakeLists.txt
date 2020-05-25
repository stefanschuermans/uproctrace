add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/src/uproctrace.pb-c.c
  ${CMAKE_CURRENT_BINARY_DIR}/src/uproctrace.pb-c.h
  DEPENDS
  ${CMAKE_SOURCE_DIR}/uproctrace.proto
  COMMAND
  protoc-c --proto_path ${CMAKE_SOURCE_DIR}
           --c_out ${CMAKE_CURRENT_BINARY_DIR}/src
           ${CMAKE_SOURCE_DIR}/uproctrace.proto
)

add_library(
  uptev
  STATIC
  include/uptev/proc_begin.h
  include/uptev/proc_end.h
  src/cleaner.c
  src/cleaner.h
  src/event.c
  src/event.h
  src/macros.h
  src/proc_begin.c
  src/proc_end.c
  src/read_file.c
  src/read_file.h
  src/stringlist.c
  src/stringlist.h
  src/symlink.c
  src/symlink.h
  src/timing.c
  src/timing.h
  ${CMAKE_CURRENT_BINARY_DIR}/src/uproctrace.pb-c.c
  ${CMAKE_CURRENT_BINARY_DIR}/src/uproctrace.pb-c.h
)

target_include_directories(
  uptev
  PUBLIC
  include
  PRIVATE
  ${CMAKE_CURRENT_BINARY_DIR}/src
)

target_link_libraries(
  uptev
  PUBLIC
  -lprotobuf-c
)
