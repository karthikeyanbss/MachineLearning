"""
Training module for custom NER models
This module provides functionality to train custom NER models using spaCy
"""

import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
import random
from pathlib import Path
from typing import List, Tuple, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NERTrainer:
    """Custom NER Model Trainer"""
    
    def __init__(self, base_model: str = "en_core_web_sm", new_labels: List[str] = None):
        """
        Initialize NER Trainer
        
        Args:
            base_model: Base spaCy model to start from
            new_labels: List of new entity labels to add
        """
        self.base_model = base_model
        self.new_labels = new_labels or []
        self.nlp = None
        self._setup_model()
    
    def _setup_model(self):
        """Setup or create the model for training"""
        try:
            self.nlp = spacy.load(self.base_model)
            logger.info(f"Loaded base model: {self.base_model}")
        except OSError:
            logger.info(f"Creating blank model")
            self.nlp = spacy.blank("en")
        
        # Get or create NER component
        if "ner" not in self.nlp.pipe_names:
            ner = self.nlp.add_pipe("ner", last=True)
        else:
            ner = self.nlp.get_pipe("ner")
        
        # Add new labels
        for label in self.new_labels:
            ner.add_label(label)
    
    def train(
        self,
        train_data: List[Tuple[str, Dict]],
        output_dir: str,
        n_iter: int = 30,
        dropout: float = 0.2
    ):
        """
        Train the NER model
        
        Args:
            train_data: List of (text, annotations) tuples
            output_dir: Directory to save the trained model
            n_iter: Number of training iterations
            dropout: Dropout rate for training
        """
        logger.info(f"Training NER model for {n_iter} iterations...")
        
        # Get NER component
        ner = self.nlp.get_pipe("ner")
        
        # Disable other pipelines during training
        other_pipes = [pipe for pipe in self.nlp.pipe_names if pipe != "ner"]
        
        with self.nlp.disable_pipes(*other_pipes):
            optimizer = self.nlp.initialize()
            
            for iteration in range(n_iter):
                random.shuffle(train_data)
                losses = {}
                
                # Create batches
                batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
                
                for batch in batches:
                    examples = []
                    for text, annotations in batch:
                        doc = self.nlp.make_doc(text)
                        example = Example.from_dict(doc, annotations)
                        examples.append(example)
                    
                    self.nlp.update(examples, drop=dropout, losses=losses)
                
                logger.info(f"Iteration {iteration + 1}/{n_iter} - Loss: {losses.get('ner', 0):.4f}")
        
        # Save model
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        self.nlp.to_disk(output_path)
        logger.info(f"Model saved to {output_path}")
    
    def evaluate(self, test_data: List[Tuple[str, Dict]]) -> Dict:
        """
        Evaluate the model on test data
        
        Args:
            test_data: List of (text, annotations) tuples
            
        Returns:
            Dictionary with evaluation metrics
        """
        examples = []
        for text, annotations in test_data:
            doc = self.nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            examples.append(example)
        
        scores = self.nlp.evaluate(examples)
        
        logger.info("Evaluation Results:")
        logger.info(f"  Precision: {scores.get('ents_p', 0):.4f}")
        logger.info(f"  Recall: {scores.get('ents_r', 0):.4f}")
        logger.info(f"  F-Score: {scores.get('ents_f', 0):.4f}")
        
        return scores


def create_sample_training_data() -> List[Tuple[str, Dict]]:
    """
    Create sample training data for demonstration
    
    Returns:
        List of training examples
    """
    TRAIN_DATA = [
        ("Google was founded in 1998 by Larry Page and Sergey Brin.", {
            "entities": [(0, 6, "ORG"), (26, 36, "PERSON"), (41, 52, "PERSON")]
        }),
        ("Microsoft was established in Albuquerque, New Mexico.", {
            "entities": [(0, 9, "ORG"), (29, 40, "GPE"), (42, 52, "GPE")]
        }),
        ("Elon Musk is the CEO of Tesla and SpaceX.", {
            "entities": [(0, 9, "PERSON"), (24, 29, "ORG"), (34, 40, "ORG")]
        }),
        ("Amazon has its headquarters in Seattle, Washington.", {
            "entities": [(0, 6, "ORG"), (31, 38, "GPE"), (40, 50, "GPE")]
        }),
        ("Mark Zuckerberg founded Facebook in 2004.", {
            "entities": [(0, 15, "PERSON"), (24, 32, "ORG")]
        }),
    ]
    
    return TRAIN_DATA


def main():
    """Example training workflow"""
    logger.info("Starting NER Model Training Example")
    
    # Create sample training data
    train_data = create_sample_training_data()
    
    # Initialize trainer
    trainer = NERTrainer(base_model="en_core_web_sm")
    
    # Train model
    output_dir = "./custom_ner_model"
    trainer.train(
        train_data=train_data,
        output_dir=output_dir,
        n_iter=20,
        dropout=0.2
    )
    
    logger.info("Training completed successfully!")
    
    # Test the trained model
    logger.info("\nTesting trained model:")
    test_text = "Jeff Bezos founded Amazon in Seattle."
    doc = trainer.nlp(test_text)
    
    print(f"\nTest text: {test_text}")
    print("Extracted entities:")
    for ent in doc.ents:
        print(f"  - {ent.text:20} | {ent.label_}")


if __name__ == "__main__":
    main()
