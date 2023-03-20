# Toolset to perform scaling analysis of ICON(-HAM), ECHAM(-HAM) and MPI-ESM(-HAM)

It has been tested on Piz Daint (CSCS) to produce the technical part of production projects at CSCS.
On Euler (ETHZ) only limited functionality is provided for the analysis of Icon.
See [Limitations on Euler](#limitations-on-euler) for more information.

Below is a description of each script and a recipe.

- Original devleopment: Colombe Siegenthaler (2020-01)
- Maintainted by Michael Jähn from 2021-03 on

## Recipe for scaling analysis with ECHAM/ICON-(HAM)

### 1. Configure and compile your model as usual.

### 2. Prepare your running script

Using conda, you can create your environment with:
    
```console
$ conda env create -f environment.yaml
```
    
To load your environment, simply type:
    
```console
$ conda env create -f environment.yaml
```

#### ICON
    
Prepare your machine-independent setting file "my_exp" (e.g. exp.atm_amip, without the '.run').

#### ECHAM
    
Prepare your setting file as usual with the jobscript toolkit:
    
```console
$ prepare_run -r [path_to_your_setting_folder] my_exp
```

### 3. Create and launch different running scripts based on my_exp, but using different numbers of nodes.

#### ICON
    
Use `send_several_run_ncpus_perf_ICON.py`.
For example for running `my_exp` on 1, 10, 12 and 16 nodes:
    
```console
$ python [path_to_scaling_analysis_tool]/send_several_run_ncpus_perf_ICON.py -e my_exp -n 1 10 12 15
```

With the command above, 4 running scripts will be created (`exp.my_exp_nnodes1.run`, `exp.my_exp_nnodes10.run`, 
`exp.my_exp_nnodes12.run` and `exp.my_exp_nnodes15.run`), and each of them will be launched.

To send several experiments on different node numbers at once, use: `send_analyse_different_exp_at_once_ICON.py`
form inside `<path_to_scaling_analysis_tool>`:
    
```console
$ python send_analyse_different_exp_at_once_ICON.py
```
    
The script `send_analyse_different_exp_at_once_ICON.py` (n_step = 1) is a wrapper which calls 
`send_several_run_ncpus_perf_ICON.py` for different experiments (for example different set-ups, or compilers).
    
The script `send_analyse_different_exp_at_once_ICON.py` (n_step = 2) is a wrapper which gets
the wallclocks from the log files for different experiments (for example different set-ups, or compilers) (point 4 of this README).

#### ECHAM
    
Use `send_several_run_ncpus_perf.py` which creates and sends several running scripts using the option -o of the jobsubm_echam script.
For example, sending the my_exp run on 1, 10, 12 and 15 nodes:
    
```console
$ python [path_to_scaling_analysis_tool]/send_several_run_ncpus_perf.py -b [path_to_echam-ham_folder]/my_experiments/my_exp -n 1 10 12 15
```

With the command above, 4 running folders will be created based on the running folder `my_exp`
(`my_exp_cpus12`, `my_exp_cpus120`, `my_exp_cpus144and my_exp_cpus180`), and each of them will be launched.

### 4. When all the runs are finished, read all the slurm/log files to get the Wallclock for each run, and put them into a table:

#### ICON
    
Use the option `-m icon`:
    
```console
$ python [path_to_scaling_analysis_tool]/create_scaling_table_per_exp.py -e my_exp -m icon
```
    
or for different experiments at once: `send_analyse_different_exp_at_once_ICON.py` (n_step = 2) (cf point 3)

#### ECHAM
    
Use the option `-m icon`
    
```console
$ python [path_to_scaling_analysis_tool]/create_scaling_table_per_exp.py -e my_exp -m echam-ham
```

For both model types, this creates a table `my_exp.csv`, which contains the wallclock, efficiency and NH for each run.

### 5. Create a summary plot and table of the variable you wish (Efficiency, NH, Wallclock) for different experiments with respect to the number of nodes.

If needed, you can define the line properties of each experiment in `def_exps_plot.py`.
    
```console
$ python [path_to_scaling_analysis_tool]/plot_perfs.py
```

## Limitations on Euler

* The scaling analysis tools were tested for Icon only.
* Because of differing nodes-architectures on Euler, the number of nodes passed via the -n option
corresponds to the number of Euler-cores.
* Parsing the logfiles only works using the --no_sys_report option.
* In order to have nice plots, the number of Euler-cores needs to be divided by 12.
* Automatic runtime-specification is not as smooth as on Daint -> a minimum of 20 min is requested in any case.

