import streamlit as st

# create a function that sets the value in state back to the default value 'B'
def clear_all():
    for i in selections:
        st.session_state[f'radio{i}'] = 'B'
    return

st.title("Reset radio buttons with stateful button")

selections = ["a", "b", "c", "d"]

for i in selections:
    st.radio(f"Select option for {i}", options=['A', 'B', 'C'], index=1, key=f'radio{i}')

# check state
st.session_state

# create your button to reset the state of the radio buttons to 'B'
st.button("Reset all to B", on_click=clear_all)