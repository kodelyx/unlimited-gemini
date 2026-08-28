# ⚡ Unlimited Gemini

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Cross-Platform](https://img.shields.io/badge/platform-macOS%20|%20Linux%20|%20Windows-success.svg)](#)
[![Zero Cost](https://img.shields.io/badge/API%20Cost-%240%20Unlimited-brightgreen.svg)](#)

A high-performance, zero-configuration Python engine and Chrome Extension bridge for **Google Gemini 3.7**, **Imagen 3 (8K Images)**, **Gemini Omni (HD Videos)**, **Instrumental Music Synthesis**, and **Embedded SQLite Memory**.

Zero API keys required. No rate-limit fees. Works out of the box.

---

## 🏛️ Architecture

```
[ Chrome Extension (gemini-extension) ] ──(Auto-sync fresh cookies via WS)──► [ ~/.gemini_engine/cookies.json ]
                                                                                         │
                                                                                         ▼
[ Any Python App / Script / Agent ] ──(HTTP REST / Stream)──► [ Go Core Engine (Port 8001) ] ──► [ Google Gemini 3.7 Cloud ]
                                                                     │
                                                                     ▼
                                                          [ SQLite WAL Mode Database ]
```

---

## 📦 Quick Setup

### 1. Load Chrome Extension (One-time, 15 seconds)
1. Open Google Chrome and navigate to `chrome://extensions`.
2. Toggle **Developer mode** ON (top-right corner).
3. Click **Load unpacked** and select the [`chrome-extension/`](./chrome-extension) folder.
4. Visit [gemini.google.com](https://gemini.google.com) once to initialize session cookies.

### 2. Install Python SDK
```bash
cd python-sdk
pip install -e .
```

### 3. Verify Everything in 1 Command
```bash
python test.py
```

---

## 🚀 Python SDK Quickstart

### 💬 1. Text Chat & Code Reasoning (Gemini 3.7 Flash)
```python
from gemini_engine import GeminiEngine

engine = GeminiEngine()
reply = engine.chat("Explain Python metaclasses with a concise code example.")
print(reply)
```

### ⚡ 2. Real-Time Streaming Chat (Typing Effect)
```python
for token in engine.stream_chat("Write a short story about an autonomous AI agent."):
    print(token, end="", flush=True)
```

### 🔄 3. Multi-Turn Conversational Memory
```python
chat = engine.start_chat()
chat.send("My name is Akash and I am building an AI agent.")
reply = chat.send("What is my name and what am I building?")
print(reply)  # Context is remembered across turns
```

### 🎨 4. 8K Image Generation (Imagen 3)
```python
# Watermark-free, ultra-HD 16:9 illustration
img = engine.generate_image("A futuristic cyber kitten on a neon city rooftop in 16:9", save_to="kitten.png")
print("Saved image to:", img["local_path"])
```

### 🎬 5. Cinematic Video Generation (Gemini Omni)
```python
# Generates and downloads native MP4 video
video = engine.generate_video("A majestic eagle soaring over snow mountains at sunset", fps=24, save_to="eagle.mp4")
print("Saved video to:", video["local_path"])
```

### 🎵 6. Instrumental Music Synthesis (Gemini Music)
```python
# Generates and downloads studio 192kbps MP3 audio
music = engine.generate_music("Create an instrumental piano melody track", save_to="piano.mp3")
print("Saved audio to:", music["local_path"])
```

### 👁️ 7. Multimodal Vision, Video, Audio & PDF Analysis
```python
# Analyze photos, videos, audio clips, or PDF documents directly with Gemini 3.7
print(engine.analyze_image("photo.png", prompt="Describe this image in detail."))
print(engine.analyze_file("recording.mp4", prompt="Summarize what happens in this video."))
print(engine.analyze_document("paper.pdf", prompt="Extract the key findings."))
```

### 🗄️ 8. Embedded SQLite History Search
```python
# Fast keyword search across past chat history
results = engine.search_history("metaclasses", limit=5)
for item in results:
    print(f"[{item['role']}]: {item['content']}")
```

---

## 📊 Feature Comparison

| Capability | Model / Engine | Quality / Output | Local Save |
|---|---|---|---|
| **Text Reasoning** | Gemini 3.7 Flash | Markdown & Code | SQLite WAL |
| **Streaming** | Server-Sent Events | Low latency tokens | SQLite WAL |
| **Stateful Memory** | Session Manager | Multi-turn context | SQLite WAL |
| **Image Generation** | Google Imagen 3 | 8K Ultra-HD (16:9 / 1:1) | `.png` |
| **Video Generation** | Gemini Omni | 24 FPS Cinematic Video | `.mp4` |
| **Music Synthesis** | Google Lyria / Music | 192 kbps Stereo Audio | `.mp3` |
| **Multimodal Vision** | Gemini 3.7 Multimodal | Text / PDF / Media Analysis | Live Reply |
| **History & Gallery** | Embedded SQLite | Fast full-text search | `data/gemini.db` |

---

## 🛡️ License

This project is licensed under the [MIT License](./LICENSE).
