"""
Google Places API - Nearby Search Test
Searches for restaurants near a specified location using Google Places API.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    print("ERROR: GOOGLE_API_KEY not found in .env file")
    exit(1)

# API endpoint
url = "https://places.googleapis.com/v1/places:searchNearby"

# Request headers
headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.rating,places.businessStatus"
}

# Request payload
payload = {
    "includedTypes": ["restaurant"],
    "maxResultCount": 10,
    "locationRestriction": {
        "circle": {
            "center": {
                "latitude": 37.7937,
                "longitude": -122.3965
            },
            "radius": 500.0
        }
    }
}

print("="*80)
print("GOOGLE PLACES API - NEARBY SEARCH")
print("="*80)
print(f"\nSearching for restaurants near coordinates:")
print(f"  Latitude: 37.7937")
print(f"  Longitude: -122.3965")
print(f"  Radius: 500 meters")
print(f"\n" + "="*80 + "\n")

try:
    # Make the POST request
    print("Sending request to Google Places API...")
    response = requests.post(url, json=payload, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        print("✅ Request successful!\n")
        
        # Parse and print the response
        data = response.json()
        
        if "places" in data:
            places = data["places"]
            print(f"Found {len(places)} restaurants:\n")
            
            for i, place in enumerate(places, 1):
                print(f"{i}. {place.get('displayName', {}).get('text', 'N/A')}")
                if "formattedAddress" in place:
                    print(f"   Address: {place['formattedAddress']}")
                if "rating" in place:
                    print(f"   Rating: {place['rating']}")
                if "businessStatus" in place:
                    print(f"   Status: {place['businessStatus']}")
                print()
        else:
            print("No places found in the response.")
        
        # Print full response for debugging
        print("\n" + "="*80)
        print("FULL API RESPONSE:")
        print("="*80)
        print(json.dumps(data, indent=2))
        
    else:
        print(f"❌ Error: HTTP {response.status_code}")
        print(f"Response: {response.text}\n")
        
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {str(e)}")
except json.JSONDecodeError as e:
    print(f"❌ Failed to parse response: {str(e)}")
except Exception as e:
    print(f"❌ Unexpected error: {str(e)}")

print("\n" + "="*80)
