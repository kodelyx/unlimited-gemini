# ⚡ GeminiEngine (Python AI Engine)

A high-performance, zero-configuration Python AI package powered by **Gemini 3.7 Flash**, **Imagen 3 (8K Images)**, **Cinematic Video & Music Generation**, and embedded **SQLite Memory**.

---

## 📦 Installation & Test

```bash
# 1. Install locally
pip install -e .

# 2. Run all-in-one test suite
python test.py
```

---

## 🚀 Complete Quickstart Guide

### 1. 💬 Standard Text Chat (Gemini 3.7 Flash)
```python
from gemini_engine import GeminiEngine

engine = GeminiEngine()
reply = engine.chat("Explain Python metaclasses with a simple example")
print(reply)
```

### 2. ⚡ Real-Time Streaming Chat (Typing Effect)
```python
for token in engine.stream_chat("Write a short story about an AI exploring Mars"):
    print(token, end="", flush=True)
```

### 3. 🔄 Multi-Turn Conversational Memory (Chat Session)
```python
chat = engine.start_chat()
chat.send("My name is Akash and I am building an AI agent.")
reply = chat.send("What is my name and what am I building?")
print(reply)  # AI remembers context across turns!
```

### 4. 🎨 8K Image Generation (Imagen 3)
```python
img = engine.generate_image("A futuristic cyber sports car on neon highway in 16:9", save_to="car.png")
print("Image saved to:", img["local_path"])
```

### 5. 🎬 Cinematic Video Generation (Gemini Omni)
```python
video = engine.generate_video("A majestic eagle soaring over snow mountains at sunset", fps=24, save_to="eagle.mp4")
print("Video saved to:", video["local_path"])
```

### 6. 🎵 Music & Audio Synthesis (Gemini Music)
```python
audio = engine.generate_music("Create an instrumental piano melody track", save_to="piano.mp3")
print("Audio saved to:", audio["local_path"])
```

### 7. 📄 PDF & Multi-Format Document Analysis (Gemini 3.7 Vision & Docs)
```python
# Pass any PDF, image, video, or audio file for deep AI analysis
summary = engine.analyze_document("research_paper.pdf", prompt="Summarize key findings in 3 bullet points")
print(summary)
```

### 8. 🗄️ Persistent SQLite Memory Search
```python
# Search past conversations across all sessions
history = engine.search_history("metaclasses", limit=5)
for item in history:
    print(f"[{item['role']}]: {item['content']}")
```

---

## 🌟 Key Features

- **100% Free & Unlimited:** No OpenAI/Claude API keys or costs required.
- **Embedded Fast Engine:** Instant initialization, zero manual server startup needed.
- **Multi-Modal AI Suite:** Text Chat, Streaming, 8K Images, HD Videos, and Music.
- **Stateful Memory Sessions:** Automatic multi-turn conversation memory.
- **Built-in SQLite DB:** Automatic chat logging and fast keyword search in WAL mode.
- **Cross-Platform:** Works automatically out-of-the-box on Mac (Apple Silicon & Intel), Linux, and Windows.
