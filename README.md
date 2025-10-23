# Advanced AI Assistant System

A comprehensive terminal-based AI system with consciousness, multi-language support, story collection, and advanced memory capabilities.

## 🚀 Features

### 🧠 **Consciousness & Thinking**
- Shows AI's internal reasoning process
- Step-by-step analysis before responding
- Transparent decision making

### 🎤 **Multi-Language Voice Support**
- English, Hindi, Telugu voice synthesis
- Natural speech with auto-adjusting speed
- Language-specific voice selection

### 📚 **Story Collection**
- Indian ghost stories (Bhangarh, Shaniwarwada, Dow Hill)
- Adventure, romance, sci-fi stories
- Keyword search and random story selection

### 🔍 **Smart Search Engine**
- Multi-source search (DuckDuckGo, Wikipedia, News)
- Intelligent search filtering
- Real-time information retrieval

### 💾 **Advanced Memory System**
- Conversation history with topic tracking
- User preference learning
- Context-aware responses
- Memory export and statistics

### 🌍 **Location & Weather Services**
- Indian pincode-based location lookup
- Weather information and forecasting
- Location-aware search enhancement

### 🔄 **Translation Services**
- Telugu, Hindi, English translation
- Voice output in selected language
- Text display in English

## 📦 Setup

1. **Install Ollama** (for local AI):
   ```bash
   winget install Ollama.Ollama
   ```

2. **Install Python packages**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Pull AI model**:
   ```bash
   ollama pull llama3.2
   ```

4. **Run the terminal AI**:
   ```bash
   python terminal_ai.py
   ```

## 🎯 Usage Commands

### **Story Commands**
- `story ghost` - Get ghost/horror stories
- `story adventure` - Get adventure stories
- `random story` - Get random story
- `search story [keyword]` - Find stories by keyword

### **Language Commands**
- `english/hindi/telugu` - Switch language
- `translate [text] to [language]` - Translate text

### **Interactive Commands**
- `ask me a question` - AI asks you questions
- `quiz me` - Interactive quiz mode

### **Memory Commands**
- `memory` - Show memory statistics
- `learn [key] [value]` - Teach preferences
- `export` - Export conversations

## 🛠️ System Requirements

- **OS**: Windows 10/11
- **Python**: 3.8+
- **RAM**: 8GB+ (16GB recommended)
- **Internet**: Required for search features

## 🚀 Getting Started

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Install Ollama and pull llama3.2 model
4. Run: `python terminal_ai.py`
5. Try: `story ghost` or `ask me a question`