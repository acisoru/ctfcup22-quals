#include <unicorn/unicorn.h>
#include <string.h>
#include <stdio.h>

#define MIPSCODE "\x3c\x02\xde\xad\x34\x42\xbe\xef\x00\x43\x18\x26\x3c\x02\xca\xfe\x34\x42\xc4\x11\x00\x43\x18\x26\x3c\x02\x5c\xa1\x34\x42\x4b\x1e\x00\x43\x18\x26\x3c\x02\x13\x37\x34\x42\x13\x37\x00\x43\x18\x26\x3c\x02\x1a\x7b\x34\x42\x55\xcd\x14\x62\x00\x04\x00\x00\x00\x00\x24\x03\x00\x01\x10\x00\x00\x02\x00\x00\x00\x00\x24\x03\x00\x00\x00\x00\x00\x00"

#define ADDRESS 0x00000000

static void hook_code(uc_engine *uc, uint64_t address, uint32_t size, void *user_data)
{
    int v0,v1;
    uc_reg_read(uc, UC_MIPS_REG_2, &v0);
    uc_reg_read(uc, UC_MIPS_REG_3, &v1);
    printf("\t[!] addr=0x%" PRIx64 ", opcode size = 0x%x,  $V0=0x%x,  $V1=0x%x\n",
           address, size, v0, v1);
}

void uc_mips_start()
{
    uc_engine* uc;
    uc_err err;
    uc_hook hook_d;
    err = uc_open(UC_ARCH_MIPS, UC_MODE_MIPS32 + UC_MODE_BIG_ENDIAN, &uc);
    if (err)
    {
        printf("[-] Can't create Emulator: %u %s\n", err, uc_strerror(err));
        return;
    }
    printf("[+] Emulator init\n");

    //int v1 = 0xaabbccdd;
    int v1 = 0x41be771a;
    uc_mem_map(uc, ADDRESS, 2*1024*1024, UC_PROT_ALL);
    uc_mem_write(uc, ADDRESS, MIPSCODE, sizeof(MIPSCODE)-1);
    uc_reg_write(uc, UC_MIPS_REG_3, &v1); //$3 is $v1
    uc_hook_add(uc, &hook_d, UC_HOOK_CODE, hook_code, NULL, ADDRESS, ADDRESS+sizeof(MIPSCODE)-1);
    printf("[+] Emulator configured\n");

    err = uc_emu_start(uc, ADDRESS, ADDRESS+sizeof(MIPSCODE)-1, 0,0);
    if (err)
    {
        printf("[-] Emulation fucked up: %u %s\n", err, uc_strerror(err));
        return;
    }
    printf("[+] Emulator done!\n");
    uc_reg_read(uc, UC_MIPS_REG_3, &v1);
    printf("$V1 = 0x%x\n", v1);

    uc_close(uc);

}


int main()
{
    uc_mips_start();

    return 0;
}