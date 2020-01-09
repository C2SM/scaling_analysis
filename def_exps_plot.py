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
e63h23_T63L47_6h_2017 = experiment(name = 'e63h23_T63L47_6h_2017', label = 'ECHAM-HAM 6h', bestconf = 16, color = 'pink', marker = 'd', linestyle = '--')
esm_ham_T63L47_1m_2017 = experiment(name = 'ESM-HAM-T63L47_1m_2017', label = 'MPI-ESM-HAM 1m', bestconf = 36, color = 'green', marker = '*', linestyle = '-')

#atm_amip_1m_gcc = experiment(name = 'atm_amip_1m_gcc', label = 'ICON gcc 1m', color = 'LightBlue', marker = 'd', linestyle = '-')
#atm_amip_1m = experiment(name = 'atm_amip_1m', label = 'ICON cray 1m', bestconf = 34, color = 'blue', marker = 'o', linestyle = '-')
#atm_amip_6h = experiment(name = 'atm_amip_6h', label = 'ICON cray 6h', bestconf = 33, color = 'purple', marker = 'o', linestyle = '--')
e63_default_T63L47_6h = experiment(name = 'e63_6h', label = 'ECHAM 1m', bestconf = 10, color = 'grey', marker = 's', linestyle = '-')
e63h23_T63L47_1m = experiment(name = 'e63ham_1m', label = 'ECHAM-HAM 1m')#, bestconf = 36, color = 'red', marker = 'd', linestyle = '-')
e63h23_T63L47_6h = experiment(name = 'e63ham_6h', label = 'ECHAM-HAM 6h', bestconf = 12, color = 'pink', marker = 'd', linestyle = '--')
esm_ham_T63L47_1m = experiment(name = 'mpiesm-ham_1m', label = 'MPI-ESM-HAM 1m', bestconf = 48, color = 'green', marker = '*', linestyle = '-')

iconham_gcc = experiment(name = 'atm_amip_hammoz_marc', label = 'ICON-HAM 1m', bestconf = 24, marker = '+') #, color = 'LightBlue', marker = 'd', linestyle = '-')

icon_amip_6h_gcc = experiment(name = 'atm_amip_gcc_6h', label = 'ICON GCC 6h', bestconf = 24, marker = '.', color = 'LightBlue', linestyle = '--')#, marker = 'd', linestyle = '-')
icon_amip_1m_gcc = experiment(name = 'atm_amip_gcc_1m', label = 'ICON GCC 1m', bestconf = 24, marker= '*', color = 'Blue')#, marker = 'd', linestyle = '-')
icon_lam_gcc = experiment(name = 'ICON_limarea_Bernhard_7d_gcc', label = 'ICON-LAM GCC', bestconf = 24 , color = 'Blue', marker = 'd')#, linestyle = '-')

icon_amip_6h_intel = experiment(name = 'atm_amip_intel_6h', label = 'ICON intel 6h', bestconf = 64, marker = '.', color = 'Red',linestyle = '--')#, marker = 'd', linestyle = '-')
icon_amip_1m_intel = experiment(name = 'atm_amip_intel_1m', label = 'ICON intel 1m', bestconf = 40, marker= '*', color = 'Purple')#, marker = 'd', linestyle = '-')
icon_lam_intel = experiment(name = 'ICON_limarea_Bernhard_7d_intel', label = 'ICON-LAM intel', bestconf = 24 , color = 'Red', marker = 'd')#, linestyle = '-')

icon_amip_6h_cray = experiment(name = 'atm_amip_6h', label = 'ICON cray 6h', bestconf = 24, marker = '.', color = 'Green',linestyle = '--')#, marker = 'c', linestyle = '-')
icon_amip_1m_cray = experiment(name = 'atm_amip_1m', label = 'ICON cray 1m', bestconf = 24, marker = '*', color = 'LightGreen')#, marker = '*', linestyle = '-')
icon_lam_cray = experiment(name = 'ICON_limarea_Bernhard_7d', label = 'ICON-LAM cray', bestconf = 128, color = 'Green', marker = 's')#, linestyle = '-')

icon_lam_init_gcc = experiment(name = 'ICON_limarea_Bernhard_init_gcc', label = 'ICON-LAM init gcc', bestconf = 24, color = 'Blue', marker = '.')#, linestyle = '-')
icon_lam_init_intel = experiment(name = 'ICON_limarea_Bernhard_init_intel', label = 'ICON-LAM init intel', bestconf = 24 , color = 'Red', marker = '.') #, linestyle = '-')
icon_lam_init_cray = experiment(name = 'ICON_limarea_Bernhard_init', label = 'ICON-LAM init cray', bestconf = 24 , color = 'Green', marker = '.')#, linestyle = '-')

icon_amip_6h_final = experiment(name = 'atm_amip_intel_6h', label = 'ICON 6h', bestconf = 64, marker = '.', color = 'Magenta',linestyle = '--')#, marker = 'd', linestyle = '-')
icon_amip_1m_final = experiment(name = 'atm_amip_intel_1m', label = 'ICON 1m', bestconf = 40, marker= '.', color = 'Purple')#, marker = 'd', linestyle = '-')
icon_lam_final = experiment(name = 'ICON_limarea_Bernhard_7d', label = 'ICON-LAM', bestconf = 128, color = 'Red', marker = '>',markersize=4, linestyle = '--')
icon_ham_final = experiment(name = 'atm_amip_hammoz_marc', label = 'ICON-HAM', bestconf = 24, marker = '.', color = 'Blue', linestyle = '-')
e63h23_1m_final = experiment(name = 'e63ham_1m', label = 'ECHAM-HAM', bestconf = 36, color = 'Green', marker = '*', linestyle = '-')
esmham_1m_final = experiment(name = 'mpiesm-ham_1m', label = 'MPI-ESM-HAM', bestconf = 48, color = 'LightGreen', marker = 'd', markersize=4, linestyle = '-')
