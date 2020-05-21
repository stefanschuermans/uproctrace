#ifndef UPTEV_TIMING_H
#define UPTEV_TIMING_H

#include <uproctrace.pb-c.h>

/**
 * @brief fill timestamp with current time
 * @param[in,out] timestamp initialized structure to set to current time
 */
void uptev_timing_get_timestamp(struct _Uproctrace__Timespec *timestamp);

/**
 * @brief fill timestamp with total CPU time used by process
 * @param[in,out] timestamp initialized structure to set to proccess CPU time
 */
void uptev_timing_get_proc_cpu_time(struct _Uproctrace__Timespec
                                     *proc_cpu_time);

#endif /* #ifndef UPTEV_TIMING_H */
