# ed25519.py - Optimized version of the reference implementation of Ed25519
#
# Written in 2011? by Daniel J. Bernstein <djb@cr.yp.to>
#            2013 by Donald Stufft <donald@stufft.io>
#            2013 by Alex Gaynor <alex.gaynor@gmail.com>
#            2013 by Greg Price <price@mit.edu>
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see
# <http://creativecommons.org/publicdomain/zero/1.0/>.

"""
NB: This code is not safe for use with secret keys or secret data.
The only safe use of this code is for verifying signatures on public messages.

Functions for computing the public key of a secret key and for signing
a message are included, namely publickey_unsafe and signature_unsafe,
for testing purposes only.

The root of the problem is that Python's long-integer arithmetic is
not designed for use in cryptography.  Specifically, it may take more
or less time to execute an operation depending on the values of the
inputs, and its memory access patterns may also depend on the inputs.
This opens it to timing and cache side-channel attacks which can
disclose data to an attacker.  We rely on Python's long-integer
arithmetic, so we cannot handle secrets without risking their disclosure.
"""

import hashlib
import operator
import sys


__version__ = "1.0.dev0"


# Useful for very coarse version differentiation.
PY3 = sys.version_info[0] == 3

if PY3:
    indexbytes = operator.getitem
    intlist2bytes = bytes
    int2byte = operator.methodcaller("to_bytes", 1, "big")
else:
    int2byte = chr
    range = xrange  # noqa: F821

    def indexbytes(buf, i):
        return ord(buf[i])

    def intlist2bytes(l):
        return b"".join(chr(c) for c in l)


b = 256
q = 2**255 - 19
l = 2**252 + 27742317777372353535851937790883648493


def H(m):
    return hashlib.sha512(m).digest()


def pow2(x, p):
    """== pow(x, 2**p, q)"""
    while p > 0:
        x = x * x % q
        p -= 1
    return x


def inv(z):
    r"""$= z^{-1} \mod q$, for z != 0"""
    # Adapted from curve25519_athlon.c in djb's Curve25519.
    z2 = z * z % q  # 2
    z9 = pow2(z2, 2) * z % q  # 9
    z11 = z9 * z2 % q  # 11
    z2_5_0 = (z11 * z11) % q * z9 % q  # 31 == 2^5 - 2^0
    z2_10_0 = pow2(z2_5_0, 5) * z2_5_0 % q  # 2^10 - 2^0
    z2_20_0 = pow2(z2_10_0, 10) * z2_10_0 % q  # ...
    z2_40_0 = pow2(z2_20_0, 20) * z2_20_0 % q
    z2_50_0 = pow2(z2_40_0, 10) * z2_10_0 % q
    z2_100_0 = pow2(z2_50_0, 50) * z2_50_0 % q
    z2_200_0 = pow2(z2_100_0, 100) * z2_100_0 % q
    z2_250_0 = pow2(z2_200_0, 50) * z2_50_0 % q  # 2^250 - 2^0
    return pow2(z2_250_0, 5) * z11 % q  # 2^255 - 2^5 + 11 = q - 2


