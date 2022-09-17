from dumb25519 import Scalar, Point
import dumb25519
import random

q=dumb25519.q
d=dumb25519.d
G=dumb25519.G
l=Scalar(dumb25519.l)

'''
# 4.2 One-time addresses
# Bob has private/public keys
k_v=dumb25519.random_scalar()
k_s=dumb25519.random_scalar()
K_v=k_v * G
K_s=k_s * G

# 1. Alice generates random number r and calculates the one-time address
r=dumb25519.random_scalar()
K_o=dumb25519.hash_to_scalar(r * K_v) * G + K_s

# 2. Payment sent to K_o, with amount 0 and rG appended to tx data.
rG=r * G

# 3. Receiver uses rG and K_o to check if tx was addressed to him.
k_vrG=k_v * rG
rK_v=k_vrG

Kprime_s=K_o - dumb25519.hash_to_scalar(rK_v) * G

if Kprime_s == K_s:
    print("Tx addressed to him")

# 4. one-time keys for the output
K_o=dumb25519.hash_to_scalar(r * K_v) * G + K_s
K_o=(dumb25519.hash_to_scalar(r * K_v) + k_s) * G #same calculation done differently

k_o=dumb25519.hash_to_scalar(r * K_v) + k_s
'''



'''
# 4.2.1 Multi-output transactions
# curve point rG
r=dumb25519.random_scalar()
rG=r * G

# Transaction outputs are given index t to ensure uniqueness
#create a set of K_o values using index t
count = 5 # number of values to create
k_v=[dumb25519.random_scalar() for i in range(count)]
k_s=[dumb25519.random_scalar() for i in range(count)]
K_v=[k_v[t] * G for t in range(count)]
K_s=[k_s[t] * G for t in range(count)]
k_o=[0]*count
K_o=[0]*count



#get r * K_v using rG for each index t
k_vrG=[k_v[t] * rG for t in range(count)]
rK_v=k_vrG

for t in range(count):
    K_o[t]=dumb25519.hash_to_scalar(rK_v[t], t) * G + K_s[t] 

#same calculation done differently
for t in range(count):
    K_o[t]=(dumb25519.hash_to_scalar(rK_v[t], t) + k_s[t]) * G

#private one-time keys using index t
for t in range(count):
    k_o[t]=dumb25519.hash_to_scalar(rK_v[t], t) + k_s[t]
'''


'''
# 4.3 Subaddresses

#start with regular private/public key pairs
count = 5 # number of subaddresses to generate
k_v=dumb25519.random_scalar()
k_s=dumb25519.random_scalar()
K_v=[Point(0,1)]*count
K_s=[Point(0,1)]*count
K_v[0]=k_v * G
K_s[0]=k_s * G

# generate subaddress i, with its own view and spend key
for i in range(1,count):
    K_s[i]=K_s[0] + dumb25519.hash_to_scalar(k_v, i) * G
    K_v[i]=k_v * K_s[i]

#same calculation done differently
for i in range(1,count):
    K_v[i]=k_v * (k_s + dumb25519.hash_to_scalar(k_v, i)) * G
    K_s[i]=(k_s + dumb25519.hash_to_scalar(k_v, i)) * G


# 4.3.1 Send to a subaddress
# send to subaddress 1, written K_v[1]/K_s[1]

# 1. Alice generates random number r and calculates the one-time address
r=dumb25519.random_scalar()
K_o=dumb25519.hash_to_scalar(r * K_v[1],0) * G + K_s[1] #0 is the index t from 4.2.1

# 2. Payment sent to K_o, with amount 0 and rG appended to tx data.
rK_s=r * K_s[1]

# 3. Receiver uses rK_s and K_o to check if tx was addressed to him.
k_vrK_s1=k_v * r * K_s[1]
rK_v1=k_vrK_s1

Kprime_s=K_o - dumb25519.hash_to_scalar(rK_v1,0) * G
if Kprime_s == K_s[1]:
    print("Tx addressed to subaddress 1")

# 4. one-time keys for the output
K_o=dumb25519.hash_to_scalar(r * K_v[1],0) * G + K_s[1]

#Calculate subaddress private spend key k_s_1 taking section from formula on bottom of pg. 39
k_s_1= k_s + dumb25519.hash_to_scalar(k_v,1)
K_o=(dumb25519.hash_to_scalar(r * K_v[1],0) + k_s_1) * G #same calculation done differently. 
k_o=dumb25519.hash_to_scalar(r * K_v[1],0) + k_s_1

'''


'''
# 4.4 Integrated addresses
# made from K_v, K_s, and payment ID

k_v=dumb25519.random_scalar()
k_s=dumb25519.random_scalar()
K_v=k_v * G
K_s=k_s * G
payment_ID=0xDEADBEEF
pid_tag=dumb25519.random_scalar()
print('payment_ID=          ',bin(payment_ID))


# Encoding
r=dumb25519.random_scalar()
rG=r * G
rK_v=r * K_v
k_mask=dumb25519.hash_to_scalar(rK_v,pid_tag)


k_mask_int=int(k_mask)
k_mask_bin=bin(k_mask_int)

k_payment_ID=k_mask_bin[:34]
print('k_payment_ID=        ',k_payment_ID)
k_payment_ID_int=int(k_payment_ID,2)
encoded_payment_ID=k_payment_ID_int^payment_ID # Perform XOR
print('encoded_payment_ID=  ',format(encoded_payment_ID, '#034b'))


# Decoding
dec_k_mask=dumb25519.hash_to_scalar(k_v * rG, pid_tag)
dec_k_payment_ID=int(dec_k_mask)
dec_k_payment_ID_bin=bin(dec_k_payment_ID)[:34]
dec_k_payment_ID_int=int(dec_k_payment_ID_bin,2)
print('decoded_k_payment_ID=',dec_k_payment_ID_bin)
dec_payment_ID=dec_k_payment_ID_int^encoded_payment_ID
print('decoded_payment_ID=  ',format(dec_payment_ID, '#034b'))
'''
