#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 21:22:37 2022
functions to create reconsolidation plot from manual
@author: kziot

- with reference to the PM4Sand manual produces Figure 4.21
- original code written by Marie-Pierre Kippen for PM4Sand3D
- adapted and extended for PM4Sand2D batched calibrations by Katerina Ziotopoulou
- caution is advised to beginner Python users
- the intention of the code is to help with efficiently testing the model against 
    multiple loading paths especially when secondary parameters are altered
- Code assumes that drivers and their results are placed one level up from code
    location & each group in their own folder
- decode_name function extracts information from each FLAC-produced txt file
- create_file_list function synthesizes list of all files that satisfy criteria
    examples are provided at each location where it is used. If no files found 
    to meet criteria then plots will come out empty (this could mean the files
    are not there or the filter criteria where not setup appropriately)
"""

import numpy as np

import glob
import pandas as pd
import matplotlib.pyplot  as plt
from   matplotlib.ticker  import (AutoMinorLocator, MultipleLocator)
from   decode_PM4SandDrivers import (decode_name, create_file_list)

plt.style.use('default')
plt.style.use('ucdavis.mplstyle')

search_string = "./../PM4Sand_Reconsolidation_batch/*.txt"
# The start location takes you to the beginning of the file string (goes past the folder)
start_loc     = 35
all_files     = glob.glob(search_string)

#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 
# Dictionaries for ... styling plots
reconsol_dens_dict = {'35': 'firebrick', '55': 'tomato', '75': 'lightsalmon'}

# Markers for different densities (circles for 35% etc.)
mar_dens_dict    =  {'35': 'o', '55': 's', '75': '^', 35.0: 'o', 55.0: 's', 75.0: '^'}

ls_dict            = {'1': "-", '0': ":"}
#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 

fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize=(5.5,4), squeeze = False)

# 1) entry 1: empty -- all 'DSS' anyways
# 2) entry 2: empty -- all 'cyc' (cyclic) anyways
# 3) entry 3: empty -- all 'u' (undrained) anyways
# 4) entry 4: empty -- reading all densities
# 5) entry 5: can be left empty because we only have one sigvc and one alpha
#             if more overburdens/alphas then:
#    create_file_list(all_files,start_loc, [],[],[],[],[['4'],['0.0','0.1']],['evol'])
#    The above would read sigv = 4atm results and alphas of 0.0 and 0.1
# 6) empty 6: read summary evol txt produced as 6th txt file from FLAC

fig421_files = create_file_list(all_files,start_loc, [],[],[],[],[[],[]],['evol'])


for ind, file in enumerate(fig421_files):
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    
    df = pd.read_table(file, header = 0, delim_whitespace=True)
    df.loc[-1] = [int(density)/100, 0, 0, 0]
    df.index = df.index + 1
    df       = df.sort_index()
  
    df.plot(ax=axs[0,0], x = 'gamma_max(%)', y = 'vol_strain(%)',
            color = reconsol_dens_dict[density],
            ms = 6,
            marker = mar_dens_dict[density],
            markeredgewidth=1 , markeredgecolor='k',
            ls     = ls_dict['1'],
            label  = "$D_R$ = " + density + " PostShake = ON",
            legend = False)
    
for row,axes in enumerate(axs):
    for col, axis in enumerate(axes):  
        axis.set_xlabel("Maximum shear strain ($γ_{max}$) during undrained loading (%)")
        axis.set_ylabel("Volumetric strain due to post-cyclic reconsolidation, $ε_v$ (%)")
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.set_ylim(0,6)
        axis.set_xlim(0,10)
        text1 = "Drained Cyclic DSS, $σ'_{vc}$ = 100 kPa, α = 0, $K_o$ = 0.5\n"
        text1 = text1 + "followed by reconsolidation to $σ'_{vc}$"
          
        axis.text(0.05, 0.95, text1, transform=axis.transAxes, va = 'top',
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        
        axis.text(0.82, 0.74, "$D_R$ = 35%", color = 'firebrick', 
                  transform=axis.transAxes, va = 'top',
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        axis.text(0.82, 0.51, "$D_R$ = 55%", color = 'tomato', 
                  transform=axis.transAxes, va = 'top',
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        axis.text(0.82, 0.35, "$D_R$ = 75%", color = 'lightsalmon', 
                  transform=axis.transAxes, va = 'top',
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        axis.text(0.82, 0.05, "Post_Shake = 1", color = 'black', 
                  transform=axis.transAxes, va = 'top',
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))

plt.savefig("Fig4-21.png", dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()