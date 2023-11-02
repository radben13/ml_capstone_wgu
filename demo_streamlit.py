import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from snowflake.snowpark.functions import col, floor as sn_floor
from snowflake.snowpark import DataFrame
from snowflake_connect import get_session as get_sf_session

from src.classes.united_states import UnitedStates

st.title('Weather Severity Prediction')

def apply_state_filter(df: DataFrame, state_id = None):
    if state_id:
        return df.where(col('state') == state_id)
    return df

def get_session():
    return get_sf_session()

@st.cache_resource
def get_states():
    return get_session().table('states').to_pandas()

@st.cache_resource
def get_mapped_stations(state_id = None):
    stations = get_session().table('weather_stations')
    return apply_state_filter(stations, state_id)\
            .select(col('latitude'), col('longitude'))\
            .to_pandas()

@st.cache_resource
def get_informed_weather_codes():
    with get_session() as session:
        codes = session.table('observed_weather_codes')
        table = session.table('informed_weather_codes')
        table = table.join(codes, on=col('code') == codes.col('code'), rsuffix='_2')
        table = table.select(col('code'), col('condition'), col('is_severe'), col('severe_reason'))
        table = table.to_pandas()
    return table


@st.cache_resource
def get_weather_data():
    return get_session().table('cleaned_station_observations')


map_modes = {
    'Weather Stations': 'stations',
    'Severe Weather': 'severe_weather',
}

map_mode = map_modes[st.radio('Map Mode', map_modes)]

if map_mode == 'stations':    
    states = get_states()
elif map_mode == 'severe_weather':
    severe_weather = get_weather_data().where(col('is_severe') & col('had_own_weather_cond_code'))


def append_stations(layers, state = None):
    if state:
        layers.append(pdk.Layer(
            'ScatterplotLayer',
            get_mapped_stations(state['STATE_ID']),
            get_position='[LONGITUDE, LATITUDE]',
            get_color='[200, 30, 0, 160]',
            get_radius=1000
        ))
    else:
        layers.append(pdk.Layer(
            'ScatterplotLayer',
            get_mapped_stations(),
            get_position='[LONGITUDE, LATITUDE]',
            get_color='[200, 30, 0, 160]',
            get_radius=1500
        ))



view_state = pdk.ViewState(
    zoom=3,
    latitude=UnitedStates.POSITION.latitude,
    longitude=UnitedStates.POSITION.longitude
)
state = None
layers = []
if map_mode in ['stations']:
    state_options = states[['STATE_NAME', 'STATE_ID']].sort_values('STATE_NAME').reset_index(drop=True)
    state_options.loc[-1] = ['None', '']
    state_options = state_options.sort_index()
    selected_state = st.selectbox('State', state_options)
    if selected_state in states['STATE_NAME'].to_list():
        state = states.set_index('STATE_NAME').to_dict(orient='index')[selected_state]
        view_state = pdk.ViewState(
            zoom=6,
            latitude=state['LATITUDE'],
            longitude=state['LONGITUDE']
        )
    append_stations(layers, state)
elif map_mode == 'severe_weather':
    mapped_severe_weather = severe_weather.select(col('latitude'), col('longitude')).to_pandas()
    layers.append(pdk.Layer(
        'ScatterplotLayer',
        mapped_severe_weather,
        get_position='[LONGITUDE, LATITUDE]',
        get_color='[200, 30, 255, 255]',
        get_radius='5000'
    ))

mapDeck = pdk.Deck(
    map_style=None,
    initial_view_state=view_state,
    layers=layers
)
st.pydeck_chart(mapDeck)

# st.altair_chart(alt.Chart(example_data)    
#         .mark_bar()
#         .encode(
#             alt.X('Labels').axis(labelAngle=0),
#             alt.Y('Values').title(None))
#     , use_container_width=True
# )


def tb_floor(row):
    row['CODE'] = round(row['CODE'])
    return row


st.table(get_informed_weather_codes().apply(tb_floor, axis=1))
