#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 23:15:13 2022
@author: kziot

- with reference to the PM4Sand manual produces Figures 4.17 to 4.20
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
import scipy.optimize as sciopt

import glob
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
from   matplotlib.ticker     import (AutoMinorLocator, MultipleLocator)
from   decode_PM4SandDrivers import (decode_name, create_file_list)

plt.style.use('default')
plt.style.use('ucdavis.mplstyle')

search_string    = "./../PM4Sand_Cyclic_DSS_drained_batch/*.txt"
# The start location takes you to the beginning of the file string (goes past the folder)
start_loc        = 38
all_files  = glob.glob(search_string)

#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 
# Dictionaries for ... styling plots
# Colors for overburdens
color_dict = {'1': 'darkviolet', '2': 'blue', '3': 'green', '4': 'gold', '5': 'salmon',
               1:  'darkviolet',  2: 'blue',   3: 'green',   4: 'gold',   5: 'salmon'}

# Matches text of overburden to element number
element_dict = {'1': '25 kPa', '2': '100 kPa', '3': '400 kPa', '4': '1600 kPa', '5': '6400 kPa'}

# Assumes Row0 will be 100 kPa and Row1 will be 400kPa
row_stress_color_dict = {0:'blue',1:'green'}

# Matches density to plot location (options for strings and floats)
dens_dict        = {'35': 0, '55': 1, '75': 2, 35.0: 0, 55.0: 1, 75.0: 2}

# Dictionary to place densities in correct locations
# Element 2 (100kPa) will be placed in 1st row of 2x2 plot
# Element 3 (40kPa) in 2nd row
stress_dict   = {'2': 0, '3': 1}

# For adding string value depending on row or column (e.g. row 0 is 35%)
location_dens_dict = {0: 35, 1: 55, 2: 75}

#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 
#EPRI 1993 strains, G/Gmax, and damping for 0-20 feet and 120-250 feet
EPRI_0_6_m = np.array([[0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10],
                       [1,1,0.98, 0.92, 0.75, 0.52, 0.27, 0.12, 0.042, 0.019, 0.007],
                       [0.36, 0.40, 1.2, 2.1, 4.2, 7.6, 14.5, 22, 27, 30.3, 33.3]])
EPRI_36_76_m = np.array([[0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10],
                         [1,1,1,0.98, 0.9, 0.75, 0.5, 0.28, 0.12, 0.066, 0.037],
                         [0.2, 0.3, 0.65, 1.2, 2.3, 4.2, 8.2, 14, 21, 25.2, 28.8]])
#-----------------------------------------------------------------------------------------
# Inputs for create_file_list 

skip   = 1   # 1 implies skipping no rows - can increase if slow
ylimtop = {'35': 80, '55': 100, '75': 120} #axes limits
ylimbot = {'35': 250, '55': 300, '75': 400} #axes limits


