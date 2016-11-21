import cPickle as pickle

OUTDIR = '/n/regal/pfister_lab/haehn/CREMIBIG/'

mergeerrors = []

for i in range(5,80,5):

    with open(OUTDIR+'merge_errors_'+str(i)+'.p', 'rb') as f:
        mergeerrors += pickle.load(f)

print 'Total merge errors', len(mergeerrors)

with open(OUTDIR+'merge_errors.p', 'wb') as f:
    pickle.dump(mergeerrors, f)

print 'All done!'
