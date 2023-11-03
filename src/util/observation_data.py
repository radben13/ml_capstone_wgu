import streamlit as st
from snowflake.snowpark.functions import col, iff, round as sf_round, expr
from src.util.snowflake_connect import get_session
import pandas as pd


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


@st.cache_resource
def get_weather_observation_data(column: str):
    data = get_session().table('cleaned_station_observations')\
        .select(
            # sf_round(col(column)).alias(column)
            col(column)
            , col('had_own_weather_cond_code')
            , col('is_severe'))\
        .where(col('had_own_weather_cond_code'))\
        .to_pandas()
    # Count where IS_SEVERE is true
    severe_counts = data[data['IS_SEVERE']].groupby(column).size().rename('IS_SEVERE_COUNT')
    # Total counts
    total_counts = data.groupby(column).size().rename('TOTAL_COUNT')
    # Combine data
    result = pd.concat([severe_counts, total_counts], axis=1).reset_index()
    # Calculate percentage
    result['SEVERE_PERCENT'] = result['IS_SEVERE_COUNT'].truediv(result['TOTAL_COUNT'], fill_value=0)
    # Clean up pandas
    result = result.dropna().reset_index()
    result['IS_SEVERE_COUNT'] = result['IS_SEVERE_COUNT'].astype(int)
    result['SEVERE_PERCENT'] = result['SEVERE_PERCENT'].astype(float)
    result[column] = result[column].astype(float)
    return result


@st.cache_resource
def get_weather_training_data():
    data = get_session().table('cleaned_station_observations')\
        .where(col('had_own_weather_cond_code'))\
        .select(
            col('is_severe'),
            col('air_temp'),
            col('pressure'),
            col('dew_point_temperature'),
            col('relative_humidity'),
            col('elevation'),
            col('wind_speed'),
            col('altimeter'),
            col('latitude'),
            col('longitude'),
            col('date_time'),
            col('station_id')
        )\
        .order_by(expr('random(1)'))\
        .drop('date_time', 'station_id')\
        .to_pandas()
    return data
