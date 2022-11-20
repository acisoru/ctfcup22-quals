#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <signal.h>

#define WRITE  0x1001
#define READ   0x2002


typedef struct{
    char* data;
    int size;
} u_req;

int fd = 0; // device fd

void setup(void);
size_t write_(uint8_t* data, uint32_t size);
size_t read_(uint8_t* data, uint32_t size);
