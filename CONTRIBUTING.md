# Contributing to UE5 Semantic Asset Organizer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

Be respectful, constructive, and professional in all interactions.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/yourusername/ue5_semantic_automation/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Unreal Engine version
   - Python version
   - Error messages/logs

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear use case
   - Expected behavior
   - Why this would be useful
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Commit with clear messages: `git commit -m 'Add amazing feature'`
7. Push to your fork: `git push origin feature/amazing-feature`
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/ue5_semantic_automation.git

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/
```

## Coding Standards

- Follow PEP 8 style guide
- Use type hints where possible
- Add docstrings to all functions/classes
- Keep functions focused and single-purpose
- Write unit tests for new features

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

## Documentation

- Update README.md if adding features
- Add docstrings to new functions
- Update USAGE.md with examples
- Keep API.md current

## Commit Messages

- Use present tense: "Add feature" not "Added feature"
- Be descriptive but concise
- Reference issues: "Fix #123: Resolve texture validation bug"

## Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing!
