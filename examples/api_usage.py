"""
Example script demonstrating NER API usage
"""

import requests
import json


def main():
    """Demonstrate NER API usage"""
    
    # Base URL (adjust for your deployment)
    BASE_URL = "http://localhost:8000"
    
    print("=" * 80)
    print("NER API Usage Examples")
    print("=" * 80)
    
    # 1. Health check
    print("\n1. Health Check")
    print("-" * 40)
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 2. Simple entity extraction
    print("\n2. Simple Entity Extraction")
    print("-" * 40)
    text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
    response = requests.post(
        f"{BASE_URL}/extract",
        json={"text": text, "include_context": False}
    )
    print(f"Input: {text}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 3. Entity extraction with context
    print("\n3. Entity Extraction with Context")
    print("-" * 40)
    text = "Google was founded by Larry Page and Sergey Brin at Stanford University."
    response = requests.post(
        f"{BASE_URL}/extract",
        json={"text": text, "include_context": True}
    )
    print(f"Input: {text}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 4. Batch processing
    print("\n4. Batch Processing")
    print("-" * 40)
    texts = [
        "Microsoft was founded by Bill Gates and Paul Allen.",
        "Amazon is headquartered in Seattle, Washington.",
        "Tesla is led by Elon Musk."
    ]
    response = requests.post(
        f"{BASE_URL}/extract/batch",
        json={"texts": texts}
    )
    print(f"Input: {len(texts)} texts")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
