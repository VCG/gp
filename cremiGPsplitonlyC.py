
import gp

import cPickle as pickle
import numpy as np
import os


HOMEDIR = '/n/home05/haehn/'
REGALDIR = '/n/regal/pfister_lab/haehn/'
DATADIR = HOMEDIR + 'data/CREMIGP/TEST/'
OUTDIR = REGALDIR + 'CREMIBIGSPLITONLY_C/'

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
test_slices = range(50,55)# + range(25+20,50) + range(50+20,75)
for z in test_slices:
    image, prob, gold, rhoana = gp.Util.read_cremi_section(os.path.expanduser('~/data/CREMIGP/TEST/'), z)
    input_image.append(image)
    input_prob.append(255.-prob)
    input_gold.append(gold)
    input_rhoana.append(rhoana)    

original_mean_VI, original_median_VI, original_VI_s = gp.Legacy.VI(input_gold, input_rhoana)





bigM_cremi_file = OUTDIR+'bigM_gp.p'
if os.path.exists(bigM_cremi_file):
  print 'loading bigM'
  with open(bigM_cremi_file, 'rb') as f:
    bigM = pickle.load(f)
    bigM = bigM[50:55]
# else:
#   print 'creating bigM'
#   bigM = gp.Legacy.create_bigM_without_mask(cnn, input_image, input_prob, input_rhoana, verbose=True, max=1000000)
#   with open(bigM_cremi_file, 'wb') as f:
#     pickle.dump(bigM, f)  










#
# run auto merge correction
#
cylinder_vi_95_file = OUTDIR + '/cremi_vi_00_w_merge_NEW.p'

# merge_vis = OUTDIR + '/cremi_merge_auto00_vis.p'
split_vis = OUTDIR + '/cremi_split_auto00_vis.p'

# merge_fixes = OUTDIR + '/cremi_merge_auto00_fixes.p'
split_fixes = OUTDIR + '/cremi_split_auto00_fixes.p'

output_95 = OUTDIR + '/cremi_auto00_output.p'

if os.path.exists(cylinder_vi_95_file):
  print 'Loading merge errors p < .05 and split errors p > .00 from file..'
  with open(cylinder_vi_95_file, 'rb') as f:
    cylinder_vi_95 = pickle.load(f)

else:      
  #



#
# run auto split correction
#
  print 'Correcting split errors with p > .0'
  bigM_cylinder_after_95, out_cylinder_volume_after_auto_95, cylinder_auto_fixes_95, cylinder_auto_vi_s_95, vi_s_per_step2 = gp.Legacy.splits_global_from_M_automatic(cnn, bigM, input_image, input_prob, input_rhoana, input_gold, sureness_threshold=.00)

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
# run oracle merge correction
#
cylinder_vi_95_file = OUTDIR + '/cremi_vi_simuser_w_merge_NEW.p'

# merge_vis = OUTDIR + '/cremi_merge_simuser_vis.p'
split_vis = OUTDIR + '/cremi_split_simuser_vis.p'

# merge_fixes = OUTDIR + '/cremi_merge_simuser_fixes.p'
split_fixes = OUTDIR + '/cremi_split_simuser_fixes.p'

output_95 = OUTDIR + '/cremi_simuser_output.p'

if os.path.exists(cylinder_vi_95_file):
  print 'Loading merge errors p < .05 and split errors p > .95 from file..'
  with open(cylinder_vi_95_file, 'rb') as f:
    cylinder_vi_95 = pickle.load(f)

else:      


#
# run oracle split correction
#
  print 'Correcting split errors with p > .95'
  bigM_cylinder_after_95, out_cylinder_volume_after_auto_95, cylinder_auto_fixes_95, cylinder_auto_vi_s_95, vi_s_per_step2 = gp.Legacy.splits_global_from_M(cnn, bigM, input_image, input_prob, input_rhoana, input_gold, hours=-1)

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

