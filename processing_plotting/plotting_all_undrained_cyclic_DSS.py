#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 23:15:13 2022

@author: kziot

- with reference to the PM4Sand manual produces Figures 4.2 to 4.11
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
import numpy  as np
import matplotlib.pyplot as plt
from   matplotlib.ticker     import (AutoMinorLocator, MultipleLocator)
from   decode_PM4SandDrivers import (power_fit, decode_name, create_file_list)

plt.style.use('default')
plt.style.use('ucdavis.mplstyle')

search_string = "./../PM4Sand_Cyclic_DSS_undrained_batch/*.txt"
# The start location takes you to the beginning of the file string (goes past the folder/)
start_loc     = 40
all_files     = glob.glob(search_string)

#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 
# Dictionaries for ... styling plots

# For annotations
label_dict       = {35 : '$D_R$ = 35%', 55 : '$D_R$ = 55%',  75 : '$D_R$ = 75%',
                   '35': '$D_R$ = 35%','55': '$D_R$ = 55%', '75': '$D_R$ = 75%'}

# For adding string value depending on row or column (e.g. row 0 is 35%)
location_dens_dict = {0: '35', 1: '55', 2: '75'}

# For matching row of plot to liq criterion used (and add string accordingly)
row_liq_dict     = {0:'98% $r_u$', 1: '1% shear strain', 2: '3% shear strain'}

# Matches density to plot location (options for strings and floats)
dens_dict        = {'35': 0, '55': 1, '75': 2, 35.0: 0, 55.0: 1, 75.0: 2}

# Colors for densities
col_dens_dict    = {35: 'silver', 55: 'darkgrey', 75: 'dimgrey'}

# Markers for different densities (circles for 35% etc.)
mar_dens_dict    =  {'35': 'o', '55': 's', '75': '^', 35.0: 'o', 55.0: 's', 75.0: '^'}

# Color for overburdens in CSR-N plots
color_sigvc_dict = {'1': 'blue', '4': 'green', '8': 'yellowgreen', '16': 'gold'}

# Marker style for overburdens
mar_sigvc_dict   = {'1': 'o', '4': 'd', '8': '^', '16': '*'}

# Fill style for markers in Kalpha plots
fill_sigvc_dict  = {1: "full", 4: "left"}

# Matches alpha value to plot location
alpha_dict       = {'0.0': 0, '0.1': 1, '0.2': 2}

# Colors for alpha values in CSR-N plots
color_alpha_dict = {'0.1': 'goldenrod', '0.2': 'darkorange', '0.3': 'firebrick', '0.0': 'saddlebrown'}

# Markers for different alpha values (circles for 35% etc.)
mar_alpha_dict   = {'0.0': 'o', '0.1': '^', '0.2': 's', '0.3': 'd'}

# Color for Ko’s in CSR-N plots
color_Ko_dict    = {'1.2': 'teal', '0.3': 'mediumvioletred', '0.5': 'darkviolet', '0.8': 'royalblue'}

# Marker style for Ko’s 
mar_Ko_dict      = {'0.3': 'o', '0.5': '^', '0.8': 's', '1.2': 'd'}
#== ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** == ** 
# create_file_list(fileList,start_loc, driverType = [], testType  = [], drainType = [], 
                                     # density    = [], extraInfo = [], output    = [])

# 1) entry 1: empty (they are all DSS anyways - nothing to filter)
# 2) entry 2: empty (they are all cyc anyways - nothing to filter))
# 3) entry 3: empty (they are all undrained anyways - nothing to filter))
# 4) entry 4: density string value
# 5) entry 5  has three parts: Part 1 = overburdens, Part 2 = alphas, Part 3 = Ko
# 6) empty 6: read element 3 that is exercised under the CRR

Fig42_files = create_file_list(all_files,start_loc, [],[],[],['35'],[['1'],['0.0','0.1','0.2'],['0.5']],['3'])
Fig43_files = create_file_list(all_files,start_loc, [],[],[],['55'],[['1'],['0.0','0.1','0.2'],['0.5']],['3'])
Fig44_files = create_file_list(all_files,start_loc, [],[],[],['75'],[['1'],['0.0','0.1','0.2'],['0.5']],['3'])

