add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/upt-gui.glade
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/upt-gui.glade
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/upt-gui.glade
        ${CMAKE_CURRENT_BINARY_DIR}/upt-gui.glade
)

add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/upt-gui.py
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/upt-gui.py
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/upt-gui.py
        ${CMAKE_CURRENT_BINARY_DIR}/upt-gui.py
)

add_custom_target(
  upt-gui
  ALL
  DEPENDS
  ${CMAKE_CURRENT_BINARY_DIR}/upt-gui.glade
  ${CMAKE_CURRENT_BINARY_DIR}/upt-gui.py
)
