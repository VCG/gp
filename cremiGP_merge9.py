
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
test_slices = range(35,40)# + range(25+20,50) + range(50+20,75)
for z in test_slices:
    image, prob, gold, rhoana = gp.Util.read_cremi_section(os.path.expanduser('~/data/CREMIGP/TEST/'), z)
    input_image.append(image)
    input_prob.append(255.-prob)
    input_gold.append(gold)
    input_rhoana.append(rhoana)    

original_mean_VI, original_median_VI, original_VI_s = gp.Legacy.VI(input_gold, input_rhoana)




# find merge errors, if we did not generate them before
merge_error_file = OUTDIR+'/merge_errors_40.p'
if os.path.exists(merge_error_file):
  print 'Loading merge errors from file..'
  with open(merge_error_file, 'rb') as f:
    merge_errors = pickle.load(f)
else:
  print 'Finding Top 5 merge errors..'
  merge_errors = gp.Legacy.get_top5_merge_errors(cnn, input_image, input_prob, input_rhoana)
  with open(merge_error_file, 'wb') as f:
    pickle.dump(merge_errors, f)

print len(merge_errors), ' merge errors found.'






print 'All done.'

