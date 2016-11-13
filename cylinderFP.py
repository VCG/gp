
import gp

import cPickle as pickle
import numpy as np
import os


HOMEDIR = '/n/home05/haehn/'
REGALDIR = '/n/regal/pfister_lab/haehn/'
DATADIR = HOMEDIR + 'data/cylinderNEW/'
OUTDIR = REGALDIR + 'cylinderFP/'

#
# load cnn
#
with open('nets/IPMLB_FULL.p', 'rb') as f:
  cnn = pickle.load(f)
cnn.uuid = 'IPMLB'

#
# load data
#
input_image = []
input_prob = []
input_rhoana = []
input_gold = []
for z in range(250, 300):
    image, prob, mask, gold, rhoana = gp.Util.read_section(DATADIR, z, verbose=False)

    input_image.append(image)
    input_prob.append(255.-prob)
    input_rhoana.append(rhoana)
    input_gold.append(gold)

#
# no merge errors
#
merge_errors = []
print len(merge_errors), 'merge errors'

#
# load bigM
#
bigM_cylinder_file = OUTDIR+'bigM_fp.p'
print 'loading bigM'
with open(bigM_cylinder_file, 'rb') as f:
  bigM = pickle.load(f)

#
# run auto split correction
#
cylinder_vi_95_file = OUTDIR + '/cylinder_vi_95.p'

split_vis = OUTDIR + '/cylinder_split_auto95_vis.p'

split_fixes = OUTDIR + '/cylinder_split_auto95_fixes.p'

output_95 = OUTDIR + '/cylinder_auto95_output.p'

if os.path.exists(cylinder_vi_95_file):
  print 'Loading split errors p > .95 from file..'
  with open(cylinder_vi_95_file, 'rb') as f:
    cylinder_vi_95 = pickle.load(f)

else:      

#
# run auto split correction
#
  print 'Correcting split errors with p > .5'
  bigM_cylinder_after_95, out_cylinder_volume_after_auto_95, cylinder_auto_fixes_95, cylinder_auto_vi_s_95, vi_s_per_step2 = gp.Legacy.splits_global_from_M_automatic(cnn, bigM, input_image, input_prob, input_rhoana, input_gold, sureness_threshold=.5, FP=True)

  cylinder_vi_95 = gp.Legacy.VI(input_gold, out_cylinder_volume_after_auto_95)

  with open(cylinder_vi_95_file, 'wb') as f:
    pickle.dump(cylinder_vi_95, f)

  with open(split_vis, 'wb') as f:
    pickle.dump(vi_s_per_step2, f)

  with open(split_fixes, 'wb') as f:
    pickle.dump(cylinder_auto_fixes_95, f)       

  with open(output_95, 'wb') as f:
    pickle.dump(out_cylinder_volume_after_auto_95, f) 


print '   Mean VI improvement', original_mean_VI-cylinder_vi_95[0]
print '   Median VI improvement', original_median_VI-cylinder_vi_95[1]





#
# run oracle split correction
#
cylinder_vi_95_file = OUTDIR + '/cylinder_vi_simuser.p'

split_vis = OUTDIR + '/cylinder_split_simuser_vis.p'

split_fixes = OUTDIR + '/cylinder_split_simuser_fixes.p'

output_95 = OUTDIR + '/cylinder_simuser_output.p'

if os.path.exists(cylinder_vi_95_file):
  print 'Loading split errors simuser from file..'
  with open(cylinder_vi_95_file, 'rb') as f:
    cylinder_vi_95 = pickle.load(f)

else:      

#
# run oracle split correction
#
  print 'Correcting split errors with p > .95'
  bigM_cylinder_after_95, out_cylinder_volume_after_auto_95, cylinder_auto_fixes_95, cylinder_auto_vi_s_95, vi_s_per_step2 = gp.Legacy.splits_global_from_M(cnn, bigM, input_image, input_prob, input_rhoana, input_gold, hours=-1, FP=True)

  cylinder_vi_95 = gp.Legacy.VI(input_gold, out_cylinder_volume_after_auto_95)

  with open(cylinder_vi_95_file, 'wb') as f:
    pickle.dump(cylinder_vi_95, f)

  with open(split_vis, 'wb') as f:
    pickle.dump(vi_s_per_step2, f)

  with open(split_fixes, 'wb') as f:
    pickle.dump(cylinder_auto_fixes_95, f)       

  with open(output_95, 'wb') as f:
    pickle.dump(out_cylinder_volume_after_auto_95, f) 


print '   Mean VI improvement', original_mean_VI-cylinder_vi_95[0]
print '   Median VI improvement', original_median_VI-cylinder_vi_95[1]





print 'All done.'

