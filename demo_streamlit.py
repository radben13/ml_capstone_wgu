import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


st.title('Demo Streamlit')
a = st.number_input('A', 0, 10, 1)
b = st.number_input('B', 0, 10, 2)

example_data = pd.DataFrame({'test': [a,b], 'val': ['a', 'b']})
st.line_chart(example_data, x='val')
# st.bar_chart(example_data, x='val')
# st.area_chart(example_data, x='val')

st.altair_chart(alt.Chart(example_data)    
        .mark_line()
        .encode(
            alt.X('val').title('value').axis(labelAngle=0),
            alt.Y('test').title(None))
    , use_container_width=True
)

st.write('<h1>hello streamlit app!</h1>', unsafe_allow_html=True)

st.subheader('Raw data')
st.write(example_data)
