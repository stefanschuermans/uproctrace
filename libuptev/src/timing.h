/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#ifndef UPTEV_TIMING_H
#define UPTEV_TIMING_H

#include <uproctrace.pb-c.h>

#include <sys/time.h>
#include <time.h>

/**
 * @brief convert timeval to protobuf
 * @param[in] ts timeval to convert
 * @param[in,out] timestamp initialized structure to set to current time
 */
void uptev_timing_timeval_to_pb(struct timeval const *tv,
                                Uproctrace__Timespec *tsp);

/**
 * @brief convert timespec to protobuf
 * @param[in] ts timespec to convert
 * @param[in,out] timestamp initialized structure to set to current time
 */
void uptev_timing_timespec_to_pb(struct timespec const *ts,
                                 Uproctrace__Timespec *tsp);

/**
 * @brief fill timestamp with current time
 * @param[in,out] timestamp initialized structure to set to current time
 */
void uptev_timing_get_timestamp(Uproctrace__Timespec *timestamp);

/**
 * @brief fill timestamp with total CPU time used by process
 * @param[in,out] timestamp initialized structure to set to proccess CPU time
 */
void uptev_timing_get_proc_cpu_time(
    Uproctrace__Timespec *proc_cpu_time);

#endif /* #ifndef UPTEV_TIMING_H */
