# plase at start user value to $v1
lui $v0, 0xdead
ori $v0, $v0, 0xbeef
xor $v1, $v0, $v1

lui $v0, 0xcafe
ori $v0, $v0, 0xc411
xor $v1, $v0, $v1

lui $v0, 0x5ca1
ori $v0, $v0, 0x4b1e
xor $v1, $v0, $v1

lui $v0, 0x1337
ori $v0, $v0, 0x1337
xor $v1, $v0, $v1

lui $v0, 0x1a7b
ori $v0, $v0, 0x55cd
bne $v1, $v0, $BOEQ

li $v1, 1
b $END
$BOEQ:
li $v1, 0
$END:
nop
# get result fron $v1

# "\x3c\x02\xde\xad\x34\x42\xbe\xef\x00\x43\x18\x26\x3c\x02\xca\xfe\x34\x42\xc4\x11\x00\x43\x18\x26\x3c\x02\x5c\xa1\x34\x42\x4b\x1e\x00\x43\x18\x26\x3c\x02\x13\x37\x34\x42\x13\x37\x00\x43\x18\x26\x3c\x02\x1a\x7b\x34\x42\x55\xcd\x14\x62\x00\x04\x00\x00\x00\x00\x24\x03\x00\x01\x10\x00\x00\x02\x00\x00\x00\x00\x24\x03\x00\x00\x00\x00\x00\x00"

# https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'Hex','string':'deadbeef'%7D,'Standard',false)XOR(%7B'option':'Hex','string':'cafec411'%7D,'Standard',false)XOR(%7B'option':'Hex','string':'5ca14b1e'%7D,'Standard',false)XOR(%7B'option':'Hex','string':'13371337'%7D,'Standard',false)To_Hex('None',0)&input=NDFiZTc3MWE