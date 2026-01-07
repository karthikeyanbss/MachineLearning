"""
Example script for training a custom NER model
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.training.train_ner import NERTrainer, create_sample_training_data


def main():
    """Train a custom NER model"""
    
    print("=" * 80)
    print("Custom NER Model Training Example")
    print("=" * 80)
    
    # Create training data
    print("\n1. Preparing training data...")
    train_data = create_sample_training_data()
    print(f"   Training samples: {len(train_data)}")
    
    # Initialize trainer
    print("\n2. Initializing trainer...")
    trainer = NERTrainer(base_model="en_core_web_sm")
    
    # Train the model
    print("\n3. Training model...")
    output_dir = "./custom_ner_model"
    trainer.train(
        train_data=train_data,
        output_dir=output_dir,
        n_iter=20,
        dropout=0.2
    )
    
    # Test the trained model
    print("\n4. Testing trained model...")
    test_texts = [
        "Jeff Bezos founded Amazon in Seattle.",
        "Mark Zuckerberg is the CEO of Meta Platforms.",
        "Satya Nadella leads Microsoft from Redmond, Washington."
    ]
    
    for text in test_texts:
        doc = trainer.nlp(text)
        print(f"\nText: {text}")
        print("Entities:")
        for ent in doc.ents:
            print(f"  - {ent.text:25} | {ent.label_:10}")
    
    print("\n" + "=" * 80)
    print(f"Model saved to: {output_dir}")
    print("To use this model in the API, set CUSTOM_MODEL_PATH in config")
    print("=" * 80)


if __name__ == "__main__":
    main()
