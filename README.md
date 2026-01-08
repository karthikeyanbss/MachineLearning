# Enterprise Named Entity Recognition (NER) Service

A complete, production-ready Named Entity Recognition service built with Python, spaCy, FastAPI, and designed for enterprise deployment on Azure.

## 🚀 Features

- **State-of-the-art NER** using spaCy's pre-trained models
- **Custom model training** capabilities for domain-specific entities
- **RESTful API** built with FastAPI
- **Batch processing** for high-throughput scenarios
- **Docker containerization** for easy deployment
- **Azure deployment** templates and CI/CD workflows
- **Comprehensive testing** suite
- **Production-ready** with logging, error handling, and health checks

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Training Custom Models](#training-custom-models)
- [Deployment](#deployment)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)

## 🎯 Quick Start

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Azure CLI (optional, for Azure deployment)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/karthikeyanbss/MachineLearning.git
   cd MachineLearning
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

  **Note:** If you encounter build errors installing `spacy` or `numpy` on Windows,
  use Python 3.10 (recommended) or activate the project's prebuilt virtualenv.
  To activate the venv on Windows:
  ```powershell
  venv\Scripts\activate
  ```
  Or create a venv with Python 3.10 explicitly:
  ```powershell
  py -3.10 -m venv venv
  ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Run the service**
   ```bash
   # Using the provided script
   bash scripts/run_service.sh
   
   # Or manually
   uvicorn src.ner_service.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Docker Deployment

1. **Build and run with Docker**
   ```bash
   bash scripts/docker_run.sh
   ```

2. **Or use Docker Compose**
   ```bash
   docker-compose up -d
   ```

## 🏗️ Architecture

```
MachineLearning/
├── src/
│   ├── ner_service/          # Main API service
│   │   ├── main.py           # FastAPI application
│   │   ├── models.py         # Pydantic models
│   │   └── ner_model.py      # Core NER functionality
│   └── training/             # Model training
│       └── train_ner.py      # Training scripts
├── config/                   # Configuration files
├── data/                     # Data storage
│   └── samples/             # Sample data
├── deployment/              # Deployment configurations
│   └── azure/              # Azure-specific configs
├── examples/               # Usage examples
├── scripts/               # Utility scripts
├── tests/                # Test suite
├── Dockerfile            # Docker configuration
├── docker-compose.yml   # Docker Compose setup
└── requirements.txt     # Python dependencies
```

## 📚 API Documentation

### Endpoints

#### Health Check
```http
GET /health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "en_core_web_sm"
}
```

#### Extract Entities
```http
POST /extract
```

Request:
```json
{
  "text": "Apple Inc. was founded by Steve Jobs in Cupertino, California.",
  "include_context": false
}
```

Response:
```json
{
  "entities": [
    {
      "text": "Apple Inc.",
      "label": "ORG",
      "start": 0,
      "end": 10,
      "label_description": "Companies, agencies, institutions, etc."
    },
    {
      "text": "Steve Jobs",
      "label": "PERSON",
      "start": 26,
      "end": 36
    },
    {
      "text": "Cupertino",
      "label": "GPE",
      "start": 40,
      "end": 49
    },
    {
      "text": "California",
      "label": "GPE",
      "start": 51,
      "end": 61
    }
  ],
  "entity_count": 4
}
```

#### Batch Processing
```http
POST /extract/batch
```

Request:
```json
{
  "texts": [
    "Microsoft was founded by Bill Gates.",
    "Amazon is based in Seattle."
  ]
}
```

### Entity Types

The default model recognizes these entity types:

- **PERSON**: People, including fictional
- **ORG**: Companies, agencies, institutions
- **GPE**: Countries, cities, states
- **DATE**: Absolute or relative dates or periods
- **MONEY**: Monetary values
- **PRODUCT**: Objects, vehicles, foods, etc.
- **EVENT**: Named hurricanes, battles, wars, sports events
- **LOC**: Non-GPE locations, mountain ranges, bodies of water

## 🎓 Training Custom Models

### Using the Training Script

```python
from src.training.train_ner import NERTrainer

# Define your training data
TRAIN_DATA = [
    ("Text with entities", {"entities": [(start, end, "LABEL")]}),
    # More examples...
]

# Initialize trainer
trainer = NERTrainer(base_model="en_core_web_sm")

# Train model
trainer.train(
    train_data=TRAIN_DATA,
    output_dir="./custom_ner_model",
    n_iter=30,
    dropout=0.2
)
```

### Running the Example

```bash
python examples/train_custom_model.py
```

### Using Custom Models

1. Train and save your model
2. Update the configuration in `config/.env`:
   ```
   CUSTOM_MODEL_PATH=/path/to/custom_ner_model
   ```
3. Restart the service

## 🚢 Deployment

### Azure App Service

1. **Create Azure resources**
   ```bash
   az group create --name ner-service-rg --location eastus
   az appservice plan create --name ner-service-plan --resource-group ner-service-rg --sku B1 --is-linux
   ```

2. **Create Web App**
   ```bash
   az webapp create --resource-group ner-service-rg --plan ner-service-plan --name ner-service --deployment-container-image-name ner-service:latest
   ```

3. **Configure and deploy**
   - Use the provided GitHub Actions workflow (`.github/workflows/azure-deploy.yml`)
   - Set up secrets in your GitHub repository:
     - `AZURE_CREDENTIALS`
     - `REGISTRY_USERNAME`
     - `REGISTRY_PASSWORD`

### Azure Container Apps

1. **Deploy using the provided configuration**
   ```bash
   kubectl apply -f deployment/azure/container-apps-deployment.yml
   ```

2. **Update the configuration**
   - Replace `<YOUR_ACR_NAME>` with your Azure Container Registry name
   - Adjust resource limits as needed

### CI/CD Pipeline

The project includes a GitHub Actions workflow that:
- Runs tests on every push
- Builds Docker images
- Deploys to Azure on main branch updates

See `.github/workflows/azure-deploy.yml` for details.

## 💻 Development

### Project Structure

- **src/ner_service/**: Main API service code
  - `main.py`: FastAPI application and endpoints
  - `models.py`: Request/response models
  - `ner_model.py`: Core NER functionality

- **src/training/**: Model training utilities
  - `train_ner.py`: Training scripts and utilities

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### API Examples

See `examples/api_usage.py` for comprehensive usage examples:

```bash
python examples/api_usage.py
```

## 🧪 Testing

The project includes comprehensive tests:

- **Unit tests**: Test individual components
- **Integration tests**: Test API endpoints
- **Model tests**: Validate NER functionality

Run tests:
```bash
pytest tests/ -v
```

## 📦 Dependencies

Key dependencies:
- **spaCy**: 3.7.2 - NLP library
- **FastAPI**: 0.109.0 - Web framework
- **Uvicorn**: 0.27.0 - ASGI server
- **Pydantic**: 2.5.3 - Data validation
- **Docker**: For containerization

See `requirements.txt` for complete list.

## 🔒 Security

- Input validation using Pydantic models
- Error handling and logging
- Health check endpoints
- CORS configuration
- No hardcoded secrets

## 📈 Performance

- Batch processing for high throughput
- Async API endpoints
- Model caching
- Docker optimization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 License

See LICENSE file for details.

## 🆘 Support

For issues and questions:
- Open an issue on GitHub
- Check the API documentation at `/docs`
- Review examples in the `examples/` directory

## 🔄 Version History

- **1.0.0**: Initial release
  - Core NER functionality
  - FastAPI REST API
  - Docker support
  - Azure deployment templates
  - Comprehensive documentation

## 🎯 Roadmap

- [ ] Support for multiple languages
- [ ] Custom entity type configuration
- [ ] Model versioning and A/B testing
- [ ] Prometheus metrics
- [ ] GPU acceleration
- [ ] Streaming API
- [ ] WebSocket support

## 📊 Example Use Cases

1. **Document Processing**: Extract entities from legal documents, contracts
2. **Customer Support**: Identify key information in support tickets
3. **Content Analysis**: Analyze news articles, social media posts
4. **Data Extraction**: Extract structured data from unstructured text
5. **Research**: Academic text analysis and information extraction

---

Built with ❤️ using Python, spaCy, and FastAPI
