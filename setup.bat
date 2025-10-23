@echo off
echo Installing Ollama...
curl -fsSL https://ollama.com/install.sh | sh

echo Installing Python packages...
pip install -r requirements.txt

echo Pulling AI model...
ollama pull llama3.2

echo Setup complete! Run: streamlit run ai_assistant.py