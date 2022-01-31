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
                      color='#fcae91',
                      linestyle='-')

euler_02 = experiment(name='atm_rte_rrtmgp_amip_test_e6_gccO2',
                      label='Euler6, gcc.O2',
                      bestconf=200,
                      marker='x',
                      color='#fb6a4a',
                      linestyle='-')

euler_03 = experiment(name='atm_rte_rrtmgp_amip_test_gccO3',
                      label='gcc.O3',
                      bestconf=35,
                      marker='o',
                      color='#cb181d',
                      linestyle='-')

daint_01 = experiment(name='atm_rte_rrtmgp_amip_test_gccO1',
                      label='gcc.O1',
                      bestconf=35,
                      marker='>',
                      color='#fcae92',
                      linestyle='-')

daint_02 = experiment(name='atm_rte_rrtmgp_amip_test_gccO2',
                      label='gcc.O2',
                      bestconf=50,
                      marker='x',
                      color='#fb6a4a',
                      linestyle='-')

daint_03 = experiment(name='atm_rte_rrtmgp_amip_test_pgiO2',
                      label='pgi.O2',
                      bestconf=35,
                      marker='o',
                      color='#cb181d',
                      linestyle='-')
