#!/bin/bash
# Quick test script using curl
# Make sure the API is running: python app.py

API="http://localhost:5001"

echo "🧪 Testing Home Object Locator API"
echo ""

# Test 1: Health check
echo "1️⃣ Health check..."
curl -s "$API/health" | python3 -m json.tool
echo ""

# Test 2: Upload a photo (you need to provide an actual image file)
# Uncomment and modify with your image path:
# echo "2️⃣ Uploading photo..."
# curl -X POST "$API/upload" \
#   -F "image=@/path/to/your/photo.jpg" \
#   -F "note=keys on kitchen counter" \
#   | python3 -m json.tool
# echo ""

# Test 3: List all objects
echo "3️⃣ Listing all objects..."
curl -s "$API/objects" | python3 -m json.tool
echo ""

# Test 4: List all locations
echo "4️⃣ Listing all locations..."
curl -s "$API/locations" | python3 -m json.tool
echo ""

# Test 5: Query where something is
echo "5️⃣ Querying: 'Where are my keys?'..."
curl -X POST "$API/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "Where are my keys?"}' \
  | python3 -m json.tool
echo ""

# Test 6: Search for objects
echo "6️⃣ Searching for 'keys'..."
curl -s "$API/search?q=keys" | python3 -m json.tool
echo ""

# Test 7: Get full graph
echo "7️⃣ Getting full graph..."
curl -s "$API/graph" | python3 -m json.tool
echo ""

echo "✅ API tests complete!"
