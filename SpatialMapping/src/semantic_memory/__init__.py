"""
Semantic Memory Layer for the Physical World

A universal semantic memory system that builds and maintains a graph of physical
entities, their properties, and relationships from photos and descriptions.
"""

__version__ = "0.1.0"

from semantic_memory.core.entity import Entity, EntityType
from semantic_memory.core.relationship import Relationship, RelationType
from semantic_memory.graph.semantic_graph import SemanticGraph
from semantic_memory.ingestion.photo_processor import PhotoProcessor
from semantic_memory.ingestion.observation import Observation

__all__ = [
    "Entity",
    "EntityType",
    "Relationship",
    "RelationType",
    "SemanticGraph",
    "PhotoProcessor",
    "Observation",
]
