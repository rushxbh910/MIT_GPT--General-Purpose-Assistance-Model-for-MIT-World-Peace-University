
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application.query import ask_question
print("✅ Import successful")


import streamlit as st

st.title("MIT-GPT: Ask Me Anything")

query = st.text_input("Enter your question:")
if query:
    with st.spinner("Generating answer..."):
        answer = ask_question(query)
        st.write("### Answer:")
        st.success(answer)
