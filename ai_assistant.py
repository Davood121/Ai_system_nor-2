import streamlit as st
import pyttsx3
import requests
import ollama
from duckduckgo_search import DDGS
import wikipedia
import threading
import time
import sounddevice as sd
import numpy as np
import whisper
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor

# Global model cache to avoid reloading
_whisper_model_cache = None
_tts_engine_cache = None

class AIAssistant:
    def __init__(self):
        global _tts_engine_cache, _whisper_model_cache

        # Reuse cached TTS engine
        if _tts_engine_cache is None:
            _tts_engine_cache = pyttsx3.init()
        self.tts_engine = _tts_engine_cache

        # Lazy load Whisper model only when needed
        self.whisper_model = None
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.response_cache = {}  # Cache for search results
        
    def _load_whisper_model(self):
        """Lazy load Whisper model only when needed"""
        global _whisper_model_cache
        if _whisper_model_cache is None:
            try:
                _whisper_model_cache = whisper.load_model("base")
            except:
                return None
        return _whisper_model_cache

    def speak(self, text):
        """Convert text to speech (async)"""
        # Run in background thread to avoid blocking
        self.executor.submit(self._speak_sync, text)

    def _speak_sync(self, text):
        """Synchronous speak operation"""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except:
            pass

    def listen(self):
        """Convert speech to text using Whisper (lazy loaded)"""
        # Load model only when needed
        if self.whisper_model is None:
            self.whisper_model = self._load_whisper_model()

        if not self.whisper_model:
            return "Voice recognition not available"

        try:
            # Record audio
            duration = 5  # seconds
            sample_rate = 16000
            audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
            sd.wait()

            # Convert to whisper format
            audio = audio.flatten().astype(np.float32)

            # Transcribe
            result = self.whisper_model.transcribe(audio)
            return result["text"]
        except:
            return None

    def search_web(self, query, max_results=3):
        """Search web using DuckDuckGo (cached)"""
        # Check cache first
        cache_key = f"{query}:{max_results}".lower()
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]

        try:
            results = []
            with DDGS() as ddgs:
                for result in ddgs.text(query, max_results=max_results):
                    results.append({
                        'title': result['title'],
                        'snippet': result['body'],
                        'url': result['href']
                    })

            # Cache the results
            self.response_cache[cache_key] = results
            return results
        except:
            return []
    
    def search_wikipedia(self, query):
        """Search Wikipedia"""
        try:
            summary = wikipedia.summary(query, sentences=3)
            return summary
        except:
            return None
    
    def get_ai_response(self, prompt, context=""):
        """Get response from local AI model (cached)"""
        # Check cache first
        cache_key = f"{prompt}:{context}".lower()[:100]
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]

        try:
            full_prompt = f"Context: {context}\n\nUser: {prompt}\n\nProvide a helpful, concise response:"

            response = ollama.chat(model='llama3.2', messages=[
                {'role': 'user', 'content': full_prompt}
            ], stream=False)

            result = response['message']['content']

            # Cache the response
            self.response_cache[cache_key] = result
            return result
        except:
            return "AI model not available. Please install Ollama and pull llama3.2 model."

    def summarize_content(self, content):
        """Summarize long content (async)"""
        prompt = f"Summarize this content in 2-3 sentences: {content}"
        # Run in background to avoid blocking UI
        self.executor.submit(self.get_ai_response, prompt)

def main():
    st.set_page_config(page_title="Personal AI Assistant", layout="wide")
    
    st.title("🤖 Personal AI Assistant")
    st.sidebar.title("Features")
    
    # Initialize assistant
    if 'assistant' not in st.session_state:
        st.session_state.assistant = AIAssistant()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    assistant = st.session_state.assistant
    
    # Sidebar options
    mode = st.sidebar.selectbox("Choose Mode:", 
                               ["💬 Chat", "🔍 Search", "🎤 Voice Chat", "📝 Summarize"])
    
    if mode == "💬 Chat":
        st.header("Chat with AI")
        
        user_input = st.text_input("Ask me anything:")
        
        if st.button("Send") and user_input:
            response = assistant.get_ai_response(user_input)
            
            st.session_state.chat_history.append({"user": user_input, "ai": response})
            
            st.write("**You:**", user_input)
            st.write("**AI:**", response)
    
    elif mode == "🔍 Search":
        st.header("Real-time Search")
        
        search_query = st.text_input("Search for anything:")
        search_type = st.selectbox("Search Type:", ["Web", "Wikipedia", "Both"])
        
        if st.button("Search") and search_query:
            context = ""
            
            if search_type in ["Web", "Both"]:
                st.subheader("Web Results:")
                web_results = assistant.search_web(search_query)
                for result in web_results:
                    st.write(f"**{result['title']}**")
                    st.write(result['snippet'])
                    st.write(f"[Read more]({result['url']})")
                    st.write("---")
                    context += f"{result['title']}: {result['snippet']} "
            
            if search_type in ["Wikipedia", "Both"]:
                st.subheader("Wikipedia:")
                wiki_result = assistant.search_wikipedia(search_query)
                if wiki_result:
                    st.write(wiki_result)
                    context += wiki_result
            
            # AI Analysis
            if context:
                st.subheader("AI Analysis:")
                ai_analysis = assistant.get_ai_response(f"Analyze and explain: {search_query}", context)
                st.write(ai_analysis)
    
    elif mode == "🎤 Voice Chat":
        st.header("Voice Assistant")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎤 Start Listening"):
                with st.spinner("Listening..."):
                    voice_input = assistant.listen()
                
                if voice_input:
                    st.write("**You said:**", voice_input)
                    
                    # Get AI response
                    response = assistant.get_ai_response(voice_input)
                    st.write("**AI Response:**", response)
                    
                    # Speak response
                    threading.Thread(target=assistant.speak, args=(response,)).start()
                else:
                    st.write("Could not understand audio")
        
        with col2:
            text_to_speak = st.text_area("Or type text to speak:")
            if st.button("🔊 Speak"):
                threading.Thread(target=assistant.speak, args=(text_to_speak,)).start()
    
    elif mode == "📝 Summarize":
        st.header("Content Summarizer")
        
        content_input = st.text_area("Paste content to summarize:", height=200)
        
        if st.button("Summarize") and content_input:
            summary = assistant.summarize_content(content_input)
            st.subheader("Summary:")
            st.write(summary)
    
    # Chat History
    if st.session_state.chat_history:
        st.sidebar.subheader("Recent Chats")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
            with st.sidebar.expander(f"Chat {len(st.session_state.chat_history)-i}"):
                st.write("**Q:**", chat["user"][:50] + "...")
                st.write("**A:**", chat["ai"][:50] + "...")

if __name__ == "__main__":
    main()