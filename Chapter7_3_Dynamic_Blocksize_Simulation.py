# This is a work in progress. Use at your own peril.

import bisect 

# Initialization
B = 0.6 #base block reward
block_weight = 100000 #first new block_weight for running simulation
TW_ref = 3000 #reference transaction weight for fee
cumulative_median_ref = 300000 #reference median for fee.
blocks_longterm_weights = [300000]*100000 #list of 100000 previous block longterm weights
hundred_blocks_weights = [100000]*100 #list of 100 previous block weights (normal weights, not longterm weights)
previous_effective_longterm_median = 300000
n = 500000 #number of blocks to simulate
newly_broadcast_tx_bytes = 100000 #newly broadcasted transaction bytes
mempool_unconfirmed = 0 # size of mempool bytes

#Data for plotting
longterm_median_archive=[]
longterm_weights_archive=[]
block_weights_archive=[]
f_min_actual_archive=[]
penalty_archive=[]
mempool_unconfirmed_archive=[]
max_next_block_weight_archive=[]

#Median Calc speedup
sorted_blocks_longterm_weights=[]
sorted_blocks_longterm_weights= sorted(blocks_longterm_weights)
longterm_mid= len(blocks_longterm_weights) // 2
sorted_hundred_blocks_weights=[]
sorted_hundred_blocks_weights= sorted(hundred_blocks_weights)
weights_mid= len(hundred_blocks_weights) // 2
#End Initialization


#Iterate n blocks
for i in range(n):
    
    #Process Current Block

    #Calculate Medians
    median_100000blocks_longterm_weights= (sorted_blocks_longterm_weights[longterm_mid] + sorted_blocks_longterm_weights[~longterm_mid]) / 2 #Faster median calculation for longterm weight
    median_100_blocks_weights= (sorted_hundred_blocks_weights[weights_mid] + sorted_hundred_blocks_weights[~weights_mid]) / 2 #Faster median calculation for shortterm weight
    
    effective_longterm_median= max(300000, median_100000blocks_longterm_weights) # effective longterm median for current block
    
    #longterm_block_weight= min(block_weight, 1.4 * previous_effective_longterm_median) #longterm block weight
    longterm_block_weight= max(min(block_weight, 1.7 * previous_effective_longterm_median), 300000, previous_effective_longterm_median / 1.7) #v16
    
    cumulative_weights_median= max(300000,min(max(300000, median_100_blocks_weights), 50 * effective_longterm_median)) #cumulative weights median
    
    max_next_block_weight = 2 * cumulative_weights_median # maximum weight of next block
    
    
    P= B * ((block_weight/cumulative_weights_median)-1)**2 #Block Reward Penalty
    if (block_weight/cumulative_weights_median)-1 < 0:
        P = 0
    
    f_min_actual = 0.95 * B * TW_ref / (effective_longterm_median**2) # Minimum fee per byte v16
    
    previous_effective_longterm_median = effective_longterm_median #Store current effective longterm median
    
    #Update longterm weights
    remove_item= bisect.bisect_left(sorted_blocks_longterm_weights, blocks_longterm_weights[0])
    sorted_blocks_longterm_weights.pop(remove_item)
    blocks_longterm_weights.pop(0)
    blocks_longterm_weights.append(longterm_block_weight)
    bisect.insort(sorted_blocks_longterm_weights, longterm_block_weight)
    
    #Update block weights
    remove_item= bisect.bisect_left(sorted_hundred_blocks_weights, hundred_blocks_weights[0])
    sorted_hundred_blocks_weights.pop(remove_item)
    hundred_blocks_weights.pop(0)
    hundred_blocks_weights.append(block_weight)
    bisect.insort(sorted_hundred_blocks_weights, block_weight)
    
    
    #Prepare values for next block
    
    
    #TX LINEAR RAMP
    if i < 300000:
        newly_broadcast_tx_bytes += 1000
    else:
        newly_broadcast_tx_bytes = 300000
    
    
    '''
    #TX FLOOD
    newly_broadcast_tx_bytes = max_next_block_weight # uncomment for max size blocks
    '''
    
    '''
    #TX PARABOLIC RAMP
    if i < 350000:
        newly_broadcast_tx_bytes = 4.4e-3 * i**2
    else:
        newly_broadcast_tx_bytes = 300000
    '''
    
    #add new tx to mempool
    mempool_unconfirmed += newly_broadcast_tx_bytes
    
    #Calculate size of next block
    block_weight=min(max_next_block_weight,mempool_unconfirmed) #guide with newly_broadcast_tx_bytes
    
    #account for bytes left out of block
    if block_weight == mempool_unconfirmed:
        mempool_unconfirmed = 0
    else:
        mempool_unconfirmed -= max_next_block_weight
        
    
    #Store data for plotting
    longterm_median_archive.append(effective_longterm_median)
    longterm_weights_archive.append(longterm_block_weight)
    block_weights_archive.append(block_weight)
    f_min_actual_archive.append(f_min_actual)
    penalty_archive.append(P)
    mempool_unconfirmed_archive.append(mempool_unconfirmed)
    max_next_block_weight_archive.append(max_next_block_weight)


    #Print Simulation Progress
    if i % 10000 == 0:
        print('Running Iteration=', i)
    



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


