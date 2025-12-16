"""Observation data structure for ingesting new information."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from semantic_memory.core.entity import Entity
from semantic_memory.core.relationship import Relationship


class Observation(BaseModel):
    """
    Represents a single observation from a device.

    An observation bundles entities and relationships detected
    from a photo, description, or other input modality.
    """

    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)

    # Source information
    device_id: str  # Identifier for source device
    source_type: str = "photo"  # "photo", "video", "description", "manual"

    # Observed entities and relationships
    entities: List[Entity] = Field(default_factory=list)
    relationships: List[Relationship] = Field(default_factory=list)

    # Original input data
    image_path: Optional[str] = None
    description: Optional[str] = None
    video_path: Optional[str] = None

    # Metadata
    location_hint: Optional[str] = None  # e.g., "warehouse", "shop floor"
    context: Optional[str] = None  # Additional context
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Processing metadata
    processed: bool = False
    processing_errors: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def add_entity(self, entity: Entity) -> None:
        """Add an entity to this observation."""
        entity.source_devices.add(self.device_id)
        self.entities.append(entity)

    def add_relationship(self, relationship: Relationship) -> None:
        """Add a relationship to this observation."""
        relationship.source_devices.add(self.device_id)
        self.relationships.append(relationship)

    def to_dict(self) -> Dict[str, Any]:
        """Convert observation to dictionary."""
        return self.model_dump(mode='json')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Observation":
        """Create observation from dictionary."""
        return cls.model_validate(data)
