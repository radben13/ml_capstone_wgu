
import streamlit as st
from PIL import Image
from src.util.section_tools import create_section_button, init_sections
from src.util.file_tools import get_example_script_contents, get_asset_path
from src.util.observation_data import get_weather_training_data
from src.util.model_training import *
import altair as alt

import json

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

The [descriptive section](/Descriptive) discusses the analysis of the data. If you wish to understand
how the data was retrieved and transformed for the training and analysis, _that_ is the focus of
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

create_section_button('2_clean_query', sections)
if st.session_state['2_clean_query']:
    st.dataframe(get_weather_training_data().iloc[:10], use_container_width=True)
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

This section is dedicated to Model Quality. How do we make the Weather Severity
Predictor "fit" the problem it's tasked to solve?

The Weather Severity Predictor (this application) is built on the Random
Forest Algorithm. It is a **_supervised_** machine learning algorithm, which
means it is trained by "labelled" data. At the beginning, the model doesn't
know what it's measuring, how different data points are related, or what
its desired outcome should be. However, by providing a list of "labelled" data,
the algorithm is able to learn patterns that it can try to replicate.

When measuring the capability or "utility" of a model, we often refer to quality
metrics to evaluate the model. There are many, but here are three that I've used
in this project:

- `accuracy`: This represents the proportion of correctly predicted classifications over the total predictions.
- `precision`: Precision focuses on the predicted "positive" cases. It answers the question: Of all the predicted positives, how many were actually positive?
- `recall`: Recall looks at the actual "positive" cases. It answers the question: Of all the actual positives, how many did we predict as positive?

With that context, the following section focuses on training new models to outperform
the default. Take a swing at it. See if you can make a better version.
"""

model_message = ''
def train_model(*args, **kwargs):
    global model_message
    model_key = json.dumps(sorted(kwargs.items()))
    if not st.session_state.get('fitting_models'):
        st.session_state['fitting_models'] = { model_key }
    elif model_key in st.session_state['fitting_models']:
        model_message = 'A model with this configuration already exists.'
        return
    model_message = ''
    model = get_random_forest_classifier(**kwargs)
    stats = get_model_stats(model)
    if 'model_stats' not in st.session_state:
        st.session_state['model_stats'] = stats
    else:
        st.session_state['model_stats'] = pd.concat(
            [st.session_state['model_stats'], stats], ignore_index=True
        )


if not st.session_state['2_model_training']:
    create_section_button('2_model_training', sections)
else:
    if 'model_stats' not in st.session_state:
        train_model()
    model_stats = st.session_state.get('model_stats')
    if model_stats is not None:
        model_metrics = model_stats.reset_index()\
            .melt(['index'], ['accuracy', 'recall', 'precision'], 'Metric', 'Quality')
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
    """
    The chart above will update to show the quality statistics of any models you train (or "fit")
    here.
    """
    model_config = get_model_training_controls()
    def trigger_model_training():
        train_model(**model_config)
    st.button('Train This Model'
        , on_click=trigger_model_training
        , disabled=json.dumps(sorted(model_config.items())) in st.session_state['fitting_models']
    )
    """
    #### Configuration Options

    The ability to configure models can involve a lot more than this tool presents, but here's a few fields you can configure.

    1. `max_leaf_nodes`: Controls the maximum number of terminal nodes (leaves) in trees. Used to prevent overfitting, or adapting too closely to the training data, by limiting the tree's growth.
    2. `min_samples_leaf`: Minimum number of samples required to be present at a leaf node. This parameter prevents very specific splits based on few data points, again preventing overfitting.
    3. `max_depth`: Maximum depth of the tree. The deeper the tree, the more complex the decisions it can make. However, too deep can lead to overfitting.
        - _There's a trend here. Overfitting can be a problem._
    4. `min_samples_split`: Minimum number of samples required to split a node. Helps in ensuring that a significant number of data points are present before making a decision.
    5. `criterion`: The function that measures the quality of a split. "gini" is for Gini impurity and "entropy" is for information gain. Both are metrics to measure how often a randomly chosen element would be incorrectly classified.
    6. `n_estimators`: Number of trees in the forest. More trees can lead to more robust models, but also longer training times.
    """
