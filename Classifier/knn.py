from . import classify as classify

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

import pickle 


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

            # channel_data: (? intervals, 190 readings/interval, 3 channels)
            channel_data = np.stack(channel_y_list, axis=-1)
            
            # channel_means: (? meaned intervals, 3 channels)
            channel_means = channel_data.mean(axis=1)
            
            train_size = int(0.5*channel_means.shape[0])
            #means are normalized only on training data
            #labels across channels should be identical
            X = channel_means/channel_means[:train_size].std(axis=0)
            y = trainingData[0][1]
    
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
       

    def saveModel(self, location):
        # Its important to use binary mode 
        knnPickle = open(location, 'wb')
        
        # source, destination 
        # pickle.dump((np.array([23.31751269 19.06549261 12.54092506]),self.model), knnPickle) 
        pickle.dump(self.model, knnPickle) 
    
    def loadModel(self, location):
        self.trainedModel = pickle.load(open(location, 'rb'))
        # (self.trainedSTD, self.trainedModel = pickle.load(open(location, 'rb'))

    def classify(self, observation):
        #observation is in this form np.array([channel0,channel1,channel2]) where each one has 190 elems
        # divide by model standard deviation
        return self.trainedModel.predict(observation)