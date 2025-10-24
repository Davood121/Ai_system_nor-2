import os
import pygame
import random

class SimpleVoiceSystem:
    def __init__(self):
        pygame.mixer.init()
        self.voice_folder = r"C:\Users\shaik\Music\voice"
        self.voice_files = {}
        self.load_voice_files()
        
    def load_voice_files(self):
        """Load voice files from folder"""
        if os.path.exists(self.voice_folder):
            for file in os.listdir(self.voice_folder):
                if file.lower().endswith(('.mp3', '.wav', '.ogg')):
                    name = os.path.splitext(file)[0]
                    self.voice_files[name] = os.path.join(self.voice_folder, file)
            print(f"🎤 Loaded {len(self.voice_files)} voice files")
        else:
            print(f"❌ Voice folder not found: {self.voice_folder}")
    
    def play_voice(self, filename=None):
        """Play voice file"""
        try:
            if filename and filename in self.voice_files:
                pygame.mixer.music.load(self.voice_files[filename])
            elif self.voice_files:
                # Play random voice file
                random_file = random.choice(list(self.voice_files.values()))
                pygame.mixer.music.load(random_file)
            else:
                print("No voice files available")
                return False
                
            pygame.mixer.music.play()
            return True
        except Exception as e:
            print(f"Voice error: {e}")
            return False
    
    def list_voices(self):
        """List available voice files"""
        if self.voice_files:
            print("\n🎵 Your Voice Files:")
            for i, name in enumerate(self.voice_files.keys(), 1):
                print(f"  {i}. {name}")
        else:
            print("No voice files found")
    
    def speak(self, text):
        """Play a voice file for AI response"""
        return self.play_voice()