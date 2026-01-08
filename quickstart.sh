#!/bin/bash
# Quick Start Script for NER Service
# This script sets up and runs the NER service locally

set -e

echo "=========================================="
echo "NER Service Quick Start"
echo "=========================================="

# Locate a Python 3.10 interpreter (preferential)
echo "Locating Python 3.10 interpreter..."
PYTHON_EXE=""

if command -v py >/dev/null 2>&1; then
    if py -3.10 -c "import sys" >/dev/null 2>&1; then
        PYTHON_EXE="py -3.10"
    fi
fi

if [ -z "$PYTHON_EXE" ] && command -v python3.10 >/dev/null 2>&1; then
    PYTHON_EXE=python3.10
fi

if [ -z "$PYTHON_EXE" ] && command -v python3 >/dev/null 2>&1; then
    PYTHON_EXE=python3
fi

if [ -z "$PYTHON_EXE" ] && command -v python >/dev/null 2>&1; then
    PYTHON_EXE=python
fi

if [ -z "$PYTHON_EXE" ]; then
    echo "ERROR: No Python interpreter found. Install Python 3.10+ and retry."
    exit 1
fi

echo "Using interpreter: $PYTHON_EXE"

# Create virtual environment (explicit interpreter)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment with $PYTHON_EXE..."
    $PYTHON_EXE -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate venv (POSIX vs Windows support)
echo "Activating virtual environment..."
if [ -f "venv/bin/activate" ]; then
    # POSIX
    # shellcheck disable=SC1091
    source venv/bin/activate
else
    # Assume Windows (Git Bash / MSYS) or user will run PowerShell instructions
    source venv/Scripts/activate || true
fi

echo "Installing/upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

echo "Installing dependencies from requirements.txt..."
python -m pip install -r requirements.txt

echo "Installing spaCy English model (en_core_web_sm)..."
# Try the spacy CLI; if that fails, fall back to installing the wheel directly
if python -m spacy download en_core_web_sm; then
    echo "✓ spaCy model downloaded"
else
    echo "spacy download failed, installing wheel directly..."
    python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
    echo "✓ spaCy model wheel installed"
fi

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
