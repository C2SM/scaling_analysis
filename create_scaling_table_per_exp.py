#!/usr/bin/python

import numpy as np
import os
import argparse
import glob
import datetime
import itertools
import pandas as pd  # need to load module load PyExtensions on Piz Daint

# defines defaults values for nnodes, wallclock and date
default_wallclock = {
    'wallclock': np.nan,
    'nnodes': 10000,
    'date_run': datetime.datetime(1900, 1, 1).strftime("%Y-%m-%d %H:%M:%S")
}

if __name__ == "__main__":

    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp', '-e', dest = 'basis_name',\
                            help='basis name of the exp to anaylse.')
    parser.add_argument('--arange_nodes', dest = 'arange_nodes',\
                            nargs = 3,\
                            type = int,\
                            help = 'nodes number to analyse.')
    parser.add_argument('--nnodes', '-n', dest = 'nodes_to_proceed',\
                            default = [],\
                            type = int,\
                            nargs = '*',\
                            help = 'cups number of the simulation to analyse.This have priority over -ncpus_incr, -niter and -nbeg_iter')
    parser.add_argument('--outfilename','-o', dest = 'outfilename',\
                            default='',\
                            help='name of the ouput file')

    parser.add_argument('--res', '-r', dest = 'res',\
                            default='',\
                            help='resolution(with ocean) eg T63L31GR15 ')

    parser.add_argument('--mod','-m', dest = 'mod',\
                            default='icon',\
                            help='model type (icon, icon-ham, icon-clm)')

    parser.add_argument('--cpu_per_node', dest = 'cpu_per_node',\
                        default = 12,\
                        type = int,\
                        help = 'numper of CPUs per node')

    parser.add_argument('--fact_nh_yr', '-y', dest = 'factor_nh_year',\
                        default = 12,\
                        type = int,\
                        help = 'factor to multiply for getting NH per year')

    parser.add_argument('--no_x', action='store_false',\
                        help = 'some model logs have a "set -x" in the first line, therefore the "Script run successfully:  OK" string is contained twice in the logfile. Passing this argument assumes NO "set -x" set.')

    parser.add_argument('--ignore_errors', action='store_true',\
                        help = 'ignores errors in the logfile. This is useful whenever the run finishes normally, but hangs at cleanup.')

    args = parser.parse_args()

    # assume you are in teh directory where all experiment directories are
    path_exps_dir = os.getcwd()
    path_out = path_exps_dir

    # define files to analyse
    #----------------------------------------------------------------------

    l_cpus_def = False

    # 1st possibility: give nnodes to proceed
    if (len(args.nodes_to_proceed) > 0):
        nodes_to_proceed = np.array(args.nodes_to_proceed)
        l_cpus_def = True

    # 2nd possiblity: give minmax and iteration on number of nodes
    # set the list of experiment to proceed
    if (not l_cpus_def) and (args.arange_nodes is not None):
        nodes_to_proceed = np.arange(args.arange_nodes[0],
                                     args.arange_nodes[1],
                                     args.arange_nodes[2])
        l_cpus_def = True

    if l_cpus_def:
        if args.mod.upper().startswith("ICON-CLM"):
            slurm_files_ar = [
                glob.glob("{}/{}_nnodes{}_*.o*".format(path_exps_dir,
                                                       args.basis_name, n))
                for n in nodes_to_proceed
            ]
            slurm_files = list(itertools.chain.from_iterable(slurm_files_ar))
        elif args.mod.upper().startswith("ICON"):
            slurm_files_ar = [
                glob.glob("{}/LOG.exp.{}_nnodes{}.run.*".format(
                    path_exps_dir, args.basis_name, n))
                for n in nodes_to_proceed
            ]
            slurm_files = list(itertools.chain.from_iterable(slurm_files_ar))

    # 3rd possibility : use all the slurm files containing the basis name
    if (not l_cpus_def):
        if args.mod.upper().startswith("ICON-CLM"):
            slurm_files = glob.glob("{}/*{}*.o*".format(
                path_exps_dir, args.basis_name, args.basis_name))
        elif args.mod.upper().startswith("ICON"):
            slurm_files = glob.glob("{}/LOG.exp.{}*.run.*".format(
                path_exps_dir, args.basis_name, args.basis_name))

    # fill up array
    #-----------------------------------------------------------------------------------------------
    iref = 0

    if args.outfilename == '':
        args.outfilename = '%s.csv' % args.basis_name

    # array for store values read in the slurm file
    np_2print = []

    # dictionary containing the indices of the variables in the array np_2print
    dict_ind = {'Wallclock': 1, 'CET': 1}

    # conversion from cpu-sec to node-hours
    nodesec_to_nodehours = 1. / 3600.

    # performs the analysis (create a csv file)
    #ilin = 0


    def grep(string, filename):
        # returns lines of file_name where string appears
        # mimic the "grep" function

        # initialisation
        # list of lines where string is found
        list_line = []
        list_iline = []
        lo_success = False
        file = open(filename, 'r')
        count = -1
        while True:
            try:  # Some lines are read in as binary with the pgi compilation
                line = file.readline()
                count += 1
                if string in line:
                    list_line.append(line)
                    list_iline.append(count)
                    lo_success = True
                if not line:
                    break
            except Exception as e:
                continue
        file.close()
        return {"success": lo_success, "iline": list_iline, "line": list_line}

    def get_wallclock_icon(filename, no_x, num_ok=1, success_message=None):

        required_ok_streams = num_ok
        if success_message:
            OK_streams = grep(success_message, filename)["line"]
        else:
            OK_streams = grep('Script run successfully:  OK', filename)["line"]

        if len(OK_streams) >= required_ok_streams:
            timezone = 'CEST'
            time_grep = grep(timezone, filename)["line"]
            if not time_grep:
                timezone = 'CET'
                time_grep = grep(timezone, filename)["line"]

            time_arr = [
                datetime.datetime.strptime(
                    s.strip(), '%a %b %d %H:%M:%S ' + timezone + ' %Y')
                for s in time_grep
            ]

            wallclock = time_arr[-1] - time_arr[0]
        else:
            print("file {} did not finish properly".format(filename))
            print("Set Wallclock = 0")
            wallclock = datetime.timedelta(0)

        return {"wc": wallclock, "st": time_arr[0]}

    def check_icon_finished(filename,
                            string_sys_report='Script run successfully:  OK'):
        # return True if icon finished properly

        # initilisation
        lo_finished_ok = False

        # look for ok_line
        if grep(string_sys_report, filename)['success']:
            lo_finished_ok = True

        return (lo_finished_ok)

    def set_default_error_slurm_file(txt_message="Problem in the slurm file"):
        # error in the slurm file, set default values

        wallclock = default_wallclock['wallclock']
        nnodes = default_wallclock['nnodes']
        date_run = default_wallclock['date_run']
        print(txt_message)
        print("Set Wallclock = {} , and nodes = {}".format(wallclock, nnodes))

        return (wallclock, nnodes, date_run)


    # security. If not file found, exit
    if len(slurm_files) == 0:
        print("No slurm file founded with this basis name")
        print("Exiting")
        exit()

    # loop over number of cpus to be lauched
    for filename in slurm_files:

        print("Read file : {}".format(os.path.basename(filename)))
        # read nnodes and wallclock from file
        if args.mod.upper() == "ICON":
            if check_icon_finished(filename) or args.ignore_errors:
                # get # nodes and wallclock
                # infer nnodes from MPI-procs in ICON output
                nodes_line = grep("mo_mpi::start_mpi ICON: Globally run on",
                                  filename)["line"][0]
                nnodes = int(nodes_line.split(' ')[6])

                nnodes = nnodes // args.cpu_per_node

                wallclock = get_wallclock_icon(
                    filename, args.no_x)["wc"].total_seconds()
                date_run = get_wallclock_icon(filename, args.no_x)["st"]
            else:
                wallclock, nnodes, date_run = set_default_error_slurm_file(
                    "Warning : Run did not finish properly")

            # get job number
            jobnumber = float(filename.split('.')[-2])
        elif args.mod.upper() == "ICON-CLM":
            success_message = "ICON experiment FINISHED"
            if check_icon_finished(filename,
                                   success_message) or args.ignore_errors:
                # get # nodes and wallclock
                # infer nnodes from MPI-procs in ICON output
                nodes_line = grep("mo_mpi::start_mpi ICON: Globally run on",
                                  filename)["line"][0]
                nnodes = int(nodes_line.split(' ')[6])

                nnodes = nnodes // args.cpu_per_node

                wallclock = get_wallclock_icon(
                    filename,
                    args.no_x,
                    num_ok=1,
                    success_message=success_message)["wc"].total_seconds()
                date_run = get_wallclock_icon(
                    filename,
                    args.no_x,
                    num_ok=1,
                    success_message=success_message)["st"]
            else:
                wallclock, nnodes, date_run = set_default_error_slurm_file(
                    "Warning : Run did not finish properly")

            # get job number
            jobnumber = filename[-8:]
            print(jobnumber)
        elif args.mod.upper() == "ICON-HAM":
            # get # nodes and wallclock
            # infer nnodes from MPI-procs in ICON output
            nodes_line = grep("mo_mpi::start_mpi ICON: Globally run on",
                              filename)["line"][0]
            nnodes = int(nodes_line.split(' ')[6])

            nnodes = nnodes // args.cpu_per_node

            wallclock = get_wallclock_icon(filename, args.no_x,
                                           num_ok=0)["wc"].total_seconds()
            date_run = get_wallclock_icon(filename, args.no_x, num_ok=0)["st"]

            # get job number
            jobnumber = float(filename.split('.')[-2])

        # fill array in
        np_2print.append([nnodes, wallclock, jobnumber, date_run])

    # put data into dataframe
    perf_df = pd.DataFrame(
        columns=['N_Nodes', 'Wallclock', 'Jobnumber', 'Date'], data=np_2print)
    perf_sorted = perf_df.sort_values(by=['N_Nodes', 'Wallclock', 'Jobnumber'],
                                      ascending=[1, 0, 1])

    # wallclock in human reading form
    perf_sorted['Wallclock_hum'] = pd.to_datetime(
        perf_sorted["Wallclock"],
        unit='s').dt.strftime("%H:%M:%S")  #,format="%H-%M-%S")

    # reference line time
    ref_time = perf_sorted.iloc[iref]

    # compute speedup normed with N_Nodes of ref_time
    perf_sorted[
        'Speedup'] = ref_time.Wallclock / perf_sorted.Wallclock * ref_time.N_Nodes

    # compute efficiency
    perf_sorted['Efficiency'] = perf_sorted.Speedup * (
        1 / perf_sorted.N_Nodes) * 100.

    # compute number of node hours
    perf_sorted[
        'Node_hours'] = perf_sorted.N_Nodes * perf_sorted.Wallclock * nodesec_to_nodehours
    perf_sorted['NH_year'] = perf_sorted.Node_hours * args.factor_nh_year

    # write csv file
    filename_out = '%s/%s' % (path_out, args.outfilename)
    perf_sorted.to_csv(filename_out,
                       columns=[
                           'Date', 'Jobnumber', 'N_Nodes', 'Wallclock',
                           'Wallclock_hum', 'Speedup', 'Node_hours',
                           'Efficiency', 'NH_year'
                       ],
                       sep=';',
                       index=False,
                       float_format="%.2f")
