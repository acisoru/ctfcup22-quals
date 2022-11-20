#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <sys/mount.h>
#include <signal.h>

#include "sha256.h"

#define STDIN_FD 0
#define USER_CODEPAGE_SIZE 0x2000
#define USER_CODE_SIZE USER_CODEPAGE_SIZE - 0x100
#define PAGE_HEADER_SIZE 6

void protect(void*, size_t);
void do_security_checks(void*);
void calc_md5_from_usercode(void*, void*);
void set_page_header(void* ptr);
void ban();
void setup();
int run_user_code(void*);
int watcher(void*);
int read_user_code(void*, size_t);
ssize_t read_into_buffer(void*, uint32_t);
uint64_t get_rnd_addr();

uint8_t user_codepage_hash[SHA256_BLOCK_SIZE];
pid_t usercode_pid = 0;

int main()
{
    setup();

    uint64_t* addr = (uint64_t*)get_rnd_addr();
    void* user_code = mmap(addr, USER_CODEPAGE_SIZE, PROT_EXEC | PROT_WRITE | PROT_READ, MAP_ANON | MAP_SHARED, -1, 0);

    if (user_code != (void*)addr)
    {
        puts("{-} mmap error!");
        return -1;
    }

    set_page_header(user_code);

    int nbytes = read_user_code(user_code, USER_CODE_SIZE);

    if (nbytes == -1)
    {
        return nbytes;
    }

    protect(user_code, USER_CODEPAGE_SIZE);
    do_security_checks(user_code);
    calc_md5_from_usercode(user_code, user_codepage_hash);

    if ((usercode_pid = fork()) == 0)
    {
        close(0);
        close(1);
        close(2);
        run_user_code(user_code);
    }

    watcher(user_code);

    return 0;
}

int run_user_code(void* ptr)
{
    if (ptr == NULL)
    {
        return -1;
    }

    asm (
        "xor rax, rax;"
        "xor rbx, rbx;"
        "xor rcx, rcx;"
        "xor rdx, rdx;"
        "xor rbp, rbp;"
        "xor rsp, rsp;"
        "xor rsi, rsi;"
        "xor r8, r8;"
        "xor r9, r9;"
        "xor r10, r10;"
        "xor r11, r11;"
        "xor r12, r12;"
        "xor r13, r13;"
        "xor r14, r14;"
        "xor r15, r15;"
        "jmp rdi;"
    );
}

void do_security_checks(void* ptr)
{
    uint8_t* code = (uint8_t*) ptr;

    for (size_t i = 6; i < USER_CODE_SIZE; ++i)
    {
        // check syscall and sysenter
        if (code[i] == 0x0f &&
            i != USER_CODE_SIZE - 1
            && (code[i + 1] == 0x05 || code[i + 1] == 0x34)
        )
        {
            ban();
        }

        // check int 80h
        if (code[i] == 0xcd &&
            i != USER_CODE_SIZE - 1
            && code[i + 1] == 0x80
        )
        {
            ban();
        }
    }
}

ssize_t read_into_buffer(void *buf, uint32_t size)
{
    if (buf == NULL)
    {
        puts("[-] invalid buffer pointer");
        return -1;
    }

    if (size == 0)
    {
        puts("[-] invalid buffer size");
        return -1;
    }

    ssize_t nbytes = read(STDIN_FD, buf, size);

    if (nbytes < 0)
    {
        puts("[-] failed to read into buffer");
        return -1;
    }

    return nbytes;
}

int watcher(void* ptr)
{
    if (ptr == NULL)
    {
        return -1;
    }

    uint8_t* code = (uint8_t*)ptr;
    while (true)
    {
        uint8_t codepage_hash[SHA256_BLOCK_SIZE];
        calc_md5_from_usercode(code, codepage_hash);

        if (memcmp(codepage_hash, user_codepage_hash, SHA256_BLOCK_SIZE) != 0)
        {
            puts("{-} Invalid hashes!");
            kill(usercode_pid, SIGKILL);
            kill(0, SIGKILL);
        }
    }
}

void calc_md5_from_usercode(void* ptr, void* output)
{
    if (ptr == NULL)
    {
        puts("[-] user code ptr is NULL!");
        exit(1);
    }

    if (output == NULL)
    {
        puts("[-] output ptr is NULL!");
        exit(2);
    }

    // calc initial md5 hash
    SHA256_CTX ctx;

    sha256_init(&ctx);
	sha256_update(&ctx, ptr, USER_CODEPAGE_SIZE);
	sha256_final(&ctx, output);
}

uint64_t get_rnd_addr()
{
    FILE* fp = fopen("/dev/urandom", "r");

    if (fp == NULL)
    {
        puts("{-} Can't open /dev/urandom file!");
        return -1;
    }

    uint64_t value;
    fread((void*)&value, sizeof(uint64_t), 1, fp);
    fclose(fp);

    return (value << 12) & 0x000000ffffffffff;
}

int read_user_code(void* ptr, size_t size)
{
    printf("{?} Enter your x86-64 code: ") ;
    int nbytes = read_into_buffer(ptr + PAGE_HEADER_SIZE, size);

    if (nbytes == -1)
    {
        puts("{-} Error in read user code!");
    }

    return nbytes;
}


void protect(void* user_code, size_t size)
{
    if (user_code != NULL)
    {
        mprotect(user_code, size, PROT_READ | PROT_EXEC);
    }
}

void setup(void)
{
    alarm(30);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void set_page_header(void* ptr)
{
    // xor rdi, rdi; nop; nop; nop
    uint8_t page_header[PAGE_HEADER_SIZE] = {0x48, 0x31, 0xff, 0x90, 0x90, 0x90};
    memcpy(ptr, page_header, PAGE_HEADER_SIZE);
}

void ban()
{
    puts("BAN!");
    exit(-1);
}
