import pandas as pd
import os
import threading
from datetime import datetime
from util.snowflake_connect import get_session as get_sf_session

def get_session():
    return get_sf_session()

def pull_observation_data(path: str):
    for obs_path in list(os.walk(path))[0][2]:
        data_path = f'{path}/{obs_path}'
        with open(data_path) as f:
            obv_data = pd.read_csv(f).astype({'VALUE': 'str'})
        print(f'data for {obs_path}: {obv_data.size}')
        print(obv_data.head())
        yield obv_data

session = None
def upload_pd_as_table(data: pd.DataFrame, table_name: str, cache_session=False):
    global session
    session = (cache_session and session) or get_session()
    print(f'start loading {data.size} at {datetime.now().strftime("%H:%M:%S")}')
    df = session.create_dataframe(data=data.values.tolist(), schema=data.columns.to_list())
    df.write.mode('append').save_as_table(table_name)
    print(f'finished loading {data.size} at {datetime.now().strftime("%H:%M:%S")}')
    if not cache_session:
        session.close()

threads = list()
for data in pull_observation_data('./data/observations'):
    new_thread = threading.Thread(target=upload_pd_as_table, args=(data, 'observations', True))
    new_thread.start()
    threads = [new_thread] + threads
    if len(threads) == 3:
        while(len(threads) == 3):
            threads.pop().join()


while(len(threads)):
    threads.pop().join()

print('finished!')
