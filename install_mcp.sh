#!/bin/bash
# MCP Agent Installation Script

echo "Installing MCP Agent for Machine Learning project..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $PYTHON_VERSION"

# Install dependencies
echo "Installing dependencies from requirements.txt..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "✗ Failed to install dependencies"
    exit 1
fi

# Verify MCP installation
echo "Verifying MCP SDK installation..."
python3 -c "import mcp; print('✓ MCP SDK version:', mcp.__version__)" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✓ MCP Agent installation complete!"
    echo ""
    echo "To start the MCP server, run:"
    echo "  python3 mcp_server.py"
else
    echo "⚠ Warning: Could not verify MCP SDK installation"
    echo "Please check the installation manually"
fi
