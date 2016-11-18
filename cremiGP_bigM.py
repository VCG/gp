
import gp

import cPickle as pickle
import numpy as np
import os


HOMEDIR = '/n/home05/haehn/'
REGALDIR = '/n/regal/pfister_lab/haehn/'
DATADIR = HOMEDIR + 'data/CREMIGP/TEST/'
OUTDIR = REGALDIR + 'CREMIBIG/'

#
# load cnn
#
with open('nets/IPMLB_FULL_CREMI_FINAL.p', 'rb') as f:
  cnn = pickle.load(f)
cnn.uuid = 'IPMLB'

#
# load data
#
input_image = []
input_prob = []
input_gold = []
input_rhoana = []
test_slices = range(75)# + range(25+20,50) + range(50+20,75)
for z in test_slices:
    image, prob, gold, rhoana = gp.Util.read_cremi_section(os.path.expanduser('~/data/CREMIGP/TEST/'), z)
    input_image.append(image)
    input_prob.append(255.-prob)
    input_gold.append(gold)
    input_rhoana.append(rhoana)    

original_mean_VI, original_median_VI, original_VI_s = gp.Legacy.VI(input_gold, input_rhoana)




# find merge errors, if we did not generate them before
bigM_cremi_file = OUTDIR+'bigM_gp.p'
if os.path.exists(bigM_cremi_file):
  print 'loading bigM'
  with open(bigM_cremi_file, 'rb') as f:
    bigM = pickle.load(f)
else:
  print 'creating bigM'
  bigM = gp.Legacy.create_bigM_without_mask(cnn, input_image, input_prob, input_rhoana, verbose=True, max=1000000)
  with open(bigM_cremi_file, 'wb') as f:
    pickle.dump(bigM, f)  






print 'All done.'

