import streamlit as st
from sentiment_analysis import generate

# Title
st.title("Sentiment Analysis")
st.markdown("Enter some text below and click **Analyse** to get the sentiment.")


# text enter area
user_input = st.text_area("Analysed Text:")


#Button to submit the text

if st.button("Analyse Sentiment"):
    if user_input.strip() != "":
        try:
            result = generate(user_input)
            st.success(f"Sentiment: {result}")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some text to analyze.")

