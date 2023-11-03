import streamlit as st

from src.util.section_tools import create_section_button, init_sections
from src.util.file_tools import get_asset_path
from src.util.model_training import *
import altair as alt



with open(get_asset_path('invertocat.svg.data')) as f:
    invertocat_svg = f.read()

sections = {
    'home_demo': 'Demonstration',
}
init_sections(sections)

"""
# Weather Severity Predictor
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


## Demonstration

Hello, Fellow Meteorologists!

Welcome to your latest "Weather Severity Predictor" solution. It's in its infancy, but this
tool will be the trick for automating a lot of weather risk calculations in your day-to-day
efforts.

"""
if not st.session_state['home_demo']:
    create_section_button('home_demo', sections)

if st.session_state['home_demo']:
    """
    This is the Weather Severity Predictor. In order to help you in your business of crunching
    the numbers, the first thing you'll need is a collection of values.

    For your benefit, I've already provided a starter value. Edit the values in the table below to see the
    prediction and confidence of the Random Forest Classifier in action. You can edit the values by double
    clicking a cell. You can also inspect the confidence and prediction details of the model
    by hovering over the pie chart.
    """
    demo_column_config = {
        '_index': st.column_config.TextColumn(disabled=True, label='Keys'),
        'Values': st.column_config.NumberColumn()
    }
    d_col_1, d_col_2 = st.columns([0.4,0.6])
    _, val_X, _, val_y = get_training_data()
    model = get_random_forest_classifier()
    with d_col_1:
        values = st.data_editor(val_X.head(1).transpose().rename(columns=lambda i: 'Values'), column_config=demo_column_config).transpose()
    with d_col_2:
        prod_cols = {'0':'Low Risk','1':'High Risk'}
        pred_ya = model.predict_proba(values)
        pred_ya = pd.DataFrame(pred_ya)
        pred_ya = pred_ya.transpose().rename(lambda i : prod_cols[str(i)])
        pred_ya = pred_ya.reset_index().rename(columns={'index': 'Prediction', 0:'Confidence'})

        prediction = alt.Chart(pred_ya).mark_arc().encode(
            alt.Theta('Confidence:Q'),
            alt.Color('Prediction:N'),
        )
        pred_y = model.predict(values)
        # prediction += alt.Chart(pred_y).mark_bar()
        st.altair_chart(prediction, use_container_width=True)
    
    feature_report = get_model_stats(model).drop(columns=['accuracy','recall', 'precision'])\
        .transpose().reset_index().rename(columns={'index': 'Feature', 0: 'Importance'})

    """
    ### Feature Importance
    If you would like some clues as to the fields you might want to change first, the following
    is the chart of the "feature importance" within the predictive model. The larger the bar,
    the more critical the model believes that value is in its predictions or classifications.

    """

    st.altair_chart(
        alt.Chart(feature_report)\
            .mark_bar()\
            .encode(
                alt.X('Feature:N'),
                alt.Y('Importance:Q'),
                alt.Color('Feature:N')
            )
        , use_container_width=True
    )
