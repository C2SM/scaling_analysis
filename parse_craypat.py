#!/usr/bin/python

# Parse the craypat analysis files to extract the info CSCS ask and create a unique csv file
# The script will read recursively all the files named "summary*.txt" in the current directory 
 

# Colombe Siegenthaler    C2SM (ETHZ) , 2018-10

import numpy as np
import pandas as pd   # needs pythn modules to be loaded:  module load cray-python/3.6.5.1 PyExtensions/3.6.5.1-CrayGNU-18.08
import os
import glob
import argparse
import subprocess
import sys

def create_summary_file(runtime_file, path_dir_for_sumfile, exp_name):
    # Create summary_[label_model_name].txt from RUNTIME (written by craypat tool) file
    # input is runtime file
    
    # final summary file for this exp
    out_summary_file = os.path.join(path_dir_for_sumfile,'summary_{}.txt'.format(exp_name))

    if not os.path.isfile(runtime_file):
        print('Warning: Runtime file is not a proper file : {}'.format(runtime_file)) 

    # copy part of runtime file into summary file
    with open(runtime_file) as fin, open(out_summary_file, 'w') as fout:
        for line in fin:
            # get starting point
            if line.startswith("#"):
               continue
            
            # copy the line into fout
            fout.write(line)
            
            # ending point
            if line.startswith('I/O Write Rate'):
               break

    return(out_summary_file)

def extract_dir_exp(runtime_file):
    # get the general path to exp dir

    path_dir = os.path.dirname(runtime_file.split('+')[0])
    exp_name = os.path.basename(path_dir)

    return (path_dir,exp_name)

def get_slurm_file_dep_mod(path_dir):
    # get the path to the slurm file depending on the model family 

    gen_mod_family = os.path.join(path_dir).split('/')[-2].upper()
    if gen_mod_family.startswith('ICON'):
        slurm_file_path = glob.glob('{}/LOG*.o'.format(path_dir))
    elif (gen_mod_family.startswith('ECHAM') or gen_mod_family.startswith('MPI-ESM')):
        slurm_file_path = glob.glob('{}/slurm*.txt'.format(path_dir))
    else:
        print("Warning: No rule for finding the slurm filefor the file {}.".format(filename))
        print("Rules for finding slurm files are only defined for module family : ECHAM, MPI-ESM or ICON ")
        print('The family model found is : {}'.format(gen_mod_family)) 
        slurm_file_path = []

    return(slurm_file_path)

def get_jobnumber_from_slurmfile(slurm_file_path):
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

    return(jobnumber)

def get_jobnumber(path_dir):

    # add look for Jobnumber of the craypat run - > need to find slurm file
    slurm_file_path = get_slurm_file_dep_mod(path_dir)

    # get the jobnumber from the slurm filename
    jobnumber = get_jobnumber_from_slurmfile(slurm_file_path)

    return(jobnumber)

if __name__ == "__main__":
    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--exclude', '-e', dest = 'exclude_dir',\
                       default = [],\
                       nargs = '*',\
                       help='folders to exclude.') 
    parser.add_argument('--out_f', '-o', dest = 'out_f',\
                       default = 'Craypat_table',\
                       help = 'filename of the output.') 
    args = parser.parse_args()

    # get current directory
    pwd = os.getcwd()

    # find all the summary files
    #all_files = glob.glob('{}/**/summary*.txt'.format(pwd), recursive=True)
    all_files = glob.glob('{}/**/RUNTIME.rpt'.format(pwd), recursive=True)

    # definition of teh directories to exclude
    #exclude_dir = ['before_update_Oct2018']
    files_to_exclude=[]
    for filename in all_files:
        if any([s in filename for s in args.exclude_dir]):
            files_to_exclude.append(filename)

    # exclude files
    for f in files_to_exclude:
        all_files.remove(f)

    # define dataframe for output
    data_global = pd.DataFrame(columns=['Variable'])

    # parse each file of the list
    for ifile,filename in enumerate(all_files):
        print('----------------------------------------------------------------------')
        print('Parsing file {}'.format(filename))

        path_dir, exp_name = extract_dir_exp(filename)

        # creation of a summary file from the report file (written by Craypat tool)
        summary_file_exp = create_summary_file(filename,path_dir,exp_name)
   
        # extract exp_name
        #exp_name = os.path.basename(summary_file_exp).split('summary_')[1].rstrip('.txt')

        # read file
        data_single = pd.read_csv(summary_file_exp, sep=':', header=None) 

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

        # get the jobnumber from the slurm filename in the directory
        jobnumber = get_jobnumber(path_dir)

        # add the jobnumber in the dtaaframe as a new line
        data_single.loc[len(data_single)] =  ['Job Number',jobnumber]
 
        # fill the outter dataframe
        data_global = pd.merge(data_global, \
                               data_single.rename(columns={exp_name:exp_name.replace('_',' ')}), \
                               how='outer', on=['Variable'])



    # write out the global dataframe
    data_global.to_csv('{}.csv'.format(args.out_f),sep=',', index=False)
 
