import streamlit as st
import plot_likert
import csv
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
import warnings

# Suppress FutureWarnings from plot_likert library
warnings.filterwarnings("ignore", category=FutureWarning, module="plot_likert")

# Define file paths
file_path = "./data/wellbeing_survey.csv"
transformed_file_path = "./data/transformed_file.csv"
output_folder = "./static/"
likert_output_filename = "likert_plot.png"
sentiment_output_filename = "sentiment_analysis_plot.png"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define the sentiment analysis pipeline
model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)

# Initialization
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
    original_scale = plot_likert.scales.agree5
    reversed_scale = original_scale[::-1]
    st.session_state.scale = reversed_scale

    # Define file path
    st.session_state.file_path = file_path

    # Check if the file exists
    st.session_state.create_new_data_file = not os.path.exists(st.session_state.file_path)

    try:
        # Load the CSV file
        df = pd.read_csv(file_path, quoting=csv.QUOTE_NONNUMERIC, encoding='utf-8')
        # Clean any newline characters in data fields (if necessary)
        df.replace({r'\r': ' ', r'\n': ' '}, regex=True, inplace=True)
        # Open the CSV file in append mode, creating it if it doesn't exist
        st.session_state.fo = open(st.session_state.file_path, "a", newline='', encoding='utf-8')
        st.session_state.writer = csv.writer(st.session_state.fo)
        if st.session_state.create_new_data_file:
            st.session_state.writer.writerow(st.session_state.header)
    except Exception as e:
        st.error(f"An error occurred while opening {st.session_state.file_path}: {e}")

# Inject custom CSS with st.markdown
st.markdown("""
    <style>
    .stTextInput>div>div>input {
        width: 200px;
        height: 25px;
        border-radius: 5px;
    }
    .stTextInput>div {
        width: 200px;
    }
    </style>
""", unsafe_allow_html=True)

# Display a label Name with a text input
st.text_input(label="Name", value="Your name", key="name")

# Display the questions and the Likert scale
for question in st.session_state.questions:
    st.radio(question, options=st.session_state.scale, index=2, key=question)  # start at neutral

# Display the text field for comments
st.text_area("Any additional comments?", key="comments")

