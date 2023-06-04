import sys 
import os 
import inspect 
import pickle 
import numpy as np 


def enumerate_all_data_path():
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)

    datadir = os.path.join(parentdir, 'data') 

    return [os.path.join(datadir, filename) for filename in os.listdir(datadir)] 

def load_data(data_path):
    with open(data_path, 'rb') as f:
        return pickle.load(f) 
    
def process_label(label: str, num_fingerprint=1):
    if ',' in label:
        labels = label.split(',')
        labels = [float(label) for label in labels]

        return np.tile(np.array(labels), (num_fingerprint, 1))
    else:
        return np.ones((num_fingerprint, 1)) * float(label) 

