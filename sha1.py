import binascii

def main():
    print(hashSHA1(""))

def hashSHA1(s):
    a, b, c, d, e = "", "", "", "", ""
    h = {}
    h["0;0"] = "01100111010001010010001100000001"
    h["0;1"] = "11101111110011011010101110001001"
    h["0;2"] = "10011000101110101101110011111110"
    h["0;3"] = "00010000001100100101010001110110"
    h["0;4"] = "11000011110100101110000111110000"
    mBlocks = getChunks(complementM(s), 512)
    m = {}
    for i in range(1, len(mBlocks) + 1):
        for k in range(16):
            m[str(i) + ";" + str(k)] = getChunks(mBlocks[i - 1], 32)[k]
    T = ""
    for i in range(1, len(mBlocks) + 1):
        w = []
        for t in range(80):
            if(0<=t and t<=15):
                w += [m[str(i) + ";" + str(t)]]
            else:
                w += [rotl(1, binXor(w[t - 3], binXor(w[t-8], binXor(w[t - 14], w[t - 16]))))]
        a = h[str(i - 1) + ";0"]
        while(len(a)<32):
            a = "0" + a
        b = h[str(i - 1) + ";1"]
        while(len(b)<32):
            b = "0" + b
        c = h[str(i - 1) + ";2"]
        d = h[str(i - 1) + ";3"]
        e = h[str(i - 1) + ";4"]
        for t in range(80):
            T = addBin(rotl(5, a), addBin(fonctions(t, b, c, d), addBin(e, addBin(csteK(t), w[t]))))
            while(len(T)<32):
                T = "0" + T
            e = d
            d = c
            c = rotl(30, b)
            b = a
            a = T
        h[str(i) + ";0"] = addBin(a, h[str(i - 1) + ";0"])
        h[str(i) + ";1"] = addBin(b, h[str(i - 1) + ";1"])
        h[str(i) + ";2"] = addBin(c, h[str(i - 1) + ";2"])
        h[str(i) + ";3"] = addBin(d, h[str(i - 1) + ";3"])
        h[str(i) + ";4"] = addBin(e, h[str(i - 1) + ";4"])
    return (str(hex(int(h[str(len(mBlocks)) + ";0"], 2))) + str(hex(int(h[str(len(mBlocks)) + ";1"], 2))) + str(hex(int(h[str(len(mBlocks)) + ";2"], 2))) + str(hex(int(h[str(len(mBlocks)) + ";3"], 2))) + str(hex(int(h[str(len(mBlocks)) + ";4"], 2)))).replace("0x", "").replace("L", "")

def rotl(n, x):
    d = x[:n]
    e = x[n:]
    return e + d

def addBin(x,y):
        maxlen = max(len(x), len(y))
        x = x.zfill(maxlen)
        y = y.zfill(maxlen)
        result = ''
        carry = 0
        for i in range(maxlen-1, -1, -1):
            r = carry
            r += 1 if x[i] == '1' else 0
            r += 1 if y[i] == '1' else 0
            result = ('1' if r % 2 == 1 else '0') + result
            carry = 0 if r < 2 else 1       
        if carry !=0 : result = '1' + result
        l = bin2dec(result.zfill(maxlen))
        l %= 2**32
        return dec2bin(l)

def csteK(t):
    if(0<=t and t<=19):
        return "01011010100000100111100110011001"
    elif(20<=t and t<=39):
        return "01101110110110011110101110100001"
    elif(40<=t and t<=59):
        return "10001111000110111011110011011100"
    elif(60<=t and t<=79):
        return "11001010011000101100000111010110"
    
def fonctions(t, x, y, z):
    if(0<=t and t<=19):
        return binOr(binAnd(x, y), binAnd(binComplement(x), z))
    elif(20<=t and t<=39):
        return binXor(binXor(x, y), z)
    elif(40<=t and t<=59):
        return binOr(binOr(binAnd(x, y), binAnd(x, z)), binAnd(y, z))
    elif(60<=t and t<=79):
        return binXor(binXor(x, y), z)
 
def txt2bin(text):
    bits = bin(int(binascii.hexlify(text.encode('utf-8', 'surrogatepass')), 16))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def bin2txt(bits):
    n = int(bits, 2)
    return int2bytes(n).decode('utf-8', 'surrogatepass')

def int2bytes(i):
    hex_string = '%x' % i
    n = len(hex_string)
    return binascii.unhexlify(hex_string.zfill(n + (n & 1)))
    
def dec2bin(n):
    c = n
    b = ""
    while c:
        b = "{}".format(c%2) + b
        c = c//2
    return b

def bin2dec(b):
    d, k = 0, 1
    for i in range(len(b)-1, -1, -1):
        if b[i]=="1":
            d += k
        k *= 2
    return d

def binAnd(x, y):
    a = ""
    while len(x)!=len(y):
        if(len(x)<len(y)):
            x = "0" + x
        else:
            y = "0" + y
    for k in range(0, len(x)):
        if(x[k]=="1" and y[k]=="1"):
            a += "1"
        else:
            a += "0"
    return a

def binComplement(x):
    a = ""
    for k in range(0, len(x)):
        if(x[k]=="0"):
            a += "1"
        else:
            a += "0"
    return a

def binOr(x, y):
    a = ""
    while len(x)!=len(y):
        if(len(x)<len(y)):
            x = "0" + x
        else:
            y = "0" + y
    for k in range(0, len(x)):
        if(x[k]=="0" and y[k]=="0"):
            a += "0"
        else:
            a += "1"
    return a

def binXor(x, y):
    a = ""
    while len(x)!=len(y):
        if(len(x)<len(y)):
            x = "0" + x
        else:
            y = "0" + y
    for k in range(0, len(x)):
        if(x[k]=="0" and y[k]=="0"):
            a += "0"
        elif(x[k]=="1" and y[k]=="1"):
            a += "0"
        else:
            a += "1"
    return a

def complementM(m):
    m = txt2bin(m)
    l = len(m)
    k = (448 % 512) - (l + 1)
    while k<0:
        k += 512
    m += "1"
    for _ in range(k):
        m += "0"
    d = dec2bin(l)
    while(len(d)<64):
        d = "0" + d
    m += d
    return m

def getChunks(x, n):
    return [x[i:i+n] for i in range(0, len(x), n)]
    
if __name__ == '__main__':
    main()