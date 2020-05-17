#ifndef LWPTEV_READ_FILE_H
#define LWPTEV_READ_FILE_H

/**
 * @brief read file contents
 * @param[in] pathname path to file containing zero-terminated string list
 * @param[out] *size size of file contents
 * @return pointer to malloc-ed file contents or NULL
 */
char * lwptev_read_file(char const *pathname, size_t *size);

#endif /* #ifndef LWPTEV_READ_FILE_H */
