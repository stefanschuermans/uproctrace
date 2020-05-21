cmake_minimum_required(VERSION 3.10)
project(uproctrace)

set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -Wall -Wextra -Werror -fPIC")

enable_testing()

add_subdirectory(dump)
add_subdirectory(libuptev)
add_subdirectory(libuptpl)
add_subdirectory(tests)
