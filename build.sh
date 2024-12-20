#!/bin/bash
# exit on error
set -o errexit

# Make script executable
chmod +x build.sh

# Install system dependencies
apt-get update -y
apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng

# Create and set permissions for necessary directories
mkdir -p uploads
chmod 777 uploads
mkdir -p flask_session
chmod 777 flask_session

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Create __init__.py in utils if it doesn't exist
mkdir -p utils
touch utils/__init__.py
