import streamlit as st
import os
import re

def get_root_path():
    return os.path.abspath(os.path.join(__file__, '../../..'))

def get_asset_path(path: str):
    return os.path.join(get_root_path(), 'assets', path)

def get_resource_path(path: str):
    return os.path.join(get_root_path(), 'resources', path)

lang = {
    '.sql': 'sql',
    '.py': 'python',
    '.json': 'json',
    '.csv': 'csv',
}

@st.cache_resource
def get_example_script_contents(filename: str):
    m = re.search('\.[^\.]+$', filename)
    with open(get_resource_path(filename)) as script:
        return f"```{lang[m.group(0)]}\n{script.read()}\n```"
