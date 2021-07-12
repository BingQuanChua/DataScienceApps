import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def main():
    today_date = datetime.now().strftime('%Y-%m-%d')
    ten_years_ago_date = (datetime.now() - relativedelta(years=10)).strftime('%Y-%m-%d')

    st.write(f"""
    # Simple Stock Price App

    Shows the stock **closing price** and **volume** of the selected company for the past 10 years!  
    Today's Date:   `{today_date}`  
    Ten Years Ago: `{ten_years_ago_date}`  
    """)

    ticker_symbols = {
        'Google': 'GOOGL',
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Tesla': 'TSLA',
        'Facebook': 'FB',
        'Amazon': 'AMZN',
        'Netflix': 'NFLX'
    }

    list_of_options = ['--select a company--']
    for key in ticker_symbols:
        list_of_options.append(key)

    company = st.selectbox('Select a company', list_of_options, index=0, help='choose a company')

    
    # define the ticker symbol
    tickerSymbol = ticker_symbols.get(company)

    if tickerSymbol is not None:

        # https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75
        # get data on this ticker
        tickerData = yf.Ticker(tickerSymbol)

        # get the historical prices for this ticker
        tickerDf = tickerData.history(period='1d', start=ten_years_ago_date, end=today_date)
        # Open	 High	 Low	 Close	  Volume	  Dividends	 Stock Splits

        st.write(f"""
        ## Closing price
        """)
        st.line_chart(tickerDf.Close)

        st.write(f"""
        ## Volume
        """)
        st.line_chart(tickerDf.Volume)

if __name__ == "__main__":
    main()