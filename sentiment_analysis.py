
import csv
from transformers import pipeline

# Define the file path
file_path = "museum_wellbeing_survey/data/wellbeing_survey.csv"

# Specify the model name DistilBERT model from Hugging Face fine-tined on the Standford Sentiment Treebank v2 (SST-2) dataset
model_name = "distilbert-base-uncased-finetuned-sst-2-english"

# Create the sentiment analysis pipeline with the specified model
sentiment_pipeline = pipeline("sentiment-analysis", model=model_name)
try:
    # Open the CSV file for reading
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        
        # Iterate over each row and print the 8th element
        for row in reader:
            # Check if the row has at least 8 elements
            if len(row) >= 8:
                data = row[7] # Get the 8th element from each row
                results = sentiment_pipeline(data) # Apply sentiment analysis
                print("Comment:", row[7], results) # Show the comment and the sentiment result
                if row[7] == "": # If the entry is blank, say so
                    print("No comment")
            else:
                print("Row does not have 8 elements:", row) # Check for missing data elements

except FileNotFoundError:
    print(f"Error: The file at {file_path} was not found.") # In case file is not found at the path
except Exception as e:
    print(f"An error occurred: {e}") # Catch other error