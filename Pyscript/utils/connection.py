from snowflake.snowpark import Session
import sys
import logging
from dotenv import load_dotenv
import configparser
import os

load_dotenv()  # Load environment variables from .env file
config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), '..', 'config.ini'))

# initiate logging at info level
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%I:%M:%S')

# snowpark session
def get_snowpark_session() -> Session:
    connection_parameters = {
        "ACCOUNT": config['SNOWFLAKE']['ACCOUNT'],
        "USER": os.getenv("SNOWFLAKE_USER"),
        "PASSWORD": os.getenv("SNOWFLAKE_PASSWORD"),
        "ROLE": config['SNOWFLAKE']['ROLE'],
        "DATABASE": config['SNOWFLAKE']['DATABASE'],
        "SCHEMA": config['SNOWFLAKE']['SCHEMA'],
        "WAREHOUSE": config['SNOWFLAKE']['WAREHOUSE']
    }
    # creating snowflake session object
    return Session.builder.configs(connection_parameters).create()   

def main():
    session = get_snowpark_session()

    context_df = session.sql("select current_role(), current_database(), current_schema(), current_warehouse()")
    context_df.show(2)

    customer_df = session.sql("select c_custkey,c_name,c_phone,c_mktsegment from snowflake_sample_data.tpch_sf1.customer limit 10")
    customer_df.show(5)

if __name__ == '__main__':
    main()