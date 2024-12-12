#!/bin/bash

# Define the root directory
ROOT_DIR="$(dirname "$0")"

# Delete the 'figures' directory in the root directory if it exists
if [ -d "$ROOT_DIR/figures" ]; then
    echo "Removing existing 'figures' directory..."
    rm -rf "$ROOT_DIR/figures"
fi

# Create a new empty 'figures' directory in the root directory
mkdir -p "$ROOT_DIR/figures"
echo "Created new 'figures' directory in the root directory."

# Run all Python files in the /code directory
for file in "$ROOT_DIR/code"/*.py; do
    if [ -f "$file" ]; then  # Ensure the file exists
        echo "Running $file"
        python "$file"
    else
        echo "No Python files found in $ROOT_DIR/code."
    fi
done
