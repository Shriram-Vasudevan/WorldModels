# Architecture

This document describes the technical architecture of the semantic memory system.

## Core Principles

### 1. No Fixed Coordinates

The system operates without global coordinate systems. Instead:
- **Relative positioning**: Entities are located relative to each other
- **Topological relationships**: Focus on connectivity and containment
- **Semantic anchoring**: Use meaningful landmarks instead of (x,y,z)

### 2. Multi-Device Observation Merging

Observations from any device contribute to a unified world model:
- **Entity resolution**: Match entities across observations
- **Confidence weighting**: More observations increase certainty
- **Conflict handling**: Reconcile contradictory information
- **Temporal awareness**: Track when entities were last seen

### 3. Semantic-First Representation

Prioritize meaning over geometry:
- **What it is**: Semantic category and function
- **Where it is**: Relationships to other entities
- **How it relates**: Functional and spatial connections

## System Components

### Entity (Core Data Structure)

```
Entity
├── Identity (UUID, name, type)
├── Semantic Attributes
│   ├── Category/subcategory
│   ├── Function
│   ├── Tags and aliases
│   └── Description
├── Visual Features
│   ├── Embeddings
│   ├── Color/shape descriptors
│   └── Appearance metadata
└── Provenance
    ├── Observation timestamps
    ├── Source devices
    └── Confidence scores
```

### Relationship (Edges in Graph)

Relationships encode how entities connect:

**Spatial Relationships** (coordinate-free):
- `ON`, `IN`, `NEAR`, `NEXT_TO`
- `ABOVE`, `BELOW`, `LEFT_OF`, `RIGHT_OF`
- `IN_FRONT_OF`, `BEHIND`, `ATTACHED_TO`

**Functional Relationships**:
- `PART_OF`, `USED_WITH`, `OPERATES`
- `PRODUCES`, `CONSUMES`

**Organizational Relationships**:
- `OWNED_BY`, `ASSIGNED_TO`, `STORED_IN`

Each relationship includes:
- Confidence scores
- Spatial properties (distance estimates, orientation)
- Observation provenance

### Semantic Graph

The graph is implemented using NetworkX MultiDiGraph:
- **Nodes**: Entities
- **Edges**: Relationships (multiple edges allowed between nodes)
- **Indices**: Fast lookup by type, name, and other attributes

Key operations:
- `add_entity()`: Insert or merge entities
- `add_relationship()`: Add edges with merging
- `query_spatial()`: Find related entities through spatial relationships
- `find_path()`: Navigate between entities
- `get_context()`: Retrieve surrounding environment

### Ingestion Pipeline

**Photo → Entities + Relationships**

1. **Vision Processing** (future: use CLIP, YOLO, etc.)
   - Object detection
   - Visual embeddings
   - Scene understanding

2. **Text Processing** (current: simple parsing)
   - Entity extraction from descriptions
   - Relationship inference
   - Semantic tagging

3. **Observation Creation**
   - Bundle entities and relationships
   - Attach provenance metadata
   - Assign confidence scores

4. **Graph Merging**
   - Match new entities with existing
   - Update or create nodes/edges
   - Resolve conflicts

## Design Decisions

### Why NetworkX?

- Mature graph library with rich algorithms
- Supports multi-edges (multiple relationships between same entities)
- Fast querying with proper indexing
- Easy serialization

**Future**: Could migrate to graph databases (Neo4j, TigerGraph) for scale.

### Why Pydantic?

- Type safety and validation
- Easy serialization to/from dict
- Clear schema definitions
- Good developer experience

### Entity Matching Strategy

Matching entities across observations uses multiple signals:

1. **Name matching**: Exact and fuzzy
2. **Visual similarity**: Embedding cosine distance
3. **Type compatibility**: Must be same or unknown
4. **Semantic overlap**: Shared tags and attributes
5. **Spatial context**: Unlikely for same entity to be in multiple locations

Threshold-based matching prevents incorrect merges.

### Confidence Management

Confidence increases with:
- Multiple consistent observations
- High-quality visual features
- Clear semantic descriptions
- Multiple source devices

Confidence decreases with:
- Conflicting observations
- Low-quality inputs
- Contradictory relationships

## Scaling Considerations

### Current Implementation (Prototype)

- In-memory graph
- Single-device processing
- Simple entity matching
- Basic text parsing

### Production Scale

**Graph Storage**:
- Distributed graph database
- Sharding by spatial locality
- Persistent storage with caching

**Vision Processing**:
- GPU-accelerated model inference
- Batch processing
- Asynchronous ingestion pipeline
- Model serving infrastructure

**Entity Resolution**:
- Approximate nearest neighbor search (FAISS, Annoy)
- Hierarchical clustering
- Active learning for ambiguous cases

**Query Optimization**:
- Spatial indexing (R-trees, grid-based)
- Caching frequent queries
- Materialized views for common patterns

## Extension Points

### 1. Vision Models

Replace `PhotoProcessor._extract_with_models()` with:
- Object detection (YOLO, Detectron2)
- Visual grounding (GLIP, OWL-ViT)
- Scene graph generation
- Depth estimation for spatial relationships

### 2. Spatial Reasoning

Add `semantic_memory/spatial/`:
- Constraint satisfaction for layout inference
- Probabilistic spatial models
- Multi-hop path reasoning
- Occlusion and visibility reasoning

### 3. Natural Language Interface

Build query layer:
- "Where is the red toolbox?" → spatial query
- "What's on the workbench?" → relationship traversal
- "Find all power tools" → semantic search

### 4. Change Detection

Track temporal evolution:
- Detect when entities move
- Monitor state changes
- Trigger notifications
- Maintain history

### 5. Multi-Robot Coordination

Enable shared world model:
- Concurrent observation merging
- Distributed task planning
- Coordination protocols

## Performance Characteristics

### Current (In-Memory, Prototype)

- **Entity insertion**: O(n) for matching
- **Relationship insertion**: O(1)
- **Spatial query**: O(k) where k = result size
- **Path finding**: O(V + E) with BFS/Dijkstra

### With Optimizations

- **Entity insertion**: O(log n) with ANN index
- **Spatial query**: O(k + log n) with spatial index
- **Path finding**: O(k log V) with A* and heuristics

## Testing Strategy

1. **Unit tests**: Core data structures (Entity, Relationship)
2. **Integration tests**: Graph operations and merging
3. **System tests**: End-to-end ingestion pipelines
4. **Benchmark tests**: Performance with large graphs

See `tests/` directory for examples.
