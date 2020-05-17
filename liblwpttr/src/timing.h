#ifndef LWPTTR_TIMING_H
#define LWPTTR_TIMING_H

#include <lwproctrace.pb-c.h>

/**
 * @brief fill timestamp with current time
 * @param[in,out] timestamp initialized structure to set to current time
 */
void timing_get_timestamp(struct _Lwproctrace__Timespec *timestamp);

/**
 * @brief fill timestamp with total CPU time used by process
 * @param[in,out] timestamp initialized structure to set to proccess CPU time
 */
void timing_get_proc_cpu_time(struct _Lwproctrace__Timespec *proc_cpu_time);

#endif /* #ifndef LWPTTR_TIMING_H */
