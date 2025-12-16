"""Entity representation for physical objects and spaces."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class EntityType(str, Enum):
    """Types of physical entities."""

    OBJECT = "object"  # Physical objects (tools, parts, products)
    SPACE = "space"  # Physical spaces (rooms, zones, areas)
    LANDMARK = "landmark"  # Reference points (doors, corners, fixtures)
    PERSON = "person"  # People in the environment
    MATERIAL = "material"  # Raw materials, supplies
    EQUIPMENT = "equipment"  # Machines, vehicles
    CONTAINER = "container"  # Boxes, shelves, bins
    SURFACE = "surface"  # Tables, floors, walls
    UNKNOWN = "unknown"  # Unclassified entities


class VisualFeatures(BaseModel):
    """Visual appearance features for entity matching."""

    embedding: Optional[List[float]] = None  # Visual embedding vector
    color_histogram: Optional[List[float]] = None
    dominant_colors: List[str] = Field(default_factory=list)
    size_estimate: Optional[str] = None  # "small", "medium", "large"
    shape_descriptor: Optional[str] = None
    texture_features: Optional[List[float]] = None


class SemanticAttributes(BaseModel):
    """Semantic properties of an entity."""

    category: Optional[str] = None  # High-level category
    subcategory: Optional[str] = None
    function: Optional[str] = None  # What it's used for
    material_composition: List[str] = Field(default_factory=list)
    brand: Optional[str] = None
    model: Optional[str] = None
    tags: Set[str] = Field(default_factory=set)
    description: Optional[str] = None
    aliases: List[str] = Field(default_factory=list)  # Alternative names


class Entity(BaseModel):
    """Represents a physical entity in the world."""

    id: UUID = Field(default_factory=uuid4)
    entity_type: EntityType
    name: str

    # Semantic information
    semantic: SemanticAttributes = Field(default_factory=SemanticAttributes)

    # Visual features
    visual: VisualFeatures = Field(default_factory=VisualFeatures)

    # Provenance
    first_observed: datetime = Field(default_factory=datetime.now)
    last_observed: datetime = Field(default_factory=datetime.now)
    observation_count: int = 1
    source_devices: Set[str] = Field(default_factory=set)

    # Confidence and uncertainty
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Custom properties
    properties: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True

    def merge_observation(self, other: "Entity", weight: float = 0.3) -> None:
        """
        Merge information from another observation of this entity.

        Args:
            other: Another entity observation to merge
            weight: Weight for the new observation (0-1)
        """
        self.last_observed = datetime.now()
        self.observation_count += 1

        # Merge semantic tags and aliases
        if other.semantic.tags:
            self.semantic.tags.update(other.semantic.tags)
        if other.semantic.aliases:
            self.semantic.aliases.extend(other.semantic.aliases)

        # Update confidence with weighted average
        self.confidence = (1 - weight) * self.confidence + weight * other.confidence

        # Merge source devices
        self.source_devices.update(other.source_devices)

        # Merge custom properties (new values override)
        self.properties.update(other.properties)

        # Update semantic fields if more confident
        if other.confidence > self.confidence:
            if other.semantic.category:
                self.semantic.category = other.semantic.category
            if other.semantic.function:
                self.semantic.function = other.semantic.function

    def matches(self, other: "Entity", threshold: float = 0.7) -> bool:
        """
        Determine if this entity likely represents the same physical object.

        Args:
            other: Another entity to compare
            threshold: Similarity threshold (0-1)

        Returns:
            True if entities likely match
        """
        # Type mismatch is strong negative signal
        if self.entity_type != other.entity_type and \
           self.entity_type != EntityType.UNKNOWN and \
           other.entity_type != EntityType.UNKNOWN:
            return False

        # Name similarity
        name_match = self.name.lower() == other.name.lower()
        if name_match:
            return True

        # Check aliases
        all_names_self = {self.name.lower()} | {a.lower() for a in self.semantic.aliases}
        all_names_other = {other.name.lower()} | {a.lower() for a in other.semantic.aliases}
        if all_names_self & all_names_other:
            return True

        # Visual similarity (if embeddings available)
        if self.visual.embedding and other.visual.embedding:
            similarity = self._cosine_similarity(self.visual.embedding, other.visual.embedding)
            if similarity > threshold:
                return True

        # Semantic tag overlap
        if self.semantic.tags and other.semantic.tags:
            tag_overlap = len(self.semantic.tags & other.semantic.tags)
            tag_union = len(self.semantic.tags | other.semantic.tags)
            if tag_union > 0 and tag_overlap / tag_union > 0.5:
                return True

        return False

    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2):
            return 0.0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = sum(a * a for a in vec1) ** 0.5
        norm2 = sum(b * b for b in vec2) ** 0.5

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary representation."""
        return self.model_dump(mode='json')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Entity":
        """Create entity from dictionary representation."""
        return cls.model_validate(data)
