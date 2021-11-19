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

euler_01 = experiment(name='atm_rte_rrtmgp_amip_test_gcc02',
                      label='Euler7, gcc.02',
                      bestconf=50,
                      marker='>',
                      color='#fcae91',
                      linestyle='-')

euler_02 = experiment(name='atm_rte_rrtmgp_amip_test_e6_gcc02',
                      label='Euler6, gcc.02',
                      bestconf=200,
                      marker='x',
                      color='#fb6a4a',
                      linestyle='-')

euler_03 = experiment(name='atm_rte_rrtmgp_amip_test_gcc03',
                      label='gcc.03',
                      bestconf=35,
                      marker='o',
                      color='#cb181d',
                      linestyle='-')

daint_01 = experiment(name='atm_rte_rrtmgp_amip_test_gcc01',
                      label='gcc.01',
                      bestconf=35,
                      marker='>',
                      color='#fcae92',
                      linestyle='-')

daint_02 = experiment(name='atm_rte_rrtmgp_amip_test_gcc02',
                      label='gcc.02',
                      bestconf=35,
                      marker='x',
                      color='#fb6a4a',
                      linestyle='-')

daint_03 = experiment(name='atm_rte_rrtmgp_amip_test_pgi02', label='pgi.02', bestconf=35, marker='o', color='#cb181d',linestyle='-')
