import numpy as np
import matplotlib.pyplot as plt
import argparse
formatter = argparse.ArgumentDefaultsHelpFormatter
parser = argparse.ArgumentParser(formatter_class=formatter)
parser.add_argument('-du','--DU', type=int,  help='DU number ypu want to analyze, type 0 if all DUs', required=False)

args = parser.parse_args()

du = args.DU
if du==0:
    alldus=True
else:
    alldus=False

path_ = '/Users/stefanotugliani/Desktop/dati_ixpe/swift/event_files/02250901/'

if alldus==True:
    path = path_ + f'ALLDU_v/'
else:
    path_du = path_ + f'DU{du}/'

segs = np.array([70,80,90,100])

thr_array, ttest_pvalue_q, ttest_pvalue_u = [], [], []

for i in range(len(segs)):
    thr_ = np.load(path+f'/seg{segs[i]}s/threshold_ALLdu_new.npy')
    thr_array.append(thr_)
    ttest_pvalue_ = np.load(path+f'ttest_data_{segs[i]}s.npy')
    ttest_pvalue_q.append(ttest_pvalue_[:,0])
    ttest_pvalue_u.append(ttest_pvalue_[:,1])

marker_list = ['o', 'v', '^', '<', '>',
    's', 'p', '*', 'h', 'H', '+', 'x', 'X', 'D', 'P', '8']

fig, ax = plt.subplots(2,1,figsize=(8,8),sharex=True)
for i in range(len(segs)):
    ax[0].plot(thr_array[i], np.array(ttest_pvalue_q[i])*100., label=f'{segs[i]}', color=f'C{i}',marker='', linestyle='-')
    ax[1].plot(thr_array[i], np.array(ttest_pvalue_u[i])*100., label=f'{segs[i]}', color=f'C{i}',marker='', linestyle='-')
    
for a in ax:
    a.axhspan(0, 5, facecolor='lightgray', alpha=0.5)
    a.axhline(y=5, color='black', linestyle='--')

ax[1].set_xlabel('thresholds')
ax[0].set_ylabel('pvalue q')
ax[1].set_ylabel('pvalue u')

ax[0].axhline(y=5, color='black')
ax[1].axhline(y=5, color='black')

ax[0].grid(True)
ax[1].grid(True)
ax[0].legend()
ax[1].legend()
ax[0].set_yscale('log')
ax[1].set_yscale('log')
fig.subplots_adjust(hspace=0.05)
fig.savefig('/Users/stefanotugliani/Desktop/dati_ixpe/swift/pvalue_thresholds_Q_U_seg_comp_70_80_90_100.png', dpi=300, bbox_inches='tight')


plt.show()