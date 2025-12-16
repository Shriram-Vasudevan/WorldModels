"""Manage semantic graph storage and retrieval."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class GraphManager:
    """Manage the semantic graph of objects and locations."""

    def __init__(self, data_file: str = "data/graph.json"):
        """Initialize graph manager with data file."""
        self.data_file = Path(data_file)
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing graph or create new
        self.graph = self._load_graph()

    def _load_graph(self) -> Dict:
        """Load graph from disk or create new."""
        if self.data_file.exists():
            try:
                with open(self.data_file, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading graph: {e}")
                return self._create_empty_graph()
        else:
            return self._create_empty_graph()

    def _create_empty_graph(self) -> Dict:
        """Create empty graph structure."""
        return {
            "objects": {},
            "locations": {},
            "metadata": {
                "created": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "total_observations": 0,
            },
        }

    def _save_graph(self) -> None:
        """Save graph to disk."""
        self.graph["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.data_file, "w") as f:
            json.dump(self.graph, f, indent=2)

    def add_observation(self, vision_result: Dict, photo_id: str) -> None:
        """
        Add observation from vision processing to graph.

        Args:
            vision_result: Result from VisionProcessor.analyze_photo()
            photo_id: Unique identifier for this photo
        """
        timestamp = vision_result.get("timestamp", datetime.now().isoformat())

        # Process objects
        for obj in vision_result.get("objects", []):
            obj_name = obj["name"].lower()
            location = obj.get("location", "unknown")

            # Add or update object
            if obj_name not in self.graph["objects"]:
                self.graph["objects"][obj_name] = {
                    "name": obj_name,
                    "description": obj.get("description", ""),
                    "location": location,
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                    "photo_id": photo_id,
                    "confidence": obj.get("confidence", 0.5),
                    "observation_count": 1,
                }
            else:
                # Update existing object
                self.graph["objects"][obj_name].update(
                    {
                        "location": location,
                        "last_seen": timestamp,
                        "photo_id": photo_id,
                        "observation_count": self.graph["objects"][obj_name].get(
                            "observation_count", 0
                        )
                        + 1,
                    }
                )

        # Process locations
        for loc in vision_result.get("locations", []):
            loc_name = loc["name"].lower()

            if loc_name not in self.graph["locations"]:
                self.graph["locations"][loc_name] = {
                    "name": loc_name,
                    "description": loc.get("description", ""),
                    "type": loc.get("type", "unknown"),
                    "objects": [],
                    "first_seen": timestamp,
                    "last_seen": timestamp,
                }
            else:
                self.graph["locations"][loc_name]["last_seen"] = timestamp

        # Process relationships to update location->object mappings
        for rel in vision_result.get("relationships", []):
            obj_name = rel["object"].lower()
            loc_name = rel["location"].lower()

            if loc_name in self.graph["locations"]:
                objects_list = self.graph["locations"][loc_name].get("objects", [])
                if obj_name not in objects_list:
                    objects_list.append(obj_name)
                self.graph["locations"][loc_name]["objects"] = objects_list

        # Update metadata
        self.graph["metadata"]["total_observations"] += 1

        # Save to disk
        self._save_graph()

    def get_object(self, name: str) -> Optional[Dict]:
        """Get object by name (fuzzy match)."""
        name_lower = name.lower()

        # Exact match
        if name_lower in self.graph["objects"]:
            return self.graph["objects"][name_lower]

        # Fuzzy match (contains)
        for obj_name, obj_data in self.graph["objects"].items():
            if name_lower in obj_name or obj_name in name_lower:
                return obj_data

        return None

    def get_location(self, name: str) -> Optional[Dict]:
        """Get location by name (fuzzy match)."""
        name_lower = name.lower()

        # Exact match
        if name_lower in self.graph["locations"]:
            return self.graph["locations"][name_lower]

        # Fuzzy match
        for loc_name, loc_data in self.graph["locations"].items():
            if name_lower in loc_name or loc_name in name_lower:
                return loc_data

        return None

    def get_objects_at_location(self, location: str) -> List[Dict]:
        """Get all objects at a location."""
        loc_data = self.get_location(location)
        if not loc_data:
            return []

        object_names = loc_data.get("objects", [])
        return [
            self.graph["objects"][name]
            for name in object_names
            if name in self.graph["objects"]
        ]

    def list_all_objects(self) -> List[Dict]:
        """Get list of all known objects."""
        return list(self.graph["objects"].values())

    def list_all_locations(self) -> List[Dict]:
        """Get list of all known locations."""
        return list(self.graph["locations"].values())

    def get_graph(self) -> Dict:
        """Get entire graph."""
        return self.graph

    def clear_graph(self) -> None:
        """Clear all data (for testing)."""
        self.graph = self._create_empty_graph()
        self._save_graph()

    def search_objects(self, query: str) -> List[Dict]:
        """Search for objects by name or description."""
        query_lower = query.lower()
        results = []

        for obj_data in self.graph["objects"].values():
            if (
                query_lower in obj_data.get("name", "").lower()
                or query_lower in obj_data.get("description", "").lower()
            ):
                results.append(obj_data)

        return results
