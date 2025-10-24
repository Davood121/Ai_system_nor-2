import requests
import pygame
import tempfile
import os
from io import BytesIO

class ElevenLabsVoice:
    def __init__(self, api_key=None):
        self.api_key = api_key or "sk_c1171d6e671e152ba77e3c776cdb0e5130908d961fd1a6e7"
        self.base_url = "https://api.elevenlabs.io/v1"
        pygame.mixer.init()
        
        # Popular voice IDs (you can get these from ElevenLabs dashboard)
        self.voices = {
            "rachel": "21m00Tcm4TlvDq8ikWAM",  # Female, American
            "drew": "29vD33N1CtxCmqQRPOHJ",   # Male, American  
            "clyde": "2EiwWnXFnvU5JabPnv8n",  # Male, American
            "dave": "CYw3kZ02Hs0563khs1Fj",   # Male, British
            "fin": "D38z5RcWu1voky8WS1ja",    # Male, Irish
            "sarah": "EXAVITQu4vr4xnSDxMaL",  # Female, American
            "antoni": "ErXwobaYiN019PkySvjV", # Male, American
            "thomas": "GBv7mTt0atIp3Br8iCZE", # Male, American
            "charlie": "IKne3meq5aSn9XLyUdCD", # Male, Australian
            "george": "JBFqnCBsd6RMkjVDRZzb", # Male, British
            "callum": "N2lVS1w4EtoT3dr4eOWO", # Male, American
            "liam": "TX3LPaxmHKxFdv7VOQHJ",   # Male, American
            "charlotte": "XB0fDUnXU5powFXDhCwa", # Female, American
            "alice": "Xb7hH8MSUJpSbSDYk0k2",   # Female, British
            "matilda": "XrExE9yKIg1WjnnlVkGX"  # Female, American
        }
        
        self.current_voice = "rachel"  # Default voice
        
    def set_api_key(self, api_key):
        """Set ElevenLabs API key"""
        self.api_key = api_key
        print(f"✅ ElevenLabs API key set")
        
    def list_voices(self):
        """List available voices"""
        print("\n🎤 Available ElevenLabs Voices:")
        for i, (name, voice_id) in enumerate(self.voices.items(), 1):
            current = " (current)" if name == self.current_voice else ""
            print(f"  {i}. {name.title()}{current}")
        return list(self.voices.keys())
        
    def set_voice(self, voice_name):
        """Set current voice"""
        if voice_name.lower() in self.voices:
            self.current_voice = voice_name.lower()
            print(f"🎤 Voice set to: {voice_name.title()}")
            return True
        else:
            print(f"❌ Voice '{voice_name}' not found")
            return False
            
    def generate_speech(self, text, voice_name=None):
        """Generate speech using ElevenLabs API"""
        try:
            if not self.api_key or self.api_key == "YOUR_ELEVENLABS_API_KEY":
                print("❌ Please set your ElevenLabs API key first")
                return None
                
            voice_id = self.voices.get(voice_name or self.current_voice)
            if not voice_id:
                print(f"❌ Voice not found: {voice_name}")
                return None
                
            url = f"{self.base_url}/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": self.api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"❌ ElevenLabs API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ ElevenLabs error: {e}")
            return None
            
    def speak(self, text, voice_name=None):
        """Speak text using ElevenLabs voice"""
        try:
            audio_data = self.generate_speech(text, voice_name)
            
            if audio_data:
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(audio_data)
                    tmp_filename = tmp_file.name
                
                # Play audio
                pygame.mixer.music.load(tmp_filename)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # Clean up
                try:
                    os.unlink(tmp_filename)
                except:
                    pass
                    
                return True
            else:
                print("❌ Failed to generate speech")
                return False
                
        except Exception as e:
            print(f"❌ Speech error: {e}")
            return False
            
    def test_voice(self, voice_name=None):
        """Test a specific voice"""
        test_text = f"Hello! This is {(voice_name or self.current_voice).title()} from ElevenLabs. How do I sound?"
        print(f"🎤 Testing {(voice_name or self.current_voice).title()}...")
        return self.speak(test_text, voice_name)
        
    def voice_demo(self):
        """Demo different voices"""
        demo_voices = ["rachel", "drew", "sarah", "thomas"]
        
        for voice in demo_voices:
            if voice in self.voices:
                print(f"\n🎤 Demo: {voice.title()}")
                self.speak(f"Hi, I'm {voice.title()}. Nice to meet you!", voice)
                
    def get_voice_info(self):
        """Get current voice information"""
        return {
            "current_voice": self.current_voice,
            "voice_id": self.voices.get(self.current_voice),
            "available_voices": list(self.voices.keys()),
            "api_configured": bool(self.api_key and len(self.api_key) > 20)
        }