add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/lwproctrace_pb2.py
  DEPENDS
  ${CMAKE_SOURCE_DIR}/lwproctrace.proto
  COMMAND
  protoc --proto_path ${CMAKE_SOURCE_DIR}
         --python_out ${CMAKE_CURRENT_BINARY_DIR}
         lwproctrace.proto
)

add_custom_command(
  OUTPUT
  ${CMAKE_CURRENT_BINARY_DIR}/dump.py
  DEPENDS
  ${CMAKE_CURRENT_SOURCE_DIR}/dump.py
  COMMAND
  cp -a ${CMAKE_CURRENT_SOURCE_DIR}/dump.py ${CMAKE_CURRENT_BINARY_DIR}/dump.py
)

add_custom_target(
  dump
  ALL
  DEPENDS
  ${CMAKE_CURRENT_BINARY_DIR}/lwproctrace_pb2.py
  ${CMAKE_CURRENT_BINARY_DIR}/dump.py
)
