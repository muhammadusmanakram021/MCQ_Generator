import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
from langchain_community.callbacks import get_openai_callback
from src.mcqgenerator.MCQ_Generator import generate_evaluate_chain
from src.mcqgenerator.logger import logging
import streamlit as st

# Load the JSON response file correctly
file_path=r'C:\Users\MSI TM\MCQ_Generator\Response.json'
with open(file_path, 'r') as file:
    RESPONSE_JSON = json.load(file)  # Use json.load() instead of json.loads()

st.title("MCQs Generator Application with LangChain")

with st.form("user_inputs"):
    uploaded_file = st.file_uploader("Upload a PDF or txt file")
    mcq_count = st.number_input("No. of MCQs", min_value=3, max_value=50)
    subject = st.text_input("Insert Subject", max_chars=20)
    tone = st.text_input("Complexity Level of Questions", max_chars=20, placeholder="Simple")
    button = st.form_submit_button("Generate MCQs")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Generating..."):
            try:
                text = read_file(uploaded_file)
                # Count token and the cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text": text,
                            "number": mcq_count,
                            "subject": subject,
                            "tone": tone,
                            "response_json": json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error(f"Error: {e}")  # Include the error message
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                
                if isinstance(response, dict):
                    # Extract the quiz data from the response
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        
                        # Debugging: Check the content of table_data
                        if table_data is None:
                            st.error("No table data returned.")
                        else:
                            st.write("Table Data:", table_data)  # Debugging line to see table_data content

                            if isinstance(table_data, (list, dict)):  # Check if table_data is a valid format
                                df = pd.DataFrame(table_data)
                                df.index = range(1, len(df) + 1)  # Correct index assignment
                                st.table(df)
                                # Display the review in a text box as well
                                st.text_area(label="Review", value=response["review"])
                            else:
                                st.error("Invalid format for table data.")
                    else:
                        st.error("No quiz data found in the response.")
