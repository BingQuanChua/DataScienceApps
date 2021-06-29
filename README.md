# Some Data Science Apps

Learning how to build data science apps from freeCodeCamp.org

[Build 12 Data Science Apps with Python and Streamlit - Full Course](https://www.youtube.com/watch?v=JwSS70SZdyM&list=PLRpb1EfB9cjuOFw_ZVmeqlCgdhYjdbBMO&index=10&ab_channel=freeCodeCamp.org)

This tutorial covers how to build interactive and data-driven web apps in Python using the Streamlit library

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

Towards Data Science article on [How to Get Stock Data Using Python](https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75) 

```
pip install yfinance
```

Lesson learned: Using Streamlit to build basic web app

## :two: Simple Bioinformatics DNA Count

A DNA nucleotide count web app which counts the nucleotide composition (A, T, G, C) of a query DNA

Lesson learned: Taking input and showing output in different formats (dictionary, text, dataframe, plot)

## :three: EDA Basketball Data

Web scraping from the [Basketball Reference](https://www.basketball-reference.com) website. Data filter. Simple exploratory data analysis by creating simple heat map

Lesson learned: Using Streamlit's select widget and multiselect widget, web scrapping with pandas, and filtering data with conditions in pandas (data wrangling).