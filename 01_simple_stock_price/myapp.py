import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

today_date = datetime.now().strftime('%Y-%m-%d')
ten_years_ago_date = (datetime.now() - relativedelta(years=10)).strftime('%Y-%m-%d')

st.write(f"""
# Simple Stock Price App

Shows the stock of Google for the past 10 years!

Today's Date:   `{today_date}`

Ten Year's Ago: `{ten_years_ago_date}`

""")

# https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

# define the ticker symbol
tickerSymbol = 'GOOGL'

# tickerSymbol = 'AAPL' # for apple

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
