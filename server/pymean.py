import os
from pandas import DataFrame
import pandas
import numpy as np
import csv

def avger(encoded_file_name, result):
    # Listing files in the directory
    csv_files, files = [], []
    files = os.listdir('/tmp') #[f for f in os.listdir('/tmp') if os.path.isfile(f)]
    for e in files:
        if(e.find('csv')!=-1):
            csv_files.append(e)
    print files
    # Initing dataframes
    mean_data = DataFrame()
    concated_data = DataFrame()
    
    # Listing csv files in pwd
    print csv_files


    # Concating all features into one
    for file in csv_files:
        print file
        data = DataFrame.from_csv('/tmp/'+file, header=None)
        mean_data = data.mean()
        frames = [concated_data, mean_data]
        concated_data = pandas.concat(frames) 
    print concated_data.shape


    #concated_data = concated_data.T
    #concated_data = list(concated_data)
    concated_data = concated_data[0].tolist()
    if result=='true':
        concated_data.append(1)
    else:
        concated_data.append(0)
    print len(concated_data)
    for file in csv_files:
        os.remove('/tmp/'+file)
    f = open('/tmp/data/data.csv', 'ab')
    writer = csv.writer(f)
    writer.writerow(list(concated_data))
    f.close()
    #np.savetxt('/tmp/'+encoded_file_name[0:-4]+'.csv', concated_data, delimiter=',')
# TODO: Piping output into a file
