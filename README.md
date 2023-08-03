# Compare the world's largest banks

This streamlit app helps you compare important metrics, like Total Desposits, amongst the world's largest banks.

The app pulls data from Snowflake and uses the Mito spreadsheet for Streamlit to display it to the user. The user can further analyze the data using the spreadsheet and pre-made graphs.

![Alt text](app_screenshot.png?raw=true "Streamlit App")

### Mito Streamlit Package 
To learn more about creating Streamlit applications using the Mito spreadsheet, checkout the docs [here](https://docs.trymito.io/mito-for-streamlit/getting-started)

### The Data
This app is connected to a Snowflake database that contains financial and economic data aggregated by [Cybersyn](https://docs.cybersyn.com/our-data-products/economic-and-financial/financial-and-economic-essentials?utm_source=snowflake.com&utm_medium=website&utm_campaign=website_docs) from the following sources: FDIC, FFIEC, FRED, BLS, CFPB, Bank of England, Bank of International Settlements, Bank of Canada, Banco de Mexico, and Banco Central do Brasil.

### Run Locally 
1. Set up your data by creating a Snowflake account and then creating a database with [this](https://app.snowflake.com/marketplace/listing/GZTSZAS2KF7/cybersyn-inc-cybersyn-financial-economic-essentials) data. Its free!

2. Create a virtual environment:
```
python3 -m venv venv
```

3. Start the virtual environment:
```
source venv/bin/activate
```

4. Install the required python packages:
```
pip install -r requirements.txt
```

5. Create a file `config.toml` in the root of this folder with the following format:
```
[snowflake]
account = "xxx"
user = "xxx"
password = "xxx"
```

6. Start the streamlit app
```
streamlit run main.py
```