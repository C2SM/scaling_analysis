#!/usr/bin/python
#
# Script to use the script "create_scaling_table_per_exp.py" on different experiments in different folders
#
#
# Example : python anaylse_different_exp_at_once.py
#
# C. Siegenthaler (C2SM) , December 2019
#
############################################################################################



import os
import subprocess


class exp_class:
    def __init__(self, name, path, mod=None,factor=None):
        self.name = name
        self.path = path
        self.mod  = mod
        self.factor = factor

lo_send_batch = True
lo_analyse_exps = False

p_to_sync = '/users/colombsi/scaling_ana/'

path_script = os.getcwd()

exps_to_analyse =[]

# define exps to proceed
p = '/scratch/snx3000/colombsi/icon-c2sm/different_install/'
exps_to_analyse.extend([exp_class(name = exp_name, path = os.path.join(p,comp), mod='icon', factor=1) \
                   for exp_name in ['atm_amip'] for comp in ['pgi','cray']])

for exp in exps_to_analyse:
    print ('EXP : {}'.format(exp.name))
    print ('DIR : {}'.format(exp.path))

    # construct and lauch different running script for different number of nodes
    # --------------------------------------------------------------------------------
    if lo_send_batch and (exp.mod.upper() == 'ICON') :
        os.chdir(exp.path)
        print('In directory {}'.format(os.getcwd()))
        subprocess.call(["python", os.path.join(path_script,'send_several_run_ncpus_perf_ICON.py'), '-e', exp.name,'-n', '1', '10', '12', '15'])
    elif lo_send_batch: 
        print('WARNING : Sending different experiments with different numbers of nodes for ECHAM_HAM has not been implemented yet')
        print('The experiment {} is not done asssociated is : {}'.format(os.path.join(exp.path,'run',exp.name),exp.mod.upper()))
    else:
        print('NOT sending any job to run')

    # analyse different experiments
    # --------------------------------------------------------------------------------
    if lo_analyse_exps:

        os.chdir(os.path.join(exp.path,'run'))

        subprocess.call(["python", os.path.join(path_script,"create_scaling_table_per_exp.py"), "-e", exp.name,"-m",exp.mod,"-y", str(exp.factor)])

        subprocess.call(["rsync", "-av", "{}.csv".format(exp.name), p_to_sync])
        print ('---------------------------------------')
