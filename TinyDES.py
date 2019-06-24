import math 
KEY = '1111110111010000'
tabelaSBoxLeft = [[6,9,10,3,4,13,7,8,14,1,2,11,5,12,15,0],
                  [9,14,11,10,4,5,0,7,8,6,3,2,12,13,1,15],
                  [8,1,12,2,13,3,14,15,0,9,5,10,4,11,6,7],
                  [9,0,2,5,10,13,6,14,1,8,11,12,3,4,7,15]]

tabelaSBoxRight = [[12,5,0,10,14,7,2,8,13,4,3,9,6,15,1,11],
                       [1,12,9,6,3,14,11,2,15,8,4,5,13,10,0,7],
                       [15,10,14,6,13,8,2,4,1,7,9,0,3,5,11,12],
                       [0,10,3,12,8,2,1,14,9,7,15,6,11,5,13,4]]

#recebe um texto e retorna um array de blocos de 16 bits
def dividirEmBlocos(st):
    bin = ''.join(format(ord(x),'08b') for x in st)

    nBitsParaCompletar = 16 - (len(bin)+8)%16
    BitsParaCompletar = '0'*nBitsParaCompletar
    nBitsParaCompletarEmBinario = format(nBitsParaCompletar,'08b')
    bin = nBitsParaCompletarEmBinario + BitsParaCompletar + bin
    
    return [bin[i:i+16] for i in range(0, len(bin), 16)]

def blocosParaString(blocos):
    st = ''.join(blocos)
    nBitsZero = st[:8]
    nBitsZero = int(nBitsZero,2)
    st = st[8+nBitsZero:]
    st = [st[i:i+8] for i in range(0, len(st), 8)]
    st = ''.join([chr(int(x,2)) for x in st])
    return st


#recebe uma string de 16 bits e retorna ela cifrada
def cifrar16(bloco,chave=KEY,decifra = 1):
    keys = quebraChave(chave)[::decifra]
    for key in keys:
        l,r = divideBlocoEmDois(bloco)
        vaiSerOl = r
        r = expand(r)
        r = format( int(r,2) ^ int(key,2),'012b')
        rl,rr = divideBlocoEmDois(r)
        rl = sBox(rl,tabelaSBoxLeft)
        rr = sBox(rr,tabelaSBoxRight)
        r = rl + rr
        r = format( int(r,2) ^ int(l,2),'08b')
        bloco = vaiSerOl + r
    return bloco

def decifra16(bloco,chave=KEY):
    l,r = divideBlocoEmDois(bloco)
    x  = cifrar16(r+l,chave,-1)
    l,r = divideBlocoEmDois(x)
    return r + l
#divide um bloco em dois
def divideBlocoEmDois(bloco):
    return (bloco[0:math.floor(len(bloco)/2)],bloco[math.floor(len(bloco)/2):])

#as Sbox
def sBox(meioBloco,tabela):
    y = int(meioBloco[0] + meioBloco[5],2)
    x = int(meioBloco[1] +
            meioBloco[2] +
            meioBloco[3] +
            meioBloco[4],2)
    return bin(tabela[y][x])[2:]
#recebe meio bloco (8 bits) e retorna 12 bits
def expand(meioBloco):
    meioBlocoExpandida = ''
    mascara = [4,7,2,1,5,7,0,2,6,5,0,3]
    for i in mascara:
        meioBlocoExpandida += meioBloco[i]
    return meioBlocoExpandida

def applymasc(bloco,mascara):
    resultado = ''
    for i in mascara:
        resultado += bloco[i]
    return resultado
#quebra chave em 4  
def quebraChave(chave):
    m = []
    m.append( [2,4,5,6,7,1,10,11,12,14,15,8])
    m.append([4,6,7,0,1,3,11,12,13,15,8,9])
    m.append([6,0,1,2,3,5,12,13,14,8,9,10])
    m.append([0,2,3,4,5,7,13,14,15,9,10,11])
    chaves = [applymasc(chave,x) for x in m]
    return chaves 

def teste():
    num = []
    errou = 0
    for i in range(2**16):
        num = format(i,'016b')
        c = cifrar16(num,'0111010101010101')
        d = decifra16(c,'0111010101010101')
        if(d != num):
            print("n é q errou mesmo")
def main():
    # mensagem = input("digite uma mensagem: ")
    # BlocosMsg = dividirEmBlocos(mensagem)
    # msgEncriptada = [cifrar16(i,KEY) for i in BlocosMsg]
    # msgStr = ''.join(msgEncriptada)
    # print('\n\nmensagem cifrada:')
    # print('\nbinary:')
    # print(msgStr)
    # print('\nhex:')
    # print(str(hex(int(msgStr, 2))))

    # msgDecifrada = [decifra16(i,KEY) for i in msgEncriptada]
    # msgDecifrada = blocosParaString(msgDecifrada)
    # print("\nmensagem decifrada: " + msgDecifrada)
    print(cifrar16('1001110100111100'))


if (__name__ == '__main__'):
    main()