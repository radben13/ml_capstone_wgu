import streamlit as st
import pandas as pd
from sklearn.metrics import accuracy_score, recall_score, precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from src.util.observation_data import get_weather_training_data

def get_model_stats(model: RandomForestClassifier):
    _, val_X, _, val_y = get_training_data()
    pred_y = model.predict(val_X)
    columns, values = list(model.feature_names_in_), list(model.feature_importances_)
    columns = ['accuracy', 'recall', 'precision'] + columns
    values = [
        accuracy_score(val_y, pred_y),
        recall_score(val_y, pred_y),
        precision_score(val_y, pred_y)
    ] + values
    return pd.DataFrame(data=[values], columns=columns)

@st.cache_resource
def get_training_data():
    training_data = get_weather_training_data()
    # Due to the overwhelming amount of data that has no
    # severe weather, I'm adjusting this to use less of the non-severe
    training_data.drop(columns=['ALTIMETER'], inplace=True)
    t_severe = training_data[training_data['IS_SEVERE']]
    f_severe = training_data[~training_data['IS_SEVERE']]
    f_severe.reset_index(drop=True, inplace=True)
    remainder = f_severe[t_severe.shape[0] * 10:]
    f_severe = f_severe[:t_severe.shape[0] * 10]
    training_data = pd.concat([t_severe, f_severe], ignore_index=True)
    training_data = training_data.dropna()
    y = training_data['IS_SEVERE']
    X = training_data.drop(columns=['IS_SEVERE'])
    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)
    val_X = pd.concat([val_X, remainder.drop(columns='IS_SEVERE', inplace=False)], ignore_index=True)
    val_y = pd.concat([val_y, remainder['IS_SEVERE']], ignore_index=True)
    return train_X, val_X, train_y, val_y

@st.cache_resource
def get_random_forest_classifier(*_, **kwargs):
    if 'loaded_model' in st.session_state:
        del st.session_state['loaded_model']
    train_X, _, train_y, _ = get_training_data()
    model = RandomForestClassifier(random_state=1, **kwargs)
    model.fit(train_X, train_y)
    st.session_state['loaded_model'] = True
    return model

def get_model_training_controls():
    enabled = st.multiselect('Select Options', [
        'max_leaf_nodes', 'min_samples_leaf', 'max_depth',
        'min_samples_split', 'criterion', 'n_estimators',
    ])
    config_values = dict()
    config_values['n_estimators'] = (
        st.slider,
        {
            'label': 'Estimators'
            , 'min_value': 0
            , 'max_value': 100
            , 'value': 100
        }
    )
    config_values['max_leaf_nodes'] = (
        st.slider,
        {
            'label': 'Max Leaf Nodes'
            , 'min_value': 0
            , 'max_value': 100
        }
    )
    config_values['min_samples_leaf'] = (
        st.slider,
        {
            'label':'Min Samples Leaf'
            , 'min_value':1
            , 'max_value':100
        }
    )
    config_values['min_samples_split'] = (
        st.slider,
        {
            'label': 'Min Samples Split'
            , 'min_value': 0
            , 'max_value': 100
        }
    )
    config_values['max_depth'] = (
        st.slider,
        {
            'label': 'Max Depth'
            , 'min_value': 0
            , 'max_value': 100
            , 'value': 100
        }
    )
    config_values['criterion'] = (
        st.select_slider,
        {
            'label':'Criterion'
            , 'options': ['gini', 'entropy']
        }
    )
    return dict([(e, config_values[e][0](**config_values[e][1])) for e in enabled])
