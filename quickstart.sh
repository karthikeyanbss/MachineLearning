#!/bin/bash
# Quick Start Script for NER Service
# This script sets up and runs the NER service locally

set -e

echo "=========================================="
echo "NER Service Quick Start"
echo "=========================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"

# Download spaCy model
echo ""
echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm > /dev/null 2>&1
echo "✓ spaCy model downloaded"

# Run a quick test
echo ""
echo "Testing NER functionality..."
python -c "
from src.ner_service.ner_model import NERModel
model = NERModel()
text = 'Apple Inc. was founded by Steve Jobs in Cupertino, California.'
entities = model.extract_entities(text)
print(f'✓ Found {len(entities)} entities in test text')
" 2>/dev/null

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "You can now:"
echo ""
echo "1. Run the API server:"
echo "   uvicorn src.ner_service.main:app --host 0.0.0.0 --port 8000"
echo ""
echo "2. Test the NER model:"
echo "   python src/ner_service/ner_model.py"
echo ""
echo "3. Train a custom model:"
echo "   python src/training/train_ner.py"
echo ""
echo "4. Try the API examples:"
echo "   # Start server first, then:"
echo "   python examples/api_usage.py"
echo ""
echo "5. View API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "=========================================="
