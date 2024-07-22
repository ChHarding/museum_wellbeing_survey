# pip install streamlit
# to run the Streamlit server open a terminal and run this:
# cd museum_wellbeing_survey
# streamlit run main.py

import streamlit as st
import plot_likert
import csv
import os
import sys
import numpy as np
import pandas as pd
import subprocess

# Suppress FutureWarnings from plot_likert library
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="plot_likert")



# CH
# this will only be done once, despite streamlit running this file
# at every refresh. So let's do all the init stuff here ....
# st.session_state is a dictionary that persists across reruns of the script
# it will have a key init_done after the first run
if 'init_done' not in st.session_state:
    st.session_state.init_done = True
    # Define the questions
    st.session_state.questions = [
        "I felt happy.",
        "I felt engaged.",
        "I felt comfortable.",
        "I felt safe and secure.",
        "I enjoyed the company of other people.",
        "I talked to other people.",
    ]

    # Define the header
    st.session_state.header = ["Name"] + st.session_state.questions + ["Comments"]

    # Define the Likert scale
    st.session_state.scale = plot_likert.scales.agree5

    # Create a dictionary to store the responses
    st.session_state.responses = {}

    # check where the interpreter is "sitting", must be the root of the project
    # To ensure this, you must open the project root folder(!) in VSCode and then
    # start this file, not just load this file into the editor 
    #print("Current working directory:", os.getcwd())
    #print("files in data folder:", os.listdir("./data"))
    st.session_state.file_path = "./data/wellbeing_survey.csv"

    # do we already have the file?
    st.session_state.create_new_data_file = True if not os.path.exists(st.session_state.file_path) else False

    try:
        # Open the CSV file in append mode, creating it if it doesn't exist
        st.session_state.fo = open(st.session_state.file_path, "a", newline='', encoding='utf-8')
    except Exception as e:
        st.error(f"An error occurred while opening {st.session_state.file_path}: {e}")
    
    st.session_state.writer = csv.writer(st.session_state.fo)
    
    if st.session_state.create_new_data_file:
        st.session_state.writer.writerow(st.session_state.header)
   

    #writer = csv.writer(fo) # this is the csv writer object

    #if create_new_data_file == True:
        #print(file_path, "does not exist, will create it.")
        #writer.writerow(header)
    #else:
        #print(file_path, "exists, will append to it.")

# Inject custom CSS with st.markdown
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        width: 200px;
        height: 25px;
        //border: 2px solid #4CAF50;
        border-radius: 5px;
    }
    /* Target the container of the input field to adjust background and size */
    .stTextInput>div {
        width: 200px; /* Adjust container width to fit the input field */
    }
    </style>
""", unsafe_allow_html=True)


# Display a label Name with a text input
name = st.text_input(label="Name", value="Your name")
responses = {}

# Display the questions and the Likert scale
for question in st.session_state.questions:
    responses[question] = st.radio(question, options=st.session_state.scale, index=2)  # start at neutral

# Display the text field for comments
comments = st.text_area("Any additional comments?")

# Function to reset the values
def clear_all():
    for question in st.session_state.questions:
        st.session_state[f'response_{question}'] = st.session_state.scale[2]  # reset to neutral (index 2)
    st.session_state.name = "Your name"
    st.session_state.comments = "Comments"
    return

# flag to track if form was submitted
form_submitted = False

# When the submit button is pressed, print the responses and the comments
if st.button('Submit'):
    st.write(f"Name: {name}")
    st.write("Responses:")
    for question, response in responses.items():
        st.write(f"{question}: {response}")
    st.write("Comments:")
    st.write(comments)


    # Prepare the record for saving
    record = [name] + [responses[question] for question in st.session_state.questions] + [comments]
    #st.write(f"Record to be saved: {record}")  # Debug

    # Write the record
    #writer.writerow(record)
    st.session_state.writer.writerow(record)
    st.session_state.fo.flush()
    # flush the buffer to disk
    # this may be needed b/c unless this app is closed, the file will not be closed
    # and so anything in the buffer will be lost
        
    st.success("Your responses have been recorded successfully!")
    form_submitted = True
    # Button to reset all values to default
    st.button("Reset", on_click=clear_all)
    st.markdown('<iframe src="https://editor.p5js.org/amendajt/full/RQqCHN8dt" width="1000" height="600"></iframe>', unsafe_allow_html=True)


    # Reset state after submission
    clear_all()



# Display the session state for debugging
st.write(st.session_state)
