import streamlit as st
import pandas as pd
from PIL import Image
import shap
import matplotlib.pyplot as plt
from sklearn import datasets
import pickle

def main():
    st.write("""
    # Boston House Price Prediction App
    This app predicts the **Boston House Price**!
    """)
    
    image = Image.open('boston.jpg')
    st.image(image, width=None)

    st.write("""
    Photo by [Cloris Ying](https://unsplash.com/@clorisyy?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/s/photos/boston-house?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
    
    ---
    """)

    # Loads the Boston House Price Dataset
    boston = datasets.load_boston()
    X = pd.DataFrame(boston.data, columns=boston.feature_names)
    Y = pd.DataFrame(boston.target, columns=["MEDV"])

    # Sidebar
    # Header of Specify Input Parameters
    st.sidebar.header('Specify Input Parameters')
    st.sidebar.write('Click the Submit button below after specifying all the features. Check the help button for more info.')
    with st.sidebar.form(key='form'):
        CRIM = st.slider('CRIM', float(X.CRIM.min()), float(X.CRIM.max()), float(X.CRIM.mean()), help="per capita crime rate by town")
        ZN = st.slider('ZN', float(X.ZN.min()), float(X.ZN.max()), float(X.ZN.mean()), help="proportion of residential land zoned for lots over 25,000 sq.ft.")
        INDUS = st.slider('INDUS', float(X.INDUS.min()), float(X.INDUS.max()), float(X.INDUS.mean()), help="proportion of non-retail business acres per town")
        CHAS = st.slider('CHAS', float(X.CHAS.min()), float(X.CHAS.max()), float(X.CHAS.mean()), help="Charles River dummy variable (= 1 if tract bounds river; 0 otherwise)")
        NOX = st.slider('NOX', float(X.NOX.min()), float(X.NOX.max()), float(X.NOX.mean()), help="nitrogen oxides concentration (parts per 10 million)")
        RM = st.slider('RM', float(X.RM.min()), float(X.RM.max()), float(X.RM.mean()), help="average number of rooms per dwelling")
        AGE = st.slider('AGE', float(X.AGE.min()), float(X.AGE.max()), float(X.AGE.mean()), help="proportion of owner-occupied units built prior to 1940")
        DIS = st.slider('DIS', float(X.DIS.min()), float(X.DIS.max()), float(X.DIS.mean()), help="weighted mean of distances to five Boston employment centres")
        RAD = st.slider('RAD', float(X.RAD.min()), float(X.RAD.max()), float(X.RAD.mean()), help="index of accessibility to radial highways")
        TAX = st.slider('TAX', float(X.TAX.min()), float(X.TAX.max()), float(X.TAX.mean()), help="full-value property-tax rate per $10,000")
        PTRATIO = st.slider('PTRATIO', float(X.PTRATIO.min()), float(X.PTRATIO.max()), float(X.PTRATIO.mean()), help="pupil-teacher ratio by town")
        B = st.slider('B', float(X.B.min()), float(X.B.max()), float(X.B.mean()), help="1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town")
        LSTAT = st.slider('LSTAT', float(X.LSTAT.min()), float(X.LSTAT.max()), float(X.LSTAT.mean()), help="lower status of the population (percent)")
        submit = st.form_submit_button(label='Submit')

    if submit:
        data = {'CRIM': CRIM,
                'ZN': ZN,
                'INDUS': INDUS,
                'CHAS': CHAS,
                'NOX': NOX,
                'RM': RM,
                'AGE': AGE,
                'DIS': DIS,
                'RAD': RAD,
                'TAX': TAX,
                'PTRATIO': PTRATIO,
                'B': B,
                'LSTAT': LSTAT}
        df = pd.DataFrame(data, index=[0])

        # Print specified input parameters
        st.header('Input Parameters')
        st.write(df)
        st.write('---')

        # Use Regression Model
        model = pickle.load(open('boston_reg.pkl', 'rb'))
        
        # Apply Model to Make Prediction
        prediction = model.predict(df)

        st.header('Prediction of MEDV')
        st.write("""The prediction of median value (MEDV) of owner-occupied homes in $1000s.""")
        st.write(prediction)
        st.write(f"""The predicted value is ${'{:.2f}'.format(float(prediction*1000))}""")
        st.write('---')

        # Explaining the model's predictions using SHAP values
        # https://github.com/slundberg/shap
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

        st.header('Feature Importance')
        plt.title('Feature importance based on SHAP values')
        shap.summary_plot(shap_values, X)
        st.set_option('deprecation.showPyplotGlobalUse', False) # disable warning
        st.pyplot(bbox_inches='tight')
        st.write('---')

        plt.title('Feature importance based on SHAP values (Bar)')
        shap.summary_plot(shap_values, X, plot_type="bar")
        st.pyplot(bbox_inches='tight')
        st.set_option('deprecation.showPyplotGlobalUse', False) # disable warning
    
    else:
        st.write('Submit input parameters from the sidebar.')

if __name__ == "__main__":
    main()