cmd_/home/dev/ctfcup2022/kernelpwn/dev/Module.symvers := sed 's/ko$$/o/' /home/dev/ctfcup2022/kernelpwn/dev/modules.order | scripts/mod/modpost -m -a  -o /home/dev/ctfcup2022/kernelpwn/dev/Module.symvers -e -i Module.symvers   -T -
