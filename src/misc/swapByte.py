def swap_endian(filename, new_filename):
    with open(filename, 'rb') as original_file, open(new_filename, 'wb') as new_file:
        while True:
            # 读取4字节
            bytes_read = original_file.read(4)
            if not bytes_read:  # 如果没有读取到数据，表示文件结束
                break  # 跳出循环
            # 大小端转换，通过切片翻转字节序
            swapped_bytes = bytes_read[::-1]
            # 写入新文件
            new_file.write(swapped_bytes)

# 使用示例
swap_endian("WhoAreYou.jpg", "out.jpg")
