#include "event.h"
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
int uptev_event_pack(struct _Uproctrace__Event *event,
                      void **data, size_t *size,
                      uptev_cleaner_t *cleaner) {
  *size = uproctrace__event__get_packed_size(event);
  *data = malloc(*size);
  if (! data) {
    uptev_cleaner_cleanup(cleaner);
    *size = 0;
    return -1;
  }
  *size = uproctrace__event__pack(event, *data);
  uptev_cleaner_cleanup(cleaner);
  return 0;
}
