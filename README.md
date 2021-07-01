# Some Data Science Apps

Learning how to build data science apps from freeCodeCamp.org

Tutorial: [Build 12 Data Science Apps with Python and Streamlit - Full Course](https://www.youtube.com/watch?v=JwSS70SZdyM&list=PLRpb1EfB9cjuOFw_ZVmeqlCgdhYjdbBMO&index=10&ab_channel=freeCodeCamp.org)

This tutorial covers how to build interactive and data-driven web apps in Python using the Streamlit library. This repo contains 9 web apps built from the tutorial with slight modifications.

To install the Streamlit library

```
pip install streamlit
```

To run a web app

```
streamlit run myapp.py
```

## :one: Simple Stock Price App

A simple web app that shows a company's stock. Retrieve stock stock data directly from Yahoo Finance.

Towards Data Science article on [How to Get Stock Data Using Python](https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75) (using `yfinance`)

```
pip install yfinance
```

* Using `streamlit` to build basic web app
* Using `yfinance` to get stock price data

## :two: Simple Bioinformatics DNA Count

A DNA nucleotide count web app which counts the nucleotide composition (A, T, G, C) of a query DNA

* Taking input and showing output in different formats (dictionary, text, dataframe, plot)

## :three: EDA Basketball and Football

Web scraping from [Basketball Reference](https://www.basketball-reference.com) and [Football Reference](https://www.pro-football-reference.com/). Performs a simple exploratory data analysis by creating a heatmap.

* Select widget and multiselect widget in `streamlit`
* Web scrapping with `pandas`
* Filtering data with conditions in `pandas` (data wrangling)
* Downloading csv files in Streamlit

## :four: EDA S&P 500 Stock Price 

The [S&P 500](https://en.wikipedia.org/wiki/S%26P_500) (the Standard and Poor's 500) is a market-​capitalization-weighted measurement stock market index of the 500 largest companies listed on stock exchanges in the United States. It is one of the most commonly followed equity indices by investors.

This web app scraps all company data from the latest [list of S&P 500 companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) on Wikipedia, fetch their respective stock price data and plot the stock closing price. 

* Web scrapping with `pandas`
* Fetching stock price with `yfinance`
* Filtering data with conditions in `pandas` (data wrangling)
* Slider in `streamlit`