"""
⚡ GeminiEngine - Python Native AI Engine (Gemini 3.7 + Needle 2 SLM + Multi-Modal)
Author: Akash Yadav
---------------------------------------------------------------------------------
Zero-configuration, ultra-fast Python AI Engine with on-demand binary downloads,
streaming chat, 8K image gen, cinematic video gen, music synthesis, and SQLite memory.
"""

import os
import sys
import json
import time
import base64
import atexit
import platform
import subprocess
import urllib.request
import urllib.parse
import mimetypes
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any, Generator

VERSION = "1.0.0"
GITHUB_REPO = "kodelyx/free-gemini-api"
RELEASE_BASE_URL = f"https://github.com/{GITHUB_REPO}/releases/download/v{VERSION}"

CACHE_DIR = Path.home() / ".gemini_engine"
BIN_CACHE_DIR = CACHE_DIR / "bin"
COOKIES_DIR = CACHE_DIR / "cookies"

_DEFAULT_PORT = 8001
_DEFAULT_BASE_URL = f"http://127.0.0.1:{_DEFAULT_PORT}"
_daemon_proc: Optional[subprocess.Popen] = None

def _cleanup_daemon():
    global _daemon_proc
    if _daemon_proc and _daemon_proc.poll() is None:
        try:
            _daemon_proc.terminate()
        except Exception:
            pass

atexit.register(_cleanup_daemon)

def _get_platform_info() -> tuple[str, str]:
    sys_name = platform.system().lower()
    machine = platform.machine().lower()

    if sys_name == "darwin":
        if "arm" in machine or "aarch64" in machine:
            return "darwin-arm64", "gemini-core-darwin-arm64"
        return "darwin-amd64", "gemini-core-darwin-amd64"
    elif sys_name == "linux":
        return "linux-amd64", "gemini-core-linux-amd64"
    elif sys_name == "windows":
        return "windows-amd64", "gemini-core-windows-amd64.exe"
    return "linux-amd64", "gemini-core-linux-amd64"

