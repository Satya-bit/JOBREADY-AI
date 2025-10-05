# Used OPENAI API key for text generation as my LLM service. Note we can change 
# and use any other model from OpenAI. We can also use Langchain here to generate the response.

import openai
from utils.config import OPENAI_API_KEY
import os
from dotenv import load_dotenv
from openai import OpenAI

# from openai import OpenAI


# openai.api_key = OPENAI_API_KEY
load_dotenv()

openai.api_key = os.getenv("GEMINI_API_KEY")
openai.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"



# Gemini client configuration
gemini_api_key = os.getenv("GEMINI_API_KEY")
client = OpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def generate_completion(prompt: str, model: str = "gemini-2.0-flash", max_tokens: int = 1500, temperature: float = 0.7) -> str:
    """Generates text completion using Gemini API (OpenAI-compatible endpoint)."""
    try:
        # Ensure prompt is a valid non-empty string
        if not prompt or not isinstance(prompt, str) or prompt.strip() == "":
            raise ValueError("Prompt must be a non-empty string.")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Extract content safely
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
        else:
            print("Warning: No content in Gemini response.")
            return "Error: No content in response."

    except ValueError as e:
        print(f"Validation Error: {e}")
        return f"Error: Invalid prompt - {e}"
    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return f"Error: Could not generate completion - {e}"













###Donot Touch

# def generate_completion(prompt: str, model: str = "gpt-4.1-mini", max_tokens: int = 500, temperature: float = 0.9) -> str:
#     """Generates text completion using OpenAI API."""
#     try:
#         response = openai.chat.completions.create(
#             model=model,
#             messages=[
#                 {"role": "system", "content": "You are a helpful AI assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             max_tokens=max_tokens,
#             temperature=temperature,
#             n=1,
#             stop=None,
#         )
#         # Check if response.choices exists and has items
#         if response.choices and len(response.choices) > 0:
#             # Check if message exists and has content
#             if response.choices[0].message and response.choices[0].message.content:
#                  return response.choices[0].message.content.strip()
#             else:
#                 print("Warning: LLM response message or content is empty.")
#                 return "Error: No content in response."
#         else:
#             print("Warning: LLM response choices list is empty.")
#             return "Error: No choices in response."
            
#     except openai.AuthenticationError as e:
#         print(f"OpenAI Authentication Error: {e}")
#         print("Please check your OPENAI_API_KEY in the .env file.")
#         return "Error: OpenAI Authentication Failed."
#     except openai.RateLimitError as e:
#         print(f"OpenAI Rate Limit Error: {e}")
#         return "Error: OpenAI Rate Limit Exceeded."
#     except Exception as e:
#         print(f"Error during OpenAI API call: {e}")
#         return f"Error: Could not generate completion - {e}"









