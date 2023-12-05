#%%
import h5py
import numpy as np
import pandas as pd
# %%
dataset = h5py.File('/Users/shivani/Easiur/Datadir/sc_8.6MVSL_area_pop2005.hdf5', 'r')
dataset.keys()
# %%
PEC = dataset['PEC_Spring']
print(PEC)
# %%
PEC_df=pd.DataFrame(PEC)
# %%
PEC_df.head()
# %%
