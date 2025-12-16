# Semantic Memory Layer for the Physical World

A universal semantic memory system that knows what things are, where they are, and how they relate across any environment—without requiring sensors, static maps, or digital twins.

## Vision

This project builds the missing infrastructure layer for AI that operates in the physical world. It creates a semantic graph that:

- **Builds itself from photos and descriptions** - No manual mapping or scanning required
- **Merges observations from any device** - Phone cameras, drones, wearables—all contribute to a unified world model
- **Works without fixed coordinates** - Uses relative spatial relationships and semantic context
- **Updates continuously** - Adapts as the physical world changes
- **Enables computable physical operations** - AI can guide work, verify steps, react to changes, and coordinate tasks

## Core Philosophy

**Make physical operations computable.** AI systems need a shared, persistent world model to operate in human environments. This system provides that foundation.

## Architecture

### Semantic Graph Core
- **Nodes**: Physical entities (objects, spaces, landmarks) with semantic attributes
- **Edges**: Spatial, functional, and semantic relationships
- **No global coordinates**: Operates on relative positioning and contextual relationships
- **Multi-modal grounding**: Links visual, linguistic, and spatial information

### Key Components

1. **Vision Ingestion Pipeline**
   - Photo processing and scene understanding
   - Object detection and semantic segmentation
   - Visual feature extraction for entity matching

2. **Graph Construction & Merging**
   - Entity resolution across observations
   - Relationship inference from spatial and semantic cues
   - Confidence-weighted graph updates
   - Conflict resolution for contradictory observations

3. **Spatial Reasoning**
   - Relative positioning without fixed frames
   - Topological relationships (containment, adjacency, paths)
   - Scale and orientation inference
   - Multi-device observation alignment

4. **Query & Operations Interface**
   - Natural language queries about physical state
   - Task verification ("is the tool on the workbench?")
   - Change detection and notifications
   - Spatial guidance for operations

## Technical Approach

### Input Modalities
- Images/photos from any camera source
- Text descriptions (natural language)
- Optional: video streams, depth data (but not required)

### Graph Representation
- Entities: Typed nodes with semantic properties
- Relationships: Spatial, functional, taxonomic
- Provenance: Track observation sources and timestamps
- Uncertainty: Confidence scores and probabilistic reasoning

### Merging Strategy
- Entity matching via visual + semantic similarity
- Spatial constraint satisfaction
- Bayesian updates for conflicting information
- Temporal awareness for change detection

## Use Cases

- **Manufacturing & Assembly**: Guide workers through complex procedures
- **Warehouse Operations**: Locate items without fixed infrastructure
- **Field Operations**: Track equipment and materials across job sites
- **Healthcare**: Monitor medical supply locations and usage
- **Retail**: Understand product placement and inventory
- **Robotics**: Shared world model for multi-robot coordination

## Getting Started

```bash
# Install dependencies
pip install -e .

# Run example ingestion
python examples/basic_ingestion.py

# Query the graph
python examples/query_graph.py
```

## Status

🚧 **Early Development** - Core architecture and proof of concept

## Philosophy

This is about making the physical world legible to AI systems. Not through expensive sensor networks or manual digital twin creation, but through the same way humans build mental models: observation, description, and continuous updates.

The goal is infrastructure, not a product. A foundational layer that enables a new class of AI applications in physical space.
