#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/mount.h>
#include <signal.h>

#define USER_CODEPAGE_SIZE 4096
#define ALPH_SIZE 18
#define USER_INPUT_SIZE 128

uint8_t alph[ALPH_SIZE] = {0x58,0x59,0x49,0x5a,0x34,0x6c,0x30,0x4f,0x40,0x50,0x41,0x48, 0x75, 0x79, 0x5d, 0x5b, 0x55, 0x69};

void run_code(void* code) {
    asm (
        "jmp dword ptr[esp+8];"
    );
};

int main() {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);

    void* code = mmap(0, USER_CODEPAGE_SIZE, PROT_EXEC | PROT_WRITE | PROT_READ, MAP_ANON | MAP_SHARED, -1, 0);
    
    printf("{?} Enter your phrase: ");
    int nbytes = read(0, code, USER_INPUT_SIZE);

    if (nbytes <= 0) {
        puts("{-} Error in read user input!");
        return 0;
    }

    for (size_t i = 0; i < nbytes; ++i) {
        int f = 0;
        for (size_t j = 0; j < ALPH_SIZE; ++j) {
            if (*(uint8_t*)(code + i) == alph[j]) {
                f = 1;
                break;
            }
        }
        if (!f) {
            puts("{-} Invalid symbol!");
            return -1;
        }
    }

    run_code(code);
    return 0;
}