import classify as classify

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

class KNN(classify.Classifier):
    def __init__(self, n):
        self.model = KNeighborsClassifier(n_neighbors=n, weights='distance')

    def train(self, trainingSets):
        # make four empty numpy arrays
        X_train_all, X_test_all, y_train_all, y_test_all = [[],[],[],[]]
        for trainingData in trainingSets:
      	# trainingData -> (c0, c1, c2) -> (x_groups, y_groups, t_groups), l_groups
          #  -> each group is 1 sec w 190 rows

            # channel_y: 3 channel list -> (? intervals, 190 recordings/interval)
            channel_y_list = [np.stack(channel[0][1]) for channel in trainingData.values()]

            # channel_data: (? intervals, 190 readings/interval, 3 channels) but all three channels in one element
            channel_data = np.stack(channel_y_list, axis=1)
            
            # flattens all three channels into one vector
            channel_data_merged = []
            for elem in channel_data:
                channel_data_merged.append(elem.flatten())
            channel_data_merged = np.array(channel_data_merged)

            
            train_size = int(0.5*channel_data_merged.shape[0])
           
            X = channel_data_merged
            y = y = trainingData[0][1]
    
            X_train, X_test = np.split(X, [train_size])
            y_train, y_test = np.split(y, [train_size])

            X_train_all.append(X_train)
            X_test_all.append(X_test)
            y_train_all.append(y_train)
            y_test_all.append(y_test)


        X_train_all = np.concatenate(X_train_all)
        X_test_all = np.concatenate(X_test_all)
        y_train_all = np.concatenate(y_train_all)
        y_test_all = np.concatenate(y_test_all)

        self.model.fit(X_train_all, y_train_all)

        results = self.model.predict(X_test_all)

        onehot_to_int = np.array([0,1,2,3,4])
        flat_y_test = (y_test_all*onehot_to_int).sum(axis=1)
        flat_results = (results*onehot_to_int).sum(axis=1)

        # rows represent true value, columns are predicted value
        self.confusion_matrix = confusion_matrix(flat_y_test, flat_results)
        self.confusion_matrixNorm = confusion_matrix(flat_y_test, flat_results, normalize='true')
        print(self.confusion_matrix)
        print(self.confusion_matrixNorm)

    def classify(self, observation):
        pass
