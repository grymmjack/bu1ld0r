// A file's last change time and size (stat): bu1ld0r notices a picture saved by
// another program without reading it. -1 when the file isn't there.
#include <sys/stat.h>

double FileTimeMs(const char *p) {
    struct stat s;
    if (stat(p, &s) != 0) return -1;
#if defined(__linux__)
    return (double)s.st_mtim.tv_sec * 1000.0 + (double)(s.st_mtim.tv_nsec / 1000000);
#elif defined(__APPLE__)
    return (double)s.st_mtimespec.tv_sec * 1000.0 + (double)(s.st_mtimespec.tv_nsec / 1000000);
#else
    return (double)s.st_mtime * 1000.0;
#endif
}

double FileBytes(const char *p) {
    struct stat s;
    if (stat(p, &s) != 0) return -1;
    return (double)s.st_size;
}
