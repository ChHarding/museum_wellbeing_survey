# museum_wellbeing_survey
<h1>Overview Flow Chart</h1>
<iframe width="768" height="432" src="https://miro.com/app/live-embed/uXjVKu2uH6w=/?moveToViewport=-533,-606,1766,842&embedId=334893654420" frameborder="0" scrolling="no" allow="fullscreen; clipboard-read; clipboard-write" allowfullscreen></iframe>
</p>
<p>There are two sections to this documentation:</p>
<ol>
<li>Collect survey data
a.  Streamlit/python</li>
<li>View survey results
a.  Flask/python
b.  P5.js
c.  HTML</li>
</ol>
<h1>for main.py to collect survey data in Streamlit</h1>
<h1>open new terminal</h1>
<h1> % cd museum_wellbeing_survey</h1>
<h1> % streamlit run main.py</h1>
<p>import streamlit as st
import plot_likert
import csv
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from transformers import pipeline
import warnings</p>
<h1>Suppress FutureWarnings from plot_likert library</h1>
<p>warnings.filterwarnings(&quot;ignore&quot;, category=FutureWarning, module=&quot;plot_likert&quot;)</p>
<h1>Define file paths</h1>
<p>file_path = &quot;./data/wellbeing_survey.csv&quot;
transformed_file_path = &quot;./static/data.csv&quot;
output_folder = &quot;./static/&quot;
likert_output_filename = &quot;likert_plot.png&quot;
sentiment_output_filename = &quot;sentiment_analysis_plot.png&quot;</p>
<h1>Ensure the output folder exists</h1>
<p>os.makedirs(output_folder, exist_ok=True)</p>
<h1>Define the sentiment analysis pipeline</h1>
<p>model_name = &quot;distilbert-base-uncased-finetuned-sst-2-english&quot;
sentiment_pipeline = pipeline(&quot;sentiment-analysis&quot;, model=model_name)</p>
<h1>Initialization</h1>
<p>if &#39;init_done&#39; not in st.session_state:
 st.session_state.init_done = True</p>
<h1>Define the questions</h1>
<p> st.session_state.questions = [
 &quot;I felt happy.&quot;,
 &quot;I felt engaged.&quot;,
 &quot;I felt comfortable.&quot;,
 &quot;I felt safe and secure.&quot;,
 &quot;I enjoyed the company of other people.&quot;,
 &quot;I talked to other people.&quot;,
 ]</p>
<h1>Define the header</h1>
<p> st.session_state.header = [&quot;Name&quot;] + st.session_state.questions + [&quot;Comments&quot;]</p>
<h1>Define the Likert scale</h1>
<p> original_scale = plot_likert.scales.agree5
 reversed_scale = original_scale[::-1]
 st.session_state.scale = reversed_scale</p>
