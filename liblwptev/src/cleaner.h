#ifndef LWPTEV_CLEANER_H
#define LWPTEV_CLEANER_H

/**
 * @brief cleaner object
 *
 * collects pointers to be freed and frees them on request
 */
typedef struct lwptev_cleaner_s lwptev_cleaner_t;

/**
 * @brief creater cleaner object
 * @return pointer to cleaner object or NULL on error
 */
lwptev_cleaner_t * lwptev_cleaner_new(void);

/**
 * @brief add pointer to be freed to cleaner object
 * @param[in] cleaner cleaner object
 * @param[in] ptr the pointer to be freed on cleanup
 * @return 0 on success, -1 on error
 *         (on error, cleanup is done and cleaner is deallocated)
 */
int lwptev_cleaner_add_ptr(lwptev_cleaner_t *cleaner, void *ptr);

/**
 * @brief cleanup all pointers in cleaner and free cleaner itself
 * @param[in] cleaner cleaner object
 */
void lwptev_cleaner_cleanup(lwptev_cleaner_t *cleaner);

#endif /* #ifndef LWPTEV_CLEANER_H */
