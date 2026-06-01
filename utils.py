# utils.py
"""
Utility functions for the LLM Output Denoising System.
Contains helper functions for the application.
"""

import os
from dotenv import load_dotenv
from datetime import datetime
import json
import requests

# Load environment variables from .env file
load_dotenv()


def get_groq_api_key():
    """
    Retrieve the Groq API key from environment variables.
    
    Returns:
        str: The Groq API key
        
    Raises:
        ValueError: If API key is not found in environment variables
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found in environment variables. "
            "Please add it to your .env file."
        )
    return api_key


def get_available_models(api_key: str) -> list:
    """
    Fetch list of available models from Groq API.
    
    Args:
        api_key (str): Groq API key
        
    Returns:
        list: List of available model IDs
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            models = [model['id'] for model in data.get('data', [])]
            return sorted(models)
        else:
            return []
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def test_model(api_key: str, model_name: str, test_prompt: str = "Hi") -> bool:
    """
    Test if a model is available and working.
    
    Args:
        api_key (str): Groq API key
        model_name (str): Model name to test
        test_prompt (str): Test prompt
        
    Returns:
        bool: True if model works, False otherwise
    """
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model_name,
            "messages": [{"role": "user", "content": test_prompt}],
            "max_tokens": 10,
            "temperature": 0
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        return response.status_code == 200
    except Exception:
        return False


def get_model_name() -> str:
    """
    Get model name from .env, or auto-detect if not specified.
    Tries multiple fallback models if configured one fails.
    
    Returns:
        str: The model name to use for API calls
    """
    configured_model = os.getenv("MODEL_NAME", "").strip()
    
    if configured_model:
        return configured_model
    
    # Auto-detect available model
    api_key = get_groq_api_key()
    
    # List of models to try in order
    models_to_try = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "llama3-70b",
        "llama3-8b",
        "gemma-7b-it",
        "mixtral-8x7b-32768"
    ]
    
    # Test each model
    for model in models_to_try:
        if test_model(api_key, model):
            return model
    
    # If all fail, return first one and let error handling catch it
    return models_to_try[0]


def calculate_quality_score(original_text: str, improved_text: str) -> dict:
    """
    Calculate comprehensive quality improvement metrics.
    
    Args:
        original_text (str): The original text
        improved_text (str): The improved text
        
    Returns:
        dict: Dictionary containing multiple quality metrics
    """
    # Count words and characters
    original_words = len(original_text.split())
    improved_words = len(improved_text.split())
    
    original_chars = len(original_text)
    improved_chars = len(improved_text)
    
    # Calculate compression ratio (less is better for redundancy removal)
    if original_chars > 0:
        compression_ratio = improved_chars / original_chars
        char_reduction = ((original_chars - improved_chars) / original_chars * 100)
    else:
        compression_ratio = 1.0
        char_reduction = 0
    
    # Calculate word reduction
    if original_words > 0:
        word_reduction = ((original_words - improved_words) / original_words * 100)
    else:
        word_reduction = 0
    
    # Base score: aim for 20-30% reduction without losing content
    ideal_ratio = 0.75  # 25% reduction is ideal
    
    # Calculate how close we are to ideal
    compression_score = 100 - (abs(compression_ratio - ideal_ratio) * 100)
    compression_score = max(0, min(100, compression_score))
    
    # Bonus for clarity (longer improvements on short originals = good)
    clarity_bonus = 0
    if original_words < 50 and improved_words > original_words:
        clarity_bonus = 10
    
    # Final quality score
    final_score = (compression_score * 0.7) + clarity_bonus
    final_score = max(0, min(100, final_score))
    
    return {
        "quality_score": round(final_score, 1),
        "word_reduction_percent": round(word_reduction, 1),
        "character_reduction_percent": round(char_reduction, 1),
        "original_word_count": original_words,
        "improved_word_count": improved_words,
        "original_char_count": original_chars,
        "improved_char_count": improved_chars,
        "compression_ratio": round(compression_ratio, 2)
    }


def validate_input(user_input: str) -> tuple[bool, str]:
    """
    Validate user input.
    
    Args:
        user_input (str): The user's input question
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not user_input or not user_input.strip():
        return False, "Please enter a question."
    
    if len(user_input.strip()) < 3:
        return False, "Question must be at least 3 characters long."
    
    if len(user_input) > 2000:
        return False, "Question must be less than 2000 characters."
    
    return True, ""
