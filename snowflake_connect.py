
from snowflake.snowpark import Session
import snowflake.connector
import os

def get_session():
    if 'SNOWFLAKE_ACCOUNT' in os.environ:
        session_configs = {
            'account': os.environ['SNOWFLAKE_ACCOUNT'],
            'user': os.environ['SNOWFLAKE_USER'],
            'password': os.environ['SNOWFLAKE_PASSWORD'],
            'warehouse ': os.environ['SNOWFLAKE_WAREHOUSE'],
            'database': os.environ['SNOWFLAKE_DATABASE'],
            'schema': os.environ['SNOWFLAKE_SCHEMA']
        }
        session = Session.builder.configs(session_configs).create()
    else:
        session = Session.builder.create()
    return session

def get_connection():
    if 'SNOWFLAKE_ACCOUNT' in os.environ:
        connection = snowflake.connector.connect({        
            'account': os.environ['SNOWFLAKE_ACCOUNT'],
            'user': os.environ['SNOWFLAKE_USER'],
            'password': os.environ['SNOWFLAKE_PASSWORD'],
            'warehouse ': os.environ['SNOWFLAKE_WAREHOUSE'],
            'database': os.environ['SNOWFLAKE_DATABASE'],
            'schema': os.environ['SNOWFLAKE_SCHEMA']
        })
    else:
        connection = snowflake.connector.connect()
    return connection
