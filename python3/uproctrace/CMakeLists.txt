add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/uproctrace_pb2.py
  DEPENDS
  ${CMAKE_SOURCE_DIR}/uproctrace.proto
  COMMAND
  protoc --proto_path ${CMAKE_SOURCE_DIR}
         --python_out ${CMAKE_CURRENT_BINARY_DIR}
         ${CMAKE_SOURCE_DIR}/uproctrace.proto
)

add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/gui_glade.py
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/gui.glade
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_header.py
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_footer.py
  COMMAND
  cat
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_header.py
  ${CMAKE_CURRENT_SOURCE_DIR}/gui.glade
  ${CMAKE_CURRENT_SOURCE_DIR}/gui_glade_footer.py
  > ${CMAKE_CURRENT_BINARY_DIR}/gui_glade.py
)

function(pyfile NAME)
  add_custom_command(
    OUTPUT
    ${CMAKE_CURRENT_BINARY_DIR}/${NAME}.py
    DEPENDS
    ${CMAKE_CURRENT_SOURCE_DIR}/${NAME}.py
    COMMAND
    cp -a ${CMAKE_CURRENT_SOURCE_DIR}/${NAME}.py
          ${CMAKE_CURRENT_BINARY_DIR}/${NAME}.py
  )
  list(APPEND PYFILES ${CMAKE_CURRENT_BINARY_DIR}/${NAME}.py)
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
  ${CMAKE_CURRENT_BINARY_DIR}/uproctrace_pb2.py
  ${CMAKE_CURRENT_BINARY_DIR}/gui_glade.py
  ${PYFILES}
)
