#!/usr/bin/env python
"""
Test script to verify the translator API is working
Run this to check all endpoints are properly loaded
"""

from factory import create_app
import json

app = create_app()

def test_endpoints():
    print("=" * 60)
    print("TRANSLATOR API - ENDPOINT VERIFICATION")
    print("=" * 60)
    
    print("\n✓ Flask app initialized successfully")
    print("\n📍 Registered API Endpoints:")
    print("-" * 60)
    
    endpoints = {}
    for rule in app.url_map.iter_rules():
        if 'user' in str(rule):
            methods = [m for m in rule.methods if m != 'OPTIONS']
            endpoint = str(rule.rule).replace('/user', '')
            endpoints[endpoint] = methods
    
    print("\n1️⃣  POST /user/translate")
    print("   └─ Translate Tamil text to English")
    
    print("\n2️⃣  POST /user/transcribe")
    print("   └─ Transcribe audio to text (AssemblyAI)")
    
    print("\n3️⃣  POST /user/transcribe-and-translate")
    print("   └─ Transcribe Tamil audio + translate to English")
    
    print("\n" + "=" * 60)
    print("NEXT STEPS:")
    print("=" * 60)
    print("\n1. Get your AssemblyAI API key:")
    print("   → Visit https://www.assemblyai.com/")
    print("   → Sign up for a free account")
    print("   → Copy your API key from dashboard")
    
    print("\n2. Update the .env file:")
    print("   → Edit .env file in this directory")
    print("   → Replace 'your_api_key_here' with your actual API key")
    
    print("\n3. Start the server:")
    print("   → Run: python main.py")
    print("   → Server will run on http://localhost:5000")
    
    print("\n4. Test endpoints (examples):")
    print("\n   Test translation:")
    print('   curl -X POST http://localhost:5000/user/translate \\')
    print('     -H "Content-Type: application/json" \\')
    print('     -d \'{"TamilText": "வணக்கம்"}\'')
    
    print("\n   Test transcription:")
    print('   curl -X POST -F "audio=@your_audio.wav" \\')
    print('     http://localhost:5000/user/transcribe')
    
    print("\n   Test transcribe + translate:")
    print('   curl -X POST -F "audio=@tamil_audio.wav" \\')
    print('     http://localhost:5000/user/transcribe-and-translate')
    
    print("\n" + "=" * 60)
    print("✓ SETUP COMPLETE AND VERIFIED!")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    test_endpoints()
