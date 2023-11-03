import streamlit as st

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

Feel free to navigate through this site to observe the capstone. The navigation is intentionally sorted in a
top-to-bottom order for ease of consumption, but there is no requirement for going in order.

"""



"""
---
"""

from PIL import Image
from src.util.section_tools import create_section_button, init_sections
from src.util.file_tools import get_example_script_contents, get_asset_path

sections = {
    '3_demo': 'Application',
    '3_sample_json': 'Sample Timeseries',
    '3_transform_py': 'Parsing Script',
    '3_upload': 'Snowflake Upload Script',
    '3_model_training': 'Training Data',
    '3_model_fitting': 'Fitting Details',

}

init_sections(sections)


"""

# Application

The following is the application portion of the capstone. It demonstrates the training
and predictive capability of the Random Forest algorithm as it relates to the classification
of weather conditions based on a weather station's data.


## Demonstration

"""




"""
## Model Creation


The process for creating this model included the following steps:

1. Data Preparation
    a. Discovery
    b. Retrieval
    c. Analysis
    d. Transformation
2. Model Training
    a. Training Data Selected
    b. Model Fitting
    c. Quality Review


## Data Preparation

The (a) discovery of the data used in this project is found in the [Introduction section](/Introduction).
The [Descriptive section](/Descriptive) discusses the (c) analysis of the data. If you wish to understand
how the data was (b) retrieved and (d) transformed for the training and analysis, _that_ is the focus of
this section.

### Retrieval

Data was retrieved from Synoptic's Weather API with a python script. After creating an
account and generating an API token, retrieving data from the weather API was as simple
as making a get request to their [timeseries endpoint](https://docs.synopticdata.com/services/time-series).
From this endpoint, station and observation data could be retrieved, and it could be requested
in large batches.

"""

create_section_button('3_sample_json', sections)
if st.session_state['3_sample_json']:
    "The following file demonstrates the original structure in which the data was retrieved:"
    st.write(get_example_script_contents('sample_timeseries.json'))
    
"""

### Transformation

Once retrieved, the json body was parsed and traversed by a python function which would take
the data object and return a pandas DataFrame of the select fields in a melted/unpivot pattern.

For every pandas dataframe produced, a csv file was created with that panda's contents by
using the built-in pandas function `to_csv()`.

"""

create_section_button('3_transform_py', sections)
if st.session_state['3_transform_py']:
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

create_section_button('3_upload', sections)
if st.session_state['3_upload']:
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

"""
