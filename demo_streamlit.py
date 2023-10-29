import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
from snowflake_connect import get_session as get_sf_session

def get_session():
    return get_sf_session()

@st.cache_resource
def get_states():
    return get_session().table('states').to_pandas()

@st.cache_resource
def get_stations():
    return get_session().table('weather_stations').to_pandas()

states = get_states()
stations = get_stations()

st.title('Demo Streamlit')
a = st.text_input('Label', 0, 10, 1)
b = st.number_input('Value', 0, 10, 2)

def add_value():
    st.session_state['custom_labels'] = np.array(st.session_state['custom_labels'].tolist() + [a])
    st.session_state['custom_values'] = np.array(st.session_state['custom_values'].tolist() + [b])

st.button('Add Values', on_click=add_value)

selected_state = st.selectbox('State', states['STATE_NAME'].sort_values())
# selected_state = st.select_slider('States', state_table['STATE_NAME'].sort_values())

selected_state = states.where(lambda r : r['STATE_NAME'] == selected_state).dropna().iloc[0]['STATE_ID']
# st.select_slider()

if 'custom_values' not in st.session_state:
    st.session_state['custom_labels'] = np.array(['value1','value2'])
    st.session_state['custom_values'] = np.array([1,2], dtype=np.intp)


example_data = pd.DataFrame({
    'Labels': st.session_state['custom_labels'],
    'Values': st.session_state['custom_values']
})

zoom = 3 if selected_state == None else 6


def clicked_object(widget, payload):
    print('widget', widget)
    print('payload', payload)

state = states.where(lambda i : i['STATE_ID'] == selected_state).dropna().iloc[0]

st.write(stations.columns.to_list())

mapDeck = pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        zoom=zoom,
        latitude=state['LATITUDE'],
        longitude=state['LONGITUDE']
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            stations.where(lambda i : i['STATE'] == selected_state).dropna()[['LONGITUDE', 'LATITUDE']],
            get_position='[LONGITUDE, LATITUDE]',
            get_color='[200, 30, 0, 160]',
            get_radius=1000
        )]
)

st.pydeck_chart(mapDeck)
st.line_chart(example_data, x='Labels')
# st.bar_chart(example_data, x='val')
# st.area_chart(example_data, x='val')

st.altair_chart(alt.Chart(example_data)    
        .mark_bar()
        .encode(
            alt.X('Labels').axis(labelAngle=0),
            alt.Y('Values').title(None))
    , use_container_width=True
)
st.subheader('Raw data')
st.write(stations)
