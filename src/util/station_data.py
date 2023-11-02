
import streamlit as st

from snowflake.snowpark.functions import col
from src.util.snowflake_connect import get_session
from src.util.geo_position import apply_state_filter

@st.cache_resource
def get_stations(state_id = None):
    stations = get_session().table('weather_stations')
    return apply_state_filter(stations, state_id)


@st.cache_resource
def get_mapped_stations(state_id = None):
    stations = get_session().table('weather_stations')
    return apply_state_filter(stations, state_id)\
            .select(col('latitude'), col('longitude'))\
            .to_pandas()
