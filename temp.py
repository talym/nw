import nibabel as nib
import numpy as np

img_path_17 = r'C:\Users\talym\PycharmProjects\nw\atlas\tpl-MNI152NLin2009cAsym_res-02_atlas-Schaefer2018_desc-400Parcels17Networks_dseg.nii'
img_path_7 = r'C:\Users\talym\PycharmProjects\nw\atlas\tpl-MNI152NLin2009cAsym_res-02_atlas-Schaefer2018_desc-400Parcels7Networks_dseg.nii'
l_17 = r'C:\Users\talym\PycharmProjects\nw\atlas\tpl-MNI152NLin2009cAsym_res-02_atlas-Schaefer2018_desc-400Parcels17Networks_dseg.nii'
l_path_7 = r'C:\Users\talym\PycharmProjects\nw\atlas\schaefer400x7CommunityAffiliation.csv'
l_path_17 = r'C:\Users\talym\PycharmProjects\nw\atlas\schaefer400x17CommunityAffiliation.csv'
mapping = r'C:\Users\talym\PycharmProjects\nw\atlas\mapping_7_17.csv'
if __name__ == '__main__':

    img_17 = nib.load(img_path_17)
    data_17 = img_17.get_fdata()
    img_7 = nib.load(img_path_7)
    data_7 = img_7.get_fdata()

    map_7_to_17 = np.zeros((400, 2))
    for parcell_7 in range(1, 400):
        chosen_parcels_7 = data_17[data_7 == parcell_7]
        if (np.unique(chosen_parcels_7).shape[0]!=1):
            print('ERROR')
        map_7_to_17[parcell_7-1, 0] = int(parcell_7)
        map_7_to_17[parcell_7 - 1, 1] = int(np.unique(chosen_parcels_7)[0])
    np.savetxt(mapping, map_7_to_17, delimiter=',')