d = -121665 * inv(121666) % q
I = pow(2, (q - 1) // 4, q)


def xrecover(y):
    xx = (y * y - 1) * inv(d * y * y + 1)
    x = pow(xx, (q + 3) // 8, q)

    if (x * x - xx) % q != 0:
        x = (x * I) % q

    if x % 2 != 0:
        x = q - x

    return x


By = 4 * inv(5)
Bx = xrecover(By)
B = (Bx % q, By % q, 1, (Bx * By) % q)
ident = (0, 1, 1, 0)




def edwards_add(P, Q):
    # This is formula sequence 'addition-add-2008-hwcd-3' from
    # http://www.hyperelliptic.org/EFD/g1p/auto-twisted-extended-1.html
    (x1, y1, z1, t1) = P
    (x2, y2, z2, t2) = Q

    a = (y1 - x1) * (y2 - x2) % q
    b = (y1 + x1) * (y2 + x2) % q
    c = t1 * 2 * d * t2 % q
    dd = z1 * 2 * z2 % q
    e = b - a
    f = dd - c
    g = dd + c
    h = b + a
    x3 = e * f
    y3 = g * h
    t3 = e * h
    z3 = f * g

    return (x3 % q, y3 % q, z3 % q, t3 % q)


def edwards_double(P):
    # This is formula sequence 'dbl-2008-hwcd' from
    # http://www.hyperelliptic.org/EFD/g1p/auto-twisted-extended-1.html
    (x1, y1, z1, t1) = P

    a = x1 * x1 % q
    b = y1 * y1 % q
    c = 2 * z1 * z1 % q
    # dd = -a
    e = ((x1 + y1) * (x1 + y1) - a - b) % q
    g = -a + b  # dd + b
    f = g - c
    h = -a - b  # dd - b
    x3 = e * f
    y3 = g * h
    t3 = e * h
    z3 = f * g

    return (x3 % q, y3 % q, z3 % q, t3 % q)


def scalarmult(P, e):
    if e == 0:
        return ident
    Q = scalarmult(P, e // 2)
    Q = edwards_double(Q)
    if e & 1:
        Q = edwards_add(Q, P)
    return Q


# Bpow[i] == scalarmult(B, 2**i)
Bpow = []


def make_Bpow():
    P = B
    for i in range(253):
        Bpow.append(P)
        P = edwards_double(P)


make_Bpow()


def scalarmult_B(e):
    """
    Implements scalarmult(B, e) more efficiently.
    """
    # scalarmult(B, l) is the identity
    e = e % l
    P = ident
    for i in range(253):
        if e & 1:
            P = edwards_add(P, Bpow[i])
        e = e // 2
    assert e == 0, e
    return P


def encodeint(y):
    bits = [(y >> i) & 1 for i in range(b)]
    return b"".join(
        [
            int2byte(sum([bits[i * 8 + j] << j for j in range(8)]))
            for i in range(b // 8)
        ]
    )


def encodepoint(P):
    (x, y, z, t) = P
    zi = inv(z)
    x = (x * zi) % q
    y = (y * zi) % q
    bits = [(y >> i) & 1 for i in range(b - 1)] + [x & 1]
    return b"".join(
        [
            int2byte(sum([bits[i * 8 + j] << j for j in range(8)]))
            for i in range(b // 8)
        ]
    )


def bit(h, i):
    return (indexbytes(h, i // 8) >> (i % 8)) & 1


def publickey_unsafe(sk):
    """
    Not safe to use with secret keys or secret data.

    See module docstring.  This function should be used for testing only.
    """
    h = H(sk)
    a = 2 ** (b - 2) + sum(2**i * bit(h, i) for i in range(3, b - 2))
    A = scalarmult_B(a)
    return encodepoint(A)


def Hint(m):
    h = H(m)
    return sum(2**i * bit(h, i) for i in range(2 * b))


def signature_unsafe(m, sk, pk):
    """
    Not safe to use with secret keys or secret data.

    See module docstring.  This function should be used for testing only.
    """
    h = H(sk)
    a = 2 ** (b - 2) + sum(2**i * bit(h, i) for i in range(3, b - 2))
    r = Hint(
        intlist2bytes([indexbytes(h, j) for j in range(b // 8, b // 4)]) + m
    )
    R = scalarmult_B(r)
    S = (r + Hint(encodepoint(R) + pk + m) * a) % l
    return encodepoint(R) + encodeint(S)


def isoncurve(P):
    (x, y, z, t) = P
    return (
        z % q != 0
        and x * y % q == z * t % q
        and (y * y - x * x - z * z - d * t * t) % q == 0
    )


def decodeint(s):
    return sum(2**i * bit(s, i) for i in range(0, b))


def decodepoint(s):
    y = sum(2**i * bit(s, i) for i in range(0, b - 1))
    x = xrecover(y)
    if x & 1 != bit(s, b - 1):
        x = q - x
    P = (x, y, 1, (x * y) % q)
    if not isoncurve(P):
        raise ValueError("decoding point that is not on curve")
    return P


class SignatureMismatch(Exception):
    pass


def checkvalid(s, m, pk):
    """
    Not safe to use when any argument is secret.

    See module docstring.  This function should be used only for
    verifying public signatures of public messages.
    """
    if len(s) != b // 4:
        raise ValueError("signature length is wrong")

    if len(pk) != b // 8:
        raise ValueError("public-key length is wrong")

    R = decodepoint(s[: b // 8])
    A = decodepoint(pk)
    S = decodeint(s[b // 8 : b // 4])
    h = Hint(encodepoint(R) + pk + m)

    (x1, y1, z1, t1) = P = scalarmult_B(S)
    (x2, y2, z2, t2) = Q = edwards_add(R, scalarmult(A, h))

    if (
        not isoncurve(P)
        or not isoncurve(Q)
        or (x1 * z2 - x2 * z1) % q != 0
        or (y1 * z2 - y2 * z1) % q != 0
    ):
        raise SignatureMismatch("signature does not pass verification")

















#ZtM additions



def double_and_add(a_scalar, b, n):
    a_binary = bin(a_scalar)
    r = 0
    s = b
    for i in range((len(a_binary) - 1), 0, -1): 
        if(a_binary[i]=='1'): #step 1(a)
            r = (r + s) % n
        s = (s + s) % n #step 1(b)
    return r #step 2



def square_and_multiply(a, e_scalar, n):
    e_binary = bin(e_scalar) #step 1
    m = a
    r = 1
    for i in range((len(e_binary) - 1), 0, -1): #step 2
        if(e_binary[i]=='1'): 
            r = r * m % n #step 2(a)
        m = m * m % n #step 2(b)
    return r #step 3




"""
#Use double_and_add to find A * B (mod N)
def print_double_and_add(a_scalar, b, n):
    a_binary = bin(a_scalar)
    r = 0
    s = b
    for i in range((len(a_binary) - 1), 0, -1): 
        if(a_binary[i]=='1'): #step 1(a)
            r = (r + s) % n
        s = (s + s) % n #step 1(b)
        print('i=',len(a_binary)-1-i)
        print('r=',r)
        print('s=',s, '\n')
    return r #step 2

result=print_double_and_add(7,8,9)
print('Result=',result)
"""



"""
#Use square_and_multiply to find A ** B (mod N)
exp_answer=square_and_multiply(8,7,9)
print('8^7 (mod 9) =',exp_answer)
"""



"""
#easy inverse calc using FLT
# see 2.4 for definition of q
#Find 1/5 (mod q)
inv_py_5=pow(5,q-2,q)
print('1/5 (mod q) =',inv_py_5)
one_check=inv_py_5 * 5 % q
print('5 * 1/5 =',one_check)
"""



"""
#square and mult to find mod. inv.
inv_SAM_5= square_and_multiply(5,q-2, q)
print('1/5 (mod q) =',inv_SAM_5)
"""



"""
#extended Euclidean algorithm: Find a (mod n) when a > n
def ext_Euclid(a_decimal, n):
    a_string = str(a_decimal)
    r = 0
    for i in range(0,len(a_string),  1): 
        r = (r * 10 + int(a_string[i])) % n
    return r 

euclid=ext_Euclid(254,13)
print('254 (mod 13)=',euclid)
"""









#Getting to the Point

#see bottom of pg. 21 for definition G =(x, 4/5)
#see 2.4.2 for getting x^2 from y (don't worry about x yet)
#see reference 75, section 5.1 for complete definition of G



print('D=',d)
print('I=',I)
print('Bx=',Bx)
print('By=    ',By)


"""
#Let's find y
#4/5 (mod q) = 4 * 1/5 (mod q)

#find 1/5 (mod q)
fifth_py=pow(5,q-2,q)
fifth_SAM=square_and_multiply(5,q-2, q)

#find 4/5 (mod q)
four_fifths_py=4 * fifth_py % q
four_fifths_SAM=4 * fifth_SAM % q
print('By_py=',four_fifths_py)
print('By_SAM=',four_fifths_SAM)
"""


"""
#Let's find x^2
#x^2 = (y^2 - 1) * (1 / (d*y^2 + 1)) (mod q)

#Find denominator (inverse)

#Find d = -121665/121666
inv_SAM_121666= square_and_multiply(121666,q-2, q)
d_answer= -121665 * inv_SAM_121666 % q

denome=(d_answer * By * By + 1) % q
inv_denome=square_and_multiply(denome,q-2, q)

#Find numerator
numera= By * By - 1 % q

#multiply to get x^2
squared = numera * inv_denome % q
print(squared)

#'cheat' and use x to check x^2
x_squared = Bx * Bx % q
print(x_squared)
"""




