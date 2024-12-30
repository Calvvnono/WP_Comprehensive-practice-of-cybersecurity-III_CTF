import socket
from Crypto.Util.number import *
import gmpy2

# 这里设置你申请的环境的IP和端口号
HOST = '10.12.153.73'
PORT = 10224

p = 1255652507375424180771153661593175450240095099309617997830398479481251473806248999027009487987474628937865240529484483880639448709701174539063275550960844784506422070337433308527616053480228338110351562500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    msg = s.recv(1024).decode()
    s.send((str(p)+'\n').encode())
    msg = s.recv(1024).decode()
    A = gmpy2.mpz(msg.split(": ")[1].strip())
    msg = s.recv(1024).decode()
    B = gmpy2.mpz(msg.split("Bob公钥: ")[1].split("\n")[0].strip())
    m = gmpy2.mpz(msg.split("密文: ")[1].strip())
    print(f"A = {A}")
    print(f"B = {B}")
    print(f"m = {m}")
    print(f"p = {p}")

'''
A = 355669952921034267831168541396567338166363947361450219963530670142687154164278499711963689789931667207960303928644101973338721608009019378529002236001354163677946386844933203453073205489158777257835345405122620355189693067109336813677425279853274540753847346090117570519936576319829093516256630287227380835834438884042941842672591004254247265449059753546783624217188034293412170221475955127046619991959632722679225589581470575106694
B = 4992551235074421871387972107968363771487136233276180239286246353689116359919410725041440739723408220491150036255059188021684456127922797856578063653007508543762038252915287314177885710762029828656129272330513550260038681775995929558879880649055420782855871380114208676073334623012899162425011870026150202171063960907783143952078876819868496068228454956523392683249724797267889518106109240459463770234197103729380352444944674569942
m = 529905113648101891970936246144584619026712228170489544108250303351975726498967447469928715993635197350465528008213412604954544642112322932091016935939664407327069321404497425823323811343729108388418224967949337788356272012533097878402642053780546701312232145530937593063913656091383846555658677949338255392032614254214581291911487366810137132348740515477804813556580096985377993909891228820887237253011458755426767833584560979924277
p = 1255652507375424180771153661593175450240095099309617997830398479481251473806248999027009487987474628937865240529484483880639448709701174539063275550960844784506422070337433308527616053480228338110351562500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001
'''