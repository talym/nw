import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
from stats_fun import ttest_with_mc_correction
from scipy.stats import pearsonr

CLINIC_PARAM = ['caps5', 'B', 'C', 'D', 'E', 'Diss', 'PCL']

class VS(object):
    #def __init__(self, en1, en2, names, title):
    def energy_heatmap(self, en1, en2, names, title):
        grAvg1 = np.mean(en1, axis=0)
        grAvg2 = np.mean(en2, axis=0)
        self.plot_heatmap(grAvg1, names, title + ' SES1')
        self.plot_heatmap(grAvg2, names, title + ' SES2')
        p_values_3d, p_values_corrected_3d, delta = ttest_with_mc_correction(en1, en2)
        self.plot_heatmap(delta, names, title + ' SES1 - SES2', p_values_3d, p_values_corrected_3d)

    def plot_heatmap(self, en, names, title, p_values_3d=None, p_values_corrected_3d = None):
        plt.Figure(figsize=(8, 6))
        ax = sns.heatmap(en, annot=False, cmap='YlGnBu_r', xticklabels=names, yticklabels=names)
        if p_values_3d is not None:
            for i in range(p_values_3d.shape[0]):
                for j in range(p_values_3d.shape[1]):
                    if p_values_3d[i, j] < 0.05:
                        ax.text(j + 0.5, i + 0.5, '*', ha='center', va='center', color='white', fontsize=20)
        if p_values_corrected_3d is not None:
            for j in range(p_values_3d.shape[1]):
                if p_values_corrected_3d[i, j] < 0.0024:
                    ax.text(j + 0.25, i + 0.25, '**', ha='center', va='center', color='white', fontsize=20)
        plt.title(title)
        plt.xlabel('Final State')
        plt.xlabel('Initial State')
        plt.show()

    def corr_heatmap(self, en1, en2, clinic, names):
        df = pd.read_excel(clinic)
        delta = pd.DataFrame()
        for c in CLINIC_PARAM:
            delta[c] = df['TP2 ' + c] - df['TP1 ' + c]
        for final_state in range(names.shape[0]):
            delta_curr = pd.DataFrame()
            delta_curr = delta.copy()
            for start_state in range(names.shape[0]):
                delta_curr[names[start_state]+'_to_'+ names[final_state]] = \
                    en2[:, start_state, final_state] - en1[:, start_state, final_state]
            self.show_corr_matrix(delta_curr, 'Transition energy', True, True)

    def show_corr_matrix(self, df, title, vis_corr, vis_p):
        print(df.shape)
        #df.dropna(inplace=True)
        correlation_matrix = df.corr(method='pearson')
        pvalues = round(df.corr(method=lambda x, y: pearsonr(x, y)[1]), 4)

        # Visualize correlation matrix using heatmap
        if vis_corr:
            plt.figure(figsize=(10, 8))
            sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, vmin=-1, vmax=1)
            plt.title('corr ' + title)
            plt.show()
        if vis_p:
            plt.figure(figsize=(10, 8))
            sns.heatmap(pvalues, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5, vmin=0.03, vmax=1)
            plt.title('P ' + title)
            plt.show()