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
df = pd.read_csv('wellbeing_survey.csv')

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
df.to_csv('transformed_file.csv', index=False)