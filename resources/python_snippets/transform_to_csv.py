import pandas as pd

def get_observation_values(data):
    obs = list()
    if 'STATION' not in data:
        raise ValueError(data)
    for stat in data['STATION']:
        for i in range(len(stat['OBSERVATIONS']['date_time'])):
                dt = stat['OBSERVATIONS']['date_time'][i]
                for dp in stat['OBSERVATIONS']:
                        dpv = [
                            stat['STID'],
                            str(dt),
                            str(dp),
                            str(stat['OBSERVATIONS'][dp][i])
                        ]
                        if dp == 'date_time':
                                continue
                        obs.append(dpv)
    return (pd.DataFrame(obs, columns=[
                'STID',
                'DATE_TIME',
                'VARIABLE',
                'VALUE'
            ])
            .set_index(['STID', 'DATE_TIME', 'VARIABLE'])
        )