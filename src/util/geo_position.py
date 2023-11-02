import streamlit as st
from src.util.snowflake_connect import get_session
from snowflake.snowpark.functions import col
from snowflake.snowpark import DataFrame
from collections import namedtuple

Position = namedtuple('Position', ['latitude', 'longitude'])

@st.cache_resource
def get_states():
    return get_session().table('states').to_pandas()

def apply_state_filter(df: DataFrame, state_id = None):
    if state_id:
        return df.where(col('state') == state_id)
    return df
