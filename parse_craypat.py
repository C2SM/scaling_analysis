#!/usr/bin/python

# Parse the craypat analysis files to extract the info CSCS ask and create a unique csv file
# The script will read recursively all the files named "summary*.txt" in the current directory 
 

# Colombe Siegenthaler    C2SM (ETHZ) , 2018-10

import numpy as np
import pandas as pd   # needs pythn modules to be loaded:  module load cray-python/3.6.5.1 PyExtensions/3.6.5.1-CrayGNU-18.08
import os
import glob

# name of the output file
out_f = 'Craypat_table'

# get current directory
pwd = os.getcwd()

# find all the summary files
all_files = glob.glob('{}/**/summary*.txt'.format(pwd), recursive=True)

# definition of teh directories to exclude
exclude_dir = ['before_update_Oct2018']
files_to_exclude=[]
for filename in all_files:
    if any([s in filename for s in exclude_dir]):
        files_to_exclude.append(filename)

# exclude files
for f in files_to_exclude:
    all_files.remove(f)

# define dataframe for output
data_global = pd.DataFrame(columns=['Variable'])

# parse each file of the list
for ifile,filename in enumerate(all_files):
    print('Parsing file {}'.format(filename))

    # get name of the exp
    try:
        exp_name = os.path.basename(filename).split('summary_')[1].rstrip('.txt')
    except:
        exp_name = "UNKNOWN_{}".format(ifile)
        print("Warning: Found a summary file whithout any model label:{}".format(filename)) 
        print("Set model label:{}".format(exp_name))

    # read file
    data_single = pd.read_csv(filename, sep=':', header=None) 

    # rename first column into 'Variable'
    data_single.rename(columns={ 0 : "Variable" },inplace=True)

    # retrieve number of columns
    ncol = len(data_single.columns) 

    # combine all the columns instead Variable together (the HH:MM:SS were separated by mistake )
    data_single[exp_name] = data_single[1]
    del data_single[1]  
    for icol in np.arange(2,ncol): 
        data_single[exp_name] = data_single[exp_name] + ':' + data_single[icol].fillna("")
        del data_single[icol] 
    
    # delete '::' in case it was added in teh column combination
    data_single[exp_name] = data_single[exp_name].str.rstrip(':')

    # add look for Jobnumber of the craypat run - > need to find slurm file
    if exp_name.upper().startswith('ICON'):
        slurm_file_path = glob.glob('{}/LOG*.o'.format(os.path.dirname(filename)))
    elif (exp_name.upper().startswith('ECHAM') or exp_name.upper().startswith('MPI-ESM')):        
        slurm_file_path = glob.glob('{}/slurm*.txt'.format(os.path.dirname(filename)))
    else:
        print("Warning: No rule for finding the slurm filefor the file {}.".format(filename))
        print("Rules for finding slurm files are only defined for summary files named summary_label*.txt, where label is one of ECHAM, MPI_ESM or ICON ")
        slurm_file_path = []

    # get the jobnumber from the slurm filename
    if not len(slurm_file_path) == 1 :
        print ("Warning, several or no slurm file.")
        print ("The following files are found:{}".format("\n".join(slurm_file_path)))
        print ("Set job number to 0")
        jobnumber = "0"
    else:
        jobnumber = os.path.basename(slurm_file_path[0]).split('.')[-2]

    # remove the submission number (especially for echam run)
    jobnumber = jobnumber.split('_')[-1]

     # add the jobnumber in the dtaaframe as a new line
    data_single.loc[len(data_single)] =  ['Job Number',jobnumber]
 
    # fill the outter dataframe
    data_global = pd.merge(data_global, \
                           data_single.rename(columns={exp_name:exp_name.replace('_',' ')}), \
                           how='outer', on=['Variable'])



# write out the global dataframe
data_global.to_csv('{}.csv'.format(out_f),sep=',', index=False)
 
