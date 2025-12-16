"""Tests for SemanticGraph class."""

import pytest

from semantic_memory.core.entity import Entity, EntityType
from semantic_memory.core.relationship import Relationship, RelationType
from semantic_memory.graph.semantic_graph import SemanticGraph


def test_graph_creation():
    """Test basic graph creation."""
    graph = SemanticGraph()
    assert graph.stats()["total_entities"] == 0
    assert graph.stats()["total_relationships"] == 0


def test_add_entity():
    """Test adding entities to graph."""
    graph = SemanticGraph()

    entity = Entity(entity_type=EntityType.OBJECT, name="Tool")
    added = graph.add_entity(entity)

    assert added.id == entity.id
    assert graph.stats()["total_entities"] == 1


def test_add_relationship():
    """Test adding relationships between entities."""
    graph = SemanticGraph()

    entity1 = Entity(entity_type=EntityType.OBJECT, name="Tool")
    entity2 = Entity(entity_type=EntityType.SURFACE, name="Table")

    graph.add_entity(entity1)
    graph.add_entity(entity2)

    rel = Relationship(
        relation_type=RelationType.ON, source_id=entity1.id, target_id=entity2.id
    )

    graph.add_relationship(rel)

    assert graph.stats()["total_relationships"] == 1


def test_query_by_type():
    """Test querying entities by type."""
    graph = SemanticGraph()

    obj1 = Entity(entity_type=EntityType.OBJECT, name="Tool1")
    obj2 = Entity(entity_type=EntityType.OBJECT, name="Tool2")
    surface = Entity(entity_type=EntityType.SURFACE, name="Table")

    graph.add_entity(obj1)
    graph.add_entity(obj2)
    graph.add_entity(surface)

    objects = graph.get_entities_by_type(EntityType.OBJECT)
    assert len(objects) == 2

    surfaces = graph.get_entities_by_type(EntityType.SURFACE)
    assert len(surfaces) == 1


def test_spatial_query():
    """Test spatial relationship queries."""
    graph = SemanticGraph()

    table = Entity(entity_type=EntityType.SURFACE, name="Table")
    tool = Entity(entity_type=EntityType.OBJECT, name="Tool")

    graph.add_entity(table)
    graph.add_entity(tool)

    rel = Relationship(
        relation_type=RelationType.ON, source_id=tool.id, target_id=table.id
    )
    graph.add_relationship(rel)

    # Query what's on the table
    spatial_rels = graph.query_spatial(tool)
    assert len(spatial_rels) > 0


def test_graph_serialization():
    """Test graph export and import."""
    graph = SemanticGraph()

    entity1 = Entity(entity_type=EntityType.OBJECT, name="Tool")
    entity2 = Entity(entity_type=EntityType.SURFACE, name="Table")

    graph.add_entity(entity1)
    graph.add_entity(entity2)

    rel = Relationship(
        relation_type=RelationType.ON, source_id=entity1.id, target_id=entity2.id
    )
    graph.add_relationship(rel)

    # Export
    export_data = graph.export_to_dict()

    # Import to new graph
    new_graph = SemanticGraph.import_from_dict(export_data)

    assert new_graph.stats()["total_entities"] == 2
    assert new_graph.stats()["total_relationships"] == 1
