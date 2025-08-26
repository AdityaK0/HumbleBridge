#!/usr/bin/env python3
"""
Test script for HumbleBridge API
Run this after starting the server to test the endpoints
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("🧪 Testing HumbleBridge API...")
    
    # Test health check
    print("\n1. Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Health check: {response.status_code} - {response.json()}")
    
    # Test registration
    print("\n2. Testing user registration...")
    donor_data = {
        "email": "donor@example.com",
        "password": "password123",
        "role": "donor"
    }
    response = requests.post(f"{BASE_URL}/register", json=donor_data)
    print(f"Donor registration: {response.status_code}")
    if response.status_code == 200:
        donor_info = response.json()
        print(f"Donor created: {donor_info['email']} (ID: {donor_info['id']})")
    
    # Test volunteer registration
    volunteer_data = {
        "email": "volunteer@example.com",
        "password": "password123",
        "role": "volunteer"
    }
    response = requests.post(f"{BASE_URL}/register", json=volunteer_data)
    print(f"Volunteer registration: {response.status_code}")
    if response.status_code == 200:
        volunteer_info = response.json()
        print(f"Volunteer created: {volunteer_info['email']} (ID: {volunteer_info['id']})")
    
    # Test login
    print("\n3. Testing login...")
    login_data = {
        "email": "donor@example.com",
        "password": "password123"
    }
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    print(f"Login: {response.status_code}")
    if response.status_code == 200:
        token_info = response.json()
        token = token_info['access_token']
        print(f"Token received: {token[:20]}...")
        
        # Test profile endpoint
        print("\n4. Testing profile endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        print(f"Profile: {response.status_code}")
        if response.status_code == 200:
            profile = response.json()
            print(f"Profile: {profile['email']} - Coins: {profile['coins']}")
        
        # Test donation creation
        print("\n5. Testing donation creation...")
        donation_data = {
            "item_name": "Winter Jacket",
            "category": "clothes",
            "description": "Warm winter jacket in good condition",
            "pickup_address": "123 Main St, City, State",
            "image_url": "https://example.com/jacket.jpg"
        }
        response = requests.post(f"{BASE_URL}/donate", json=donation_data, headers=headers)
        print(f"Donation creation: {response.status_code}")
        if response.status_code == 200:
            donation = response.json()
            print(f"Donation created: {donation['item_name']} (ID: {donation['id']})")
    
    print("\n✅ API test completed!")
    print(f"📚 API Documentation: {BASE_URL}/docs")
    print(f"🔍 Alternative Docs: {BASE_URL}/redoc")

if __name__ == "__main__":
    test_api() 