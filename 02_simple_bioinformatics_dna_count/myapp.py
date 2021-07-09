import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

def main():
    image = Image.open('dna.jpg')
    st.image(image)

    st.write('''
    Photo by [PublicDomainPictures](https://pixabay.com/users/publicdomainpictures-14/) on [Pixabay](https://pixabay.com)
    

    # DNA Nucleotide Count Web App

    This app counts the nucleotide composition of query DNA!

    ***
    ''')

    ## input text box

    st.header('Enter DNA sequence')

    sequence_input = "GAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

    #sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
    with st.form(key='input'):
        sequence = st.text_area("Sequence input", sequence_input, help="type the DNA sequence", height=250)
        submit = st.form_submit_button(label='Submit')

    if submit:
        sequence = sequence.splitlines()
        sequence = ''.join(sequence) # concatenates list to string

        st.write("""
        ***
        """)

        ## Prints the input DNA sequence
        st.header('Input (DNA Query)')
        st.text(sequence)

        ## DNA nucleotide count
        st.header('Output (DNA Nucleotide Count)')

        col1, col2 = st.beta_columns((1,1))

        # different ways of displaying the output
        #############################################################
        col1.subheader('Dictionary Output')

        

        X = dna_nucleotide_count(sequence)

        # key and value of the dictionary
        # X_label = list(X)
        # X_values = list(X.values())

        col1.write(X)

        #############################################################
        col1.subheader('Text output')
        col1.write('There are  ' + str(X['A']) + ' adenine (A).')
        col1.write('There are  ' + str(X['T']) + ' thymine (T).')
        col1.write('There are  ' + str(X['G']) + ' guanine (G).')
        col1.write('There are  ' + str(X['C']) + ' cytosine (C).')

        #############################################################
        col2.subheader('Display DataFrame')
        df = pd.DataFrame.from_dict(X, orient='index')
        df = df.rename({0: 'count'}, axis='columns')
        df.reset_index(inplace=True)
        df = df.rename(columns = {'index':'nucleotide'})
        col2.write(df)

        #############################################################
        col2.subheader('Bar Chart Display')
        p = alt.Chart(df).mark_bar().encode( # displaying plot using altair
            x='nucleotide',
            y='count'
        )
        p = p.properties(
            width=alt.Step(80)  # controls width of bar.
        )
        col2.write(p)
        #############################################################

def dna_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C'))
    ])
    return d

if __name__ == "__main__":
    main()