for k,density in enumerate(['35', '55', '75']):
    # create_file_list receives all txt files in the folder, and filters those that are for MRD curves,
    # selects only outputs 2 and 3 (elements under 100 and 400 kPa respectively)
    # other entries are left empty (no filter applied)
    fig_files_left    = create_file_list(all_files,start_loc, [],['MRD'],[],[density],[],['2','3'])
    
    # selects only outputs _MRD.txt that are the FLAC post-processed for the MRD curves
    fig_files_right   = create_file_list(all_files,start_loc, [],['MRD'],[],[density],[],['MRD'])

       
    # Create empty plot 
    fig, axs = plt.subplots(nrows = 2, ncols = 2, figsize=(6.25,5), squeeze = False)
    
    # Add traces to corresponding plots
    filelist = fig_files_left
    for file in filelist:
        [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
        
        df = pd.read_table(file, header = 0, 
                    usecols = ['eps_xy(%)', 'tauxy'],
                    delim_whitespace=True, skiprows=lambda x: x > 3 and x % skip)
        
        df['tauxy'] = df['tauxy'].div(1000) # Pascal to kPa
        axs_row = stress_dict[output]
        if axs_row == 0:
            df.plot(ax=axs[axs_row,0], x = 'eps_xy(%)', y = 'tauxy',
                    xlim  = (-4,4), 
                    ylim  = (-ylimtop[density], ylimtop[density]),     
                    style = color_dict[output],
                    linewidth = 1, 
                    alpha  = 1,
                    legend = False)
        if axs_row == 1:
            df.plot(ax=axs[axs_row,0], x = 'eps_xy(%)', y = 'tauxy',
                    xlim  = (-4,4), 
                    ylim  = (-ylimbot[density], ylimbot[density]),     
                    style = color_dict[output],
                    linewidth = 1, 
                    alpha  = 1,
                    legend = False)
        
    filelist = fig_files_right
    for file in filelist:
        [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
        numCyc = int(extra[0][4:])   # number of cycles at each stress! required to avoid multiple points
        
        df = pd.read_table(file, header = 0, 
                            delim_whitespace=True, skiprows=lambda x: x % numCyc)
        
        columns = [['G/Gmax2', 'G/Gmax3','G/Gmax4'],['Damp2','Damp3','Damp4']]
        for r in range(2):
            axs[r,1].plot(EPRI_0_6_m[0],   EPRI_0_6_m[r+1],   ls = "--", c = 'black', marker = "None")
            axs[r,1].plot(EPRI_36_76_m[0], EPRI_36_76_m[r+1], ls = "--", c = 'black', marker = "None")
            
            for i,col in enumerate(columns[r]):
                df.plot(ax=axs[r,1], x = 'eps_xy', y = col,
                        xlim = (0.0001,10), logx = True,
                        marker = 'o',
                        style = color_dict[i+2], #element
                        linewidth = 1, 
                        alpha = 1,
                        legend = False)
        
    for row,axes in enumerate(axs):
        for col, axis in enumerate(axes):   
            axis.set_xlabel("Shear strain γ (%)")
            axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
            if col == 0:
                axis.xaxis.set_major_locator(MultipleLocator(2))
                axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
                axis.set_ylabel('Shear stress τ (kPa)')
                text1 = "$D_R$ = {:.0f}%\n".format(float(density))
                text1 = text1 + "σ$'_{vc}$ = " # finished below by row
                if row == 0:
                    text1 = text1 + "100 kPa"
                if row == 1:
                    text1 = text1 + "400 kPa" 
                # text1 = text1 + element_dict[output]                        
                axis.text(0.95, 0.05, text1,color=row_stress_color_dict[row], transform=axis.transAxes, ha = "right", 
                          bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
                
            if col == 1:
                if row == 0:
                    axis.set_ylabel('G / $G_{max}$')
                    axis.set_ylim(0,1.2)
                    text2 = "Dashed lines:\nEPRI (1993)\nfor depths of\n0-6m & 36-76m"
                    axis.annotate(text2, xy=(0.034, 0.52), xytext=(0.00015, 0.07), 
                                  arrowprops=dict(arrowstyle="->"),
                                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 0))
                if row == 1:
                    axis.yaxis.set_major_locator(MultipleLocator(20))
                    axis.set_ylabel('ξ (%)')
                    axis.set_ylim(-10,60)
                    text3 = "Solid lines:\nSimulations for\nσ$'_{vc}$ = 100, 400, & 1600 kPa"
                    axis.annotate(text3, xy=(0.3, 24), xytext=(0.00015, 44), 
                                  arrowprops=dict(arrowstyle="->"),
                                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 0))
    
    plt.subplots_adjust()
    list181920 = ['17','18','19']
    savefigname = "Fig4-" + list181920[k] + ".png"
    plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
    plt.show()
    plt.close()

#%%
#-----------------------------------------------------------------------------------------
# Function here keeps the _vol outputs (so DSS strain controlled drivers ran at the same strain for multiple
# cycles). Fifth entry can be left either empty to keep all files OR received two entries: one for the 
# Number of cycles applied and one for the strain at which the elements were exercised
# Element 2 is kept for 100 kPa (can be changed, colors and annotations will be updated)

fig_420_files = create_file_list(all_files,start_loc,[],['vol'],[],[],[['20'],['1']],['2'])

# Create empty plot 
fig, axs = plt.subplots(nrows = 1, ncols = 3, figsize=(8,4), squeeze = False)
    
for file in fig_420_files:
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    
    df = pd.read_table(file, header = 0, 
               usecols = ['eps_xy(%)', 'eps_yy(%)'],
               delim_whitespace=True, skiprows=lambda x: x > 3 and x % skip)
    
    axs_col = dens_dict[density]
    df.plot(ax=axs[0,axs_col], x = 'eps_xy(%)', y = 'eps_yy(%)',
            xlim = (-2,2), 
            ylim = (-0.5, 5),     
            style = color_dict[output],
            linewidth = 1, 
            alpha = 1,
            legend = False)
    axs[0,axs_col].scatter(x = [0], y = [0],
               color = "lightgrey",
               edgecolors = "dimgrey",
               s = 150,
               zorder = 3)
 
for row,axes in enumerate(axs):
    for col, axis in enumerate(axes):  
        axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.invert_yaxis()
        axis.set_xlabel("Shear strain γ (%)")
        axis.set_ylabel('Vertical strain, $ε_v$ (%)')
        text1 = "Drained Simple Shear\n"
        text1 = text1 + "$D_{Ro}$ = "
        text1 = text1 + "{:.0f}%, ".format(location_dens_dict[col])
        text1 = text1 + "σ$'_{vc}$ = " +  element_dict[output]
        axis.text(0.95, 0.05, text1, transform=axis.transAxes, ha = "right",
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
                
plt.subplots_adjust()
savefigname = "Fig4-20.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()



