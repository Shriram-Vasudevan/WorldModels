# Home Object Locator - Prototype

A quick prototype for finding household objects using photos, notes, and GPT-4.

## Concept

1. **Capture**: Take photos around your house with notes ("keys on kitchen counter", "laptop on desk")
2. **Build**: System uses GPT-4 Vision to extract objects and locations into a semantic graph
3. **Query**: Ask "Where are my keys?" via API and get natural language answers
4. **Mobile**: Swift app sends photos/queries to local API

## Quick Start

```bash
# Install dependencies
pip install flask openai pillow python-dotenv

# Set your OpenAI API key
export OPENAI_API_KEY="your-key-here"

# Run the server
python app.py

# Server runs on http://localhost:5001
```

## API Endpoints

### POST /upload
Upload photo with optional note
```bash
curl -X POST http://localhost:5001/upload \
  -F "image=@photo.jpg" \
  -F "note=keys on kitchen counter"
```

### POST /query
Ask where something is
```bash
curl -X POST http://localhost:5001/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Where are my keys?"}'
```

### GET /graph
Get current semantic graph
```bash
curl http://localhost:5001/graph
```

### GET /locations
List all known locations
```bash
curl http://localhost:5001/locations
```

### GET /objects
List all known objects
```bash
curl http://localhost:5001/objects
```

## Swift Integration

See `swift_example.swift` for iOS integration example.

## How It Works

1. **Photo Upload**: You send a photo (+ optional note) to `/upload`
2. **GPT-4 Vision**: Analyzes photo, extracts objects and their locations
3. **Graph Update**: Stores objects, locations, and relationships in JSON
4. **Query**: When you ask "Where's X?", GPT-4 searches the graph and responds naturally

## Data Storage

Everything stored in `data/graph.json`:
```json
{
  "objects": {
    "keys": {
      "location": "kitchen counter",
      "last_seen": "2025-01-15T10:30:00",
      "photo_id": "abc123",
      "confidence": 0.9
    }
  },
  "locations": {
    "kitchen counter": {
      "objects": ["keys", "wallet"],
      "description": "counter next to the sink"
    }
  }
}
```

## Prototype Limitations

- No authentication
- Single user only
- JSON file storage (no real database)
- Basic error handling
- Photos stored in memory only
- No photo history/persistence

For production, you'd want:
- User accounts
- Proper database (PostgreSQL + vector store)
- Photo storage (S3)
- Better entity matching
- Temporal tracking (object movement over time)
