import pickle
import numpy as np 


class LocalizationModel:
    def __init__(self):
        pass 

    def train(self, x, y, *args, **kwargs):
        self.x = x 
        self.y = y
        pass 

    def predict(self, x, *args, **kwargs):
        # 1-kNN
        minval = np.nanmin(self.x) 

        train_x = self.x.copy() 

        train_x[np.isnan(train_x)] = minval

        x[np.isnan(x)] = minval


        dists = np.linalg.norm(train_x - np.tile(x, (train_x.shape[0], 1)), axis=1)
        min_ind = np.argmin(dists) 

        return self.y[min_ind].squeeze() 

    def save_model(self, model_path: str):
        with open(model_path, 'wb') as f:
            pickle.dump(self, f) 

    @staticmethod  
    def load_model(model_path: str):
        with open(model_path, 'rb') as f:
            return pickle.load(f) 
