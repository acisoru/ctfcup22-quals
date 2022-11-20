#include <unicorn/unicorn.h>
#include <string.h>
#include <stdio.h>

#define SPARKCODE "\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x82\x00\x40\x01\x84\x10\x00\x01\x03\x2a\xaa\xaa\x82\x10\x62\xaa\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x01\x03\x15\x55\x55\x82\x10\x61\x55\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x02\x03\x33\x33\x33\x82\x10\x60\xcc\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x02\x03\x0c\xcc\xcc\x82\x10\x63\x33\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x04\x03\x3c\x3c\x3c\x82\x10\x60\xf0\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x04\x03\x03\xc3\xc3\x82\x10\x63\x0f\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x18\xc2\x07\xbf\xfc\x87\x28\x60\x08\x03\x00\x3f\xc0\x82\x08\xc0\x01\x84\x10\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x08\x03\x00\x00\x3f\x82\x10\x63\x00\x82\x08\xc0\x01\x84\x10\x80\x01\xc2\x07\xbf\xfc\x83\x30\x60\x18\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc4\x07\xbf\xfc\x03\x1b\x22\x13\x82\x10\x62\xa1\x80\xa0\x80\x01\x12\x80\x00\x05\x01\x00\x00\x00\x82\x10\x20\x01\x10\x80\x00\x03\x01\x00\x00\x00\x82\x10\x20\x00\x01\x00\x00\x00"

#define ADDRESS 0x00000000

static void hook_code(uc_engine *uc, uint64_t address, uint32_t size, void *user_data)
{
    int v0,v1, g2;
    uc_reg_read(uc, UC_SPARC_REG_G1, &v0);
    uc_reg_read(uc, UC_SPARC_REG_G2, &g2);
    uc_reg_read(uc, UC_SPARC_REG_FP, &v1);
    printf("\t[!] addr=0x%" PRIx64 ", opcode size = 0x%x,  $g1=0x%x, $g2=0x%x\n",
           address, size, v0,g2);
}

void uc_mips_start()
{
    uc_engine* uc;
    uc_err err;
    uc_hook hook_d;
    err = uc_open(UC_ARCH_SPARC, UC_MODE_SPARC32 + UC_MODE_BIG_ENDIAN, &uc);
    if (err)
    {
        printf("[-] Can't create Emulator: %u %s\n", err, uc_strerror(err));
        return;
    }
    printf("[+] Emulator init\n");

    //int g1 = 0xaabbccdd;
    int g1 =  0x85721136;
    int sp = 2*1024;
    int fp = sp;


    uc_mem_map(uc, ADDRESS, 16*1024*1024, UC_PROT_ALL);
    uc_mem_write(uc, ADDRESS, SPARKCODE, sizeof(SPARKCODE)-1);
    uc_reg_write(uc, UC_SPARC_REG_G1, &g1); 
    uc_reg_write(uc, UC_SPARC_REG_FP, &fp); 
    uc_reg_write(uc, UC_SPARC_REG_SP, &sp); 
    uc_hook_add(uc, &hook_d, UC_HOOK_CODE, hook_code, NULL, ADDRESS, ADDRESS+sizeof(SPARKCODE)-1);
    printf("[+] Emulator configured\n");

    err = uc_emu_start(uc, ADDRESS, ADDRESS+sizeof(SPARKCODE)-1, 0,0);
    if (err)
    {
        printf("[-] Emulation fucked up: %u %s\n", err, uc_strerror(err));
        return;
    }
    printf("[+] Emulator done!\n");
    uc_reg_read(uc, UC_SPARC_REG_G1, &g1);
    printf("$g1 = 0x%x\n", g1);

    uc_close(uc);

}


int main()
{
    uc_mips_start();

    return 0;
}