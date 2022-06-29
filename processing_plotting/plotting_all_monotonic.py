#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 21:22:37 2022
@author: kziot

- with reference to the PM4Sand manual produces Figures 4.12 to 4.16
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
# import numpy  as np
import matplotlib.pyplot as plt
from   matplotlib.ticker     import (AutoMinorLocator, MultipleLocator)
from   decode_PM4SandDrivers import (decode_name, create_file_list)

plt.style.use('default')
plt.style.use('ucdavis.mplstyle')

search_string = "./../PM4Sand_Monotonic_batch/*.txt"
# The start location takes you to the beginning of the file string (goes past the folder)
start_loc     = 29
all_files     = glob.glob(search_string)

#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 
# Dictionaries for ... styling plots
# Colors for overburdens
color_dict = {'1': 'darkviolet', '2': 'blue', '3': 'green', '4': 'gold', '5': 'salmon',
               1:  'darkviolet',  2: 'blue',   3: 'green',   4: 'gold',   5: 'salmon'}

# Matches density to plot location (options for strings and floats)
dens_dict        = {'35': 0, '55': 1, '75': 2, 35.0: 0, 55.0: 1, 75.0: 2}


# For adding string value depending on row or column (e.g. row 0 is 35%)
location_dens_dict = {0: '35', 1: '55', 2: '75'}

fillstyle_dict = {'35': "full", '55': "right", '75': "none"}

#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 
#-----------------------------------------------------------------------------------------
# Each create_file_list function creates the list of files that:
# 1) entry 1: are DSS (instead of PSC)
# 2) entry 2: empty or could be 'mono' (they are all 'mono' so it doesn't matter)
# 3) entry 3: 'd' for drained or 'u' for undrained (if left empty it will keep both)
# 4) entry 4: density
# 5) entry 5: no extra variables for monotonics so left empty
# 6) empty 6: read all elements (all overburdens)
 
fig412_files_35 = create_file_list(all_files,start_loc, ['DSS'],[],['d'],['35'],[],['1','2','3','4','5'])
fig412_files_55 = create_file_list(all_files,start_loc, ['DSS'],[],['d'],['55'],[],['1','2','3','4','5'])
fig412_files_75 = create_file_list(all_files,start_loc, ['DSS'],[],['d'],['75'],[],['1','2','3','4','5'])

fig412_files_ar = [fig412_files_35, fig412_files_55, fig412_files_75]

skip = 1 #1 implies skipping no rows - can increase if slow

# Create empty plot 
fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize=(9,4.5))

