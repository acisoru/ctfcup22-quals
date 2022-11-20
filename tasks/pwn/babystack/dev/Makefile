
obj-m += kernel_pwn.o
KVERSION = 6.0.7
#ccflags-y := -O0

all:
	make -C /home/dev/linux-6.0.7/ M=$(PWD) modules
clean:
	make -C /home/dev/linux-6.0.7/ M=$(PWD) clean

