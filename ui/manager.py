import cPickle as pickle
import numpy as np
import os

import sys
sys.path.append('../')

import gp
from uitools import UITools

class Manager(object):

  def __init__(self, output_dir):
    '''
    '''
    self._data_path = '/home/d/dojo_xp/data/'
    self._output_path = os.path.join(self._data_path, 'ui_out', output_dir)
    self._merge_errors = None

    self._corrections = []
    self._correction_times = []
    self._correction_vis = []

    self._mode = 'GP'

  def start( self, mode ):
    '''
    '''

    self._cnn = UITools.load_cnn()

    self._mode = mode

    if self._mode == 'GP*':
        # now we use the matlab engine
        print 'Using Active Label Suggestion'
        import matlab.engine
        eng = matlab.engine.start_matlab()


        self._merge_errors = self.load_merge_errors()
        self._bigM = self.load_split_errors()

        # let's generate our active label features and store a lsit


    elif self._mode == 'GP':
        print 'Using GP proper'

        self._merge_errors = self.load_merge_errors()
        self._bigM = self.load_split_errors()


    elif self._mode == 'FP':
        print 'Using FP'
        self._merge_errors = []

        self._bigM = self.load_split_errors(filename='bigM_fp.p')

    elif self._mode == 'TEST':
        print 'Test mode using FP'
        self._merge_errors = []

        self._bigM = self.load_split_errors(filename='bigM_fp_test.p')


    else:
        print 'WRONG MODE, should be GP, GP* or FP'
        sys.exit(2)

    # load data
    if self._mode == 'TEST':
        print 'We are using dummy data for testing'
        input_image, input_prob, input_gold, input_rhoana, dojo_bbox = gp.Legacy.read_dojo_test_data() 
        self._mode = 'FP'
    else:
        input_image, input_prob, input_gold, input_rhoana, dojo_bbox = gp.Legacy.read_dojo_data() 

    self._input_image = input_image
    self._input_prob = input_prob
    self._input_gold = input_gold
    self._input_rhoana = input_rhoana
    self._dojo_bbox = dojo_bbox

    print 'VI at start:', UITools.VI(self._input_gold, self._input_rhoana)[1]
    print 'aRE at start:', UITools.adaptedRandError(self._input_rhoana, self._input_gold)[1]


  def gen_active_label_features(self):
    '''
    '''
    active_labels_file = os.path.join(self._data_path, 'split_active_labels.p')
    if os.path.exists(active_labels_file):
        with open(active_labels_file, 'rb') as f:
            feature_vector = pickle.load(f)
        print 'Feature vector loaded from pickle.'

    else:
        print 'Calculating active labels...'

        # we work on a copy of bigM, let's call it bigD like daddy
        bigD = self._bigM.copy()

        import theano
        import theano.tensor as T
        from lasagne.layers import get_output

        # go from highest prob to lowest in our bigD
        prediction = np.inf
        while prediction > -1:
            z, labels, prediction = UITools.find_next_split_error(bigD)

            # create patch
            l,n = labels
            patches = []
            patches_l, patches_n = Patch.grab(image, prob, segmentation, l, n, sample_rate=10, oversampling=False)
            patches += patches_l
            patches += patches_n

            grouped_patches = Patch.group(patches)





            # let CNN without softmax analyze the patch to create features
            x = X_test[100].reshape(1,4,75,75)
            layer = net.layers_['hidden5']
            xs = T.tensor4('xs').astype(theano.config.floatX)
            get_activity = theano.function([xs], get_output(layer, xs))

            activity = get_activity(x)

        # create feature vector


        # store feature vector to pickle
        with open(active_labels_file, 'wb') as f:
            pickle.dump(feature_vector, f)
        print 'Feature vector stored.'


    # Now, we need to represent the distance between each of these items using the graph Laplacian matrix 'LGReg'.
    # We're going to build this now using a MATLAB function - 'BuildLGRegularizer.m'

    # First, we need to set two parameters, as this is an approximation of the true graph laplacian to allow us to
    # use this on very large datasets
    manifoldDim = 17;
    kNNSize = 20;
    # Second, we set the regularization strength of this graph Laplacian
    lambdaRP = 0.005;

    # Next, we call the function
    #LGReg = eng.BuildLGRegularizer( x, manifoldDim, kNNSize, nargout=1 );
    # ...but, two problems:
    # 1) We need to transform our numpy array x into something MATLAB can handle

    xM = matlab.double( size=[nItems, nFeatures] )
    for j in range(0, nFeatures-1):
        for i in range(0, nItems-1):
            xM[i][j] = x[i][j];

    # 2) LGReg is a 'sparse' matrix type, and python doesn't support that. 
    # Let's leave the output variable in the MATLAB workspace, and until we need to use it.
    eng.workspace['xM'] = xM;
    # We also need to pass our function variables
    eng.workspace['nItems'] = nItems;
    eng.workspace['nFeatures'] = nFeatures;
    eng.workspace['lambdaRP'] = lambdaRP;
    eng.workspace['manifoldDim'] = manifoldDim;
    eng.workspace['kNNSize'] = kNNSize;

    # OK, now let's call our function
    eng.eval( "LGReg = BuildLGRegularizer( xM, manifoldDim, kNNSize )", nargout=0 )


  def load_merge_errors(self, filename='merges_new_cnn.p'):
    '''
    '''
    with open(os.path.join(self._data_path, filename), 'rb') as f:
      merge_errors = pickle.load(f)

    return sorted(merge_errors, key=lambda x: x[3], reverse=False)

  def load_split_errors(self, filename='bigM_new_cnn.p'):
    '''
    '''
    with open(os.path.join(self._data_path, filename), 'rb') as f:
      bigM = pickle.load(f)

    return bigM

  def get_next_merge_error(self):
    '''
    '''
    if len(self._merge_errors) == 0:
        return None
    return self._merge_errors[0]

  def get_next_split_error(self):
    '''
    '''
    if self._mode == 'GP' or self._mode == 'FP':
        z, labels, prediction = UITools.find_next_split_error(self._bigM)

    elif self._mode == 'GP*':
        #
        # here, let's check for the next active label suggestion
        # but only if we already corrected twice
        #
        pass


    self._split_error = (z, labels, prediction)

    return self._split_error

  def get_merge_error_image(self, merge_error, number):

    border = merge_error[3][number][1]


    z = merge_error[0]
    label = merge_error[1]
    prob = merge_error[2]

    input_image = self._input_image
    input_prob = self._input_prob
    input_rhoana = self._input_rhoana


    a,b,c,d,e,f,g,h,i,j = gp.Legacy.get_merge_error_image(input_image[z], input_rhoana[z], label, border)

    border_before = b
    labels_before = h
    border_after = c
    labels_after = i
    slice_overview = g
    cropped_slice_overview = j

    return border_before, border_after, labels_before, labels_after, slice_overview, cropped_slice_overview
    
  def get_split_error_image(self, split_error, number=1):

    z = split_error[0]
    labels = split_error[1]

    input_image = self._input_image
    input_prob = self._input_prob
    input_rhoana = self._input_rhoana

    a,b,c,d,e,f,g = gp.Legacy.get_split_error_image(input_image[z], input_rhoana[z], labels)

    labels_before = b
    borders_before = c
    borders_after = d
    labels_after = e
    slice_overview = f
    cropped_slice_overview = g

    return borders_before, borders_after, labels_before, labels_after, slice_overview, cropped_slice_overview

  def correct_merge(self, clicked_correction):

    input_image = self._input_image
    input_prob = self._input_prob
    input_rhoana = self._input_rhoana

    if not clicked_correction == 'current':
        clicked_correction = int(clicked_correction)-1

        #
        # correct the merge
        #
        merge_error = self._merge_errors[0]
        number = clicked_correction
        border = merge_error[3][number][1]
        z = merge_error[0]
        label = merge_error[1]

        a,b,c,d,e,f,g,h,i,j = gp.Legacy.get_merge_error_image(input_image[z], input_rhoana[z], label, border)

        new_rhoana = f

        self._input_rhoana[z] = new_rhoana

        vi = UITools.VI(self._input_gold, input_rhoana)
        # print 'New global VI', vi[1]
        self._correction_vis.append(vi[2])        

        #
        # and remove the original label from our bigM matrix
        #
        self._bigM[z][label,:] = -3
        self._bigM[z][:,label] = -3
        
        # now add the two new labels
        label1 = new_rhoana.max()
        label2 = new_rhoana.max()-1
        new_m = np.zeros((self._bigM[z].shape[0]+2, self._bigM[z].shape[1]+2), dtype=self._bigM[z].dtype)
        new_m[:,:] = -1
        new_m[0:-2,0:-2] = self._bigM[z]

        print 'adding', label1, 'to', z

        new_m = gp.Legacy.add_new_label_to_M(self._cnn, new_m, input_image[z], input_prob[z], new_rhoana, label1)
        new_m = gp.Legacy.add_new_label_to_M(self._cnn, new_m, input_image[z], input_prob[z], new_rhoana, label2)

        # re-propapage new_m to bigM
        self._bigM[z] = new_m


    # remove merge error
    del self._merge_errors[0]

    mode = 'merge'
    if len(self._merge_errors) == 0:

        mode = 'split'

    return mode

  def correct_split(self, clicked_correction):

    input_image = self._input_image
    input_prob = self._input_prob
    input_rhoana = self._input_rhoana

    split_error = self._split_error

    z = split_error[0]
    labels = split_error[1]
    m = self._bigM[z]

    if clicked_correction == 'current':
        # we skip this split
        # print 'FP or current'
        new_m = UITools.skip_split(m, labels[0], labels[1])
        self._bigM[z] = new_m

    else:
        # we correct this split
        # print 'fixing slice',z,'labels', labels
        # vi = gp.Util.vi(self._input_gold[z], self._input_rhoana[z])
        # print 'bef vi', vi
        new_m, new_rhoana = UITools.correct_split(self._cnn, m, self._mode, input_image[z], input_prob[z], input_rhoana[z], labels[0], labels[1], oversampling=False)
        self._bigM[z] = new_m
        self._input_rhoana[z] = new_rhoana
        # vi = gp.Util.vi(self._input_gold[z], self._input_rhoana[z])
        # print 'New VI', vi[0]
        vi = UITools.VI(self._input_gold, self._input_rhoana)
        print 'New global VI', vi[0]
        self._correction_vis.append(vi[2])

        # self.finish()
        
    return 'split'


  def store(self):

    vi = UITools.VI(self._input_gold, self._input_rhoana)
    print 'New VI', vi[1]
    are = UITools.adaptedRandError(self._input_rhoana, self._input_gold)
    print 'New aRE', are[1]

    if not os.path.exists(self._output_path):
        os.makedirs(self._output_path)

    # store our changed rhoana
    with open(os.path.join(self._output_path, 'ui_results.p'), 'wb') as f:
        pickle.dump(self._input_rhoana, f)

    # store the times
    with open(os.path.join(self._output_path, 'times.p'), 'wb') as f:
        pickle.dump(self._correction_times, f)

    # store the corrections
    with open(os.path.join(self._output_path, 'corrections.p'), 'wb') as f:
        pickle.dump(self._corrections, f)

    with open(os.path.join(self._output_path, 'correction_vis.p'), 'wb') as f:
        pickle.dump(self._correction_vis, f)

    print 'All stored.'







