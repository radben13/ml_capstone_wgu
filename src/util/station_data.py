
import streamlit as st
from snowflake.snowpark.functions import col, expr, random
from src.util.snowflake_connect import get_session
from src.util.geo_position import apply_state_filter

@st.cache_resource
def get_stations(state_id = None):
    stations = get_session().table('weather_stations')
    return apply_state_filter(stations, state_id)\
        .order_by(random(1)).limit(100)\
        .to_pandas()


@st.cache_resource
def get_mapped_stations(state_id = None):
    stations = get_session().table('weather_stations')
    return apply_state_filter(stations, state_id)\
            .select(col('latitude'), col('longitude'))\
            .to_pandas()

@st.cache_resource
def get_graphed_stations():
    return get_session()\
        .table('cleaned_station_observations')\
        .group_by('station_id', 'county', 'state')\
        .agg(
            expr('boolor_agg(had_own_weather_cond_code)').alias('REPORTS_WEATHER_CONDITONS')
        )\
        .select('station_id', 'county', 'state', 'REPORTS_WEATHER_CONDITONS')\
        .to_pandas()
