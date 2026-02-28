import streamlit as st

st.set_page_config(
    page_title="sumokwon"
)

prompt = st.chat_input("send a message")

if prompt: 
    st.write(prompt)