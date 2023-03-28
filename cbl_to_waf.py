
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import TotalDepth
from TotalDepth.LIS.core import File, FileIndexer

import sys

lis_filename = Path(sys.argv[1])

file = File.FileRead(str(lis_filename))
file_idx = FileIndexer.FileIndex(file)
log_passes = [lp for lp in file_idx.genLogPasses()]

log_passes[0].logPass.setFrameSet(file)
sc = [sc for sc in log_passes[0].logPass.genFrameSetScNameUnit()]
data = log_passes[0].logPass.frameSet.frames

block_idx = {}

n = 0
for block in log_passes[0].logPass._dfsr.dsbBlocks:
    block_name = block.mnem.strip().decode()
    k = block.values()
    block_idx[block_name] = (n, n + k, k)
    n += k
block_idx

curve_logs = {name: block_idx[name][0] for name, (i0, i1, k) in block_idx.items() if k == 1}
arr_logs = {name: block_idx[name] for name, (i0, i1, k) in block_idx.items() if k > 1}

null = -999.25
data[data == null] = np.nan

data_extr = {}
for name, idx in curve_logs.items():
    data_extr[name] = data[:, idx]
    
for name, (i0, i1, k) in arr_logs.items():
    data_extr[name] = data[:, i0: i1]

indices = {
    'map': {
        'w5': 'w5_idx',
        'w3': 'w3_idx',
        'ws1': 'ws_idx',
        'ws2': 'ws_idx',
        'ws3': 'ws_idx',
        'ws4': 'ws_idx',
        'ws5': 'ws_idx',
        'ws6': 'ws_idx',
        'WVFC': 'wcal_idx',
    },
    'data': {
        'w3_idx': np.linspace(0, 500, 250 + 1),
        'w5_idx': np.linspace(0, 1500, 750 + 1),
        'ws_idx': np.linspace(0, 300, 150 + 1),
        'wcal_idx': np.linspace(0, 600, 200 + 1),
    },
    'units': {
        'w3_idx': 'us',
        'w5_idx': 'us',
        'ws_idx': 'us',
        'wcal_idx': 'us',
    }
}

def get_index_for(name):
    index_name = indices['map'][name]
    return {
        'data': indices['data'][index_name],
        'unit': indices['units'][index_name],
    }

import lasio
import pandas as pd

index_data = None
filename = f"{lis_filename.stem}_curves.las"

names = [n for n in curve_logs.keys()]

df = pd.DataFrame({name: data_extr[name] for name in names})
df = df.set_index('DEPT')

las = lasio.LASFile()
las.well.WELL = lis_filename.name
las.set_data_from_df(df)

with open(filename, "w") as f:
    las.write(f)

log_aliases = {
    'w3': 'wvf_3ft',
    'w5': 'wvf_5ft',
    'ws1': 'wvf_18in_s1',
    'ws2': 'wvf_18in_s2',
    'ws3': 'wvf_18in_s3',
    'ws4': 'wvf_18in_s4',
    'ws5': 'wvf_18in_s5',
    'ws6': 'wvf_18in_s6',
    'WVFC': 'wvf_cal'
}

import wellcadformats

for name in arr_logs.keys():
    alias = log_aliases[name]
    
    filename = f"{lis_filename.stem}_{alias}.waf"
    arr_data = data_extr[name]
    arr_idx_data = get_index_for(name)
    
    log = wellcadformats.WAF()
    log.generate(arr_data, depths=data_extr['DEPT'], times=arr_idx_data['data'])
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    log.imshow(ax=ax)
    ax.set_title(filename)
    
    with open(filename, 'w') as f:
        log.to_file(f)

