# Home Object Locator - Prototype Overview

## What Is This?

A working prototype that lets you **find household objects using photos and AI**.

**The Concept:**
1. Walk around your house taking photos with your phone
2. Add optional notes like "keys on kitchen counter"
3. GPT-4 Vision extracts objects and locations into a semantic graph
4. Ask "Where are my keys?" and get natural answers
5. All accessible via a simple REST API that your Swift app can use

## What's Built

### ✅ Complete Backend System

**Files:**
```
prototype/home_locator/
├── app.py                    # Flask REST API (200+ lines)
├── vision_processor.py       # GPT-4 Vision integration (200+ lines)
├── graph_manager.py          # Semantic graph storage (250+ lines)
├── test_api.py              # Offline test script
├── test_with_curl.sh        # API test script
├── swift_example.swift      # iOS integration example (200+ lines)
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── QUICKSTART.md           # 5-minute setup guide
└── README.md               # API documentation
```

### Key Features

**Vision Processing** (vision_processor.py):
- GPT-4 Vision API integration
- Extracts objects, locations, and spatial relationships from photos
- Natural language query interface
- Context-aware answers

**Semantic Graph** (graph_manager.py):
- JSON-based storage (simple, no database needed)
- Entity matching and merging
- Fuzzy search
- Temporal tracking (last seen timestamps)
- Location-based queries

**REST API** (app.py):
- `POST /upload` - Upload photo + note
- `POST /query` - Ask where something is
- `GET /objects` - List all objects
- `GET /locations` - List all locations
- `GET /search?q=term` - Search objects
- `GET /graph` - Get full semantic graph
- `DELETE /graph` - Clear data (testing)

**Swift Integration**:
- Complete iOS example code
- Image upload with multipart/form-data
- JSON query interface
- SwiftUI example view

## How to Use

### 1. Quick Test (2 minutes)

```bash
cd prototype/home_locator
pip install -r requirements.txt
python test_api.py
```

This runs offline tests with simulated data. No API key needed.

### 2. Run API Server (5 minutes)

```bash
# Set your OpenAI API key
export OPENAI_API_KEY="sk-..."

# Start server
python app.py

# Server runs at http://localhost:5001
```

### 3. Upload Real Photos

```bash
# Take a photo of your desk
curl -X POST http://localhost:5001/upload \
  -F "image=@desk_photo.jpg" \
  -F "note=my desk with laptop and phone"
```

### 4. Query for Objects

```bash
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Where is my laptop?"}'
```

Response:
```json
{
  "answer": "Your MacBook Pro is on the desk in your bedroom, near the window. It was last seen there today at 2:30 PM. There's also a charging cable nearby."
}
```

### 5. Build Swift App

- Copy code from `swift_example.swift`
- Update `baseURL` to your Mac's IP address
- Implement camera capture
- Connect to API endpoints
- Done!

## Example Use Cases

### 1. Daily Object Finding
"Where are my keys?" → "On the kitchen counter, next to the coffee maker"

### 2. Pre-Trip Checklist
"Do I have my passport?" → "Yes, in your black backpack on the bedroom chair"

### 3. Family Coordination
"Where did dad leave the car keys?" → Everyone uses same graph

### 4. Memory Aid
"What was on my desk yesterday?" → Temporal queries

## Technical Highlights

### Smart Entity Extraction

GPT-4 Vision doesn't just detect "keys" - it extracts:
- **Specific description**: "silver Toyota keys with black fob"
- **Precise location**: "kitchen counter next to the sink"
- **Spatial relationships**: "on the counter", "near the coffee maker"
- **Confidence scores**: How certain it is

### Intelligent Merging

If you take two photos of the same object:
- System recognizes it's the same thing (fuzzy matching)
- Updates location if it moved
- Increases confidence with more observations
- Tracks observation count

### Natural Language Queries

Not just keyword search - GPT understands:
- "Where are my keys?"
- "Did I leave my wallet upstairs?"
- "What's on the kitchen table?"
- "Where did I put that charger?"

Answers in full sentences with context.

### Zero Infrastructure

- No database server (JSON files)
- No cloud storage (local only)
- No fixed sensors
- Just photos + GPT-4

## What's Missing (For Production)

This is a **prototype**. For real deployment you'd want:

**Storage:**
- Database (PostgreSQL) instead of JSON
- Photo storage (S3 or local filesystem)
- Vector database for similarity search

**Features:**
- User accounts and authentication
- Photo history and replay
- Object movement tracking over time
- Shared graphs for families
- Push notifications ("Your keys moved!")
- Categories and tags

**Performance:**
- Caching for frequent queries
- Background processing queue
- Batch photo uploads
- Incremental graph updates

**Mobile:**
- Native photo capture
- Offline mode with sync
- Background uploads
- Widget for quick queries

## Cost Estimate

OpenAI API costs (as of 2025):
- **GPT-4 Vision**: ~$0.01 per image
- **GPT-4 Text**: ~$0.001 per query

**Example monthly usage:**
- 10 photos/day = 300/month = $3
- 20 queries/day = 600/month = $0.60
- **Total: ~$3.60/month**

Very affordable for personal use.

## Architecture Alignment

This prototype demonstrates the **core vision** of the larger project:

✅ **Physical world, computable**
- Photos → structured graph
- Natural language queries work

✅ **No fixed infrastructure**
- Any phone camera works
- No sensors or pre-mapping

✅ **Multi-device merging**
- Different phones add to same graph
- Automatic entity resolution

✅ **Semantic-first**
- Focus on what/where, not coordinates
- Relationships, not just positions

This is the semantic memory system, **simplified and focused** on household objects.

## Next Steps

### For You Right Now

1. **Test it**: Run `python test_api.py`
2. **Try real photos**: Start the API, upload photos
3. **Build Swift app**: Use example code as starting point
4. **Use it daily**: Track your stuff for a week

### To Extend

**Easy wins:**
- Add photo thumbnails to responses
- Email/text notifications
- Export to CSV
- Location categories (home vs office)

**Medium complexity:**
- Object history timeline
- Probability tracking (likely locations)
- Integration with calendar (temporal queries)
- Voice interface (Siri shortcuts)

**Advanced:**
- Video support (continuous scanning)
- 3D spatial understanding
- Multi-user with privacy
- Predictive "you'll need X soon"

## Files You'll Edit Most

**To customize backend:**
- `vision_processor.py` - Tweak GPT prompts, add vision models
- `graph_manager.py` - Change storage, add queries
- `app.py` - Add endpoints, modify responses

**To build iOS app:**
- `swift_example.swift` - Copy this as starting template
- Create SwiftUI views for camera, query, results
- Add background upload, notifications

## Questions?

This is a **vibecode prototype** - it's meant to be:
- Simple enough to understand quickly
- Complete enough to actually use
- Extensible enough to build on

Try it out, break it, extend it. The foundation is solid.

---

**Start here:** `cd prototype/home_locator && cat QUICKSTART.md`