skip = 1  # 1 implies skipping no rows - can increase if slow

filelist_ar = [Fig42_files, Fig43_files, Fig44_files]

for fileind, filelist in enumerate(filelist_ar):
    fig, axs = plt.subplots(nrows = 3, ncols = 2, figsize=(6.25,6.25))
    for ind, file in enumerate(filelist):
        [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
        sigvc = extra[0][3:]
        alpha = extra[1][1:]
        Ko    = extra[2][2:]
        
        df = pd.read_table(file, header = 0, 
                     usecols = ['shear_strain', 'CSR', 'sigv/sigvc'],
                     delim_whitespace=True, skiprows=lambda x: x > 3 and x % skip)
    
        axs_row = alpha_dict[alpha]
        
        df.plot(ax=axs[axs_row,0], x = 'shear_strain', y = 'CSR',
                xlim = (-2,10), color = "black",
                linewidth = 1, 
                alpha = 1,
                legend = False)
    
        df.plot(ax=axs[axs_row,1], x = 'sigv/sigvc', y = 'CSR', 
                xlim = (0,1), color = "black",
                linewidth = 1, 
                alpha = 1,
                legend = False)
        
        for row,axes in enumerate(axs):
            for col, axis in enumerate(axes): 
                axis.set_ylabel("Shear stress ratio, τ / $σ'_{vc}$")
                axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
                axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))                
                if col == 0:
                    axis.set_xlabel("Shear strain γ (%)")
                    text1 = "α = τ / $σ'_{vc}$ = 0." + str(row) #row: 0,1,2
                    axis.text(0.95, 0.05, text1, transform=axis.transAxes, ha = 'right',
                              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
                    text2 = "$D_R$ = {}%\n".format(density)
                    text2 = text2 + "$σ'_{vc}$ = 100 kPa"
                    axis.text(0.05, 0.05, text2, transform=axis.transAxes,
                              bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
                if col == 1:
                    axis.set_xlabel("Vertical Effective Stress, $σ'_v$/$σ'_{vc}$")
                
                if col == 0 and row == 0:
                    axis.set_xlim(-6,6)
                
                if int(density) == 75:
                    axis.set_ylim(-0.6, 0.6)
                else:
                    axis.set_ylim(-0.4, 0.4)

    plt.subplots_adjust()
    list234 = ['2', '3', '4']
    savefigname = "Fig4-" + list234[fileind] + ".png"
    plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
    plt.show()
    plt.close()
#%%
#-----------------------------------------------------------------------------------------
# 1) entry 1: empty (they are all DSS anyways - nothing to filter)
# 2) entry 2: empty (they are all cyc anyways - nothing to filter))
# 3) entry 3: empty (they are all undrained anyways - nothing to filter))
# 4) entry 4: empty so that it reads all densities
# 5) entry 5  has three parts: Part 1 = overburdens, Part 2 = alphas, Part 3 = Ko
# 6) empty 6: read element 3 that is exercised under the CRR

Fig45_files = create_file_list(all_files,start_loc, [],[],[],[],[['1'],['0.0'],['0.5']],['3'])

skip = 1
fig, axs = plt.subplots(nrows = 3, ncols = 1, figsize=(4,7.5), squeeze = False)
for ind, file in enumerate(Fig45_files):
    cycNum = 0
    
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    sigvc = extra[0][3:]
    alpha = extra[1][1:]
    Ko    = extra[2][2:]
        
    df = pd.read_table(file, header = 0, 
                usecols = ['shear_strain', 'CSR','Ncyc'],
                delim_whitespace=True, skiprows=lambda x: x > 3 and x % skip)

    cycNumStop = df[abs(df['shear_strain']) >= 2.0]['Ncyc'].values[0]
    
    df[df['Ncyc'] <= cycNumStop].plot(ax=axs[dens_dict[density],0], 
            x = 'shear_strain', y = 'CSR',
            xlim = (-2,2), color = "black",
            linewidth = 1, alpha = 1, legend = False)
    
    for row,axes in enumerate(axs):
        for col, axis in enumerate(axes): 
            axis.set_ylabel("Shear stress ratio, τ / $σ'_{vc}$")
            axis.set_xlabel("Shear strain γ (%)")
            text2 = "$D_R$ = {}%\n".format(location_dens_dict[row])
            text2 = text2 + "$σ'_{vc}$ = 100 kPa"
            axis.text(0.05, 0.95, text2, transform=axis.transAxes, va = 'top',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
            axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
            axis.yaxis.set_major_locator(plt.MaxNLocator(4))
            axis.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
            ylim = 0.1*2**row
            axis.set_ylim(-ylim, ylim)
            
savefigname = "Fig4-5.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()

#-----------------------------------------------------------------------------------------
# 1) entry 1: empty (they are all DSS anyways - nothing to filter)
# 2) entry 2: empty (they are all cyc anyways - nothing to filter))
# 3) entry 3: empty (they are all undrained anyways - nothing to filter))
# 4) entry 4: empty so that it reads all densities
# 5) entry 5  has three parts: Part 1 = overburdens, Part 2 = alphas, Part 3 = Ko
# 6) empty 6: read the summary csrN.txt from FLAC that carries the liquefaction triggering information

Fig46_files = create_file_list(all_files,start_loc, [],[],[],[],[['1'],['0.0'],['0.5']],['csrN'])

fig, axs = plt.subplots(nrows = 3, ncols = 1, figsize=(4,7.5), squeeze = False)

for ind, file in enumerate(Fig46_files):
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    
    df = pd.read_table(file, header = 0, delim_whitespace=True)
    
    ##need to get fits from points: CSR versus cycNum
    pts = 100    
    if len(df[df['N_to_98%_ru']>0]) >= 3:  # need at least three points to fit properly
        [ind_1p, amp_1p, s1p_x, s1p_y] = power_fit(df,'N_to_98%_ru','CSR',pts)
        axs[0,0].plot(s1p_x, s1p_y, color = 'grey', ls = "--")
        axs[0,0].text(0.99*s1p_x[int(pts*0.05)], 1.15*s1p_y[int(pts*0.05)], "b = {:.2f}".format(-ind_1p),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
    
    df.plot(ax=axs[0,0], x = 'N_to_98%_ru', y = 'CSR',
            linestyle = "None", color = 'black',
            marker = mar_dens_dict[density],
            ms = 4* 1,
            alpha = 1,
            label = "$D_R$ = " + density + "%")
    #axs[1,0].text(0.8, 0.025+round(df['CSR'].max(),2), "$D_R$ =" + density + "%")
#-------------------------------------------------------------------- 
    if len(df[df['N_to_1%_strain']>0]) >= 3: #need at least three points to fit properly
        [ind_3p, amp_3p, s3p_x, s3p_y] = power_fit(df,'N_to_1%_strain','CSR',pts) 
        axs[1,0].plot(s3p_x, s3p_y, color = 'grey', ls = "--")
        axs[1,0].text(s3p_x[int(pts*0.05)], 1.15*s3p_y[int(pts*0.05)], "b = {:.2f}".format(-ind_3p),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
    
    df.plot(ax=axs[1,0], x = 'N_to_1%_strain', y = 'CSR',
            linestyle = "None", color = 'black',
            marker = mar_dens_dict[density],
            ms = 4* 1, alpha = 1,
            label = "$D_R$ = " + density + "%")
#-------------------------------------------------------------------- 
    if len(df[df['N_to_3%_strain']>0]) >= 3: #need at least three points to fit properly
        [ind_ru, amp_ru, ru_x, ru_y] = power_fit(df,'N_to_3%_strain','CSR',pts)
        axs[2,0].plot(ru_x, ru_y, color = 'grey', ls = "--")
        axs[2,0].text(ru_x[int(pts*0.05)], 1.15*ru_y[int(pts*0.05)], "b = {:.2f}".format(-ind_ru),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))

    df.plot(ax=axs[2,0], x = 'N_to_3%_strain', y = 'CSR',
            linestyle = "None", color = 'black',
            marker = mar_dens_dict[density],
            ms = 4 * 1,
            alpha = 1,
            label = "$D_R$ = " + density + "%")
#-------------------------------------------------------------------- 
for row,axes in enumerate(axs):
    for col, axis in enumerate(axes): 
        axis.set_ylabel("Cyclic Stress Ratio")
        axis.set_xlabel("Number of uniform cycles")
        axis.set_xlim(1,100);  axis.set_ylim(0, 0.6)
        axis.set_xscale('log')
        axis.legend(loc = "upper left")
        text2 = "$σ'_{vc}$ = 100 kPa\n"
        text2 = text2 + "{}".format(row_liq_dict[row])
        axis.text(0.95, 0.95, text2, transform=axis.transAxes, va = "top", ha = "right",
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        axis.yaxis.set_major_locator(MultipleLocator(.2))
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.grid(which = "minor", axis = "x", lw = 0.2)


plt.subplots_adjust()
savefigname = "Fig4-6.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#%%
#-----------------------------------------------------------------------------------------
# Entry 5  has three parts: Part 1 = overburdens - get them all for Ksigma 
#                           Part 2 = alphas - only keep level ground
#                           Part 3 = Ko - only keep 0.5

Fig47_files = create_file_list(all_files,start_loc, [],[],[],[],[[],['0.0'],['0.5']],['csrN'])

fig, axs = plt.subplots(nrows = 3, ncols = 1, figsize=(4,7.5), squeeze = False)

for ind, file in enumerate(Fig47_files):
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    sigvc = extra[0][3:]
    alpha = extra[1][1:]
    Ko    = extra[2][2:]
    
    df = pd.read_table(file, header = 0, delim_whitespace=True)
    sigvc_str = "$σ'_{vc}$ = "
    # Row based on density of file
    df[df["N_to_3%_strain"] > 0].plot(ax=axs[dens_dict[density],0], x = 'N_to_3%_strain', y = 'CSR',
            color  = color_sigvc_dict[sigvc],
            marker = mar_sigvc_dict[sigvc],
            ms    = 5* 1,
            alpha = 1,
            linewidth = 1, 
            label = sigvc_str +  "{:.0f} atm".format(float(sigvc)))

for row,axes in enumerate(axs):
    for col, axis in enumerate(axes): 
        axis.set_ylabel("Cyclic Stress Ratio to γ = 3%")
        axis.set_xlabel("Number of uniform cycles")
        axis.set_xlim(1,100)
        axis.set_ylim(0, 0.6)
        axis.set_xscale('log')
        axis.legend(loc = "upper left")
        if row == 2:
            axis.legend(loc = "lower left")

        text2 = "$D_R$ = {}%\n".format(location_dens_dict[row])
        text2 = text2 + "3% shear strain\n"
        text2 = text2 + "α = 0.0"
        axis.text(0.95, 0.95, text2, transform=axis.transAxes, va = 'top', ha = 'right',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        axis.yaxis.set_major_locator(MultipleLocator(.2))
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.grid(which = "minor", axis = "x", lw = 0.2)

plt.subplots_adjust()
savefigname = "Fig4-7.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#%%
#-----------------------------------------------------------------------------------------
forKsigma_Fig48 = create_file_list(all_files,start_loc, [],[],[],[],[[],['0.0'],['0.5']],['csrN'])

numFiles = len(forKsigma_Fig48)
if numFiles != 9:
    print("Error in creating K_sigma figure. Too many or not enough files found to represent all points.")
    print("numFiles = {}".format(numFiles))
    
df_summary = np.zeros([3,12])
CSR1atm    = np.zeros(3)

fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize=(4,4))

for ind, file in enumerate(forKsigma_Fig48):
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    sigvc   = float(extra[0][3:])
    density = float(density)
    df      = pd.read_table(file, header = 0, delim_whitespace=True)
    
    if len(df[df['N_to_3%_strain']>0]) >= 3: # need at least three points to fit properly
        [ind_ru, amp_ru, ru_x, ru_y] = power_fit(df,'N_to_3%_strain','CSR',10)
        CSR_15cyc = amp_ru*15**ind_ru
        # Enter information in df_summary array
        df_summary[0,ind] = sigvc
        df_summary[1,ind] = density
        df_summary[2,ind] = CSR_15cyc
        if sigvc == 1.0:
            CSR1atm[dens_dict[density]] = CSR_15cyc
   
    else: # Not enough points to fit line.
        print(file)
        print("File did not have enough points to determine a CSR. Should be rerun. CSR set = 1 to allow plot to go without errors.")
        CSR_15cyc = 1
        df_summary[:,ind] = [extra[0][3:], density, CSR_15cyc]
        if sigvo == 1.0:
            CSR1atm[dens_dict[density]] = CSR_15cyc

# Calculate and plot K_sigmas  
for ind in range(numFiles):
    sig    = df_summary[0,ind]
    den    = df_summary[1,ind]
    Ksigma = df_summary[2,ind] / CSR1atm[dens_dict[den]]
    # print(Ksigma)
    # print(den)
    # print(sig)
    # print(df_summary[2,ind])
    axs.plot(sig,Ksigma, 
            label = label_dict[den], 
            marker =  mar_dens_dict[den], 
            markersize = 6, 
            color = 'black',
            linestyle = "none")

# Create legend
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
axs.legend(by_label.values(), by_label.keys(), 
            loc = "lower left", title = "Model Simulations")

# =====================================================================#
# Plot Idriss and Boulanger relationships for comparison               #
# =====================================================================#
bi2008_x = np.linspace(0.0001,20,num=1000)
Csig_35  = min(0.3, 1/(18.9-17.3*0.35))
Csig_55  = min(0.3, 1/(18.9-17.3*0.55))
Csig_75  = min(0.3, 1/(18.9-17.3*0.75))
bi2008_y_35 = 1 - Csig_35*np.log(bi2008_x)
bi2008_y_55 = 1 - Csig_55*np.log(bi2008_x)
bi2008_y_75 = 1 - Csig_75*np.log(bi2008_x)
bi2008_y_35[bi2008_y_35>1.1] = 1.1
bi2008_y_55[bi2008_y_55>1.1] = 1.1
bi2008_y_75[bi2008_y_75>1.1] = 1.1

axs.plot(bi2008_x, bi2008_y_35, color = "darkgrey", zorder = 1)
axs.plot(bi2008_x, bi2008_y_55, color = "grey", zorder = 1)
axs.plot(bi2008_x, bi2008_y_75, color = "dimgrey", zorder = 1)

text = "Relationships recommended by\nBoulanger & Idriss (2004):"
axs.annotate(text, c = "dimgrey", xy=(5.8, 0.86), xytext=(1.8, 1.1), 
                                  arrowprops=dict(arrowstyle="->", color = "dimgrey"),
                                  bbox=dict(facecolor="white", edgecolor="none", pad = 1))
axs.annotate("35%", c = "darkgrey", xy=(8.7, 0.833),
                                  bbox=dict(facecolor="white", edgecolor="none", pad = 1))
axs.annotate("55%", c = "grey", xy=(8.7, 0.755),
                                  bbox=dict(facecolor="white", edgecolor="none", pad = 1))
axs.annotate("75%", c = "dimgrey", xy=(8.7, 0.62),
                                  bbox=dict(facecolor="white", edgecolor="none", pad = 1))
# =====================================================================#
# Finish plot details
axs.set_ylabel("$K_σ$")
axs.set_xlabel("Vertical effective stress, $σ'_{vc}$/$P_{atm}$")

axs.set_xlim(0,10)
axs.set_ylim(0, 1.4)
axs.yaxis.set_major_locator(MultipleLocator(.2))
axs.xaxis.set_minor_locator(AutoMinorLocator(n = 2))
axs.yaxis.set_minor_locator(AutoMinorLocator(n = 1))

axs.grid(which = "minor", axis = "x", lw = 0.2)
       
plt.subplots_adjust()
savefigname = "Fig4-8.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#-----------------------------------------------------------------------------------------
Fig49_files = create_file_list(all_files,start_loc, [],[],[],[],[['1'],['0.0','0.1','0.2','0.3'],['0.5']],['csrN'])

fig, axs = plt.subplots(nrows = 3, ncols = 1, figsize=(4,7.5), squeeze = False)

for ind, file in enumerate(Fig49_files):
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    sigvc = extra[0][3:]
    alpha = extra[1][1:]
    Ko    = extra[2][2:]
    
    df = pd.read_table(file, header = 0, delim_whitespace=True)

    # Row based on density of file, plot only portion of dataframe here cycNum > 0
    df[df["N_to_3%_strain"] > 0].plot(ax=axs[dens_dict[density],0], x = 'N_to_3%_strain', y = 'CSR',
            color = color_alpha_dict[alpha], 
            label  = "α = {:.1f}".format(float(extra[1][1:])),
            marker = mar_alpha_dict[alpha],
            mfc    = color_alpha_dict[alpha],
            mec    = color_alpha_dict[alpha],
            markersize = 5 * 1,
            linewidth = 1, alpha = 1)

handles, labels = axs[0,0].get_legend_handles_labels()
handles = [handles[-1]] + handles[0:-1]
for row,axes in enumerate(axs):
    for col, axis in enumerate(axes): 
        axis.set_ylabel("Cyclic Stress Ratio to γ = 3%")
        axis.set_xlabel("Number of uniform cycles")
        axis.set_xlim(1,100)
        axis.set_ylim(0, 0.6)
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
        axis.yaxis.set_major_locator(MultipleLocator(.2))
        axis.set_xscale('log')
        text2 = "$D_R$ = {}%\n".format(location_dens_dict[row])
        text2 = text2 + "$σ'_{vc}$ = 100 kPa"
        axis.text(0.95, 0.95, text2, transform=axis.transAxes, va = 'top', ha = 'right',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        axis.legend(handles = handles, loc = "upper left")
        axis.grid(which = "minor", axis = "x", lw = 0.2)

plt.subplots_adjust()
savefigname = "Fig4-9.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#%%
#--------------------------------------------------------------------
forKalpha_Fig410 = create_file_list(all_files,start_loc, [],[],[],[],[['1','4'],[],['0.5']],['csrN'])

numFiles = len(forKalpha_Fig410)

if numFiles != 24:
    print("Number of files incorrect. Check filters. {}".format(numFiles))
    
df_summary = pd.DataFrame(np.zeros([24,6]), columns=['dens', 'sig', 'alpha', 'csr_98','csr_1p','csr_3p'])

fig, axs = plt.subplots(nrows = 1, ncols = 1, figsize=(4,4))

for ind, file in enumerate(forKalpha_Fig410):
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    df  = pd.read_table(file, header = 0, delim_whitespace=True)
    sig = extra[0][3:]
    alf = extra[1][1:]
    
    if len(df[df['N_to_3%_strain']>0]) >= 3: #need at least three points to fit properly
        [ind_ru, amp_ru, ru_x, ru_y] = power_fit(df,'N_to_3%_strain','CSR',10)
        CSR_15cyc = min(15, amp_ru*15**ind_ru)
        
        df_summary['dens'][ind]   = int(density)
        df_summary['sig'][ind]    = int(sig)
        df_summary['alpha'][ind]  = float(alf)
        df_summary['csr_3p'][ind] = CSR_15cyc
    else:
        print("Not enough points in file to create fit. CSR = 0 automatically. {}".format(file))
        df_summary['dens'][ind]   = int(density)
        df_summary['sig'][ind]    = int(sig)
        df_summary['alpha'][ind]  = float(alf)
        df_summary['csr_3p'][ind] = 0
        
df_summary.sort_values(by=['alpha'], inplace = True)

for d in [35,55,75]:
    for s in [1,4]:
        plot_df = df_summary[(df_summary['dens']==d) & (df_summary['sig']==s)]
        plot_df.plot(ax = axs,
                    x = 'alpha', y = 'csr_3p',
                    fillstyle  = fill_sigvc_dict[s],
                    marker     = mar_dens_dict[d],
                    markersize = 6,
                    # color = col_dens_dict[d],
                    color = color_sigvc_dict[str(s)],
                    linestyle = "-",
                    legend = False)


axs.annotate("$D_R$ = 35%", c = "black", xy=(0.02, 0.05),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.annotate("$D_R$ = 55%", c = "black", xy=(0.02, 0.18),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.annotate("$D_R$ = 75%", c = "black", xy=(0.02, 0.34),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))

axs.annotate("$σ'_{vc}$ = 1 atm", c = "blue", xy=(0.31, 0.06),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.annotate("$σ'_{vc}$ = 4 atm", c = "green", xy=(0.31, 0.02),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.annotate("$σ'_{vc}$ = 1 atm", c = "blue", xy=(0.31, 0.16),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.annotate("$σ'_{vc}$ = 4 atm", c = "green", xy=(0.31, 0.10),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.annotate("$σ'_{vc}$ = 1 atm", c = "blue", xy=(0.31, 0.38),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.annotate("$σ'_{vc}$ = 4 atm", c = "green", xy=(0.31, 0.25),
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 1))
axs.set_ylabel("Cyclic Stress Ratio to γ = 3% at 15 cycles")
axs.set_xlabel("Static shear stress ratio, α =$τ_{static}$/$σ'_{vc}$")

axs.set_xlim(0, 0.4)
axs.set_ylim(0, 0.5)
axs.xaxis.set_major_locator(MultipleLocator(.1))
axs.yaxis.set_minor_locator(AutoMinorLocator(n = 2))
axs.xaxis.set_minor_locator(AutoMinorLocator(n = 2))

plt.subplots_adjust()
savefigname = "Fig4-10.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
#%%
#-----------------------------------------------------------------------------------------
Fig411_files = create_file_list(all_files,start_loc, [],[],[],[],[['1'],['0.0'],['0.3','0.5','0.8','1.2']],['csrN'])

fig, axs = plt.subplots(nrows = 3, ncols = 1, figsize=(4,7.5), squeeze = False)

for ind, file in enumerate(Fig411_files):
    [driver, goal, water, density, extra, output] = decode_name(file,start_loc)
    Ko = extra[2][2:]
    
    df = pd.read_table(file, header = 0, delim_whitespace=True)
    df[df["N_to_3%_strain"] > 0].plot(ax=axs[dens_dict[density],0], 
                                    x = 'N_to_3%_strain', y = 'CSR', 
                                    color = color_Ko_dict[Ko],
                                    marker = mar_Ko_dict[Ko],
                                    ms = 5* 1,
                                    linewidth = 1, 
                                    alpha = 1,
                                    label = "$K_o$ = {:.1f}".format(float(Ko)))
    
for row,axes in enumerate(axs):
    for col, axis in enumerate(axes): 
        axis.set_ylabel("Cyclic Stress Ratio to γ = 3%")
        axis.set_xlabel("Number of uniform cycles")
        axis.set_xlim(1,100)
        axis.set_ylim(0, 0.6)
        axis.set_xscale('log')
        text2 = "$D_R$ = {}%\n".format(location_dens_dict[row])
        text2 = text2 + "$σ'_{vc}$ = 100 kPa\n"
        text2 = text2 + "α = 0.0"
        axis.text(0.95, 0.95, text2, transform=axis.transAxes, va = 'top', ha = 'right',
                      bbox=dict(facecolor='white', edgecolor='none', alpha=1, pad = 2))
        axis.legend(loc = "upper left")
        axis.grid(which = "minor", axis = "x", lw = 0.2)
        axis.yaxis.set_major_locator(MultipleLocator(.2))
        axis.yaxis.set_minor_locator(AutoMinorLocator(n = 2))

plt.subplots_adjust()
savefigname = "Fig4-11.png"
plt.savefig(savefigname, dpi = 600, bbox_inches = 'tight')
plt.show()
plt.close()
