add_custom_command(
  OUTPUT
  ${CMAKE_BINARY_DIR}/bin/upt-dump
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/upt-dump.py
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/upt-dump.py
        ${CMAKE_BINARY_DIR}/bin/upt-dump
)

add_custom_target(
  upt-dump
  ALL
  DEPENDS
  ${CMAKE_BINARY_DIR}/bin/upt-dump
)
