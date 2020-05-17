#ifndef LWPTTR_PROC_BEGIN_H
#define LWPTTR_PROC_BEGIN_H

#include <stdlib.h>

/**
 * @brief make a process begin event
 * @param[out] *data pointer to event data (malloc-ed)
 * @param[out] *size size of data
 * @return 0 on success (*data, *size set),
 *         -1 on error (*data = NULL, *size = 0)
 */
int lwptev_proc_begin(void **data, size_t *size);

#endif /* #ifndef LWPTTR_PROC_BEGIN_H */
