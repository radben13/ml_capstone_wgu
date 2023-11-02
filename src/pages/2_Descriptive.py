import streamlit as st

from src.sections.weather_stations import show_weather_station_data
from src.sections.weather_observations import show_weather_observation_data
from src.util.geo_position import get_states

def toggle_weather_stations():
    if 'weather_station_init' in st.session_state:
        st.session_state['weather_station_init'] = not st.session_state['weather_station_init']
    else:
        st.session_state['weather_station_init'] = True

"""
# Descriptive

This section describes the data retrieved, and the information we can glean from its
exploration. There are a few categories of information analyzed and used for this capstone:

- Weather Station Data
- Geographic Data
- Weather Observation Data
    - Measured Data Points
    - Observed Conditions

Let's break these down to be more clear.

## Weather Station Data

Across the world, weather data providers have established weather stations to measure the environment
around them. For much of the weather data providers, they share the data publicly as a public service.
Many governments facilitate this weather collection through air ports or other locations.

Feel free to examine some weather station data for many that are found within the United States.

_All Weather Station Data was retrieved from Synoptic's Weather API_

"""

if 'weather_station_init' not in st.session_state:
    st.session_state['weather_station_init'] = False

if not st.session_state['weather_station_init']:
    st.button('View Weather Station Data', on_click=toggle_weather_stations)
else:
    st.button('Close Weather Station Data', on_click=toggle_weather_stations)
    show_weather_station_data()

"""
## Geographic Data

The Geographic Data was pretty simply set up. Starting with the data about the states within the
Union, the following is their data:

"""

st.dataframe(get_states(), use_container_width=True)


"""
The data compiled for the states was constructed by averaging the latitude and longitude of the
stations within each state. This resulted in a fairly implementation of maps being able to navigate,
but it didn't play a factor in the machine learning algorithm.
"""

show_weather_observation_data()
