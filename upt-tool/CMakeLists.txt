add_custom_command(
  OUTPUT
  ${CMAKE_BINARY_DIR}/lib/uproctrace/upt-tool.py
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/upt-tool.py
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/upt-tool.py
        ${CMAKE_BINARY_DIR}/lib/uproctrace/upt-tool.py
)

add_custom_command(
  OUTPUT
  ${CMAKE_BINARY_DIR}/bin/upt-tool
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/upt-tool.bash
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/upt-tool.bash
        ${CMAKE_BINARY_DIR}/bin/upt-tool
)

add_custom_target(
  upt-tool
  ALL
  DEPENDS
  ${CMAKE_BINARY_DIR}/lib/uproctrace/upt-tool.py
  ${CMAKE_BINARY_DIR}/bin/upt-tool
)
