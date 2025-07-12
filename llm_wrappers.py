
import os
import sys
import json
from typing import Any, List, Dict, Union
from crewai import BaseLLM
import google.generativeai as genai  # Compatibily issues

class GeminiLLM(BaseLLM):
    def __init__(self, model: str = "gemini-1.5-flash"):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("[FATAL ERROR] GOOGLE_API_KEY not found.")
            sys.exit(1)

        super().__init__(temperature=0.1, model=model)
        genai.configure(api_key=api_key)
        self.model_instance = genai.GenerativeModel(model)

    def call(self, prompt: Union[str, List[Dict[str, str]]], **kwargs: Any) -> str:
        if isinstance(prompt, list):
            prompt_text = prompt[-1]['content']
        else:
            prompt_text = prompt
        try:
            # Attempt the API call
            response = self.model_instance.generate_content(prompt_text)
            return response.text
        except Exception as e:
            # Rate limit error handling
            print(f"[ERROR] GeminiLLM API call failed: {e}")
            
            # Create a JSON object that conforms to the expected Pydantic schema
            error_response = {
                "review_summary": f"A critical error occurred with the LLM API: {e}",
                "extracted_entities": {
                    "API_Error": "The AI model could not be reached. Please check your API plan and billing details or try again later."
                }
            }
            return json.dumps(error_response) # Return as a valid JSON string

    def get_context_window_size(self): return 32768
    def supports_function_calling(self): return False