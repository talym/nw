import numpy as np
from scipy.stats import ttest_ind
from statsmodels.stats.multitest import multipletests


def ttest_with_mc_correction(group1, group2):
    # Reshape the data into 2D arrays (samples x features)
    group1_2d = group1.reshape((group1.shape[0], -1))
    group2_2d = group2.reshape((group2.shape[0], -1))

    t_stat, p_values = ttest_ind(group1_2d, group2_2d, axis = 0)
    reject, p_values_corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
    p_values_corrected_3d = p_values_corrected.reshape(group1.shape[1:])
    p_values_3d = p_values.reshape(group1.shape[1:])
    p_values_corrected_3d = p_values_corrected.reshape(group1.shape[1:])
    delta = np.mean(group1 - group2, axis=0)
    return p_values_3d, p_values_corrected_3d, delta