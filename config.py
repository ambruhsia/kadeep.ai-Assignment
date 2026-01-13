"""
Configuration for InternHub AI Agent
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration
USE_MOCK_LLM = True  # Set to False to use real OpenAI API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_NAME = "gpt-4"  # or "gpt-3.5-turbo"

# Application settings
CONFIDENCE_THRESHOLD = 0.5  # Match confidence threshold (0-1)
MAX_SKILL_GAPS = 5  # Max skill gaps to highlight
