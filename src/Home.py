import streamlit as st

from src.util.file_tools import get_asset_path

with open(get_asset_path('invertocat.svg.data')) as f:
    invertocat_svg = f.read()

"""
# Weather Severity Prediction
by Braden Van Wagenen &mdash; Student ID: 001345438

The following is a Streamlit application created for my WGU Computer Science Capstone.

The application is powered by [Streamlit Cloud](https://streamlit.io/cloud), a free resource for
hosting [Streamlit](https://streamlit.io/) applications. It is also leveraging
[Snowflake](https://www.snowflake.com/en/) and its
[Snowpark Python resources](https://docs.snowflake.com/en/developer-guide/snowpark/python/index).

All data used in the application comes from [Synoptic](https://synopticdata.com/), a Public Benefit
organization with a [Weather API](https://synopticdata.com/weatherapi/) that enables the retrieval
of weather station observation data across the world. With the Open Access License, 1 year of historical
data is available for academic institutions or hobbyists to retrieve free of charge.

Feel free to navigate through this site or the GitHub repo, [![GitHub Invertocat](""" + invertocat_svg + """)](https://github.com/radben13/ml_capstone_wgu)
[radben13/ml_capstone_wgu](https://github.com/radben13/ml_capstone_wgu), to observe the capstone. The navigation is intentionally sorted in a
top-to-bottom order for ease of consumption, but there is no requirement for going in order.

"""



"""
---
"""
