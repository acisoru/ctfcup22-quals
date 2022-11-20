#include "kernel_pwn.h"


static noinline long ioctlHandler(struct file *file, unsigned int cmd, unsigned long arg){
    long result = 1337;
    char buf[BUF_SIZE];
    char* ptr = &buf[0];
    char* tbuf = NULL;

    u_req* uReq = (u_req*) kmalloc(sizeof(u_req), GFP_KERNEL);

    if (copy_from_user((void *)uReq, (void *)arg, sizeof(u_req))){
        printk("{-} Some error in copy_from_user!");
        return result;
    }

    tbuf = (char*) kmalloc(uReq->size, GFP_KERNEL);

    switch(cmd) {
        case WRITE:
            copy_from_user(tbuf, uReq->data, uReq->size);
            memcpy_(ptr, tbuf, uReq->size);
            result = WRITE;
            break;
        case READ:
            memcpy_(tbuf, ptr, uReq->size);
            copy_to_user(uReq->data, tbuf, uReq->size);
            result = READ;
            break;
        default:
            result = 1338;
            break;
    }

    kfree(uReq);
    return result;
};


static noinline void memcpy_(void* dst, void* src, size_t size) {
    size_t i = 0;

    for (i = 0; i < size; i += 1) {
        *(uint8_t*)(dst+i) = *(uint8_t*)(src+i);
    }
}

static int __init init_dev(void){
    reg = misc_register(&kernel_pwn_dev);
    if (reg < 0){
        printk("[-] Failed to register secure_notes!");
    }
    return 0;
};

static void __exit exit_dev(void){
    misc_deregister(&kernel_pwn_dev);
}

module_init(init_dev);
module_exit(exit_dev);
