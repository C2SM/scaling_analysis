#!/usr/bin/python

# Wrapper to send several runs using the jobscriptoolkit
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
import argparse
import datetime

def create_runscript(exp_base,nnodes):
    # name experiment
    exp_nnodes = "%s_nnodes%i" %(exp_base,nnodes)

    # create scripts
    os.system("./config/make_target_runscript in_folder=run in_script=exp.%s in_script=exec.iconrun out_script=exp.%s.run EXPNAME=%s memory_model='large' omp_stacksize=200M grids_folder='/scratch/snx3000/colombsi/ICON_input/grids' no_of_nodes=%i" %(exp_base,exp_nnodes,exp_nnodes,nnodes))

    #return name of exp
    return(exp_nnodes)

if __name__ == "__main__":

    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-basis_folder_icon', dest = 'basis_folder',\
                            default = os.getcwd(),\
                            help='basis model folder e.g. /users/colombsi/icon-hammoz') 
    parser.add_argument('-exp_base', dest = 'exp_base',\
                            default = 'atm_amip_1month',\
                            help='basis model folder e.g. atm_amip_1month')
    parser.add_argument('-arrange_nnodes', dest = 'arrange_nnodes',\
                            default = [1,11,1],\
                            type = int,\
                            nargs = 3,\
                            help = 'list of number of nodes in the np.arrange format : [begining iteration, end iteration, step]. Default:[1,11,1] (=[1,2,3,4,5,6,7,8,9,10]')
    parser.add_argument('-nnodes', dest = 'nodes_to_proceed',\
                            default = [],\
                            type = int,\
                            nargs = '*',\
                            help = 'cups number of the simulation to analyse. This have priority over -arrange_nnodes')  
    
    args = parser.parse_args()

    # base experiment
    exp_base = args.exp_base

    if len(args.nodes_to_proceed) == 0 :
        args.nodes_to_proceed = np.arange(args.arrange_nnodes[0],args.arrange_nnodes[1],args.arrange_nnodes[2])
    
    # change directory to be in the basis folder
    if os.path.isdir(args.basis_folder):   
        os.chdir(args.basis_folder)
    else:
	print ("The following basis direcotory does not exist :%s" %args.basis_folder)
	print ("Please give an existing directory with the option -basis_folder_icon")
	print ("Exiting")
	exit(-1)    

    #define run dir
    path_run_dir = os.path.join(args.basis_folder,"run")

    # estimated time for one node
    one_node_hour = 24

    # loop over number of nodes to create scripts
    for nnodes in args.nodes_to_proceed:

        # need to be in basis folder to have some function defined
        os.chdir(args.basis_folder) 

	# create the runscripts with the icon script creating tool 
        print ("Create runscript")
	new_script = create_runscript(exp_base,nnodes)
	
	# path to the newly created script (needed for launching it)
	path_to_newscript = os.path.join(path_run_dir,"exp.%s.run" %new_script)

        # need to be in run folder to have some function defined
        os.chdir(path_run_dir)

	# roughly estimated time in sbatch format	
        seconds = datetime.timedelta(hours=np.float(one_node_hour)/nnodes).total_seconds()
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        wallclocktime = "%02i:%02i:00" %(hours,minutes)

        # job definition and submission
        print ('sbatch --time=%s %s' %(wallclocktime,path_to_newscript))
        os.system('sbatch --time=%s %s' %(wallclocktime,path_to_newscript))
        print('--------------------------------------------------------------------------------------------------------')
