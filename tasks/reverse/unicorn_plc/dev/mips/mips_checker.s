	.file	1 "mips_checker.c"
	.section .mdebug.abi32
	.previous
	.nan	legacy
	.module	fp=xx
	.module	nooddspreg
	.abicalls
	.text
	.align	2
	.globl	mips_checker
	.set	nomips16
	.set	nomicromips
	.ent	mips_checker
	.type	mips_checker, @function
mips_checker:
	.frame	$fp,8,$31		# vars= 0, regs= 1/0, args= 0, gp= 0
	.mask	0x40000000,-4
	.fmask	0x00000000,0
	.set	noreorder
	.set	nomacro
	addiu	$sp,$sp,-8
	sw	$fp,4($sp)
	move	$fp,$sp
	sw	$4,8($fp)
	lw	$3,8($fp)
	li	$2,-559087616			# 0xffffffffdead0000
	ori	$2,$2,0xbeef
	xor	$2,$3,$2
	sw	$2,8($fp)
	lw	$3,8($fp)
	li	$2,-889323520			# 0xffffffffcafe0000
	ori	$2,$2,0xc411
	xor	$2,$3,$2
	sw	$2,8($fp)
	lw	$3,8($fp)
	li	$2,1554055168			# 0x5ca10000
	ori	$2,$2,0xab1e
	xor	$2,$3,$2
	sw	$2,8($fp)
	lw	$3,8($fp)
	li	$2,322371584			# 0x13370000
	ori	$2,$2,0x1337
	xor	$2,$3,$2
	sw	$2,8($fp)
	lw	$3,8($fp)
	li	$2,444268544			# 0x1a7b0000
	ori	$2,$2,0xb5cd
	bne	$3,$2,$L2
	nop

	li	$2,1			# 0x1
	.option	pic0
	b	$L3
	nop

	.option	pic2
$L2:
	move	$2,$0
$L3:
	move	$sp,$fp
	lw	$fp,4($sp)
	addiu	$sp,$sp,8
	jr	$31
	nop

	.set	macro
	.set	reorder
	.end	mips_checker
	.size	mips_checker, .-mips_checker
	.rdata
	.align	2
$LC0:
	.ascii	"%d\012\000"
	.text
	.align	2
	.globl	main
	.set	nomips16
	.set	nomicromips
	.ent	main
	.type	main, @function
main:
	.frame	$fp,32,$31		# vars= 0, regs= 2/0, args= 16, gp= 8
	.mask	0xc0000000,-4
	.fmask	0x00000000,0
	.set	noreorder
	.set	nomacro
	addiu	$sp,$sp,-32
	sw	$31,28($sp)
	sw	$fp,24($sp)
	move	$fp,$sp
	lui	$28,%hi(__gnu_local_gp)
	addiu	$28,$28,%lo(__gnu_local_gp)
	.cprestore	16
	li	$2,-1430585344			# 0xffffffffaabb0000
	ori	$4,$2,0xccdd
	.option	pic0
	jal	mips_checker
	nop

	.option	pic2
	lw	$28,16($fp)
	move	$5,$2
	lui	$2,%hi($LC0)
	addiu	$4,$2,%lo($LC0)
	lw	$2,%call16(printf)($28)
	move	$25,$2
	.reloc	1f,R_MIPS_JALR,printf
1:	jalr	$25
	nop

	lw	$28,16($fp)
	move	$2,$0
	move	$sp,$fp
	lw	$31,28($sp)
	lw	$fp,24($sp)
	addiu	$sp,$sp,32
	jr	$31
	nop

	.set	macro
	.set	reorder
	.end	main
	.size	main, .-main
	.ident	"GCC: (Ubuntu 9.4.0-1ubuntu1~20.04) 9.4.0"
