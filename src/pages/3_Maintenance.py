import streamlit as st

from src.util.file_tools import get_asset_path

with open(get_asset_path('invertocat.svg.data')) as f:
    invertocat_svg = f.read()

"""
## Maintenance &amp; Monitoring

**Maintenance**

For this application, if this were going to be adopted by an organization, it has a lot going for it already.
For maintenance of the application, this exists within a Github Repository:

[![GitHub Invertocat](""" + invertocat_svg + """)](https://github.com/radben13/ml_capstone_wgu)
[radben13/ml_capstone_wgu](https://github.com/radben13/ml_capstone_wgu)

The data lives in an industry-leading data warehouse tool, Snowflake. If something were to cause the loss of access,
to Snowflake, however, the 2 Gigabytes of data is preserved in AWS S3 as [a zip file](https://braden-personal-public.s3.amazonaws.com/wgu/observations.zip).

The ability to adjust this application is also heightened by its existing on a flexible framework, Streamlit.
Streamlit isn't bound to Streamlit Cloud. It can also be deployed on private servers.

**Monitoring**

Snowflake and the Streamlit both provide monitoring resources for their platforms.

Snowflake has detailed logs of queries, storage, computation, and computation. It's an analytics database
with its own logs available to be analyzed.

"""

st.image(get_asset_path('snowflake_query_history.png'))
st.image(get_asset_path('snowflake_usage.png'))

"""
Snowflake's usage charts, [built in alerting and notifications](https://docs.snowflake.com/en/guides-overview-alerts),
and other monitoring tools make it a strong contender to stay as this application grows or
gets more traffic.


Streamlit has a simple way to view the analytics of a user's app. It isn't overly complex,
but for such a light and simple deployment experience, it's sufficient.
They also have helpful logging in the cloud and the console (when running locally).

"""

str_col1, str_col2 = st.columns([0.7, 0.3])
with str_col1:
    st.image(get_asset_path('streamlit_analytics.png'))
with str_col2:
    st.image(get_asset_path('streamlit_analytics_menu.png'))
st.image(get_asset_path('streamlit_logs.png'))