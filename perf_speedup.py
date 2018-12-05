#!/usr/bin/python
#
# Script to parse the slurm or echam6.log file to get the wallclock time, create a table containing wallclock time and associated speed-up
# mouve the files in project.
#
#
#Example : perf_speedup.py -basis_name  prf_echam61ham22_T63L47 -ncpus_incr 32 -niter 10
#
# C. Siegenthaler (C2SM) , July 2015
# C. Siegenthaler (C2SM): adaptation for ICON, November 2017
#
############################################################################################


import numpy as np
import os
import argparse
import glob
import shutil
import datetime
import itertools
import pandas as pd # need to load module load cray-python/2.7.15.1 PyExtensions/2.7.15.1-CrayGNU-18.08

if __name__ == "__main__":

    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-basis_name', dest = 'basis_name',\
                            help='basis name of the exp to anaylse.') 
    parser.add_argument('-arange_nodes', dest = 'arange_nodes',\
                            nargs = 3,\
                            type = int,\
                            help = 'nodes number to analyse.') 
    parser.add_argument('-nnodes', dest = 'nodes_to_proceed',\
                            default = [],\
                            type = int,\
                            nargs = '*',\
                            help = 'cups number of the simulation to analyse.This have priority over -ncpus_incr, -niter and -nbeg_iter')  
    parser.add_argument('-outfilename', dest = 'outfilename',\
                            default='',\
                            help='name of the ouput file') 

    parser.add_argument('-res', dest = 'res',\
                            default='',\
                            help='resolution(with ocean) eg T63L31GR15 ') 

    parser.add_argument('-mod', dest = 'mod',\
                            default='echam-ham',\
                            help='model type (echam-ham, icon)') 

    parser.add_argument('-cpu_per_node', dest = 'cpu_per_node',\
                        default = 12,\
                        type = int,\
                        help = 'numper of CPUs per node') 

    parser.add_argument('-no_sys_report', action='store_true',\
                        help = 'no time report provided by the system, per defualt, the wallclock will be taken from this report. If this option enabled, the wallclok will computed in a different way')                    

    args = parser.parse_args()

    # assume you are in teh directory where all experiment directories are
    path_exps_dir = os.getcwd()
    path_out = path_exps_dir

    # define files to analyse
    #----------------------------------------------------------------------

    l_cpus_def = False

    # 1st possibility: give nnodes to proceed
    if (len(args.nodes_to_proceed)>0):
        nodes_to_proceed = np.array(args.nodes_to_proceed)
        l_cpus_def = True

    # 2nd possiblity: give minmax and iteration on number of nodes 
    # set the list of experiment to proceed
    if (not l_cpus_def) and (args.arange_nodes is not None):
        nodes_to_proceed = np.arange(args.arange_nodes[0],args.arange_nodes[1],args.arange_nodes[2])
        l_cpus_def = True
    
    if l_cpus_def:
        if args.mod.upper() == "ICON" :
            slurm_files_ar = [glob.glob("{}/LOG.exp.{}_nnodes{}.run.*".format(path_exps_dir,args.basis_name,n)) for n in nodes_to_proceed]
            slurm_files = list(itertools.chain.from_iterable(slurm_files_ar))
        elif args.mod.upper() == "ECHAM-HAM":
            slurm_files_ar = [glob.glob("{}/{}_cpus{}/slurm*".format(path_exps_dir,args.basis_name,n*args.cpu_per_node)) for n in nodes_to_proceed]
            slurm_files = list(itertools.chain.from_iterable(slurm_files_ar))
                              
    # 3rd possibility : use all the slurm files containing the basis name
    if (not l_cpus_def):
        if args.mod.upper() == "ICON" :
            slurm_files = glob.glob("{}/LOG.exp.{}*.run.*".format(path_exps_dir,args.basis_name,args.basis_name))
        elif args.mod.upper() == "ECHAM-HAM":
            slurm_files = glob.glob("{}/{}*/slurm_{}*".format(path_exps_dir,args.basis_name,args.basis_name))
    

    # fill up array
    #-----------------------------------------------------------------------------------------------
