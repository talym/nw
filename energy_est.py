# Assumes ses1 subjects first, ses2 subjects second.
# Assumes num. ses1 subj == num. ses2 subj

from nctpy.utils import matrix_normalization
from nctpy.energies import sim_state_eq, get_control_inputs, integrate_u
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

SAVE_ENERGY = r'results\energy.npy'

DEBUG = False
LOAD = False
T_HORIZON = 0.001 # time horizon
RHO = 1  # mixing parameter for state trajectory constraint
SYSTEM = 'continuous' #'discrete'
class EnergyEst(object):
    def __init__(self, cm, cent, clustersNames):
        self.min_t_energy = None
        self.system = SYSTEM
        self.clustersNames = clustersNames
        cm[cm < 1000] = 0
        if SYSTEM == 'continuous':
            c = 0
        else:
            c = 1
        self.A_norm = matrix_normalization(A=cm.values, c=c, system=self.system) #0 - continuose, 1 - discrete
        self.cent = cent
        self.subj_num = cent.shape[0]/2

    def GetSubjEn(self, start_type, stop_type, ses):
        start = int((ses - 1)*self.subj_num + start_type)
        stop = int((ses - 1)*self.subj_num + stop_type)
        print(f'ses: start: {start}, stop: {stop}')
        return self.min_t_energy[start:stop]
    def CalcMinU(self):
        if LOAD:
            self.min_t_energy = np.load(SAVE_ENERGY)
            return
        n_nodes = self.A_norm.shape[0]
        self.min_t_energy = np.zeros((self.cent.shape[0], self.clustersNames.shape[0], self.clustersNames.shape[0]))
        T = T_HORIZON
        rho = RHO
        S = np.eye(n_nodes)  # nodes in state trajectory to be constrained
        B = np.eye(n_nodes)  # uniform full control set

        for subj in range(self.cent.shape[0]):
            print(subj)
            for final_state in range(self.clustersNames.shape[0]):
                for start_state in range(self.clustersNames.shape[0]):
                    if DEBUG:
                        self.VisualizeImpResp(n_nodes, self.cent[subj])

                    x0 = self.cent[subj, :, start_state]
                    xf = self.cent[subj, :, final_state]

                    # get the state trajectory (x) and the control inputs (u)
                    x, u, n_err = get_control_inputs(A_norm=self.A_norm, T=T, B=B, x0=x0, xf=xf, system=self.system, rho=rho, S=S)
                    if n_err[0] > 1e-8:
                        print(subj, ' - Solving for the control signals was NOT well-conditioned')
                    if n_err[1] > 1e-8:
                        print(subj, ' - state transition was NOT completed successfully')

                    # integrate control inputs to get control energy
                    node_energy = integrate_u(u)

                    # summarize nodal energy to get control energy
                    self.min_t_energy[subj, start_state, final_state] = np.sum(node_energy)
            np.save(SAVE_ENERGY, self.min_t_energy)
            print('Saved')

    def VisualizeImpResp(self, n_nodes, x0):
        sns.set(style='whitegrid', context='paper', font_scale=1)

        T = 1000  # time horizon
        U = np.zeros((n_nodes, T))  # the input to the system
        U[:, 0] = 1  # impulse, 1 input at the first time point delivered to all nodes
        B = np.eye(n_nodes)  # uniform full control set
        x = sim_state_eq(A_norm=self.A_norm, B=B, x0=x0, U=U, system=self.system)

        # plot
        f, ax = plt.subplots(1, 1, figsize=(3, 3))
        ax.plot(x.T)
        ax.set_ylabel('Simulated neural activity (arbitrary units)')
        ax.set_xlabel('Time (arbitrary units)')
        f.savefig('A_stable.png', dpi=600, bbox_inches='tight', pad_inches=0.01)
        plt.show()