"""Core semantic graph for storing and querying physical world knowledge."""

from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID

import networkx as nx

from semantic_memory.core.entity import Entity, EntityType
from semantic_memory.core.relationship import Relationship, RelationType


class SemanticGraph:
    """
    Graph-based semantic memory for physical world entities and relationships.

    This graph stores entities as nodes and relationships as edges, supporting
    queries, merging, and updates without requiring global coordinates.
    """

    def __init__(self):
        """Initialize an empty semantic graph."""
        self.graph = nx.MultiDiGraph()  # Supports multiple edges between nodes
        self._entity_index: Dict[UUID, Entity] = {}
        self._relationship_index: Dict[UUID, Relationship] = {}

        # Secondary indices for fast lookup
        self._entities_by_type: Dict[EntityType, Set[UUID]] = {}
        self._entities_by_name: Dict[str, Set[UUID]] = {}

    def add_entity(self, entity: Entity, merge_if_exists: bool = True) -> Entity:
        """
        Add an entity to the graph.

        Args:
            entity: Entity to add
            merge_if_exists: If True, merge with existing similar entities

        Returns:
            The entity (potentially merged with existing)
        """
        if merge_if_exists:
            # Try to find matching entity
            existing = self._find_matching_entity(entity)
            if existing:
                existing.merge_observation(entity)
                self._update_entity_indices(existing)
                return existing

        # Add new entity
        self.graph.add_node(entity.id, entity=entity)
        self._entity_index[entity.id] = entity

        # Update indices
        self._update_entity_indices(entity)

        return entity

    def add_relationship(
        self,
        relationship: Relationship,
        merge_if_exists: bool = True
    ) -> Relationship:
        """
        Add a relationship between entities.

        Args:
            relationship: Relationship to add
            merge_if_exists: If True, update existing similar relationship

        Returns:
            The relationship (potentially merged)
        """
        # Verify entities exist
        if relationship.source_id not in self._entity_index:
            raise ValueError(f"Source entity {relationship.source_id} not found")
        if relationship.target_id not in self._entity_index:
            raise ValueError(f"Target entity {relationship.target_id} not found")

        # Check for existing relationship
        if merge_if_exists:
            existing = self._find_existing_relationship(relationship)
            if existing:
                existing.merge_observation()
                return existing

        # Add new relationship
        self.graph.add_edge(
            relationship.source_id,
            relationship.target_id,
            key=relationship.id,
            relationship=relationship
        )
        self._relationship_index[relationship.id] = relationship

        return relationship

    def get_entity(self, entity_id: UUID) -> Optional[Entity]:
        """Get entity by ID."""
        return self._entity_index.get(entity_id)

    def get_entities_by_type(self, entity_type: EntityType) -> List[Entity]:
        """Get all entities of a specific type."""
        entity_ids = self._entities_by_type.get(entity_type, set())
        return [self._entity_index[eid] for eid in entity_ids]

    def get_entities_by_name(self, name: str, fuzzy: bool = False) -> List[Entity]:
        """
        Get entities by name.

        Args:
            name: Entity name to search for
            fuzzy: If True, match substrings and aliases

        Returns:
            List of matching entities
        """
        name_lower = name.lower()

        if not fuzzy:
            entity_ids = self._entities_by_name.get(name_lower, set())
            return [self._entity_index[eid] for eid in entity_ids]

        # Fuzzy matching
        matches = []
        for entity in self._entity_index.values():
            if name_lower in entity.name.lower():
                matches.append(entity)
            elif any(name_lower in alias.lower() for alias in entity.semantic.aliases):
                matches.append(entity)

        return matches

    def get_relationships(
        self,
        source_id: Optional[UUID] = None,
        target_id: Optional[UUID] = None,
        relation_type: Optional[RelationType] = None
    ) -> List[Relationship]:
        """
        Get relationships matching criteria.

        Args:
            source_id: Filter by source entity
            target_id: Filter by target entity
            relation_type: Filter by relationship type

        Returns:
            List of matching relationships
        """
        relationships = []

        if source_id and target_id:
            # Get specific edges
            if self.graph.has_edge(source_id, target_id):
                edge_data = self.graph.get_edge_data(source_id, target_id)
                for rel in edge_data.values():
                    relationships.append(rel['relationship'])
        elif source_id:
            # Get all outgoing edges from source
            for _, _, data in self.graph.out_edges(source_id, data=True):
                relationships.append(data['relationship'])
        elif target_id:
            # Get all incoming edges to target
            for _, _, data in self.graph.in_edges(target_id, data=True):
                relationships.append(data['relationship'])
        else:
            # Get all relationships
            relationships = list(self._relationship_index.values())

        # Filter by type
        if relation_type:
            relationships = [r for r in relationships if r.relation_type == relation_type]

        return relationships

    def query_spatial(
        self,
        entity: Entity,
        relation_type: Optional[RelationType] = None,
        max_hops: int = 1
    ) -> List[Tuple[Entity, Relationship]]:
        """
        Query spatial relationships from an entity.

        Args:
            entity: Starting entity
            relation_type: Specific relationship type to filter
            max_hops: Maximum graph distance to search

        Returns:
            List of (related_entity, relationship) tuples
        """
        results = []

        # Direct relationships (1 hop)
        for rel in self.get_relationships(source_id=entity.id):
            if relation_type and rel.relation_type != relation_type:
                continue
            if rel.is_spatial():
                target = self.get_entity(rel.target_id)
                if target:
                    results.append((target, rel))

        # Multi-hop search
        if max_hops > 1:
            visited = {entity.id}
            current_level = {entity.id}

            for _ in range(max_hops - 1):
                next_level = set()
                for eid in current_level:
                    for rel in self.get_relationships(source_id=eid):
                        if rel.target_id not in visited:
                            if relation_type is None or rel.relation_type == relation_type:
                                if rel.is_spatial():
                                    target = self.get_entity(rel.target_id)
                                    if target:
                                        results.append((target, rel))
                            next_level.add(rel.target_id)
                            visited.add(rel.target_id)
                current_level = next_level

        return results

    def find_path(
        self,
        source: Entity,
        target: Entity,
        relation_types: Optional[Set[RelationType]] = None
    ) -> Optional[List[Entity]]:
        """
        Find path between two entities through spatial relationships.

        Args:
            source: Starting entity
            target: Target entity
            relation_types: Allowed relationship types (default: all spatial)

        Returns:
            List of entities forming path, or None if no path exists
        """
        if relation_types is None:
            # Use all spatial relationship types
            relation_types = {
                RelationType.ON, RelationType.IN, RelationType.NEAR,
                RelationType.NEXT_TO, RelationType.ATTACHED_TO
            }

        # Create filtered view of graph with only allowed edges
        def edge_filter(u, v, key):
            rel = self.graph.edges[u, v, key]['relationship']
            return rel.relation_type in relation_types

        filtered_graph = nx.subgraph_view(self.graph, filter_edge=edge_filter)

        try:
            path_ids = nx.shortest_path(filtered_graph, source.id, target.id)
            return [self.get_entity(eid) for eid in path_ids]
        except nx.NetworkXNoPath:
            return None

    def get_context(self, entity: Entity, radius: int = 2) -> Dict[str, Any]:
        """
        Get contextual information around an entity.

        Args:
            entity: Entity to get context for
            radius: Graph distance to include

        Returns:
            Dictionary with context information
        """
        context = {
            "entity": entity,
            "spatial_neighbors": [],
            "container": None,
            "contents": [],
            "nearby": []
        }

        # Get spatial relationships
        for rel in self.get_relationships(source_id=entity.id):
            if not rel.is_spatial():
                continue

            target = self.get_entity(rel.target_id)
            if not target:
                continue

            if rel.relation_type == RelationType.IN:
                context["container"] = target
            elif rel.relation_type == RelationType.NEAR:
                context["nearby"].append(target)

        # Get incoming containment (what's inside this entity)
        for rel in self.get_relationships(target_id=entity.id):
            if rel.relation_type == RelationType.IN:
                source = self.get_entity(rel.source_id)
                if source:
                    context["contents"].append(source)

        # Get all spatial neighbors
        spatial_results = self.query_spatial(entity, max_hops=radius)
        context["spatial_neighbors"] = spatial_results

        return context

    def _find_matching_entity(self, entity: Entity) -> Optional[Entity]:
        """Find existing entity that matches the given entity."""
        # Check by name first
        candidates = self.get_entities_by_name(entity.name)

        for candidate in candidates:
            if candidate.matches(entity):
                return candidate

        # Check by visual similarity if available
        if entity.visual.embedding:
            for existing in self._entity_index.values():
                if existing.entity_type == entity.entity_type:
                    if existing.matches(entity):
                        return existing

        return None

    def _find_existing_relationship(self, rel: Relationship) -> Optional[Relationship]:
        """Find existing relationship matching the given one."""
        existing_rels = self.get_relationships(
            source_id=rel.source_id,
            target_id=rel.target_id,
            relation_type=rel.relation_type
        )
        return existing_rels[0] if existing_rels else None

    def _update_entity_indices(self, entity: Entity) -> None:
        """Update secondary indices for an entity."""
        # Type index
        if entity.entity_type not in self._entities_by_type:
            self._entities_by_type[entity.entity_type] = set()
        self._entities_by_type[entity.entity_type].add(entity.id)

        # Name index
        name_lower = entity.name.lower()
        if name_lower not in self._entities_by_name:
            self._entities_by_name[name_lower] = set()
        self._entities_by_name[name_lower].add(entity.id)

    def stats(self) -> Dict[str, Any]:
        """Get graph statistics."""
        return {
            "total_entities": len(self._entity_index),
            "total_relationships": len(self._relationship_index),
            "entities_by_type": {
                entity_type.value: len(entities)
                for entity_type, entities in self._entities_by_type.items()
            },
            "spatial_relationships": sum(
                1 for r in self._relationship_index.values() if r.is_spatial()
            ),
            "graph_density": nx.density(self.graph),
        }

    def export_to_dict(self) -> Dict[str, Any]:
        """Export entire graph to dictionary."""
        return {
            "entities": [e.to_dict() for e in self._entity_index.values()],
            "relationships": [r.to_dict() for r in self._relationship_index.values()],
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "stats": self.stats()
            }
        }

    @classmethod
    def import_from_dict(cls, data: Dict[str, Any]) -> "SemanticGraph":
        """Import graph from dictionary."""
        graph = cls()

        # Import entities
        for entity_data in data.get("entities", []):
            entity = Entity.from_dict(entity_data)
            graph.add_entity(entity, merge_if_exists=False)

        # Import relationships
        for rel_data in data.get("relationships", []):
            relationship = Relationship.from_dict(rel_data)
            graph.add_relationship(relationship, merge_if_exists=False)

        return graph
