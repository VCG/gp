import cPickle as pickle
import os; import sys; sys.path.append('..')
import gp
import gp.nets as nets

# PATCH_PATH = ('ipmlb')

X_train, y_train, X_test, y_test = gp.Patch.load_big()

print 'Training patches', y_train.shape[0]
print 'Test patches', y_test.shape[0]


cnn = nets.RGBANetPlus()

cnn = cnn.fit(X_train, y_train)

test_accuracy = cnn.score(X_test, y_test)

print test_accuracy

# store CNN
sys.setrecursionlimit(1000000000)
with open(os.path.expanduser('/n/regal/pfister_lab/haehn/FINAL/IPMLB_before_NP/IPMLB_FULL_BIG.p'), 'wb') as f:
  pickle.dump(cnn, f, -1)
with open(os.path.expanduser('~/Projects/gp/nets/IPMLB_FULL_BIG.p'), 'wb') as f:
  pickle.dump(cnn, f, -1)

print 'STORED.'
