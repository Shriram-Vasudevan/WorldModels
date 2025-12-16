# Quick Start - Home Object Locator

Get this running in 5 minutes!

## Setup

### 1. Install Dependencies

```bash
cd prototype/home_locator
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

```bash
# Copy env template
cp .env.example .env

# Edit .env and add your key
# OPENAI_API_KEY=sk-...
```

Or just export it:
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### 3. Test Without API (Offline)

```bash
# Run offline test - no API calls, just tests the graph
python test_api.py
```

You should see:
```
🧪 Testing Home Object Locator (without API calls)
1️⃣ Simulating photo observations...
✓ Added observation 1: Keys and mug on kitchen counter
...
✅ Test complete!
```

### 4. Start the API Server

```bash
python app.py
```

You should see:
```
🏠 Home Object Locator API starting on port 5001...
📝 Make sure OPENAI_API_KEY is set in your environment
🔗 API running at http://localhost:5001
```

## Using the API

### Test with Browser

Open http://localhost:5001 in your browser to see API info.

### Upload a Photo

Take a photo of something in your house, then:

```bash
curl -X POST http://localhost:5001/upload \
  -F "image=@/path/to/photo.jpg" \
  -F "note=keys on kitchen counter"
```

Response:
```json
{
  "success": true,
  "photo_id": "abc-123",
  "extracted": {
    "objects": [
      {
        "name": "car keys",
        "location": "kitchen counter",
        "confidence": 0.9
      }
    ]
  },
  "message": "Processed photo and found 1 objects"
}
```

### Ask Where Something Is

```bash
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Where are my keys?"}'
```

Response:
```json
{
  "success": true,
  "question": "Where are my keys?",
  "answer": "Your car keys are on the kitchen counter. They were last seen there on [timestamp]. The keys are silver Toyota keys with a black fob."
}
```

### List Everything

```bash
# All objects
curl http://localhost:5001/objects

# All locations
curl http://localhost:5001/locations

# Full graph
curl http://localhost:5001/graph
```

## Swift App Integration

### 1. Find Your Mac's IP Address

```bash
# macOS
ifconfig | grep "inet " | grep -v 127.0.0.1
```

You'll see something like `inet 192.168.1.100`

### 2. Update Swift Code

In `swift_example.swift`, change:
```swift
static let baseURL = "http://192.168.1.100:5001"  // Your Mac's IP
```

### 3. Make Sure Firewall Allows Connections

System Preferences → Security & Privacy → Firewall → Allow incoming connections for Python

### 4. Build Your iOS App

Use the SwiftUI example in `swift_example.swift` as a starting point:
- Take photo with camera
- Add optional note
- Upload to API
- Query for objects
- Display results

## Example Workflow

### Scenario: Finding Your Keys

**Step 1**: Walk around house taking photos

```bash
# Photo 1: Kitchen
curl -X POST http://localhost:5001/upload \
  -F "image=@kitchen.jpg" \
  -F "note=kitchen counter"

# Photo 2: Bedroom
curl -X POST http://localhost:5001/upload \
  -F "image=@bedroom.jpg" \
  -F "note=desk and nightstand"

# Photo 3: Living room
curl -X POST http://localhost:5001/upload \
  -F "image=@living_room.jpg" \
  -F "note=coffee table"
```

**Step 2**: System builds semantic graph automatically

**Step 3**: Later, ask where things are

```bash
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Where are my keys?"}'

curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Where did I leave my wallet?"}'
```

## Troubleshooting

### "No module named flask"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
```bash
export OPENAI_API_KEY="sk-..."
# Or add to .env file
```

### "Connection refused" from iOS
- Make sure API is running: `python app.py`
- Check firewall settings
- Verify IP address in Swift code
- Try from Mac first: `curl http://localhost:5001`

### GPT-4 Vision errors
- Check your API key is valid
- Make sure you have GPT-4 Vision access
- Image might be too large (max 16MB)

## Next Steps

1. **Take real photos** around your house
2. **Build the Swift app** using the example code
3. **Add features**:
   - Photo history
   - Location categories
   - Object tracking over time
   - Notifications when objects move
   - Share graph with family members

## Cost Estimate

GPT-4 Vision API costs:
- ~$0.01 per image analysis
- ~$0.001 per text query

Example: 50 photos + 100 queries = ~$0.60

Keep an eye on your OpenAI usage at https://platform.openai.com/usage
