#!/usr/bin/python

#figure with one line per exp.
# Merge all .csv files (one per exp) into one big file containing all exps
# By defauylt, all the csv files present in 'path' are used. The definition if the plotting properties of each experiment is in defined in 'def_exps_plot.py'.

# Colombe Siegenthaler    C2SM (ETHZ) , 09.2018
# Michael Jähn            C2SM (ETHZ) , 09.2021

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages  # tiple pages in pdf
import pandas as pd
import os
import glob
import numpy as np
import socket
import argparse

import def_exps_plot as defexp

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--minN',
                        '-miN',
                        dest='min_N',
                        default=0,
                        type=int,
                        help='minimum number of nodes')
    parser.add_argument('--maxN',
                        '-maN',
                        dest='max_N',
                        default=None,
                        type=int,
                        help='maximum number of nodes')
    parser.add_argument('--xtick',
                        '-x',
                        dest='xticks',
                        type=int,
                        help='number of ticks on x axis')
    parser.add_argument('--title',
                        '-t',
                        dest='title',
                        default='Scaling plot',
                        help='title')
    parser.add_argument('--name',
                        '-n',
                        dest='name_plot',
                        default='scaling_plot',
                        help='name of plot')
    args = parser.parse_args()

    # Path to the .csv files
    path = os.getcwd()

    #Check host
    host = socket.gethostname()
    var = dir(defexp)  #Get all classes of defexp
    if 'eu' in host:
        experiments = [x for x in var if x.startswith('euler')]
        xlabel = '# Cores'
    elif 'daint' in host:
        experiments = [x for x in var if x.startswith('daint')]
        xlabel = '# Nodes'
    else:
        raise Exception('Unknown host')

    variables = ['Efficiency', 'Wallclock', 'Speedup', 'NH_year']

    lo_wc_min = True  # transform Wallclock in minutes
    lo_write_csv = True  # write csv file of data in the plot
    lo_savefig = True
    lo_best_conf = True  # plot the best configuration on Efficiency plot
    lo_zoom_wc = False

    #----------------------Begin of script-----------------------------------------------------------

    # list of exp to plot not given, take all csv files in the folder 'path'
    if len(experiments) == 0:
        csv_files = glob.glob(os.path.join(path, '*.csv'))
        experiments = [
            defexp.experiment(name=os.path.basename(fn).split('.csv')[0],
                              marker='o') for fn in csv_files
        ]

    # define possible units
    unit = {'Wallclock': 'seconds', 'Efficiency': '%'}
    if lo_wc_min:
        unit['Wallclock'] = 'minutes'

    # filename
    if lo_zoom_wc:
        args.name_plot += '_zoom'

    # Define figure
    fig, ax = plt.subplots()

    # open multipage pdf
    if lo_savefig:
        pp = PdfPages(os.path.join(path, '{}.pdf'.format(args.name_plot)))

    for var_to_plot in variables:
        # Define global Dataframe (per variable) for output
        out_df = pd.DataFrame(columns=['N_Nodes'])


        print('Plot variable {}'.format(var_to_plot))

        fig, ax = plt.subplots()
        # for each file, read the dataframe and plot
        for exp_name in experiments:
            if isinstance(exp_name, str):
                exp = getattr(defexp, exp_name)
            # path to the file
            abs_path = os.path.join(path, "{}.csv".format(exp.name))

            if not os.path.isfile((abs_path)):
                print('Warning: File does not exist : {}'.format(abs_path))

            if exp.name.endswith('2017'):
                sep = ','
            else:
                sep = ';'
            dt = pd.read_csv(abs_path, sep=sep)

            # drop lines containing Nan
            dt.dropna(inplace=True)

            # remove the lines with identical number of nodes. Keep the shortest time
            dt.sort_values(
                by=['N_Nodes', 'Wallclock'], ascending=[1, 0], inplace=True
            )  # reorder the dataframe by 1st number of nodes, and then descending wallcloks
            # for a given # nodes, shorter wallclock will be the last line
            dt.drop_duplicates(
                subset=['N_Nodes'], keep='last',
                inplace=True)  # remove line duplicates, keeps the last line

            if var_to_plot == 'Wallclock' and lo_wc_min:
                dt['Wallclock'] = dt['Wallclock'] / 60.

            # plot
            dt.plot(kind='line',
                    x='N_Nodes',
                    y=var_to_plot,
                    ax=ax,
                    label=exp.label,
                    title=args.title + ', ' + var_to_plot,
                    **exp.line_appareance)

            # highlight the chosen config for all plots
            if lo_best_conf:
                best_n = exp.bestconf
                if best_n in dt.N_Nodes.values:
                    if var_to_plot == 'Efficiency':
                        perf_chosen = float(
                            dt[dt.N_Nodes == best_n].Efficiency)
                    if var_to_plot == 'Wallclock':
                        perf_chosen = float(dt[dt.N_Nodes == best_n].Wallclock)
                    if var_to_plot == 'Speedup':
                        perf_chosen = float(dt[dt.N_Nodes == best_n].Speedup)
                    if var_to_plot == 'NH_year':
                        perf_chosen = float(dt[dt.N_Nodes == best_n].NH_year)
                    ax.scatter(best_n,
                               perf_chosen,
                               s=120.,
                               alpha=0.7,
                               color=exp.line_appareance['color'],
                               edgecolor='k')
                else:
                    print(
                        "Warning, the number of nodes defined for the best configuration ({}) is not in the experiment definition"
                        .format(best_n))
                    print("The number of nodes in the csv files are: ")
                    print("{}".format(dt.N_Nodes))
                    print("Not plotting the best configuration point")

            # Fill the out dataframe
            out_df = pd.merge(out_df, \
                          dt[['N_Nodes',var_to_plot]].rename(columns={var_to_plot: f'{exp.label}_{var_to_plot}'}), \
                      how='outer', on=['N_Nodes'])

            # cleaning
            del dt

        # general plot properties
        ax.grid(color='grey', which='both', linestyle=':')

        # x-axis
        if args.max_N is None:
            args.max_N = max(out_df.N_Nodes) * 1.05
        ax.set_xlim([args.min_N, args.max_N])
        if args.xticks is not None:
            ax.set_xticks(np.arange(args.min_N,
                                    args.max_N + 1,
                                    step=args.xticks),
                          minor=False)
        ax.set_xlabel(xlabel)
        if lo_zoom_wc:
            ax.set_ylim([0, 7])

        #y-axis
        if var_to_plot == 'Efficiency':
            ax.set_ylim([20, 120])
            ax.axhline(y=70, color='k')

        if var_to_plot == 'Speedup':
            ax.plot([0, args.max_N], [0, args.max_N], color='black')
            ax.set_ylim([args.min_N, args.max_N])
        #ax.set_ylim([10,45])

        # y label
        ylab = var_to_plot
        if var_to_plot in unit.keys():
            ylab = '{} [{}]'.format(ylab, unit[var_to_plot])
        ax.set_ylabel(ylab)

        ax.legend()

        # sort global dataframe
        out_df.sort_values(by=['N_Nodes'], ascending=[1], inplace=True)

        # write out global dataframe
        if lo_write_csv:
            filename_out = os.path.join(
                path, 'summary_{}_tot_{}.csv'.format(var_to_plot,
                                                     args.name_plot))
            out_df.to_csv(filename_out,
                          sep=';',
                          index=False,
                          float_format="%.2f")

        if lo_savefig:
            pp.savefig()

    if lo_savefig:
        pp.close()
