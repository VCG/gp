import cPickle as pickle
import os; import sys; sys.path.append('..')
import gp
import gp.nets as nets

PATCH_PATH = ('ipmb')

X_train, y_train, X_test, y_test = gp.Patch.load_rgb(PATCH_PATH)


cnn = nets.RGBANetPlus()

cnn = cnn.fit(X_train, y_train)

test_accuracy = cnn.score(X_test, y_test)

print test_accuracy

# store CNN
sys.setrecursionlimit(1000000000)
with open(os.path.expanduser('~/Projects/gp/nets/IPMB_FULL.p'), 'wb') as f:
  pickle.dump(cnn, f, -1)
