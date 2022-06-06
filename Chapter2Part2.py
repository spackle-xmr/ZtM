# built off https://github.com/coinstudent2048/ecc_tutorials

from dumb25519 import Scalar, Point
import dumb25519

q=dumb25519.q
d=dumb25519.d
G=dumb25519.G


def double_and_add_scalar_product(a_scalar, p):
    #a_binary = bin(a_scalar)
    bits = [(a_scalar >> i) & 1 for i in range(260)]
    #print(bits)
    r = Point(0,1)
    s = Point(p.x,p.y)
    for i in range(len(bits)-3):
        if(bits[i]==1): #step 2(a)
            r = r + s
            #print(p)
            #print(r)
        s = s + s #step 2(b)
    #print(len(bits))
    return r #step 3





'''
#Get example n
example_n = dumb25519.random_scalar()
print('value ',example_n)

#Get R=nP

done=double_and_add_scalar_product(example_n.x, G)
done_check= example_n * G
print('result = ',done.y)
print('check =  ',done_check.y)
'''


'''
# 2.3.2 Private to Public Key

k= dumb25519.random_scalar() #to pick random 

K= k * G
print(K.y)
'''


'''
# 2.3.3 Diffie-Hellman: Simple
alice=Scalar(867) #= dumb25519.random_scalar() #to pick random 
bob=Scalar(5309) #= dumb25519.random_scalar() #to pick random 
alice_public=alice * G
bob_public=bob * G

alice_S=bob_public * alice
bob_S=alice_public * bob

if alice_S == bob_S:
    print('DH success')
'''



'''
# 2.3.4 Schnorr Signatures

# P proves knowledge of k to V without revealing anything about it

# P starts with private/public key pair
k=dumb25519.random_scalar()
K= k * G

# 1. P generates random int within Z_l and compute alpha * G
alpha=dumb25519.random_scalar()
alphaG=alpha * G

# 2. V generates challenge with alpha * G now published
c=dumb25519.random_scalar()

# 3. P generates response
r=alpha + c * k

# 4. V computes and checks result
R=r * G
Rprime=alpha * G + c * K

if R == Rprime:
    print("Verified")



 #Uncomment with previous section
# If P reuses alpha we get two responses & two challenges to solve for k

# V sends another challenge
cprime=dumb25519.random_scalar()

# P generates another response with alpha (the fool!)
rprime=alpha + cprime * k

# Set of challenges and responses used to calculate private key
k_numera = r - rprime 
k_denome = c - cprime
k_solution = k_numera * k_denome.invert()

if k == k_solution:
    print("Oh no")

#print(k)
#print(k_solution)
'''



'''
# Fiat-Shamir Transform generates challenge with a hash function instead, making process
# non-interactive and publicly verifiable

# Non-interactive proof

# P starts with private/public key pair
k=dumb25519.random_scalar()
K= k * G

# 1. P generates random int within Z_l and compute alpha * G
alpha=dumb25519.random_scalar()
alphaG=alpha * G

# 2. P calculates challenge using cryptographically secure hash function
c=dumb25519.hash_to_scalar(alphaG)

# 3. P defines response
r=alpha + c * k

# 4. P publishes proof including alpha * G and response
proof=(alphaG, r)

#Verification

# 1. calculate challenge from proof (same as #2 above)
cprime=dumb25519.hash_to_scalar(proof[0]) #proof[0] == alphaG

# 2. Compute R and Rprime from proof
R=proof[1] * G #proof[1] == r
Rprime=alphaG + cprime * K

# 3. Check R == Rprime
if R == Rprime:
    print("Publically Verified P knows k")
'''



