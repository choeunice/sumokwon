import streamlit as st
import json
import requests
from snowflake import connector as snowflake_connector
# import snowflake.connector
import sseclient

#st.markdown("info box?", True, help=None, width="stretch", text_alignment="left",)


# replace these values in your .secrets.toml file, not here!
HOST = st.secrets["snowflake"]["host"]
ACCOUNT = st.secrets["snowflake"]["account"]
USER =st.secrets["snowflake"]["user"]
API_KEY = st.secrets["snowflake"]["api_key"]
ROLE = st.secrets["snowflake"]["role"]


st.set_page_config(
    page_title="sumokwon"
)

# prompt = st.chat_input("send a message")

# if prompt: 
#     st.write(prompt)

# API configuration 
API_ENDPOINT = "/api/v2/cortex/inference:complete"
API_TIMEOUT = 50000  # in milliseconds
MODEL_NAME = "claude-3-5-sonnet" # change me to mistral-large2, llama3.1-70b or claude-3-5-sonnet and see what happens!

# Chat assistant defaults 
icons = {"assistant": "❄️", "user": "⛷️"}

default_message = [{"role": "assistant", "content": "Hi. I'm a simple chat bot that uses `"+MODEL_NAME+"` to answer questions. Ask me anything."}]


def clear_chat_history():
    st.session_state.messages = default_message


def api_call(prompt: str):

    text = ""
    sql = ""
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "content": prompt
            }
        ],
        "top_p": 0,
        "temperature": 0
    }
    
    resp = requests.post(
            url=f"https://{HOST}"+API_ENDPOINT,
            json=payload,
            headers={
                "Authorization": f'Snowflake Token="{st.session_state.CONN.rest.token}"'
            }
        ,stream=True)

    #try:
    if resp.status_code < 400:
        client = sseclient.SSEClient(resp)


        for event in client.events():

            try: 
                parsed = json.loads(event.data)

                try: 
                    if parsed['choices'][0]['delta']['type'] == 'text': 
                        text = parsed['choices'][0]['delta']['text']
                        #parsed
                        yield text

                    else: 
                        text = parsed
                        yield text


                except:
                    continue
            except:
                continue


def connect_to_snowflake():
    # connection
    if 'CONN' not in st.session_state or st.session_state.CONN is None:
        st.session_state.CONN = None

        try: 
            st.session_state.CONN = snowflake_connector.connect(
                user=USER,
                password=API_KEY,
                account=ACCOUNT,
                host=HOST,
                port=443,
                role=ROLE
            )  
            st.info('Snowflake Connection established!', icon="💡")    
        except:
            st.error('Connection not established. Check that you have correctly entered your Snowflake credentials!', icon="🚨")    

def main():

    st.sidebar.title("My First Chat App")

    st.sidebar.caption("Visit [CORTEX PLAYGROUND](https://app.snowflake.com/_deeplink/#/cortex/playground) for an interactive interface to test out models, and view model availability")

    st.sidebar.button('Clear chat history', on_click=clear_chat_history)

    connect_to_snowflake()

    #  Initialize session state
    # Store LLM-generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = default_message

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.write(message["content"])


    # User-provided prompt
    if prompt := st.chat_input(disabled=not st.session_state.CONN):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=icons["user"]):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant", avatar=icons["assistant"]):
            response = api_call(prompt)
            full_response = st.write_stream(response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
            
   
if __name__ == "__main__":
    main()

