#!/bin/bash
# Script to run the NER service locally

echo "Starting NER Service..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download spaCy model if not present
python -m spacy download en_core_web_sm

# Run the service
echo "Starting API server on http://localhost:8000"
python -m uvicorn src.ner_service.main:app --host 0.0.0.0 --port 8000 --reload
