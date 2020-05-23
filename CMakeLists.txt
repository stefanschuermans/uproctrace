cmake_minimum_required(VERSION 3.10)
project(uproctrace)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -fPIC")

enable_testing()

add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/exports
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/exports
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/exports ${CMAKE_CURRENT_BINARY_DIR}/exports
)

add_custom_target(
  copy_exports
  ALL
  DEPENDS
  exports
)

add_subdirectory(libuptev)
add_subdirectory(libuptpl)
add_subdirectory(python3)
add_subdirectory(upt-gui)
add_subdirectory(upt-tool)
add_subdirectory(upt-trace)
add_subdirectory(tests)
