#include <stdlib.h>
#include <stdio.h>


int mips_checker(int part)
{
    part ^= 0xdeadbeef;
    part ^= 0xcafec411;
    part ^= 0x5ca1ab1e;
    part ^= 0x13371337;

    if (part == 0x1a7bb5cd)
    {
        return 1;
    }

    return 0;
}

int main()
{
    printf("%d\n", mips_checker(0xaabbccdd));
    return 0;
}