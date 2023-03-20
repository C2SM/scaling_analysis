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


# Definition of each experiment properties (colors, labels,ect)

euler_01 = experiment(name='atm_rte_rrtmgp_amip_test_gccO2',
                      label='Euler7, gcc.O2',
                      bestconf=50,
                      marker='>',
                      color='#253494',
                      linestyle='-')

daint_01 = experiment(name='icon_cordex_12km_era5_gpu_20230222',
                      label='CORDEX-12km',
                      bestconf=36,
                      marker='>',
                      color='#253494',
                      linestyle='-')
