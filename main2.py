# Import necessary libraries
import streamlit as st
import plot_likert
import csv
import os
import numpy as np
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
from transformers import pipeline
from textblob import TextBlob

# Suppress FutureWarnings from plot_likert library
import warnings
warnings.filterwarnings("ignore", category=FutureWarning, module="plot_likert")

# Define paths and filenames
file_path = "./data/wellbeing_survey.csv"
output_folder = "./museum_wellbeing_survey/static/"
likert_plot_filename = "likert_plot.png"
sentiment_plot_filename = "sentiment_analysis_plot.png"

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

# Function to reset form values
def reset_form_and_reload():
    st.session_state.name = "Your name"
    st.session_state.responses = {question: st.session_state.scale[2] for question in st.session_state.questions}  # index 2 for neutral
    st.session_state.comments = ""
        # Close the CSV file
    st.session_state.fo.close()
    st.experimental_rerun() # reload the Streamlit app

# Display a label Name with a text input
name = st.text_input(label="Name", value="Your name")
responses = {}

# Display the questions and the Likert scale
for question in st.session_state.questions:
    responses[question] = st.radio(question, options=st.session_state.scale, index=2)  # start at neutral

# Display the text field for comments
comments = st.text_area("Any additional comments?")

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
    st.markdown('<iframe src="https://editor.p5js.org/amendajt/full/RQqCHN8dt" width="1000" height="600"></iframe>', unsafe_allow_html=True)

# Display the reset button after submission success message
if form_submitted:
    if st.button('Reset'):
        reset_form_and_reload()
        # Reset form inputs to initial state
        #name = "Your name"
        #responses = {question: st.session_state.scale[2] for question in st.session_state.questions}  # index 2 for neutral
        #comments = ""
        #st.experimental_rerun()  # Rerun the app to reset the form
    else:
        st.session_state.reset = False

def perform_senitment_analysis(df):
    # Define the file path
    file_path = "./data/wellbeing_survey.csv"

    # Specify the model name DistilBERT model from Hugging Face fine-tuned on the Standford Sentiment Treebank v2 (SST-2) dataset
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"

    # Create the sentiment analysis pipeline with the specified model
    sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)

        # Check if the 'Sentiment Score' column exists, if not create it
        if 'Sentiment Score' not in df.columns:
            df['Sentiment Score'] = None

        # Empty list to accumulate sentiment scores
        new_sentiment_scores = []
        comments = []
        original_texts = []

        # Iterate over each row in the DataFrame
        for index, row in df.iterrows():
            if pd.isna(row['Sentiment Score']):  # Only analyze rows without a sentiment score
                if pd.isna(row['Comments']) or row['Comments'] == "":  # If the comment is blank
                    score = 0  # Assign a score of zero
                    print(f"Row {index}: No comment, sentiment score assigned: {score}")
                else:
                    data = row['Comments']
                    results = sentiment_pipeline(data)  # Apply sentiment analysis
                    score = results[0]['score'] if results[0]['label'] == 'POSITIVE' else -results[0]['score']
                    print(f"Row {index}: Comment: {row['Comments']}, Sentiment score: {score}")

                # Update the DataFrame with the sentiment score
                df.at[index, 'Sentiment Score'] = score
                new_sentiment_scores.append(score)
                comments.append(row['Comments'])
                original_texts.append(data)
            else:
                # Existing scores should also be included in the plotting data
                score = row['Sentiment Score']
                new_sentiment_scores.append(score)
                comments.append(row['Comments'])
                original_texts.append(row['Comments'])

        # Save the updated DataFrame back to the CSV file
        df.to_csv(file_path, index=False)

        # Calculate the average sentiment score for all scores
        all_scores = df['Sentiment Score'].tolist()
        if all_scores:
            average_score = sum(all_scores) / len(all_scores)
            print(f"Average Sentiment Score: {average_score}")
        else:
            print("No comments to analyze for sentiment.")

        # Create a DataFrame to store the sentiment scores and optional comments
        df_sentiment = pd.DataFrame({'Sentiment Score': all_scores, 'Comment': comments, 'Text': original_texts})

        # Create bar chart with colored bars based on sentiment score
        colors = ['green' if score >= 0 else 'red' for score in df_sentiment['Sentiment Score']]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(df_sentiment.index, df_sentiment['Sentiment Score'], color=colors)

        # Add labels, title, and axis labels
        plt.title('Sentiment Analysis')
        plt.ylabel('Sentiment Score')

        # Add value labels on top of the bars
        for bar, score in zip(bars, df_sentiment['Sentiment Score']):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{round(score, 2)}',
                 ha='center', va='bottom', fontsize=9)

        # Add horizontal line for average sentiment score
        plt.axhline(y=average_score, color='gray', linestyle='--', label=f'Average Score: {round(average_score, 2)}')

        plt.legend()  # Show legend with average score
        plt.tight_layout()

        # Save the plot as a PNG file in the 'static' folder
        static_folder = 'static'
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)
    
        plt.savefig(f'{static_folder}/sentiment_analysis_plot.png', overwrite=True)

        # Display the plot
        plt.show()

    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")  # In case file is not found at the path
    except Exception as e:
        print(f"An error occurred: {e}")  # Catch other errors  

    