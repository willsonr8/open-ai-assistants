import streamlit as st
from functionality import chatbot_find_bars_near_me

st.title("Bar Oracle")
prompt = st.text_input(label="Tell me what you want to drink and I will tell you where to go.")
st.write(chatbot_find_bars_near_me(prompt))
