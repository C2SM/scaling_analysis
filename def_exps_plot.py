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

atm_amip_1m_gcc = experiment(name = 'atm_amip_1m_gcc', label = 'ICON gcc 1m', color = 'LightBlue', marker = 'd', linestyle = '-')
atm_amip_1m = experiment(name = 'atm_amip_1m', label = 'ICON cray 1m', bestconf = 34, color = 'blue', marker = 'o', linestyle = '-')
atm_amip_6h = experiment(name = 'atm_amip_6h', label = 'ICON cray 6h', bestconf = 33, color = 'purple', marker = 'o', linestyle = '--')
e63_default_T63L47_6h = experiment(name = 'e63_6h', label = 'ECHAM 1m', bestconf = 10, color = 'orange', marker = 's', linestyle = '-')
e63h23_T63L47_1m = experiment(name = 'e63ham_1m', label = 'ECHAM-HAM 1m', bestconf = 36, color = 'red', marker = 'd', linestyle = '-')
e63h23_T63L47_6h = experiment(name = 'e63ham_6h', label = 'ECHAM-HAM 6h', bestconf = 12, color = 'pink', marker = 'd', linestyle = '--')
esm_ham_T63L47_1m = experiment(name = 'mpiesm-ham_1m', label = 'MPI-ESM-HAM 1m', bestconf = 48, color = 'green', marker = '*', linestyle = '-')

iconham_gcc = experiment(name = 'atm_amip_hammoz_marc', label = 'ICON-HAM', color = 'LightBlue', marker = 'd', linestyle = '-')
