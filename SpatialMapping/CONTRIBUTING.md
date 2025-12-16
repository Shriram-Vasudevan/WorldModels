# Contributing

Thank you for your interest in contributing to the Semantic Memory project.

## Development Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install in development mode:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

We use:
- **Black** for code formatting
- **isort** for import sorting
- **mypy** for type checking

Format your code before committing:
```bash
black src/ tests/
isort src/ tests/
mypy src/
```

## Testing

Run tests with pytest:
```bash
pytest tests/
```

Add tests for new features in the `tests/` directory.

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with clear commit messages
3. Add tests for new functionality
4. Ensure all tests pass
5. Format code with black and isort
6. Submit a pull request with description of changes

## Areas for Contribution

### High Priority
- **Vision integration**: Object detection, visual embeddings
- **Spatial reasoning**: Constraint satisfaction, multi-hop inference
- **Performance**: Indexing, caching, optimization
- **Tests**: Increase coverage, add integration tests

### Documentation
- Tutorial notebooks
- API documentation
- Architecture diagrams
- Use case examples

### Research
- Novel entity matching techniques
- Advanced spatial reasoning algorithms
- Vision-language integration
- Uncertainty quantification

## Questions?

Open an issue for discussion or questions about contributing.
