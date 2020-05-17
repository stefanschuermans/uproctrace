#ifndef LWPTTR_TIMESTAMP_H
#define LWPTTR_TIMESTAMP_H

#include <lwproctrace.pb-c.h>

/**
 * @brief fill timestamp with current time
 * @param[in,out] timestamp initialized structure to set to current time
 */
void lwpttr_event_get_timestamp(struct _Lwproctrace__Timespec *timestamp);

#endif /* #ifndef LWPTTR_TIMESTAMP_H */
