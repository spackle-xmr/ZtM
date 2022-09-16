from dumb25519 import Scalar, Point
import dumb25519
import random

q=dumb25519.q
d=dumb25519.d
G=dumb25519.G
l=Scalar(dumb25519.l)

'''
# 3.1 Prove k in kG, kR, and that k is the same for both (without revealing k)

# Non-interactive proof
k=dumb25519.random_scalar()
count = 20 # base key count
J= []
J= [dumb25519.random_point() for i in range(count)]
K= [k * value for value in J]

# 1. Generate random numbers alpha and compute alpha * J
alpha= dumb25519.random_scalar()
alphaJ = [alpha * value for value in J]

# 2. Calculate the challenge
c=dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(alphaJ[i] for i in range(count)))

# 3. Define the response
r=alpha - c * k

# 4. Publish signature
signature=(c,r)

# Verification

# 1. Calculate the challenge
Computation=[signature[1] * J[i] + signature[0] * K[i] for i in range(count)]
cprime= dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(Computation[i] for i in range(count)))


# 2. Check c == cprime
print('c =      ', c)
print('cprime = ',cprime)
'''

'''
# 3.2 
count = 20 # key count

# Non-interactive proof
k=[dumb25519.random_scalar() for i in range(count)]
J= []
J= [dumb25519.random_point() for i in range(count)]
K= [k[i] * J[i] for i in range(count)]

# 1. Generate random numbers alpha and compute alpha * J
alpha= [dumb25519.random_scalar() for i in range(count)]
alphaJ = [alpha[i] * J[i] for i in range(count)]

# 2. Calculate the challenge
c=dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(alphaJ[i] for i in range(count)))

# 3. Define each response
r=[alpha[i] - c * k[i] for i in range(count)]

# 4. Publish the signature
signature = (c,r)


# Verification -- same as before, with individualized responses

# 1. Calculate the challenge
Computation=[signature[1][i] * J[i] + signature[0] * K[i] for i in range(count)]
cprime= dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(Computation[i] for i in range(count)))

# 2. Check c == cprime
print('c =      ', c)
print('cprime = ',cprime)
'''

'''
# 3.3 SAG

m="Someone among us said this."
count = 20 # key count
pi= count-1 #Set pi as final index to simplify example code. Same effect as a random selection with the elements rearranged.
k_pi=dumb25519.random_scalar()
K_pi= k_pi * G
R= [dumb25519.random_point() for i in range(count)]
R[pi]=K_pi

# 1. Generate random number alpha, and fake responses for all but pi
alpha= dumb25519.random_scalar()
alphaG= alpha * G
c=[Scalar(0)]*count
r=[dumb25519.random_scalar() for i in range(count)]
r[pi]=Scalar(0) # exclude i = pi

# 2. Calculate challenge for pi+1
c[0]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, alphaG)

# 3. Starting after pi, calculate challenges
for index in range(pi):
    c[index+1]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, r[index] * G + c[index] * R[index])

# 4. Define the real response
r[pi] = alpha - c[pi] * k_pi


#Verification

cprime=[0]*(count+1)


# 1. Compute set of cprime values
cprime[0] = c[0] #start with signature value
for index in range(1,count+1):
    cprime[index]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, r[index-1] * G + cprime[index-1] * R[index-1])

# 2. Check c_1 == cprime_1, with cprime_1 being the last term calculated. 
if c[0] == cprime[count]:
    print('Valid')

'''

'''
# 3.4 bLSAG

m="Someone among us said this."
count = 20 # key count
pi= count-1 #Set pi as final index to simplify example code. Same effect as a random selection with the elements rearranged.
k_pi=dumb25519.random_scalar()
K_pi= k_pi * G
R= [dumb25519.random_point() for i in range(count)]
R[pi]=K_pi

# Signature

# 1. Calculate key image K_tilde
K_tilde = k_pi * dumb25519.hash_to_point(K_pi)

# 2. Generate random number alpha, and fake responses for all but pi
alpha= dumb25519.random_scalar()
alphaG= alpha * G
r=[dumb25519.random_scalar() for i in range(count)]
r[pi]=Scalar(0) # exclude i = pi
c=[0]*count

# 3. Calculate challenge for pi+1
c[0]=dumb25519.hash_to_scalar(m, alphaG, alpha * dumb25519.hash_to_point(K_pi))

# 4. Compute challenge set
for index in range(pi):
    c[index+1]=dumb25519.hash_to_scalar(m, r[index] * G + c[index] * R[index], r[index] * dumb25519.hash_to_point(R[index]) + c[index] * K_tilde)

# 5. Define real response
r[pi] = alpha - c[pi] * k_pi

#Verification
cprime=[0]*(count+1)

# 1. Check l * K_tilde returns zero/point-at-infinity element (0,1)
zero_check = l * K_tilde

if zero_check.x == 0:
    print('zero check passed')

# 2. Compute cprime set
cprime[0] = c[0] #start with signature value
for index in range(1,count+1):
    cprime[index]=dumb25519.hash_to_scalar(m, r[index-1] * G + cprime[index-1] * R[index-1], r[index-1] * dumb25519.hash_to_point(R[index-1]) + c[index-1] * K_tilde)

# 3. Check c_1 == cprime_1, with cprime_1 being the last term calculated. 
if c[0] == cprime[count]:
    print('Valid')
'''

'''
# NOT WORKING/IN PROGRESS
# 3.5 MLSAG 
# 2d set of public keys K_i_j, with knowledge of m private key k_pi_j for index i = pi
m="Someone among us said this."
count = 3 # key count (size of each dimension of R)
pi= count-1 #Set pi as final index to simplify example code. Same effect as a random selection with the elements rearranged.
k_pi_j=[dumb25519.random_scalar() for i in range(count)]
K_pi_j= [k_pi_j[i] * G for i in range(count)]
R= [[dumb25519.random_point() for i in range(count)] for j in range(count)]
R[pi]=K_pi_j

# Signature

# 1. Calculate key images K_tilde_j
K_tilde_j= [k_pi_j[j] * dumb25519.hash_to_point(K_pi_j[j]) for j in range(count)]
#print(K_tilde_j)

# 2. Generate random numbers alpha_j and r_i_j except for the pi set of j 
alpha_j=[dumb25519.random_scalar() for i in range(count)]
r_i_j=[[dumb25519.random_scalar() for i in range(count)] for j in range(count)]
r_i_j[pi]=[0]*count # clear pi set of j
c=[0]*count


# 3. Compute challenge for pi+1 (note that pi+1 is index 0)
#prepare ordered list of calculated items to hash
ordered=[0]*(2*count)
for index in range(count):
    alphaG=alpha_j[index] * G
    alphaHash=alpha_j[index] * dumb25519.hash_to_point(K_pi_j[index])
    ordered[index*2]=alphaG
    ordered[index*2+1]=alphaHash

#print(ordered)
c[0]=dumb25519.hash_to_scalar(m, ordered)
print(c)

# 4. Compute other challenges
'''
