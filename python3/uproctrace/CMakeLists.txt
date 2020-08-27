set(
  PYTHON_UPT_DIR
  ${CMAKE_BINARY_DIR}/lib/python3/dist-packages/uproctrace
)
set(
  PYTHON_UPT_INSTALL_DIR
  lib/python3/dist-packages/uproctrace
)

add_custom_command(
  OUTPUT
  ${PYTHON_UPT_DIR}/uproctrace_pb2.py
  DEPENDS
  ${PROJECT_SOURCE_DIR}/uproctrace.proto
  COMMAND
  protoc --proto_path ${PROJECT_SOURCE_DIR}
         --python_out ${PYTHON_UPT_DIR}
         ${PROJECT_SOURCE_DIR}/uproctrace.proto
)
install(
  FILES
  ${PYTHON_UPT_DIR}/uproctrace_pb2.py
  DESTINATION
  ${PYTHON_UPT_INSTALL_DIR}
)

add_custom_command(
  OUTPUT
  ${PYTHON_UPT_DIR}/gui_glade.py
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/gui.glade
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_header.py
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_footer.py
  COMMAND
  cat
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_header.py
  ${CMAKE_CURRENT_SOURCE_DIR}/gui.glade
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_footer.py
  > ${PYTHON_UPT_DIR}/gui_glade.py
)
install(
  FILES
  ${PYTHON_UPT_DIR}/gui_glade.py
  DESTINATION
  ${PYTHON_UPT_INSTALL_DIR}
)

function(pyfile NAME)
  add_custom_command(
    OUTPUT
    ${PYTHON_UPT_DIR}/${NAME}.py
    DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/${NAME}.py
    COMMAND
    cp -a ${CMAKE_CURRENT_SOURCE_DIR}/${NAME}.py
          ${PYTHON_UPT_DIR}/${NAME}.py
  )
  list(APPEND PYFILES ${PYTHON_UPT_DIR}/${NAME}.py)
  set(PYFILES ${PYFILES} PARENT_SCOPE)
  install(
    FILES
    ${PYTHON_UPT_DIR}/${NAME}.py
    DESTINATION
    ${PYTHON_UPT_INSTALL_DIR}
  )
endfunction(pyfile)

pyfile(__init__)
pyfile(dump)
pyfile(gui)
pyfile(parse)
pyfile(processes)
pyfile(tool)

add_custom_target(
  python3_uproctrace
  ALL
  DEPENDS
  ${PYTHON_UPT_DIR}/uproctrace_pb2.py
  ${PYTHON_UPT_DIR}/gui_glade.py
  ${PYFILES}
)
