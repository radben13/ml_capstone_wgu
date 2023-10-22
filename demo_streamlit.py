import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


st.title('Demo Streamlit')
a = st.text_input('Label', 0, 10, 1)
b = st.number_input('Value', 0, 10, 2)

def add_value():
    st.session_state['custom_labels'] = np.array(st.session_state['custom_labels'].tolist() + [a])
    st.session_state['custom_values'] = np.array(st.session_state['custom_values'].tolist() + [b])

st.button('Add Values', on_click=add_value)

if 'custom_values' not in st.session_state:
    st.session_state['custom_labels'] = np.array(['value1','value2'])
    st.session_state['custom_values'] = np.array([1,2], dtype=np.intp)


example_data = pd.DataFrame({
    'Labels': st.session_state['custom_labels'],
    'Values': st.session_state['custom_values']
})



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

st.write('<h1>hello streamlit app!</h1>', unsafe_allow_html=True)

st.subheader('Raw data')
st.write(example_data)
