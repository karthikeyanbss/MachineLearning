"""
Tests for NER model functionality
"""

import pytest
from src.ner_service.ner_model import NERModel


def test_ner_model_initialization():
    """Test NER model can be initialized"""
    model = NERModel(model_name="en_core_web_sm")
    assert model.nlp is not None
    assert model.model_name == "en_core_web_sm"


def test_extract_entities():
    """Test basic entity extraction"""
    model = NERModel(model_name="en_core_web_sm")
    text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
    
    entities = model.extract_entities(text)
    
    assert isinstance(entities, list)
    assert len(entities) > 0
    
    # Check entity structure
    for entity in entities:
        assert "text" in entity
        assert "label" in entity
        assert "start" in entity
        assert "end" in entity


def test_extract_entities_with_context():
    """Test entity extraction with context"""
    model = NERModel(model_name="en_core_web_sm")
    text = "Google is headquartered in Mountain View, California."
    
    result = model.extract_entities_with_context(text)
    
    assert "text" in result
    assert "entities" in result
    assert "entity_count" in result
    assert "entity_types" in result
    assert result["text"] == text


def test_batch_extraction():
    """Test batch entity extraction"""
    model = NERModel(model_name="en_core_web_sm")
    texts = [
        "Microsoft was founded by Bill Gates.",
        "Amazon is based in Seattle."
    ]
    
    results = model.batch_extract_entities(texts)
    
    assert isinstance(results, list)
    assert len(results) == 2
    
    for result in results:
        assert "text" in result
        assert "entities" in result


def test_empty_text():
    """Test handling of empty text"""
    model = NERModel(model_name="en_core_web_sm")
    entities = model.extract_entities("")
    
    assert isinstance(entities, list)
    assert len(entities) == 0
