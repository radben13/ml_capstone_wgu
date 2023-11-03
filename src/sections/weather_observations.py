import streamlit as st
from src.util.observation_data import get_weather_classifications, get_informed_weather_codes, get_weather_observation_data
import altair as alt

def tb_floor(row):
    row['CODE'] = round(row['CODE'])
    return row

wo_header_1 = """

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

def show_weather_condition_data():
    st.write(wo_header_1)
    st.dataframe(get_informed_weather_codes().apply(tb_floor, axis=1), use_container_width=True)
    st.write(wo_header_2)
    show_classification_pie()

def get_environment_variable_options():
    return {
        'Air Temperature': 'AIR_TEMP',
        'Atmospheric Pressure': 'PRESSURE',
        'Dew Point Temperature': 'DEW_POINT_TEMPERATURE',
        'Relative Humidity': 'RELATIVE_HUMIDITY',
        'Elevation': 'ELEVATION',
        'Wind Speed': 'WIND_SPEED',
        'Altimeter': 'ALTIMETER'
    }


def show_weather_observation_data():
    options = get_environment_variable_options()
    col1, col2 = st.columns(2)
    with col1:
        selected_option = st.radio('Environment Variable', options)
    column = options[selected_option]
    result = get_weather_observation_data(column)
    with col2:
        st.altair_chart(
            alt.Chart(result).mark_point().encode(
                alt.X(f'{column}:Q').axis(title=selected_option).scale(alt.Scale(domain=[result[column].min(), result[column].max()])),
                alt.Y('SEVERE_PERCENT:Q')
                    .axis(format="%", title='Severe Weather Percent')
            ),
            use_container_width=True
        )
    st.write("""
    _**My's Reactions, Musings, and Questions in response to the data...**_
    """)
    if column == 'AIR_TEMP':
        st.write("""
> _Because the 10 days collected were within the latter half of October,
> it isn't very surprising that air temperature would have the increased
> presence of data in the mid 60 degrees Farenheit._
        """)
    elif column == 'WIND_SPEED':
        st.write("""
> _Many of the conditions that were classified as "Severe" were due to
> the presence of wind. It's no surpise then that there would be a correlation
> of wind speed with this data._
""")
    elif column == 'PRESSURE':
        st.write("""
> _Until it was displayed in this graph, I didn't anticipate seeing pressure
> so clearly indicate severe weather. This makes me suspect the machine learning
> model will notice that as well._
""")
    elif column == 'DEW_POINT_TEMPERATURE':
        st.write("""
> _It makes sense that as severe weather approaches, the amount of saturation in
> the air increases, lowering the dew-point temperature. This seems obvious now
> after seeing the data. Nonetheless, I didn't expect such a strong correlation._
""")
    elif column == 'RELATIVE_HUMIDITY':
        st.write("""
> _Relative Humidity would make sense with some storms. If severe weather involves
> any precipitation, it is likely to increase the water content of the air. However,
> I don't know that it is required for all severe weather. A blizzard would involve the
> air cooling, thus reducing its water retention._
""")
    elif column == 'ELEVATION':
        st.write("""
> _The amount of 100% correlations with elevation and severe weather make me
> suspicious this is more of a symptom of individual stations exclusively reporting
> something that falls within the severe category, not that there's actually a
> strong relationship. This is further validated by the spread of the 100% values
> across the spectrum of elevation._
""")
    elif column == 'ALTIMETER':
        st.write("""
> _I don't see a strong variety or correlation based on this value. After seeing that,
> I'm concerned enough about it not being present that I'll just remove it from the
> training datasets._
""")
