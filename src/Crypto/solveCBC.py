token = "d5f4a79d3fd8d17320acda3e93884b59e1d9fb322de7027be8a3829b9340861a"
iv = bytes.fromhex(token[:32])
token1 = b'HUSTCTFer!______'
token2 = b'AdminAdmin!_____'
iv2 = b''
for i in range(16):
    k = token1[i]^token2[i]^iv[i] # 先异或原来的明文抵消掉原明文，再异或替换的明文
    iv2 += k.to_bytes()
iv = iv2
token = iv.hex() + token[32:]
print(token)