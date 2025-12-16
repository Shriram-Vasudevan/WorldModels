# Quick Start Guide

Get up and running with the Semantic Memory system in 5 minutes.

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package
pip install -e .
```

## Run Your First Example

```bash
# Run basic usage example
python examples/basic_usage.py
```

This will:
1. Create a semantic graph of a workshop environment
2. Add entities (workbench, tools, storage)
3. Define spatial relationships (on, in, near, above)
4. Run queries to find objects and paths

**Expected output:**
```
=== Graph Statistics ===
Total entities: 5
Total relationships: 4
Spatial relationships: 4

=== Query Examples ===
1. Finding all objects:
   - Hammer (tool)

2. What's on the workbench?
   - Red Toolbox
...
```

## Build Your Own Graph

```python
from semantic_memory import Entity, EntityType, Relationship, RelationType, SemanticGraph

# Create graph
graph = SemanticGraph()

# Add entities
table = Entity(
    entity_type=EntityType.SURFACE,
    name="Desk",
)
laptop = Entity(
    entity_type=EntityType.EQUIPMENT,
    name="Laptop",
)

graph.add_entity(table)
graph.add_entity(laptop)

# Add relationship
rel = Relationship(
    relation_type=RelationType.ON,
    source_id=laptop.id,
    target_id=table.id,
)
graph.add_relationship(rel)

# Query
print(f"Total entities: {graph.stats()['total_entities']}")
```

## Process Photos (Demo)

```bash
python examples/photo_ingestion.py
```

This demonstrates:
- Processing observations with text descriptions
- Extracting entities from descriptions
- Merging observations into a unified graph
- Handling multiple data sources

**Note:** For actual vision processing, you'll need to:
1. Install vision models: `pip install sentence-transformers ultralytics`
2. Set `use_vision_model=True` in PhotoProcessor
3. Provide real image files

## Next Steps

### 1. Explore the Core Concepts

Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) to understand:
- Entity and relationship models
- Graph structure and operations
- Design principles

### 2. Check the Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for:
- Current capabilities
- Planned features
- Extension points

### 3. Extend the System

Key areas to build on:

**Vision Integration:**
- Add object detection (YOLO, Detectron2)
- Implement visual embeddings (CLIP)
- Extract spatial relationships from images

**Spatial Reasoning:**
- Multi-hop relationship inference
- Constraint satisfaction
- Path planning algorithms

**Query Interface:**
- Natural language queries
- Complex spatial queries
- Real-time updates

### 4. Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# With coverage
pytest tests/ --cov=semantic_memory
```

### 5. Build an Application

Pick a use case:
- **Manufacturing**: Track tools and parts on assembly lines
- **Warehouse**: Locate items without RFID infrastructure
- **Field ops**: Monitor equipment across job sites
- **Robotics**: Shared world model for multi-robot systems

## Project Structure

```
SpatialMapping/
├── src/semantic_memory/      # Core package
│   ├── core/                 # Entity, Relationship classes
│   ├── graph/                # SemanticGraph implementation
│   ├── ingestion/            # Photo processing pipeline
│   ├── spatial/              # Spatial reasoning (future)
│   ├── vision/               # Vision models (future)
│   └── utils/                # Utilities
├── examples/                 # Example scripts
├── tests/                    # Unit tests
├── docs/                     # Documentation
├── data/                     # Data storage
└── models/                   # Model weights

```

## Common Tasks

### Export a Graph

```python
# Export to dict
data = graph.export_to_dict()

# Save to JSON
import json
with open('graph.json', 'w') as f:
    json.dump(data, f, indent=2, default=str)
```

### Load a Graph

```python
import json

with open('graph.json', 'r') as f:
    data = json.load(f)

graph = SemanticGraph.import_from_dict(data)
```

### Find Spatial Context

```python
# Get everything around an entity
context = graph.get_context(entity, radius=2)

print(f"Container: {context['container']}")
print(f"Contents: {context['contents']}")
print(f"Nearby: {context['nearby']}")
```

### Query Relationships

```python
# Find what's ON the table
relationships = graph.get_relationships(
    target_id=table.id,
    relation_type=RelationType.ON
)

for rel in relationships:
    entity = graph.get_entity(rel.source_id)
    print(f"{entity.name} is on {table.name}")
```

## Getting Help

- Read the [Architecture docs](docs/ARCHITECTURE.md)
- Check [examples/](examples/) for code samples
- See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Open an issue for bugs or questions

## Vision

This system is about making physical operations computable. The goal is to provide AI systems with a shared, persistent world model they need to operate in human environments—without expensive sensors, manual mapping, or digital twins.

Start building the missing infrastructure layer for AI that works outside software.
