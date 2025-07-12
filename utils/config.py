import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "Clara - Casual Conversational") 

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in .env file")

RECORDING_SAMPLE_RATE = 44100
RECORDING_CHANNELS = 1
RECORDING_DURATION_SECONDS = 12 
TEMP_AUDIO_FILENAME = "data/recordings/temp_user_response.wav"