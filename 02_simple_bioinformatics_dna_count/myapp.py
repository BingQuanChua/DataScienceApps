import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

image = Image.open('dna.jpg')

st.image(image, use_column_width=True)

st.write('''
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
''')

## input text box

st.header('Enter DNA sequence')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

#sequence = st.sidebar.text_area("Sequence input", sequence_input, height=250)
sequence = st.text_area("Sequence input", sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:] # skips the sequence name (first line)
sequence = ''.join(sequence) # concatenates list to string

st.write("""
***
""")

## Prints the input DNA sequence
st.header('Input (DNA Query)')
sequence

## DNA nucleotide count
st.header('Output (DNA Nucleotide Count)')

# different ways of displaying the output
#############################################################
st.subheader('Dictionary Output')

def dna_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C'))
    ])
    return d

X = dna_nucleotide_count(sequence)

# key and value of the dictionary
# X_label = list(X)
# X_values = list(X.values())

X

#############################################################
st.subheader('Text output')
st.write('There are  ' + str(X['A']) + ' adenine (A).')
st.write('There are  ' + str(X['T']) + ' thymine (T).')
st.write('There are  ' + str(X['G']) + ' guanine (G).')
st.write('There are  ' + str(X['C']) + ' cytosine (C).')

#############################################################
st.subheader('Display DataFrame')
df = pd.DataFrame.from_dict(X, orient='index')
df = df.rename({0: 'count'}, axis='columns')
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'nucleotide'})
st.write(df)

#############################################################
st.subheader('Display Bar Chart')
p = alt.Chart(df).mark_bar().encode( # displaying plot using altair
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(80)  # controls width of bar.
)
st.write(p)
#############################################################