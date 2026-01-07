# MachineLearning
Complete, enterprise‑style Named Entity Recognition (NER) project using Python, NLP techniques

## MCP Agent Installation

This project includes a Model Context Protocol (MCP) server that provides AI-accessible tools for machine learning operations.

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the MCP server:
```bash
python mcp_server.py
```

### Using the MCP Server

The MCP server can be integrated with AI assistants that support the Model Context Protocol. Configure your AI assistant to use this server by pointing it to the `mcp_config.json` file or by adding the following to your MCP settings:

```json
{
  "mcpServers": {
    "ml-operations": {
      "command": "python",
      "args": ["mcp_server.py"],
      "description": "Machine Learning operations server for NER project"
    }
  }
}
```

### Available Tools

The MCP server provides the following tools:

- **get_ml_info**: Get information about the Machine Learning project
- **check_dependencies**: Check if required ML dependencies are installed

### Testing the Installation

To verify the MCP server is working correctly, you can run:

```bash
python -c "import mcp; print('MCP SDK installed successfully')"
```
