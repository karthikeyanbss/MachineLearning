# API Reference

Complete API documentation for the Named Entity Recognition service.

## Base URL

- Local: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication

Currently, the API is open. For production, consider implementing:
- API keys
- OAuth 2.0
- Azure AD authentication

## Endpoints

### Root

**GET /**

Returns basic API information.

**Response:**
```json
{
  "service": "Named Entity Recognition API",
  "version": "1.0.0",
  "status": "operational",
  "documentation": "/docs"
}
```

### Health Check

**GET /health**

Check service health status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_name": "en_core_web_sm"
}
```

**Status Codes:**
- `200`: Service is healthy
- `503`: Service unavailable

### Extract Entities

**POST /extract**

Extract named entities from text.

**Request Body:**
```json
{
  "text": "string",
  "include_context": boolean (optional, default: false)
}
```

**Parameters:**
- `text` (required): Text to analyze
- `include_context` (optional): Include additional context in response

**Response (include_context=false):**
```json
{
  "entities": [
    {
      "text": "Apple Inc.",
      "label": "ORG",
      "start": 0,
      "end": 10,
      "label_description": "Companies, agencies, institutions, etc."
    }
  ],
  "entity_count": 1
}
```

**Response (include_context=true):**
```json
{
  "text": "Apple Inc. was founded by Steve Jobs.",
  "entities": [...],
  "entity_count": 2,
  "entity_types": ["ORG", "PERSON"]
}
```

**Status Codes:**
- `200`: Success
- `422`: Validation error (empty text, etc.)
- `500`: Internal server error
- `503`: Service unavailable

**Example:**
```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple Inc. was founded by Steve Jobs.", "include_context": true}'
```

### Batch Extract Entities

**POST /extract/batch**

Extract entities from multiple texts.

**Request Body:**
```json
{
  "texts": ["string", "string", ...]
}
```

**Parameters:**
- `texts` (required): Array of texts to analyze (minimum 1)

**Response:**
```json
{
  "results": [
    {
      "entities": [...],
      "entity_count": 2
    },
    {
      "entities": [...],
      "entity_count": 3
    }
  ],
  "total_texts": 2
}
```

**Status Codes:**
- `200`: Success
- `422`: Validation error
- `500`: Internal server error
- `503`: Service unavailable

**Example:**
```bash
curl -X POST "http://localhost:8000/extract/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Apple Inc. is in California.", "Google is in Mountain View."]}'
```

## Data Models

### Entity

```typescript
{
  text: string;           // The entity text
  label: string;          // Entity type (ORG, PERSON, GPE, etc.)
  start: number;          // Start position in text
  end: number;            // End position in text
  label_description?: string;  // Human-readable label description
}
```

### Entity Labels

- **PERSON**: People, including fictional
- **NORP**: Nationalities, religious or political groups
- **FAC**: Buildings, airports, highways, bridges, etc.
- **ORG**: Companies, agencies, institutions, etc.
- **GPE**: Countries, cities, states
- **LOC**: Non-GPE locations, mountain ranges, bodies of water
- **PRODUCT**: Objects, vehicles, foods, etc.
- **EVENT**: Named hurricanes, battles, wars, sports events, etc.
- **WORK_OF_ART**: Titles of books, songs, etc.
- **LAW**: Named documents made into laws
- **LANGUAGE**: Any named language
- **DATE**: Absolute or relative dates or periods
- **TIME**: Times smaller than a day
- **PERCENT**: Percentage, including "%"
- **MONEY**: Monetary values, including unit
- **QUANTITY**: Measurements, as of weight or distance
- **ORDINAL**: "first", "second", etc.
- **CARDINAL**: Numerals that do not fall under another type

## Error Handling

All errors follow this format:

```json
{
  "error": "Error type",
  "detail": "Detailed error message"
}
```

### Common Errors

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**500 Internal Server Error:**
```json
{
  "error": "Internal server error",
  "detail": "Error message"
}
```

**503 Service Unavailable:**
```json
{
  "detail": "NER model not loaded"
}
```

## Rate Limiting

Currently no rate limiting is implemented. Consider adding:
- Per-IP rate limiting
- API key-based quotas
- Request throttling

## Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Code Examples

### Python

```python
import requests

# Simple extraction
response = requests.post(
    "http://localhost:8000/extract",
    json={"text": "Apple Inc. was founded by Steve Jobs."}
)
print(response.json())

# Batch extraction
response = requests.post(
    "http://localhost:8000/extract/batch",
    json={"texts": ["Text 1", "Text 2"]}
)
print(response.json())
```

### JavaScript

```javascript
// Using fetch
const response = await fetch('http://localhost:8000/extract', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    text: 'Apple Inc. was founded by Steve Jobs.'
  })
});
const data = await response.json();
console.log(data);
```

### cURL

```bash
# Extract entities
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here"}'

# Batch extraction
curl -X POST "http://localhost:8000/extract/batch" \
  -H "Content-Type: application/json" \
  -d '{"texts": ["Text 1", "Text 2"]}'
```

## Best Practices

1. **Text Length**: Keep text under 1MB for optimal performance
2. **Batch Size**: Process 10-100 texts per batch for best throughput
3. **Error Handling**: Always handle 422, 500, and 503 errors
4. **Timeouts**: Set reasonable timeouts (30-60 seconds)
5. **Retries**: Implement exponential backoff for failures

## Performance

- Single text: ~100-500ms
- Batch (10 texts): ~500ms-2s
- Throughput: ~100-500 requests/minute (single instance)

For higher throughput, scale horizontally with multiple instances.
