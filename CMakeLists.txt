cmake_minimum_required(VERSION 3.10)
project(lwproctrace)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -fPIC")

enable_testing()

add_subdirectory(liblwptpl)
add_subdirectory(liblwpttr)
add_subdirectory(tests)
