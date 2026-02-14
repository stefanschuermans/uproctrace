add_test(
  NAME
  pylint
  COMMAND
  pylint --rcfile=${CMAKE_CURRENT_SOURCE_DIR}/pylint.rc
         --ignore uproctrace.uproctrace_pb2.py uproctrace
)

SET_TESTS_PROPERTIES(
  pylint
  PROPERTIES
  ENVIRONMENT
  "PYTHONPATH=${CMAKE_BINARY_DIR}/lib/python3/dist-packages"
)
