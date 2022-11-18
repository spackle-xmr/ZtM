# Simulation of maximum transaction flood (per ZtM 2.0, NOT v16!!! THESE CALCULATIONS ARE NOT CORRECT FOR THE CURRENT MONERO NETWORK!!!)
# This is a work in progress. Use at your own peril.


import bisect 
#import math
#from statistics import median


# Initialization
B=0.6 #base block reward
block_weight=100000 #block_weight
blocks_longterm_weights=[] #list of 100000 previous block longterm weights
blocks_weights=[] #list of 100 previous block weights (normal weights, not longterm weights)

#Create longterm weights
for i in range(100000):
    blocks_longterm_weights.append(100000) #100k size block history

#Create normal weights
for i in range(100):
    blocks_weights.append(100000) #100k size block history

#Median Calc speedup
sorted_blocks_longterm_weights=[]
sorted_blocks_longterm_weights= sorted(blocks_longterm_weights)
longterm_mid= len(blocks_longterm_weights) // 2

sorted_blocks_weights=[]
sorted_blocks_weights= sorted(blocks_weights)
weights_mid= len(blocks_weights) // 2

previous_effective_longterm_median= 100000
#End Initialization

#Data for plotting
longterm_weights_archive=[]
blocks_weights_archive=[]

#Iterate n blocks
n=500000 #This takes a while
for i in range(n):
    
    #Process Current Block
    
    
    #median_blocks_longterm_weights= median(blocks_longterm_weights) #calculate median longterm weight for past 1e5 blocks
    median_blocks_longterm_weights= (sorted_blocks_longterm_weights[longterm_mid] + sorted_blocks_longterm_weights[~longterm_mid]) / 2 #Fast median calculation for longterm weight
    
    #median_blocks_weights= median(blocks_weights) #calculate median block weight for past 100 blocks
    median_blocks_weights= (sorted_blocks_weights[weights_mid] + sorted_blocks_weights[~weights_mid]) / 2 #Fast median calculation for longterm weight
    
    effective_longterm_median= max(300000, median_blocks_longterm_weights) # effective longterm median
    
    longterm_block_weight= min(block_weight, 1.4 * previous_effective_longterm_median) #longterm block weight
    
    cumulative_weights_median= max(300000,min(max(300000, median_blocks_weights), 50 * effective_longterm_median)) #cumulative weights median
    
    max_next_block_weight = 2 * cumulative_weights_median # maximum weight of next block
    
    P= B * ((block_weight/cumulative_weights_median)-1)**2 #Block Reward Penalty
    
    
    #Prepare values for next block
    #Set next block to maximum allowable size
    block_weight= max_next_block_weight
    
    #Update longterm weights
    sorted_blocks_longterm_weights.remove(blocks_longterm_weights[0]) 
    blocks_longterm_weights.pop(0)
    blocks_longterm_weights.append(longterm_block_weight)
    bisect.insort(sorted_blocks_longterm_weights, longterm_block_weight)
    
    
    #Update block weights
    sorted_blocks_weights.remove(blocks_weights[0])
    blocks_weights.pop(0)
    blocks_weights.append(block_weight)
    bisect.insort(sorted_blocks_weights, block_weight)
    
    #Store current effective longterm median
    previous_effective_longterm_median= effective_longterm_median
    
    #Store data for plotting
    longterm_weights_archive.append(longterm_block_weight)
    blocks_weights_archive.append(block_weight)
    



'''
# 7.3.1 Block Reward

L=2**64-1

B_0= (L - 0) >> 20
print('L=', L, ' atomic units')
print('B_0=',B_0, ' atomic units')

print('L=', L * 1e-12, ' XMR')
print('B_0=',B_0 * 1e-12, ' XMR')

# Example Base Block Reward Calculation
M= int(18000000 * 1e12) #18 million total supply
B= ((L - M) >> 19) * 1e-12
print('Block Reward With 18 million XMR In Circulation=', B, ' XMR')
'''

'''
# 7.3.2 Dynamic Block Weight

# Example with ~2kB size, 5 outputs
transaction_size=2000 #2k
p=5
num_dummy_outs=3
transaction_clawback= 0.8 * ((23 * (p + num_dummy_outs) / 2) * 32 - (2 * (math.log2(64 * p)) + 9) * 32)
transaction_weight = transaction_size + transaction_clawback

print('transaction_weight=  ', transaction_weight)
print('transaction_size=    ', transaction_size)
print('transaction_clawback=', transaction_clawback)

# Long Term Block Weight
#longterm_block_weight= min(block_weight, 1.4 * previous_effective_longterm_median)
#effective_longterm_median= max(300000, median_100000blocks_longterm_weights)


# Cumulative Median Weights
#cumulative_weights_median= max(300000,min(max(300000, median_100blocks_weights), 50 * effective_longterm_median))
#max_next_block_weight = 2 * cumulative_weights_median
'''

'''
# 7.3.3 Block Reward Penalty
B=0.6 #base block reward
P= B * ((block_weight/cumulative_weights_median)-1)**2
B_actual= B - P
B_actual= B * (1-((block_weight/cumulative_weights_median)-1)**2)
'''

'''
# 7.3.4 Dynamic Minimum Fee
BW=3000 #bytes
# Fee = Marginal Penalty : F = MP
#F= B * (((BW + TW)/cumulative_median - 1)**2- B * ((BW/cumulative_median - 1)**2))
#WF_b= (BW/cumulative_media - 1)
#WF_t= (TW/cumulative_media)
#F= B * (2 * WF_b * WF_t + WF_t**2)

TW_ref=300000
cumulative_median= 300000
#F = B * WF_t**2

#f_B_default=F_general/TW_general
#f_B_default= B * (1/cumulative_median_general) * (TW_ref/cumulative_median_ref)
#f_B_min= B * (1/cumulative_weights_median) * (TW_ref/cumulative_median_ref) * (1/5)

smallest_median= max(300000,min(median_100block_weights, effective_longterm_median))

f_B_min_actual = B * (1/smallest_median) * (TW_ref/cumulative_median_ref) * (1/5)
'''



'''
# 7.3.5 Emission Tail

if (M / 1e12) > 18132171.273709551615:
    B = 0.6
'''


