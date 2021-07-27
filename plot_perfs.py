#!/usr/bin/python

#figure with one line per exp.
# Merge all .csv files (one per exp) into one big file containing all exps
# By defauylt, all the csv files present in 'path' are used. The definition if the plotting properties of each experiment is in defined in 'def_exps_plot.py'.
 
# Colombe Siegenthaler    C2SM (ETHZ) , 09.2108

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages  # tiple pages in pdf
import pandas as pd
import os
import glob
import numpy as np

import def_exps_plot as defexp

# path to the .csv files
path = os.getcwd()

# files to include

# all ICONs, all compils
files_to_read = [defexp.atm_amip_gcc_O1,defexp.atm_amip_gcc_O2,defexp.atm_amip_gcc_O3,
                 defexp.atm_amip_pgi_O1,defexp.atm_amip_pgi_O2,defexp.atm_amip_pgi_O3,
                 ]

# all files in folder
#files_to_read = []

variables = ['Efficiency','Wallclock','Speedup','NH_year']
version = '2.6.3.0'
machine = 'euler' # daint
name_plot = 'ICON-AMIP-' + machine.upper()  + '-' + version
title = 'ICON ' + version
if machine == 'euler':
    xlabel = '# Cores'
else:
    xlabel = '# Nodes'

lo_wc_min = True       # transform Wallclock in minutes
lo_write_csv = True    # write csv file of data in the plot
lo_savefig = True
lo_best_conf = True    # plot the best configuration on Efficiency plot
lo_zoom_wc = False

# x-axis lim
min_N = None
max_N = None
#----------------------Begin of script-----------------------------------------------------------

# list of exp to plot not given, take all csv files in the folder 'path'
if len(files_to_read) == 0:
    csv_files = glob.glob(os.path.join(path,'*.csv'))

    files_to_read = [defexp.experiment(name = os.path.basename(fn).split('.csv')[0],marker='o') for fn in csv_files]

# define possible units
unit = {'Wallclock' : 'seconds', 'Efficiency' : '%'}
if lo_wc_min:
    unit['Wallclock'] = 'minutes'

# filename
if lo_zoom_wc:
    name_plot += '_zoom'

# Define figure
fig, ax = plt.subplots()

# Define global Dataframe for output
out_df = pd.DataFrame(columns=['N_Nodes'])

# open multipage pdf
if lo_savefig:
    pp = PdfPages(os.path.join(path,'{}.pdf'.format(name_plot)))

for var_to_plot in variables :

    print('Plot variable {}'.format(var_to_plot))

    fig, ax = plt.subplots()
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
        dt.plot(kind='line', x='N_Nodes', y=var_to_plot, ax=ax,label=exp.label, title=title+', '+var_to_plot, **exp.line_appareance)

        # highlight the chosen config (only for efficiency)
        if var_to_plot == 'Efficiency' and lo_best_conf :
            best_n = exp.bestconf
            if best_n in dt.N_Nodes.values:
                perf_chosen = float(dt[dt.N_Nodes == best_n].Efficiency)
                ax.scatter(best_n, perf_chosen, s=80.,color='k')
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
    if min_N is None :
        min_N = 0
    if max_N is None:
        max_N = max(out_df.N_Nodes)
    ax.set_xlim([min_N,max_N])
    ax.set_xticks(np.arange(min_N, max_N, step=5),minor=True)
    ax.set_xlabel(xlabel)
    if lo_zoom_wc:
        ax.set_ylim([0,7])

    #y-axis
    if var_to_plot == 'Efficiency':
        ax.set_ylim([20,120])
        ax.axhline(y=70,color='k')

    if var_to_plot == 'Speedup':
        ax.plot([0,max_N],[0,max_N], color='black')
        ax.set_ylim([0,max_N])
    #ax.set_ylim([10,45])

    # y label
    ylab = var_to_plot
    if var_to_plot in unit.keys():
        ylab = '{} [{}]'.format(ylab,unit[var_to_plot])
    ax.set_ylabel(ylab)

    ax.legend()

    # sort global dataframe
    out_df.sort_values(by=['N_Nodes'], ascending = [1],inplace=True)

    # write out global dataframe
    if lo_write_csv:
        filename_out = os.path.join(path,'summary_{}_tot_{}.csv'.format(var_to_plot,name_plot))
        out_df.to_csv(filename_out,sep=';', index=False, float_format="%.2f")

    if lo_savefig :
        pp.savefig()

if lo_savefig:
    pp.close()
