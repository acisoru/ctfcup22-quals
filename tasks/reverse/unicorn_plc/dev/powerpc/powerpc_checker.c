
int ppc_checker()
{
    //int part = 0xaabbccdd;
    int part = 0x9c1337a6;
    char data[4] = {(part >> 24) & 0xff, (part >> 16) & 0xff, (part >> 8) & 0xff, (part >> 0) & 0xff};
    char add[4] = {0x4a, 0x11, 0xc0, 0xef};
    char mul[4] = {0x90, 0xba, 0x13, 0x02};

    for (int i = 0; i<4; i++)
    {
        data[i] = (mul[i]*data[i]+add[i]) & 0xff;
    }

    if (data[0] == 0x0a && data[1] == 0xdf && data[2] == 0xd5 & data[3] == 0x3b)
    {
        return 1;
    }
    return 0;
}

int _start()
{
    return ppc_checker();
}