add_executable(
  forkapp
  forkapp.c
)

add_test(
  NAME
  fork
  COMMAND
  ${CMAKE_CURRENT_SOURCE_DIR}/forktest.bash ${CMAKE_BINARY_DIR}
)
