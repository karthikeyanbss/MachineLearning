"""
Configuration module for NER Service
"""

import os
from pathlib import Path
from typing import Optional


class Config:
    """Application configuration"""
    
    # Server settings
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # Model settings
    MODEL_NAME: str = os.getenv("MODEL_NAME", "en_core_web_sm")
    CUSTOM_MODEL_PATH: Optional[str] = os.getenv("CUSTOM_MODEL_PATH")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
    
    # API settings
    API_TITLE: str = os.getenv("API_TITLE", "Named Entity Recognition API")
    API_VERSION: str = os.getenv("API_VERSION", "1.0.0")
    
    # Project paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODELS_DIR: Path = BASE_DIR / "models"
    
    @classmethod
    def ensure_dirs(cls):
        """Ensure required directories exist"""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)


# Initialize configuration
config = Config()
