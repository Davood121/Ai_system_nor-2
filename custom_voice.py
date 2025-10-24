import os
import pygame
import pyttsx3
from gtts import gTTS
import tempfile
import random
from elevenlabs_voice import ElevenLabsVoice

class CustomVoiceSystem:
    def __init__(self):
        pygame.mixer.init()
        self.tts_engine = pyttsx3.init()
        self.voice_folder = r"C:\Users\shaik\Music\voice"
        self.custom_voices = {}
        self.current_mode = "custom"  # "tts", "custom", or "elevenlabs"
        self.elevenlabs = ElevenLabsVoice()
        self.load_custom_voices()
        
    def load_custom_voices(self):
        """Load custom voice files from the voice folder"""
        if os.path.exists(self.voice_folder):
            for file in os.listdir(self.voice_folder):
                if file.lower().endswith(('.mp3', '.wav', '.ogg')):
                    name = os.path.splitext(file)[0]
                    self.custom_voices[name] = os.path.join(self.voice_folder, file)
            print(f"🎤 Loaded {len(self.custom_voices)} custom voice files")
        else:
            print(f"❌ Voice folder not found: {self.voice_folder}")
    
    def list_custom_voices(self):
        """List available custom voices"""
        if self.custom_voices:
            print("\n🎵 Available Custom Voices:")
            for i, name in enumerate(self.custom_voices.keys(), 1):
                print(f"  {i}. {name}")
            return list(self.custom_voices.keys())
        else:
            print("❌ No custom voices found")
            return []
    
    def play_custom_voice(self, voice_name):
        """Play a specific custom voice file"""
        if voice_name in self.custom_voices:
            try:
                pygame.mixer.music.load(self.custom_voices[voice_name])
                pygame.mixer.music.play()
                print(f"🔊 Playing custom voice: {voice_name}")
                return True
            except Exception as e:
                print(f"❌ Error playing {voice_name}: {e}")
                return False
        else:
            print(f"❌ Voice '{voice_name}' not found")
            return False
    
    def play_random_custom_voice(self):
        """Play a random custom voice"""
        if self.custom_voices:
            voice_name = random.choice(list(self.custom_voices.keys()))
            return self.play_custom_voice(voice_name)
        return False
    
    def text_to_custom_voice(self, text, voice_style="default"):
        """Convert text to speech using custom voice style"""
        try:
            # Create temporary audio file
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tmp_filename = tmp_file.name
            tmp_file.close()
            
            # Generate TTS audio
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(tmp_filename)
            
            # Verify file exists
            if os.path.exists(tmp_filename):
                # Play the generated audio
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
                print("❌ Temp file not created")
                return False
                
        except Exception as e:
            print(f"❌ Custom TTS error: {e}")
            # Fallback to regular TTS
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
            return False
    
    def speak_with_custom_voice(self, text, use_custom=True):
        """Main speaking function using your voice files"""
        if self.current_mode == "custom":
            # For AI responses, use your voice files with gTTS
            self.text_to_custom_voice(text)
        elif self.current_mode == "elevenlabs":
            # Use ElevenLabs voice
            if not self.elevenlabs.speak(text):
                # Fallback to gTTS
                self.text_to_custom_voice(text)
        else:
            # Use regular TTS
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
    
    def set_voice_mode(self, mode):
        """Set voice mode: 'tts', 'custom', or 'elevenlabs'"""
        if mode in ['tts', 'custom', 'elevenlabs']:
            self.current_mode = mode
            print(f"🎤 Voice mode set to: {mode}")
            return True
        else:
            print("❌ Invalid mode. Use 'tts', 'custom', or 'elevenlabs'")
            return False
    
    def add_voice_effects(self, text):
        """Add voice effects based on text content"""
        # Detect emotion and adjust voice accordingly
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['excited', 'amazing', 'awesome', 'great']):
            # Excited voice - faster, higher pitch
            self.tts_engine.setProperty('rate', 200)
        elif any(word in text_lower for word in ['sad', 'sorry', 'unfortunately']):
            # Sad voice - slower, lower pitch
            self.tts_engine.setProperty('rate', 150)
        elif any(word in text_lower for word in ['important', 'warning', 'attention']):
            # Important voice - clear, moderate pace
            self.tts_engine.setProperty('rate', 175)
        else:
            # Normal voice
            self.tts_engine.setProperty('rate', 175)
        
        return text
    
    def create_voice_greeting(self):
        """Create a personalized voice greeting"""
        greetings = [
            "Hello! I'm your AI assistant with custom voice support!",
            "Welcome! Ready to experience enhanced voice interaction?",
            "Hi there! Your AI is now powered with custom voice capabilities!",
            "Greetings! Let's explore what I can do with my new voice!"
        ]
        
        greeting = random.choice(greetings)
        self.speak_with_custom_voice(greeting)
        return greeting
    
    def voice_test(self):
        """Test all voice capabilities"""
        print("\n🎤 Voice System Test:")
        
        # Test regular TTS
        print("1. Testing regular TTS...")
        self.set_voice_mode("tts")
        self.speak_with_custom_voice("This is regular text to speech.")
        
        # Test custom voice mode
        print("2. Testing custom voice mode...")
        self.set_voice_mode("custom")
        self.speak_with_custom_voice("This is custom voice mode with enhanced capabilities.")
        
        # Test custom voice files
        if self.custom_voices:
            print("3. Testing custom voice files...")
            self.play_random_custom_voice()
        
        print("✅ Voice test complete!")
    
    def set_elevenlabs_key(self, api_key):
        """Set ElevenLabs API key"""
        self.elevenlabs.set_api_key(api_key)
        
    def set_elevenlabs_voice(self, voice_name):
        """Set ElevenLabs voice"""
        return self.elevenlabs.set_voice(voice_name)
        
    def list_elevenlabs_voices(self):
        """List ElevenLabs voices"""
        return self.elevenlabs.list_voices()
        
    def test_elevenlabs_voice(self, voice_name=None):
        """Test ElevenLabs voice"""
        return self.elevenlabs.test_voice(voice_name)
        
    def play_greeting_voice(self):
        """Play a greeting from your voice files"""
        greetings = [name for name in self.custom_voices.keys() if 'hello' in name.lower() or 'hi' in name.lower() or 'greeting' in name.lower()]
        if greetings:
            return self.play_custom_voice(greetings[0])
        else:
            return self.play_random_custom_voice()
    
    def speak_with_your_voice(self, text):
        """Use your voice files when possible, gTTS otherwise"""
        # Check if you have a matching voice file
        text_lower = text.lower()
        
        # Look for matching voice files
        for name, path in self.custom_voices.items():
            name_lower = name.lower()
            if any(word in name_lower for word in ['hello', 'hi'] if word in text_lower):
                return self.play_custom_voice(name)
        
        # If no matching file, use gTTS with your voice style
        return self.text_to_custom_voice(text)
    
    def get_voice_status(self):
        """Get current voice system status"""
        status = {
            'mode': self.current_mode,
            'custom_voices_count': len(self.custom_voices),
            'custom_voices_available': list(self.custom_voices.keys()),
            'voice_folder': self.voice_folder,
            'elevenlabs_info': self.elevenlabs.get_voice_info()
        }
        return status