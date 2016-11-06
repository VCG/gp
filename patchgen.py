import gp
import glob
import mahotas as mh
import numpy as np
import os
import time

def read_section(path, z, verbose=True, withNP=True):
  '''
  '''
  image = sorted(glob.glob(os.path.join(path, 'image', '*_'+str(z).zfill(9)+'_image.png')))
  mask = sorted(glob.glob(os.path.join(path, 'mask', 'z'+str(z).zfill(8)+'.png')))   
  gold = sorted(glob.glob(os.path.join(path, 'gold', 'z'+str(z).zfill(8)+'.png')))

  if withNP:
    # load from neuroproof
    rhoana = sorted(glob.glob(os.path.join(path, 'neuroproof', '*_'+str(z).zfill(9)+'_neuroproof.png')))
  else:
    # load from segmentation
    rhoana = sorted(glob.glob(os.path.join(path, 'segmentation', '*_'+str(z).zfill(9)+'_segmentation.png')))

  prob = sorted(glob.glob(os.path.join(path, 'prob', str(z).zfill(4)+'.png')))

  if verbose:
    print 'Loading', os.path.basename(image[0])

  image = mh.imread(image[0])
  mask = mh.imread(mask[0]).astype(np.bool)
  gold = mh.imread(gold[0])
  rhoana = mh.imread(rhoana[0])
  prob = mh.imread(prob[0])

  #convert ids from rgb to single channel
  rhoana_single = np.zeros((rhoana.shape[0], rhoana.shape[1]), dtype=np.uint64)
  rhoana_single[:, :] = rhoana[:,:,0]*256*256 + rhoana[:,:,1]*256 + rhoana[:,:,2]
  gold_single = np.zeros((gold.shape[0], gold.shape[1]), dtype=np.uint64)
  gold_single[:, :] = gold[:,:,0]*256*256 + gold[:,:,1]*256 + gold[:,:,2]

  # # relabel the segmentations
  # gold_single = Util.relabel(gold_single)
  # rhoana_single = Util.relabel(rhoana_single)


  #mask the rhoana output
  rhoana_single[mask==0] = 0

  return image, prob, mask, gold_single, rhoana_single




def generate_patches(start_slice, end_slice, withNP):

    patch_index = 0

    all_patches_count = 0
    patch_list = []
    all_error_patches = []
    all_correct_patches = []
    
    for z in range(start_slice, end_slice):

        t0 = time.time()
        print 'working on slice', z
        input_image, input_prob, input_mask, input_gold, input_rhoana = read_section('/n/regal/pfister_lab/haehn/FINAL/cylinder/',z, False, withNP)

        error_patches, patches = gp.Patch.patchify_maxoverlap(input_image, input_prob, input_mask, input_rhoana, input_gold, sample_rate=1)
        
        print 'Generated', len(error_patches), 'split error patches and', len(patches), ' correct patches in', time.time()-t0, 'seconds.'
        
        patch_list.append(patches)
        all_error_patches += error_patches
        all_correct_patches += patches
        
    
    
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



def run(PATCH_PATH, start_slice, end_slice, filename, withNP):
    
    if not os.path.exists(PATCH_PATH):
        os.makedirs(PATCH_PATH)
    
    p = generate_patches(start_slice, end_slice, withNP)
    
    shuffled = shuffle_in_unison_inplace(p[0],
                                         p[1]
                                        )
    
    print 'saving..'
    np.savez(PATCH_PATH+filename+'.npz', rgba=shuffled[0])
    np.savez(PATCH_PATH+filename+'_targets.npz', targets=shuffled[1])
    print 'Done!'


run('/n/regal/pfister_lab/haehn/FINAL/IPMLB', 10, 20, 'train', True)

#run('/n/regal/pfister_lab/haehn/FINAL/IPMLB_before_NP', 10, 20, 'train', False)
