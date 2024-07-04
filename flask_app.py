from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Define the file path
file_path = "museum_wellbeing_survey/data/wellbeing_survey.csv"

@app.route('/')
def index():
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

        # Ensure all questions are in the DataFrame
        for question in questions:
            if question not in df.columns:
                raise KeyError(f"Column '{question}' not found in the CSV file.")

        # Get relevant columns for Likert scale analysis
        likert_data = df[questions]

        # Create a plot
        fig = px.histogram(likert_data.melt(var_name='Question', value_name='Response'), 
                           x='Response', color='Question', barmode='group', 
                           category_orders={"Response": ["Strongly agree", "Agree", "Neither agree nor disagree", "Disagree", "Strongly disagree"]})

        # Convert the plot to HTML
        plot_html = pio.to_html(fig, full_html=False)

    except FileNotFoundError:
        return f"Error: The file at {file_path} was not found."
    except pd.errors.EmptyDataError:
        return "Error: The CSV file is empty."
    except KeyError as e:
        return f"An error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"

    # Render the plot in an HTML template
    return render_template('index.html', plot_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)