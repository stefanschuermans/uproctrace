add_library(
  lwptpl
  SHARED
  src/constructor.c
)

target_link_libraries(lwptpl lwpttr)

