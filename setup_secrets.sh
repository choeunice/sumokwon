#!/bin/bash

echo "🚀 Starting secrets file creation..."
echo "Current directory: $(pwd)"
echo "Listing root directory:"
ls -la

# Create the .streamlit directory inside the pomelo folder
mkdir -p pomelo/.streamlit

# Create the secrets.toml file
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
echo ""
echo "Verifying file exists:"
ls -la pomelo/.streamlit/