import numpy as np
import sys
sys.path.append('../')
import gp
import os

import cPickle as pickle

e_p = []
p = []
for z in range(250,300):
    
    image, prob, mask, gold, rhoana = gp.Util.read_section(os.path.expanduser('~/data/cylinderNEW'),z)
    
    error_patches, patches = gp.Patch.patchify_maxoverlap(image, prob, mask, rhoana, gold, sample_rate=1, clamp_result=False)
    
    e_p.append(error_patches)
    p.append(patches)    

OUTDIR = '/n/regal/pfister_lab/haehn/CYLPATCHES/'

with open(OUTDIR+'e_p.p', 'wb') as f:
  pickle.dump(e_p, f)

with open(OUTDIR+'p.p', 'wb') as f:
  pickle.dump(p, f)

print 'all done'
