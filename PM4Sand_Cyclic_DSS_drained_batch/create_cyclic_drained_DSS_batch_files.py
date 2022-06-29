#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:10:27 2022
@author: kziot

- File opens Template with header line info, writes parametrically varying 
  parameters underneath, writes complete contents of DSS_cyclic_drained.fis file
  sets savefile information (for *.sav in running FLAC) and closes it
- Each produced *.fis file is named according to the varied parameters
- a batch_drainedDSS_vol.fis or batch_drainedDSS_MRD.fis is produced populated by call commands for each file
  generated for later being called in FLAC
- As of now, placeholders for relative density (can be provided with 1 or more array values)
  number of cycles to be performed at each strain limit (degradation), and maximum strain
  to be reached by each driver
- if 'volumetric' set to 1 then files are produced that apply uniform strain controlled @1% loading for a maximum
  number of cycles / if not the file produces files for MRD curves that exercise the element for Ncyc across an 
  array of shear strains
- all other variables are defined inside DSS_cyclic_drained.fis and can be either
  changed within (if constant across all drivers) or brought herein to be added as 
  other array to be iterated over following the same philosophy
- only batch_drainedDSS_***.fis file needs to be called by FLAC
- original file in Matlab by kziot, then modified for python by sksinha, melkortbawi, kziot
- extended by kziot June 2022
- CAUTION: file naming conventions intimately related to post-processing & plotting protocols
"""

# Input Parameters
Soil     = ""
TestName = "dDSS" # will match template Driver and built upon that

# Create arrays of values to be varied across all Drivers
# Produced files will be named accordingly
volumetric  = 0
Dr          = [0.35, 0.55, 0.75]    # Relative Density
Ncyc        = [3]                   # Number of Cycles to be performed at each strain (N<=10)
gamma_count = [8]                   # Stop at this value in limit array(10) [index in array]

# Dictionary that matches strain array index to actual maximum strain reached in driver
gamma_dict = {1:"0.0003%",2:"0.001%",3:"0.003%",4:"0.01%",5:"0.03%",6:"0.1%",7:"0.3%",8:"1%",9:"3%",10:"10%"}

Test_File     = "DSS_cyclic_drained.fis"
Template_File = "templ_drDSScyc.fis"

# Initialize lines for final batch file
call_line   = 'call #\n'
batch_lines = []

if volumetric  != 1:
  for Dr_i in Dr:
      for Ncyc_i in Ncyc:
          for gamma_count_i in gamma_count:
                # First create a file name 
                BaseFile = TestName+Soil+ "_MRD" + "_Dr" +str(int(Dr_i*100))+"_Ncyc"+str(Ncyc_i)+"_max"+str(gamma_dict[gamma_count_i])
                FileName = BaseFile+".fis"

                # Create a new file and open template and test file
                fileID 			= open(FileName,"w+");
                Template_fileId = open(Template_File,"r");
                Test_fileId     = open(Test_File,"r")

                # Writing to a file
                fileID.write(Template_fileId.read())
                fileID.write("\n\n")

                fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
                fileID.write("def $var_inputs\n")
                fileID.write("\t$Dr           = " + str(Dr_i) + " \n")
                fileID.write("\t$Ncycles      = " + str(Ncyc_i) + " \n")
                fileID.write("\t$strain_count = " + str(gamma_count_i) + " \n")
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
  batch_file = open("batch_drainedDSS_MRD.fis", "w")

else:
  for Dr_i in Dr:
      for Ncyc_i in Ncyc:
                # First create a file name 
                BaseFile = TestName+ Soil +"_vol"+ "_Dr"+str(int(Dr_i*100))+"_Ncyc"+str(Ncyc_i)+"_max"+str(gamma_dict[8])
                FileName = BaseFile+".fis"

                # Create a new file and open template and test file
                fileID          = open(FileName,"w+");
                Template_fileId = open(Template_File,"r");
                Test_fileId     = open(Test_File,"r")

                # Writing to a file
                fileID.write(Template_fileId.read())
                fileID.write("\n\n")

                fileID.write(";------------GENERAL INPUT CONDITIONS------------\n")
                fileID.write("def $var_inputs\n")
                fileID.write("\t$Dr           = " + str(Dr_i) + " \n")
                fileID.write("\t$Ncycles      = " + str(Ncyc_i) + " \n")
                fileID.write("\t$strain_count = 1                   \n")
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
  batch_file = open("batch_drainedDSS_vol.fis", "w")


batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write(";                     FLAC batch calling of input files                 \n")
batch_file.write(";-----------------------------------------------------------------------\n")
batch_file.write("\n")
batch_file.writelines(batch_lines)
batch_file.close()
''' EoF'''