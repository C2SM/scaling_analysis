#!/usr/bin/python

# Wrapper to send several ICON (-HAM) runs
# for performance anaylsis with different number of cpus
#
# This script uses the automatic running script generation in ICON (make_target_runscript).
#
# Usage : send_several_run_ncpus_perf_ICON.py -b $SCRATCH/icon-eniac/ -e my_exp -n 10 12 15
#
# C. Siegenthaler (C2SM) , July 2015
#
############################################################################################


import numpy as np
import os
import argparse
import datetime

def create_runscript(exp_base,output_postfix,nnodes,nproma=None):
    # name experiment
    exp_nnodes = "{}{}_nnodes{}".format(exp_base,output_postfix,nnodes)

    # create scripts
    if nproma is None:
        os.system("/bin/bash ./run/make_target_runscript in_folder=run in_script=exp.{} in_script=exec.iconrun out_script=exp.{}.run EXPNAME={} memory_model='large' omp_stacksize=200M grids_folder='/scratch/snx3000/colombsi/ICON_input/grids' no_of_nodes={}".format(exp_base,exp_nnodes,exp_nnodes,nnodes))
    else:
        os.system("/bin/bash ./run/make_target_runscript in_folder=run in_script=exp.{} in_script=exec.iconrun out_script=exp.{}.run EXPNAME={} memory_model='large' omp_stacksize=200M grids_folder='/scratch/snx3000/colombsi/ICON_input/grids' no_of_nodes={} nproma={}".format(exp_base,exp_nnodes,exp_nnodes,nnodes,nproma))
 
    #return name of exp
    return(exp_nnodes)

def define_and_submit_job(hostname,wallclocktime,path_to_newscript,nnodes,euler_node,account):


    # Daint login nodes
    if 'daint' in hostname:
        if account == None:
            # Use standard account
            account = os.popen('id -gn').read().split('\n')[0]
        submit_job = 'sbatch --time=%s --account=%s %s' %(wallclocktime,account,path_to_newscript)

    # Euler login nodes
    elif 'eu-login' in hostname:
        if euler_node == 7:
            submit_job = 'bsub -W %s -n %s -R "select[model==EPYC_7H12]" < %s' %(wallclocktime,nnodes,path_to_newscript)
        elif euler_node == 6:
            submit_job = 'bsub -W %s -n %s -R "select[model==EPYC_7742]" < %s' %(wallclocktime,nnodes,path_to_newscript)
        elif euler_node == 4:
            submit_job = 'bsub -W %s -n %s -R "select[model==XeonGold_6150]" -R "span[ptile=36]" < %s' %(wallclocktime,nnodes,path_to_newscript)
        else:
            print('Error: Please specify a correct Euler node (4,6 or 7).')
            exit(-1)
    

    print(submit_job)
    os.system(submit_job)
    print('--------------------------------------------------------------------------------------------------------')

if __name__ == "__main__":

    # parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--basis_folder_icon', '-b', dest = 'basis_folder',\
                            default = os.getcwd(),\
                            help='basis model folder e.g. /users/colombsi/icon-hammoz') 
    parser.add_argument('--exp_base', '-e', dest = 'exp_base',\
                            default = 'atm_amip_1month',\
                            help='basis model folder e.g. atm_amip_1month')
    parser.add_argument('--output_postfix', '-o', dest = 'output_postfix',\
                            default = '',\
                            help='postfix for the output name of the running scripts e.g. "_cray" will give exp.atm_amip_cray_nnodesX.run')
    parser.add_argument('--arrange_nnodes', '-a', dest = 'arrange_nnodes',\
                            default = [1,11,1],\
                            type = int,\
                            nargs = 3,\
                            help = 'list of number of nodes in the np.arrange format : [begining iteration, end iteration, step]. Default:[1,11,1] (=[1,2,3,4,5,6,7,8,9,10]')
    parser.add_argument('--nnodes', '-n', dest = 'nodes_to_proceed',\
                            default = [],\
                            type = int,\
                            nargs = '*',\
                            help = 'cups number of the simulation to analyse. This have priority over -arrange_nnodes')  
    parser.add_argument('--wallclock','-w', dest = 'wallclock' ,\
                            default = None,\
                            type = str,\
                            help = 'wallclock to use when sending the run to the batch system')    
    parser.add_argument('--nproma','-p', dest = 'nproma' ,\
                            default = None,\
                            type = int,\
                            help = 'value of nproma')    
    parser.add_argument('--oneNH','-NH', dest = 'oneNH' ,\
                            default = 24,\
                            type = int,\
                            help = 'estimation of one node hour (wallclock time in hour when running on 1 node). This will be used for estimating a wallclock to use. In case -w is set, oneNH is not used.')
    parser.add_argument('--euler-node','-m', dest = 'euler_node' ,\
                            default = 6,\
                            type = int,\
                            help = 'node type for Euler simulations')    
    parser.add_argument('--account','-A', dest = 'account' ,\
                            default = None,\
                            type = str,\
                            help = 'project account on Piz Daint')    

    args = parser.parse_args()

    hostname = os.uname()[1]

    # Daint login nodes
    if 'daint' in hostname:
        print('Host is Daint')

    # Euler login nodes
    elif 'eu-login' in hostname:
        print('Host is Euler')

    # unknown host
    else:
        print("Unknown host with hostname %s" %(hostname))
        exit(-1)

    # base experiment
    exp_base = args.exp_base

    # Euler node
    euler_node = args.euler_node

    # account
    account = args.account

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

    # define run dir
    path_run_dir = os.path.join(args.basis_folder,"run")

    # estimated time for one node
    one_node_hour = args.oneNH

    # nproma
    nproma = args.nproma

    # loop over number of nodes to create scripts
    for nnodes in args.nodes_to_proceed:

        # need to be in basis folder to have some function defined
        os.chdir(args.basis_folder) 

	# create the runscripts with the icon script creating tool 
        print ("Create runscript")
        new_script = create_runscript(exp_base,args.output_postfix,nnodes,nproma)
	
	# path to the newly created script (needed for launching it)
        path_to_newscript = os.path.join(path_run_dir,"exp.%s.run" %new_script)

        # need to be in run folder to have some function defined
        os.chdir(path_run_dir)

        wallclocktime = args.wallclock
        # roughly estimated time in sbatch format	
        if args.wallclock is None :
            seconds = datetime.timedelta(hours=np.float(one_node_hour)/nnodes).total_seconds()
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            if 'eu-login' in hostname:
                # ensure no -W 0:00 request
                if seconds < 1200:
                    minutes=20
                wallclocktime = "%02i:%02i" %(hours,minutes)
            else:
                wallclocktime = "%02i:%02i:00" %(hours,minutes)

                

        # submit machine-dependent job
        define_and_submit_job(hostname,wallclocktime,path_to_newscript,nnodes,euler_node,account)


