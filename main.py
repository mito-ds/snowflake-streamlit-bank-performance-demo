"""
This is a demo of the mitosheet library. It's a simple streamlit app that connects to a snowflake database and displays the results of a SQL query in a spreadsheet.
"""

import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.public.v3 import *
from queries import *
from credentials import ACCOUNT, PASSWORD, USER

st.set_page_config(layout="wide")
st.title("Explore Financial Data in Snowflake")

st.markdown("""
This app is connected to a Swnowflake database that contains financial and economic data including: central bank rates, FDIC insurnace data, bank financials, etc. 

The data is aggregated by [Cybersyn](https://docs.cybersyn.com/our-data-products/economic-and-financial/financial-and-economic-essentials?utm_source=snowflake.com&utm_medium=website&utm_campaign=website_docs) from the following sources: FDIC, FFIEC, FRED, BLS, CFPB, Bank of England, Bank of International Settlements, Bank of Canada, Banco de Mexico, and Banco Central do Brasil.

The app is already connected to the database and comes preloaded some SQL queries to pull interesting datasets, so all you need to do is select a dataset and start exploring. No coding required!
""")

# Initialize connection.
conn = st.experimental_connection(
    'snowpark', 
    account=ACCOUNT,
    user=USER,
    password=PASSWORD,
    warehouse="COMPUTE_WH",
    database="CYBERSYN_FINANCIAL__ECONOMIC_ESSENTIALS",
    schema="cybersyn",
    client_session_keep_alive = True
)

@st.cache_data
def get_largest_banks():
    return conn.query(big_banks_query, ttl=600)

large_banks_df = get_largest_banks()

selected_banks = st.multiselect(
    label='#### Select banks', 
    options=list(large_banks_df['NAME']), 
    default=list(large_banks_df["NAME"].head(10))
)

bank_info_query = get_bank_income_query(selected_banks)

st.code(bank_info_query)

# Perform query.
df = conn.query(bank_info_query, ttl=600)

df["DATE"] = pd.to_datetime(df["DATE"])

# Some companies report multiple numbers for the same date. We default to using the larger of the two.
df['VALUE'] = to_float_series(df['VALUE'])
df = df.sort_values(by='VALUE', ascending=True, na_position='first')
df = df.drop_duplicates(subset=['DATE', 'UNIT', 'VARIABLE_NAME', 'NAME'], keep='last')

# Convert the data from long format to wide format.
tmp_df = df[['VARIABLE_NAME', 'VALUE', 'NAME', 'DATE']].copy()
pivot_table = tmp_df.pivot_table(
    index=['DATE', 'NAME'],
    columns=['VARIABLE_NAME'],
    values=['VALUE'],
    aggfunc={'VALUE': ['sum']}
)
pivot_table = pivot_table.set_axis([flatten_column_header(col) for col in pivot_table.keys()], axis=1)
df1_pivot = pivot_table.reset_index()

# Some companies report multiple numbers for the same date. We default to using the larger of the two.
df = df.sort_values(by=['DATE', 'VARIABLE_NAME', 'NAME'], ascending=[True, True, True])

dfs, code = spreadsheet(df)
st.code(code)

