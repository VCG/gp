import cPickle as pickle
import gp
import glob
import mahotas as mh
import numpy as np
import os
import time


def generate_patches(start_slice, end_slice):

    patch_index = 0

    all_patches_count = 0
    patch_list = []
    all_error_patches = []
    all_correct_patches = []
    
    for z in range(start_slice, end_slice):

        t0 = time.time()
        print 'working on slice', z
        input_image, input_prob, input_gold, input_rhoana = gp.Util.read_cremi_section(os.path.expanduser('~/data/CREMIGP/TEST/'), z)


        error_patches, patches = gp.Patch.patchify_maxoverlap(input_image, input_prob, np.zeros((1,1250,1250),dtype=np.bool), input_rhoana, input_gold, sample_rate=1)
        
        print 'Generated', len(error_patches), 'split error patches and', len(patches), ' correct patches in', time.time()-t0, 'seconds.'
        
        patch_list.append(patches)
        all_error_patches += error_patches
        all_correct_patches += patches
        
    with open('/n/regal/pfister_lab/haehn/CREMITEST/e_p.p', 'wb') as f:
      pickle.dump(all_error_patches, f)

    with open('/n/regal/pfister_lab/haehn/CREMITEST/p.p', 'wb') as f:
      pickle.dump(all_correct_patches, f)
    
    NO_PATCHES = len(all_error_patches) + len(all_correct_patches)

    print 'We have a total of',NO_PATCHES,'patches.'
    print 'Errors:',len(all_error_patches)
    print 'Correct:',len(all_correct_patches)    
    
    PATCH_BYTES = 75*75
    P_SIZE = (NO_PATCHES, 4, 75,75) # rather than raveled right now
    
    p_rgba = np.zeros(P_SIZE, dtype=np.float32)
    

    p_target = np.zeros(NO_PATCHES)


    i = 0
    for p in all_error_patches:

        p_rgba[i][0] = p['image']
        p_rgba[i][1] = 1. - p['prob'] ### INVERT PROB
        p_rgba[i][2] = p['merged_array']
        p_rgba[i][3] = p['larger_border_overlap']  
        
        p_target[i] = 1 # <--- important
        i += 1

        
    for p in all_correct_patches:

        p_rgba[i][0] = p['image']
        p_rgba[i][1] = 1. - p['prob'] ### INVERT PROB
        p_rgba[i][2] = p['merged_array']
        p_rgba[i][3] = p['larger_border_overlap']
             
        
        p_target[i] = 0 # <--- important
        i+=1
        
    
    return p_rgba, p_target



def shuffle_in_unison_inplace(a, b):
    assert len(a) == len(b)
    p = np.random.permutation(len(a))
    return a[p], b[p]



def run(PATCH_PATH, start_slice, end_slice, filename):
    
    if not os.path.exists(PATCH_PATH):
        os.makedirs(PATCH_PATH)
    
    p = generate_patches(start_slice, end_slice)
    
    shuffled = shuffle_in_unison_inplace(p[0],
                                         p[1]
                                        )
    
    print 'saving..'
    np.save(PATCH_PATH+filename+'.npz', shuffled[0])
    np.save(PATCH_PATH+filename+'_targets.npz', shuffled[1])
    print 'Done!'


run('/n/regal/pfister_lab/haehn/CREMITEST/', 0, 17, 'trainA')
run('/n/regal/pfister_lab/haehn/CREMITEST/', 17, 25, 'testA')
run('/n/regal/pfister_lab/haehn/CREMITEST/', 25, 25+17, 'trainB')
run('/n/regal/pfister_lab/haehn/CREMITEST/', 25+17, 50, 'testB')
run('/n/regal/pfister_lab/haehn/CREMITEST/', 50, 50+17, 'trainC')
run('/n/regal/pfister_lab/haehn/CREMITEST/', 50+17, 75, 'testC')

#run('/n/regal/pfister_lab/haehn/FINAL/IPMLB_before_NP', 10, 20, 'train', False)
