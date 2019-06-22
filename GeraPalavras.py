import TinyDes.py
numeros = []
for i in range(2**15):
    num = format(i,'015b')
    P = num[0:14] + '0' + num[-1]
    Plinha = num[0:14] + '1' + num[-1]
    numeros.append(P + ' ' +Plinha)


