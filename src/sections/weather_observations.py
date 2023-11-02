import streamlit as st
from src.util.observation_data import get_weather_classifications, get_informed_weather_codes
import altair as alt

def tb_floor(row):
    row['CODE'] = round(row['CODE'])
    return row

wo_header_1 = """
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
- Altimeter

### Observed Conditions

The observed conditions are classifications of the current weather at that station's location.
The list of potential conditions reported can be retrieved from
[Synoptic's Weather API documentation](https://docs.synopticdata.com/services/weather-condition-codes)
but the values leveraged by this application are only those that were observed by stations within
the US for the 10 days of data retrieved for this app (from October 15th to October 25th of 2023).

Here are the values seen:

**Weather Condition Codes**
"""



wo_header_2 = """
An eagle-eyed reader might see the addition of `IS_SEVERE` and `SEVERE_REASON` to this table.
In an effort to create a tool that can predict "high risk" of severe weather, data needs to be
classification as "high risk." While I would have preferred to classify "high risk" as something
more dangerous, like tornadoes, funnel clouds, and water spouts (which are present in the larger
collection of potential codes), it wouldn't help to train a machine learning algorithm on data
I don't have.

With the limited data I have at present, the best I could do is to train a model to predict the
high risk of the _more severe_ conditions. For that purpose, I classified 15 of the available
conditions as "severe"; this resulted in the following distribution of high risk classification
to the reported weather conditions:
"""

def show_classification_pie():
    base = alt.Chart(get_weather_classifications()).encode(
        alt.Theta("COUNT:Q").stack(True),
        alt.Color("SEVERITY:N").legend(None)
    )
    pie = base.mark_arc(outerRadius=120)
    text = base.mark_text(radius=140, size=20).encode(text="SEVERITY:N")
    st.altair_chart(
        pie + text
    , use_container_width=True)

def show_weather_observation_data():
    st.write(wo_header_1)
    st.dataframe(get_informed_weather_codes().apply(tb_floor, axis=1))
    st.write(wo_header_2)
    show_classification_pie()
