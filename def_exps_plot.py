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

icon_amip_intel = experiment(name = 'atm_amip_intel', label = 'atm_amip intel', bestconf = 22, marker = '>', color = 'Red',linestyle = '-')#, marker = 'd', linestyle = '-')
icon_amip_6h_intel = experiment(name = 'atm_amip_6h_intel', label = 'atm_amip intel 6h', bestconf = 26, marker = '.', color = 'Red',linestyle = '--')#, marker = 'd', linestyle = '-')
icon_amip_1m_intel = experiment(name = 'atm_amip_1m_intel', label = 'atm_amip intel 1m', bestconf = 20, marker= '*', color = 'Red',linestyle = '-.')#marker = 'd', linestyle = '-')

icon_amip_cray = experiment(name = 'atm_amip_cray', label = 'atm_amip cray', bestconf = 38, marker = '>', color = 'Green',linestyle = '-')#, marker = 'c', linestyle = '-')
icon_amip_6h_cray = experiment(name = 'atm_amip_6h_cray', label = 'atm_amip cray 6h', bestconf = 36, marker = '.', color = 'Green',linestyle = '--')#, marker = 'c', linestyle = '-')
icon_amip_1m_cray = experiment(name = 'atm_amip_1m_cray', label = 'atm_amip cray 1m', bestconf = 34, marker = '*', color = 'Green',linestyle = '-.')#, marker = '*', linestyle = '-')

icon_amip_pgi = experiment(name = 'atm_amip_pgi', label = 'atm_amip PGI', bestconf = 38, marker = '>', color = 'Blue', linestyle = '-')
icon_amip_6h_pgi = experiment(name = 'atm_amip_6h_pgi', label = 'atm_amip PGI 6h', bestconf = 38, marker = '.', color = 'Blue', linestyle = '--')
icon_amip_1m_pgi = experiment(name = 'atm_amip_1m_pgi', label = 'atm_amip PGI 1m', bestconf = 38, marker= '*', color = 'Blue',linestyle = '-.')