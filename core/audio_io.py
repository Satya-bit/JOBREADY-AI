# This file is responsible for handling audio input/output operations,
# including text-to-speech, audio recording, and transcription.

# For audio generation this uses elevenlabs API and for transcription it uses SpeechRecognition 
# library with Google Web Speech API.

# Still the speech recognition(transcription) is not perfect using Google Web Speech API 
# and can fail in some cases. But can be improved by using better audio quality. 


import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from elevenlabs import generate,play, save, Voice, VoiceSettings
import numpy as np
import time
import os

from utils.config import (
    ELEVENLABS_API_KEY,
    ELEVENLABS_VOICE_ID,
    RECORDING_SAMPLE_RATE,
    RECORDING_CHANNELS,
    TEMP_AUDIO_FILENAME,
)



# Initialize recognizer
r = sr.Recognizer()

def speak_text(text: str): #text to speech
    """Generates speech from text using ElevenLabs API and plays it."""
   

    try:
        print("Generating audio...")
        voice_obj = Voice(
            voice_id=ELEVENLABS_VOICE_ID,
            settings=VoiceSettings(stability=0.6, similarity_boost=0.85, style=0.9, use_speaker_boost=True)
        )
        #STABILITY=Controls consistency in tone and delivery. Higher = more stable voice
        #SIMIILARITY_BOOST=Makes the voice more similar to the original (improves realism)
        #STYLE- 	Adds emotional variation. Low = neutral
        #USE_SPEAKER_BOOST=Enhances clarity and presence of the speaker

        audio = generate(
            text=text,
            api_key=ELEVENLABS_API_KEY,
            voice=voice_obj,
            model="eleven_multilingual_v2" 
        )
        print("Speaking...")
        play(audio)
        print("Finished speaking.")
    except Exception as e:
        print(f"Error during ElevenLabs TTS: {e}")
        print("Fallback: Printing text instead.")
        print(f"Interviewer: {text}")
        time.sleep(len(text.split()) / 3) # Approximate delay


# Record audio and saves it to a file
def record_audio(duration: int = 12, filename: str = TEMP_AUDIO_FILENAME) -> str | None:
    """Records audio from the microphone for a specified duration."""
    print(f"\n🎙️ Recording for {duration} seconds... Speak clearly into the microphone.")
    try:
        # Makes sure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        recording = sd.rec(int(duration * RECORDING_SAMPLE_RATE),
                           samplerate=RECORDING_SAMPLE_RATE,# tiny snap_shots of voice(sound_wave)
                           channels=RECORDING_CHANNELS, #USING MONO AUDIO
                           dtype='float32') # Use float32 which soundfile handles well and high quality audio
        sd.wait()  # Wait until recording is finished

        # Normalize if needed (optional, but can help)
        # recording /= np.max(np.abs(recording)) if np.max(np.abs(recording)) > 0 else 1

        # Saves as WAV file using soundfile
        sf.write(filename, recording, RECORDING_SAMPLE_RATE, subtype='PCM_16') #pcm_16 commonly uncompressed used format for audio files

        print(f"✅ Recording saved to {filename}")

        return filename
    except Exception as e:
        print(f"Error during audio recording: {e}")
        return None

#Speech to text transcription using Google Web Speech API
def transcribe_audio(filename: str = TEMP_AUDIO_FILENAME) -> str | None:
    """Transcribes audio file to text using SpeechRecognition (Google Web Speech API)."""
    print("Transcribing your response...")
    if not os.path.exists(filename):
        print(f"Error: Audio file not found for transcription: {filename}")
        return None

    with sr.AudioFile(filename) as source:
        try:
            audio_data = r.record(source) # Reads the entire audio file
            # Use Google Web Speech API for transcription
            text = r.recognize_google(audio_data)
            print(f"🎤 You said: {text}")
            return text
        except sr.UnknownValueError:
            print("❓ Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred during transcription: {e}")
            return None
     





