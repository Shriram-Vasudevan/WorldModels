"""Quick test script for the API - no real photos needed."""

import json
from datetime import datetime

from graph_manager import GraphManager

print("🧪 Testing Home Object Locator (without API calls)\n")

# Initialize graph manager
graph = GraphManager(data_file="data/test_graph.json")

# Clear any existing test data
graph.clear_graph()

# Simulate some observations
print("1️⃣ Simulating photo observations...\n")

# Observation 1: Keys on kitchen counter
obs1 = {
    "objects": [
        {
            "name": "car keys",
            "description": "silver Toyota keys with black fob",
            "location": "kitchen counter",
            "confidence": 0.9,
        },
        {
            "name": "coffee mug",
            "description": "blue ceramic mug",
            "location": "kitchen counter",
            "confidence": 0.85,
        },
    ],
    "locations": [
        {
            "name": "kitchen counter",
            "description": "granite counter next to the sink",
            "type": "surface",
        }
    ],
    "relationships": [
        {"object": "car keys", "relation": "on", "location": "kitchen counter"},
        {"object": "coffee mug", "relation": "on", "location": "kitchen counter"},
    ],
    "timestamp": datetime.now().isoformat(),
}

graph.add_observation(obs1, "photo_001")
print("✓ Added observation 1: Keys and mug on kitchen counter")

# Observation 2: Laptop on desk
obs2 = {
    "objects": [
        {
            "name": "macbook pro",
            "description": "silver laptop, 14 inch",
            "location": "desk in bedroom",
            "confidence": 0.95,
        },
        {
            "name": "charging cable",
            "description": "white USB-C cable",
            "location": "desk in bedroom",
            "confidence": 0.8,
        },
    ],
    "locations": [
        {
            "name": "desk in bedroom",
            "description": "wooden desk near the window",
            "type": "surface",
        }
    ],
    "relationships": [
        {"object": "macbook pro", "relation": "on", "location": "desk in bedroom"},
        {"object": "charging cable", "relation": "near", "location": "macbook pro"},
    ],
    "timestamp": datetime.now().isoformat(),
}

graph.add_observation(obs2, "photo_002")
print("✓ Added observation 2: Laptop on desk")

# Observation 3: Wallet in backpack
obs3 = {
    "objects": [
        {
            "name": "wallet",
            "description": "brown leather wallet",
            "location": "black backpack",
            "confidence": 0.7,
        }
    ],
    "locations": [
        {
            "name": "black backpack",
            "description": "backpack hanging on chair in bedroom",
            "type": "container",
        }
    ],
    "relationships": [
        {"object": "wallet", "relation": "in", "location": "black backpack"}
    ],
    "timestamp": datetime.now().isoformat(),
}

graph.add_observation(obs3, "photo_003")
print("✓ Added observation 3: Wallet in backpack\n")

# Test queries
print("2️⃣ Testing queries...\n")

# Query 1: Find keys
keys = graph.get_object("keys")
if keys:
    print(f"🔑 Car Keys:")
    print(f"   Location: {keys['location']}")
    print(f"   Last seen: {keys['last_seen'][:19]}")
    print(f"   Description: {keys['description']}\n")

# Query 2: Find laptop
laptop = graph.get_object("macbook")
if laptop:
    print(f"💻 MacBook Pro:")
    print(f"   Location: {laptop['location']}")
    print(f"   Last seen: {laptop['last_seen'][:19]}")
    print(f"   Description: {laptop['description']}\n")

# Query 3: What's on kitchen counter?
kitchen_objects = graph.get_objects_at_location("kitchen counter")
print(f"🍳 Kitchen Counter contains:")
for obj in kitchen_objects:
    print(f"   - {obj['name']}")
print()

# Query 4: List all locations
print("📍 All known locations:")
for loc in graph.list_all_locations():
    obj_count = len(loc.get("objects", []))
    print(f"   - {loc['name']} ({obj_count} objects)")
print()

# Query 5: Search
print("🔍 Searching for 'wallet':")
results = graph.search_objects("wallet")
for r in results:
    print(f"   Found: {r['name']} at {r['location']}")
print()

# Show graph stats
print("3️⃣ Graph Statistics:")
graph_data = graph.get_graph()
metadata = graph_data["metadata"]
print(f"   Objects: {len(graph_data['objects'])}")
print(f"   Locations: {len(graph_data['locations'])}")
print(f"   Total observations: {metadata['total_observations']}")
print()

# Export graph
print("4️⃣ Full graph:")
print(json.dumps(graph_data, indent=2, default=str))
print()

print("✅ Test complete! Graph saved to data/test_graph.json")
print("\nNext step: Run 'python app.py' and try uploading real photos!")