'''
# 2.3.5 Signing messages

# Alice starts with private/public key pair and message m
k=dumb25519.random_scalar()
K= k * G
m="I said this, noone else."

# 1. Alice generates random int within Z_l and compute alpha * G
alpha=dumb25519.random_scalar()
alphaG=alpha * G

# 2. Calculate challenge using message hash
c=dumb25519.hash_to_scalar(m, alphaG)

# 3. Define response using alpha and private key
r=alpha - c * k

# 4. Publish signature
signature=(c,r)

# Verification

# 1. Calculate challenge using signature, m, G, K
alphaG_equivalent = signature[1] * G + signature[0] * K #signature [0] == c , signature[1] == r
cprime=dumb25519.hash_to_scalar(m, alphaG_equivalent)

# 2. Check c = cprime
if c == cprime:
    print("Signature Passes")
'''


'''
# 2.4.2 Point Compression


def xfrompoint_ztm(pointcheck): #Function receives Point, calculates x coordinate via 2.4.2
    ypbytes=bytearray.fromhex(repr(pointcheck))
    biny = bin(int.from_bytes(ypbytes, "little"))[2:].zfill(256)
    b = biny[0]
    newbin = biny[1:]
    newy = '0' + newbin
    y = int(newy,2)
    xp = 0

    u = (y*y - 1) % q 
    v = (d*y*y + 1) % q
    z = (u * v**3) * pow(u*v**7,((q-5)//8), q) % q

    if ((v*z**2) % q) == (u % q):
        xp = (z % q)
    if ((v*z**2) % q) == (-u % q):
        xp = z * pow(2,((q-1)//4), q) % q
    
    if b != bin(xp)[-1]:
        return -xp % q
    else:
        return xp % q


def xfromy_ztm(yp): #Function receives integer y value, calculates x coordinate via 2.4.2
    biny = bin(yp)[2:].zfill(256) 
    b = biny[0]
    newbin = biny[1:]
    newy = '0' + newbin
    y = int(newy,2) # step 1
    xp = 0

    u = (y*y - 1) % q # step 2
    v = (d*y*y + 1) % q
    z = (u * v**3) * pow(u*v**7,((q-5)//8), q) % q # step 3

    if ((v*z**2) % q) == (u % q): # step 3(a)
        xp = (z % q)
    if ((v*z**2) % q) == (-u % q): # step 3(b)
        xp = z * pow(2,((q-1)//4), q) % q
    
    if b != bin(xp)[-1]: # step 4 & 5
        return -xp % q
    else:
        return xp % q



# note difference between K.y and int.from_bytes(bytearray.fromhex(repr(K)),"little")
K=dumb25519.random_point()
Kint=int.from_bytes(bytearray.fromhex(repr(K)),"little")
builtinx=dumb25519.xfromy(K.y)
xcalc=xfrompoint_ztm(K)
xycalc=xfromy_ztm(Kint)
print('K.y=',K.y)
print('K.x=',K.x)
print('xfromy=',builtinx)
print('xfrompoint=',xcalc)
print('xfromy_ztm=',xycalc)
'''


'''
# 2.4.3 EdDSA signature algorithm

# Python from ZtM reference 75 is it's own whole thing... gunna leave it alone

# Signature

# Signer starts with private/public key pair and message
k=dumb25519.random_scalar()
K= k * G
m="Very important message."

# 1. Create hash of private key, then create hash of result and message
h=dumb25519.hash_to_scalar(k)
alpha=dumb25519.hash_to_scalar(h,m)

# 2. Calculate alpha * G and channge ch
alphaG=alpha * G
ch=dumb25519.hash_to_scalar(alphaG,K,m)

# 3. Calculate the response
r=alpha + ch * k

# 4. Create signature
signature=(alphaG,r)


# Verification

# 1. Compute chprime
chprime=dumb25519.hash_to_scalar(alphaG,K,m)

# 2. Check equality
c=3 #?
twoc_scalar=Scalar(2**c)
left=twoc_scalar * r * G
right=twoc_scalar * alphaG + twoc_scalar * chprime * K

if left == right:
    print("Signature is Valid")
'''


'''
# 2.5 Binary operator XOR

a=0b11
b=0b10
c=a^b
print('c=',bin(c))
'''
