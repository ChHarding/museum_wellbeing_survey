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
import time

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
st.text_input(label="Name", value="Your name", key="name") # => st.session_state.name


# Display the questions and the Likert scale
for question in st.session_state.questions:
    # This automatically updates st.session_state.responses[question] with key=question
    st.radio(question, options=st.session_state.scale, index=2, key=question)  # start at neutral


# Display the text field for comments
st.text_area("Any additional comments?", key="comments")

st.session_state



# When the submit button is pressed, print the responses and the comments
if st.button('Submit'):
    st.write(f"Name: {st.session_state.name}")
    st.write("Responses:")
    for question in st.session_state.questions:
        st.write(f"{question}: {st.session_state[question]}")
    st.write("Comments:")
    st.write(st.session_state.comments)


    # Prepare the record for saving
    record = [st.session_state.comments] + [st.session_state[question] for question in st.session_state.questions] + [st.session_state.comments]
    #st.write(f"Record to be saved: {record}")  # Debug

    # Write the record
    #writer.writerow(record)
    st.session_state.writer.writerow(record)
    st.session_state.fo.flush()
    # flush the buffer to disk
    # this may be needed b/c unless this app is closed, the file will not be closed
    # and so anything in the buffer will be lost
        
    st.success("Your responses have been recorded successfully!")

    def clear_all():
        st.session_state.pop('init_done')
        
        # Close the CSV file
        st.session_state.fo.close()
        
        # set all values back to default
        st.session_state["name"] = "Your name"

        # set all responses back to neutral (value 2)
        for question in st.session_state.questions:
            st.session_state[question] = st.session_state.scale[2]  
        st.session_state["comments"] = ""


        

    # create your button to reset the state of the radio buttons to 'B'
    st.button("End Session", on_click=clear_all)





