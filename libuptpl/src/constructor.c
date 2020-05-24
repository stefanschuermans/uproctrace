/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#include <uptev/proc_begin.h>

#include "write.h"

#include <stdlib.h>

__attribute__((constructor)) static void constructor(void) {
  void *data = NULL;
  size_t size = 0;
  uptev_proc_begin(&data, &size);
  uptpl_write(data, size);
}
