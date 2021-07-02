import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

def main():

    # Main page
    st.title('Sports Exploratory Data Analysis')
    st.markdown("""
    This app performs simple web scraping and EDA! Select a sport on the left to get started.
    """)

    # Sidebar - Sports selection
    st.sidebar.header('User Input Features')
    selected_sports = st.sidebar.selectbox('Sport', 
    ['--🏃‍♂️select a sport--', '🏀 Basketball', '⚽ Football'])
    
    if 'Basketball' in selected_sports:
        main_title = st.header('NBA Player Stats Explorer')
        eda_basketball()
    elif 'Football' in selected_sports:
        main_title = st.header('NFL Football Stats (Rushing) Explorer')
        eda_football()


def eda_basketball():

    markdown = st.markdown("""
    This app performs simple webscraping of NBA player stats data!
    * **Python libraries:** base64, pandas, streamlit
    * **Data source:** [Basketball Reference](https://www.basketball-reference.com/).
    """)

    # Web scraping of NBA player stats
    url = "https://www.basketball-reference.com/leagues/NBA_yyyy_per_game.html"
    
    unique_pos = ['C','PF','SF','PG','SG']
    
    load_app_structure(markdown, url, 0, unique_pos)

def eda_football():
    
    markdown = st.markdown("""
    This app performs simple webscraping of NFL Football player stats data (focusing on Rushing)!
    * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
    * **Data source:** [Football Reference](https://www.pro-football-reference.com/).
    """)

    # Website URL, sample: https://www.pro-football-reference.com/years/2019/rushing.htm
    url = "https://www.pro-football-reference.com/years/yyyy/rushing.htm"

    # Unique position selection
    unique_pos = ['RB','QB','WR','FB','TE']

    load_app_structure(markdown, url, 1, unique_pos)

def load_app_structure(markdown, url, header, unique_pos):

    markdown = markdown

    # Sidebar - Year selection
    this_year = int(datetime.now().strftime('%Y'))
    selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,this_year))))

    # Web scraping of NFL player stats
    url = url.replace("yyyy", str(selected_year))
    playerstats = load_data(url, header)

    # Sidebar - Team selection
    sorted_unique_team = sorted(playerstats.Tm.unique())
    selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

    # Sidebar - Position selection
    selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

    # Filtering data
    df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

    st.subheader('Display Player Stats of Selected Team(s)')
    st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
    st.dataframe(df_selected_team)

    # Download NBA player stats data
    st.markdown(download_file(df_selected_team), unsafe_allow_html=True)

    # Heatmap
    if st.button('Intercorrelation Heatmap'):
        generate_heatmap(df_selected_team)


# python web scraping
@st.cache
def load_data(url, header):
    html = pd.read_html(url, header=header)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats

# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def download_file(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

# generates heatmap and output csv
def generate_heatmap(df_selected_team):
    st.subheader('Intercorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')
    
    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        fig, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(fig)

if __name__ == "__main__":
    main()