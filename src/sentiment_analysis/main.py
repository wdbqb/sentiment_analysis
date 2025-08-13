import streamlit as st
from sentiment_analysis import generate
import pandas as pd
import re
import json



# Title
st.title("Sentiment Analysis")
st.markdown("Enter some text below and click **Analyse** to get the sentiment.")


# text enter area
user_input = st.text_area("Analysed Text:")


#Button to submit the text

if st.button("Analyse Sentiment"):
    if user_input.strip() != "":
        try:
            result = str(generate(user_input))
            # parse result
            match = re.search(r'(\{.*\})', result, re.DOTALL)

            if match:
                json_text = match.group(1)
                data = json.loads(json_text)
            else:
                st.write("JSON cannot be parsed.")
                data = None

            # Two separate result boxes
            st.subheader("Outcome")
            st.write(data['sentiment'])

            st.subheader("Reason")
            st.write(data['reasoning'])
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter some text to analyze.")

