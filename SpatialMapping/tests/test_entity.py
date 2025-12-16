"""Tests for Entity class."""

import pytest

from semantic_memory.core.entity import Entity, EntityType, SemanticAttributes


def test_entity_creation():
    """Test basic entity creation."""
    entity = Entity(
        entity_type=EntityType.OBJECT,
        name="Test Tool",
        semantic=SemanticAttributes(category="tool", function="testing"),
    )

    assert entity.name == "Test Tool"
    assert entity.entity_type == EntityType.OBJECT
    assert entity.semantic.category == "tool"
    assert entity.confidence == 0.5  # Default


def test_entity_matching():
    """Test entity matching logic."""
    entity1 = Entity(
        entity_type=EntityType.OBJECT,
        name="Hammer",
        confidence=0.8,
    )

    entity2 = Entity(
        entity_type=EntityType.OBJECT,
        name="Hammer",
        confidence=0.7,
    )

    # Same name should match
    assert entity1.matches(entity2)


def test_entity_merge():
    """Test merging entity observations."""
    entity1 = Entity(
        entity_type=EntityType.OBJECT,
        name="Tool",
        confidence=0.5,
    )
    entity1.semantic.tags = {"red", "metal"}

    entity2 = Entity(
        entity_type=EntityType.OBJECT,
        name="Tool",
        confidence=0.8,
    )
    entity2.semantic.tags = {"heavy"}

    initial_count = entity1.observation_count
    entity1.merge_observation(entity2)

    # Observation count should increase
    assert entity1.observation_count == initial_count + 1

    # Tags should be merged
    assert "red" in entity1.semantic.tags
    assert "heavy" in entity1.semantic.tags


def test_entity_serialization():
    """Test entity to/from dict conversion."""
    entity = Entity(
        entity_type=EntityType.EQUIPMENT,
        name="Test Machine",
        semantic=SemanticAttributes(category="machinery"),
    )

    # Convert to dict and back
    entity_dict = entity.to_dict()
    restored = Entity.from_dict(entity_dict)

    assert restored.name == entity.name
    assert restored.entity_type == entity.entity_type
    assert restored.semantic.category == entity.semantic.category
