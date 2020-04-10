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

p_to_sync = '/users/colombsi/scaling_ana/'

path_script = os.getcwd()

exps_to_anaylse =[]

p = '/scratch/snx3000/colombsi/icon_c2sm_intel/run'
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon', factor=1) \
                   for exp_name in ['atm_amip_intel_6h','atm_amip_intel_1m']])
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon', factor=53) \
                   for exp_name in ['ICON_limarea_Bernhard_7d_intel']])
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon', factor=52) \
                   for exp_name in ['ICON_limarea_Bernhard_init_intel']])

p = '/scratch/snx3000/colombsi/icon_c2sm_gcc/run'
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon',factor=1) \
                   for exp_name in ['atm_amip_gcc_6h','atm_amip_gcc_1m']])
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon',factor=121) \
                   for exp_name in ['ICON_limarea_Bernhard_3d_gcc']])
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon',factor=52) \
                   for exp_name in ['ICON_limarea_Bernhard_init_gcc']])

p = '/scratch/snx3000/colombsi/icon_c2sm_cray/run'
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon',factor=1) \
                   for exp_name in ['atm_amip_6h','atm_amip_1m']])
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon',factor=53) \
                   for exp_name in ['ICON_limarea_Bernhard_7d']])
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon',factor=52) \
                   for exp_name in ['ICON_limarea_Bernhard_init']])

p = '/scratch/snx3000/colombsi/icon-hammoz_gcc_benchmark/run'
exps_to_anaylse.extend([exp_class(name = exp_name, path = p, mod='icon',factor=12) \
                   for exp_name in ['atm_amip_hammoz_marc','atm_amip_hammoz_marc_tsx2']])

for exp in exps_to_anaylse:
    print ('EXP : {}'.format(exp.name))
    print ('DIR : {}'.format(exp.path))
    os.chdir(exp.path)
    
    subprocess.call(["python", os.path.join(path_script,"create_scaling_table_per_exp.py"), "-e", exp.name,"-m",exp.mod,"-y", str(exp.factor)])

    subprocess.call(["rsync", "-av", "{}.csv".format(exp.name), p_to_sync])
    print ('---------------------------------------')
