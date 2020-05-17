#include "cleaner.h"
#include "macros.h"

#include <stdlib.h>

struct lwptev_cleaner_s {
  unsigned int free_ptr_cnt; /**< number of pointer to be freed */
  void * free_ptrs[64]; /**< pointers to be freed */
  lwptev_cleaner_t *next; /**< next cleaner object, linked list */
};

lwptev_cleaner_t * lwptev_cleaner_new(void) {
  lwptev_cleaner_t *cleaner = malloc(sizeof(lwptev_cleaner_t));
  if (! cleaner) {
    return NULL;
  }
  cleaner->free_ptr_cnt = 0;
  cleaner->next = NULL;
  return cleaner;
}

int lwptev_cleaner_add_ptr(lwptev_cleaner_t *cleaner, void *ptr) {
  /* find last cleaner in chain */
  lwptev_cleaner_t *cl = cleaner;
  while (cl->next != NULL) {
    cl = cl->next;
  }
  /* last cleaner full? */
  if (cl->free_ptr_cnt >= countof(cl->free_ptrs)) {
    /* create new one */
    cl->next = lwptev_cleaner_new();
    /* error ? */
    if (! cl->next) {
      /* cleanup everything and reutrn error */
      lwptev_cleaner_cleanup(cleaner);
      return -1;
    }
    /* go to new cleaner */
    cl = cl->next;
  }
  /* add pointer */
  cl->free_ptrs[cl->free_ptr_cnt++] = ptr;
  return 0;
}

void lwptev_cleaner_cleanup(lwptev_cleaner_t *cleaner) {
  lwptev_cleaner_t *cl = cleaner;
  while (cl) {
    /* free all pointers in cleaner */
    for (unsigned int i = 0; i < cl->free_ptr_cnt; ++i) {
      free(cl->free_ptrs[i]);
    }
    /* move to next cleaner */
    cl = cl->next;
  }
}
