from __future__ import print_function, division

import numpy as np
import keras
from keras.layers import Convolution1D, Dense, MaxPooling1D, Flatten, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import Sequential
import matplotlib.pyplot as plt
import os
import pickle

''' Implemented code from GitHub user: jkleint; 
    Link: https://gist.github.com/jkleint/1d878d0401b28b281eb75016ed29f2ee
'''

def make_timeseries_regressor(window_size:int, filter_length:int, nb_input_series=1, nb_outputs=1, nb_filter=4):
    model = Sequential((
        Convolution1D(nb_filter=nb_filter, filter_length=filter_length, activation='relu',
                      input_shape=(window_size, nb_input_series)),
        Dropout(0.30),
        Convolution1D(nb_filter=nb_filter // 2, filter_length=filter_length // 2, activation='relu'),
        MaxPooling1D(),
        Convolution1D(nb_filter=nb_filter // 6, filter_length=filter_length // 6, activation='relu'),
        MaxPooling1D(),
        Flatten(),
        Dense(150, activation='relu'),
        Dense(nb_outputs, activation='linear'),  # For binary classification, change the activation to 'sigmoid'
    ))
    model.compile(loss='mse', optimizer='adam', metrics=['mae'])
    return model


def make_timeseries_instances(timeseries:np.array, window_size:int) -> tuple:
    ''' the X-data '''
    timeseries = np.asarray(timeseries)
    assert 0 < window_size < timeseries.shape[0]
    X = np.atleast_3d(
        np.array([timeseries[start:start + window_size] for start in range(0, timeseries.shape[0] - window_size)]))
    y = timeseries[window_size:]
    q = np.atleast_3d([timeseries[-window_size:]])
    return X, y, q


def evaluate_timeseries(timeseries:np.array, window_size:int):
    global region_num
    model_save_file = 'region' + str(region_num) + '_confirmed_cases_modeltst.h5'
    filter_length = 8
    nb_filter = 10
    timeseries = np.atleast_2d(timeseries)
    if timeseries.shape[0] == 1:
        timeseries = timeseries.T  # Convert 1D vectors to 2D column vectors

    nb_samples, nb_series = timeseries.shape

    if os.path.isfile(model_save_file):
        model = keras.models.load_model(model_save_file)
    else:
        model = make_timeseries_regressor(window_size=window_size, filter_length=filter_length,
                                          nb_input_series=nb_series, nb_outputs=nb_series, nb_filter=nb_filter)

    model.summary()

    X, y, q = make_timeseries_instances(timeseries, window_size)
    X_train, y_train = X, y

    patience = EarlyStopping(monitor='val_loss', patience=150)
    checkpoint = ModelCheckpoint(model_save_file, monitor='loss', verbose=1, save_best_only=True, mode='auto')

    model.fit(X_train, y_train, nb_epoch=1, batch_size=8, verbose=2, callbacks=[checkpoint, patience])
    model = keras.models.load_model(model_save_file)
    pred = model.predict(X_train)

    return y_train, pred


def display_prediction_results(y_true:np.array, pred:np.array, test_cities:list) -> None:
    ''' example test_cities=["Boone, Kentucky, US", "Cook, Illinois, US", "Hancock, Ohio, US", "Holmes, Ohio, US"] for region 0'''
    pickle_in = open("region_and_city_to_index.dict", "rb")
    region_and_city_to_index = pickle.load(pickle_in)
    global region_num
    for city_name in test_cities:
      test_ind = region_and_city_to_index[(region_num, city_name)]
      plt.title(city_name)
      plt.xlabel('Days')
      plt.ylabel('Confirmed Cases')
      plt.plot(y_true[:, test_ind], 'b', label='Real')
      plt.plot(pred[:, test_ind], 'r', label='Predicted')
      plt.legend()
      plt.show()


def final_run():
    ''' Trains the ML model given a specific region number which the user can change. '''
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    np.set_printoptions(threshold=25)
    global region_num
    region_num = 0
    timeseries = np.load('./RegionData/Region' + str(region_num) + '_confirmed_cases_data.npy', allow_pickle=True)
    window_size = 14 #uses previous 2 weeks of data to predict the next data point
    '''In order to use this model to predict, get the past 2 weeks of corona virus data for a region in a list. time on rows, locations on columns, elements are #confirmed cases'''
    y_train, pred = evaluate_timeseries(timeseries, window_size)
    return y_train, pred


y_true, pred = final_run()
#can use these two variables to plot the predictive results for a particular city
test_cities = ["Boone, Kentucky, US", "Cook, Illinois, US", "Hancock, Ohio, US", "Holmes, Ohio, US"] #example of city prediction plot visualization
display_prediction_results(y_true, pred, test_cities)