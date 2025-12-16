"""
Example of ingesting photos with descriptions to build semantic graph.

This demonstrates:
1. Processing photos with text descriptions
2. Merging observations into graph
3. Handling multiple observations from different devices
"""

from pathlib import Path

from semantic_memory import PhotoProcessor, SemanticGraph


def main():
    print("=== Photo Ingestion Example ===\n")

    # Initialize graph and processor
    graph = SemanticGraph()
    processor = PhotoProcessor(use_vision_model=False)  # Set to True if models installed

    print("Note: This example uses simple description-based extraction.")
    print("For real usage, set use_vision_model=True and install ML models.\n")

    # Simulate observations from different devices/times
    observations = [
        {
            "image_path": "photos/workshop_1.jpg",
            "description": "Red toolbox on the workbench with hammer and screwdriver",
            "device_id": "phone_camera_1",
            "location_hint": "main workshop",
        },
        {
            "image_path": "photos/workshop_2.jpg",
            "description": "Drill on the shelf above the workbench",
            "device_id": "phone_camera_1",
            "location_hint": "main workshop",
        },
        {
            "image_path": "photos/warehouse_1.jpg",
            "description": "Parts box on the shelf near the door",
            "device_id": "tablet_1",
            "location_hint": "parts warehouse",
        },
    ]

    print("Processing observations...")
    for i, obs_data in enumerate(observations, 1):
        print(f"\n--- Observation {i} ---")
        print(f"Device: {obs_data['device_id']}")
        print(f"Description: {obs_data['description']}")

        # Process the observation
        # Note: image_path doesn't need to exist for this demo
        observation = processor.process_photo(
            image_path=obs_data["image_path"],
            description=obs_data["description"],
            device_id=obs_data["device_id"],
            location_hint=obs_data.get("location_hint"),
        )

        if observation.processed:
            print(f"Extracted {len(observation.entities)} entities")
            print(f"Extracted {len(observation.relationships)} relationships")

            # Merge entities into graph
            for entity in observation.entities:
                merged = graph.add_entity(entity, merge_if_exists=True)
                print(f"  - Entity: {merged.name} (observations: {merged.observation_count})")

            # Add relationships
            for relationship in observation.relationships:
                graph.add_relationship(relationship, merge_if_exists=True)

        else:
            print(f"Processing failed: {observation.processing_errors}")

    # Show graph state
    print("\n=== Graph State After Ingestion ===")
    stats = graph.stats()
    print(f"Total entities: {stats['total_entities']}")
    print(f"Total relationships: {stats['total_relationships']}")
    print(f"Entities by type: {stats['entities_by_type']}")

    # List all entities
    print("\n=== All Entities ===")
    for entity_type, count in stats['entities_by_type'].items():
        entities = graph.get_entities_by_type(entity_type)
        print(f"\n{entity_type} ({count}):")
        for entity in entities:
            print(f"  - {entity.name}")
            print(f"    Observations: {entity.observation_count}")
            print(f"    Devices: {', '.join(entity.source_devices)}")
            print(f"    Confidence: {entity.confidence:.2f}")

    # Export graph
    print("\n=== Exporting Graph ===")
    export_data = graph.export_to_dict()
    print(f"Exported {len(export_data['entities'])} entities")
    print(f"Exported {len(export_data['relationships'])} relationships")

    # You could save this to a file:
    # import json
    # with open('graph_export.json', 'w') as f:
    #     json.dump(export_data, f, indent=2, default=str)

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
