#!/usr/bin/python
#
# Script to use perftool analysis script on different experiments in different folders
#
#
#Example : perf_speedup.
#
# C. Siegenthaler (C2SM) , December 2019
#
############################################################################################



import os
import subprocess

exp_to_analyse = {path}


class exp_class:
    def __init__(self, name, path, mod=None,factor=None):
        self.name = name
        self.path = path
        self.mod  = mod
        self.factor = factor


exps_to_anaylse =[]

p = '/scratch/snx3000/colombsi/icon_c2sm_intel/run'
exps_to_anaylse = [exp_class(name = exp_name, path = p, mod='icon', factor=1) \
                   for exp_name in ['atm_amip_intel_6h','atm_amip_intel_1m']
exps_to_anaylse.append([exp_class(name = exp_name, path = p, mod='icon', factor=53) \
                   for exp_name in ['ICON_limarea_Bernhard_7d_intel']])

p = '/scratch/snx3000/colombsi/icon_c2sm_gcc/run'
exps_to_anaylse = [exp_class(name = exp_name, path = p, mod='icon',factor=1) \
                   for exp_name in ['atm_amip_gcc_6h','atm_amip_gcc_1m']

p = '/scratch/snx3000/colombsi/icon_c2sm_cray/run'
exps_to_anaylse = [exp_class(name = exp_name, path = p, mod='icon',factor=1) \
                   for exp_name in ['atm_amip_6h','atm_amip_1m']
exps_to_anaylse.append([exp_class(name = exp_name, path = p, mod='icon',factor=53) \
                   for exp_name in ['ICON_limarea_Bernhard_7d']])

p = '/scratch/snx3000/colombsi/icon-hammoz_gcc_benchmark/run'
exps_to_anaylse = [exp_class(name = exp_name, path = p, mod='icon',factor=12) \
                   for exp_name in ['atm_amip_hammoz_marc','atm_amip_hammoz_marc_tsx2']

for exp in exps_to_anaylse:
    os.chdir(exp.path)

    subprocess.call(["python", "scaling_analysis", "-e", exp.name,"-m",exp.mod])

