#include <unicorn/unicorn.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define ADDRESS 0x00000000
// MIPS EMULATION
#define MIPSCODE "\x3c\x02\xde\xad\x34\x42\xbe\xef\x00\x43\x18\x26\x3c\x02\xca\xfe\x34\x42\xc4\x11\x00\x43\x18\x26\x3c\x02\x5c\xa1\x34\x42\x4b\x1e\x00\x43\x18\x26\x3c\x02\x13\x37\x34\x42\x13\x37\x00\x43\x18\x26\x3c\x02\x1a\x7b\x34\x42\x55\xcd\x14\x62\x00\x04\x00\x00\x00\x00\x24\x03\x00\x01\x10\x00\x00\x02\x00\x00\x00\x00\x24\x03\x00\x00\x00\x00\x00\x00"


unsigned int uc_mips_start(unsigned int part)
{
    uc_engine* uc;
    uc_err err;

    err = uc_open(UC_ARCH_MIPS, UC_MODE_MIPS32 + UC_MODE_BIG_ENDIAN, &uc);
    if (err)
    {
        puts("[-] Error in license checking process.");
        return 0;
    }

    int v1 = part;
    uc_mem_map(uc, ADDRESS, 2*1024*1024, UC_PROT_ALL);
    uc_mem_write(uc, ADDRESS, MIPSCODE, sizeof(MIPSCODE)-1);
    uc_reg_write(uc, UC_MIPS_REG_3, &v1); //$3 is $v1

    err = uc_emu_start(uc, ADDRESS, ADDRESS+sizeof(MIPSCODE)-1, 0,0);
    if (err)
    {
        puts("[-] Error in license checking process.");
        return 0;
    }
    uc_reg_read(uc, UC_MIPS_REG_3, &v1);
    uc_close(uc);
    return v1;
}

// POWERPC EMULATION
#define PPC64CODE "\x91\x3f\x00\x0c\x81\x3f\x00\x0c\x55\x29\x46\x3e\x55\x29\x06\x3e\x99\x3f\x00\x10\x81\x3f\x00\x0c\x7d\x29\x86\x70\x55\x29\x06\x3e\x99\x3f\x00\x11\x81\x3f\x00\x0c\x7d\x29\x46\x70\x55\x29\x06\x3e\x99\x3f\x00\x12\x81\x3f\x00\x0c\x55\x29\x06\x3e\x99\x3f\x00\x13\x3d\x20\x4a\x11\x61\x29\xc0\xef\x91\x3f\x00\x14\x3d\x20\x90\xba\x61\x29\x13\x02\x91\x3f\x00\x18\x39\x20\x00\x00\x91\x3f\x00\x08\x48\x00\x00\x60\x39\x5f\x00\x18\x81\x3f\x00\x08\x7d\x2a\x4a\x14\x89\x49\x00\x00\x39\x1f\x00\x10\x81\x3f\x00\x08\x7d\x28\x4a\x14\x89\x29\x00\x00\x7d\x2a\x49\xd6\x55\x2a\x06\x3e\x39\x1f\x00\x14\x81\x3f\x00\x08\x7d\x28\x4a\x14\x89\x29\x00\x00\x7d\x2a\x4a\x14\x55\x2a\x06\x3e\x39\x1f\x00\x10\x81\x3f\x00\x08\x7d\x28\x4a\x14\x99\x49\x00\x00\x81\x3f\x00\x08\x39\x29\x00\x01\x91\x3f\x00\x08\x81\x3f\x00\x08\x2c\x09\x00\x03\x40\x81\xff\x9c\x89\x3f\x00\x10\x28\x09\x00\x0a\x40\x82\x00\x50\x89\x3f\x00\x11\x28\x09\x00\xdf\x40\x82\x00\x44\x89\x3f\x00\x12\x69\x29\x00\xd5\x7d\x29\x00\x34\x55\x29\xd9\x7e\x55\x2a\x06\x3e\x89\x3f\x00\x13\x69\x29\x00\x3b\x7d\x29\x00\x34\x55\x29\xd9\x7e\x55\x29\x06\x3e\x7d\x49\x48\x38\x55\x29\x06\x3e\x2c\x09\x00\x00\x41\x82\x00\x0c\x39\x20\x00\x01\x48\x00\x00\x08\x39\x20\x00\x00\x39\x00\x00\x00"

unsigned int uc_ppc_start(unsigned int part)
{
    uc_engine* uc;
    uc_err err;
    uc_hook hook_d;
    err = uc_open(UC_ARCH_PPC, UC_MODE_PPC32 + UC_MODE_BIG_ENDIAN, &uc);
    if (err)
    {
        puts("[-] Error in license checking process.");
        return 0;
    }

    //int r9 = 0xaabbccdd;
    int r9 = part;
    int r31 = 2*1024;
    
    uc_mem_map(uc, ADDRESS, 2*1024*1024, UC_PROT_ALL);
    uc_mem_write(uc, ADDRESS, PPC64CODE, sizeof(PPC64CODE)-1);
    uc_reg_write(uc, UC_PPC_REG_9, &r9); 
    uc_reg_write(uc, UC_PPC_REG_31, &r31); 

    err = uc_emu_start(uc, ADDRESS, ADDRESS+sizeof(PPC64CODE)-1, 0,0);
    if (err)
    {
        puts("[-] Error in license checking process.");
        return 0;
    }
    uc_reg_read(uc, UC_PPC_REG_9, &r9);
    uc_close(uc);
    return r9;
}

