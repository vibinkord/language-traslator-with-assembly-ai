#!/usr/bin/env python
"""
Test the Tamil Translator API endpoints
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_root():
    """Test root endpoint"""
    print("\n1️⃣ Testing ROOT endpoint (GET /)")
    print("-" * 50)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def test_translate():
    """Test translation endpoint"""
    print("\n2️⃣ Testing TRANSLATE endpoint (POST /user/translate)")
    print("-" * 50)
    try:
        payload = {"TamilText": "வணக்கம்"}
        response = requests.post(
            f"{BASE_URL}/user/translate",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        print("Response:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")

def test_transcribe():
    """Test transcribe endpoint"""
    print("\n3️⃣ Testing TRANSCRIBE endpoint (POST /user/transcribe)")
    print("-" * 50)
    print("⚠️ Skipped (requires audio file)")
    print("Example: curl -X POST -F \"audio=@audio.wav\" http://localhost:5000/user/transcribe")

def test_transcribe_translate():
    """Test transcribe-and-translate endpoint"""
    print("\n4️⃣ Testing TRANSCRIBE+TRANSLATE endpoint (POST /user/transcribe-and-translate)")
    print("-" * 50)
    print("⚠️ Skipped (requires audio file)")
    print("Example: curl -X POST -F \"audio=@audio.wav\" http://localhost:5000/user/transcribe-and-translate")

if __name__ == "__main__":
    print("=" * 50)
    print("TAMIL TRANSLATOR API - ENDPOINT TEST")
    print("=" * 50)
    
    try:
        test_root()
        time.sleep(1)
        test_translate()
        time.sleep(1)
        test_transcribe()
        test_transcribe_translate()
        
        print("\n" + "=" * 50)
        print("✓ TEST COMPLETE")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\n\n❌ Test interrupted")
