import ollama

try:
    response = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': 'Hello, can you respond with just "Yes, I can respond"?'}
    ])
    print("AI Response:", response['message']['content'])
except Exception as e:
    print("Error:", e)
    print("Make sure Ollama is running: ollama serve")