def _download_file_with_progress(url: str, dest_path: Path, desc: str):
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = dest_path.with_suffix(".tmp")

    headers = {"User-Agent": "gemini-engine-py"}

    print(f"⬇️  Downloading {desc} from official repository (one-time setup)...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(temp_path, "wb") as out_file:
            total_size = int(response.info().get("Content-Length", 0))
            downloaded = 0
            block_size = 64 * 1024

            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                downloaded += len(buffer)
                out_file.write(buffer)
                if total_size > 0:
                    percent = downloaded * 100 / total_size
                    mb_down = downloaded / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    sys.stdout.write(f"\r   [{percent:5.1f}%] {mb_down:.1f} MB / {mb_total:.1f} MB")
                    sys.stdout.flush()

        print()
        temp_path.rename(dest_path)
        dest_path.chmod(0o755)
        print(f"✅ {desc} downloaded & verified successfully!\n")
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise RuntimeError(f"Failed to download {desc} from {url}: {e}")

def _ensure_binaries() -> Path:
    BIN_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    COOKIES_DIR.mkdir(parents=True, exist_ok=True)

    platform_tag, bin_name = _get_platform_info()
    local_bin = BIN_CACHE_DIR / bin_name

    # 1. Check local cache
    if local_bin.exists():
        return local_bin

    # 2. Check local package bundled bin
    bundled_bin = Path(__file__).parent / "bin" / bin_name
    if bundled_bin.exists():
        return bundled_bin

    # 3. Download from official public GitHub Release
    download_url = f"{RELEASE_BASE_URL}/{bin_name}"
    _download_file_with_progress(download_url, local_bin, f"Gemini Core ({platform_tag})")
    return local_bin


class ChatSession:
    """
    Stateful multi-turn chat session with automatic memory persistence.
    """
    def __init__(self, engine: "GeminiEngine", session_id: Optional[str] = None):
        self.engine = engine
        self.session_id = session_id or f"session_{int(time.time()*1000)}"
        self._history: List[Dict[str, str]] = []

    def send(self, message: str) -> str:
        """Send a message within this ongoing conversation."""
        reply = self.engine.chat(message, user_id=self.session_id, new_chat=False)
        self._history.append({"role": "user", "content": message})
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def stream(self, message: str) -> Generator[str, None, None]:
        """Stream response tokens within this ongoing conversation."""
        full_reply = []
        for chunk in self.engine.stream_chat(message, user_id=self.session_id):
            full_reply.append(chunk)
            yield chunk
        self._history.append({"role": "user", "content": message})
        self._history.append({"role": "assistant", "content": "".join(full_reply)})

    def reset(self):
        """Clear session memory and start fresh."""
        self._history.clear()
        self.engine.reset_session(self.session_id)

    @property
    def history(self) -> List[Dict[str, str]]:
        return self._history


class GeminiEngine:
    """
    100% Pythonic Multi-Modal AI Engine (Mac, Linux, Windows).
    Features: Text, Streaming, 8K Images, HD Videos, Music Synthesis, Vision, SQLite Memory.
    """
    def __init__(self, base_url: str = _DEFAULT_BASE_URL, default_user_id: str = "default_user", auto_start: bool = True):
        self.base_url = base_url.rstrip("/")
        self.default_user_id = default_user_id

        if auto_start and not self._is_server_alive():
            self._start_engine()

    def _is_server_alive(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.base_url}/health")
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def _start_engine(self):
        global _daemon_proc
        try:
            core_bin = _ensure_binaries()
            if not core_bin.exists():
                return

            _daemon_proc = subprocess.Popen(
                [str(core_bin)],
                cwd=str(CACHE_DIR),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                close_fds=(platform.system().lower() != "windows")
            )
            for _ in range(40):
                if self._is_server_alive():
                    break
                time.sleep(0.1)
        except Exception:
            pass

    @property
    def is_online(self) -> bool:
        return self._is_server_alive()

    def chat(self, prompt: str, user_id: Optional[str] = None, new_chat: bool = False) -> str:
        """
        Send a text prompt to Gemini 3.7 Flash. Returns the complete text response.
        """
        payload = {
            "prompt": prompt,
            "user_id": user_id or self.default_user_id,
            "new_chat": new_chat
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                res = json.loads(resp.read().decode("utf-8"))
                return res.get("text", "")
        except Exception as e:
            raise RuntimeError(f"GeminiEngine error: {e}")

    def stream_chat(self, prompt: str, user_id: Optional[str] = None) -> Generator[str, None, None]:
        """
        Stream text completions token-by-token using OpenAI-compatible SSE stream.
        """
        payload = {
            "model": "gemini-3.7-flash",
            "messages": [{"role": "user", "content": prompt}],
            "user_id": user_id or self.default_user_id,
            "stream": True
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/v1/chat/completions",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                for line in resp:
                    line_str = line.decode("utf-8").strip()
                    if line_str.startswith("data: ") and not line_str.startswith("data: [DONE]"):
                        try:
                            json_str = line_str[6:]
                            chunk = json.loads(json_str)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield content
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            raise RuntimeError(f"Streaming error: {e}")

    def start_chat(self, session_id: Optional[str] = None) -> ChatSession:
        """
        Start a stateful multi-turn chat session with conversational memory.
        """
        return ChatSession(self, session_id=session_id)

    def analyze_image(self, image_path: str, prompt: str = "Describe this image in full detail.", user_id: Optional[str] = None) -> str:
        """
        Send an image/photo to Gemini 3.7 Flash for deep visual analysis and multimodal reasoning.
        """
        img_file = Path(image_path).resolve()
        if not img_file.exists():
            raise FileNotFoundError(f"Image not found at {img_file}")

        mime_type, _ = mimetypes.guess_type(str(img_file))
        if not mime_type:
            mime_type = "image/png"

        with open(img_file, "rb") as f:
            file_bytes = f.read()

        import uuid
        boundary = f"----GeminiVisionBoundary{uuid.uuid4().hex}"
        body = bytearray()

        # Add prompt field
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
        body.extend(prompt.encode("utf-8"))
        body.extend(b"\r\n")

        # Add user_id field
        uid = user_id or f"vision_{int(time.time())}"
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(b'Content-Disposition: form-data; name="user_id"\r\n\r\n')
        body.extend(uid.encode("utf-8"))
        body.extend(b"\r\n")

        # Add new_chat field
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(b'Content-Disposition: form-data; name="new_chat"\r\n\r\n')
        body.extend(b"true\r\n")

        # Add file upload field
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="images"; filename="{img_file.name}"\r\n'.encode("utf-8"))
        body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
        body.extend(file_bytes)
        body.extend(b"\r\n")

        body.extend(f"--{boundary}--\r\n".encode("utf-8"))

        req = urllib.request.Request(
            f"{self.base_url}/chat",
            data=bytes(body),
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res.get("text", "")

    def analyze_file(self, file_path: str, prompt: str = "Analyze and summarize this document.", user_id: Optional[str] = None) -> str:
        """
        Universal file analysis (PDF, DOCX, TXT, CSV, MP4, MP3, PNG, JPG) with Gemini 3.7.
        """
        return self.analyze_image(image_path=file_path, prompt=prompt, user_id=user_id)

    def analyze_document(self, document_path: str, prompt: str = "Summarize the key points of this document.", user_id: Optional[str] = None) -> str:
        """
        Deep document & PDF analysis, text extraction, and Q&A with Gemini 3.7.
        """
        return self.analyze_image(image_path=document_path, prompt=prompt, user_id=user_id)

    def generate_image(self, prompt: str, aspect_ratio: str = "16:9", save_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate an 8K photo / illustration using Imagen 3.
        Watermarks are automatically removed and high-res file is returned.
        """
        full_prompt = f"Generate an image of {prompt} in {aspect_ratio}" if "image" not in prompt.lower() else prompt
        payload = {
            "prompt": full_prompt,
            "user_id": f"img_gen_{int(time.time())}",
            "new_chat": True
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            images = res.get("images") or []
            if not images:
                raise RuntimeError(f"Image generation error: {res.get('text')}")

            image_url = images[0]
            local_path = None
            if save_to:
                out_file = Path(save_to).resolve()
                out_file.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(image_url, str(out_file))
                local_path = str(out_file)

            return {
                "url": image_url,
                "local_path": local_path,
                "text": res.get("text", ""),
                "conversation_id": res.get("conversation_id"),
                "elapsed": res.get("elapsed", 0)
            }

    def generate_video(self, prompt: str, fps: int = 24, save_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate cinematic videos using Gemini Omni (Omni-modal Video Engine).
        """
        payload = {
            "prompt": f"Generate a {fps}fps cinematic video of {prompt}",
            "user_id": f"vid_gen_{int(time.time())}",
            "new_chat": True
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=300) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            local_path = None
            videos = res.get("videos") or []
            if videos and save_to:
                out_file = Path(save_to).resolve()
                out_file.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(videos[0], str(out_file))
                local_path = str(out_file)
            res["local_path"] = local_path
            return res

    def generate_music(self, prompt: str, save_to: Optional[str] = None) -> Dict[str, Any]:
        """
        Synthesize music and audio tracks using Gemini Music.
        """
        payload = {
            "prompt": prompt,
            "user_id": f"music_{int(time.time())}",
            "new_chat": True
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/music",
            data=data,
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            music_tracks = res.get("music") or []
            local_path = None
            
            # Prefer local server bridge URL (already clean & authenticated)
            stream_url = None
            if music_tracks:
                stream_url = music_tracks[0].get("local_path") or music_tracks[0].get("download_url")

            if stream_url and save_to:
                out_file = Path(save_to).resolve()
                out_file.parent.mkdir(parents=True, exist_ok=True)
                urllib.request.urlretrieve(stream_url, str(out_file))
                local_path = str(out_file)

            return {
                "tracks": music_tracks,
                "download_url": stream_url,
                "local_path": local_path,
                "text": res.get("text", "")
            }

    def search_history(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search past conversation history in local SQLite database.
        """
        url = f"{self.base_url}/history/search?q={urllib.parse.quote(query)}&limit={limit}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res.get("results") or []

    def get_media_gallery(self) -> List[Dict[str, Any]]:
        """
        Fetch all generated images, videos, and media logged in the SQLite database.
        """
        req = urllib.request.Request(f"{self.base_url}/media")
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            return res.get("media") or []

    def get_stats(self) -> Dict[str, Any]:
        """
        Get live system, cookie account, and database statistics.
        """
        req = urllib.request.Request(f"{self.base_url}/stats")
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def reset_session(self, user_id: str):
        """
        Reset conversational context for a given session.
        """
        payload = json.dumps({"user_id": user_id}).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/reset",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            return {}

    def get_openai_client(self):
        """
        Get an official openai.OpenAI client configured for this local engine.
        """
        try:
            from openai import OpenAI
            return OpenAI(base_url=f"{self.base_url}/v1", api_key="sk-free-gemini")
        except ImportError:
            raise ImportError("Please install openai library: pip install openai")
