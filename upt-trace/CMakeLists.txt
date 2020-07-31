add_custom_command(
  OUTPUT
  ${CMAKE_BINARY_DIR}/bin/upt-trace
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/upt-trace.bash
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/upt-trace.bash
        ${CMAKE_BINARY_DIR}/bin/upt-trace
)

add_custom_target(
  upt-trace
  ALL
  DEPENDS
  ${CMAKE_BINARY_DIR}/bin/upt-trace
)

install(
  PROGRAMS
  ${CMAKE_BINARY_DIR}/bin/upt-trace
  DESTINATION
  bin
)
