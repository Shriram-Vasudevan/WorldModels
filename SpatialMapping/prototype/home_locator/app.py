"""Flask API for home object locator."""

import os
import uuid
from datetime import datetime
from io import BytesIO

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from PIL import Image

from graph_manager import GraphManager
from vision_processor import VisionProcessor

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size

# Initialize components
graph_manager = GraphManager()
vision_processor = VisionProcessor()


@app.route("/", methods=["GET"])
def index():
    """API info."""
    return jsonify(
        {
            "name": "Home Object Locator API",
            "version": "0.1.0",
            "endpoints": {
                "POST /upload": "Upload photo with optional note",
                "POST /query": "Ask where something is",
                "GET /graph": "Get current semantic graph",
                "GET /locations": "List all known locations",
                "GET /objects": "List all known objects",
                "GET /search": "Search for objects (query param: q)",
                "DELETE /graph": "Clear all data",
            },
        }
    )


@app.route("/upload", methods=["POST"])
def upload_photo():
    """
    Upload a photo with optional note.

    Form data:
        image: Image file (required)
        note: Text note/context (optional)

    Returns:
        JSON with extracted objects and locations
    """
    try:
        # Check if image is present
        if "image" not in request.files:
            return jsonify({"error": "No image file provided"}), 400

        image_file = request.files["image"]
        if image_file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        # Get optional note
        note = request.form.get("note", None)

        # Load image
        image = Image.open(image_file.stream)

        # Convert to RGB if needed (for PNGs with alpha)
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Analyze photo with GPT-4 Vision
        print(f"Analyzing photo... (note: {note})")
        vision_result = vision_processor.analyze_photo(image, note)

        # Generate photo ID
        photo_id = str(uuid.uuid4())

        # Add to graph
        graph_manager.add_observation(vision_result, photo_id)

        # Return result
        return jsonify(
            {
                "success": True,
                "photo_id": photo_id,
                "timestamp": vision_result.get("timestamp"),
                "extracted": {
                    "objects": vision_result.get("objects", []),
                    "locations": vision_result.get("locations", []),
                    "relationships": vision_result.get("relationships", []),
                },
                "message": f"Processed photo and found {len(vision_result.get('objects', []))} objects",
            }
        )

    except Exception as e:
        print(f"Error uploading photo: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/query", methods=["POST"])
def query_location():
    """
    Ask where something is.

    JSON body:
        question: "Where are my keys?" (required)

    Returns:
        Natural language answer
    """
    try:
        data = request.get_json()
        if not data or "question" not in data:
            return jsonify({"error": "No question provided"}), 400

        question = data["question"]

        # Get current graph data
        graph_data = graph_manager.get_graph()

        # Query using GPT
        answer = vision_processor.query_location(question, graph_data)

        return jsonify(
            {
                "success": True,
                "question": question,
                "answer": answer,
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        print(f"Error processing query: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/graph", methods=["GET"])
def get_graph():
    """Get entire semantic graph."""
    return jsonify(graph_manager.get_graph())


@app.route("/objects", methods=["GET"])
def list_objects():
    """List all known objects."""
    objects = graph_manager.list_all_objects()
    return jsonify({"count": len(objects), "objects": objects})


@app.route("/locations", methods=["GET"])
def list_locations():
    """List all known locations."""
    locations = graph_manager.list_all_locations()
    return jsonify({"count": len(locations), "locations": locations})


@app.route("/search", methods=["GET"])
def search_objects():
    """
    Search for objects.

    Query params:
        q: Search query

    Returns:
        List of matching objects
    """
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided (use ?q=search_term)"}), 400

    results = graph_manager.search_objects(query)
    return jsonify({"query": query, "count": len(results), "results": results})


@app.route("/graph", methods=["DELETE"])
def clear_graph():
    """Clear all graph data (for testing)."""
    graph_manager.clear_graph()
    return jsonify({"success": True, "message": "Graph cleared"})


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify(
        {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "stats": graph_manager.get_graph().get("metadata", {}),
        }
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print(f"\n🏠 Home Object Locator API starting on port {port}...")
    print(f"📝 Make sure OPENAI_API_KEY is set in your environment")
    print(f"🔗 API running at http://localhost:{port}\n")

    app.run(host="0.0.0.0", port=port, debug=True)
