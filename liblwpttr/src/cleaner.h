#ifndef LWPTTR_CLEANER_H
#define LWPTTR_CLEANER_H

/**
 * @brief cleaner object
 *
 * collects pointers to be freed and frees them on request
 */
typedef struct lwpttr_cleaner_s lwpttr_cleaner_t;

/**
 * @brief creater cleaner object
 * @return pointer to cleaner object or NULL on error
 */
lwpttr_cleaner_t * lwpttr_cleaner_new(void);

/**
 * @brief add pointer to be freed to cleaner object
 * @param[in] cleaner cleaner object
 * @param[in] ptr the pointer to be freed on cleanup
 * @return 0 on success, -1 on error
 *         (on error, cleanup is done and cleaner is deallocated)
 */
int lwpttr_cleaner_add_ptr(lwpttr_cleaner_t *cleaner, void *ptr);

/**
 * @brief cleanup all pointers in cleaner and free cleaner itself
 * @param[in] cleaner cleaner object
 */
void lwpttr_cleaner_cleanup(lwpttr_cleaner_t *cleaner);

#endif /* #ifndef LWPTTR_CLEANER_H */
