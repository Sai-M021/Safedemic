import numpy as np
import keras
from keras.layers import Convolution1D, Dense, MaxPooling1D, Flatten, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.models import Sequential, load_model
import pickle
import csv
import pandas as pd
import os


def list_of_lists_to_csv(to_csv:list, filename:str) -> None:
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(to_csv)


def get_coordinates_from_combined_key(df:pd.core.frame.DataFrame, combined_key:str) -> tuple:
    '''dont use this.'''
    i = 0
    correct_ind = 0
    found = False
    while found is False:
        if df.loc[i, 'Combined_Key'] == combined_key:
            correct_ind = i
            found = True
        i += 1
    lat = df.loc[i, 'Lat']
    long = df.loc[i, 'Long_']
    return lat, long


def create_city_to_coordinates_dict(df:pd.core.frame.DataFrame, save=True) -> dict:
    city_to_coordinates = {}
    for i in range(df.shape[0]):
        city_to_coordinates[df.loc[i, 'Combined_Key']] = (df.loc[i, 'Lat'], df.loc[i, 'Long_'])
    if save:
        pickle_out = open("city_to_coordinates.dict", "wb")
        pickle.dump(city_to_coordinates, pickle_out)
        pickle_out.close()
    return city_to_coordinates



def main() -> None:
    '''Creates the num new cases prediction csv file that can be uploaded to the Web App for users to interact with'''
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    num_regions = 9
    model_list = [load_model('./models/region' + str(i) + '_confirmed_cases_model.h5') for i in range(num_regions)]
    region_data = [0 for _ in range(num_regions)]
    prediction_prevs = [0 for _ in range(num_regions)]
    prediction_posts = [0 for _ in range(num_regions)]
    window_size = 14
    for i in range(num_regions):
        region_data[i] = np.load('./RegionData/Region' + str(i) + '_confirmed_cases_data.npy', allow_pickle=True)
        p = np.atleast_3d([region_data[i][-(window_size+1):-1]])
        q = np.atleast_3d([region_data[i][-window_size:]])
        prediction_prevs[i] = model_list[i].predict(p).squeeze()
        prediction_posts[i] = model_list[i].predict(q).squeeze()

    pickle_in = open("region_and_city_to_index.dict", "rb")
    region_and_city_to_index = pickle.load(pickle_in)

    pickle_in2 = open("city_to_coordinates.dict", "rb")
    city_to_coordinates = pickle.load(pickle_in2)

    #url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv'  # replace with better pointer
    #ts_covid19_US = pd.read_csv(url, error_bad_lines=False)

    output_list = []
    for (region, city) in region_and_city_to_index:
        ind_in_pred = region_and_city_to_index[(region, city)]
        print(region, city, ind_in_pred)
        lat, long = city_to_coordinates[city]
        curr_prev_pred = round(prediction_prevs[region][ind_in_pred])
        curr_post_pred = round(prediction_posts[region][ind_in_pred])
        num_new_cases = curr_post_pred - curr_prev_pred
        output_list.append([lat, long, num_new_cases, city, region])
    print(output_list)
    list_of_lists_to_csv(output_list, 'prediction_num_new_cases_all_regions.csv')


main()