#!/bin/bash

# Setup script for Secure Chat Room

# Exit on error
set -e

# Define paths
BASE_DIR="$(pwd)"
DB_DIR="$BASE_DIR/database"
SCHEMA_FILE="$DB_DIR/schema.sql"
DB_FILE="$DB_DIR/chat.db"

# Create database directory if it doesn't exist
mkdir -p "$DB_DIR"

# Create schema.sql if it doesn't exist
if [ ! -f "$SCHEMA_FILE" ]; then
    echo "Creating schema.sql..."
    cat << EOF > "$SCHEMA_FILE"
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL,
    timestamp TEXT NOT NULL
);
EOF
fi

# Initialize the database
echo "Initializing database..."
python server/db.py

# Verify database creation
if [ -f "$DB_FILE" ]; then
    echo "Database initialized successfully at $DB_FILE"
else
    echo "Error: Database file $DB_FILE was not created"
    exit 1
fi

echo "Setup complete. Set ENCRYPTION_KEY and run the server and client."
echo "Example: export ENCRYPTION_KEY=\$(python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\")"