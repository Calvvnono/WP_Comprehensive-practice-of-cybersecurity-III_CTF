import socket
import hashlib
from ecdsa import ecdsa as ec

# 已知参数
N = ec.generator_192.order()
r = 4602663246806817676753764620691597969452322302394314855333
s1 = 1501918255985409722174552207703420548040311184115000968900
h1 = 217021246783606243167148604888781092806
s2 = 3855389277850218272055897690931945277969062284217918469713
h2 = 128731416951084210800762839995065393670

# 计算 k (nonce)
def calculate_nonce(r, s1, h1, s2, h2, N):
    k = ((h2 - h1) * pow(s2 - s1, -1, N)) % N
    return k

# 计算 r * d_A (私钥乘以 r)
def calculate_r_da(r, s1, k, h1, N):
    r_da = (s1 * k - h1) % N
    return r_da

# 构造伪造签名
def forge_signature(r, r_da, k, message_hash, N):
    s = ((message_hash + r_da) * pow(k, -1, N)) % N
    return r, s

if __name__ == "__main__":
    # 计算 nonce (k)
    k = calculate_nonce(r, s1, h1, s2, h2, N)
    print("Recovered nonce (k):", k)

    # 计算 r * d_A
    r_da = calculate_r_da(r, s1, k, h1, N)
    print("Recovered r * d_A:", r_da)

    time_str = "15:08:32:get_flag"
    message_hash = int(hashlib.md5(f"{time_str}".encode()).hexdigest(), 16)
    # 伪造签名
    forged_r, forged_s = forge_signature(r, r_da, k, message_hash, N)
    print(f"{forged_r},{forged_s}")

