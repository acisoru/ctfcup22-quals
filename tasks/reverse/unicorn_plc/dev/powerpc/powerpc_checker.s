	.file	"powerpc_checker.c"
	.machine ppc
	.section	".text"
	.align 2
	.globl ppc_checker
	.type	ppc_checker, @function
ppc_checker:
.LFB0:
	.cfi_startproc
	stwu 1,-48(1)
	.cfi_def_cfa_offset 48
	stw 31,44(1)
	.cfi_offset 31, -4
	mr 31,1
	.cfi_def_cfa_register 31
	lis 9,0x9c13
	ori 9,9,0x37a6
	
	stw 9,12(31)
	lwz 9,12(31)
	srwi 9,9,24
	rlwinm 9,9,0,0xff
	stb 9,16(31)
	lwz 9,12(31)
	srawi 9,9,16
	rlwinm 9,9,0,0xff
	stb 9,17(31)
	lwz 9,12(31)
	srawi 9,9,8
	rlwinm 9,9,0,0xff
	stb 9,18(31)
	lwz 9,12(31)
	rlwinm 9,9,0,0xff
	stb 9,19(31)
	lis 9,0x4a11
	ori 9,9,0xc0ef
	stw 9,20(31)
	lis 9,0x90ba
	ori 9,9,0x1302
	stw 9,24(31)
	li 9,0
	stw 9,8(31)
	b .L2
.L3:
	addi 10,31,24
	lwz 9,8(31)
	add 9,10,9
	lbz 10,0(9)
	addi 8,31,16
	lwz 9,8(31)
	add 9,8,9
	lbz 9,0(9)
	mullw 9,10,9
	rlwinm 10,9,0,0xff
	addi 8,31,20
	lwz 9,8(31)
	add 9,8,9
	lbz 9,0(9)
	add 9,10,9
	rlwinm 10,9,0,0xff
	addi 8,31,16
	lwz 9,8(31)
	add 9,8,9
	stb 10,0(9)
	lwz 9,8(31)
	addi 9,9,1
	stw 9,8(31)
.L2:
	lwz 9,8(31)
	cmpwi 0,9,3
	ble 0,.L3
	lbz 9,16(31)
	cmplwi 0,9,10
	bne 0,.L4
	lbz 9,17(31)
	cmplwi 0,9,223
	bne 0,.L4
	lbz 9,18(31)
	xori 9,9,0xd5
	cntlzw 9,9
	srwi 9,9,5
	rlwinm 10,9,0,0xff
	lbz 9,19(31)
	xori 9,9,0x3b
	cntlzw 9,9
	srwi 9,9,5
	rlwinm 9,9,0,0xff
	and 9,10,9
	rlwinm 9,9,0,0xff
	cmpwi 0,9,0
	beq 0,.L4
	li 9,1
	b .L6
.L4:
	li 9,0
.L6:
	mr 3,9
	addi 11,31,48
	lwz 31,-4(11)
	.cfi_def_cfa 11, 0
	mr 1,11
	.cfi_restore 31
	.cfi_def_cfa_register 1
	blr
	.cfi_endproc
.LFE0:
	.size	ppc_checker,.-ppc_checker
	.align 2
	.globl _start
	.type	_start, @function
_start:
.LFB1:
	.cfi_startproc
	stwu 1,-16(1)
	.cfi_def_cfa_offset 16
	mflr 0
	stw 0,20(1)
	stw 31,12(1)
	.cfi_offset 65, 4
	.cfi_offset 31, -4
	mr 31,1
	.cfi_def_cfa_register 31
	bl ppc_checker
	mr 9,3
	mr 3,9
	addi 11,31,16
	lwz 0,4(11)
	mtlr 0
	lwz 31,-4(11)
	.cfi_def_cfa 11, 0
	mr 1,11
	.cfi_restore 31
	.cfi_def_cfa_register 1
	blr
	.cfi_endproc
.LFE1:
	.size	_start,.-_start
	.ident	"GCC: (Ubuntu 9.4.0-1ubuntu1~20.04.1) 9.4.0"
	.section	.note.GNU-stack,"",@progbits