// SPARK EMULATION

#define SPARKCODE "\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x82\x00\x40\x01\x84\x10\x00\x01\x03\x2a\xaa\xaa\x82\x10\x62\xaa\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x01\x03\x15\x55\x55\x82\x10\x61\x55\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x02\x03\x33\x33\x33\x82\x10\x60\xcc\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x02\x03\x0c\xcc\xcc\x82\x10\x63\x33\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x04\x03\x3c\x3c\x3c\x82\x10\x60\xf0\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x04\x03\x03\xc3\xc3\x82\x10\x63\x0f\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x18\xc2\x07\xbf\xfc\x87\x28\x60\x08\x03\x00\x3f\xc0\x82\x08\xc0\x01\x84\x10\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x08\x03\x00\x00\x3f\x82\x10\x63\x00\x82\x08\xc0\x01\x84\x10\x80\x01\xc2\x07\xbf\xfc\x83\x30\x60\x18\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc4\x07\xbf\xfc\x03\x1b\x22\x13\x82\x10\x62\xa1\x80\xa0\x80\x01\x12\x80\x00\x05\x01\x00\x00\x00\x82\x10\x20\x01\x10\x80\x00\x03\x01\x00\x00\x00\x82\x10\x20\x00\x01\x00\x00\x00"

unsigned int uc_spark_start(unsigned int part)
{
    uc_engine* uc;
    uc_err err;
    uc_hook hook_d;
    err = uc_open(UC_ARCH_SPARC, UC_MODE_SPARC32 + UC_MODE_BIG_ENDIAN, &uc);
    if (err)
    {
        puts("[-] Error in license checking process.");
        return 0;
    }

    int g1 =  part;
    int sp = 2*1024;
    int fp = sp;


    uc_mem_map(uc, ADDRESS, 16*1024*1024, UC_PROT_ALL);
    uc_mem_write(uc, ADDRESS, SPARKCODE, sizeof(SPARKCODE)-1);
    uc_reg_write(uc, UC_SPARC_REG_G1, &g1); 
    uc_reg_write(uc, UC_SPARC_REG_FP, &fp); 
    uc_reg_write(uc, UC_SPARC_REG_SP, &sp); 

    err = uc_emu_start(uc, ADDRESS, ADDRESS+sizeof(SPARKCODE)-1, 0,0);
    if (err)
    {
        puts("[-] Error in license checking process.");
        return 0;
    }
    uc_reg_read(uc, UC_SPARC_REG_G1, &g1);

    uc_close(uc);
    return g1;
}


int main(int argc, char** argv)
{
    puts("[[ UNICORN ICS INC. ]]");
    puts(" _______\)%%%%%%%%._              \n"
"`''''-'-;   % % % % %'-._         \n"
"        :b) \            '-.      \n"
"        : :__)'    .'    .'       \n"
"        :.::/  '.'   .'           \n"
"        o_i/   :    ;             \n"
"               :   .'             \n"
"                ''`");

    //cup{41be771a9c1337a685721136}
    if (argc != 2)
    {
        printf("[!] Use: %s <Activation Code>\n", argv[0]);
        exit(-1);
    }
    char* flag = argv[1];
    if (strlen(flag) != 29)
    {
        puts("[-] Error in license checking process.");
        exit(-1);
    }
    int flag_i = (flag[0] << 24) | (flag[1] << 16) | (flag[2] << 8) | (flag[3]);
    if (flag_i != 0x4355507b || flag[28] != 0x7d)
    {
        puts("[-] Error in license checking process.");
        exit(-1);
    }
    int result_mips  = 0;
    int result_ppc   = 0;
    int result_spark = 0;
    for (int i = 4; i <= 20; i+=8)
    {
        char part[8];
        strncpy(part, flag+i, 8);
        unsigned int part_i = strtol(part, NULL, 16);
        switch (i)
        {
        case 4:
            result_mips = uc_mips_start(part_i);
            break;
        case 12:
            result_ppc = uc_ppc_start(part_i);
            break;
        case 20:
            result_spark = uc_spark_start(part_i);
            break;
        default:
            exit(-1);
            break;
        }
    }
    if (result_mips*result_ppc*result_spark == 1)
    {
        puts("[+] Your Activation Code is valid!");
        puts("#TODO (from master) - Finish demo BEFORE start of conference, not after!!!");
        //TODO: мем про конфу
    } else {
        puts("[-] Your Activation Code is invalid :(");
    }
    return 0;
}