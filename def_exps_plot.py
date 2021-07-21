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

atm_amip_gcc_O1 = experiment(name = 'atm_amip_gcc.O1', label = 'gcc.O1', bestconf = 8, marker = '>', color = '#fee0d2',linestyle = '-')#, marker = 'd', linestyle = '-')
atm_amip_gcc_O2 = experiment(name = 'atm_amip_gcc.O2', label = 'gcc.O2', bestconf = 8, marker = 'x', color = '#fc9272',linestyle = '-')#, marker = 'd', linestyle = '-')
atm_amip_gcc_O3 = experiment(name = 'atm_amip_gcc.O3', label = 'gcc.O3', bestconf = 8, marker = 'o', color = '#de2d26',linestyle = '-')#, marker = 'd', linestyle = '-')
atm_amip_pgi_O1 = experiment(name = 'atm_amip_pgi.O1', label = 'pgi.O1', bestconf = 8, marker = '>', color = '#edf8b1',linestyle = '-')#, marker = 'd', linestyle = '-')
atm_amip_pgi_O2 = experiment(name = 'atm_amip_pgi.O2', label = 'pgi.O2', bestconf = 8, marker = 'x', color = '#7fcdbb',linestyle = '-')#, marker = 'd', linestyle = '-')
#atm_amip_pgi_O3 = experiment(name = 'atm_amip_pgi.O3', label = 'pgi.O3', bestconf = 8, marker = 'x', color = '#2c7fb8',linestyle = '-')#, marker = 'd', linestyle = '-')
