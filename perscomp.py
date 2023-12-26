import numpy as np
import gudhi
from persim.landscapes.visuals import plot_landscape_simple , PersLandscapeExact
import pandas as pd
import matplotlib.pyplot as plt

from utils import read_xyz_file

class RipsComplex:
    def __init__(self, pt_cloud):
        self.rips = gudhi.RipsComplex(points=pt_cloud)
        self.simplex_tree = self.rips.create_simplex_tree(max_dimension=3)
        self.diag = self.simplex_tree.persistence(homology_coeff_field=2, min_persistence=0)
        #self.dgms_pt_cloud = [np.unique(self.rips.fit_transform(data)[d], axis = 0) for d in range(maxdim)]

class PersLandscape:
    def __init__(self, filepath: str):
        self.xyz_data = read_xyz_file(filepath=filepath)
        self.ripscomplex = RipsComplex(self.xyz_data[['x', 'y', 'z']].values)

    def construct_bd_functions(self):
        # FIX THIS IN TERMS OF GUDHI
        def return_hom_frame(hom):
            data = [(b, d, 0.5*(d-b), 0.5*(d+b)) for b,d in self.dgms_pt_cloud[hom]]
            return pd.DataFrame(data, columns = ['b', 'd', 'max_y', 'max_x']).drop_duplicates().replace([np.inf, -np.inf], np.nan).dropna()
        ffs_0 = return_hom_frame(0)
        ffs_1 = return_hom_frame(1)
        ffs_2 = return_hom_frame(2)
        return ffs_0, ffs_1, ffs_2

    def plot(self):
        # FIX THIS IN TERMS OF GUDHI
        fig, axs = plt.subplots(2, 3)
        fig.set_size_inches(10, 5)

        data_0, data_1, data_2 = self.construct_bd_functions()
        colors = ['red', 'blue', 'green']
        for i, data in enumerate([data_0, data_1, data_2]):
            axs[0, i].title.set_text(f"Degree {i} Functions")

        for j, row in data.iterrows():
            axs[0, i].plot([row['b'], row['max_x'], row['d']],[0, row['max_y'], 0], c = 'black')
        axs[0, i].scatter(data['max_x'], data['max_y'], c = colors[i], alpha = 0.5)

        plot_landscape_simple(PersLandscapeExact(self.dgms_pt_cloud, hom_deg=0),title="Degree 0 Persistence Landscape of Point Cloud", ax = axs[1, 0])
        plot_landscape_simple(PersLandscapeExact(self.dgms_pt_cloud, hom_deg=1),title="Degree 1 Persistence Landscape of Point Cloud", ax = axs[1, 1])
        plot_landscape_simple(PersLandscapeExact(self.dgms_pt_cloud, hom_deg=2),title="Degree 2 Persistence Landscape of Point Cloud", ax = axs[1, 1])
        
        plt.tight_layout()
        plt.show()


class PersLandscapeGauss(RipsComplex):
    def __init__(self, filepath: str):
        self.xyz_data = read_xyz_file(filepath=filepath)
        self.ripscomplex = RipsComplex(self.xyz_data[['x', 'y', 'z']].values)

class PersImage:
    def __init__(self, filepath: str):
        self.xyz_data = read_xyz_file(filepath=filepath)
        self.ripscomplex = RipsComplex(self.xyz_data[['x', 'y', 'z']].values)

pl = PersLandscape("/workspaces/PersistenceComparison/xyz_data/n2folder/10.xyz")
print(pl.ripscomplex.rips)