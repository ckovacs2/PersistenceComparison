import pandas as pd
import os
import numpy as np

def read_xyz_file(filepath: str):
    element=np.loadtxt(filepath,dtype=str,usecols=(0,), skiprows=2)
    x=np.loadtxt(filepath,dtype=float,usecols=(1), skiprows=2)
    y=np.loadtxt(filepath,dtype=float,usecols=(2),skiprows=2)
    z=np.loadtxt(filepath,dtype=float,usecols=(3),skiprows=2)
    return pd.DataFrame({'element':element, 'x':x, "y":y, "z":z})

def construct_file_frame(xyz_dir:str = "/workspaces/PersistenceComparison/xyz_data"):
    outpath = os.path.join(xyz_dir, "filepaths.csv")
    if os.path.exists(outpath):
        return pd.read_csv(outpath)
    
    datastores = [os.path.join(xyz_dir, dir) for dir in os.listdir(xyz_dir) if not dir.startswith('.') and dir != 'gas_only']
    filepaths = [(os.path.join(ds, file), ds.split('/')[-1], int(file.rstrip(".xyz"))) for ds in datastores for file in os.listdir(ds) if not file.startswith(".")]
    dataframe = pd.DataFrame(filepaths, columns = ["Filepath", "Dir", "Filename"])
    dataframe = dataframe.sort_values(['Dir', 'Filename'])
    dataframe['Filename'] = dataframe['Filename'].apply(lambda x: str(x) + '.xyz')
    dataframe = dataframe.reset_index(drop = True)
    dataframe.to_csv(outpath, index=False)
    return dataframe