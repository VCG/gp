import cPickle as pickle
import os; import sys; sys.path.append('..')
import gp
import gp.nets as nets

# PATCH_PATH = ('ipmlb')

X_train, y_train, X_test, y_test = gp.Patch.load_cremi()
# X_train, y_train = gp.Patch.load_cremi()

print 'Training patches', y_train.shape[0]
print 'Test patches', y_test.shape[0]


cnn = nets.RGBANetPlus()

cnn = cnn.fit(X_train, y_train)


# store CNN
sys.setrecursionlimit(1000000000)
with open('/n/regal/pfister_lab/haehn/CREMITEST/IPMLB_FULL_CREMI_FINAL.p', 'wb') as f:
  pickle.dump(cnn, f, -1)
with open(os.path.expanduser('~/Projects/gp/nets/IPMLB_FULL_CREMI_FINAL.p'), 'wb') as f:
  pickle.dump(cnn, f, -1)


test_accuracy = cnn.score(X_test, y_test)

print test_accuracy

print 'STORED.'
