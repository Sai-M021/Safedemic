import pandas as pd
import geopy.distance
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
import math
import pickle

''' Dataset obtained from: https://github.com/CSSEGISandData/COVID-19.git
    Using file "time_series_covid19_confirmed_US.csv
'''
''' https://www.ncdc.noaa.gov/monitoring-references/maps/us-climate-regions.php
    Central = 0, East North Central = 1, Northeast = 2, Northwest = 3, South = 4, Southeast = 5, Southwest = 6, West = 7, West North Central = 8'''
state_to_region = {0 : ["Illinois", "Indiana", "Kentucky", "Missouri", "Ohio" ,"Tennessee", "West Virginia"],
                   1 : ["Iowa", "Michigan",  "Minnesota", "Wisconsin",],
                   2 : ["Connecticut", "Delaware","Maine" ,"Maryland" ,"Massachusetts", "New Hampshire","New Jersey","New York","Pennsylvania", "Rhode Island", "Vermont"],
                   3 : ["Idaho","Oregon", "Washington"],
                   4 : ["Arkansas","Kansas","Louisiana","Mississippi","Oklahoma", "Texas"],
                   5 : ["Alabama","Florida","Georgia","North Carolina","South Carolina", "Virginia"],
                   6 : ["Arizona","Colorado","New Mexico", "Utah"],
                   7 : ["California", "Nevada"],
                   8 : ["Montana","Nebraska" ,"North Dakota" ,"South Dakota", "Wyoming"]
                   }


def get_datapoints_inside_region_circular(df:pd.core.frame.DataFrame, radius:float, ref_coords:tuple) -> list:
    ''' radius is in kilometers '''
    region_indicies = []
    for i in range(df.shape[0]):
        if math.isnan(df.loc[i, 'Lat']) or math.isnan(df.loc[i, 'Long_']): continue
        coords = (df.loc[i, 'Lat'], df.loc[i, 'Long_'])
        if geopy.distance.geodesic(ref_coords, coords).km < radius:
            region_indicies.append(i)
    return region_indicies


def get_datapoints_inside_region_climate(df:pd.core.frame.DataFrame, region:int) -> list:
    region_indicies = []
    for i in range(df.shape[0]):
        if df.loc[i, "Province_State"] in state_to_region[region]:
            region_indicies.append(i)
    return region_indicies


def print_locations_given_indicies(df:pd.core.frame.DataFrame, indicies:list) -> None:
    print('%i Locations in this Region: ' % len(indicies))
    for i in indicies:
        print(df.loc[i, 'Combined_Key'])


def plot_confirmed_cases(df:pd.core.frame.DataFrame, city_index:int, tick_interval=20) -> None:
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    y = list(df.loc[city_index, '1/22/20':])
    x = [datetime.datetime(2020, 1, 22) + datetime.timedelta(days=i) for i in range(len(y))]
    plt.plot(x, y)
    plt.xlabel('Confirmed Cases')
    plt.ylabel('Time')
    plt.title(df.loc[city_index, 'Combined_Key'])
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=tick_interval))
    plt.show()


def convert_to_dataset_with_region_indicies(df:pd.core.frame.DataFrame, region_indicies: list, region_name:str, save=True) -> np.array:
    df_region = df.iloc[region_indicies, :]
    df_region = df_region.T
    df_region_data = df_region.loc['1/22/20':, :].values #only take confirmed cases information
    #print(df_region_data)
    if save:
        np.save('./RegionData/' + region_name + '_confirmed_cases_data.npy', df_region_data)
    return df_region_data


def get_region_from_state(state:str) -> int:
    for region in state_to_region:
        if state in state_to_region[region]: return region
    return -1


def create_region_and_city_to_index_dict(df:pd.core.frame.DataFrame, save_dict=True) -> dict:
    index_counter = [0 for i in range(len(state_to_region))]
    region_and_city_to_index = {}
    for i in range(df.shape[0]):
        region = get_region_from_state(df.loc[i, "Province_State"])
        if region == -1: continue
        region_and_city_to_index[(region, df.loc[i, 'Combined_Key'])] = index_counter[region]
        index_counter[region] += 1
    if save_dict:
        pickle_out = open("region_and_city_to_index.dict", "wb")
        pickle.dump(region_and_city_to_index, pickle_out)
        pickle_out.close()
    print(region_and_city_to_index)
    return region_and_city_to_index


def main():
    ''' Draw out 8-9 regions that encompass the US mainland. Sort all datapoints into these regions and use them to train separate ML models.
        Theory behind this is that one datapoints confirmed cases will only effect nearby areas.
        Do regions based on what state the datapoint is in as opposted to location.
    '''

    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv' #replace with better pointer
    ts_covid19_US = pd.read_csv(url, error_bad_lines=False)

    ''' Creates datasets for each region on the mainland US '''
    '''for region_num in state_to_region:
        region_indicies = get_datapoints_inside_region_climate(ts_covid19_US, region_num)
        region_name = 'Region' + str(region_num)
        convert_to_dataset_with_region_indicies(ts_covid19_US, region_indicies, region_name)'''
    '''pickle_in = open("region_and_city_to_index.dict", "rb")
    region_and_city_to_index = pickle.load(pickle_in)
    print(region_and_city_to_index)'''


    #create_region_and_city_to_index_dict(ts_covid19_US)


main()