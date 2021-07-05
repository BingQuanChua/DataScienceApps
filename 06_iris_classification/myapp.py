import streamlit as st
import pandas as pd
from PIL import Image
from sklearn import datasets
import pickle


def main():

    st.set_page_config(layout="wide")
    
    st.write("""
    # Simple Iris Flower Prediction App
    This app predicts the **Iris flower** type! Image by [Hulkido](https://github.com/Hulkido/Fisheriris_MATLAB)
    """)

    image = Image.open('iris_type.jpeg')
    st.image(image)

    st.write("""
    Input your data from the sidebar on the left.
    """)

    # User input
    st.sidebar.header('User Input Parameters')
    df = user_input_features()

    st.subheader('User Input Parameters')
    st.write(df)

    iris = datasets.load_iris()
    prediction, prediction_proba = predict(df)
    
    st.subheader('Class labels and their corresponding index number')
    st.write(iris.target_names)

    st.subheader('Prediction')
    st.write(iris.target_names[prediction])
    # st.write(prediction) # shows the index

    st.subheader('Prediction Probability')
    st.write(prediction_proba)


def user_input_features():
    sepal_length = st.sidebar.slider('Sepal length', 4.3, 7.9, 5.4)
    sepal_width = st.sidebar.slider('Sepal width', 2.0, 4.4, 3.4)
    petal_length = st.sidebar.slider('Petal length', 1.0, 6.9, 1.3)
    petal_width = st.sidebar.slider('Petal width', 0.1, 2.5, 0.2)
    data = {'sepal_length': sepal_length,
            'sepal_width': sepal_width,
            'petal_length': petal_length,
            'petal_width': petal_width}
    features = pd.DataFrame(data, index=[0])
    return features


def predict(df):

    clf = pickle.load(open('iris_clf.pkl', 'rb'))
    prediction = clf.predict(df)
    prediction_proba = clf.predict_proba(df)

    return prediction, prediction_proba


if __name__ == "__main__":
    main()