"""
NER Service - Core module for Named Entity Recognition
This module provides the main NER functionality using spaCy
"""

import spacy
from typing import List, Dict, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NERModel:
    """Named Entity Recognition Model wrapper"""
    
    def __init__(self, model_name: str = "en_core_web_sm", custom_model_path: Optional[str] = None):
        """
        Initialize NER model
        
        Args:
            model_name: Name of the spaCy model to load
            custom_model_path: Path to custom trained model (optional)
        """
        self.model_name = model_name
        self.custom_model_path = custom_model_path
        self.nlp = None
        self._load_model()
    
    def _load_model(self):
        """Load the spaCy model"""
        try:
            if self.custom_model_path:
                logger.info(f"Loading custom model from {self.custom_model_path}")
                self.nlp = spacy.load(self.custom_model_path)
            else:
                logger.info(f"Loading pretrained model: {self.model_name}")
                self.nlp = spacy.load(self.model_name)
        except OSError:
            logger.warning(f"Model {self.model_name} not found. Attempting to download...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", self.model_name])
            self.nlp = spacy.load(self.model_name)
    
    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from text
        
        Args:
            text: Input text to process
            
        Returns:
            List of dictionaries containing entity information
        """
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        
        return entities
    
    def extract_entities_with_context(self, text: str) -> Dict:
        """
        Extract entities with additional context
        
        Args:
            text: Input text to process
            
        Returns:
            Dictionary with entities and metadata
        """
        doc = self.nlp(text)
        
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char,
                "label_description": spacy.explain(ent.label_)
            })
        
        return {
            "text": text,
            "entities": entities,
            "entity_count": len(entities),
            "entity_types": list(set([ent["label"] for ent in entities]))
        }
    
    def batch_extract_entities(self, texts: List[str]) -> List[Dict]:
        """
        Process multiple texts in batch
        
        Args:
            texts: List of texts to process
            
        Returns:
            List of results for each text
        """
        results = []
        for doc in self.nlp.pipe(texts):
            entities = []
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
            results.append({
                "text": doc.text,
                "entities": entities
            })
        
        return results


def main():
    """Example usage of NER model"""
    # Initialize model
    ner = NERModel()
    
    # Example text
    sample_text = """
    Apple Inc. was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in April 1976.
    The company is headquartered in Cupertino, California and has operations in over 
    50 countries worldwide. Tim Cook became CEO in August 2011.
    """
    
    # Extract entities
    print("=" * 80)
    print("Named Entity Recognition Example")
    print("=" * 80)
    print(f"\nInput Text:\n{sample_text}\n")
    
    result = ner.extract_entities_with_context(sample_text)
    
    print(f"Found {result['entity_count']} entities:")
    print(f"Entity Types: {', '.join(result['entity_types'])}\n")
    
    for entity in result['entities']:
        print(f"  - {entity['text']:30} | {entity['label']:10} | {entity['label_description']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
