
import streamlit as st


from PIL import Image
from src.util.section_tools import create_section_button, init_sections
from src.util.file_tools import get_example_script_contents, get_asset_path
from src.util.observation_data import get_weather_training_data
from src.util.model_training import *
import altair as alt

sections = {
    '2_demo': 'Application',
    '2_sample_json': 'Sample Timeseries',
    '2_transform_py': 'Parsing Script',
    '2_upload': 'Snowflake Upload Script',
    '2_clean_query': 'Cleaning Observations Query',
    '2_model_training': 'Training Simulation',
    '2_model_fitting': 'Fitting Details',

}

init_sections(sections)


"""

# Application

The following is the application portion of the capstone. It demonstrates the training
and predictive capability of the Random Forest algorithm as it relates to the classification
of weather conditions based on a weather station's data.


## Model Creation


The process for creating this model included the following steps:

1. Data Preparation
    - Retrieval
    - Analysis
    - Transformation
2. Model Training
    - Training Data Selected
    - Model Fitting
    - Quality Review


## Data Preparation

The [descriptive section](/Descriptive) discusses the (c) analysis of the data. If you wish to understand
how the data was (b) retrieved and (d) transformed for the training and analysis, _that_ is the focus of
this section.

### Retrieval

Data was retrieved from Synoptic's Weather API with a python script. After creating an
account and generating an API token, retrieving data from the weather API was as simple
as making a get request to their [timeseries endpoint](https://docs.synopticdata.com/services/time-series).
From this endpoint, station and observation data could be retrieved, and it could be requested
in large batches.

"""

create_section_button('2_sample_json', sections)
if st.session_state['2_sample_json']:
    "The following file demonstrates the original structure in which the data was retrieved:"
    st.write(get_example_script_contents('sample_timeseries.json'))
    
"""

### Transformation

Once retrieved, the json body was parsed and traversed by a python function which would take
the data object and return a pandas DataFrame of the select fields in a melted/unpivot pattern.

For every pandas dataframe produced, a csv file was created with that panda's contents by
using the built-in pandas function `to_csv()`.

"""

create_section_button('2_transform_py', sections)
if st.session_state['2_transform_py']:
    "The function demonstrates how the object was parsed into a pandas DataFrame:"
    st.write(get_example_script_contents('python_snippets/transform_to_csv.py'))

"""

#### Snowflake

The end goal of the retrieval was to get the data to Snowflake so the cleaning and preparation
of data could be done with SQL and iterative transformation. Snowflake is a great tool
for storing and transforming large amounts of structured data, and after pulling 10 days of
observation data, I had over 2 Gigabytes of CSV files (when compressed in zip file).

This totaled over two thousand CSV files, and I _was not_ going to upload that manually into
Snowflake. To get the data loaded, I leveraged the `snowflake.snowpark` python package.
When creating a `snowpark.DataFrame`, the module creates a temporary table in Snowflake
that houses the data passed to it. Once there, it was a simple task to "write" the table
in append mode to its destination.
"""

st.image(Image.open(get_asset_path('retrieval.jpeg')))

create_section_button('2_upload', sections)
if st.session_state['2_upload']:
    """
    Using this script, I uploaded all of the data, three files at a time, into the
    `ML_CAPSTONE.WEATHER.OBSERVATIONS` table in Snowflake (the database and schema were set in
    the default configuration for the snowflake connection).
    """
    st.write(get_example_script_contents('python_snippets/load_observation_data.py'))


"""
Once in Snowflake, the work to analyze and transform the data for the task of training
the model began.

There were four transformations that needed to occur:
1. Parse and label Weather Condition Codes as "High Risk" or not.
2. Clean up variable names.
3. Pivot and join observations to their stations.
4. Remove stations lacking the material data required for the model.

Step 1 is covered in the [descriptive section](/Descriptive#observed-conditions).

For step 2, the variable names were split into groups with different `_set` suffixes. Those needed
to be removed for the training data to be consistent. To accomplish this, the following view was
created on top of the observations table:

"""

st.write(get_example_script_contents('sql_scripts/clean_observations.sql'))

"""

For steps 3 and 4, the observations were joined to the station, providing latitude, longitude, and elevation,
then filtered down to the records that had everything required for the model.

"""

st.dataframe(get_weather_training_data().iloc[:10], use_container_width=True)

create_section_button('2_clean_query', sections)
if st.session_state['2_clean_query']:
    "The following file shows the query that was used to clean the used observations:"
    st.write(get_example_script_contents('sql_scripts/cleaned_station_observations.sql'))

"""

## Model Training

Now that the data is ready, it's time to train the model. The best way to do this is to split the data into different
groups. To measure overfitting or bias, it's best to test a model against different records than those which trained
it.

### Training Data Selected

Leveraging the scikit-learn library, there are many available utilities to make this easy to implement.

"""
st.write(get_example_script_contents('python_snippets/training_dataset.py'))

"""

### Model Fitting

Prepared data and scripts are a way to 

"""

if  st.session_state:
    pass

def train_model():
    pass

if ('model_configs' not in st.session_state) or ('model_stats' not in st.session_state):
    st.session_state['model_stats'] = []
    st.session_state['model_configs'] = []

# st.file_uploader('Train Models from JSON', on_change=)

create_section_button('2_model_training', sections)
if st.session_state['2_model_training']:
    model_config = get_model_training_controls()
    st.button('Train This Model', on_click=train_model)
    model_stats = None
    for stats in st.session_state['model_stats']:
        if model_stats is None:
            model_stats = stats.copy()
        else:
            model_stats.loc[model_stats.shape[0]] = stats.iloc[0]
    if model_stats is not None:
        model_metrics = model_stats.reset_index().melt(['index'], ['accuracy', 'recall', 'precision'], 'Metric', 'Quality')
        st.dataframe(model_metrics)
        st.altair_chart(
            alt.Chart(model_metrics)
                .mark_bar()
                .encode(
                    x=alt.X('index:N').axis(title='Model Number', labelAngle=0)
                    , xOffset='Metric:N'
                    , y=alt.Y('Quality:Q')
                    , color='Metric:N'
                )
            , use_container_width=True
        )

    # with tr_col_1:
    # with tr_col_2:
    st.dataframe(model_config)
    st.write(st.session_state['model_configs'])
