add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/uproctrace_pb2.py
  DEPENDS
  ${CMAKE_SOURCE_DIR}/uproctrace.proto
  COMMAND
  protoc --proto_path ${CMAKE_SOURCE_DIR}
         --python_out ${CMAKE_CURRENT_BINARY_DIR}
         uproctrace.proto
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

add_custom_target(
  python3_uproctrace
  ALL
  DEPENDS
  ${CMAKE_CURRENT_BINARY_DIR}/uproctrace_pb2.py
  ${PYFILES}
)
