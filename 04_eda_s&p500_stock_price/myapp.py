import streamlit as st
import pandas as pd
import base64
import numpy as np
import yfinance as yf
import altair as alt

def main():
    st.set_page_config(layout="wide")

    st.title('S&P 500 App')

    st.markdown("""
    This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
    * **Python libraries:** streamlit, base64, pandas, numpy, yfinance, altair
    * **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
    """)

    st.sidebar.header('User Input Features')

    df = load_data()
    sector = df.groupby('GICS Sector')

    # Sidebar - Sector selection
    sorted_sector_unique = sorted( df['GICS Sector'].unique() )
    with st.sidebar.form(key='data_form'):
        st.write('Select S&P 500 sector/sectors of interest.')
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
            selected_company = st.multiselect('Company/Companies', sorted(list(df_selected_sector.Symbol)), None)
            plot = st.form_submit_button(label='Plot')

        if plot and len(selected_company) > 10:
            st.error('You have selected too many companies!')

        elif plot and len(selected_company) > 0:
            
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

            df = data.T.reset_index()
            if len(selected_company) == 1:
                
                df_filtered = df[df.get('index')=='Close'].copy()
                df_filtered.at[3, 'index']=selected_company[0]

                df_melt = pd.melt(df_filtered, id_vars=["index"]).rename(
                    columns={"index":"Company", "value": "Closing Value"}
                )

            else:
                
                df_filtered = df[df['level_1']=='Close'].copy()
                df_filtered.drop(columns='level_1', inplace=True)

                df_melt = pd.melt(df_filtered, id_vars=["level_0"]).rename(
                    columns={"level_0":"Company", "value": "Closing Value"}
                )
            
            try:
                chart = (
                    alt.Chart(df_melt)
                    .mark_area(opacity=0.4)
                    .encode(
                        x="Date:T",
                        y=alt.Y("Closing Value"),
                        color="Company:N"
                    )
                )
                st.altair_chart(chart, use_container_width=True)
            except:
                st.error('You have selected too many companies! Please select lesser.')
            
    else:
        st.error('Please select at least **one** sector to proceed.')
        if st.button('Secret cheer up button 🎈'):
            st.balloons()
    
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
    href = f'<a href="data:file/csv;base64,{b64}" download="S&P500.csv">Download CSV File</a>'
    return href

if __name__ == "__main__":
    main()