import streamlit as st
from functionality import chatbot_find_restaurants_near_me

st.title("Food Oracle")
prompt = st.text_input(label="Tell me what you want to eat and I will tell you where to go.")
st.write(chatbot_find_restaurants_near_me(prompt, 'burger'))




    
    