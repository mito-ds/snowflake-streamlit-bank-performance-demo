"""
This is a demo of the mitosheet library. It's a simple streamlit app that connects to a snowflake database and displays the results of a SQL query in a spreadsheet.
"""

import streamlit as st
import pandas as pd
from mitosheet.streamlit.v1 import spreadsheet
from mitosheet.public.v3 import *
from graph import get_plotly_fig
from queries import *
from credentials import ACCOUNT, PASSWORD, USER

st.set_page_config(layout="wide")
st.title("Compare the world's largest banks")

##                              ##
##  Step 1:                     ##
##  Collect the data            ##
##                              ##

# Initialize the connection to Swnowflake 
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

# Get the names of the largest banks so we can display them to the app user. 
# Cache this result so we don't have to re-run the query every time the user changes the selection.
@st.cache_data
def get_largest_banks():
    return conn.query(big_banks_query, ttl=600)

large_banks_df = get_largest_banks()

# Display a multiselect widget to the user so they can select which banks they want to compare.
selected_banks = st.multiselect(
    label='#### Select banks', 
    options=list(large_banks_df['NAME']), 
    default=list(large_banks_df["NAME"].head(10))
)

# Execute the SQL query to pull data about the selected banks
bank_info_query = get_bank_income_query(selected_banks)
df = conn.query(bank_info_query, ttl=600)

##                                      ##
##  Step 2:                             ##
##  Clean the data before displaying it ##
##                                      ## 

# Convert the Date column 
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

# Rename columns to make them more readable
df1_pivot.rename(columns={
    'VALUE sum Total deposits': 'Total deposits',
    'VALUE sum Estimated Insured Deposits': 'Estimated Insured Deposits',
    'VALUE sum Net Operating Income': 'Net Operating Income',
    'VALUE sum Total Interest Income': 'Total Interest Income',
}, inplace=True)

# Reorder columns
df1_columns = [col for col in df1_pivot.columns if col != 'Total deposits']
df1_columns.insert(2, 'Total deposits')
df1_pivot = df1_pivot[df1_columns]

##                                  ##
##   Step 3:                        ##
##   Display data in a spreadsheet  ##
##                                  ##

dfs, code = spreadsheet(df1_pivot)


##                                  ##
##   Step 4:                        ##
##   Create basic graphs of data    ##
##                                  ##           

# This dataframe has all of the user edits applied to it. 
# Use this dataframe so that the user edits are reflected in the graphs.
updated_df = dfs["df1"]

# Before creating each graph, makes sure that the column exists in the dataframe, 
# as the user may have deleted it through the spreadsheet.
column_headers = list(updated_df.columns)
if 'Total deposits' in column_headers:
    total_deposits_fig = get_plotly_fig(updated_df, 'Total deposits')
    st.plotly_chart(total_deposits_fig, use_container_width=True)

if 'Estimated Insured Deposits' in column_headers:
    estimated_insured_deposits_fig = get_plotly_fig(updated_df, 'Estimated Insured Deposits')
    st.plotly_chart(estimated_insured_deposits_fig, use_container_width=True)

if 'Net Operating Income' in column_headers:
    net_operating_income_fig = get_plotly_fig(updated_df, 'Net Operating Income')
    st.plotly_chart(net_operating_income_fig, use_container_width=True)

if 'Total Interest Income' in column_headers:
    total_interest_income_fig = get_plotly_fig(updated_df, 'Total Interest Income')
    st.plotly_chart(total_interest_income_fig, use_container_width=True)

st.markdown("""This app is connected to a Snowflake database that contains financial and economic data aggregated by [Cybersyn](https://docs.cybersyn.com/our-data-products/economic-and-financial/financial-and-economic-essentials?utm_source=snowflake.com&utm_medium=website&utm_campaign=website_docs) from the following sources: FDIC, FFIEC, FRED, BLS, CFPB, Bank of England, Bank of International Settlements, Bank of Canada, Banco de Mexico, and Banco Central do Brasil.""")