#    if args.mod.upper() == "ICON" :
#        iref = 1
#    elif args.mod.upper() == "ECHAM-HAM":
    iref = 0 


    if args.outfilename == '':
        args.outfilename = '%s.csv' %args.basis_name

    # array for store values read in the slurm file
    np_2print = [] #np.zeros([len(slurm_files),4]) 
    
    
    # dictionary containing the indices of the variables in the array np_2print
    dict_ind = {'Wallclock' : 1, 'CET' : 1}  
             
    # conversion from cpu-sec to node-hours
    nodesec_to_nodehours = 1./3600.
               
    
    # performs the analysis (create a csv file)   
    ilin = 0

    def grep(string,filename):
        # returns lines of file_name where string appears
        # mimic the "grep" function 
        
        # list of lines where string is found
        list_line = []
        list_iline = []
     
        for iline,line in enumerate(open(filename)):
            if string in line:
                list_line.append(line)
                list_iline.append(iline)
        
        return {"iline" : list_iline, "line" : list_line}
    
    def get_wallclock_icon(filename):
       
        OK_streams = grep('Script run successfully:  OK',filename)["line"]
   
        if len(OK_streams) > 1 :
            time_grep = grep('CEST',filename)["line"]
            time_arr = [datetime.datetime.strptime(s.strip(), '%a %b %d %H:%M:%S CEST %Y') for s in time_grep]

            wallclock = time_arr[-1] - time_arr[0] 
        else:
            print ("file {} did not finish properly".format(filename))
            print ("Set Wallclock = 0")
            wallclock = datetime.timedelta(0)
    
        return {"wc" : wallclock, "st": time_arr[0]} 
    
    def get_wallclock_Nnodes_gen_daint(filename, string_sys_report="Elapsed"):

        # Find report
        summary_in_file = grep(string_sys_report, filename)
        summary_line = summary_in_file["line"][0]
        summary_iline = summary_in_file["iline"][0]

        if len(summary_line) > 0 :
	    f = open(filename)
            lines =f.readlines()

            #find index of "start" and "end" in the report line 
            line_labels = [s.strip() for s in summary_line.split()]
            ind_start = line_labels.index('Start')
            ind_end = line_labels.index('End')
            
            line_time = [lines[summary_iline+2].split()[i] for i in [ind_start,ind_end]]
            time_arr = [datetime.datetime.strptime(s.strip(), '%Y-%m-%dT%H:%M:%S') for s in line_time]
            wallclock = time_arr[-1] - time_arr[0] 
            
            # Nnodes
            line_labels_n = [s.strip() for s in lines[summary_iline+4].split()]
            ind_nodes = line_labels_n.index('NNodes')
            nodes = int(lines[summary_iline+6].split()[ind_nodes])

            f.close()
        else:
            print ("Warning : file {} did not finish properly or the word {} is not found".format(filename, string_sys_report))
            print ("Set Wallclock = 0 , and nodes = 100")
            wallclock = 0.
            nodes = 100

        return {"n" : nodes, "wc" : wallclock, "st": time_arr[0]}

    # security. If not file found, exit	
    if len(slurm_files) == 0 :
	print("No slurm file founded with this basis name")
	print ("Exiting")
        exit()

    # loop over number of cpus to be lauched
    for filename in slurm_files:

        print("Read file : {}".format(os.path.basename(filename)))
        # read nnodes and wallclock from file
        if args.mod.upper() == "ICON" :
         
            # get # nodes and wallclock
            if args.no_sys_report:
                nodes_line = grep("no_of_nodes=",filename)["line"][0]
                nnodes = int(nodes_line.split('=')[1].split()[0].strip())
   
                wallclock = get_wallclock_icon(filename)["wc"].total_seconds()
		date_run = get_wallclock_icon(filename)["st"]
            else:
                nnodes = get_wallclock_Nnodes_gen_daint(filename)["n"]
                wallclock = get_wallclock_Nnodes_gen_daint(filename)["wc"].total_seconds()
		date_run = get_wallclock_Nnodes_gen_daint(filename)["st"]

            # get job number
            jobnumber = float(filename.split('.')[-2])

        elif args.mod.upper() == "ECHAM-HAM":
            ncpus_line = grep("Total number of PEs",filename)["line"][0]
            ncpus = int(ncpus_line.split(':')[1].split()[0].strip())
            nnodes = ncpus/float(args.cpu_per_node)

            wallclock_line = grep("Wallclock",filename)["line"][0]
            wallclock = float(wallclock_line.split(':')[1].strip()[:-1])
	   
            # to do: get date of teh run from slurm file 
	    date_run = datetime.datetime(1900,01,01) 

            jobnumber = float (filename.replace('_','.').split('.')[-2])

        # fill array in
        # number of nodes
       # np_2print[ilin,0] = nnodes
        np_2print.append([nnodes,wallclock,jobnumber,date_run])

        # wallclock
        #np_2print[ilin,1] = wallclock
    
	# jobnumber
	#np_2print[ilin,2] = jobnumber       

        # date of the run
	#np_2print[ilin,3] = date_run

	#ilin += 1

    # put data into dataframe
    perf_df = pd.DataFrame(columns=['N_Nodes','Wallclock','Jobnumber','Date'],data=np_2print)
    perf_sorted = perf_df.sort_values(by=['N_Nodes','Wallclock','Jobnumber'], ascending = [1,0,1]) 
    # reference line time
    ref_time = perf_sorted.iloc[iref]

    # compute speedup
    perf_sorted['Speedup'] = ref_time.Wallclock/perf_sorted.Wallclock

    # compute efficiency
    perf_sorted['Efficiency'] = perf_sorted.Speedup * (ref_time.N_Nodes/perf_sorted.N_Nodes)*100.

    # compute number of node hours
    perf_sorted['Node_hours'] = perf_sorted.N_Nodes * perf_sorted.Wallclock * nodesec_to_nodehours
    perf_sorted['NH_year'] = perf_sorted.Node_hours * 12 
    

    #ilin += 1


    filename_out = '%s/%s' %(path_out,args.outfilename)
    perf_sorted.to_csv(filename_out, columns=['Date','Jobnumber','N_Nodes','Wallclock','Speedup','Node_hours','Efficiency','NH_year'],sep=';', index=False, float_format="%.2f")



################################################################################



