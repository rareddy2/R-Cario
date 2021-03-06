import classify as classify

import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from scipy.fft import fft, fftfreq
from scipy.signal import welch

class KNN_FFT(classify.Classifier):
    def __init__(self, n):
        self.model = KNeighborsClassifier(n_neighbors=n, weights='distance')

    def train(self, trainingSets):
        # make four empty numpy arrays
        X_train_all, X_test_all, y_train_all, y_test_all = [[],[],[],[]]

        X = []
        X_test = []
        y = []
        y_test = []
        for trainingData in trainingSets:
      	# trainingData -> (c0, c1, c2) -> (x_groups, y_groups, t_groups), l_groups
          #  -> each group is 1 sec w 190 rows

            # channel_y: 3 channel list -> (? intervals, 190 recordings/interval)
            channel_y_list = [np.stack(channel[0][1]) for channel in trainingData.values()]
            print(channel_y_list[0][0].shape)

            channel_y_listFFT_0 = []
            for obs in channel_y_list[0]:
                channel_y_listFFT_0.append(fft(obs))


            # # channel_data: (? intervals, 190 readings/interval, 3 channels)
            # channel_data = np.stack(channel_y_list, axis=-1)

            # channel_fft = np.abs(fft(channel_data, axis=1))
            # freqs = fftfreq(channel_data.shape[1])
            # channel_freqs = np.stack([freqs]*3, axis=1)
            
            # # channel_means: (? meaned intervals, 3 channels)
            # channel_means = (channel_freqs*channel_fft).mean(axis=1)
            
            train_size = int(0.8*216)
            # #means are normalized only on training data
            # #labels across channels should be identical
            # X = channel_means/channel_means[:train_size].std(axis=0)
            # y = trainingData[0][1]
    
            # X_train, X_test = np.split(np.arange(216), [train_size])
            # y_train, y_test = np.split(np.array(channel_y_list), [train_size])

            # X_train_all.append(X_train)
            # X_test_all.append(X_test)
            # y_train_all.append(y_train)
            # y_test_all.append(y_test)

            print(len(channel_y_listFFT_0))
            X = channel_y_listFFT_0[0:150]
            X_test = channel_y_listFFT_0[150:]

            y = trainingData[0][1][0:150]
            y_test = trainingData[0][1][150:]

        
        # X_train_all = np.concatenate(X_train_all)
        # X_test_all = np.concatenate(X_test_all)
        # y_train_all = np.concatenate(y_train_all)
        # y_test_all = np.concatenate(y_test_all)

        # print(X)
        # print(y_test)
        self.model.fit(np.real(X), y)

        results = self.model.predict(np.real(X_test))

        onehot_to_int = np.array([0,1,2,3,4])
        flat_y_test = (y_test*onehot_to_int).sum(axis=1)
        flat_results = (results*onehot_to_int).sum(axis=1)

        # rows represent true value, columns are predicted value
        self.confusion_matrix = confusion_matrix(flat_y_test, flat_results)
        print(self.confusion_matrix)

    def classify(self, observation):
        pass
