	.file	"spark_checker.c"
	.section	".text"
	.align 4
	.global reverse
	.type	reverse, #function
	.proc	016
reverse:
	save	%sp, -104, %sp
	sethi	%hi(-2056122368), %g1
	or	%g1, 310, %g1
	st	%g1, [%fp-4]
	ld	[%fp-4], %g1
	add	%g1, %g1, %g1
	mov	%g1, %g2
	sethi	%hi(-1431656448), %g1
	or	%g1, 682, %g1
	and	%g2, %g1, %g2
	ld	[%fp-4], %g1
	srl	%g1, 1, %g3
	sethi	%hi(1431655424), %g1
	or	%g1, 341, %g1
	and	%g3, %g1, %g1
	or	%g2, %g1, %g1
	st	%g1, [%fp-4]
	ld	[%fp-4], %g1
	sll	%g1, 2, %g2
	sethi	%hi(-858993664), %g1
	or	%g1, 204, %g1
	and	%g2, %g1, %g2
	ld	[%fp-4], %g1
	srl	%g1, 2, %g3
	sethi	%hi(858992640), %g1
	or	%g1, 819, %g1
	and	%g3, %g1, %g1
	or	%g2, %g1, %g1
	st	%g1, [%fp-4]
	ld	[%fp-4], %g1
	sll	%g1, 4, %g2
	sethi	%hi(-252645376), %g1
	or	%g1, 240, %g1
	and	%g2, %g1, %g2
	ld	[%fp-4], %g1
	srl	%g1, 4, %g3
	sethi	%hi(252644352), %g1
	or	%g1, 783, %g1
	and	%g3, %g1, %g1
	or	%g2, %g1, %g1
	st	%g1, [%fp-4]
	ld	[%fp-4], %g1
	sll	%g1, 24, %g2
	ld	[%fp-4], %g1
	sll	%g1, 8, %g3
	sethi	%hi(16711680), %g1
	and	%g3, %g1, %g1
	or	%g2, %g1, %g2
	ld	[%fp-4], %g1
	srl	%g1, 8, %g3
	sethi	%hi(64512), %g1
	or	%g1, 768, %g1
	and	%g3, %g1, %g1
	or	%g2, %g1, %g2
	ld	[%fp-4], %g1
	srl	%g1, 24, %g1
	or	%g2, %g1, %g1
	st	%g1, [%fp-4]
	ld	[%fp-4], %g2
	sethi	%hi(1820871680), %g1
	or	%g1, 673, %g1
	cmp	%g2, %g1
	bne	.L2
	 nop
	mov	1, %g1
	ba .L3
	 nop
.L2:
	mov	0, %g1
.L3:
	nop
	return	%i7+8
	 nop
	.size	reverse, .-reverse
	.align 4
	.global _start
	.type	_start, #function
	.proc	04
_start:
	save	%sp, -96, %sp
	call	reverse, 0
	 nop
	mov	%o0, %g1
	mov	%g1, %i0
	return	%i7+8
	 nop
	.size	_start, .-_start
	.ident	"GCC: (Ubuntu 9.4.0-1ubuntu1~20.04) 9.4.0"
	.section	.note.GNU-stack,"",@progbits

# "\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x82\x00\x40\x01\x84\x10\x00\x01\x03\x2a\xaa\xaa\x82\x10\x62\xaa\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x01\x03\x15\x55\x55\x82\x10\x61\x55\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x02\x03\x33\x33\x33\x82\x10\x60\xcc\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x02\x03\x0c\xcc\xcc\x82\x10\x63\x33\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x04\x03\x3c\x3c\x3c\x82\x10\x60\xf0\x84\x08\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x04\x03\x03\xc3\xc3\x82\x10\x63\x0f\x82\x08\xc0\x01\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc2\x07\xbf\xfc\x85\x28\x60\x18\xc2\x07\xbf\xfc\x87\x28\x60\x08\x03\x00\x3f\xc0\x82\x08\xc0\x01\x84\x10\x80\x01\xc2\x07\xbf\xfc\x87\x30\x60\x08\x03\x00\x00\x3f\x82\x10\x63\x00\x82\x08\xc0\x01\x84\x10\x80\x01\xc2\x07\xbf\xfc\x83\x30\x60\x18\x82\x10\x80\x01\xc2\x27\xbf\xfc\xc4\x07\xbf\xfc\x03\x1b\x22\x13\x82\x10\x62\xa1\x80\xa0\x80\x01\x82\x10\x20\x01\x10\x68\x00\x03\x01\x00\x00\x00\x82\x10\x20\x00\x01\x00\x00\x00"