# Add traces to corresponding plots
for filelist in fig412_files_ar:
    for file in filelist:
        [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
        df = pd.read_table(file,header = 0, 
                   usecols = ['eps_xy(%)', 'tauxy/sigvc', 'eps_yy(%)'],
                   dtype = 'float64',
                   delim_whitespace=True, 
                   skiprows=lambda x: x > 3 and x % skip)
        
        axs_col = dens_dict[density]
       
        df.plot(ax=axs[0,axs_col], x = 'eps_xy(%)', y = 'tauxy/sigvc',
                xlim = (0,10), ylim = (0,1.0), yticks = [0, 0.2, 0.4, 0.6, 0.8, 1.0] ,
                style = color_dict[output],
                linewidth = 1, 
                alpha = 1,
                legend = False)

        df.plot(ax=axs[1,axs_col], x = 'eps_xy(%)', y = 'eps_yy(%)', 
                    xlim = (0,10), ylim = (-4,4),
                    style = color_dict[output],
                    linewidth = 1, 
                    alpha = 1,
                    legend = False)
    
for row,axes in enumerate(axs):
    for col, axis in enumerate(axes):
        axis.set_xlabel('Shear strain γ (%)')
        if row == 0:
            axis.set_ylabel("Shear stress ratio, $τ/σ'_{vc}$")
            text1 = "$D_R$ = {}%\n".format(location_dens_dict[col])
            text1 = text1 + "σ$'_{vc}$ = 0.25, 1, 4, 16 & 64 atm"
            axis.text(0.95, 0.2, text1, transform=axis.transAxes, ha = 'right', va = 'top',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        if row == 1:
            axis.set_ylabel('Volumetric strain, $ε_v$ (%)')
            axis.invert_yaxis()
            text1 = "$D_R$ = {}%\n".format(location_dens_dict[col])
            text1 = text1 + "σ$'_{vc}$ = 0.25, 1, 4, 16 & 64 atm"
            axis.text(0.05, 0.05, text1, transform=axis.transAxes,
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        
        axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))

plt.subplots_adjust()
plt.savefig("Fig4-12.png", dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#%%
#-----------------------------------------------------------------------------------------
fig413_files_35 = create_file_list(all_files,start_loc, ['PSC'],[],['d'],['35'],[],['1','2','3','4','5'])
fig413_files_55 = create_file_list(all_files,start_loc, ['PSC'],[],['d'],['55'],[],['1','2','3','4','5'])
fig413_files_75 = create_file_list(all_files,start_loc, ['PSC'],[],['d'],['75'],[],['1','2','3','4','5'])

fig413_files_ar = [fig413_files_35, fig413_files_55, fig413_files_75]

skip = 1 #1 implies skipping no rows - can increase if slow

# Create empty plot 
fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize=(9,4.5))

# Add traces to corresponding plots
for filelist in fig413_files_ar:
    for file in filelist:
        [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
        df = pd.read_table(file,header = 0, 
                   usecols = ['e_vol(%)','eps_yy(%)','s1/s3'],
                   dtype = 'float64',
                   delim_whitespace=True, 
                   skiprows=lambda x: x > 3 and x % skip)
        
        axs_col = dens_dict[density]
       
        df.plot(ax=axs[0,axs_col], x = 'eps_yy(%)', y = 's1/s3',
                xlim = (0,10), ylim = (0,6.0), yticks = [0,1.0,2.0,3.0,4.0,5.0,6.0] ,
                style = color_dict[output],
                linewidth = 1, 
                alpha = 1,
                legend = False)

        df.plot(ax=axs[1,axs_col], x = 'eps_yy(%)', y = 'e_vol(%)', 
                    xlim = (0,10), ylim = (-4,5),
                    style = color_dict[output],
                    linewidth = 1, 
                    alpha = 1,
                    legend = False)
    
for row,axes in enumerate(axs):
    for col, axis in enumerate(axes):
        axis.set_xlabel('Axial strain $ε_{a}$ (%)')
        if row == 0:
            axis.set_ylabel("Principal stress ratio, $σ'_{1}/σ'_{3}$")
            text1 = "$D_R$ = {}%\n".format(location_dens_dict[col])
            text1 = text1 + "σ$'_{vc}$ = 0.25, 1, 4, 16 & 64 atm"
            axis.text(0.95, 0.2, text1, transform=axis.transAxes, ha = 'right', va = 'top',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        if row == 1:
            axis.set_ylabel('Volumetric strain, $ε_v$ (%)')
            axis.invert_yaxis()
            text1 = "$D_R$ = {}%\n".format(location_dens_dict[col])
            text1 = text1 + "σ$'_{vc}$ = 0.25, 1, 4, 16 & 64 atm"
            axis.text(0.03, 0.05, text1, transform=axis.transAxes,
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        
        axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))

plt.subplots_adjust()
plt.savefig("Fig4-13.png", dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()

#-----------------------------------------------------------------------------------------
# Create file lists
# 1) entry 1: are DSS (instead of PSC)
# 2) entry 2: empty or could be 'mono' (they are all 'mono' so it doesn't matter)
# 3) entry 3: 'd' for drained or 'u' for undrained (if left empty it will keep both)
# 4) entry 4: density
# 5) entry 5: no extra variables for monotonics so left empty
# 6) empty 6: read first four elements (overburdens 25,100,400,1600 kPa)

fig415_files_35 = create_file_list(all_files,start_loc, ['DSS'],[],['u'],['35'],[],['1','2','3','4'])
fig415_files_55 = create_file_list(all_files,start_loc, ['DSS'],[],['u'],['55'],[],['1','2','3','4'])
fig415_files_75 = create_file_list(all_files,start_loc, ['DSS'],[],['u'],['75'],[],['1','2','3','4'])

fig415_files_ar = [fig415_files_35, fig415_files_55, fig415_files_75]
skip = 1 #1 implies skipping no rows - can increase if slow

# Create empty plot 
fig, axs = plt.subplots(nrows = 3, ncols = 2, figsize=(6.25,6.25))
   
#add traces to corresponding plots
for filelist in fig415_files_ar:
    for file in filelist:
        [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
        
        df = pd.read_table(file, header = 0, 
                   usecols = ['eps_xy(%)', 'tauxy', 'sigv'],
                   dtype   = 'float64',
                   delim_whitespace=True, 
                   skiprows=lambda x: x > 3 and x % skip)
        
        df['tauxy'] = df['tauxy'].div(1000) #Pascal to kPa
        df['sigv']  = df['sigv'].div(1000) #Pascal to kPa
        axs_row     = dens_dict[density]
       
        df.plot(ax=axs[axs_row,0], x = 'eps_xy(%)', y = 'tauxy',
                xlim  = (0,10), ylim = (0,1500),
                style = color_dict[output],
                linewidth = 1, 
                alpha  = 1,
                legend = False)

        df.plot(ax=axs[axs_row,1], x = 'sigv', y = 'tauxy', 
                    xlim = (0,4000), ylim = (0,1500),
                    style = color_dict[output],
                    linewidth = 1, 
                    alpha = 1,
                    legend = False)

for row,axes in enumerate(axs):
    for col, axis in enumerate(axes):   
        axis.set_ylabel('Shear stress τ (kPa)')
        axis.ticklabel_format(style = 'sci', scilimits = (-100,100))
        if col == 0:
            axis.yaxis.set_major_locator(MultipleLocator(300))
            axis.set_xlabel("Shear strain γ (%)")
            text1 = "$D_R$ = {}%\n".format(location_dens_dict[row])
            text1 = text1 + "σ$'_{vc}$ = 0.25, 1, 4, & 16 atm"
            axis.text(0.05, 0.95, text1, transform=axis.transAxes, va = 'top',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
            axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))

        if col == 1:
            axis.yaxis.set_major_locator(MultipleLocator(300))
            axis.set_xlabel("Vertical Effective Stress, $σ'_v$")
            axis.xaxis.set_major_locator(MultipleLocator(1000))
            axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
            axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
            
plt.subplots_adjust()
plt.savefig("Fig4-15.png", dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#-------------------------------------------------------------------------------------------------
# Create file list
fig416_files_35 = create_file_list(all_files,start_loc, ['DSS'],[],['u'],['35'],[],['1','2','3','4'])
fig416_files_55 = create_file_list(all_files,start_loc, ['DSS'],[],['u'],['55'],[],['1','2','3','4'])
fig416_files_75 = create_file_list(all_files,start_loc, ['DSS'],[],['u'],['75'],[],['1','2','3','4'])


fig416_files_ar = [fig416_files_35, fig416_files_55, fig416_files_75]

skip = 1 #1 implies skipping no rows - can increase if slow

# Create empty plot 
fig, axs = plt.subplots(nrows = 3, ncols = 2, figsize=(6.25,6.25))
   
# Add traces to corresponding plots
for filelist in fig416_files_ar:
    for file in filelist:
        [driver, goal, water, density, extra, output] = decode_name(file,start_loc)

        df = pd.read_table(file, header = 0, 
                   usecols = ['eps_xy(%)', 'tauxy/sigvc', 'sigv/sigvc'],
                   delim_whitespace=True, 
                   skiprows=lambda x: x > 3 and x % skip)
        
        axs_row = dens_dict[density]
       
        df.plot(ax=axs[axs_row,0], x = 'eps_xy(%)', y = 'tauxy/sigvc',
                xlim = (0,10), ylim = (0,1.6),
                style = color_dict[output],
                linewidth = 1, 
                alpha = 1,
                legend = False)

        df.plot(ax=axs[axs_row,1], x = 'sigv/sigvc', y = 'tauxy/sigvc', 
                    xlim = (0,2), ylim = (0,1.6),
                    style = color_dict[output],
                    linewidth = 1, 
                    alpha = 1,
                    legend = False)

for row,axes in enumerate(axs):
    for col, axis in enumerate(axes): 
        axis.yaxis.set_major_locator(MultipleLocator(0.4))
        axis.set_ylabel("τ / $σ'_{vc}$")
        if col == 0:
            axis.set_xlabel("Shear strain γ (%)")
        if col == 1:
            axis.set_xlabel("$σ'_v$ / $σ'_{vc}$")
            text1 = "$D_R$ = {}%\n".format(location_dens_dict[row])
            text1 = text1 + "σ$'_{vc}$ = 0.25, 1, 4, & 16 atm"
            axis.text(0.05, 0.95, text1, transform=axis.transAxes, va = "top",
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
            axis.xaxis.set_major_locator(MultipleLocator(0.4))
        axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
        
plt.subplots_adjust()
plt.savefig("Fig4-16.png", dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#%%
#-----------------------------------------------------------------------------------------
# 1) entry 1: are DSS or PSC
# 2) entry 2: empty or could be 'mono' (they are all 'mono' so it doesn't matter)
# 3) entry 3: 'd' for drained
# 4) entry 4: empty so that it reads all densities
# 5) entry 5: no extra variables for monotonics so left empty
# 6) empty 6: read the summary peakPhi txt

fig414_bottom_plot = create_file_list(all_files,start_loc, ['DSS'],[],['d'],[],[],['peakPhi'])
fig414_top_plot    = create_file_list(all_files,start_loc, ['PSC'],[],['d'],[],[],['peakPhi'])

fig, axs = plt.subplots(nrows = 2, ncols = 1, figsize=(4.5,6.5))

# Create Bolton x-axis of mean effective stress
bolton_x_p = np.linspace(0.01,1000,num=1000)
Q = 10    # default property in PM4Sand driver
R = 1.5   # default property in PM4Sand driver

# Plane Strain Compression relationship for PSC plot
phicv = 33
bolton_y_35_PSC = 5*((0.35*(Q - np.log(bolton_x_p*100))) - R) + phicv
bolton_y_35_PSC[bolton_y_35_PSC < phicv] = phicv
bolton_y_55_PSC = 5*((0.55*(Q - np.log(bolton_x_p*100))) - R) + phicv
bolton_y_55_PSC[bolton_y_55_PSC < phicv] = phicv
bolton_y_75_PSC = 5*((0.75*(Q - np.log(bolton_x_p*100))) - R) + phicv
bolton_y_75_PSC[bolton_y_75_PSC < phicv] = phicv

# Plot
axs[0].plot(bolton_x_p, bolton_y_35_PSC, ls = "--", color = 'dimgrey')
axs[0].plot(bolton_x_p, bolton_y_55_PSC, ls = "--", color = 'grey')
axs[0].plot(bolton_x_p, bolton_y_75_PSC, ls = "--", color = 'darkgrey')

# DSS relationship for DSS plot
phicv = 28.6
bolton_y_35_DSS = 5*((0.35*(Q - np.log(bolton_x_p*100))) - R) + phicv
bolton_y_35_DSS[bolton_y_35_DSS < phicv] = phicv
bolton_y_55_DSS = 5*((0.55*(Q - np.log(bolton_x_p*100))) - R) + phicv
bolton_y_55_DSS[bolton_y_55_DSS < phicv] = phicv
bolton_y_75_DSS = 5*((0.75*(Q - np.log(bolton_x_p*100))) - R) + phicv
bolton_y_75_DSS[bolton_y_75_DSS < phicv] = phicv

# Plot
axs[1].plot(bolton_x_p, bolton_y_35_DSS, ls = ":", color = 'dimgrey')
axs[1].plot(bolton_x_p, bolton_y_55_DSS, ls = ":", color = 'grey')
axs[1].plot(bolton_x_p, bolton_y_75_DSS, ls = ":", color = 'darkgrey')

# Plot data points from PM4Sand Drivers

for file in fig414_top_plot:
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    df = pd.read_table(file, header = 0, delim_whitespace=True)

    df.loc[df['peakPhi'] < 33.0, 'peakPhi'] = 33.0
    df['sig1']  = df['sigvc'] *(np.tan((df['peakPhi']/2 + 45.0)*np.pi/180))**2
    df['p_eff'] = (df['sig1'] + df['sigvc'])/2.0  
        
    df.plot(ax=axs[0], x = 'p_eff', y = 'peakPhi',
            xlim = (0.1,100), ylim = (20,50), ls = "-",
            marker = 's', 
            markersize = 50/10, 
            color = 'black',
            fillstyle = fillstyle_dict[density],
            alpha = 1,
            legend = False)

    
for file in fig414_bottom_plot:
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    df = pd.read_table(file, header = 0, delim_whitespace=True)

    #------------------------------------------------------------------
    # If peakPhi are less than 28.6, change to 28.6
    # Could have used Pandas Masking function too
    # df[‘column_name’].mask( df[‘column_name’] == ‘some_value’, value, inplace=True)
    df.loc[df['peakPhi'] < 28.6, 'peakPhi'] = 28.6
    
    df.plot(ax=axs[1], x = 'sigvc', y = 'peakPhi',
            xlim = (0.1,100), ylim = (20,50), ls = "-",
            marker = 'o', 
            markersize = 50/10, 
            color = 'black',
            fillstyle = fillstyle_dict[density],
            alpha = 1,
            legend = False)
    #------------------------------------------------------------------

for row, axis in enumerate(axs):  
    axis.set_xscale('log')

    if row == 0:
        axis.set_ylabel("Φ' = 2[$tan^{-1}((σ'_1/σ'_3)^{0.5}$) - 45°]")
        axis.set_xlabel("Mean effective stress p' (atm)")
        text1 = "Plane Strain Compression\n  $Φ'_{cv}$= 33°, $K_o$ = 1.0"
        axis.text(0.95, 0.95, text1, transform=axis.transAxes, va = 'top', ha = 'right',
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        
        axis.text(0.3, 0.90, "$D_R$ = 75%", transform=axis.transAxes,
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        axis.text(0.025, 0.85, "$D_R$ = 55%", transform=axis.transAxes,
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        axis.text(0.025, 0.52, "$D_R$ = 35%", transform=axis.transAxes,
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        
        text1 = "Bolton's Relationship (PSC)\n   $Φ'_{cv}$= 5$I_R$"
        axis.annotate(text1, xy=(1.3, 34.5), xytext=(0.25, 26.5),
                              arrowprops=dict(arrowstyle="->", lw = 0.95),
                              bbox=dict(pad=0, facecolor="white", edgecolor="none"))
        axis.annotate("", xy=(1.7, 37), xytext=(1.3, 34),
                  arrowprops=dict(arrowstyle="->", color = "grey"),
                  bbox=dict(pad=-3, facecolor="none", edgecolor="none"))
        axis.annotate("", xy=(2.2, 39.1), xytext=(1.62, 36.6),
                  arrowprops=dict(arrowstyle="->", color = "darkgrey"),
                  bbox=dict(pad=-3, facecolor="none", edgecolor="none"))
        
    # Direct Simple Shear plot labels
    if row == 1:
        axis.set_ylabel("Φ' = $tan^{-1}(τ'_h/σ'_v$)")
        axis.set_xlabel("Vertical effective stress (atm)")
        text1 = "Direct Simple Shear\n$Φ'_{cv}$= 33°, $K_o$ = 0.5"
        axis.text(0.95, 0.95, text1, transform=axis.transAxes, va = 'top', ha = 'right',
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        
        axis.text(0.025, 0.85,  "$D_R$ = 75%", transform=axis.transAxes,
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        axis.text(0.025, 0.70, "$D_R$ = 55%", transform=axis.transAxes,
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
        axis.text(0.025, 0.47,  "$D_R$ = 35%", transform=axis.transAxes,
                  bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
       
        text2 = "arctan(sin($Φ'_{cv,DSS}$)) = 28.6°"
        axis.annotate(text2, xy=(7, 28.6), xytext=(5, 23.5),
                              arrowprops=dict(arrowstyle="->"),
                              bbox=dict(pad=-1, facecolor="white", edgecolor="none"))
        
        text1 = "Bolton's Relationship (PSC)\n   $Φ'_{cv}$= 5$I_R$"
        axis.annotate(text1, xy=(1.4, 30.3), xytext=(0.18, 21.5),
                              arrowprops=dict(arrowstyle="->", lw = 0.95),
                              bbox=dict(pad=0, facecolor="white", edgecolor="none"))
        
    axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))

axs[0].axhline(y = 33, lw = 1)
axs[1].axhline(y = 28.6, lw = 1)    
plt.subplots_adjust()
plt.savefig("Fig4-14.png", dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()