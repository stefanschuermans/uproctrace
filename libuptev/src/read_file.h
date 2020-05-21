#ifndef UPTEV_READ_FILE_H
#define UPTEV_READ_FILE_H

/**
 * @brief read file contents
 * @param[in] pathname path to file containing zero-terminated string list
 * @param[out] *size size of file contents
 * @return pointer to malloc-ed file contents or NULL
 */
char *uptev_read_file(char const *pathname, size_t *size);

#endif /* #ifndef UPTEV_READ_FILE_H */
