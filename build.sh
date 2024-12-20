#!/bin/bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update -y
apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng

# Create necessary directories
mkdir -p uploads
chmod 777 uploads

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt
