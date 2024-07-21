import streamlit as st
import streamlit.components.v1 as components


# Check if the JS file has already been loaded
if 'js_loaded' not in st.session_state:

    # Load kaleidoscope.js file 
    
    try:
        f = open("results_kaleidoscope.js", "r")
        p5_sketch = f.read()
    except:
        st.write("Error loading results_kaleidoscope.js")
    
    finally:
        f.close()
        # This flag ensures that the JS file is only loaded once
        st.session_state['js_loaded'] = True

        # Store the JS content in session state to use later
        st.session_state['p5_sketch'] = p5_sketch
else:
    # Retrieve the JS content from session state
    p5_sketch = st.session_state['p5_sketch']
    p5_sketch = '<iframe src="https://editor.p5js.org/amendajt/full/RQqCHN8dt" width="900" height="900"></iframe>'


# Embed the p5.js sketch in Streamlit
components.html(p5_sketch, height=900, width=900)