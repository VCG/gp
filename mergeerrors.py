import cPickle as pickle
import gp
import sys

Z = sys.argv[1]

OUTPUT = '/n/regal/pfister_lab/haehn/MERGEERRORS/'

print 'running for slice', Z


# load CNN
with open('nets/IPMLB_FULL.p', 'rb') as f:
  cnn = pickle.load(f)

cnn.uuid = 'IPMLB'


# load slice
image, prob, mask, gold, rhoana = gp.Util.read_section('/n/home05/haehn/data/cylinderNEW/', int(Z), verbose=False)

merge_errors = gp.Legacy.get_top5_merge_errors(cnn, [image], [prob], [rhoana], True)

with open(OUTPUT + str(Z) + '.p') as f:
  pickle.dump(merge_errors, f)