<h1>Define file path</h1>
<p> st.session_state.file_path = file_path</p>
<h1>Check if the file exists</h1>
<p> st.session_state.create_new_data_file = not os.path.exists(st.session_state.file_path)</p>
<p> try:</p>
<h1>Load the CSV file</h1>
<p> df = pd.read_csv(file_path, quoting=csv.QUOTE_NONNUMERIC, encoding=&#39;utf-8&#39;)</p>
<h1>Clean any newline characters in data fields (if necessary)</h1>
<p> df.replace({r&#39;\r&#39;: &#39; &#39;, r&#39;\n&#39;: &#39; &#39;}, regex=True, inplace=True)</p>
<h1>Open the CSV file in append mode, creating it if it doesn&#39;t exist</h1>
<p> st.session_state.fo = open(st.session_state.file_path, &quot;a&quot;, newline=&#39;&#39;, encoding=&#39;utf-8&#39;)
 st.session_state.writer = csv.writer(st.session_state.fo)
 if st.session_state.create_new_data_file:
 st.session_state.writer.writerow(st.session_state.header)
 except Exception as e:
 st.error(f&quot;An error occurred while opening {st.session_state.file_path}: {e}&quot;)</p>
<h1>Inject custom CSS with st.markdown</h1>
<p>st.markdown(&quot;&quot;&quot;
 <style>
 .stTextInput&gt;div&gt;div&gt;input {
 width: 200px;
 height: 25px;
 border-radius: 5px;
 }
 .stTextInput&gt;div {
 width: 200px;
 }
 </style>
&quot;&quot;&quot;, unsafe_allow_html=True)</p>
<h1>Display a label Name with a text input</h1>
<p>st.text_input(label=&quot;Name&quot;, value=&quot;Your name&quot;, key=&quot;name&quot;)</p>
<h1>Display the questions and the Likert scale</h1>
<p>for question in st.session_state.questions:
 st.radio(question, options=st.session_state.scale, index=2, key=question) # start at neutral</p>
<h1>Display the text field for comments</h1>
<p>st.text_area(&quot;Any additional comments?&quot;, key=&quot;comments&quot;)</p>
<h1>When the submit button is pressed, print the responses and the comments</h1>
<p>if st.button(&#39;Submit&#39;):
 st.write(f&quot;Name: {st.session_state.name}&quot;)
 st.write(&quot;Responses:&quot;)
 for question in st.session_state.questions:
 st.write(f&quot;{question}: {st.session_state[question]}&quot;)
 st.write(&quot;Comments:&quot;)
 st.write(st.session_state.comments)</p>
<h1>Perform sentiment analysis on the comments</h1>
<p> comment = st.session_state.comments
 if not comment:
 sentiment_score = 0
 else:
 result = sentiment_pipeline(comment)
 sentiment_score = result[0][&#39;score&#39;] if result[0][&#39;label&#39;] == &#39;POSITIVE&#39; else -result[0][&#39;score&#39;]</p>
<h1>Save the responses and sentiment score</h1>
<p> record = [st.session_state.name] + [st.session_state[question] for question in st.session_state.questions] + [st.session_state.comments, sentiment_score]
 try:
 st.session_state.writer.writerow(record)
 st.session_state.fo.flush()
 st.success(&quot;Your responses have been recorded successfully!&quot;)
 except Exception as e:
 st.error(f&quot;An error occurred while writing to {st.session_state.file_path}: {e}&quot;)</p>
<h1>Reset form fields</h1>
<p> def clear_all():
 st.session_state.pop(&#39;init_done&#39;)
 st.session_state[&quot;name&quot;] = &quot;Your Name&quot;
 for question in st.session_state.questions:
 st.session_state[question] = st.session_state.scale[2]
 st.session_state[&quot;comments&quot;] = &quot;&quot;</p>
<p> st.button(&quot;Reset&quot;, on_click=clear_all)</p>
<h1>Read and analyze the CSV file</h1>
<p> try:
 df = pd.read_csv(file_path)
 if &#39;Sentiment Score&#39; not in df.columns:
 df[&#39;Sentiment Score&#39;] = None
 new_sentiment_scores = []
 comments = []
 original_texts = []</p>
<p> for index, row in df.iterrows():
 if pd.isna(row[&#39;Sentiment Score&#39;]):
 if pd.isna(row[&#39;Comments&#39;]) or row[&#39;Comments&#39;] == &quot;&quot;:
 score = 0
 else:
 data = row[&#39;Comments&#39;]
 results = sentiment_pipeline(data)
 score = results[0][&#39;score&#39;] if results[0][&#39;label&#39;] == &#39;POSITIVE&#39; else -results[0][&#39;score&#39;]
 df.at[index, &#39;Sentiment Score&#39;] = score
 new_sentiment_scores.append(score)
 comments.append(row[&#39;Comments&#39;])
 original_texts.append(data)
 else:
 score = row[&#39;Sentiment Score&#39;]
 new_sentiment_scores.append(score)
 comments.append(row[&#39;Comments&#39;])
 original_texts.append(row[&#39;Comments&#39;])</p>
<p> df.to_csv(file_path, index=False)
 all_scores = df[&#39;Sentiment Score&#39;].tolist()
 average_score = sum(all_scores) / len(all_scores) if all_scores else 0
 df_sentiment = pd.DataFrame({&#39;Sentiment Score&#39;: all_scores, &#39;Comment&#39;: comments, &#39;Text&#39;: original_texts})</p>
<h1>Create sentiment analysis plot</h1>
<p> colors = [&#39;green&#39; if score &gt;= 0 else &#39;red&#39; for score in df_sentiment[&#39;Sentiment Score&#39;]]
 plt.figure(figsize=(10, 6))
 bars = plt.bar(df_sentiment.index, df_sentiment[&#39;Sentiment Score&#39;], color=colors)
 plt.title(&#39;Sentiment Analysis&#39;)
 plt.ylabel(&#39;Sentiment Score&#39;)
 for bar, score in zip(bars, df_sentiment[&#39;Sentiment Score&#39;]):
 plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f&#39;{round(score, 2)}&#39;, ha=&#39;center&#39;, va=&#39;bottom&#39;, fontsize=9)
 plt.axhline(y=average_score, color=&#39;gray&#39;, linestyle=&#39;--&#39;, label=f&#39;Average Score: {round(average_score, 2)}&#39;)
 plt.legend()
 plt.tight_layout()</p>
<h1>Save the plot as PNG file</h1>
<p> plt.savefig(os.path.join(output_folder, sentiment_output_filename))
 plt.close() # Close the figure to free up memory</p>
<h1>Create Likert scale plot</h1>
<p> questions = st.session_state.questions
 likert_data = df[questions]
 unique_responses = pd.unique(likert_data.values.ravel(&#39;K&#39;))
 print(&quot;Unique responses found in the data:&quot;, unique_responses)</p>
<p> myscale = (&quot;Strongly agree&quot;, &quot;Agree&quot;, &quot;Neither agree nor disagree&quot;, &quot;Disagree&quot;, &quot;Strongly disagree&quot;)
 fig, ax = plt.subplots(figsize=(11, 2)) # Create a new figure and axes
 plot_likert.plot_likert(likert_data, myscale, plot_percentage=True, ax=ax)
 fig.tight_layout()</p>
<h1>Save the Likert plot as PNG file</h1>
<p> fig.savefig(os.path.join(output_folder, likert_output_filename))
 plt.close(fig) # Close the figure to free up memory</p>
<p> except FileNotFoundError:
 st.error(f&quot;Error: The file at {file_path} was not found.&quot;)
 except pd.errors.EmptyDataError:
 st.error(&quot;Error: The CSV file is empty.&quot;)
 except Exception as e:
 st.error(f&quot;An error occurred: {e}&quot;)</p>
<p> import pandas as pd</p>
<h1>Define the mapping dictionaries</h1>
<p>response_mapping = {
 &#39;Strongly disagree&#39;: 100,
 &#39;Disagree&#39;: 200,
 &#39;Neither agree nor disagree&#39;: 300,
 &#39;Agree&#39;: 400,
 &#39;Strongly agree&#39;: 500
}</p>
<p>width_mapping = {
 &#39;Strongly disagree&#39;: 1,
 &#39;Disagree&#39;: 2,
 &#39;Neither agree nor disagree&#39;: 3,
 &#39;Agree&#39;: 4,
 &#39;Strongly agree&#39;: 5
}</p>
<p>noise_mapping = {
 &#39;Strongly disagree&#39;: 0.0,
 &#39;Disagree&#39;: 0.25,
 &#39;Neither agree nor disagree&#39;: 0.5,
 &#39;Agree&#39;: 0.75,
 &#39;Strongly agree&#39;: 1.0
}</p>
<h1>Function to map sentiment score to 0-359</h1>
<p>def map_sentiment_to_color(value):
 return abs(value) * 359</p>
<h1>Function to create the &#39;+ or -&#39; column</h1>
<p>def create_plus_minus(value):
 return 100 if value &gt; 0 else 70</p>
<h1>Load the CSV file</h1>
<p>df = pd.read_csv(file_path)</p>
<h1>Rename columns</h1>
<p>df = df.rename(columns={
 &#39;I felt happy.&#39;: &#39;x1&#39;,
 &#39;I felt engaged.&#39;: &#39;x2&#39;,
 &#39;I felt comfortable.&#39;: &#39;y1&#39;,
 &#39;I felt safe and secure.&#39;: &#39;y2&#39;,
 &#39;I enjoyed the company of other people.&#39;: &#39;width&#39;,
 &#39;I talked to other people.&#39;: &#39;noise&#39;
})</p>
<h1>Print columns to debug</h1>
<p>print(&quot;Columns after renaming:&quot;, df.columns)</p>
<h1>Map responses to numeric values</h1>
<p>df[&#39;x1&#39;] = df[&#39;x1&#39;].map(response_mapping)
df[&#39;x2&#39;] = df[&#39;x2&#39;].map(response_mapping)
df[&#39;y1&#39;] = df[&#39;y1&#39;].map(response_mapping)
df[&#39;y2&#39;] = df[&#39;y2&#39;].map(response_mapping)
df[&#39;width&#39;] = df[&#39;width&#39;].map(width_mapping)
df[&#39;noise&#39;] = df[&#39;noise&#39;].map(noise_mapping)</p>
<h1>Add the &quot;color&quot; column by mapping sentiment score to color values (0-359)</h1>
<p>df[&#39;color&#39;] = df[&#39;Sentiment Score&#39;].apply(map_sentiment_to_color)</p>
<h1>Create the &#39;+ or -&#39; column</h1>
<p>df[&#39;+ or -&#39;] = df[&#39;Sentiment Score&#39;].apply(create_plus_minus)</p>
<h1>Drop the Name and Comments columns</h1>
<p>df = df.drop(columns=[&#39;Name&#39;, &#39;Comments&#39;])</p>
<h1>Save the transformed DataFrame to a new CSV file</h1>
<p>df.to_csv(os.path.join(transformed_file_path), index=False)</p>
<h1></h1>

