
import os
from datetime import datetime,timedelta
import pandas as pd
import requests as req

WS_TOKEN = os.environ['WS_TOKEN']

observation_variables = [
    'air_temp',
    'weather_condition',
    'pressure',
    'altimeter',
    'heat_index',
    'relative_humidity',
    'wind_speed',
    'weather_cond_code',
    'weather_summary',
    'wind_chill',
    'dew_point_temperature'
]
time_format = '%Y%m%d%H%M'

def get_weather_data_for_time(start:datetime, end:datetime=None, interval:dict=None, stations=[], vars=observation_variables, state='', country=''):
    if end is None and interval is None:
        raise ValueError('Either end datetime or interval options are required')
    elif end is None:
        end = start + timedelta(**interval)
    url = f'https://api.synopticdata.com/v2/stations/timeseries?token={WS_TOKEN}&units=english'
    url += f'&start={start.strftime(time_format)}&end={end.strftime(time_format)}'
    if len(stations):
        url += f'&stid={str.join(",", stations)}'
    if len(vars):
        url += f'&vars={str.join(",", vars)}'
    if len(state):
        url += f'&state={state}'
    if len(country):
        url += f'&country={country}'
    return req.get(url).json()

def get_observation_values(data):
    obs = list()
    if 'STATION' not in data:
        raise ValueError(data)
    for stat in data['STATION']:
        for i in range(len(stat['OBSERVATIONS']['date_time'])):
                dt = stat['OBSERVATIONS']['date_time'][i]
                for dp in stat['OBSERVATIONS']:
                        dpv = [stat['STID'], str(dt), str(dp), str(stat['OBSERVATIONS'][dp][i])]
                        if dp == 'date_time':
                                continue
                        obs.append(dpv)
    return (pd.DataFrame(obs, columns=['STID', 'DATE_TIME', 'VARIABLE', 'VALUE'])
            .set_index(['STID', 'DATE_TIME', 'VARIABLE'])
        )

def get_observations_for_interval(start:datetime, end:datetime=None, interval:dict=None, chunk:dict={'minutes': 5}):
    if end is None and interval is None:
        raise ValueError('Either end datetime or interval options are required')
    elif end is None: 
        end = start + timedelta(**interval)
    chunk_suffix = '_'.join([f'{k}_{v}' for k,v in chunk.items()])
    while start < end:
        print(f'Retrieving data for {start.strftime(time_format)}_{chunk_suffix}.csv')
        data = get_weather_data_for_time(start, interval=chunk, country='US')
        print(f'Parsing data for {start.strftime(time_format)}_{chunk_suffix}.csv')
        values = get_observation_values(data)
        del data
        print(f'Saving data for {start.strftime(time_format)}_{chunk_suffix}.csv')
        with open(f'./data/observations/{start.strftime(time_format)}_{chunk_suffix}.csv', 'w') as f:
            f.write(values.to_csv())
        del values
        start += timedelta(**chunk)

    print('Complete!')
