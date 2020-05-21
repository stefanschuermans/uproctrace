add_library(
  uptpl
  SHARED
  src/constructor.c
  src/destructor.c
  src/write.c
  src/write.h
)

target_link_libraries(uptpl uptev)

