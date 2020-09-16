Tool-set to perform scaling analysis of ICON(-HAM) , ECHAM(-HAM) and MPI-ESM(-HAM).

It has been tested on Piz daint (CSCS) to produce the technical p
art of production projects at CSCS.
On Euler (ETHZ) only limited functionality is provided for the analysis of Icon.
See "limitations on Euler" for more information.

Below is a description of each script and a recipe.

C. Siegenthaler 2020-01

---------------------------------------------------------------
Recipe for scaling analysis with ECHAM/ICON-(HAM)
---------------------------------------------------------------
---------------------------------------------------------------
1) Configure and Compile your model as usual.

2) Prepare your running script
If you are on Piz Daint (CSCS), you need to load the following modules before using the python scripts:
module load cray-python PyExtensions python_virtualenv
You might need to construct a virtual environment if some packages are missing (http://usertest.cscs.ch/tools/interactive/python/ )

* ICON :
i) Prepare your machine-independent setting file "my_exp" (e.g. exp.atm_amip, without the '.run').

* ECHAM :
i) Prepare your setting file as usual with the jobscript toolkit
> prepare_run -r [path_to_your_setting_folder] my_exp

3) Create and launch different running scripts based on my_exp, but using different numbers of nodes.

* ICON
Use send_several_run_ncpus_perf_ICON.py.
For example for running "my_exp" on 1, 10,12 and 16 nodes:
> python [path_to_scaling_analysis_tool]/send_several_run_ncpus_perf_ICON.py -e my_exp -n 1 10 12 15

With the command above, 4 running scripts will be created (exp.my_exp_nnodes1.run, exp.my_exp_nnodes10.run, exp.my_exp_nnodes12.run and exp.my_exp_nnodes15.run), and each of them will be launched.

To send several experiments on different node numbers at once, use: send_analyse_different_exp_at_once_ICON.py form inside path_to_scaling_analysis_tool :
> python send_analyse_different_exp_at_once_ICON.py
The script send_analyse_different_exp_at_once_ICON.py (n_step = 1) is a wrapper which calls send_several_run_ncpus_perf_ICON.py for different experiments (for example different set-ups, or compilers).
The script send_analyse_different_exp_at_once_ICON.py (n_step = 2) is a wrapper which get the wallclocks from the log files for different experiments (for example different set-ups, or compilers) (point 4 of this README).

* ECHAM
Use send_several_run_ncpus_perf.py which create and send several running scripts using the option -o of the jobsubm_echam script.
For example, sending the my_exp run on 1, 10, 12 and 15 nodes:
> python [path_to_scaling_analysis_tool]/send_several_run_ncpus_perf.py -b [path_to_echam-ham_folder]/my_experiments/my_exp -n 1 10 12 15

With the command above, 4 running folder will be created based on the running folder my_exp (my_exp_cpus12, my_exp_cpus120, my_exp_cpus144and my_exp_cpus180), and each of them will be launched.

4) When all the runs are finished, read all the slurm/log files to get the Wallclock for each run, and put them in a table:
> module load PyExtensions

* ICON
Use the option -m icon
> python [path_to_scaling_analysis_tool]/create_scaling_table_per_exp.py -e my_exp -m icon
or for different experiments at once : send_analyse_different_exp_at_once_ICON.py (n_step = 2) (cf point 3)

* ECHAM
Use the option -m icon
> python [path_to_scaling_analysis_tool]/create_scaling_table_per_exp.py -e my_exp -m echam-ham

For both model type, this creates a table my_exp.csv which contains the wallclock , efficiency and NH for each run.
Caution, for using this script, the module PyExtensions needs to be loaded.

5) Create a summary plot and table of the variable you wish (Efficiency, NH, Wallclock) for different experiments with respect to number of node.
If needed you can define the line properties of each experiment in def_exps_plot.py.
> plot_perfs.py

---------------------------------------------------------------
Recipe for use of Craypat analysis tool with ICON-(HAM)
---------------------------------------------------------------

1) According to CSCS, for getting the Craypat analysis tool work on daint, you should just load it (module load perftools-lite) before compiling the model.
However, loading perftools-lite before configuration of ICON leads to a crash at configuration, so adding the module perftools-lite directly to the modules to load in config/mh-linux is not working.

Thus, you have to configure normally without perftools-lite loaded and, after configuration is done:
- load perftools-lite, and
- add manually 'perftools-lite' to the modules to load (variable load_modules, resp. use_load_module) in both 1) scripts 'build_command' and 2)'config/set-up.info'.
Both of scripts 'build_command' and 'config/set-up.info' are actually written at the configuration.

