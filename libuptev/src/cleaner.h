/**
 * UProcTrace: User-space Process Tracing
 * Copyright 2020: Stefan Schuermans, Aachen, Germany <stefan@schuermans.info>
 * Copyleft: GNU LESSER GENERAL PUBLIC LICENSE version 3 (see LICENSE)
 */

#ifndef UPTEV_CLEANER_H
#define UPTEV_CLEANER_H

/**
 * @brief cleaner object
 *
 * collects pointers to be freed and frees them on request
 */
typedef struct uptev_cleaner_s uptev_cleaner_t;

/**
 * @brief creater cleaner object
 * @return pointer to cleaner object or NULL on error
 */
uptev_cleaner_t *uptev_cleaner_new(void);

/**
 * @brief add pointer to be freed to cleaner object
 * @param[in] cleaner cleaner object
 * @param[in] ptr the pointer to be freed on cleanup
 * @return 0 on success, -1 on error
 *         (on error, cleanup is done and cleaner is deallocated)
 */
int uptev_cleaner_add_ptr(uptev_cleaner_t *cleaner, void *ptr);

/**
 * @brief cleanup all pointers in cleaner and free cleaner itself
 * @param[in] cleaner cleaner object
 */
void uptev_cleaner_cleanup(uptev_cleaner_t *cleaner);

#endif /* #ifndef UPTEV_CLEANER_H */
