#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:10:27 2022
@author: kziot

- File opens Template with header line info, writes parametrically varying 
  parameters underneath, writes complete contents of DSSmono.fis file
  sets savefile information (for *.sav in running FLAC) and closes it
- Each produced *.fis file is named according to the varied parameters
- a batch_DSS_mono.fis is produced populated by call commands for each file
  generated for later being called in FLAC
- As of now, placeholders for relative density (can be provided with 1 or more array values)
  and the drainage conditions have been used
- all other variables are defined inside DSSmono.fis and can be either
  changed within (if constant across all drivers) or brought herein to be added as 
  other array to be iterated over following the same philosophy
- only batch_DSS_mono.fis file needs to be called by FLAC
- original file in Matlab by kziot, then modified for python by kziot
"""

# Input Parameters - CHANGE HERE BETWEEN PSC and DSS
Soil     = ""
TestName       = "PSC_mono"              # choices now as 'PSC_mono' or 'DSS_mono' will match template Driver and built upon that
Test_File      = "PSC_monotonic.fis"     # 'DSS_monotonic.fis'
Template_File  = "templ_PSCmono.fis"     # 'templ_DSSmono.fis'
batch_FileName = "batch_PSC_mono.fis"    # 'batch_DSS_mono.fis'

# Create arrays of values to be varied across all Drivers
# Produced files will be named accordingly
Dr       = [0.35, 0.55, 0.75]    # Relative Density
drainage = [0, 1]                # 0 for undrained, 1 for drained

# Dictionary that matches strain array index to actual maximum strain reached in driver
drain_dict  = {0:"u",1:"d"}

# Initialize lines for final batch file
call_line   = 'call #\n'
batch_lines = []

for drainage_i in drainage:
  for Dr_i in Dr:
    # First create a file name 
    BaseFile = str(drain_dict[drainage_i]) + TestName + Soil + "_Dr" + str(int(Dr_i*100))
    FileName = BaseFile + ".fis"
    
    # Create a new file and open template and test file
    fileID 			    = open(FileName,"w+");
    Template_fileId = open(Template_File,"r");
    Test_fileId     = open(Test_File,"r")

    # Writing to a file
    fileID.write(Template_fileId.read())
    fileID.write("\n\n")

    fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
    fileID.write("def $var_inputs\n")
    fileID.write("\t$Dr           = " + str(Dr_i) + " \n")
    fileID.write("\t$drained      = " + str(drainage_i) + " \n")
    fileID.write("\t$basefile     = \'" + BaseFile + "\' \n")
    fileID.write("end \n");
    fileID.write("$var_inputs\n\n")

    fileID.write(Test_fileId.read())

    fileID.write(";-------------Footer-------------------\n")
    fileID.write(";save @$savefile\n")
    fileID.write(";--------------------------------------\n")

    # Closing the files
    Test_fileId.close()
    Template_fileId.close()
    fileID.close()
    batch_lines.append(call_line.replace("#", FileName))

batch_file = open(batch_FileName, "w")   #'batch_DSS_mono.fis'

batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write(";                     FLAC batch calling of input files                 \n")
batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write("\n")
batch_file.writelines(batch_lines)
batch_file.close()
''' EoF'''