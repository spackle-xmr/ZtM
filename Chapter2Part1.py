from dumb25519 import Scalar, Point
import dumb25519
import random

q=dumb25519.q
d=dumb25519.d
G=dumb25519.G
l=Scalar(dumb25519.l)

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




'''
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
'''



'''
#Use square_and_multiply to find A ** B (mod N)
exp_answer=square_and_multiply(8,7,9)
print('8^7 (mod 9) =',exp_answer)
'''



'''
#easy inverse calc using FLT
# see 2.4 for definition of q
#Find 1/5 (mod q)
inv_py_5=pow(5,q-2,q)
print('1/5 (mod q) =',inv_py_5)
one_check=inv_py_5 * 5 % q
print('5 * 1/5 (mod q) =',one_check)
'''



'''
#square and mult to find mod. inv.
inv_SAM_5= square_and_multiply(5,q-2, q)
print('1/5 (mod q) =',inv_SAM_5)
'''



'''
#extended Euclidean algorithm: Find a (mod n) when a > n
def ext_Euclid(a_decimal, n):
    a_string = str(a_decimal)
    r = 0
    for i in range(0,len(a_string),  1): 
        r = (r * 10 + int(a_string[i])) % n
    return r 

euclid=ext_Euclid(254,13)
print('254 (mod 13)=',euclid)
'''









#Getting to the Point

#see bottom of pg. 21 for definition G =(x, 4/5)
#see 2.4.2 for getting x^2 from y (don't worry about x yet)
#see reference 75, section 5.1 for complete definition of G

'''
B=G
print('D=',d)
print('Bx=',B.x)
print('By=    ',B.y)
'''

'''
#Let's find y
#4/5 (mod q) = 4 * 1/5 (mod q)

#find 1/5 (mod q)
fifth_py=pow(5,q-2,q)
fifth_SAM=square_and_multiply(5,q-2, q)

#find 4/5 (mod q)
four_fifths_py=4 * fifth_py % q
four_fifths_SAM=4 * fifth_SAM % q
print('By_py= ',four_fifths_py)
print('By_SAM=',four_fifths_SAM)




#Let's find x^2
#x^2 = (y^2 - 1) * (1 / (d*y^2 + 1)) (mod q)

#Find denominator (inverse)

#Find d = -121665/121666
inv_SAM_121666= square_and_multiply(121666,q-2, q)
d_answer= -121665 * inv_SAM_121666 % q

denome=(d_answer * B.y * B.y + 1) % q
inv_denome=square_and_multiply(denome,q-2, q)

#Find numerator
numera= B.y * B.y - 1 % q

#multiply to get x^2
squared = numera * inv_denome % q
print(squared)

#'cheat' and use x to check x^2
x_squared = B.x * B.x % q
print(x_squared)
'''
