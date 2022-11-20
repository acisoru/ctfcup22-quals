#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/slab.h>
#include <linux/uaccess.h>
#include <linux/miscdevice.h> 
#include <linux/random.h>

MODULE_AUTHOR("revker@localhost");                    
MODULE_DESCRIPTION("Kernel pwn");
MODULE_LICENSE("GPL");

#define BUF_SIZE 512

#define WRITE  0x1001
#define READ   0x2002

int reg;

typedef struct{
    char* data;
    int size;
} u_req;

static noinline void memcpy_(void* dst, void* src, size_t size);
static noinline long ioctlHandler(struct file *file, unsigned int cmd, unsigned long arg);
static struct file_operations kernel_pwn_fops = {.unlocked_ioctl = ioctlHandler}; 

struct miscdevice kernel_pwn_dev = {
    .minor = MISC_DYNAMIC_MINOR,
    .name = "kernel_pwn",
    .fops = &kernel_pwn_fops,
};
