from dumb25519 import Scalar, Point
import dumb25519
import random

q=dumb25519.q
d=dumb25519.d
G=dumb25519.G
l=Scalar(dumb25519.l)



'''
# 5.2 Pederson commitments

a=dumb25519.random_scalar() #value to commit to
x=dumb25519.random_scalar() #blinding factor
gamma=dumb25519.random_scalar() #reference for new generator
H= gamma * G #new generator
C=x*G + a*H
'''

'''
# 5.3 Amount commitments

b=dumb25519.random_scalar() #value to commit to
y=dumb25519.random_scalar() #blinding factor
gamma=dumb25519.random_scalar() #reference for new generator
H= gamma * G #new generator
C=y*G + b*H



#use shared secret rK_v
#rK_v
k_v=dumb25519.random_scalar()
k_s=dumb25519.random_scalar()
K_v=k_v * G
K_s=k_s * G
r=dumb25519.random_scalar()
rK_v=r * K_v


# output mask y_t and amount_t for t = 0
y_t=dumb25519.hash_to_scalar('commitment_mask',dumb25519.hash_to_scalar(rK_v,0))
b_t=0xA5A5A5A5A5A5A5A5# 8 bytes
print('b_t=        ',bin(b_t))
xor_bytes=dumb25519.hash_to_scalar('amount',dumb25519.hash_to_scalar(rK_v,0))
xor_bytes_int=int(xor_bytes)
xor_bytes_bin=bin(xor_bytes_int)
xor_bytes_8=xor_bytes_bin[:66]
print('xor_bytes_8=',xor_bytes_8)
xor_bytes_8_int=int(xor_bytes_8,2)
amount_t=b_t^xor_bytes_8_int # Perform XOR
print('amount_t=   ',format(amount_t, '#066b'))
'''



# 5.4 RingCT introduction
'''
#Check commitments for inputs - outputs = 0
count=10 #number of commitments
a=[Scalar(1)]*count #input values to commit to
b=[Scalar(1)]*count #output values to commit to
y=[dumb25519.random_scalar() for i in range(count)] #blinding factors
gamma=[dumb25519.random_scalar() for i in range(count)] #reference for new generator
H=[gamma[i] * G for i in range(count)] #new generators
C_a=[y[i]*G + a[i]*H[i] for i in range(count)]
C_b=[y[i]*G + b[i]*H[i] for i in range(count)]

#sum commitments
C_a_sum= C_a[0]
C_b_sum= C_b[0]
for i in range(1,count):
    C_a_sum=C_a_sum + C_a[i]
    C_b_sum=C_b_sum + C_b[i]

#Check sums balance
if C_a_sum == C_b_sum:
    print('Input and output commitments balance')
'''

'''
count=10 #number of commitments
a=[Scalar(1)]*count #input values to commit to
x=[dumb25519.random_scalar() for i in range(count)] #blinding factors
y=[dumb25519.random_scalar() for i in range(count)] #blinding factors
x_prime=[dumb25519.random_scalar() for i in range(count)] #different blinding factors

#all blinding factors are random, except final x_prime which is calculated to balance sums of y_t and all other x_prime
y_sum=y[0]
x_prime_sum=Scalar(0)
for i in range(1,count):
    y_sum=y_sum + y[i]
    x_prime_sum=x_prime_sum + x_prime[i-1]
x_prime[count-1]=y_sum - x_prime_sum

gamma=[dumb25519.random_scalar() for i in range(count)] #reference for new generator
H=[gamma[i] * G for i in range(count)] #new generators
C_a=[x[i]*G + a[i]*H[i] for i in range(count)]
C_a_prime=[x_prime[i]*G + a[i]*H[i] for i in range(count)] #Pseudo output commitment
C_a_delta=[C_a[i] - C_a_prime[i] for i in range(count)]
z=[x[i] - x_prime[i] for i in range(count)]
zG=[z[i] * G for i in range(count)]

if C_a_delta == zG:
    print('Commitment to zero')
'''

'''
# 5.5 Range proofs
#problem with negative values
count=2 #number of commitments
a=[Scalar(6),Scalar(5)]#input values to commit to
b=[Scalar(21),Scalar(-10)]#output values to commit to
y=[dumb25519.random_scalar() for i in range(count)] #blinding factors
gamma=dumb25519.random_scalar() #reference for new generator
H=gamma * G #new generator
C_a=[y[i]*G + a[i]*H for i in range(count)]
C_b=[y[i]*G + b[i]*H for i in range(count)]

#sum commitments
C_a_sum= C_a[0]
C_b_sum= C_b[0]
for i in range(1,count):
    C_a_sum=C_a_sum + C_a[i]
    C_b_sum=C_b_sum + C_b[i]

#Check sums balance
if C_a_sum == C_b_sum:
    print('Input and output commitments balance, which is a problem')
'''
