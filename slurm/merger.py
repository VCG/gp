import numpy as np

#
#
#

basedir = '/n/regal/pfister_lab/haehn/FINAL/IPMLB_before_NP/'

train1 = basedir + 'train1.npz'
train1_targets = basedir + 'train1_targets.npz'
train2 = basedir + 'train2b.npz.npy'
train2_targets = basedir + 'train2b_targets.npz.npy'
train3 = basedir + 'train3b.npz.npy'
train3_targets = basedir + 'train3b_targets.npz.npy'
train4 = basedir + 'train4.npz'
train4_targets = basedir + 'train4_targets.npz'
train5 = basedir + 'train5b.npz.npy'
train5_targets = basedir + 'train5b_targets.npz.npy'

counter = 0

train1 = np.load(train1, mmap_mode='r')
train1_count = train1['rgba'].shape[0]

train2 = np.load(train2, mmap_mode='r')
train2_count = train2.shape[0]

train3 = np.load(train3, mmap_mode='r')
train3_count = train3.shape[0]

train4 = np.load(train4, mmap_mode='r')
train4_count = train4['rgba'].shape[0]

train5 = np.load(train5, mmap_mode='r')
train5_count = train5.shape[0]

all_count = train1_count + train2_count + train3_count + train4_count + train5_count

#
# allocate large array
# 
PATCH_BYTES = 75*75
NO_PATCHES = all_count
P_SIZE = (NO_PATCHES, 4, 75,75) # rather than raveled right now

p_rgba = np.zeros(P_SIZE, dtype=np.float32)

p_rgba[0:train1_count] = train1['rgba']
p_rgba[train1_count:train1_count+train2_count] = train2
p_rgba[train2_count:train2_count+train3_count] = train3
p_rgba[train3_count:train3_count+train4_count] = train4['rgba']
p_rgba[train4_count:train4_count+train5_count] = train5

# now store this bad boy
np.save(basedir+'train.npy', p_rgba)

print 'STORED BIG BOY!'
train1 = None
train2 = None
train3 = None
train4 = None
train5 = None
p_rgba = None # free them all

#
# same for targets
#
train1_targets = np.load(train1_targets)
train2_targets = np.load(train2_targets)
train3_targets = np.load(train3_targets)
train4_targets = np.load(train4_targets)
train5_targets = np.load(train5_targets)

p_target = np.zeros(NO_PATCHES)

p_target[0:train1_count] = train1_targets['targets']
p_target[train1_count:train1_count+train2_count] = train2_targets
p_target[train2_count:train2_count+train3_count] = train3_targets
p_target[train3_count:train3_count+train4_count] = train4_targets['targets']
p_target[train4_count:train4_count+train5_count] = train5_targets

# now store this lady boy
np.save(basedir+'train_targets.npy', p_target)

print 'ALL DONE!'
