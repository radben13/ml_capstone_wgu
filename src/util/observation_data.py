import streamlit as st
from snowflake.snowpark.functions import col, iff
from src.util.snowflake_connect import get_session


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
def get_weather_classifications():
    return get_session().table('cleaned_station_observations')\
        .where(col('had_own_weather_cond_code'))\
        .group_by(col('is_severe'))\
        .count()\
        .select(iff(col('is_severe'), 'High Risk', 'Low Risk').alias('severity'), col('count'))\
        .to_pandas()
