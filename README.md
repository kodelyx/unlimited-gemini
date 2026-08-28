# ⚡ Unlimited Gemini

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Cross-Platform](https://img.shields.io/badge/platform-macOS%20|%20Linux%20|%20Windows-success.svg)](#)
[![Zero Cost](https://img.shields.io/badge/API%20Cost-%240%20Unlimited-brightgreen.svg)](#)

> **Free, unlimited, multi-modal Google Gemini 3.7 AI Engine for Python & REST API.**  
> **Inbuilt Tool Calling • 8K Images (Nano Banana 2) • HD Videos (Gemini Omni) • Studio Audio • Multimodal Vision & SQLite Memory.**

**Zero API keys required • No rate-limit fees • Works out-of-the-box**

---

## 📦 Quick Setup (15 Seconds)

1. **Chrome Extension (One-time):** Load [`chrome-extension/`](./chrome-extension) in `chrome://extensions` (Developer Mode).
2. **Install Engine:**
   ```bash
   cd gemini-engine && pip install -e .
   ```
3. **Verify:**
   ```bash
   python test.py
   ```

---

## 🚀 1-Minute Python Usage

```python
from gemini_engine import GeminiEngine

engine = GeminiEngine()

# 💬 Text Chat & Reasoning
print(engine.chat("Why is Python popular?"))

# ⚡ Real-Time Streaming (Typing Effect)
for token in engine.stream_chat("Write a 2-line poem"):
    print(token, end="", flush=True)

# 🎨 8K Image Generation (Nano Banana 2)
engine.generate_image("Cyberpunk kitten in 16:9", save_to="kitten.png")

# 🎬 HD Cinematic Video (Gemini Omni)
engine.generate_video("Eagle flying over mountains", save_to="eagle.mp4")

# 🎵 Music & Audio Synthesis
engine.generate_music("Create an instrumental piano melody track", save_to="piano.mp3")

# 👁️ Multimodal Vision (Image, Video, Audio, PDF)
print(engine.analyze_file("sample_doc.pdf", prompt="Summarize this document"))
```

---

## 🌐 Simple cURL / HTTP Requests (Any Language)

Call the local engine directly on port `8001` with zero setup:

```bash
# 💬 Text Chat
curl http://127.0.0.1:8001/chat -d '{"prompt": "Why is Python popular?"}'

# ⚡ Streaming (Typing Effect)
curl http://127.0.0.1:8001/chat -d '{"prompt": "Count 1 to 5", "stream": true}'

# 🎨 8K Image (Nano Banana 2)
curl http://127.0.0.1:8001/chat -d '{"prompt": "Generate an image of a red sports car in 16:9"}'

# 🎬 HD Video (Gemini Omni)
curl http://127.0.0.1:8001/chat -d '{"prompt": "Generate a 24fps cinematic video of eagle flying"}'

# 🎵 Music Synthesis
curl http://127.0.0.1:8001/music -d '{"prompt": "Create an instrumental piano melody track"}'

# 👁️ Vision / PDF / Media Analysis
curl http://127.0.0.1:8001/chat -F "prompt=Summarize this" -F "images=@document.pdf"

# 🔌 OpenAI Drop-In Endpoint
curl http://127.0.0.1:8001/v1/chat/completions -d '{"messages": [{"role": "user", "content": "Hello!"}]}'
```

---

## 📊 Feature Comparison

| Capability | Model / Engine | Output | Local Save |
|---|---|---|---|
| **Text Reasoning** | Gemini 3.7 Flash | Markdown & Code | SQLite WAL |
| **Inbuilt Tool Calling** | Python Sandbox & Web | Autonomous execution | SQLite WAL |
| **Streaming** | Server-Sent Events | Low latency tokens | SQLite WAL |
| **8K Images** | Nano Banana 2 (Imagen 3) | 8K Ultra-HD (16:9 / 1:1) | `.png` |
| **HD Videos** | Gemini Omni | 24 FPS Cinematic Video | `.mp4` |
| **Music Synthesis** | Google Lyria / Music | 192 kbps Stereo Audio | `.mp3` |
| **Multimodal Vision** | Gemini 3.7 Multimodal | Text / PDF / Media Analysis | Live Reply |
| **Database Memory** | Embedded SQLite | Fast full-text search | `data/gemini.db` |

---

## 🛡️ License

This project is licensed under the [MIT License](./LICENSE).
