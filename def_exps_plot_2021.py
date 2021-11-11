# definition of the object "experiment". It contains mostly the potting properties

import numpy as np


class experiment:
    def __init__(self,
                 name,
                 label=None,
                 bestconf=np.nan,
                 linewidth=1.,
                 **kwargs):
        self.name = name
        if label is None:
            self.label = name
        else:
            self.label = label
        self.bestconf = bestconf

        self.line_appareance = kwargs
        self.line_appareance['linewidth'] = linewidth


# Color palette
#fdcc8a
#fc8d59
#d7301f
#bdc9e1
#67a9cf
#02818a

# Definition of each experiment properties (colors, labels,ect)

echam_ham_amip_T63L47 = experiment(name='ECHAM-HAM_amip_T63L47',
                                   label='ECHAM-HAM 1M (cpu, intel)',
                                   bestconf=36,
                                   marker='>',
                                   color='#fdcc8a',
                                   linestyle='-')
icon_ham_amip = experiment(name='ICON-HAM_amip',
                           label='ICON-HAM 1M (cpu, pgi)',
                           bestconf=19,
                           marker='<',
                           color='#fc8d59',
                           linestyle='-')
icon_cpu_gcc_amip = experiment(name='ICON_cpu_gcc_amip',
                               label='ICON 1M (cpu, gcc)',
                               bestconf=43,
                               marker='x',
                               color='#bdc9e1',
                               linestyle='--')
icon_cpu_pgi_amip = experiment(name='ICON_cpu_pgi_amip',
                               label='ICON 1M (cpu, pgi)',
                               bestconf=42,
                               marker='x',
                               color='#67a9cf',
                               linestyle='-')
icon_gpu_pgi_amip_rte = experiment(name='ICON_gpu_pgi_amip_rte',
                                   label='ICON 1M (gpu, pgi)',
                                   bestconf=4,
                                   marker='v',
                                   color='#02818a',
                                   linestyle='-')
icon_r2b9 = experiment(name='ICON_R2B9',
                       label='ICON@R2B9 1h (gpu, pgi)',
                       bestconf=1692,
                       marker='.',
                       color='#b30000',
                       linestyle='-')
