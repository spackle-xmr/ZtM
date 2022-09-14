# built off https://github.com/coinstudent2048/ecc_tutorials

from dumb25519 import Scalar, Point
import dumb25519
import random

q=dumb25519.q
d=dumb25519.d
G=dumb25519.G

'''
# 3.1 Prove k in kG, kR, and that k is the same for both (without revealing k)

# Non-interactive proof
k=dumb25519.random_scalar()
#K= k * G
count = 20 # base key count
J= []
J= [dumb25519.random_point() for i in range(count)]
K= [k * value for value in J]
alpha= dumb25519.random_scalar()
alphaJ = [alpha * value for value in J]
c=dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(alphaJ[i] for i in range(count)))


r=alpha - c * k
# Printing values during calculation breaks process?! Example:
#print(K) 


# Verification
Comp=[r * J[i] + c * K[i] for i in range(count)]

cprime= dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(Comp[i] for i in range(count)))


#print(J)
#print(Comp)
#print(r)
print('c =      ', c)
print('cprime = ',cprime)
'''

'''
# 3.2 
count = 20 # key count

# Non-interactive proof
k=[dumb25519.random_scalar() for i in range(count)]
#K= k * G

J= []
J= [dumb25519.random_point() for i in range(count)]
K= [k[i] * J[i] for i in range(count)]
alpha= [dumb25519.random_scalar() for i in range(count)]
alphaJ = [alpha[i] * J[i] for i in range(count)]
c=dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(alphaJ[i] for i in range(count)))


r=[alpha[i] - c * k[i] for i in range(count)]

# Printing values during calculation breaks process?! Example:
#print(K)


# Verification -- same as before, with individualized responses
Comp=[r[i] * J[i] + c * K[i] for i in range(count)]

cprime= dumb25519.hash_to_scalar((J[i] for i in range(count)),(K[i] for i in range(count)),(Comp[i] for i in range(count)))

print('c =      ', c)
print('cprime = ',cprime)
'''


'''
# 3.3 SAG

m="Someone among us said this."
count = 20 # key count
pi= random.randint(0, count-2) #Cut end to make life easy
k_pi=dumb25519.random_scalar()
K_pi= k_pi * G
R= [dumb25519.random_point() for i in range(count)]
R[pi]=K_pi


# Step 1
alpha= dumb25519.random_scalar()
alphaG= alpha * G
c=[Scalar(0)]*count
r=[dumb25519.random_scalar() for i in range(count)]
r[pi]=Scalar(0) # exclude i = pi

# Step 2
c[pi+1]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, alphaG)

# Step 3 Starting after pi, calculate challenges
for index in range(pi+1,count-1):
    c[index+1]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, r[index] * G + c[index] * R[index])
c[0]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, r[-1] * G + c[-1] * R[-1])
for index in range(0,pi):
    c[index+1]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, r[index] * G + c[index] * R[index])


# Step 4
r[pi] = alpha - c[pi] * k_pi


#Verification
cprime=[0]*count

# Step 1
for index in range(count-1):
    cprime[index+1]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, r[index] * G + c[index] * R[index])
cprime[0]=dumb25519.hash_to_scalar((R[i] for i in range(count)),m, r[-1] * G + c[-1] * R[-1])

#print(c)
#print(cprime)
#print(c[0])
#print(cprime[0])

# Step 2
if cprime[0] == c[0]:
    print('Valid')
'''



