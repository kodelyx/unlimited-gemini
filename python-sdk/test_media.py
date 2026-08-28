#!/usr/bin/env python3
"""
🎬 Complete Video & 🎵 Music Verification Test
"""

from gemini_engine import GeminiEngine

def main():
    engine = GeminiEngine()
    print("==================================================")
    print("🎬 1. TESTING CINEMATIC VIDEO GENERATION")
    print("==================================================")
    vid_res = engine.generate_video("A majestic eagle soaring over snow mountains at sunset", fps=24, save_to="eagle_video.mp4")
    print("✅ Video generated & saved to:", vid_res.get("local_path"))
    print("🔗 Video URL:", vid_res.get("videos"))

    print("\n==================================================")
    print("🎵 2. TESTING INSTRUMENTAL MUSIC SYNTHESIS")
    print("==================================================")
    music_res = engine.generate_music("Create an instrumental piano melody track", save_to="piano_melody.mp3")
    print("✅ Music generated & saved to:", music_res.get("local_path"))
    print("🔗 Music Download URL:", music_res.get("download_url"))

if __name__ == "__main__":
    main()
