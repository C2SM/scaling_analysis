#!/usr/bin/python

# Read the .csv performance files and plot a figure with one line per exp.
# Merge all .csv files (one per exp) into one big file containing all exps
 
# Colombe Siegenthaler    C2SM (ETHZ) , 09.2108

import matplotlib.pyplot as plt
import pandas as pd
import os
import glob

import def_exps_plot as defexp

# path to the .csv files
path = '/Users/colombsi/Documents/CSCS/perfs/2019/perfs_per_config'

# files to include
#files_to_read = [defexp.atm_amip_6h, defexp.atm_amip_1m, defexp.e63_default_T63L47_6h, defexp.e63h23_T63L47_6h, defexp.e63h23_T63L47_1m, defexp.esm_ham_T63L47_1m]
#files_to_read = [defexp.atm_amip_6h, defexp.atm_amip_1m, defexp.atm_amip_1m_gcc]
files_to_read = []


var_to_plot = 'Efficiency'
name_plot = 'ICON'

lo_write_csv = False

#----------------------Begin of script-----------------------------------------------------------

# list of exp to plot not given, take all csv files in the folder 'path'
if len(files_to_read) == 0:
    csv_files = glob.glob(os.path.join(path,'*.csv'))

    files_to_read = [defexp.experiment(name = os.path.basename(fn).split('.csv')[0]) for fn in csv_files]



# Define figure
fig, ax = plt.subplots()

# Define global Dataframe for output
out_df = pd.DataFrame(columns=['N_Nodes'])

# for each file, read the dataframe and plot 
for exp in files_to_read:

    # path to the file
    abs_path = os.path.join(path,"{}.csv".format(exp.name))
 
    
    if exp.name.endswith('2017'):
        sep=','
    else:
        sep=';'
    dt = pd.read_csv(abs_path, sep=sep)

    # drop lines containing Nan
    dt.dropna(inplace=True)

    # remove the lines with identical number of nodes. Keep the shortest time
    dt.sort_values(by=['N_Nodes','Wallclock'], ascending = [1,0], inplace=True)   # reorder the dataframe by 1st number of nodes, and then descending wallcloks
                                                                                  # for a given # nodes, shorter wallclock will be the last line 
    dt.drop_duplicates(subset=['N_Nodes'], keep='last',inplace=True)  # remove line duplicates, keeps the last line

    # plot
    dt.plot(kind='line', x='N_Nodes', y=var_to_plot, ax=ax, **exp.line_appareance)

    # highlight the chosen config (only for efficiency)
    if var_to_plot == 'Efficiency' :
        best_n = exp.bestconf
        if best_n in dt.N_Nodes.values:
            perf_chosen = float(dt[dt.N_Nodes == best_n].Efficiency)
            ax.scatter(best_n, perf_chosen, s=150.,color='k')
        else:	
            print ("Warning, the number of nodes defined for the best configuration ({}) is not in the experiment definition".format(best_n))
            print ("The number of nodes in the csv files are: ")
            print("{}".format(dt.N_Nodes))
            print ("Not plotting the best configuration point")

    # Fill the out dataframe
    out_df = pd.merge(out_df, \
 	              dt[['N_Nodes','Efficiency']].rename(columns={'Efficiency': '{}'.format(exp.label)}), \
		      how='outer', on=['N_Nodes'])

    # cleaning
    del dt

# general plot properties 
ax.grid(color='grey', linestyle=':')
if var_to_plot == 'Efficiency':
    ax.set_ylim([40,115])
    ax.axhline(y=70,color='k')
if var_to_plot == 'Speedup':
    max_N = 40
    ax.plot([0,max_N],[0,max_N])
    ax.set_xlim([0,max_N])
    ax.set_ylim([0,max_N])

ax.set_xlabel('# Nodes')
ax.set_ylabel(var_to_plot) #'Efficiency [%]')
ax.legend()

# sort global dataframe
out_df.sort_values(by=['N_Nodes'], ascending = [1],inplace=True)

if len(name_plot) > 0:
     name_plot = '_{}'.format(name_plot)

# savefig
fig.savefig(os.path.join(path,'{}{}.pdf'.format(var_to_plot,name_plot)))

# write out global dataframe
if lo_write_csv:
    filename_out = os.path.join(path,'summary_performances_tot{}.csv'.format(name_plot))	
    out_df.to_csv(filename_out,sep=',', index=False, float_format="%.2f")
