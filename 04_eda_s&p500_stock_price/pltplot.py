import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
today_date = datetime.now().strftime('%Y-%m-%d')
ten_years_ago_date = (datetime.now() - relativedelta(years=10)).strftime('%Y-%m-%d')

def main():
    st.set_page_config(layout="wide")

    st.title('S&P 500 App')

    st.markdown("""
    This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
    * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
    * **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
    """)

    st.sidebar.header('User Input Features')

    df = load_data()
    sector = df.groupby('GICS Sector')

    # Sidebar - Sector selection
    sorted_sector_unique = sorted( df['GICS Sector'].unique() )
    with st.sidebar.form(key='data_form'):
        st.write('Select sector/sectors of interest.')
        selected_sector = st.multiselect('Sector/Sectors', sorted_sector_unique, sorted_sector_unique)
        submit = st.form_submit_button(label='Submit')

    # Filtering data
    df_selected_sector = df[ (df['GICS Sector'].isin(selected_sector)) ]

    if len(df_selected_sector) > 0:

        st.header('Display Companies in Selected Sector')
        st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
        st.dataframe(df_selected_sector)

        st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

        # Plot closing price
        with st.sidebar.form(key='plot_form'):
            st.write('Select company/companies to plot the closing price.')
            selected_company = st.multiselect('Company/Companies', list(df_selected_sector.Symbol), None)
            plot = st.form_submit_button(label='Plot')

        if plot and len(selected_company) > 0:
            
            data = yf.download(
                tickers = selected_company,
                period = "ytd",
                interval = "1d",
                group_by = 'ticker',
                auto_adjust = True,
                prepost = True,
                threads = True,
                proxy = None
            )

            st.header('Stock Closing Price')
            for symbol in selected_company:
                plot=price_plot(data, symbol)
    else:
        st.warning('Please select at least **one** sector to proceed.')
        if st.button('Secret cheer up button'):
            st.balloons()
            st.info('Please select at least **one** sector to proceed.')
    
# Web scraping of S&P 500 data
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

# Plot Closing Price of Query Symbol
def price_plot(data, symbol):
    try:
        # multiindex data
        df = pd.DataFrame(data[symbol].Close)
    except:
        # in case only one symbol in the data
        df = pd.DataFrame(data.Close)

    df['Date'] = df.index

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
    
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')

    st.set_option('deprecation.showPyplotGlobalUse', False)
    
    return st.pyplot()

if __name__ == "__main__":
    main()