"""Relationships between entities in the semantic graph."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RelationType(str, Enum):
    """Types of relationships between entities."""

    # Spatial relationships (no fixed coordinates)
    ON = "on"  # A is on top of B
    IN = "in"  # A is inside/contained by B
    NEAR = "near"  # A is near B (proximity)
    NEXT_TO = "next_to"  # A is adjacent to B
    ABOVE = "above"  # A is above B (vertical)
    BELOW = "below"  # A is below B (vertical)
    LEFT_OF = "left_of"  # A is to the left of B
    RIGHT_OF = "right_of"  # A is to the right of B
    IN_FRONT_OF = "in_front_of"  # A is in front of B
    BEHIND = "behind"  # A is behind B
    ATTACHED_TO = "attached_to"  # A is physically attached to B

    # Functional relationships
    PART_OF = "part_of"  # A is a component of B
    USED_WITH = "used_with"  # A is used together with B
    OPERATES = "operates"  # A operates/controls B
    PRODUCES = "produces"  # A creates/produces B
    CONSUMES = "consumes"  # A uses/consumes B

    # Taxonomic relationships
    IS_A = "is_a"  # A is a type of B
    INSTANCE_OF = "instance_of"  # A is an instance of category B

    # Organizational relationships
    OWNED_BY = "owned_by"  # A is owned by person/org B
    ASSIGNED_TO = "assigned_to"  # A is assigned to person/location B
    STORED_IN = "stored_in"  # A is typically stored in location B

    # Temporal relationships
    BEFORE = "before"  # A happens/exists before B
    AFTER = "after"  # A happens/exists after B
    REPLACES = "replaces"  # A replaces B

    # Generic
    RELATED_TO = "related_to"  # Generic relationship


class SpatialProperties(BaseModel):
    """Properties specific to spatial relationships."""

    distance_estimate: Optional[str] = None  # "touching", "close", "medium", "far"
    distance_meters: Optional[float] = None  # Estimated distance if known
    relative_orientation: Optional[float] = None  # Angle in degrees
    elevation_difference: Optional[str] = None  # "same_level", "higher", "lower"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class Relationship(BaseModel):
    """Represents a relationship between two entities."""

    id: UUID = Field(default_factory=uuid4)
    relation_type: RelationType

    # Entities in relationship (source -> target)
    source_id: UUID  # The "subject" entity
    target_id: UUID  # The "object" entity

    # Relationship properties
    spatial: Optional[SpatialProperties] = None

    # Provenance
    first_observed: datetime = Field(default_factory=datetime.now)
    last_observed: datetime = Field(default_factory=datetime.now)
    observation_count: int = 1
    source_devices: set[str] = Field(default_factory=set)

    # Confidence
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)

    # Directional or bidirectional
    is_bidirectional: bool = False

    # Custom properties
    properties: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        use_enum_values = True

    def inverse_type(self) -> Optional[RelationType]:
        """Get the inverse relationship type if applicable."""
        inverses = {
            RelationType.ON: RelationType.BELOW,
            RelationType.BELOW: RelationType.ON,
            RelationType.ABOVE: RelationType.BELOW,
            RelationType.LEFT_OF: RelationType.RIGHT_OF,
            RelationType.RIGHT_OF: RelationType.LEFT_OF,
            RelationType.IN_FRONT_OF: RelationType.BEHIND,
            RelationType.BEHIND: RelationType.IN_FRONT_OF,
            RelationType.BEFORE: RelationType.AFTER,
            RelationType.AFTER: RelationType.BEFORE,
            RelationType.PART_OF: None,  # Not symmetric
            RelationType.IN: None,  # Not symmetric (contains is different)
        }
        return inverses.get(self.relation_type)

    def merge_observation(self, weight: float = 0.3) -> None:
        """
        Update relationship with new observation.

        Args:
            weight: Weight for the new observation (0-1)
        """
        self.last_observed = datetime.now()
        self.observation_count += 1

        # Increase confidence with more observations
        self.confidence = min(1.0, self.confidence + weight * (1 - self.confidence))

    def is_spatial(self) -> bool:
        """Check if this is a spatial relationship."""
        spatial_types = {
            RelationType.ON, RelationType.IN, RelationType.NEAR,
            RelationType.NEXT_TO, RelationType.ABOVE, RelationType.BELOW,
            RelationType.LEFT_OF, RelationType.RIGHT_OF,
            RelationType.IN_FRONT_OF, RelationType.BEHIND,
            RelationType.ATTACHED_TO
        }
        return self.relation_type in spatial_types

    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary representation."""
        return self.model_dump(mode='json')

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Relationship":
        """Create relationship from dictionary representation."""
        return cls.model_validate(data)
