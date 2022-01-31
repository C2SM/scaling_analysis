#!/usr/bin/python
#
# Script to use the script "create_scaling_table_per_exp.py" on different experiments in different folders
#
#
# Example : python send_analyse_different_exp_at_once.py
#
# C. Siegenthaler (C2SM) , December 2019
#
############################################################################################

import os
import shutil
import subprocess


class exp_class:

    def __init__(self, name, path, mod=None, factor=None, comp=None):
        self.name = name
        self.path = path
        self.mod = mod
        self.factor = factor
        self.comp = comp


n_step = 1  # step of the analyse : 1 -> send jobs
#                       2 -> analyse and synchronise csv file in home
lo_send_batch = False
lo_analyse_exps = False
lo_sync_home = False

if n_step == 1:
    lo_send_batch = True
elif n_step == 2:
    lo_analyse_exps = True
    lo_sync_home = True
else:
    print(
        'Info : Uses default : lo_send_batch = {} , lo_analyse_exps = {}, lo_sync_home = {}'
        .format(lo_send_batch, lo_analyse_exps, lo_sync_home))

# folder to put the final files at the end
p_to_sync = '/users/colombsi/scaling_ana/'

path_script = os.getcwd()

# initialize list of experiments to analyse
exps_to_analyse = []

# define exps to proceed
p = '/scratch/snx3000/colombsi/icon-c2sm/different_install/'
exps_to_analyse.extend([exp_class(name = exp_name, path = os.path.join(p,comp), mod='icon', factor=1, comp='_{}'.format(comp)) \
                   for exp_name in ['atm_amip','atm_amip_6h','atm_amip_1m'] for comp in ['intel','cray','pgi']])

for exp in exps_to_analyse:
    print('EXP : {}'.format(exp.name))
    print('DIR : {}'.format(exp.path))

    # construct and lauch different running script for different number of nodes
    # --------------------------------------------------------------------------------
    if lo_send_batch and (exp.mod.upper() == 'ICON'):

        print('Launch exp {}{}'.format(exp.name, exp.comp))

        os.chdir(exp.path)

        print('In directory {}'.format(os.getcwd()))
        subprocess.call(["python", os.path.join(path_script,'send_several_run_ncpus_perf_ICON.py'), \
                        '-e', exp.name,'-o', exp.comp, \
                        '-NH','6', '-n', '1', '12','16','36','48'])
    elif lo_send_batch:
        print(
            'WARNING : Sending different experiments with different numbers of nodes for ECHAM_HAM has not been implemented yet'
        )
        print('The experiment {} is not done asssociated is : {}'.format(
            os.path.join(exp.path, 'run', exp.name), exp.mod.upper()))
    else:
        print('NOT sending any job to run')

    # analyse different experiments
    # --------------------------------------------------------------------------------
    if lo_analyse_exps:

        os.chdir(os.path.join(exp.path, 'run'))

        total_exp_name = '{}{}'.format(exp.name, exp.comp)
        print('Analyse exp {}'.format(total_exp_name))

        subprocess.call([
            "python",
            os.path.join(path_script, "create_scaling_table_per_exp.py"), "-e",
            total_exp_name, "-m", exp.mod, "-y",
            str(exp.factor)
        ])

    # copy files
    # --------------------------------------------------------------------------------
    if lo_sync_home:

        if not os.path.isdir(p_to_sync):
            os.mkdir(p_to_sync)

        filename = '{}{}.csv'.format(exp.name, exp.comp)
        file_to_copy = os.path.join(exp.path, 'run', filename)

        if os.path.isfile(file_to_copy):
            print('Copy file {}'.format(filename))
            shutil.copy2(file_to_copy, p_to_sync)
        else:
            print('WARNING : the summary file does not exists : {}'.format(
                file_to_copy))
    print('---------------------------------------')
