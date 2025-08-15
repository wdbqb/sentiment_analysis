import streamlit as st
from sentiment_analysis import generate
import pandas as pd
import re
import json



# Title
st.title("Sentiment Analysis")
st.markdown("""
This tool analyses any text you enter and identifies whether the sentiment is positive, negative, or neutral. """)

# Example card

with st.expander("Example"):
    st.write(
        "**Input**\n\n"
        "`I really enjoyed the presentation today — it was clear, engaging, and well-structured.`\n\n"
        "**Outcome**\n\n"
        "`Positive`\n\n"
        "**Reasoning**\n\n"
        "`The user explicitly states they 'really enjoyed' the presentation and uses positive adjectives like 'clear', 'engaging', and 'well-structured' to describe it.`"
    )

# text enter area
# user_input = st.text_area("Analysed Text:")


user_input = st.text_area(
    "Analysed Text:",
    placeholder="Type a sentence or short paragraph to analyse its sentiment…",
    height=160
)

#Button to submit the text

if st.button("Run Analysis"):
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

