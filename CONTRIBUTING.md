# Contributing to BOB Google Maps V3.0

First off, thank you for considering contributing to BOB! 🙏

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported
2. Create a new issue with:
   - Clear title
   - Detailed description
   - Steps to reproduce
   - Expected vs actual behavior
   - System info (OS, Python version, etc.)

### Suggesting Features

1. Check existing feature requests
2. Create an issue describing:
   - The feature
   - Why it's needed
   - Possible implementation

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests
5. Ensure tests pass (`pytest tests/`)
6. Commit with clear messages
7. Push to your fork
8. Create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/BOB-Google-Maps.git
cd BOB-Google-Maps

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Install Playwright
python3 -m playwright install chromium

# Run tests
pytest tests/
```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings
- Run `black` for formatting
- Run `flake8` for linting

## Testing

- Write tests for new features
- Ensure all tests pass
- Maintain test coverage above 80%

## Thank You!

**Author:** Divyanshu Singh Chouhan
**Project:** BOB Google Maps V3.0
