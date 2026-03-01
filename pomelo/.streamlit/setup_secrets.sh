#!/bin/bash

# Create the .streamlit directory
mkdir -p /workspace/.streamlit

# Create secrets.toml from environment variables
cat <<EOF > /workspace/.streamlit/secrets.toml
[snowflake]
host = "${SNOWFLAKE_HOST}"
account = "${SNOWFLAKE_ACCOUNT}"
user = "${SNOWFLAKE_USER}"
api_key = "${SNOWFLAKE_API_KEY}"
role = "${SNOWFLAKE_ROLE}"
EOF

echo "Secrets file created successfully"