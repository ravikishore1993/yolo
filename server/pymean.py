import os
from pandas import DataFrame
import pandas
import numpy as np

# Listing files in the directory
csv_files, files = [], []
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for e in files:
    if(e.find('.csv')!=-1):
        csv_files.append(e)

# Initing dataframes
mean_data = DataFrame()
concated_data = DataFrame()

# Listing csv files in pwd
print csv_files

# Concating all features into one
for file in csv_files:
    print file
    data = pandas.read_csv(file, header=None, skiprows=5)
    mean_data = data.mean()
    frames = [concated_data, mean_data]
    concated_data = pandas.concat(frames) 

print concated_data.shape

# TODO: Piping output into a file
