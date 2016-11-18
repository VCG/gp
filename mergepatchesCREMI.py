import numpy as np

#
#
#

basedir = '/n/regal/pfister_lab/haehn/CREMIBIG/'

trainA = basedir + 'train_0_100.npz.npy'
trainA_targets = basedir + 'train_0_100_targets.npz.npy'
trainB = basedir + 'train_100_200.npz.npy'
trainB_targets = basedir + 'train_100_200_targets.npz.npy'
trainC = basedir + 'train_200_289.npz.npy'
trainC_targets = basedir + 'train_200_298_targets.npz.npy'

counter = 0

trainA = np.load(trainA, mmap_mode='r')
trainA_count = trainA.shape[0]

trainB = np.load(trainB, mmap_mode='r')
trainB_count = trainB.shape[0]

trainC = np.load(trainC, mmap_mode='r')
trainC_count = trainC.shape[0]

all_count = trainA_count + trainB_count + trainC_count

#
# allocate large array
# 
PATCH_BYTES = 75*75
NO_PATCHES = all_count
P_SIZE = (NO_PATCHES, 4, 75,75) # rather than raveled right now

p_rgba = np.zeros(P_SIZE, dtype=np.float32)

p_rgba[0:trainA_count] = trainA
p_rgba[trainA_count:trainA_count+trainB_count] = trainB
p_rgba[trainB_count:trainB_count+trainC_count] = trainC

# now store this bad boy
np.save(basedir+'train.npy', p_rgba)

# print 'STORED BIG BOY!'
p_rgba = None # free them all

#
# same for targets
#
trainA_targets = np.load(trainA_targets)
trainA_count = trainA_targets.shape[0]
trainB_targets = np.load(trainB_targets)
trainB_count = trainB_targets.shape[0]
trainC_targets = np.load(trainC_targets)
trainC_count = trainC_targets.shape[0]

all_count = trainA_count + trainB_count + trainC_count
NO_PATCHES = all_count

p_target = np.zeros(NO_PATCHES)

p_target[0:trainA_count] = trainA_targets
p_target[trainA_count:trainA_count+trainB_count] = trainB_targets
p_target[trainB_count:trainB_count+trainC_count] = trainC_targets

# now store this lady boy
np.save(basedir+'train_targets.npy', p_target)

print 'ALL DONE!'
