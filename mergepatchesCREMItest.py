import numpy as np

#
#
#

basedir = '/n/regal/pfister_lab/haehn/CREMITEST/'

testA = basedir + 'testA.npz.npy'
testA_targets = basedir + 'testA_targets.npz.npy'
testB = basedir + 'testB.npz.npy'
testB_targets = basedir + 'testB_targets.npz.npy'
testC = basedir + 'testC.npz.npy'
testC_targets = basedir + 'testC_targets.npz.npy'

counter = 0

# testA = np.load(testA, mmap_mode='r')
# testA_count = testA.shape[0]

# testB = np.load(testB, mmap_mode='r')
# testB_count = testB.shape[0]

# testC = np.load(testC, mmap_mode='r')
# testC_count = testC.shape[0]

# all_count = testA_count + testB_count + testC_count

# #
# # allocate large array
# # 
# PATCH_BYTES = 75*75
# NO_PATCHES = all_count
# P_SIZE = (NO_PATCHES, 4, 75,75) # rather than raveled right now

# p_rgba = np.zeros(P_SIZE, dtype=np.float32)

# p_rgba[0:testA_count] = testA
# p_rgba[testA_count:testA_count+testB_count] = testB
# p_rgba[testB_count:testB_count+testC_count] = testC

# # now store this bad boy
# np.save(basedir+'test.npy', p_rgba)

# print 'STORED BIG BOY!'
p_rgba = None # free them all

#
# same for targets
#
testA_targets = np.load(testA_targets)
testA_count = testA_targets.shape[0]
testB_targets = np.load(testB_targets)
testB_count = testB_targets.shape[0]
testC_targets = np.load(testC_targets)
testC_count = testC_targets.shape[0]

all_count = testA_count + testB_count + testC_count
NO_PATCHES = all_count

p_target = np.zeros(NO_PATCHES)

p_target[0:testA_count] = testA_targets
p_target[testA_count:testA_count+testB_count] = testB_targets
p_target[testB_count:testB_count+testC_count] = testC_targets

# now store this lady boy
np.save(basedir+'test_targets.npy', p_target)

print 'ALL DONE!'



# import numpy as np

# #
# #
# #

# basedir = '/n/regal/pfister_lab/haehn/CREMITEST/'

# testA = basedir + 'testA.npz.npy'
# testA_targets = basedir + 'testA_targets.npz.npy'
# testB = basedir + 'testB.npz.npy'
# testB_targets = basedir + 'testB_targets.npz.npy'
# testC = basedir + 'testC.npz.npy'
# testC_targets = basedir + 'testC_targets.npz.npy'

# counter = 0

# testA = np.load(testA, mmap_mode='r')
# testA_count = testA.shape[0]

# testB = np.load(testB, mmap_mode='r')
# testB_count = testB.shape[0]

# testC = np.load(testC, mmap_mode='r')
# testC_count = testC.shape[0]

# all_count = testA_count + testB_count + testC_count

# #
# # allocate large array
# # 
# PATCH_BYTES = 75*75
# NO_PATCHES = all_count
# P_SIZE = (NO_PATCHES, 4, 75,75) # rather than raveled right now

# p_rgba = np.zeros(P_SIZE, dtype=np.float32)

# p_rgba[0:testA_count] = testA
# p_rgba[testA_count:testA_count+testB_count] = testB
# p_rgba[testB_count:testB_count+testC_count] = testC

# # now store this bad boy
# np.save(basedir+'test.npy', p_rgba)

# print 'STORED BIG BOY!'
# p_rgba = None # free them all

# #
# # same for targets
# #
# testA_targets = np.load(testA_targets)
# testB_targets = np.load(testB_targets)
# testC_targets = np.load(testC_targets)

# p_target = np.zeros(NO_PATCHES)

# p_target[0:testA_count] = testA_targets
# p_target[testA_count:testA_count+testB_count] = testB_targets
# p_target[testB_count:testB_count+testC_count] = testC_targets

# # now store this lady boy
# np.save(basedir+'test_targets.npy', p_target)

# print 'ALL DONE!'
