"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class Entity(BaseModel):
    """Single entity model"""
    text: str = Field(..., description="The text of the entity")
    label: str = Field(..., description="The entity type/label")
    start: int = Field(..., description="Start character position")
    end: int = Field(..., description="End character position")
    label_description: Optional[str] = Field(None, description="Human-readable description of the label")


class NERRequest(BaseModel):
    """Request model for NER extraction"""
    text: str = Field(..., description="Text to extract entities from", min_length=1)
    include_context: bool = Field(default=False, description="Include additional context in response")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "text": "Apple Inc. was founded by Steve Jobs in Cupertino, California.",
                "include_context": True
            }
        }
    )


class NERResponse(BaseModel):
    """Response model for NER extraction"""
    entities: List[Entity] = Field(..., description="List of extracted entities")
    entity_count: int = Field(..., description="Total number of entities found")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
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
        }
    )


class NERContextResponse(BaseModel):
    """Extended response model with context"""
    text: str = Field(..., description="Original input text")
    entities: List[Entity] = Field(..., description="List of extracted entities")
    entity_count: int = Field(..., description="Total number of entities found")
    entity_types: List[str] = Field(..., description="Unique entity types found")


class BatchNERRequest(BaseModel):
    """Request model for batch NER extraction"""
    texts: List[str] = Field(..., description="List of texts to process", min_length=1)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "texts": [
                    "Apple Inc. was founded by Steve Jobs.",
                    "Google is headquartered in Mountain View, California."
                ]
            }
        }
    )


class BatchNERResponse(BaseModel):
    """Response model for batch NER extraction"""
    results: List[NERResponse] = Field(..., description="Results for each input text")
    total_texts: int = Field(..., description="Total number of texts processed")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether the NER model is loaded")
    model_name: str = Field(..., description="Name of the loaded model")
    
    model_config = ConfigDict(protected_namespaces=())


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
