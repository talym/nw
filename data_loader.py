import pandas as pd
from scipy.io import loadmat

class DataLoader(object):
    def __init__(self, cm, cent, part):
        self.cm = pd.read_csv(cm, header=None)
        self.cent = loadmat(cent)['centroids']
        self.clustersNames = loadmat(part)['clusters']
        print(self.clustersNames[0])

