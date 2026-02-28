import streamlit as st\

st.markdown("info box?", True, help=None, width="stretch", text_alignment="left",)

st.set_page_config(
    page_title="sumokwon"
)

prompt = st.chat_input("send a message")

if prompt: 
    st.write(prompt)

