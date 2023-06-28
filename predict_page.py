import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', "rb") as f:
        data = pickle.load(f)
    return data

data = load_model()

decision_forest_model = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.title("Software Developer Salary Prediction")
    
    st.write("""### Enter your info to predict your salary""")
    
    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",                
        "Brazil",              
        "France",                 
        "Spain",                  
        "Australia",              
        "Netherlands",            
        "Poland",                 
        "Italy",                 
        "Russian Federation",     
        "Sweden"                 
    )
    
    educations = (
        "Less than a Bachelor’s",
        "Post Grad",
        'Master’s degree',
        'Bachelor’s degree'
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education", educations)
    
    experience = st.slider("Years of Experience", 0, 50, 3)
    
    ok = st.button("Calculate Salary")
    if ok:
        user_input = np.array([[country, education, experience]])
        user_input[:, 0] = le_country.transform(user_input[:, 0])
        user_input[:, 1] = le_education.transform(user_input[:, 1])
        user_input = user_input.astype(float)
        
        salary = decision_forest_model.predict(user_input)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
    
    
        
    