# When the submit button is pressed, print the responses and the comments
if st.button('Submit'):
    st.write(f"Name: {st.session_state.name}")
    st.write("Responses:")
    for question in st.session_state.questions:
        st.write(f"{question}: {st.session_state[question]}")
    st.write("Comments:")
    st.write(st.session_state.comments)

    # Perform sentiment analysis on the comments
    comment = st.session_state.comments
    if not comment:
        sentiment_score = 0
    else:
        result = sentiment_pipeline(comment)
        sentiment_score = result[0]['score'] if result[0]['label'] == 'POSITIVE' else -result[0]['score']

    # Save the responses and sentiment score
    record = [st.session_state.name] + [st.session_state[question] for question in st.session_state.questions] + [st.session_state.comments, sentiment_score]
    try:
        st.session_state.writer.writerow(record)
        st.session_state.fo.flush()
        st.success("Your responses have been recorded successfully!")
    except Exception as e:
        st.error(f"An error occurred while writing to {st.session_state.file_path}: {e}")

    # Reset form fields
    def clear_all():
        st.session_state.pop('init_done')
        st.session_state["name"] = "Your Name"
        for question in st.session_state.questions:
            st.session_state[question] = st.session_state.scale[2]
        st.session_state["comments"] = ""

    st.button("Reset", on_click=clear_all)

    # Read and analyze the CSV file
    try:
        df = pd.read_csv(file_path)
        if 'Sentiment Score' not in df.columns:
            df['Sentiment Score'] = None
        new_sentiment_scores = []
        comments = []
        original_texts = []
        
        for index, row in df.iterrows():
            if pd.isna(row['Sentiment Score']):
                if pd.isna(row['Comments']) or row['Comments'] == "":
                    score = 0
                else:
                    data = row['Comments']
                    results = sentiment_pipeline(data)
                    score = results[0]['score'] if results[0]['label'] == 'POSITIVE' else -results[0]['score']
                df.at[index, 'Sentiment Score'] = score
                new_sentiment_scores.append(score)
                comments.append(row['Comments'])
                original_texts.append(data)
            else:
                score = row['Sentiment Score']
                new_sentiment_scores.append(score)
                comments.append(row['Comments'])
                original_texts.append(row['Comments'])
        
        df.to_csv(file_path, index=False)
        all_scores = df['Sentiment Score'].tolist()
        average_score = sum(all_scores) / len(all_scores) if all_scores else 0
        df_sentiment = pd.DataFrame({'Sentiment Score': all_scores, 'Comment': comments, 'Text': original_texts})
        
        # Create sentiment analysis plot
        colors = ['green' if score >= 0 else 'red' for score in df_sentiment['Sentiment Score']]
        plt.figure(figsize=(10, 6))
        bars = plt.bar(df_sentiment.index, df_sentiment['Sentiment Score'], color=colors)
        plt.title('Sentiment Analysis')
        plt.ylabel('Sentiment Score')
        for bar, score in zip(bars, df_sentiment['Sentiment Score']):
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{round(score, 2)}', ha='center', va='bottom', fontsize=9)
        plt.axhline(y=average_score, color='gray', linestyle='--', label=f'Average Score: {round(average_score, 2)}')
        plt.legend()
        plt.tight_layout()

        # Save the plot as PNG file
        plt.savefig(os.path.join(output_folder, sentiment_output_filename))
        plt.close()  # Close the figure to free up memory

        # Create Likert scale plot
        questions = st.session_state.questions
        likert_data = df[questions]
        unique_responses = pd.unique(likert_data.values.ravel('K'))
        print("Unique responses found in the data:", unique_responses)

        myscale = ("Strongly agree", "Agree", "Neither agree nor disagree", "Disagree", "Strongly disagree")
        fig, ax = plt.subplots(figsize=(11, 2))  # Create a new figure and axes
        plot_likert.plot_likert(likert_data, myscale, plot_percentage=True, ax=ax)
        fig.tight_layout()

        # Save the Likert plot as PNG file
        fig.savefig(os.path.join(output_folder, likert_output_filename))
        plt.close(fig)  # Close the figure to free up memory

    except FileNotFoundError:
        st.error(f"Error: The file at {file_path} was not found.")
    except pd.errors.EmptyDataError:
        st.error("Error: The CSV file is empty.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

        import pandas as pd

# Define the mapping dictionaries
response_mapping = {
    'Strongly disagree': 100,
    'Disagree': 200,
    'Neither agree nor disagree': 300,
    'Agree': 400,
    'Strongly agree': 500
}

width_mapping = {
    'Strongly disagree': 1,
    'Disagree': 2,
    'Neither agree nor disagree': 3,
    'Agree': 4,
    'Strongly agree': 5
}

noise_mapping = {
    'Strongly disagree': 0.0,
    'Disagree': 0.25,
    'Neither agree nor disagree': 0.5,
    'Agree': 0.75,
    'Strongly agree': 1.0
}

# Function to map sentiment score to 0-359
def map_sentiment_to_color(value):
    return abs(value) * 359

# Function to create the '+ or -' column
def create_plus_minus(value):
    return 100 if value > 0 else 70

# Load the CSV file
df = pd.read_csv(file_path)

# Rename columns
df = df.rename(columns={
    'I felt happy.': 'x1',
    'I felt engaged.': 'x2',
    'I felt comfortable.': 'y1',
    'I felt safe and secure.': 'y2',
    'I enjoyed the company of other people.': 'width',
    'I talked to other people.': 'noise'
})

# Print columns to debug
print("Columns after renaming:", df.columns)

# Map responses to numeric values
df['x1'] = df['x1'].map(response_mapping)
df['x2'] = df['x2'].map(response_mapping)
df['y1'] = df['y1'].map(response_mapping)
df['y2'] = df['y2'].map(response_mapping)
df['width'] = df['width'].map(width_mapping)
df['noise'] = df['noise'].map(noise_mapping)

# Add the "color" column by mapping sentiment score to color values (0-359)
df['color'] = df['Sentiment Score'].apply(map_sentiment_to_color)

# Create the '+ or -' column
df['+ or -'] = df['Sentiment Score'].apply(create_plus_minus)

# Drop the Name and Comments columns
df = df.drop(columns=['Name', 'Comments'])

# Save the transformed DataFrame to a new CSV file
df.to_csv(transformed_file_path, index=False)


