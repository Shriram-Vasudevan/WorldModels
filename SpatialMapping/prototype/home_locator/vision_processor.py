"""GPT-4 Vision integration for analyzing photos and extracting objects/locations."""

import base64
import os
from datetime import datetime
from io import BytesIO
from typing import Dict, List, Optional

from openai import OpenAI
from PIL import Image


class VisionProcessor:
    """Process photos using GPT-4 Vision to extract objects and locations."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with OpenAI API key."""
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def encode_image(self, image: Image.Image) -> str:
        """Encode PIL Image to base64 string."""
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    def analyze_photo(
        self, image: Image.Image, user_note: Optional[str] = None
    ) -> Dict:
        """
        Analyze photo to extract objects and their locations.

        Args:
            image: PIL Image object
            user_note: Optional user-provided context

        Returns:
            Dict with extracted objects, locations, and relationships
        """
        # Encode image
        base64_image = self.encode_image(image)

        # Build prompt
        prompt = """Analyze this photo and extract:
1. Objects you can see (be specific - "black backpack", not just "backpack")
2. Locations/surfaces where objects are placed (be specific - "wooden desk near window")
3. Spatial relationships (what's on/in/near what)

Format your response as JSON:
{
  "objects": [
    {
      "name": "object name",
      "description": "brief description",
      "location": "where it is",
      "confidence": 0.0-1.0
    }
  ],
  "locations": [
    {
      "name": "location name",
      "description": "what this location looks like",
      "type": "surface/room/container/etc"
    }
  ],
  "relationships": [
    {
      "object": "object name",
      "relation": "on/in/near/etc",
      "location": "location name"
    }
  ]
}

Be specific and detailed. If you see multiple similar items, distinguish them (left vs right, color, etc).
"""

        if user_note:
            prompt += f"\n\nUser's note: {user_note}\n"

        # Call GPT-4 Vision
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using gpt-4o which has vision capabilities
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=1000,
            )

            # Parse response
            content = response.choices[0].message.content

            # Try to extract JSON from response
            import json
            import re

            # Look for JSON block in response
            json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", content, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group(1))
            else:
                # Try parsing entire content as JSON
                result = json.loads(content)

            # Add metadata
            result["timestamp"] = datetime.now().isoformat()
            result["user_note"] = user_note
            result["raw_response"] = content

            return result

        except Exception as e:
            print(f"Error analyzing photo: {e}")
            # Return basic structure with error
            return {
                "objects": [],
                "locations": [],
                "relationships": [],
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def query_location(self, question: str, graph_data: Dict) -> str:
        """
        Answer a question about object location using the semantic graph.

        Args:
            question: User's question (e.g., "Where are my keys?")
            graph_data: Current semantic graph data

        Returns:
            Natural language answer
        """
        # Build context from graph
        context = self._build_graph_context(graph_data)

        prompt = f"""You are a helpful assistant that helps people find their belongings.

Here's what we know about objects in the house:

{context}

User question: {question}

Provide a helpful, natural answer. If you know where the object is, be specific about:
- What it looks like
- Exactly where it was last seen
- When it was last seen
- Any nearby landmarks

If you don't know, say so clearly and suggest what photos they could take to help locate it.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Sorry, I encountered an error: {e}"

    def _build_graph_context(self, graph_data: Dict) -> str:
        """Build text context from graph data for GPT."""
        context_parts = []

        # Add objects
        if "objects" in graph_data:
            context_parts.append("Known objects:")
            for obj_name, obj_data in graph_data["objects"].items():
                location = obj_data.get("location", "unknown location")
                last_seen = obj_data.get("last_seen", "unknown time")
                desc = obj_data.get("description", "")

                context_parts.append(
                    f"- {obj_name}: {desc if desc else ''} "
                    f"at {location} (last seen: {last_seen})"
                )

        # Add locations
        if "locations" in graph_data:
            context_parts.append("\nKnown locations:")
            for loc_name, loc_data in graph_data["locations"].items():
                objects = loc_data.get("objects", [])
                desc = loc_data.get("description", "")

                obj_list = ", ".join(objects) if objects else "empty"
                context_parts.append(
                    f"- {loc_name}: {desc if desc else ''} (contains: {obj_list})"
                )

        return "\n".join(context_parts) if context_parts else "No data yet."
