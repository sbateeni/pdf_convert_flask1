#!/usr/bin/env bash
# exit on error
set -o errexit

# Install system dependencies
apt-get update
apt-get install -y poppler-utils tesseract-ocr tesseract-ocr-ara tesseract-ocr-eng

# Install Python dependencies
pip install -r requirements.txt
