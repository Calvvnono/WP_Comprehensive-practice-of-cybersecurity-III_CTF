from Crypto.Util.number import *
from sage.all import *

def is_printable(s):
    for char in s:
        if not char == ' ' and not char.isprintable():
            return False
    return True

# 密文数据
raw = b'>u\x10l9\npI,0\x04^J\x00ib\x03\x0c\x158d\x1f\x08Ixk\nF\x19fz\x14PT\x04\x03>R~'
rawi = [int(x) for x in raw]

# 明文 "vmc{}" 对应的 ASCII 数字
# "vmc" 对应 [118, 109, 99]
# "{ }" 对应 [123, 32, 32]
# 用补充的空格来填充（ASCII 32为空格）
c = matrix(Zmod(127), 3, 3 , [118, 109, 99, 123, 0, 0, 125, 32, 32])

# 密文 " >u\x10 " 对应的 ASCII 数字
# ">u\x10" 对应 [62, 117, 16]
# "l9\n" 对应 [108, 57, 10]
# "pI," 对应 [112, 73, 44]
# 所有值通过 ASCII 转换
p = matrix(Zmod(127), 3, 3 , [62, 117, 16, 108, 57, 10, 62, 82, 126])

# 穷举方法尝试爆破两个未知数
for i in range(127):
    for j in range(127):
        c[1,1] = j
        c[1,2] = i
        flag = True
        if c.is_invertible():  # 如果矩阵可逆，则尝试解
            K = c.solve_right(p)  # 求得加密矩阵K
            decode = ''
            for k in range(13):
                # 每 3 个字节处理一次密文块
                tmp = matrix(Zmod(127), 1, 3 , rawi[k*3:(k+1)*3])
                A = K.solve_left(tmp)  # 使用加密矩阵 K 解密
                for l in range(3):
                    char = chr(A[0,l])
                    if not char == ' ' and not char.isprintable():  # 检查是否为可打印字符
                        flag = False
                        break
                    decode += char
            if flag:  # 如果解密过程没有问题，输出结果
                print(f"解密后的明文：{decode}")
                break
