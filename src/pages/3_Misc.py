import streamlit as st

from src.util.file_tools import get_asset_path

with open(get_asset_path('invertocat.svg.data')) as f:
    invertocat_svg = f.read()

"""
# Miscellaneous

Any additional details for the capstone project management.

## Maintenance &amp; Monitoring

For maintenance of the application, this exists within a Github Repository:

[![GitHub Invertocat](""" + invertocat_svg + """)](https://github.com/radben13/ml_capstone_wgu)
[radben13/ml_capstone_wgu](https://github.com/radben13/ml_capstone_wgu)

The data lives in Snowflake, which will cease to be the case when the project reaches its conclusion. However,
the data exists in [a zip file](https://braden-personal-public.s3.amazonaws.com/wgu/observations.zip).

While Snowflake and the Streamlit application are active, monitoring can be handled in a few places. Snowflake has
a wide variety of monitoring tools, both for query activity and infrastructure work done behind the scenes 
(these can include computation and storage costs).

"""

st.image(get_asset_path('snowflake_query_history.png'))
st.image(get_asset_path('snowflake_usage.png'))


str_col1, str_col2 = st.columns([0.7, 0.3])
with str_col1:
    st.image(get_asset_path('streamlit_analytics.png'))
with str_col2:
    st.image(get_asset_path('streamlit_analytics_menu.png'))