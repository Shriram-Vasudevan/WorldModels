"""
Basic usage example for semantic memory system.

This demonstrates:
1. Creating entities and relationships
2. Building a semantic graph
3. Querying spatial relationships
4. Finding paths between entities
"""

from semantic_memory import (
    Entity,
    EntityType,
    Relationship,
    RelationType,
    SemanticGraph,
)
from semantic_memory.core.entity import SemanticAttributes
from semantic_memory.core.relationship import SpatialProperties


def main():
    print("=== Semantic Memory System - Basic Usage ===\n")

    # Initialize the semantic graph
    graph = SemanticGraph()

    # Create entities for a workshop environment
    print("Creating entities...")

    workbench = Entity(
        entity_type=EntityType.SURFACE,
        name="Main Workbench",
        semantic=SemanticAttributes(
            category="furniture",
            function="work surface",
            description="Large wooden workbench in center of shop",
        ),
        confidence=0.9,
    )

    toolbox = Entity(
        entity_type=EntityType.CONTAINER,
        name="Red Toolbox",
        semantic=SemanticAttributes(
            category="storage",
            function="tool storage",
            tags={"metal", "red", "portable"},
        ),
        confidence=0.85,
    )

    hammer = Entity(
        entity_type=EntityType.OBJECT,
        name="Hammer",
        semantic=SemanticAttributes(
            category="tool",
            subcategory="hand tool",
            function="driving nails",
        ),
        confidence=0.95,
    )

    drill = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Cordless Drill",
        semantic=SemanticAttributes(
            category="power tool",
            function="drilling and driving",
            brand="DeWalt",
        ),
        confidence=0.9,
    )

    shelf = Entity(
        entity_type=EntityType.SURFACE,
        name="Wall Shelf",
        semantic=SemanticAttributes(
            category="storage",
            function="elevated storage",
        ),
        confidence=0.8,
    )

    # Add entities to graph
    print("Adding entities to graph...")
    graph.add_entity(workbench)
    graph.add_entity(toolbox)
    graph.add_entity(hammer)
    graph.add_entity(drill)
    graph.add_entity(shelf)

    # Create spatial relationships
    print("Creating spatial relationships...")

    # Toolbox is on the workbench
    rel1 = Relationship(
        relation_type=RelationType.ON,
        source_id=toolbox.id,
        target_id=workbench.id,
        spatial=SpatialProperties(
            distance_estimate="touching",
            confidence=0.9,
        ),
        confidence=0.9,
    )

    # Hammer is in the toolbox
    rel2 = Relationship(
        relation_type=RelationType.IN,
        source_id=hammer.id,
        target_id=toolbox.id,
        spatial=SpatialProperties(
            distance_estimate="contained",
            confidence=0.95,
        ),
        confidence=0.95,
    )

    # Drill is on the shelf
    rel3 = Relationship(
        relation_type=RelationType.ON,
        source_id=drill.id,
        target_id=shelf.id,
        spatial=SpatialProperties(
            distance_estimate="touching",
            confidence=0.85,
        ),
        confidence=0.85,
    )

    # Shelf is above the workbench
    rel4 = Relationship(
        relation_type=RelationType.ABOVE,
        source_id=shelf.id,
        target_id=workbench.id,
        spatial=SpatialProperties(
            distance_estimate="medium",
            elevation_difference="higher",
            confidence=0.8,
        ),
        confidence=0.8,
    )

    # Add relationships to graph
    graph.add_relationship(rel1)
    graph.add_relationship(rel2)
    graph.add_relationship(rel3)
    graph.add_relationship(rel4)

    print("\n=== Graph Statistics ===")
    stats = graph.stats()
    print(f"Total entities: {stats['total_entities']}")
    print(f"Total relationships: {stats['total_relationships']}")
    print(f"Spatial relationships: {stats['spatial_relationships']}")
    print(f"Entities by type: {stats['entities_by_type']}")

    # Query examples
    print("\n=== Query Examples ===")

    # Find all tools
    print("\n1. Finding all objects:")
    objects = graph.get_entities_by_type(EntityType.OBJECT)
    for obj in objects:
        print(f"   - {obj.name} ({obj.semantic.category})")

    # Find what's on the workbench
    print("\n2. What's on the workbench?")
    on_workbench = graph.get_relationships(
        target_id=workbench.id, relation_type=RelationType.ON
    )
    for rel in on_workbench:
        entity = graph.get_entity(rel.source_id)
        print(f"   - {entity.name}")

    # Get context around the hammer
    print("\n3. Context around the hammer:")
    context = graph.get_context(hammer, radius=2)
    print(f"   Container: {context['container'].name if context['container'] else 'None'}")
    print(f"   Spatial neighbors: {len(context['spatial_neighbors'])}")

    # Find path from hammer to drill
    print("\n4. Finding spatial path from hammer to drill:")
    path = graph.find_path(hammer, drill)
    if path:
        path_names = " -> ".join([e.name for e in path])
        print(f"   Path: {path_names}")
    else:
        print("   No path found")

    # Search by name
    print("\n5. Search for 'toolbox':")
    results = graph.get_entities_by_name("toolbox", fuzzy=True)
    for entity in results:
        print(f"   - {entity.name} (type: {entity.entity_type})")

    # Query spatial relationships from toolbox
    print("\n6. Spatial relationships from toolbox:")
    spatial_rels = graph.query_spatial(toolbox, max_hops=1)
    for entity, rel in spatial_rels:
        print(f"   - {rel.relation_type.value} {entity.name}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
