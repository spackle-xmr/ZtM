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

# Signature

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
# 3.5 MLSAG 
# 2d set of public keys K_i_j, with knowledge of m private key k_pi_j for index i = pi
m="Someone among us said this."
count = 5 # key count (size of each dimension of R, for a total of count^2 keys)
pi= count-1 #Set pi as final index to simplify example code. Same effect as a random selection with the elements rearranged.
k_pi_j=[dumb25519.random_scalar() for i in range(count)]
K_pi_j= [k_pi_j[i] * G for i in range(count)]
R= [[dumb25519.random_point() for i in range(count)] for j in range(count)]
R[pi]=K_pi_j

# Signature

# 1. Calculate key images K_tilde_j
K_tilde_j= [k_pi_j[j] * dumb25519.hash_to_point(K_pi_j[j]) for j in range(count)]

# 2. Generate random numbers alpha_j and r_i_j except for the pi set of j 
alpha_j=[dumb25519.random_scalar() for i in range(count)]
r_i_j=[[dumb25519.random_scalar() for j in range(count)] for i in range(count)]
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
c[0]=dumb25519.hash_to_scalar(m, ordered)

# 4. Compute challenge set
for number in range(0,pi):
    ordered=[0]*(2*count)
    for index in range(count):
        rGcK=r_i_j[number][index] * G + c[number] * R[number][index]
        rHashcK_tilde=r_i_j[number][index] * dumb25519.hash_to_point(R[number][index]) + c[number] * K_tilde_j[index]
        ordered[index*2]=rGcK
        ordered[index*2+1]=rHashcK_tilde
    c[number+1]=dumb25519.hash_to_scalar(m, ordered)

# 5. Define all r_pi_j = alpha_j - c_pi * k_pi_j
for index in range(count):
    r_i_j[pi][index]=alpha_j[index] - c[pi] * k_pi_j[index]


# Verification
cprime=[0]*(count+1)

# 1. zero check all l * K_tilde_j
for index in range(count):
    zero_check= l * K_tilde_j[index]
    if zero_check.x != 0:
        print('Zero Check Fail')
        break
    if index == count-1:
        print('Zero Check Passed')

# 2. Compute cprime set
cprime[0] = c[0] #start with signature value

# Exact same calculation performed in Signature step 4, but expanded to calculate signature challenge value twice
for number in range(0,count):
    ordered=[0]*(2*count)
    for index in range(count):
        rGcK=r_i_j[number][index] * G + c[number] * R[number][index]
        rHashcK_tilde=r_i_j[number][index] * dumb25519.hash_to_point(R[number][index]) + c[number] * K_tilde_j[index]
        ordered[index*2]=rGcK
        ordered[index*2+1]=rHashcK_tilde
    cprime[number+1]=dumb25519.hash_to_scalar(m, ordered)

# 3. Check c_1 == cprime_1
if c[0] == cprime[count]:
    print('Valid')

'''

# 3.6 CLSAG
# 2d set of public keys K_i_j, with knowledge of m private key k_pi_j for index i = pi
m="Someone among us said this."
count = 10 # key count (size of each dimension of R, for a total of count^2 keys)
pi= count-1 #Set pi as final index to simplify example code. Same effect as a random selection with the elements rearranged.
k_pi_j=[dumb25519.random_scalar() for i in range(count)]
K_pi_j= [k_pi_j[i] * G for i in range(count)]
R= [[dumb25519.random_point() for i in range(count)] for j in range(count)]
R[pi]=K_pi_j

# Signature

# 1. Calculate key images K_tilde_j
K_tilde_j= [k_pi_j[j] * dumb25519.hash_to_point(K_pi_j[0]) for j in range(count)]

# 2. Generate random numbers alpha and r_i_j except for the pi set of j 
alpha=dumb25519.random_scalar()
r_i=[dumb25519.random_scalar() for j in range(count)]
r_i[pi]=0
c=[0]*count

# 3. Calculate aggreate public keys W_i for all i, and aggreate key image W_tilde
W_i=[0]*count
j_terms=[0]*count
T_j_raw=['CLSAG_']*count
T_j=[f'{elm}{index+1}' for index, elm in enumerate(T_j_raw)]
#T_j=['CLSAG_1', 'CLSAG_2', 'CLSAG_3', 'CLSAG_4', 'CLSAG_5']
T_c=('CLSAG_c')

# Aggreate public keys W_i for all i
for i in range(count):
    #get sum of j terms
    for j in range(count):
        j_terms[j]=dumb25519.hash_to_scalar(T_j[j], R, K_tilde_j) * R[i][j]
        if j == 0:
            j_sum = j_terms[j]
        j_sum = j_sum + j_terms[j]
    W_i[i]=j_sum


# Aggreate key image W_tilde
for j in range(count):
        j_terms[j]=dumb25519.hash_to_scalar(T_j[j], R, K_tilde_j) * K_tilde_j[j]
        if j == 0:
            j_sum = j_terms[j]
        j_sum = j_sum + j_terms[j]
W_tilde=j_sum

# Aggregate private key w_pi
for j in range(count):
        j_terms[j]=dumb25519.hash_to_scalar(T_j[j], R, K_tilde_j) * k_pi_j[j]
        if j == 0:
            j_sum = j_terms[j]
        j_sum = j_sum + j_terms[j]
w_pi=j_sum

# 4. Compute challenge for pi+1 (note that pi+1 is index 0)
c[0]=dumb25519.hash_to_scalar(T_c, R, m, alpha * G, alpha * dumb25519.hash_to_point(K_pi_j[0]))

# 5. Compute challenge set
for i in range(pi):
    c[i+1]=dumb25519.hash_to_scalar(T_c, R, m, r_i[i] * G + c[i] * W_i[i], r_i[i] * dumb25519.hash_to_point(R[i][0]) + c[i] * W_tilde)

# 6. Define r_pi
r_i[pi]=alpha - c[pi] * w_pi


# Verification
cprime=[0]*(count+1)

# 1. zero check all l * K_tilde_j
for index in range(count):
    zero_check= l * K_tilde_j[index]
    if zero_check.x != 0:
        print('Zero Check Fail')
        break
    if index == count-1:
        print('Zero Check Passed')

# 2. Calculate aggreate public keys W_i for all i, and aggreate key image W_tilde (same as Signature step 3, without knowledge of private keys)
W_i=[0]*count
j_terms=[0]*count

# Aggreate public keys W_i for all i
for i in range(count):
    #get sum of j terms
    for j in range(count):
        j_terms[j]=dumb25519.hash_to_scalar(T_j[j], R, K_tilde_j) * R[i][j]
        if j == 0:
            j_sum = j_terms[j]
        j_sum = j_sum + j_terms[j]
    W_i[i]=j_sum

# Aggreate key image W_tilde
for j in range(count):
        j_terms[j]=dumb25519.hash_to_scalar(T_j[j], R, K_tilde_j) * K_tilde_j[j]
        if j == 0:
            j_sum = j_terms[j]
        j_sum = j_sum + j_terms[j]
W_tilde=j_sum

# 3. Compute cprime set
cprime[0] = c[0] #start with signature value
# Exact same calculation performed in Signature step 5, but expanded to calculate signature challenge value twice
for i in range(count):
    cprime[i+1]=dumb25519.hash_to_scalar(T_c, R, m, r_i[i] * G + cprime[i] * W_i[i], r_i[i] * dumb25519.hash_to_point(R[i][0]) + cprime[i] * W_tilde)

# 4. Check c_1 == cprime_1
if c[0] == cprime[count]:
    print('Valid')


