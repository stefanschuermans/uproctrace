add_test(
  NAME
  trace_build
  COMMAND
  ${CMAKE_CURRENT_SOURCE_DIR}/trace_build.bash ${CMAKE_SOURCE_DIR}
                                               ${CMAKE_BINARY_DIR}
)
