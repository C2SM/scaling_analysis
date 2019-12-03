#!/usr/bin/python

# Read the .csv performance files and plot a figure with one line per exp.
# Merge all .csv files (one per exp) into one big file containing all exps
 
# Colombe Siegenthaler    C2SM (ETHZ) , 09.2108

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# path to the .csv files
path = '/Users/colombsi/Documents/CSCS/perfs/2018/perfs_per_config'

# definition of the object "experiment". It contains mostly teh potting properties 
class experiment:
     def __init__(self, name, label, color, symbol, linestyle, linewidth = 1., bestconf = np.nan):
         self.name = name
         self.label = label
         self.color = color
         self.symbol = symbol
         self.linestyle = linestyle
         self.linewidth = linewidth
         self.bestconf = bestconf

# Definition of each experiment properties (colors, labels,ect)
atm_amip_1m_old = experiment(name = 'atm_amip_1m_Sep2018', label = 'old ICON 1m', color = 'blue', symbol = 'o', linewidth = 0.5, linestyle = '--', bestconf = 22)
atm_amip_6h_old = experiment(name = 'atm_amip_6h_Sep2018', label = 'old ICON 6h', color = 'purple', symbol = 'o', linewidth = 0.5, linestyle = '--', bestconf = 20)
e63_default_T63L47_1m_old = experiment(name = 'e63_default_T63L47_1m_Sep2018', label = 'ECHAM 1m', color = 'orange', symbol = 's', linestyle = '-', bestconf = 17)
e63_default_T63L47_6h_old = experiment(name = 'e63_default_T63L47_6h_Sep2018', label = 'ECHAM 6h', color = 'orange', symbol = 's', linestyle = '--', bestconf = 8)
e63h23_T63L47_1m_2017_old = experiment(name = 'e63h23_T63L47_1m_2017', label = 'ECHAM-HAM 1m', color = 'red', symbol = 'd', linestyle = '-', bestconf = 34)
e63h23_T63L47_6h_2017 = experiment(name = 'e63h23_T63L47_6h_2017', label = 'ECHAM-HAM 6h', color = 'pink', symbol = 'd', linestyle = '--', bestconf = 16)
esm_ham_T63L47_1m_2017 = experiment(name = 'ESM-HAM-T63L47_1m_2017', label = 'MPI-ESM-HAM 1m', color = 'green', symbol = '*', linestyle = '-', bestconf = 36)

atm_amip_1m_gcc = experiment(name = 'atm_amip_1m_gcc', label = 'ICON gcc 1m', color = 'LightBlue', symbol = 'd', linestyle = '-')
atm_amip_1m = experiment(name = 'atm_amip_1m', label = 'ICON cray 1m', color = 'blue', symbol = 'o', linestyle = '-', bestconf = 34)
atm_amip_6h = experiment(name = 'atm_amip_6h', label = 'ICON cray 6h', color = 'purple', symbol = 'o', linestyle = '--', bestconf = 33)
e63_default_T63L47_6h = experiment(name = 'e63_6h', label = 'ECHAM 1m', color = 'orange', symbol = 's', linestyle = '-', bestconf = 10)
e63h23_T63L47_1m = experiment(name = 'e63ham_1m', label = 'ECHAM-HAM 1m', color = 'red', symbol = 'd', linestyle = '-', bestconf = 36)
e63h23_T63L47_6h = experiment(name = 'e63ham_6h', label = 'ECHAM-HAM 6h', color = 'pink', symbol = 'd', linestyle = '--', bestconf = 12)
esm_ham_T63L47_1m = experiment(name = 'mpiesm-ham_1m', label = 'MPI-ESM-HAM 1m', color = 'green', symbol = '*', linestyle = '-', bestconf = 48)

 
# files to include
#files_to_read = [atm_amip_6h, atm_amip_1m, e63_default_T63L47_6h, e63h23_T63L47_6h, e63h23_T63L47_1m, esm_ham_T63L47_1m]
files_to_read = [atm_amip_6h, atm_amip_1m, atm_amip_1m_gcc]

var_to_plot = 'Wallclock'
name_plot = 'ICON'

lo_write_csv = False

#----------------------Begin of script-----------------------------------------------------------

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
    dt.plot(kind='line', x='N_Nodes', y=var_to_plot, ax=ax, label=exp.label, color=exp.color, style=exp.linestyle, marker=exp.symbol, linewidth = exp.linewidth)

    # highlight the chosen config (only for efficiency)
    if var_to_plot == 'Efficiency' :
        best_n = exp.bestconf
        if best_n in dt.N_Nodes.values:
    	    perf_chosen = float(dt[dt.N_Nodes == best_n].Efficiency)
    	    ax.scatter(best_n, perf_chosen, s=150.,color='k')
        else:	
	    print ("Warning, the number of nodes defined for the best configuration ({}) is not in the csv file : {}.csv ".format(best_n,exp.name))  
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
