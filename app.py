import streamlit as st
from predict_page import show_predict_page
# from explore_page import show_explore_page

response = st.sidebar.selectbox("Explore or Predict", ("Predict", "Explore"))

show_predict_page()

# if response == "Predict":
#     show_predict_page()
# else:
#     show_explore_page()
