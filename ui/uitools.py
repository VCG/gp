import sys
sys.path.append('../')

import gp

import os
import mahotas as mh
import numpy as np
import time
import skimage.measure
import cPickle as pickle

class UITools(object):

  @staticmethod
  def load_cnn():

    with open('../nets/IPMLB_FULL.p', 'rb') as f:
        cnn = pickle.load(f)

    cnn.uuid = 'IPMLB'

    return cnn




  @staticmethod
  def find_next_split_error(bigM):
    '''
    '''
    bigM_max = -1
    bigM_max_index = None
    bigM_max_z = -1
    for z,m in enumerate(bigM):
        if m.max() > bigM_max:
            bigM_max = m.max()
            bigM_max_indices = np.where(m == bigM_max)
            bigM_max_index = [bigM_max_indices[0][0], bigM_max_indices[1][0]]
            bigM_max_z = z

    return bigM_max_z, bigM_max_index, bigM_max


  @staticmethod
  def correct_split(cnn, m, mode, input_image, input_prob, input_rhoana, label1, label2, oversampling=False):

    rhoana_copy = np.array(input_rhoana)

    new_m = np.array(m)

    rhoana_copy[rhoana_copy == label2] = label1

    if mode == 'FP':
      print 'skip neighbors'


      # grab old neighbors of label 2 which are now neighbors of label1
      label2_neighbors = gp.Util.grab_neighbors(input_rhoana, label2)
      for l_neighbor in label2_neighbors:

        if l_neighbor == 0:
          continue

        if label1 == l_neighbor:
          continue

        # get old score
        old_score = new_m[label2, l_neighbor]

        label1_neighbor_score = new_m[label1, l_neighbor]

        # and now choose the max of these two
        new_m[label1, l_neighbor] = max(label1_neighbor_score, old_score)
        new_m[l_neighbor, label1] = max(label1_neighbor_score, old_score)


      # label2 does not exist anymore
      new_m[:,label2] = -2
      new_m[label2, :] = -2      

      return new_m, rhoana_copy


    # label2 does not exist anymore
    new_m[:,label2] = -2
    new_m[label2, :] = -2

    label1_neighbors = gp.Util.grab_neighbors(rhoana_copy, label1)

    # print 'neighbors', label1_neighbors

    for l_neighbor in label1_neighbors:
      # recalculate new neighbors of l

      if l_neighbor == 0:
          # ignore neighbor zero
          continue

      prediction = gp.Patch.grab_group_test_and_unify(cnn, input_image, input_prob, rhoana_copy, label1, l_neighbor, oversampling=oversampling)

      new_m[label1,l_neighbor] = prediction
      new_m[l_neighbor,label1] = prediction


    return new_m, rhoana_copy


  @staticmethod
  def skip_split(m, label1, label2):

    new_m = np.array(m)

    new_m[label1, label2] = -3
    new_m[label2, label1] = -3

    return new_m

  @staticmethod
  def VI(gt, seg):
      # total_vi = 0
      slice_vi = []    
      for i in range(10):
          current_vi = gp.Util.vi(gt[i].astype(np.int64), seg[i].astype(np.int64))
          # total_vi += current_vi
          slice_vi.append(current_vi)
      # total_vi /= 10
      return np.mean(slice_vi), np.median(slice_vi), slice_vi


  @staticmethod
  def adaptedRandError(seg, gt):
      # total_vi = 0
      slice_vi = []    
      for i in range(10):
          current_vi = gp.metrics.adapted_rand(seg[i].astype(np.int64), gt[i].astype(np.int64))
          # total_vi += current_vi
          slice_vi.append(current_vi)
      # total_vi /= 10
      return np.mean(slice_vi), np.median(slice_vi), slice_vi
















