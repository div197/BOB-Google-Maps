# Contributing to BOB Google Maps

Thank you for your interest in contributing to BOB Google Maps! This document provides guidelines for contributing to the project.

## Code of Conduct

Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Provide a clear description of the problem
3. Include reproduction steps
4. Add system information (OS, Python version)

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run tests (`python -m pytest tests/`)
6. Commit with clear messages
7. Push to your fork
8. Submit a pull request

### Development Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/BOB-Google-Maps.git
cd BOB-Google-Maps

# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Run tests
python -m pytest tests/
```

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

### Testing

All new features must include tests:
- Unit tests for individual functions
- Integration tests for feature interactions
- End-to-end tests for complete workflows

## Questions?

Feel free to open an issue for any questions about contributing.