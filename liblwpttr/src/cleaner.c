#include "cleaner.h"
#include "macros.h"

#include <stdlib.h>

struct lwpttr_cleaner_s {
  unsigned int free_ptr_cnt; /**< number of pointer to be freed */
  void * free_ptrs[64]; /**< pointers to be freed */
  lwpttr_cleaner_t *next; /**< next cleaner object, linked list */
};

lwpttr_cleaner_t * lwpttr_cleaner_new(void) {
  lwpttr_cleaner_t *cleaner = malloc(sizeof(lwpttr_cleaner_t));
  if (! cleaner) {
    return NULL;
  }
  cleaner->free_ptr_cnt = 0;
  cleaner->next = NULL;
  return cleaner;
}

int lwpttr_cleaner_add_ptr(lwpttr_cleaner_t *cleaner, void *ptr) {
  /* find last cleaner in chain */
  lwpttr_cleaner_t *cl = cleaner;
  while (cl->next != NULL) {
    cl = cl->next;
  }
  /* last cleaner full? */
  if (cl->free_ptr_cnt >= countof(cl->free_ptrs)) {
    /* create new one */
    cl->next = lwpttr_cleaner_new();
    /* error ? */
    if (! cl->next) {
      /* cleanup everything and reutrn error */
      lwpttr_cleaner_cleanup(cleaner);
      return -1;
    }
    /* go to new cleaner */
    cl = cl->next;
  }
  /* add pointer */
  cl->free_ptrs[cl->free_ptr_cnt++] = ptr;
  return 0;
}

void lwpttr_cleaner_cleanup(lwpttr_cleaner_t *cleaner) {
  lwpttr_cleaner_t *cl = cleaner;
  while (cl) {
    /* free all pointers in cleaner */
    for (unsigned int i = 0; i < cl->free_ptr_cnt; ++i) {
      free(cl->free_ptrs[i]);
    }
    /* move to next cleaner */
    cl = cl->next;
  }
}
