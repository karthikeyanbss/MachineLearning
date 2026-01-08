#!/bin/bash
# Script to run the NER service locally

echo "Starting NER Service..."

# Check if virtual environment exists; create with `python` for compatibility
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment (POSIX first, then try Windows-style activate for Git Bash)
if [ -f "venv/bin/activate" ]; then
    # POSIX
    # shellcheck disable=SC1091
    source venv/bin/activate
elif [ -f "venv/Scripts/activate" ]; then
    # Git Bash / MSYS may use this path
    # shellcheck disable=SC1091
    source venv/Scripts/activate
else
    echo "WARNING: Could not find venv activation script. Ensure venv is created and activate it manually."
fi

echo "Installing dependencies..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

echo "Ensuring spaCy English model is installed..."
if ! python -c "import spacy, pkgutil; import sys; sys.exit(0 if pkgutil.find_loader('en_core_web_sm') or pkgutil.find_loader('en_core_web_sm') else 1)" 2>/dev/null; then
    python -m spacy download en_core_web_sm || python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl
fi

echo "Starting API server on http://localhost:8000"
python -m uvicorn src.ner_service.main:app --host 0.0.0.0 --port 8000 --reload
