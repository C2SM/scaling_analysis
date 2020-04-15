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


icon_amip_intel = experiment(name = 'atm_amip_intel', label = 'ICON intel', bestconf = 64, marker = '<', color = 'Red')#,linestyle = '-')#, marker = 'd', linestyle = '-')
icon_amip_6h_intel = experiment(name = 'atm_amip_intel_6h', label = 'ICON intel 6h', bestconf = 64, marker = '.', color = 'Red')#,linestyle = '--')#, marker = 'd', linestyle = '-')
icon_amip_1m_intel = experiment(name = 'atm_amip_intel_1m', label = 'ICON intel 1m', bestconf = 40, marker= '*', color = 'Red')#, marker = 'd', linestyle = '-')

icon_amip_6h_cray = experiment(name = 'atm_amip_6h', label = 'ICON cray 6h', bestconf = 24, marker = '.', color = 'Green',linestyle = '--')#, marker = 'c', linestyle = '-')
icon_amip_1m_cray = experiment(name = 'atm_amip_1m', label = 'ICON cray 1m', bestconf = 24, marker = '*', color = 'LightGreen')#, marker = '*', linestyle = '-')
icon_lam_init_cray = experiment(name = 'ICON_limarea_Bernhard_init', label = 'ICON-LAM init cray', bestconf = 24 , color = 'Green', marker = '.')#, linestyle = '-')
icon_lam_cray = experiment(name = 'ICON_limarea_Bernhard_7d', label = 'ICON-LAM cray', bestconf = 128, color = 'Green', marker = 's')#, linestyle = '-')

icon_amip_6h_final = experiment(name = 'atm_amip_intel_6h', label = 'ICON 6h', bestconf = 64, marker = '.', color = 'Magenta',linestyle = '--')#, marker = 'd', linestyle = '-')
icon_amip_1m_final = experiment(name = 'atm_amip_intel_1m', label = 'ICON 1m', bestconf = 40, marker= '.', color = 'Purple')#, marker = 'd', linestyle = '-')
icon_lam_final = experiment(name = 'ICON_limarea_Bernhard_7d', label = 'ICON-LAM', bestconf = 128, color = 'Red', marker = '>',markersize=4, linestyle = '--')
icon_ham_final = experiment(name = 'atm_amip_hammoz_marc', label = 'ICON-HAM', bestconf = 24, marker = '.', color = 'Blue', linestyle = '-')
e63h23_1m_final = experiment(name = 'e63ham_1m', label = 'ECHAM-HAM', bestconf = 36, color = 'Green', marker = '*', linestyle = '-')
esmham_1m_final = experiment(name = 'mpiesm-ham_1m', label = 'MPI-ESM-HAM', bestconf = 48, color = 'LightGreen', marker = 'd', markersize=4, linestyle = '-')

icon_amip_6h_pgi = experiment(name = 'atm_amip_pgi_6h', label = 'ICON PGI 6h', bestconf = 24, marker = '.', color = 'darkviolet', linestyle = '--')
icon_amip_1m_pgi = experiment(name = 'atm_amip_pgi_1m', label = 'ICON PGI 1m', bestconf = 24, marker= '*', color = 'plum')