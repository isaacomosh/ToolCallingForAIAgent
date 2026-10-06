import os

from google import genai
from google.genai import types

from tools import AVAILABLE_TOOLS

#create Gemini Client
client=genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)