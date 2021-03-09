#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>

void run(char const *path) {
  pid_t child = fork();
  if (child == 0) {
    execl(path, path, NULL);
    exit(EXIT_FAILURE);
  } else if (child > 0) {
    waitpid(child, NULL, 0);
  }
}

int main() {
  run("/bin/ls");
  pid_t child = fork();
  if (child == 0) {
    run("/bin/uptime");
  } else if (child > 0) {
    waitpid(child, NULL, 0);
    run("/bin/hostname");
  }
  return EXIT_SUCCESS;
}
