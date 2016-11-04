#!/usr/bin/env python
# -*- coding: utf-8 -*-


from numpy import *
from ray import imio, morpho, evaluate as ev
from scipy.ndimage import binary_dilation, generate_binary_structure
import getopt
import errno
import os
import sys
import json
import argparse

import pdb


larva_gt='/groups/flyem/proj/data/larva_fib_groundtruth_round2.h5'
medulla_gt='/groups/flyem/proj/data/larva_fib_groundtruth_round2.h5'

class Error(Exception):
    """Base-class for exceptions in this module."""

class UsageError(Error):
    def __init__(self, msg):
        self.msg = msg

def main(argv):
    parser = argparse.ArgumentParser(description='Perform VI accuracy comparison between two stacks')
    parser.add_argument('--stack1', type=str, help='Stack compared against base stack (stack path or h5)', dest='stack1', required=True)
    parser.add_argument('--synapsejson', type=str, help='JSON file with synapse annotations', dest='synapsejson', default='')
    parser.add_argument('--grayscale', type=str, help='grayscale h5 volume', dest='grayscale', required=True)
    parser.add_argument('--outdir', type=str, help='raveler output directory', dest='outdir', required=True)
    
    parser.add_argument('--relabel1', action='store_true', default=False, help='Relabel ids in stack 1 to prevent memory issues', dest='relabel1')
    parser.add_argument('--relabelbase', action='store_true', default=False, help='Relabel ids in stack base to prevent memory issues', dest='relabelbase')
    parser.add_argument('--filtersize', type=int, default=1000, help='Size below which comparisons are not made', dest='filtersize')
    parser.add_argument('--VIthres', type=float, default=0.02, help='VI difference below which is unimportant', dest='VIthres')
    parser.add_argument('--stack1_outjson', type=str, default='stack1_merged.json', help='output json file name for stack 1 (outputs over-merged bodies in stack 1)', dest='stack1_outjson')
    parser.add_argument('--stackbase_outjson', type=str, default='stackbase_merged.json', help='output json file name for stack base (outputs over-merged bodies in stack base)', dest='stackbase_outjson')

    parser.add_argument('--dilate1', type=int, default=0, help='Create and dilate edges on stack 1', dest='dilate1')
    parser.add_argument('--dilatebase', type=int, default=0, help='Create and dilate edges on base image', dest='dilatebase')

    args = parser.parse_args()

    filtersize = args.filtersize
    if args.synapsejson != '':
        filtersize = 0
    #pdb.set_trace()
    stack1=args.stack1
    stack1_int = None
    if stack1.endswith('.h5'):
        stack1_int = imio.read_image_stack(stack1)
    else: 
        stack1_int = imio.raveler_to_labeled_volume(stack1, glia=False, use_watershed=False)
    stack1_int = morpho.remove_small_connected_components(stack1_int, min_size=filtersize, in_place=True)
   
    if args.dilate1 > 0:
        conn = 1 # the connectivity, can be in {1, 2, ..., seg.ndim}
        strel = generate_binary_structure(stack1_int.ndim, conn)        
        bound = morpho.seg_to_bdry(stack1_int)
        bound = binary_dilation(bound, strel, iterations=args.dilate1)
        stack1_int[bound] = 0
 
    if args.relabel1:
        stack1_int, dummy1, dummy2 = ev.relabel_from_one(stack1_int)
    print "Imported first stack with {0} superpixels".format(unique(stack1_int).shape[0])
    #pdb.set_trace()	
    gt_fname = args.grayscale
    out_dirname = args.outdir
    gg = imio.read_image_stack(gt_fname,'volume/data')
    if len(gg.shape)==3:
        imio.raveler_output_shortcut(stack1_int+1,stack1_int+1,gg,out_dirname)    
    else:	
        imio.raveler_output_shortcut(stack1_int+1,stack1_int+1,gg[0,:,:,:],out_dirname)    
    
sys.exit(main(sys.argv))
