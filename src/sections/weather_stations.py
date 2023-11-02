import streamlit as st

from src.util.station_data import get_mapped_stations, get_stations
from src.util.geo_position import get_states
from classes.united_states import UnitedStates
from snowflake.snowpark.functions import col, random
from src.util.snowflake_connect import get_session
import altair as alt
import pydeck as pdk


ws_heading_1 = """
### Data Format

As displayed below in this table, there are many fields that can be retrieved
about a particular weather station. This is a small subset of the values that
can be retrieved, and only a tiny fraction of the stations nationwide.
"""

ws_heading_2 = """
For weather severity prediction, the most helpful datapoints are the following:

- Elevation
- Latitude and Longitude

The following chart shows the distribution of the stations that provide data
to Synoptic (and thanks to their API, this project) across the country.

"""

ws_heading_3 = """

A helpful visual of the stations across the country can be viewed with the following
interactive map:

"""


def append_stations(layers, state = None):
    radius = 1500
    if state:
        data = get_mapped_stations(state['STATE_ID'])
    else:
        data = get_mapped_stations()
    layers.append(pdk.Layer(
        'ScatterplotLayer',
        data,
        get_position='[LONGITUDE, LATITUDE]',
        get_color='[200, 30, 0, 200]',
        get_radius=radius
    ))

def get_view_state(state = None):
    if state:
        lat = state['LATITUDE']
        lon = state['LONGITUDE']
        zoom = 6
    else:
        lat = UnitedStates.POSITION.latitude
        lon = UnitedStates.POSITION.longitude
        zoom = 3
    return pdk.ViewState(zoom=zoom, latitude=lat, longitude=lon)

def get_state_selector():
    state = None
    states = get_states()
    state_options = states[['STATE_NAME', 'STATE_ID']].sort_values('STATE_NAME').reset_index(drop=True)
    state_options.loc[-1] = ['None', '']
    state_options = state_options.sort_index()
    selected_state = st.selectbox('State', state_options)
    if selected_state in states['STATE_NAME'].to_list():
        state = states.set_index('STATE_NAME').to_dict(orient='index')[selected_state]
    return state

def show_weather_station_data():
    # Station sample
    st.write(ws_heading_1)
    st.dataframe(get_stations().order_by(random(1)).limit(100))
    # Stations per state
    st.write(ws_heading_2)
    stations = get_stations().select(col('county'), col('state')).to_pandas()
    st.altair_chart(alt.Chart(stations)
        .mark_bar()
        .encode(
            alt.X('STATE'),
            alt.Y(aggregate='count', title='Count of Stations'),
        )
        , use_container_width=True
    )
    # Interactive Map
    st.write(ws_heading_3)
    state = get_state_selector()
    local_layers = []
    append_stations(local_layers, state)
    view_state = get_view_state(state)
    mapDeck = pdk.Deck(
        map_style=None,
        initial_view_state=view_state,
        layers=local_layers
    )
    st.pydeck_chart(mapDeck)
