import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from snowflake.snowpark.functions import col
from snowflake_connect import get_session as get_sf_session

st.title('Weather Severity Prediction')

def get_session():
    return get_sf_session()

@st.cache_resource
def get_states():
    return get_session().table('states').to_pandas()

@st.cache_resource
def get_stations():
    return get_session().table('weather_stations').to_pandas()

@st.cache_resource
def get_informed_weather_codes():
    return get_session().table('informed_weather_codes').to_pandas()

@st.cache_resource
def get_severe_weather_data():
    return get_session().table('cleaned_station_observations')\
        .where((col('is_severe')))\
        .to_pandas()
#  & (col('had_own_weather_cond_code')))

states = get_states()
stations = get_stations()

map_modes = {
    'Weather Stations': 'stations',
    'Severe Weather': 'severe_weather',
}

map_mode = map_modes[st.radio('Map Mode', map_modes)]

selected_state = st.selectbox('State', states['STATE_NAME'].sort_values())
state = states.set_index('STATE_NAME').to_dict(orient='index')[selected_state]

layers = []
if map_mode == 'stations':
    layers.append(pdk.Layer(
        'ScatterplotLayer',
        stations.where(lambda i : i['STATE'] == state['STATE_ID']).dropna()[['LONGITUDE', 'LATITUDE']],
        get_position='[LONGITUDE, LATITUDE]',
        get_color='[200, 30, 0, 160]',
        get_radius=1000
    ))
elif map_mode == 'severe_weather':
    severe_weather = get_severe_weather_data()# .where(lambda i : i['STATE'] == state['STATE_ID'])[['LONGITUDE', 'LATITUDE', 'HAD_OWN_WEATHER_COND_CODE']].dropna()
    st.write(state)
    st.write(severe_weather)
    layers.append(pdk.Layer(
        'ScatterplotLayer',
        severe_weather,
        get_position='[LONGITUDE, LATITUDE]',
        get_color='[200, 30, HAD_OWN_WEATHER_COND_CODE ? 0 : 250, HAD_OWN_WEATHER_COND_CODE ? 255 : 50 / (METERS_DISTANCE / 20000)]',
        get_radius='HAD_OWN_WEATHER_COND_CODE ? 5000 : 10000'
    ))

mapDeck = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        zoom=6,
        latitude=state['LATITUDE'],
        longitude=state['LONGITUDE']
    ),
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
st.subheader('Raw data')
st.write(stations)

st.write(get_informed_weather_codes())
