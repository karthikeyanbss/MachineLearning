"""
FastAPI Application for Named Entity Recognition Service
Enterprise-grade REST API for NER with proper error handling and documentation
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from ner_service.models import (
    NERRequest,
    NERResponse,
    NERContextResponse,
    BatchNERRequest,
    BatchNERResponse,
    HealthResponse,
    ErrorResponse,
    Entity
)
from ner_service.ner_model import NERModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global NER model instance
ner_model: NERModel = None


def _ensure_ner_model() -> NERModel:
    """Ensure the global NER model is initialized (lazy init).

    Returns the model instance or None if initialization failed.
    """
    global ner_model
    if ner_model is None:
        try:
            logger.info("Lazy-loading NER model...")
            ner_model = NERModel(model_name="en_core_web_sm")
            logger.info("NER model lazy-loaded successfully")
        except Exception as e:
            logger.error(f"Failed to lazy-load NER model: {e}")
            return None
    return ner_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    global ner_model
    try:
        logger.info("Loading NER model...")
        ner_model = NERModel(model_name="en_core_web_sm")
        logger.info("NER model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load NER model: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down NER service...")


# Initialize FastAPI app
app = FastAPI(
    title="Named Entity Recognition API",
    description="Enterprise-grade NER service using spaCy",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "service": "Named Entity Recognition API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    }


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check endpoint"
)
async def health_check():
    """
    Check the health status of the NER service
    
    Returns:
        Health status including model information
    """
    try:
        model = ner_model or None
        # Don't raise here; report current status. Try to lazy-load if not present.
        if model is None:
            model = _ensure_ner_model()
        return HealthResponse(
            status="healthy" if model else "degraded",
            model_loaded=model is not None,
            model_name=model.model_name if model else "none"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service unhealthy"
        )


from typing import Union


@app.post(
    "/extract",
    response_model=Union[NERResponse, NERContextResponse],
    tags=["NER"],
    summary="Extract named entities from text"
)
async def extract_entities(request: NERRequest):
    """
    Extract named entities from the provided text
    
    Args:
        request: NER request with text and options
        
    Returns:
        Extracted entities with metadata
    """
    try:
        model = ner_model or _ensure_ner_model()
        if not model:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="NER model not loaded"
            )
        
        if request.include_context:
            result = ner_model.extract_entities_with_context(request.text)
            # Convert to Entity objects
            entities = [Entity(**ent) for ent in result["entities"]]
            return NERContextResponse(
                text=result["text"],
                entities=entities,
                entity_count=result["entity_count"],
                entity_types=result["entity_types"]
            )
        else:
            entities_raw = ner_model.extract_entities(request.text)
            entities = [Entity(**ent) for ent in entities_raw]
            return NERResponse(
                entities=entities,
                entity_count=len(entities)
            )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting entities: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing request: {str(e)}"
        )


@app.post(
    "/extract/batch",
    response_model=BatchNERResponse,
    tags=["NER"],
    summary="Extract entities from multiple texts"
)
async def extract_entities_batch(request: BatchNERRequest):
    """
    Extract named entities from multiple texts in batch
    
    Args:
        request: Batch request with list of texts
        
    Returns:
        Results for each text
    """
    try:
        model = ner_model or _ensure_ner_model()
        if not model:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="NER model not loaded"
            )

        results_raw = model.batch_extract_entities(request.texts)
        
        results = []
        for result in results_raw:
            entities = [Entity(**ent) for ent in result["entities"]]
            results.append(NERResponse(
                entities=entities,
                entity_count=len(entities)
            ))
        
        return BatchNERResponse(
            results=results,
            total_texts=len(results)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in batch extraction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing batch request: {str(e)}"
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
