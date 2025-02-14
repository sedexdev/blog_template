#!/bin/bash

# pull updated repo from GitHub

echo "Starting application update..."

# Navigate to your app directory
cd "/home/your-username/your-project/"

# Pull the latest changes
git pull origin main

# run the reload script
python3 src/reload.py

echo "Update complete!"