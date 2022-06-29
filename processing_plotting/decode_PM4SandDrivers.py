# -*- coding: utf-8 -*-
import numpy as np
import scipy.optimize as sciopt

#------------------------------------------------------------
def power_fit(df, df_x_name, df_y_name, pts):
    df_nonzero = df[df[df_x_name]>0]
    #create x values from minimum to maximum numCycles in dataframe
    x    = np.linspace(df_nonzero[df_x_name].min(), df_nonzero[df_x_name].max(), pts)
    logx = np.log10(df_nonzero[df_x_name])
    logy = np.log10(df_nonzero[df_y_name])

    # define our (line) fitting function
    # fitfunc = lambda p, x: p[0] + p[1] * x   
    errfunc = lambda p, x, y: (y - (p[0] + p[1] * x ))
    pinit   = [0.15, -0.25] #initial guess
    out     = sciopt.leastsq(errfunc, pinit, args=(logx, logy))
    pfinal  = out[0]
    index   = pfinal[1]
    amp     = 10.0**pfinal[0]
    y       = amp*x**index
    return [index, amp, x, y]  
#------------------------------------------------------------
# decode file names used during runs for ability to retrieve loading paths, drainage, d_r, etc.
# function create here / used later
def decode_name(filework,start_loc):
    # function receives a name
    infoList = filework[start_loc:-4].split("_")
    
    water    = infoList[0][0]   # will be 'u' or 'd'
    driver   = infoList[0][1:]  # will be 'DSS' or 'PSC'
    goal     = infoList[1]      # will be 'mono','MRD','vol','cyc','rec'
    density  = infoList[2][2:]  # will be '35','55','75'
    output   = infoList[-1]     # will be '1'-'5' or peakPhi, csrN etc.
    
    if infoList[1]   == "cyc":
        # Cyclic Undrained DSS drivers have 3 extra pieces of info
        # all others have 2 extra pieces of info
        # monotonics have none
        extra = infoList[-4:-1]
    elif infoList[1] == "MRD":
        extra = infoList[-3:-1]
    elif infoList[1] == "vol":
        extra = infoList[-3:-1]
    elif infoList[1] == "rec":
        extra = infoList[-3:-1]
    else:
        extra = 0
    return([driver, goal, water, density, extra, output])
#------------------------------------------------------------
# driverType = 'DSS' or 'PSC'
# testType   = 'mono','MRD','vol','cyc','rec'
# drainType  = 'u' or 'd'
# density    = '35','55','75' or [] for all
# output     = single element number or summary file (e.g. peakPhi, csrN)

def create_file_list(fileList,start_loc, driverType = [], testType  = [], drainType = [], 
                                         density    = [], extraInfo = [], output    = []):
    file_list = [] # reset list
    for file in fileList:
        match = 0  # use to check matches all parameters provided    
        file_info = decode_name(file, start_loc)
        if not driverType:
            match = match + 1
        else:         
            for value in driverType:      # if user selects multiple types
                if file_info[0] == value: # check driver types: mnotonic, cyclic, mod-red
                    match = match + 1
                    break
        
        if not testType:
            match = match + 1
        else:                 
            for value in testType:
                if file_info[1] == value:
                    match = match + 1
                    break

        if not drainType:
            match = match + 1
        else: 
            for value in drainType:
                if file_info[2] == value:
                    match = match + 1
                    break
                    
        if not density:
            match = match + 1
        else:                      
            for value in density:         # if user selects multiple types
                if file_info[3] == value: # check density (decimal)
                    match = match + 1
                    break
        
        if not output:
            match = match + 1
        else:                      
            for value in output:          # if user selects multiple types
                if file_info[5] == value: # check density (decimal)
                    match = match + 1
                    break
        #===================================================================
        if not extraInfo:
            match = match + 1
        #===================================================================
        elif file_info[1] == ('cyc'):               
            submatch = 0
            sigvc = extraInfo[0]
            alpha = extraInfo[1]
            Ko    = extraInfo[2]
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not sigvc:
                submatch = submatch + 1   # any stress okay
            else:
                for value in sigvc:       # check each item in value[1]
                    if file_info[4][0][3:] == value:
                        submatch = submatch + 1
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not alpha:
                submatch = submatch + 1   # any static stress ratio okay
            else:                         # alpha exists, could be giving multiple alpha
                for value in alpha:       # check each item in alpha
                    if file_info[4][1][1:] == value:
                        submatch = submatch + 1 
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not Ko:
                submatch = submatch + 1   # any Ko value okay
            else:                         # Ko exists, could be giving multiple Ko values
                for value in Ko:          # check each item in Ko
                    if file_info[4][2][2:] == value:
                        submatch = submatch + 1 
                        break  
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if submatch == 3:
                match = match + 1             
        #===================================================================
        elif file_info[1] == 'MRD':
            submatch = 0
            Ncyc  = extraInfo[0]
            maxg  = extraInfo[1]
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not Ncyc:
                submatch = submatch + 1   # any number of cycles okay
            else:
                for value in Ncyc:        # check each item in value
                    if file_info[4][0][4:] == value:
                        submatch = submatch + 1
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not maxg:
                submatch = submatch + 1   # any static stress ratio okay
            else:                         # alpha exists, could be giving multiple alpha
                for value in maxg:        # check each item in alpha
                    if file_info[4][1][3] == value:  # assumes single digit shear strain (need to do 3:4 for double)
                        submatch = submatch + 1 
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if submatch == 2:
                match = match + 1
        #===================================================================
        elif file_info[1] == 'vol':
            submatch = 0
            Ncyc  = extraInfo[0]
            maxg  = extraInfo[1]
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not Ncyc:
                submatch = submatch + 1   # any number of cycles okay
            else:
                for value in Ncyc:        # check each item in value
                    if file_info[4][0][4:] == value:
                        submatch = submatch + 1
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not maxg:
                submatch = submatch + 1   # any static stress ratio okay
            else:                         # alpha exists, could be giving multiple alpha
                for value in maxg:        # check each item in alpha
                    if file_info[4][1][3] == value:  # assumes single digit shear strain (need to do 3:4 for double)
                        submatch = submatch + 1 
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if submatch == 2:
                match = match + 1
        #===================================================================
        elif file_info[1] == 'rec':
            submatch = 0
            sigvc = extraInfo[0]
            alpha = extraInfo[1]
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not sigvc:
                submatch = submatch + 1   # any number of cycles okay
            else:
                for value in sigvc:        # check each item in value
                    if file_info[4][0][3:] == value:
                        submatch = submatch + 1
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if not alpha:
                submatch = submatch + 1   # any static stress ratio okay
            else:                         # alpha exists, could be giving multiple alpha
                for value in alpha:       # check each item in alpha
                    if file_info[4][1][1:] == value:  # assumes single digit shear strain (need to do 3:4 for double)
                        submatch = submatch + 1 
                        break
            #--**--**--**--**--**--**--**--**--**--**--**--**--**--**--**--*
            if submatch == 2:
                match = match + 1
                    
        if match == 6:
            file_list.append(file)
    return file_list