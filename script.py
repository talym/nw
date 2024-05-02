# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from data_loader import DataLoader
from energy_est import EnergyEst
from visualizer import VS

CM = r'atlas\cs400_7NW.csv'
CENTROIDS = r'Energy\subjcentroids_split_k6.mat'
PARTITION_BP = r'Energy\TransProbsData_bp_k6.mat'
CLINIC = r'atlas\ptsd_fo_pcl.xlsx'
PTSD_NUM = 79

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    dl = DataLoader(cm=CM, cent=CENTROIDS, part=PARTITION_BP)
    en = EnergyEst(cm=dl.cm, cent=dl.cent, clustersNames=dl.clustersNames)
    en.CalcMinU()
    ptsd_subj_energy_1 = en.GetSubjEn(start_type=0, stop_type=79, ses=1)
    ptsd_subj_energy_2 = en.GetSubjEn(start_type=0, stop_type=79, ses=2)
    vs = VS()
    vs.energy_heatmap(ptsd_subj_energy_1, ptsd_subj_energy_2, dl.clustersNames, 'PTSD transition energy')
    #vs.corr_heatmap(ptsd_subj_energy_1, ptsd_subj_energy_2, CLINIC, dl.clustersNames)
