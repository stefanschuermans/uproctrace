set(
  PYTHON_UPT_DIR
  ${CMAKE_BINARY_DIR}/lib/python3/dist-packages/uproctrace
)

add_custom_command(
  OUTPUT
  ${PYTHON_UPT_DIR}/uproctrace_pb2.py
  DEPENDS
  ${CMAKE_SOURCE_DIR}/uproctrace.proto
  COMMAND
  protoc --proto_path ${CMAKE_SOURCE_DIR}
         --python_out ${PYTHON_UPT_DIR}
         ${CMAKE_SOURCE_DIR}/uproctrace.proto
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
