#!/bin/bash

echo "Starting setup process..."

# Step 1: Install required tools
echo "Installing required tools..."
bash dependencies/install-required-tools.sh
echo "Required tools installed successfully!"

# Step 2: Install Python dependencies
echo "Installing Python dependencies..."
python3 -m pip install -r dependencies/requirements.txt
echo "Python dependencies installed successfully!"

# Step 3: Download Nuclei templates
echo "Downloading Nuclei templates..."
python3 dependencies/nuclei-templates-downloader.py
echo "Nuclei templates downloaded successfully!"

echo "Setup process complete!"