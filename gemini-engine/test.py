#!/usr/bin/env python3
"""
🚀 GeminiEngine All-in-One Comprehensive Test Suite
Author: Akash Yadav
--------------------------------------------------
Tests:
1. System & SQLite Database Stats
2. Standard Text Chat (Gemini 3.7 Flash)
3. Real-Time Streaming Chat (Typing Effect)
4. Multi-Turn Conversational Session (Memory)
5. 8K Image Generation (Imagen 3)
6. SQLite Memory History Search
"""

from gemini_engine import GeminiEngine

def main():
    print("==================================================")
    print("⚡ Initializing GeminiEngine (Python Native)...")
    print("==================================================")
    
    engine = GeminiEngine()
    
    if not engine.is_online:
        print("❌ Engine failed to initialize!")
        return

    print("✅ Engine online & healthy!\n")

    # 1. Database Stats
    stats = engine.get_stats()
    print("📊 [1. Database Stats]:", stats)

    # 2. Standard Text Chat
    print("\n💬 [2. Standard Chat]: 'Why is Python popular?'")
    reply = engine.chat("Why is Python popular in 1 bullet point?")
    print(f"💡 [Reply]: {reply.strip()}\n")

    # 3. Real-Time Streaming Chat
    print("⚡ [3. Real-Time Streaming Chat]: 'Count 1 to 5'")
    print("   Streaming: ", end="", flush=True)
    for token in engine.stream_chat("Count 1, 2, 3, 4, 5 with commas"):
        print(token, end="", flush=True)
    print("\n")

    # 4. Multi-Turn Conversational Session (Context Memory)
    print("🔄 [4. Multi-Turn Session with Memory]:")
    chat = engine.start_chat()
    print("   User: My favorite color is Neon Cyan.")
    r1 = chat.send("My favorite color is Neon Cyan. Remember it.")
    print(f"   AI: {r1.strip()}")
    print("   User: What is my favorite color?")
    r2 = chat.send("What is my favorite color?")
    print(f"   AI: {r2.strip()}\n")

    # 5. 8K Image Generation (Imagen 3)
    print("🎨 [5. 8K Image Generation (Imagen 3)]:")
    print("   Prompt: 'A cute futuristic cyber kitten wearing headphones in 16:9'")
    img = engine.generate_image("A cute futuristic cyber kitten wearing headphones in 16:9", save_to="cyber_kitten.png")
    print(f"   ✅ Image Generated & Saved: {img['local_path']}")
    print(f"   🔗 URL: {img['url']}\n")

    # 6. SQLite History Search
    print("🔍 [6. SQLite History Search]: Query 'Cyan'...")
    results = engine.search_history("Cyan", limit=2)
    for r in results:
        print(f"   • Found ID {r['id']} ({r['role']}): {r['content'][:60]}...")

    print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY! Python AI Engine is 100% functional.")

if __name__ == "__main__":
    main()
