import cPickle as pickle
import os; import sys; sys.path.append('..')
import gp
import gp.nets as nets

PATCH_PATH = ('iplb')

X_train, y_train, X_test, y_test = gp.Patch.load_rgb(PATCH_PATH)
X_train = X_train[:,:-1,:,:]
X_test = X_test[:,:-1,:,:]

cnn = nets.RGNetPlus()

cnn = cnn.fit(X_train, y_train)

test_accuracy = cnn.score(X_test, y_test)

print test_accuracy

# store CNN
sys.setrecursionlimit(1000000000)
with open(os.path.expanduser('~/Projects/gp/nets/IP_FULL.p'), 'wb') as f:
  pickle.dump(cnn, f, -1)
