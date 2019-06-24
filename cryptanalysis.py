from TinyDES import *

ITERATIONS=10000
PLAIN_TEST='1001110100111100'

def recoverySubkey():
  count = [0] * 64

  for i in range(ITERATIONS):
    PBase = format(i,'015b')
    P = PBase[0:14] + '0' + PBase[-1]
    Plinha = PBase[0:14] + '1' + PBase[-1]

    C = cifrar16(P)
    Clinha = cifrar16(Plinha)

    if (format(int(C, 2) ^ int(Clinha, 2), '016b') == '0000001000000010'):
      smallC = C[0] + C[2] + C[6] + C[5] + C[0] + C[3]
      smallClinha = Clinha[0] + Clinha[2] + Clinha[6] + Clinha[5] + Clinha[0] + Clinha[3]
      
      for k in range(64):
        sBoxC = sBox(format(int(smallC, 2) ^ int(k), '06b'), tabelaSBoxRight)
        sBoxClinha = sBox(format(int(smallClinha, 2) ^ int(k), '06b'), tabelaSBoxRight)

        if(format(int(sBoxC, 2) ^ int(sBoxClinha, 2), '04b') == '0010'):
          count[k] += 1


  for i in range(64):
   print(str(i) + ' ' + str(count[i]))
  maxCount = max(count)
  print(maxCount)
  possibleKeys = []
  for index,i in enumerate(count):
    if i == maxCount:
      possibleKeys.append(format(index,'06b'))

  # possibleKeys = ['01100', '10101']
  print(possibleKeys)

  for keyPart in possibleKeys:
    for i in range(2**10):
      restKey = format(i, '010b')
      possibleKey = \
        restKey[0] + restKey[1] + restKey[2] + restKey[3] + restKey[4]  + \
        restKey[5] + restKey[6] + restKey[7] + restKey[8] + keyPart[3]  + \
        keyPart[4] + keyPart[5] + restKey[9] + keyPart[0] + keyPart[1] + \
        keyPart[2]



      if(possibleKey == '1111110111010000'):
        print('foi')

      cifrado = cifrar16(PLAIN_TEST)
      decifrado = decifra16(cifrado, possibleKey)

      if(decifrado == PLAIN_TEST):
        print('Chave: '+ str(possibleKey))
        break
      
def main():
  recoverySubkey()

if (__name__ == '__main__'):
    main()