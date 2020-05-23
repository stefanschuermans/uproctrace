add_test(
  NAME
  pylint
  COMMAND
  pylint3 --rcfile=${CMAKE_CURRENT_SOURCE_DIR}/pylint.rc
          --ignore uproctrace_pb2.py uproctrace
)

SET_TESTS_PROPERTIES(
  pylint
  PROPERTIES
  ENVIRONMENT
  "PYTHONPATH=${CMAKE_BINARY_DIR}/python3"
)
