# definition of the object "experiment". It contains mostly the potting properties

import numpy as np

class experiment:
     def __init__(self, name, label = None, bestconf = np.nan, linewidth = 1., **kwargs):
         self.name = name
         if label is None:
             self.label = name
         else:
             self.label = label
         self.bestconf = bestconf

         self.line_appareance = kwargs
         self.line_appareance['linewidth'] = linewidth

# Definition of each experiment properties (colors, labels,ect)

echam_ham_amip_T63L47 = experiment(name='ECHAM-HAM_amip_T63L47',
                                   label='ECHAM-HAM 1M', bestconf=36,
                                   marker='>', color='#fcae91', linestyle='-')
icon_cpu_gcc_amip = experiment(name='ICON_cpu_gcc_amip',
                               label='ICON (cpu, gcc) 1M', bestconf=43,
                               marker='o', color='green', linestyle='--')
icon_cpu_pgi_amip = experiment(name='ICON_cpu_pgi_amip',
                               label='ICON (cpu, pgi) 1M', bestconf=42,
                               marker='o', color='blue', linestyle='-')
