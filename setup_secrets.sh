#!/bin/bash

echo "🚀 Starting secrets file creation..."
echo "Current directory: $(pwd)"
echo "SNOWFLAKE_USER = '$SNOWFLAKE_USER'"
echo "SNOWFLAKE_HOST = '$SNOWFLAKE_HOST'"

# Check if critical variables are empty
if [ -z "$SNOWFLAKE_USER" ]; then
    echo "❌ ERROR: SNOWFLAKE_USER is not set!"
    exit 1
fi

if [ -z "$SNOWFLAKE_HOST" ]; then
    echo "❌ ERROR: SNOWFLAKE_HOST is not set!"
    exit 1
fi

# Create the .streamlit directory inside the pomelo folder
mkdir -p pomelo/.streamlit

# Create the secrets.toml file - NOTE: using api_key NOT password
cat > pomelo/.streamlit/secrets.toml << EOF
[snowflake]
host = "$SNOWFLAKE_HOST"
account = "$SNOWFLAKE_ACCOUNT"
user = "$SNOWFLAKE_USER"
api_key = "$SNOWFLAKE_API_KEY"
role = "$SNOWFLAKE_ROLE"
EOF

echo "✅ Secrets file created successfully at pomelo/.streamlit/secrets.toml"
echo "File contents:"
cat pomelo/.streamlit/secrets.toml