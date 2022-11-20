#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>

#define STDIN_FD 0
#define STDOUT_FD 1

void setup(void);
ssize_t read_into_buffer(void* , uint32_t);
int read_integer(void);
long long read_long_integer(void);

int main() 
{
    setup();

    char name[128];
    printf("{?} Enter your name: ");
    read_into_buffer(name, 127);

    int size = 0;
    printf("{?} Enter ozne size: ");
    size = read_integer();

    if (size <= 0) {
        puts("{-} Error in ozne size!");
        return -1;
    }

    uint64_t* ozne = (uint64_t*) malloc(size * sizeof(uint64_t));

    if (ozne == NULL) {
        puts("{-} Error in ozne create!");
        return -1;
    }

    // read 
    printf("{?} Enter index of view: ");
    uint32_t view_idx = 0;
    view_idx = (uint32_t)read_integer();
    printf("{?} ozne[%d]: %lu\n", view_idx, ozne[view_idx]);

    // write
    printf("{?} Enter index of edit: ");
    uint32_t edit_idx = 0;
    edit_idx = (uint32_t)read_integer();
    
    printf("{?} Enter value of edit: ");
    uint64_t value = 0;
    value = (uint64_t) read_long_integer();

    ozne[edit_idx] = value;

    printf("%s, thanks to use OZNE!\nBye\n", name);
    exit(0);
}


void setup(void)
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

ssize_t read_into_buffer(void *buf, uint32_t size) 
{
    if (buf == NULL) {
        puts("[-] invalid buffer pointer");
        return -1;
    }

    if (size == 0) {
        puts("[-] invalid buffer size");
        return -1;
    }

    ssize_t nbytes = read(STDIN_FD, buf, size);

    if (nbytes < 0) {
        puts("[-] failed to read into buffer");
        return -1;
    }

    return nbytes;
}

int read_integer(void)
{
    const size_t buflen = 16;

    char buf[buflen];
    ssize_t nbytes = read_into_buffer(buf, buflen);

    if (nbytes == -1) {
        puts("[-] failed to read int");
        return -1;
    }

    return atoi(buf);
}

long long read_long_integer(void)
{
    const size_t buflen = 32;

    char buf[buflen];
    ssize_t nbytes = read_into_buffer(buf, buflen);

    if (nbytes == -1) {
        puts("[-] failed to read int");
        return -1;
    }

    return atoll(buf);
}