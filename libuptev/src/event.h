#ifndef UPTEV_EVENT_H
#define UPTEV_EVENT_H

#include "cleaner.h"

#include <uproctrace.pb-c.h>

#include <stdlib.h>

/**
 * @brief pack event to a buffer
 * @param[in] event the event to pack to a buffer
 * @param[out] *data pointer to event data (malloc-ed)
 * @param[out] *size size of data
 * @param[in] cleaner cleaned up after building data buffer (also on error)
 * @return 0 on success (*data, *size set),
 *         -1 on error (*data = NULL, *size = 0)
 */
int uptev_event_pack(struct _Uproctrace__Event *event, void **data,
                     size_t *size, uptev_cleaner_t *cleaner);

#endif /* #ifndef UPTEV_EVENT_H */
