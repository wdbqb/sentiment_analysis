import streamlit as st
import pandas as pd

st.title("Sentiment Analysis")
st.markdown("Enter some text below and click **Analyse** to get the sentiment.")
user_input = st.text_area("Analysed Text:")
if st.button("Analyse"):
    st.balloons()

if st.button("Analyse"):
    if not user_input.strip():
        st.warning("Please enter some text to analyse.")