steps to do:
> ./configure --with-fortran=[compiler you choose]
> module load perftools-lite
> add manually perftools-lite in 'build_command' and 'config/set-up.info'

2) Compile the model
>./build_command

3) Construct and launch the script of your experiment as usual.
The Craypat analysis tool creates a folder in the running directory called [model_used]+[some_numbers], for example echam6+6303-2417s, mpiom.x+6303-2417s, icon+1226-3277s.
> ./make_runscripts my_exp
> adjust the number of nodes if needed in my_exp.run
> sbatch my_exp.run

-----------------------------------------------------------------------------------------------
Recipe for use of Craypat analysis tool with ECHAM-(HAM)
-----------------------------------------------------------------------------------------------
For ECHAM and MPI-ESM, loading the Craypat analysis tool before configuration works. You only need to first load the module 'perftools-lite', and configure, compile and run the model as usual.

1) Load the modules
> module load perftools-lite

2) compile and configure
> conf_echam
> make

3) Construct and launch the script of your experiment as usual using the jobscript-toolkit.
> prepare_run.sh my_exp
> jobsubm my_exp
The Craypat analysis tool creates a folder in the running directory called [model_used]+[some_numbers], for example echam6+6303-2417s, mpiom.x+6303-2417s, icon+1226-3277s.
For MPIE-ESM, we get 2 Craypat folders.

-----------------------------------------------------------------------------------------------
Recipe for extracting the needed variables produced by the Craypat analysis tool (ECHAM/ICON-(HAM))
-----------------------------------------------------------------------------------------------
This recipe follows the Section 'Recipe for use of Craypat analysis tool with ICON-(HAM)' or 'Recipe for use of Craypat analysis tool with ECHAM-(HAM)' above.

4) Once the runs (with Craypat analysis tool loaded) are finished, create a folder for all the craypat analysis files you want to share with CSCS, for example (craypat_analysis_files).
In the new folder craypat_analysis_files, define a folder per experiment and put there the folder created by the Craypat analysis tool, the slurm/log file, setting file, etc.

> mkdir [path_to_folder_to_share_with CSCS]/craypat_analysis_files

Below is the arboretum I used:
craypat_analysis_files
    |_ECHAM-HAM
        |_e63h23_default_T63L47_1m_craypat
            |_echam6+3487-2377s
            |_slurm_e63h23_default_T63L47_1m_craypat_9805235.txt
            |_settings-e63h23_default_T63L47_1m_craypat
    |_ICON
        |_icon_amip_r2b4_intel_1m_craypat
            |_exp.atm_amip_intel_1m
            |_exp.atm_amip_intel_1m.run
            |_icon+7994-2051s
            |_LOG.exp.atm_amip_intel_1m.run.18772778.
        |_icon_amip_r2b4_intel_6h_craypat
    |_ICON-HAM
        |_[...]
    |_ICON-LAM
        |_[...]
    |_MPI-ESM-HAM
        |_mpiesm12ham_1m_craypat/
            |_echam6+12078-3101s
            |_mpiom.x+12078-3101s
            |_settings_BM_MPI-ESM-1-2-HAM
            |_slurm_BM_MPI-ESM-1-2-HAM.1_9705235.txt

The folder 'craypat_analysis_files' containing all the Craypat analysis files will be shared with CSCS within the additional documentation folder.

5) In the folder created by the the Craypat analysis tool, a summary file is produced : [model_used]+[some_numbers]/rpt-files/RUNTIME.rpt
For the written technical report, some key variables from these summary file are needed.
For knowing which variables to extract, please read: https://user.cscs.ch/access/report/

The script 'parse_craypat.py' produces a (very) short summary from the Craypat analysis tool's summary for each experiment, and put all teh summaries for each experiment together to put into the report.
> cd craypat_analysis_files
> python [path_to_scaling_analysis_tool]/parse_craypat.py

This creates the file ./Craypat_table.csv which contains the variables asked by CSCS for the technical report for each experiment.
Caution, for using this script, the module PyExtensions needs to be loaded.

-----------------------------------------------------------------------------------------------
Limitations on Euler
-----------------------------------------------------------------------------------------------
  * The scaling analysis tools were tested for Icon only.
  * Because of differing nodes-architectures on Euler, the number of nodes passed via the -n option
corresponds to the number of Euler-cores.
  * Parsing the logfiles only works using the --no_sys_report option.
  * In order to have nice plots, the number of Euler-cores needs to be divided by 12.
  * Automatic runtime-specification is not as smooth as on Daint -> a minimum of 20 min is requested in any case.

