cmd_/home/dev/ctfcup2022/kernelpwn/dev/modules.order := {   echo /home/dev/ctfcup2022/kernelpwn/dev/kernel_pwn.ko; :; } | awk '!x[$$0]++' - > /home/dev/ctfcup2022/kernelpwn/dev/modules.order
