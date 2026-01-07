"""
Test suite for NER API
"""

import pytest
from httpx import AsyncClient, ASGITransport
from src.ner_service.main import app


@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "Named Entity Recognition API"


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
        assert "model_loaded" in data


@pytest.mark.asyncio
async def test_extract_entities():
    """Test entity extraction"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/extract",
            json={
                "text": "Apple Inc. was founded by Steve Jobs in Cupertino, California.",
                "include_context": False
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "entities" in data
        assert "entity_count" in data
        assert data["entity_count"] > 0


@pytest.mark.asyncio
async def test_extract_entities_with_context():
    """Test entity extraction with context"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/extract",
            json={
                "text": "Google is headquartered in Mountain View, California.",
                "include_context": True
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "entities" in data
        assert "entity_types" in data
        assert "text" in data


@pytest.mark.asyncio
async def test_batch_extraction():
    """Test batch entity extraction"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/extract/batch",
            json={
                "texts": [
                    "Microsoft was founded by Bill Gates.",
                    "Amazon is led by Andy Jassy."
                ]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "results" in data
        assert "total_texts" in data
        assert data["total_texts"] == 2


@pytest.mark.asyncio
async def test_empty_text():
    """Test handling of empty text"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/extract",
            json={"text": ""}
        )
        # Should return 422 for validation error
        assert response.status_code == 422
