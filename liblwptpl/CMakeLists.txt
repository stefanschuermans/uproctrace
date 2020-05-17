add_library(
  lwptpl
  SHARED
  src/constructor.c
  src/destructor.c
  src/write.c
  src/write.h
)

target_link_libraries(lwptpl lwpttr)

