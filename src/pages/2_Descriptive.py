import streamlit as st

from src.sections.weather_stations import show_weather_station_data
from src.sections.weather_observations import show_weather_observation_data, show_weather_condition_data
from src.util.geo_position import get_states
from src.util.section_tools import create_section_button, init_sections


sections = {
    '2_station': 'Weather Station Data',
    '2_geographic': 'Geographic Data',
    '2_conditions': 'Weather Condition Data',
    '2_analysis': 'Data Analysis'
}
init_sections(sections)

"""
# Descriptive

This section describes the data retrieved and the information we can glean from its
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
Many governments facilitate this weather collection through airports or other locations.

Feel free to examine some weather station data for many that are found within the United States.

_All Weather Station Data was retrieved from Synoptic's Weather API_

"""

create_section_button('2_station', sections)

if st.session_state['2_station']:
    show_weather_station_data()

"""
## Geographic Data

The Geographic Data was pretty simple to set up. The majority of the geographic data concerns
the states within the United States.

The data compiled for the states was constructed by averaging the latitude and longitude of the
stations within each state. This resulted in a fairly simple implementation of state coordinates
for navigation on the map, but it didn't play a factor in the machine learning algorithm.

"""

create_section_button('2_geographic', sections)

if st.session_state['2_geographic']:
    st.dataframe(get_states(), use_container_width=True)


"""

## Weather Observation Data

The weather observation data all came from Synoptic's Weather API, and it includes some data points
that are measured values, and other data points that are observations of the conditions of weather.

### Measured Data Points

The material measured data points used in the application include:

- Air Temperature
- Relative Humidity
- Air Pressure
- Wind Speed
- Dew Point Temperature
- Elevation
- Altimeter

### Observed Conditions

The observed conditions are classifications of the current weather at that station's location.
The list of potential conditions reported can be retrieved from
[Synoptic's Weather API documentation](https://docs.synopticdata.com/services/weather-condition-codes)
but the values leveraged by this application are only those that were observed by stations within
the US for the 10 days of data retrieved for this app (from October 15th to October 25th of 2023).

"""


create_section_button('2_conditions', sections)
if st.session_state['2_conditions']:
    show_weather_condition_data()


"""
## Data Analysis

The correlations of the different environmental variables and their influence on the outcoming weather
conditions are complex. Simple analysis of the data makes it hard to see any direct relationships,
but with aggregated weather data, some relationships can start to display.

Please explore the relationships of environment variables and the frequency of severe weather
occurring with those different values.
"""


create_section_button('2_analysis', sections)
if st.session_state['2_analysis']:
    show_weather_observation_data()
