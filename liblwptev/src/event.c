#include "event.h"
#include "cleaner.h"

#include <lwproctrace.pb-c.h>

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
int lwptev_event_pack(struct _Lwproctrace__Event *event,
                      void **data, size_t *size,
                      lwptev_cleaner_t *cleaner) {
  *size = lwproctrace__event__get_packed_size(event);
  *data = malloc(*size);
  if (! data) {
    lwptev_cleaner_cleanup(cleaner);
    *size = 0;
    return -1;
  }
  *size = lwproctrace__event__pack(event, *data);
  lwptev_cleaner_cleanup(cleaner);
  return 0;
}
