import pandas as pd
import plot_likert
import matplotlib.pyplot as plt
import os


file_path = "./data/wellbeing_survey.csv"
output_folder = "./museum_wellbeing_survey/static/" 
output_filename = "likert_plot.png"  # Ensure the filename ends with .png
output_path = os.path.join(output_folder, output_filename)

try:
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Check the unique values to identify responses
    questions = [
        "I felt happy.",
        "I felt engaged.",
        "I felt comfortable.",
        "I felt safe and secure.",
        "I enjoyed the company of other people.",
        "I talked to other people.",
    ]

    # Get relevant columns for Likert scale analysis
    likert_data = df[questions]
    unique_responses = pd.unique(likert_data.values.ravel('K'))
    print("Unique responses found in the data:", unique_responses)

    # Define the Likert scale
    myscale = ("Strongly agree", "Agree", "Neither agree nor disagree", "Disagree", "Strongly disagree")

    # Plot the Likert data
    fig, ax = plot_likert.plot_likert(likert_data, myscale, plot_percentage=True, figsize=(11, 2))

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Save the plot as PNG file
    fig.savefig(output_path)
    print(f"Plot saved as {output_path}")

except FileNotFoundError:
    print(f"Error: The file at {file_path} was not found.") 
except pd.errors.EmptyDataError:
    print("Error: The CSV file is empty.")
except Exception as e:
    print(f"An error occurred: {e}")