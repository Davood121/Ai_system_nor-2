"""
Voice Installation Helper for Windows
Run this to check and install additional language voices
"""

import subprocess
import sys

def check_installed_voices():
    """Check what voices are currently installed"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print("Currently installed voices:")
        print("-" * 50)
        
        for i, voice in enumerate(voices):
            print(f"{i+1}. {voice.name}")
            print(f"   ID: {voice.id}")
            print(f"   Languages: {getattr(voice, 'languages', 'Unknown')}")
            print()
            
        return voices
    except Exception as e:
        print(f"Error checking voices: {e}")
        return []

def install_language_packs():
    """Instructions for installing language packs on Windows"""
    print("\n" + "="*60)
    print("HOW TO INSTALL ADDITIONAL LANGUAGE VOICES ON WINDOWS")
    print("="*60)
    
    print("\n1. WINDOWS SETTINGS METHOD:")
    print("   - Open Windows Settings (Win + I)")
    print("   - Go to Time & Language > Speech")
    print("   - Click 'Add voices'")
    print("   - Download Hindi, Telugu, or other language packs")
    
    print("\n2. CONTROL PANEL METHOD:")
    print("   - Open Control Panel")
    print("   - Go to Clock and Region > Region")
    print("   - Click 'Administrative' tab")
    print("   - Click 'Copy settings' and enable for new users")
    
    print("\n3. POWERSHELL METHOD (Run as Administrator):")
    print("   Get-WindowsCapability -Online | Where-Object {$_.Name -like '*TextToSpeech*'}")
    print("   Add-WindowsCapability -Online -Name 'TextToSpeech.hi-IN~~~~0.0.1.0'")
    print("   Add-WindowsCapability -Online -Name 'TextToSpeech.te-IN~~~~0.0.1.0'")
    
    print("\n4. ALTERNATIVE TTS ENGINES:")
    print("   - Install Microsoft Speech Platform")
    print("   - Download language-specific TTS engines")
    print("   - Use Azure Cognitive Services Speech SDK")

def test_language_voices():
    """Test different language voices"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        test_texts = {
            'english': 'Hello, this is a test of English voice.',
            'hindi': 'नमस्ते, यह हिंदी आवाज का परीक्षण है।',
            'telugu': 'హలో, ఇది తెలుగు వాయిస్ టెస్ట్.'
        }
        
        print("\nTesting available voices:")
        print("-" * 30)
        
        for i, voice in enumerate(voices):
            print(f"\nTesting voice {i+1}: {voice.name}")
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 150)
            
            # Test with English first
            engine.say("Testing voice")
            engine.runAndWait()
            
            input("Press Enter to continue to next voice...")
            
    except Exception as e:
        print(f"Error testing voices: {e}")

if __name__ == "__main__":
    print("Voice Installation Helper")
    print("=" * 30)
    
    # Check current voices
    voices = check_installed_voices()
    
    # Show installation instructions
    install_language_packs()
    
    # Ask if user wants to test voices
    test = input("\nDo you want to test available voices? (y/n): ")
    if test.lower() == 'y':
        test_language_voices()
    
    print("\nAfter installing new language packs:")
    print("1. Restart your computer")
    print("2. Run your AI assistant")
    print("3. Try switching languages with 'hindi' or 'telugu' commands")