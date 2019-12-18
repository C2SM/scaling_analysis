#!/usr/bin/python

# Read the .csv performance files and plot a figure with one line per exp.
# Merge all .csv files (one per exp) into one big file containing all exps
 
# Colombe Siegenthaler    C2SM (ETHZ) , 09.2108

import matplotlib.pyplot as plt
import pandas as pd
import os
import glob
import numpy as np

import def_exps_plot as defexp

# path to the .csv files
path = '/Users/colombsi/Documents/CSCS/perfs/2019/perfs_per_config'

# files to include
# ECHAM/MPI_ESM
#files_to_read = [defexp.e63h23_T63L47_1m, defexp.esm_ham_T63L47_1m]

# all ICONs, all compils
#files_to_read = [defexp.iconham_gcc,
#                 defexp.icon_amip_1m_cray,defexp.icon_amip_1m_intel,defexp.icon_amip_1m_gcc,
#                 defexp.icon_amip_6h_cray,defexp.icon_amip_6h_intel,defexp.icon_amip_6h_gcc]

# all ICON-LAM
#files_to_read = [defexp.icon_lam_cray,defexp.icon_lam_intel] #defexp.icon_lam_gcc,

# ICON-LAM init
#files_to_read =  [defexp.icon_lam_init_cray,defexp.icon_lam_init_intel,defexp.icon_lam_init_gcc]

# ICON, best config
#files_to_read = [defexp.iconham_gcc, defexp.icon_amip_6h_intel, defexp.icon_amip_1m_intel,defexp.icon_lam_cray]

# all mods, best config
files_to_read = [defexp.iconham_gcc, defexp.icon_amip_6h_intel, defexp.icon_amip_1m_intel,defexp.icon_lam_cray, defexp.e63h23_T63L47_1m, defexp.esm_ham_T63L47_1m]

# all files in folder
#files_to_read = []


var_to_plot = 'Efficiency'
name_plot = 'all-mods'

lo_wc_min = True       # transform Wallclock in minutes
lo_write_csv = True    # write csv file of data in the plot
lo_best_conf = False   # pllot the best configuration on Efficiency plot

#----------------------Begin of script-----------------------------------------------------------

# list of exp to plot not given, take all csv files in the folder 'path'
if len(files_to_read) == 0:
    csv_files = glob.glob(os.path.join(path,'*.csv'))

    files_to_read = [defexp.experiment(name = os.path.basename(fn).split('.csv')[0],marker='o') for fn in csv_files]

# define possible units
unit = {'Wallclock' : 'seconds', 'Efficiency' : '%'}
if lo_wc_min:
    unit['Wallclock'] = 'minutes'

# Define figure
fig, ax = plt.subplots()

# Define global Dataframe for output
out_df = pd.DataFrame(columns=['N_Nodes'])

# for each file, read the dataframe and plot 
for exp in files_to_read:

    # path to the file
    abs_path = os.path.join(path,"{}.csv".format(exp.name))

    if not os.path.isfile((abs_path)):
        print('Warning: File does not exist : {}'.format(abs_path))
    
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

    if var_to_plot == 'Wallclock' and lo_wc_min:
        dt['Wallclock'] = dt['Wallclock']/60.

    # plot
    dt.plot(kind='line', x='N_Nodes', y=var_to_plot, ax=ax,label=exp.label, **exp.line_appareance)

    # highlight the chosen config (only for efficiency)
    if var_to_plot == 'Efficiency' and lo_best_conf :
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
 	              dt[['N_Nodes',var_to_plot]].rename(columns={var_to_plot: '{}'.format(exp.label)}), \
		      how='outer', on=['N_Nodes'])

    # cleaning
    del dt

# general plot properties 
ax.grid(color='grey', which='both',linestyle=':')

# x-axis
min_N = 0
max_N = max(out_df.N_Nodes)
#max_N = 50
ax.set_xlim([min_N,max_N])
ax.set_xticks(np.arange(min_N, max_N, step=5),minor=True)
ax.set_xlabel('# Nodes')
#ax.set_ylim([0,70])

#y-axis
if var_to_plot == 'Efficiency':
    ax.set_ylim([20,110])
    ax.axhline(y=70,color='k')

if var_to_plot == 'Speedup':
    ax.plot([0,max_N],[0,max_N])
    ax.set_ylim([0,max_N])

# y label
ylab = var_to_plot
if var_to_plot in unit.keys():
    ylab = '{} [{}]'.format(ylab,unit[var_to_plot])
ax.set_ylabel(ylab)

ax.legend()

# sort global dataframe
out_df.sort_values(by=['N_Nodes'], ascending = [1],inplace=True)

if len(name_plot) > 0:
     name_plot = '_{}'.format(name_plot)

# savefig
fig.savefig(os.path.join(path,'{}{}.pdf'.format(var_to_plot,name_plot)))

# write out global dataframe
if lo_write_csv:
    filename_out = os.path.join(path,'summary_{}_tot{}.csv'.format(var_to_plot,name_plot))
    out_df.to_csv(filename_out,sep=';', index=False, float_format="%.2f")
