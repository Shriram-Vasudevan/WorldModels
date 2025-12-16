# Examples

This directory contains example scripts demonstrating the semantic memory system.

## Running Examples

Make sure you've installed the package first:

```bash
cd ..
pip install -e .
```

## Available Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates core functionality:
- Creating entities (objects, spaces, equipment)
- Defining spatial relationships (on, in, above, near)
- Building a semantic graph
- Querying entities and relationships
- Finding spatial paths
- Getting context around entities

```bash
python basic_usage.py
```

### 2. Photo Ingestion (`photo_ingestion.py`)

Shows how to process photos with descriptions:
- Processing observations from photos
- Extracting entities and relationships from descriptions
- Merging observations from multiple devices
- Building a unified graph from distributed observations
- Exporting graph data

```bash
python photo_ingestion.py
```

**Note:** The photo ingestion example uses simple text-based extraction by default. For actual vision-based processing:

1. Install vision dependencies:
   ```bash
   pip install sentence-transformers ultralytics
   ```

2. Modify the example to use `use_vision_model=True`

3. Provide real image files

## Next Steps

After exploring the examples, you can:

1. **Extend the vision pipeline**: Integrate proper object detection, scene understanding, and visual grounding

2. **Add spatial reasoning**: Implement constraint satisfaction and multi-hop spatial inference

3. **Build query interfaces**: Create natural language query capabilities

4. **Scale the graph**: Add persistence, distributed graph storage, and incremental updates

5. **Deploy for real use cases**: Integrate with cameras, mobile devices, or robotic systems
