import os
import pygame
import tempfile
from gtts import gTTS
import requests
import random
import time
from pydub import AudioSegment
from pydub.playback import play

class VoiceCloneSystem:
    def __init__(self):
        pygame.mixer.init()
        self.voice_folder = r"C:\Users\shaik\Music\voice"
        self.sample_voice = None
        self.human_effects = True
        self.find_sample_voice()
        
    def find_sample_voice(self):
        """Find a sample voice file to use as reference"""
        if os.path.exists(self.voice_folder):
            for file in os.listdir(self.voice_folder):
                if file.lower().endswith(('.mp3', '.wav', '.ogg')):
                    self.sample_voice = os.path.join(self.voice_folder, file)
                    print(f"🎤 Using voice sample: {file}")
                    break
        
        if not self.sample_voice:
            print("❌ No voice samples found")
    
    def clone_voice_elevenlabs(self, text):
        """Use ElevenLabs voice cloning with your voice sample"""
        try:
            # This would require uploading your voice sample to ElevenLabs
            # and getting a custom voice ID
            api_key = "sk_c1171d6e671e152ba77e3c776cdb0e5130908d961fd1a6e7"
            
            # For now, use a similar sounding voice
            voice_id = "21m00Tcm4TlvDq8ikWAM"  # Rachel - adjust to match your voice
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.8,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(url, json=data, headers=headers)
            
            if response.status_code == 200:
                return response.content
            else:
                print(f"ElevenLabs error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Voice clone error: {e}")
            return None
    
    def speak_like_you(self, text):
        """Generate speech that sounds like your voice with human effects"""
        try:
            if self.human_effects:
                # Add pre-speech human effects (silent pauses only)
                effects = self.add_human_effects(text)
                for effect in effects:
                    self.play_human_effect(effect)
            
            # Clean text for speech (remove all symbols)
            enhanced_text = self.clean_text_for_speech(text)
            
            # Try ElevenLabs voice cloning with enhanced settings
            audio_data = self.clone_voice_elevenlabs(enhanced_text)
            
            if audio_data:
                # Play the cloned voice
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                    tmp_file.write(audio_data)
                    tmp_filename = tmp_file.name
                
                pygame.mixer.music.load(tmp_filename)
                pygame.mixer.music.play()
                
                # Wait for playback
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # Clean up
                try:
                    os.unlink(tmp_filename)
                except:
                    pass
                
                # Add post-speech breathing (20% chance)
                if self.human_effects and random.random() < 0.2:
                    time.sleep(0.3)
                    print("🎤 *exhales softly*")
                    time.sleep(0.2)
                    
                return True
            else:
                # Fallback to enhanced TTS
                return self.enhanced_tts(enhanced_text)
                
        except Exception as e:
            print(f"Speech error: {e}")
            return False
    
    def enhanced_tts(self, text):
        """Enhanced TTS as fallback"""
        try:
            # Use gTTS with settings to match your voice style
            tts = gTTS(text=text, lang='en', slow=False, tld='com')
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
                    
                return True
                
        except Exception as e:
            print(f"TTS error: {e}")
            return False
    
    def add_human_effects(self, text):
        """Add minimal human speech effects for speed"""
        effects = []
        
        # Add breathing before speaking (30% chance)
        if random.random() < 0.3:
            effects.append("breathing")
        
        # Add throat clearing for longer responses (10% chance)
        if len(text) > 100 and random.random() < 0.1:
            effects.append("throat_clear")
        
        # Add thinking pauses (20% chance)
        if random.random() < 0.2:
            effects.append("thinking")
        
        return effects
    
    def clean_text_for_speech(self, text):
        """Clean text and remove symbols that shouldn't be spoken"""
        # Remove all effect symbols and markers
        import re
        text = re.sub(r'\*[^*]*\*', '', text)  # Remove *symbols*
        text = re.sub(r'\s+', ' ', text)  # Fix multiple spaces
        text = text.strip()
        return text
    
    def enhance_speech_quality(self, text):
        """Enhance speech with ElevenLabs professional settings"""
        # Enhanced voice settings for more human-like speech
        enhanced_settings = {
            "stability": 0.6,  # Slight variation for naturalness
            "similarity_boost": 0.9,  # High similarity to your voice
            "style": 0.7,  # More expressive
            "use_speaker_boost": True
        }
        return enhanced_settings
    
    def play_human_effect(self, effect):
        """Play human sound effects (minimal pauses)"""
        if effect == "breathing":
            print("🎤 *takes a breath*")
            time.sleep(0.2)  # Quick breathing pause
        elif effect == "throat_clear":
            print("🎤 *clears throat*")
            time.sleep(0.1)  # Quick throat clearing pause
        elif effect == "thinking":
            print("🎤 *pauses to think*")
            time.sleep(0.3)  # Quick thinking pause
    
    def test_voice(self):
        """Test the voice cloning with human effects"""
        test_text = "Hello! This is how I sound when I speak. Do you like my voice?"
        print("🎤 Testing voice clone with human effects...")
        return self.speak_like_you(test_text)