# Contributing to TinyPixels

Thanks for your interest in contributing! This is a young project and we welcome all contributions.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/nafasebra/tinypixels`
3. Create a branch: `git checkout -b feature/your-feature-name`

## Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-mock pytest-cov
```

## Running Tests

```
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src/tinypixels
```

## Making Changes

1. Write your code
2. Add tests for new features
3. Make sure all tests pass
4. Commit with clear messages and use git conventions
5. Push and open a Pull Request

## Code Style

- Follow PEP 8
- Keep functions focused and simple
- Add docstrings for public functions
- Write tests for new features

## Questions?

Open an issue or start a discussion. This project is still evolving, so your feedback matters!
