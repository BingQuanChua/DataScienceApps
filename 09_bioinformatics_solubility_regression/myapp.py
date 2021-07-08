######################
# Import libraries
######################
import numpy as np
import pandas as pd
import streamlit as st
import pickle
from PIL import Image
import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors


def main():
    ######################
    # Page Title
    ######################

    st.set_page_config(layout="wide")
    image = Image.open('solubility.png')
    st.image(image, use_column_width=True)

    st.write("""
    Photo by [Terry Vlisidis](https://unsplash.com/@vlisidis?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/chemistry?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
    

    # Molecular Solubility Prediction Web App

    This app predicts the **Solubility (LogS)** values of molecules!

    Data obtained from the John S. Delaney. [ESOL:  Estimating Aqueous Solubility Directly from Molecular Structure](https://pubs.acs.org/doi/10.1021/ci034243x). ***J. Chem. Inf. Comput. Sci.*** 2004, 44, 3, 1000-1005.
    ***
    """)

    ######################
    # Input molecules (Side Panel)
    ######################

    st.sidebar.header('User Input Features')

    ## Read SMILES input
    smiles_input = "C(=O)=O\nCC(=O)OC1=CC=CC=C1C(=O)O"
    st.sidebar.write("The **Simplified Molecular-Input Line-Entry System** (SMILES) is a specification in the form of a line notation for describing the structure of chemical species using short ASCII strings.")
    smiles = st.sidebar.text_area("SMILES input", smiles_input, help="Accepts multiple inputs separated by new line")
    smiles = smiles.split('\n')

    st.header('Input SMILES')
    smiles

    ## Calculate molecular descriptors
    st.header('Computed molecular descriptors')
    X = generate(smiles)
    titles = pd.DataFrame({
        "SMILES": smiles
    })
    computed_descriptors = pd.concat([titles, X], axis=1)
    computed_descriptors

    ######################
    # Pre-built model
    ######################

    # Reads in saved model
    load_model = pickle.load(open('solubility_model.pkl', 'rb'))

    # Apply model to make predictions
    prediction = load_model.predict(X)
    #prediction_proba = load_model.predict_proba(X)

    st.header('Predicted LogS values')
    prediction = pd.DataFrame({
        "Predicted LogS": prediction
    })
    predicted_values = pd.concat([titles, prediction], axis=1)
    predicted_values


######################
# Custom function
######################
## Calculate molecular descriptors
def AromaticProportion(m):
  aromatic_atoms = [m.GetAtomWithIdx(i).GetIsAromatic() for i in range(m.GetNumAtoms())]
  aa_count = []
  for i in aromatic_atoms:
    if i==True:
      aa_count.append(1)
  AromaticAtom = sum(aa_count)
  HeavyAtom = Descriptors.HeavyAtomCount(m)
  AR = AromaticAtom/HeavyAtom
  return AR


def generate(smiles, verbose=False):

    moldata= []
    for elem in smiles:
        mol=Chem.MolFromSmiles(elem)
        moldata.append(mol)

    baseData= np.arange(1,1)
    i=0
    for mol in moldata:
        desc_MolLogP = Descriptors.MolLogP(mol)
        desc_MolWt = Descriptors.MolWt(mol)
        desc_NumRotatableBonds = Descriptors.NumRotatableBonds(mol)
        desc_AromaticProportion = AromaticProportion(mol)

        row = np.array([desc_MolLogP,
                        desc_MolWt,
                        desc_NumRotatableBonds,
                        desc_AromaticProportion])

        if(i==0):
            baseData=row
        else:
            baseData=np.vstack([baseData, row])
        i=i+1

    columnNames=["MolLogP","MolWt","NumRotatableBonds","AromaticProportion"]
    descriptors = pd.DataFrame(data=baseData,columns=columnNames)

    return descriptors

if __name__ == "__main__":
    main()