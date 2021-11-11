#!/usr/bin/python

# Wrapper to send several ECHAM-(HAM) runs using the jobscriptoolkit
# for performance anaylsis with different number of cpus
#
# Usage: go into your echam run directory, prepare the basis run set-up
# call the present script
#
# C. Siegenthaler (C2SM) , July 2015
#
############################################################################################

import numpy as np
import os
import datetime
import argparse

if __name__ == "__main__":

    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--basis_folder', '-b', dest = 'basis_folder',\
                            help='basis folder run containing the configuration as to use as template. The name has to finish with "_cpusXX".')
    parser.add_argument('--ncpus_incr', dest = 'cpus_incr',\
                            default = 16,\
                            type = int,\
                            help = 'increment of cpus number between each simulation.')
    parser.add_argument('--niter', dest = 'niter',\
                            default = 10,\
                            type = int,\
                            help = 'number of iterations (niter simulations will be performed with the number of cpus for each simulation is [1,2,....,niter-1]*ncpus_incr.')

    parser.add_argument('--nbeg_iter', dest = 'nbeg_iter',\
                            default = 1,\
                            type = int,\
                            help = 'begining of the iteration (the simulations will be performed with the number of cpus for each simulation is [nbeg_iter,nbeg_iter+1....,niter-1]*ncpus_incr.')

    parser.add_argument('--ncpus', dest = 'cpus_to_proceed',\
                            default = [],\
                            type = int,\
                            nargs = '*',\
                            help = 'cups number of the simulation to analyse.This have priority over -ncpus_incr, -niter and -nbeg_iter')
    parser.add_argument('--nnodes', '-n', dest = 'nodes_to_proceed',\
                            default = [],\
                            type = int,\
                            nargs = '*',\
                            help = 'nodes number of the simulation to analyse. This have priority over -ncpus_incr, -niter and -nbeg_iter')
    parser.add_argument('--cpu_per_node', dest = 'cpu_per_node',\
                            default = 12,\
                            type = int,\
                            help = 'numper of CPUs per node')
    parser.add_argument('-d', action='store_true',\
                            help = 'perform dry run, i.e. run the script competely, but do not send the jobs to the batch queue')
    parser.add_argument('-dw', action='store_true',\
                            help = 'redifine walltime')

    args = parser.parse_args()

    # define number of cpus for which experiment should be sent
    #-------------------------------------------------------------
    l_cpus_def = False

    if (len(args.cpus_to_proceed) > 0) and (len(args.nodes_to_proceed) > 0):
        print(
            'You can specify either the number of cpus or the number of nodes, not both.'
        )
        print('Exiting')
        exit(1)

    if (len(args.nodes_to_proceed) > 0):
        args.cpus_to_proceed = args.cpu_per_node * np.array(
            args.nodes_to_proceed)
        l_cpus_def = True

    if len(args.cpus_to_proceed) > 0:
        l_cpus_def = True

    if not l_cpus_def:
        args.cpus_to_proceed = (np.arange(args.nbeg_iter, args.niter) *
                                args.cpus_incr)
        l_cpus_def = True

    # define new experiment name
    #--------------------------------------------------------------
    # experiment name basis exp
    exp_name_bas_exp = os.path.basename(args.basis_folder)

    # setting filename basis exp
    setting_bas_exp = os.path.join(args.basis_folder,
                                   'settings_{}'.format(exp_name_bas_exp))

    # check if the basis name is finishing by "cpusXX" and  assign kernel name of teh new experiments
    if (exp_name_bas_exp.split('_')[-1].startswith('cpus')):
        exp_name_nucl = '_'.join(
            exp_name_bas_exp.split('_')[:-1])  # name of the new experiments
    else:
        exp_name_nucl = exp_name_bas_exp

    # get walltime and cpus from basis exp, for computning later the new walltime
    #--------------------------------------------------------------
    def grep(string, filename):
        # returns lines of file_name where string appears
        # mimic the "grep" function

        # list of lines where string is found
        list_line = []

        for line in open(filename):
            if string in line:
                list_line.append(line)
        return list_line

    def value_string_file(string, filename):
        # returns the value of a variable defined in a file
        # e.g. for walltime, returns 8:00:00 if if filename walltime=8:00:00

        #initialisation
        values = []

        # list of occurences found by "grep"
        occurences = grep(string, setting_bas_exp)

        for occ in occurences:

            #remove comments
            line_wo_comment = occ.split('#')[0]

            # get value
            def_split = [s.strip() for s in line_wo_comment.split('=')]

            # do not consider variable if string is in the middle of another word
            if string == def_split[0]:
                values.append(def_split[1])
        return (values)

    walltime_bas = value_string_file("walltime", setting_bas_exp)[0].strip('"')
    ncpus_bas = int(value_string_file("ncpus", setting_bas_exp)[0].strip('"'))

    #time in datetime format
    basis_day = "2000-01-01"
    walltime_datetime = datetime.datetime.strptime('{} {}'.format(basis_day,walltime_bas), '%Y-%m-%d %H:%M:%S') - \
                        datetime.datetime.strptime(basis_day, '%Y-%m-%d')

    # send experiments
    #---------------------------------------------------------------

    # change directory to be in the basis folder
    #   os.chdir(args.basis_folder)

    # loop over number of cpus to be lauched
    for ncpus in args.cpus_to_proceed:

        # define name of the new experiment
        new_exp_name = '%s_cpus%i' % (exp_name_nucl, ncpus
                                      )  # new experiment name

        # new walltime
        comp_walltime = (walltime_datetime * ncpus_bas / ncpus)
        new_walltime = datetime.timedelta(
            seconds=round(comp_walltime.total_seconds()))

        # job definition and submission
        string_to_overwrite = "ncpus={};exp={}".format(ncpus, new_exp_name)
        if args.dw:
            string_to_overwrite += ";walltime={}".format(new_walltime)

        print('jobsubm_echam.sh -o "{}" {}'.format(string_to_overwrite,
                                                   setting_bas_exp))
        print(
            '--------------------------------------------------------------------------------------------------------'
        )
        if not args.d:
            os.system('jobsubm_echam.sh -o "{}" {}'.format(
                string_to_overwrite, setting_bas_exp))
