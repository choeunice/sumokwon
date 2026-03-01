import streamlit as st
import json
import requests
from snowflake import connector as snowflake_connector
import sseclient
import os
import sys

# DEBUG: Print all environment variables (be careful with this in production!)
print("=== ENVIRONMENT VARIABLES (first 10 chars only) ===")
for key in ["SNOWFLAKE_HOST", "SNOWFLAKE_ACCOUNT", "SNOWFLAKE_USER", "SNOWFLAKE_API_KEY", "SNOWFLAKE_ROLE"]:
    value = os.getenv(key, "NOT SET")
    if value != "NOT SET" and len(value) > 10:
        print(f"{key}: {value[:10]}...")
    else:
        print(f"{key}: {value}")

print(f"Current working directory: {os.getcwd()}")
print(f"Files in current directory: {os.listdir('.')}")
if os.path.exists('pomelo'):
    print(f"Files in pomelo directory: {os.listdir('pomelo')}")
if os.path.exists('pomelo/.streamlit'):
    print(f"Files in pomelo/.streamlit directory: {os.listdir('pomelo/.streamlit')}")
    if os.path.exists('pomelo/.streamlit/secrets.toml'):
        print("secrets.toml exists!")
        with open('pomelo/.streamlit/secrets.toml', 'r') as f:
            content = f.read()
            # Mask sensitive data
            for line in content.split('\n'):
                if '=' in line:
                    key = line.split('=')[0].strip()
                    value = line.split('=')[1].strip().strip('"')
                    if value and len(value) > 4:
                        print(f"{key} = {value[:4]}...")
                    else:
                        print(f"{key} = {value}")
    else:
        print("secrets.toml does NOT exist!")
else:
    print("pomelo/.streamlit directory does NOT exist!")

HOST = None
ACCOUNT = None
USER = None
API_KEY = None
ROLE = None

# Define a function to load configuration
def load_config():
    global HOST, ACCOUNT, USER, API_KEY, ROLE

    print("=== LOADING CONFIG ===")
    try:    
        # replace these values in your .secrets.toml file, not here!
        print("Trying st.secrets...")
        print(f"st.secrets keys: {st.secrets.keys()}")
        if "snowflake" in st.secrets:
            print(f"snowflake keys: {st.secrets['snowflake'].keys()}")
            
        HOST = st.secrets["snowflake"]["host"]
        ACCOUNT = st.secrets["snowflake"]["account"]
        USER = st.secrets["snowflake"]["user"]
        API_KEY = st.secrets["snowflake"]["api_key"]
        ROLE = st.secrets["snowflake"]["role"]
        
        print(f"✅ Loaded from secrets: USER={USER}, HOST={HOST}")

    except Exception as e:
        print(f"❌ Failed to load from st.secrets: {e}")
        print("Falling back to environment variables...")
        HOST = os.getenv("SNOWFLAKE_HOST")
        ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
        USER = os.getenv("SNOWFLAKE_USER")
        API_KEY = os.getenv("SNOWFLAKE_API_KEY")
        ROLE = os.getenv("SNOWFLAKE_ROLE")
        
        print(f"From env: USER={USER}, HOST={HOST}")

# Call load_config immediately
load_config()

st.set_page_config(
    page_title="sumokwon"
)

def connect_to_snowflake():
    # connection
    if 'CONN' not in st.session_state or st.session_state.CONN is None:
        st.session_state.CONN = None

        try:
            print("=== ATTEMPTING SNOWFLAKE CONNECTION ===")
            print(f"Connection params: user={USER}, account={ACCOUNT}, host={HOST}, role={ROLE}")
            print(f"API_KEY exists: {'Yes' if API_KEY else 'No'}")
            
            # Check if any params are None or empty
            if not USER:
                st.error("USER is empty! Check secrets or environment variables.", icon="🚨")
                return
                
            st.session_state.CONN = snowflake_connector.connect(
                user=USER,
                password=API_KEY,
                account=ACCOUNT,
                host=HOST,
                port=443,
                role=ROLE
            )  
            st.success('Snowflake Connection established!', icon="💡")    
        except Exception as e:
            st.error(f'Connection failed: {str(e)}', icon="🚨")
            print(f"❌ Connection exception: {e}")

# Rest of your functions remain the same...
def clear_chat_history():
    st.session_state.messages = default_message

def api_call(prompt: str):
    # ... (keep your existing api_call function)

def main():
    st.sidebar.title("수목원")
    st.sidebar.button('Clear chat history', on_click=clear_chat_history)
    connect_to_snowflake()
    # ... (rest of your main function)

# Make sure to define default_message before using it
default_message = [{"role": "assistant", "content": "Hi. I'm a simple chat bot that uses `"+MODEL_NAME+"` to answer questions. Ask me anything."}]
MODEL_NAME = "claude-3-5-sonnet"
icons = {"assistant": "🌳", "user": "🦋"}

if __name__ == "__main__":
    main()